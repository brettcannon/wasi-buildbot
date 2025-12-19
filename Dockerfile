FROM ghcr.io/python/wasicontainer:latest

RUN dnf -y --nodocs --setopt=install_weak_deps=False install buildbot-worker && dnf -y clean all

# Create a dedicated user for buildbot-worker with a proper home directory
RUN useradd -m -s /bin/bash buildbot

COPY --chmod=755 entrypoint.sh /usr/local/bin/entrypoint.sh

USER buildbot

ENTRYPOINT ["entrypoint.sh"]
