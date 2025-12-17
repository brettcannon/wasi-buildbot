FROM ghcr.io/python/wasicontainer:latest

RUN dnf install -y buildbot-worker && dnf clean all

COPY --chmod=755 entrypoint.sh /usr/local/bin/entrypoint.sh

USER buildbot

ENTRYPOINT ["entrypoint.sh"]
