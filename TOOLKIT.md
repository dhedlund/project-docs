# Toolkit container

Everything needed to build these docs runs inside one portable container image —
`localhost/project-docs-toolkit`. It runs on **Podman or Docker**, the same on
Linux and macOS, needs no host tooling beyond a container engine + `make`, and
bakes in no project content (you mount a project at `/docs`). The same image is
reused by the [`example/`](example/) project.

## Prerequisites

A container engine — **Podman or Docker** — plus **make** (preinstalled on macOS
and most Linux). Nothing else: no Python, Node, or doc tooling on the host.

- **Podman** — Linux: your package manager. macOS: Podman Desktop, then
  `podman machine init && podman machine start`.
- **Docker** — Linux: Docker Engine. macOS: Docker Desktop.

The `make` targets **auto-detect** the engine (Podman preferred); force one with
`make build ENGINE=docker`.

## Build the docs (the main thrust — "just works")

From the repo root:

```bash
make build      # static site -> ./site  (offline, --strict)
make serve      # live preview at http://localhost:8000
make versions   # show the resolved tool versions
```

`make build` runs with `--network none` (building docs needs no network) and the
container drops all Linux capabilities. First run builds the image (a few
minutes); after that it's cached.

> **Preview over HTTP, not `file://`.** Use `make serve`. If you open the built
> `site/` files directly (`file://`), client-rendered diagrams (Mermaid) stay as
> plain text — the browser blocks loading Mermaid's module over `file://`. Served
> over HTTP they render fine. D2 is baked in at build time and shows either way.

The [`example/`](example/) project has the same targets (preview on port 8001),
which is the quickest way to confirm your setup works end-to-end:

```bash
cd example && make build && make serve
```

## What's in the image

| Tool | Purpose |
|------|---------|
| `mkdocs` + Material | build/serve the docs site (the core) |
| `d2` | render fenced `d2` "hero" diagrams to SVG (light + dark variants) |
| `tsp` (TypeSpec) | author API contracts → compile to OpenAPI |
| `oasdiff` | detect breaking changes between OpenAPI versions |
| `schemathesis` | property-based provider conformance against a spec |
| `prism` | mock server + **validating proxy** |
| `asyncapi` | AsyncAPI tooling incl. backward-compat `diff` |

Mermaid needs no tooling — it renders client-side in the browser.

## Interacting with a live service stack (contracts & proxying)

Building docs is self-contained and offline. **Verifying contracts against real
services is different**: those commands need network access to the stack and are
deliberately *not* part of the default build. Run them from a toolkit shell, and
grant only the network the task needs.

```bash
make shell      # toolkit shell with tsp / oasdiff / schemathesis / prism
```

Capabilities and what they look like in practice:

- **Author → OpenAPI.** A TypeSpec contract is a small project (it pins its libs in
  `package.json`): `cd contracts/<svc> && npm install && tsp compile main.tsp` →
  the OpenAPI artifact the rest of the tools consume. (The file-based tools below
  need no project — they read the spec directly.)
- **Backward-compat gate (offline).** `oasdiff breaking old.yaml new.yaml --fail-on ERR`
  — pure spec-vs-spec; no stack needed. Safe in CI.
- **Provider conformance (needs the service).**
  `schemathesis run <spec>.yaml --base-url http://<service-host>:<port> --checks all`
  — fuzzes the running service against its spec; this is the main
  "is our reverse-engineered understanding correct?" check.
- **Validating proxy (sits in front of the service).**
  `prism proxy <spec>.yaml http://<service-host>:<port>` — proxies real traffic
  and flags responses that violate the spec. `prism mock <spec>.yaml` stands up a
  fake from the spec instead.
- **Async backward-compat.** `asyncapi diff old.yaml new.yaml` for RabbitMQ
  contracts (oasdiff is OpenAPI-only).

Notes for live-stack runs:

- The `make`/compose tasks default to a locked-down, build-only posture
  (`--network none`, `--cap-drop=ALL`). For proxy/conformance work, run
  `podman run` / `docker run` yourself with the specific network/ports you need
  rather than loosening the defaults — keep the default build hermetic.
- Treat reaching into a real environment as the exception, scoped per task. A
  short per-service runbook (host, port, auth, which check) is worth writing once
  you know the targets; `example/contracts/README.md` shows the command shapes.

## CI later

`make build` is CI-ready as-is (offline, `--strict`, non-zero exit on warnings).
A pipeline can run the image the same way; per-project customization (extra
plugins, link-check, frontmatter lint) layers on top without changing this base.
