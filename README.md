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

With a custom credentials file path:

```bash
./run.py --credentials /path/to/credentials.env
```

With a custom parent directory for the buildarea:

```bash
./run.py --buildarea-parent /path/to/parent
```

Both options can be combined:

```bash
./run.py --credentials /path/to/credentials.env --buildarea-parent /path/to/parent
```

### Manual execution

Build the container:

```bash
docker build -t wasi-buildbot .
```

Run the container:

```bash
docker run --rm -it \
    -v /path/to/buildarea:/buildarea \
    --env-file credentials.env \
    wasi-buildbot
```

Or with explicit environment variables:

```bash
docker run --rm -it \
    -v /path/to/buildarea:/buildarea \
    -e BUILDBOT_USERNAME=xxx \
    -e BUILDBOT_PASSWORD=xxx \
    wasi-buildbot
```
