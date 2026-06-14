# `example/` — reference & testbed (disposable)

This is a **complete, self-contained miniature** of the docs setup, built around a
**fictional** product called **Beacon**. It serves two purposes:

1. **Reference** — show agents what a good, fully-realized set of docs looks like:
   filled-in pages, working cross-links between layers, diagrams, and a real (toy)
   contract pipeline. Agents copy *patterns* from here when authoring real pages.
2. **Testbed** — a place to actually run `mkdocs serve` and the contract tooling
   (oasdiff / Schemathesis / Prism) against a toy spec, so the toolchain is proven
   on fiction before it touches the real system.

> ⚠️ **Beacon is not real.** Nothing here describes our actual product. Never copy
> Beacon's *content* into real docs — only its *structure and style*.

## Canonical-while-it-exists

While this directory exists, **its config is the source of truth.** Tune
`mkdocs.yml`, extensions, and tooling here first (where you can run them), then
promote proven changes up to the root `mkdocs.yml`. Templates remain canonical at
the repo root (`../templates/`); the pages here are simply filled-in instances of
those templates.

## Delete me when…

…the real project is scaffolded enough that this no longer earns its keep. Because
it's self-contained, deletion is a clean `rm -rf example/` — root will already have
inherited any config/tooling changes you promoted.

## Beacon at a glance (the fiction)

A customer-messaging SaaS. Three services, deliberately polyglot to mirror our real
stack:

| Service | Lang | Stores | Role |
|---------|------|--------|------|
| accounts-service | Java / Spring | MySQL | orgs & users |
| billing-service | Ruby / Rails | MySQL | plans, subscriptions, invoices |
| messaging-service | Elixir / Phoenix | PostgreSQL, MongoDB, RabbitMQ | sends notifications, logs delivery events, emits/consumes events |

## Building

Uses the same portable toolkit image as the root project (see
[../TOOLKIT.md](../TOOLKIT.md)) — **Podman or Docker**, no host tooling beyond a
container engine + `make`:

```
make build      # build the Beacon site -> ./site
make serve      # preview at http://localhost:8001
```

`make image` builds the shared image from the repo root. This is the quickest
end-to-end check that the toolchain works.
