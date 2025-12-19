# Agent Instructions for WASI Buildbot

## Project Overview

This repository contains the configuration and scripts for the WASI buildbot worker for CPython. It runs a containerized buildbot worker that connects to Python's buildbot infrastructure to test CPython on WASI (WebAssembly System Interface).

**Key Maintainers:** @brettcannon and @Devid-Ba

**Purpose:** Automated testing of CPython on WASI platform through Python's buildbot infrastructure.

## Technology Stack

- **Container Runtime:** Podman (not Docker)
- **Base Image:** `ghcr.io/python/wasicontainer:latest`
- **Build System:** Buildbot (buildbot-worker)
- **Language:** Python 3, Shell
- **Platform:** WASI (WebAssembly System Interface)

## Repository Structure

Key files in this repository:

```
.
├── Dockerfile          # Container definition using WASI base image
├── entrypoint.sh       # Container entrypoint, initializes and runs buildbot-worker
├── run.py              # Helper script to build and run the container with Podman
├── README.md           # User documentation
├── LICENSE             # Apache 2.0 license
├── .gitignore          # Git ignore patterns
├── AGENTS.md           # This file - instructions for AI coding agents
└── .github/
    └── FUNDING.yml     # GitHub Sponsors configuration
```

## Setup and Testing

### Prerequisites
- Podman must be installed (not Docker)
- Valid buildbot credentials

### Running the Container
- Use `./run.py` to build and run (recommended approach)
- Script handles credential validation, buildarea setup, and container lifecycle
- Credentials must be in a secure file (mode 600) with format:
  ```
  BUILDBOT_USERNAME=your_username
  BUILDBOT_PASSWORD=your_password
  ```

### Testing Changes
1. For Python code changes to `run.py`: Test with `python3 run.py --help`
2. For container changes: Build with `podman build -t wasi-buildbot .`
3. For entrypoint changes: Verify shell syntax with `shellcheck entrypoint.sh` if available

## Code Style and Best Practices

### Python Code
- Follow PEP 8 conventions
- Use type hints (as seen in `run.py`)
- Use pathlib for file paths
- Add descriptive docstrings
- Handle errors gracefully with informative error messages

### Shell Scripts
- Use POSIX-compliant shell (`#!/bin/sh`)
- Include `set -e` for fail-fast behavior
- Provide clear error messages to stderr
- Validate all required conditions before proceeding

### Container/Dockerfile
- Use official base images from ghcr.io/python/wasicontainer
- Run as non-root user (`buildbot`)
- Keep images minimal (use `--nodocs` and `--setopt=install_weak_deps=False` for dnf)
- Clean up package manager caches after installation

## Security Considerations

1. **Credentials:** Must never be committed to the repository
   - Always use separate credential files
   - Enforce secure permissions (mode 600)
   - Use `--env-file` for passing credentials to containers

2. **Container Security:**
   - Run as non-root user (buildbot)
   - Use official trusted base images
   - Keep base image updated (`--pull` flag in build)

3. **File Permissions:**
   - Credentials: mode 600 (owner read/write only)
   - Scripts: mode 755 (executable)
   - Build area: mode 777 (world-writable on the host directory, required for container user access due to UID/GID mapping between host and container; this is safe because it's a dedicated build directory that's cleaned on each run)

## Common Tasks and Guidance

### Updating Dependencies
- Base image updates: Modify `FROM` line in Dockerfile
- DNF packages: Add to `RUN dnf` command in Dockerfile
- Clean caches with `dnf -y clean all` after installations

### Modifying Container Behavior
- Worker initialization: Edit `entrypoint.sh`
- Container runtime options: Edit `run.py`
- Validation checks: Add to `entrypoint.sh` before worker start

### Improving Error Handling
- Add validation early (fail fast)
- Provide actionable error messages
- Check file permissions, existence, and environment variables
- Use exit codes appropriately (0 for success, non-zero for errors)

## What to Focus On

When making changes:
1. **Maintain backward compatibility** with existing credential files and workflows
2. **Keep changes minimal** - this is a focused, working system
3. **Test container builds** before committing Dockerfile changes
4. **Validate shell syntax** for entrypoint.sh changes
5. **Update README.md** if user-facing behavior changes
6. **Preserve security** - never weaken credential or permission checks

## What NOT to Do

- Don't switch from Podman to Docker (Podman is required for its rootless container capabilities, daemon-less architecture, and better security model with improved user namespace isolation)
- Don't commit credentials or sensitive information
- Don't remove security checks from scripts
- Don't change the base image without coordination with maintainers
- Don't add unnecessary dependencies
- Don't make the container run as root
- Don't modify buildbot connection details without maintainer approval

## Testing Your Changes

Since this is infrastructure code:
1. Verify Python scripts run without syntax errors
2. Check shell scripts with shellcheck if available
3. Test container builds successfully
4. For significant changes, coordinate with maintainers for integration testing
5. Document any manual testing steps in PR descriptions
