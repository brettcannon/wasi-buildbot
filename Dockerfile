FROM ghcr.io/python/wasicontainer:latest

RUN dnf -y --nodocs --setopt=install_weak_deps=False install buildbot-worker && dnf -y clean all

COPY --chmod=755 entrypoint.sh /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
