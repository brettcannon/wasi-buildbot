#!/usr/bin/env python3
"""Run the WASI buildbot container with Podman or Docker.

The credentials file should be in KEY=VALUE format:

    BUILDBOT_USERNAME=your_username
    BUILDBOT_PASSWORD=your_password

Create it with:

    touch wasi-buildbot.env
    chmod 600 wasi-buildbot.env
    # Then edit to add your credentials.
"""

import argparse
import os
import pathlib
import shutil
import stat
import subprocess
import sys

# If changed, also update the module docstring.
DEFAULT_CREDENTIALS_PATH = pathlib.Path("wasi-buildbot.env")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the WASI buildbot container")
    parser.add_argument(
        "--credentials",
        type=pathlib.Path,
        default=DEFAULT_CREDENTIALS_PATH,
        help=f"Path to credentials file (default: {os.fsdecode(DEFAULT_CREDENTIALS_PATH)})",
    )
    parser.add_argument(
        "--buildarea-parent",
        type=pathlib.Path,
        default=pathlib.Path.cwd(),
        help="Parent directory for buildarea/ (default: current working directory)",
    )
    parser.add_argument(
        "--container-runtime",
        choices=["podman", "docker"],
        help="Container runtime to use (default: auto-detect, preferring podman)",
    )
    args = parser.parse_args()

    # Validate credentials file exists and has secure permissions.
    if not args.credentials.exists():
        sys.exit(f"Error: credentials file not found: {args.credentials}")
    mode = args.credentials.stat().st_mode
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        sys.exit(
            f"Error: credentials file {args.credentials} must NOT be readable/writable by group or others"
        )

    script_dir = pathlib.Path(__file__).resolve().parent

    # Clean up any existing buildarea directory in the buildarea parent directory so the
    # volume mount points at the expected location regardless of where the
    # command is launched from.
    buildarea_parent = args.buildarea_parent.resolve()
    if (buildarea := buildarea_parent / "buildarea").exists():
        shutil.rmtree(buildarea)
    buildarea.mkdir()

    # Find container runtime executable.
    if args.container_runtime:
        runtime = shutil.which(args.container_runtime)
        if runtime is None:
            sys.exit(f"Error: {args.container_runtime} not found in PATH")
        runtime_name = args.container_runtime
    else:
        # Auto-detect, preferring podman.
        if (runtime := shutil.which("podman")) is not None:
            runtime_name = "podman"
        elif (runtime := shutil.which("docker")) is not None:
            runtime_name = "docker"
        else:
            sys.exit("Error: neither podman nor docker found in PATH")

    # Remove any existing image to avoid cached layers.
    subprocess.run([runtime, "rmi", "-f", "wasi-buildbot"], capture_output=True)

    # Build the container, pulling the latest base image.
    subprocess.run(
        [
            runtime,
            "build",
            "--pull",
            "--no-cache",
            "-t",
            "wasi-buildbot",
            os.fsdecode(script_dir),
        ],
        check=True,
    )

    # Prune dangling images and old base images.
    subprocess.run([runtime, "image", "prune", "-f"], capture_output=True)

    # Build the container run command.
    cmd = [
        runtime,
        "run",
        "--rm",
        "-it",
    ]
    
    # When using Podman, add --userns=keep-id so files written to the mounted
    # volume are owned by the host user rather than a mapped subuid.
    if runtime_name == "podman":
        cmd.append("--userns=keep-id")
    
    cmd.extend([
        "-v",
        f"{buildarea}:/buildarea",
        "--env-file",
        os.fsdecode(args.credentials.resolve()),
        "wasi-buildbot",
    ])

    # Replace this process with the container runtime.
    os.execv(runtime, cmd)


if __name__ == "__main__":
    main()
