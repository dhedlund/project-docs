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
# Versions are intentionally unpinned for now so the first build "just works"
# against current releases. Pin them in a later convergence pass for
# reproducibility (note the resolved versions printed by `make versions`).

# Pinned Node, copied into the Python base for a clean, known version.
FROM node:20-bookworm-slim AS node

FROM python:3.12-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

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
      @typespec/compiler @typespec/http @typespec/openapi3 \
      @stoplight/prism-cli \
      @asyncapi/cli

# d2 (diagram rendering, for when the D2 plugin is wired) and
# oasdiff (OpenAPI breaking-change detection). Both install to /usr/local/bin.
RUN curl -fsSL https://d2lang.com/install.sh | sh -s -- \
 && curl -fsSL https://raw.githubusercontent.com/oasdiff/oasdiff/main/install.sh | sh

# Schemathesis (provider conformance) — Python, kept off the docs-core layer.
RUN pip install --no-cache-dir schemathesis

# The repo's doc tools, baked in as `docs-check` / `docs-report`.
COPY tools/check.py /usr/local/bin/docs-check
COPY tools/report.py /usr/local/bin/docs-report
RUN chmod +x /usr/local/bin/docs-check /usr/local/bin/docs-report

WORKDIR /docs
EXPOSE 8000

# A bare `run` prints what's inside and how to use it.
CMD ["bash", "-lc", "echo 'project-docs toolkit'; mkdocs --version; echo 'mount a project at /docs and run: mkdocs serve -a 0.0.0.0:8000  |  mkdocs build --strict'"]
