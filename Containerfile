# syntax=docker/dockerfile:1
#
# Universal documentation toolkit — project-agnostic.
# Holds everything needed to BUILD the docs (the main thrust) and to work with
# the contract pipeline. It bakes in NO project content: mount a project at
# /docs and run mkdocs against it.
#
# Portable: any host running Podman or Docker (Linux, or macOS via
# `podman machine`). No host tooling required beyond Podman + make.
#
# Build:  podman build -t localhost/project-docs-toolkit:latest -f Containerfile .
# Use:    see Makefile, compose.yaml, and TOOLKIT.md
#
# Package versions are pinned (pip, npm, and the d2/oasdiff binaries) to avoid
# surprise breaking changes — bump them deliberately; `make versions` prints what's
# installed. Base images stay on their rolling tags so they keep receiving OS
# security updates.

# Node, copied into the Python base for a clean, known major version.
FROM node:20-bookworm-slim AS node

FROM python:3.12-slim

# --- OS deps -------------------------------------------------------------
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates curl git make tar \
 && rm -rf /var/lib/apt/lists/*

# --- Node 20 (from the node stage) --------------------------------------
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -sf /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
 && ln -sf /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

# --- Docs build core (the main thrust) ----------------------------------
# mkdocs-material bundles mkdocs + the pymdownx extensions our mkdocs.yml uses.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# --- Contract / API tooling (universal extras) --------------------------
# TypeSpec (author -> OpenAPI), Prism (mock + validating proxy),
# AsyncAPI CLI (async backward-compat diff).
RUN npm install -g --no-fund --no-audit \
      @typespec/compiler@1.11.0 @typespec/http@1.11.0 @typespec/openapi3@1.11.0 \
      @stoplight/prism-cli@5.14.2 \
      @asyncapi/cli@4.1.1

# d2 (diagram rendering) and oasdiff (OpenAPI breaking-change detection), pinned
# and installed by direct release download (arch-detected: amd64 / arm64).
ARG D2_VERSION=0.7.1
ARG OASDIFF_VERSION=1.19.1
RUN set -eux; \
    arch="$(dpkg --print-architecture)"; \
    curl -fsSL "https://github.com/terrastruct/d2/releases/download/v${D2_VERSION}/d2-v${D2_VERSION}-linux-${arch}.tar.gz" -o /tmp/d2.tgz; \
    tar -C /tmp -xzf /tmp/d2.tgz; \
    install "/tmp/d2-v${D2_VERSION}/bin/d2" /usr/local/bin/d2; \
    curl -fsSL "https://github.com/oasdiff/oasdiff/releases/download/v${OASDIFF_VERSION}/oasdiff_${OASDIFF_VERSION}_linux_${arch}.tar.gz" -o /tmp/oasdiff.tgz; \
    tar -C /usr/local/bin -xzf /tmp/oasdiff.tgz oasdiff; \
    rm -rf /tmp/d2* /tmp/oasdiff*

# Schemathesis (provider conformance) — Python, kept off the docs-core layer.
RUN pip install --no-cache-dir schemathesis==4.21.6

# The repo's doc tools, baked in as `docs-check` / `docs-report` / `docs-drift`.
COPY tools/check.py /usr/local/bin/docs-check
COPY tools/report.py /usr/local/bin/docs-report
COPY tools/drift.py /usr/local/bin/docs-drift
RUN chmod +x /usr/local/bin/docs-check /usr/local/bin/docs-report /usr/local/bin/docs-drift

# mkdocs build hook: status badges + derived "Used by" backlinks. Referenced from
# mkdocs.yml as /usr/local/lib/docs/hook.py (absolute, so root and example share it).
COPY tools/mkdocs_hook.py /usr/local/lib/docs/hook.py

WORKDIR /docs
EXPOSE 8000

# A bare `run` prints what's inside and how to use it.
CMD ["bash", "-lc", "echo 'project-docs toolkit'; mkdocs --version; echo 'mount a project at /docs and run: mkdocs serve -a 0.0.0.0:8000  |  mkdocs build --strict'"]
