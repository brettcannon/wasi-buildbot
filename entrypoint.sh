#!/bin/sh
set -e

if [ ! -d /buildarea ] || [ "$(stat -c %d /buildarea)" = "$(stat -c %d /)" ]; then
    echo "Error: /buildarea must be mounted as a volume" >&2
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
