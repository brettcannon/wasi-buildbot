#!/bin/sh
set -e

# Check that /buildarea exists
if [ ! -d /buildarea ]; then
    echo "Error: /buildarea directory does not exist - it must be mounted as a volume" >&2
    exit 1
fi

# Check that /buildarea is readable
if [ ! -r /buildarea ]; then
    echo "Error: /buildarea is not readable" >&2
    exit 1
fi

# Check that /buildarea is writable
if [ ! -w /buildarea ]; then
    echo "Error: /buildarea is not writable" >&2
    exit 1
fi

# Check that /buildarea is coming from outside the container (mounted as a volume)
if ! grep -q " /buildarea " /proc/mounts; then
    echo "Error: /buildarea must be mounted as a volume from outside the container" >&2
    exit 1
fi

cd /buildarea

# Initialize the worker if not already done.
if [ ! -f buildbot.tac ]; then
    if [ -z "${BUILDBOT_USERNAME}" ] || [ -z "${BUILDBOT_PASSWORD}" ]; then
        echo "Error: BUILDBOT_USERNAME and BUILDBOT_PASSWORD must be set" >&2
        exit 1
    fi
    buildbot-worker create-worker . buildbot-api.python.org:9020 "${BUILDBOT_USERNAME}" "${BUILDBOT_PASSWORD}"
    echo "https://github.com/brettcannon/wasi-buildbot" > info/admin
    echo "WASI builder based on https://github.com/python/cpython-devcontainers/pkgs/container/wasicontainer" > info/host
fi

exec buildbot-worker start --nodaemon .
