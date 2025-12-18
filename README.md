# WASI Buildbot
Configuration details for the [WASI buildbot worker for for CPython](https://buildbot.python.org/#/workers/70) ([builder view](https://buildbot.python.org/#/builders?tags=%2Bwasi&tags=%2Bstable)).

Maintained by [@brettcannon](https://github.com/brettcannon) and [@Devid-Ba](https://github.com/Devid-Ba).

## Setup

1. Create a credentials file:

   ```bash
   touch credentials.env
   chmod 600 credentials.env
   ```

2. Edit `credentials.env` to add your Buildbot credentials:

   ```
   BUILDBOT_USERNAME=your_username
   BUILDBOT_PASSWORD=your_password
   ```

## Running

### Using the helper script (recommended)

The `run.py` script builds the container fresh (pulling the latest base image) and runs it. It supports both Podman and Docker, auto-detecting the available runtime (preferring Podman).

Basic usage:

```bash
./run.py
```

With a custom credentials file path:

```bash
./run.py --credentials /path/to/credentials.env
```

With a custom parent directory for the buildarea:

```bash
./run.py --buildarea-parent /path/to/parent
```

Explicitly choose a container runtime:

```bash
./run.py --container-runtime podman
./run.py --container-runtime docker
```

All options can be combined:

```bash
./run.py --credentials /path/to/credentials.env --buildarea-parent /path/to/parent --container-runtime podman
```

### Manual execution

Build the container (using Docker):

```bash
docker build -t wasi-buildbot .
```

Or with Podman:

```bash
podman build -t wasi-buildbot .
```

Run the container (using Docker):

```bash
docker run --rm -it \
    -v /path/to/buildarea:/buildarea \
    --env-file credentials.env \
    wasi-buildbot
```

Or with Podman (note the `--userns=keep-id` flag to ensure proper file ownership):

```bash
podman run --rm -it \
    --userns=keep-id \
    -v /path/to/buildarea:/buildarea \
    --env-file credentials.env \
    wasi-buildbot
```

With explicit environment variables (Docker):

```bash
docker run --rm -it \
    -v /path/to/buildarea:/buildarea \
    -e BUILDBOT_USERNAME=xxx \
    -e BUILDBOT_PASSWORD=xxx \
    wasi-buildbot
```

With explicit environment variables (Podman):

```bash
podman run --rm -it \
    --userns=keep-id \
    -v /path/to/buildarea:/buildarea \
    -e BUILDBOT_USERNAME=xxx \
    -e BUILDBOT_PASSWORD=xxx \
    wasi-buildbot
```
