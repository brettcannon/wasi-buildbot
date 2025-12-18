#!/usr/bin/env python3
"""Run the WASI buildbot container with podman.

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
        "credentials",
        nargs="?",
        type=pathlib.Path,
        default=DEFAULT_CREDENTIALS_PATH,
        help=f"Path to credentials file (default: {os.fsdecode(DEFAULT_CREDENTIALS_PATH)})",
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

    # Clean up any existing buildarea directory.
    if (buildarea := pathlib.Path.cwd() / "buildarea").exists():
        shutil.rmtree(buildarea)
    buildarea.mkdir()

    # Find podman executable.
    if (podman := shutil.which("podman")) is None:
        sys.exit("Error: podman not found in PATH")

    # Remove any existing image to avoid cached layers.
    subprocess.run([podman, "rmi", "-f", "wasi-buildbot"], capture_output=True)

    # Build the container, pulling the latest base image.
    script_dir = pathlib.Path(__file__).resolve().parent
    subprocess.run(
        [
            podman,
            "build",
            "--pull=always",
            "--no-cache",
            "-t",
            "wasi-buildbot",
            os.fsdecode(script_dir),
        ],
        check=True,
    )

    # Prune dangling images and old base images.
    subprocess.run([podman, "image", "prune", "-f"], capture_output=True)

    # Build the podman command.
    cmd = [
        podman,
        "run",
        "--rm",
        "-it",
        "-v",
        f"{buildarea}:/buildarea:Z",
        "--env-file",
        os.fsdecode(args.credentials.resolve()),
        "wasi-buildbot",
    ]

    # Replace this process with podman.
    os.execv(podman, cmd)


if __name__ == "__main__":
    main()
