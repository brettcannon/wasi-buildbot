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

The `run.py` script builds the container fresh (pulling the latest base image) and runs it:

```bash
./run.py
```

Or with a custom credentials file path:

```bash
./run.py --credentials /path/to/credentials.env
```

### Manual execution

Build the container:

```bash
podman build -t wasi-buildbot .
```

Run the container:

```bash
podman run --rm -it \
    -v /path/to/buildarea:/buildarea:Z \
    --env-file credentials.env \
    wasi-buildbot
```

Or with explicit environment variables:

```bash
podman run --rm -it \
    -v /path/to/buildarea:/buildarea:Z \
    -e BUILDBOT_USERNAME=xxx \
    -e BUILDBOT_PASSWORD=xxx \
    wasi-buildbot
```
