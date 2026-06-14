# Project Docs

A single, product-wide knowledge base for our multi-service system, authored and
maintained primarily by agents over many passes, version-controlled, and rendered
as a [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) site.

The goal: rebuild a shared understanding of the system **layer by layer** — from
product features down through service boundaries to the data models behind them —
and keep it discoverable, cross-linked, and honest about confidence.

## How it's organized

```
project-docs/
├── docs/              # the site content (what gets built)
│   ├── index.md       # L0 — product overview / the map
│   ├── features/      # L1 — product-facing capabilities & journeys
│   ├── services/      # L2 — services as black boxes + their contracts
│   ├── models/        # L3 — data/domain models and how they map to storage
│   ├── datastores/    # the databases & queues services depend on
│   ├── glossary.md    # shared vocabulary
│   └── decisions/     # L4 — architecture decision records (ADRs)
├── templates/         # starting points for new pages (NOT part of the site)
├── CONVENTIONS.md     # how we write these docs — read this first
└── mkdocs.yml         # site config
```

The layers are levels of **hierarchy and understanding**, not separate systems —
one site holds them all, and pages link up and down between layers so readers
drop to the right level at the right time.

## Authoring

Read **[CONVENTIONS.md](CONVENTIONS.md)** before writing. The short version:

- Copy a file from `templates/` to start a new page.
- Treat structure **organically** — evolve it, don't force it. We converge on a
  standard in a later pass, once patterns emerge.
- Lead with what matters now; push nuance, history, and cleanup into collapsible
  sections below.
- Record a confidence score and what a page was derived from.

## Diagrams

- **Mermaid** is the default (renders inline, no extra tooling). Use it for
  sequence diagrams (feature flows), ER diagrams, flowcharts, state.
- **D2** is reserved for large "hero" architecture diagrams where layout quality
  matters. It needs a render step (Kroki/D2), wired up later — see CONVENTIONS.

## Building the site

Everything runs through one portable container image — **Podman or Docker**, no
host tooling beyond a container engine + `make` (works on Linux and macOS). The
`make` targets auto-detect the engine; force one with `make build ENGINE=docker`.
See [TOOLKIT.md](TOOLKIT.md).

```
make            # list all targets
make build      # static site -> ./site  (offline, strict)
make serve      # live preview at http://localhost:8000
make check      # lint frontmatter + cross-link graph
make report     # coverage / staleness report
make ci         # build + check (the local gate; what CI runs)
```

The same targets exist in [`example/`](example/) (preview on port 8001) and are
the quickest way to confirm your setup works end to end.

## Service contracts

Service interfaces are the one place we keep **formal, testable** specs. Author in
**TypeSpec**, compile to **OpenAPI** (HTTP) and pair with **AsyncAPI** (RabbitMQ).

Verification is a trio of best-of-breed tools (chosen over a single platform like
Specmatic for being lighter and OpenAPI-centric):

- **[oasdiff](https://github.com/oasdiff/oasdiff)** (Go) — backward-compatibility
  gate in CI; detects breaking changes between spec versions.
- **[Schemathesis](https://github.com/schemathesis/schemathesis)** — property-based
  testing that verifies a running service actually conforms to its spec (our main
  "is our reverse-engineered understanding correct?" check).
- **[Prism](https://github.com/stoplightio/prism)** — validating proxy / mock for
  watching live traffic against a spec.

A worked example of the whole pipeline lives in `example/contracts/`.

## The `example/` reference

`example/` is a **self-contained, disposable** copy of this setup, built around a
fictional product ("Beacon") that mirrors our stack (Java/Ruby/Elixir;
MySQL/PostgreSQL/MongoDB/RabbitMQ). It exists to show agents *what good looks like*
and to serve as a live testbed for the site config and contract tooling. Its
config is **canonical while it exists** — prove changes there, then promote to
root. Delete it once the real project no longer benefits from it.
