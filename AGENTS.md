# AGENTS.md — start here

This repository is a **product-wide documentation knowledge base** plus the
**process harness** that lets agents build and maintain it largely on their own,
over many passes. Documentation is authored as Markdown + diagrams, rendered with
MkDocs Material, and built through a portable Podman/Docker toolkit (no host
tooling needed — see [TOOLKIT.md](TOOLKIT.md)).

A product can span **many repositories**. This single docs repo documents all of
them, in layers (features → services → models → decisions).

## What do you want to do?

Match the user's intent to a routine and follow that document:

| The user says (or means)… | Do this |
|---------------------------|---------|
| "set up new project", "set this up", "bootstrap", "onboard a new product" | Follow **[agent_docs/process/new-project-bootstrap.md](agent_docs/process/new-project-bootstrap.md)**. **It will stop and ask you questions first — do not skip that.** |
| "work on what's next", "continue", "work the backlog", "keep going" | Follow **[agent_docs/process/loop.md](agent_docs/process/loop.md)**: take the *Now* item from `agent_docs/process/plan.md`, do it, reflect, route findings, commit, repeat. |
| "audit", "check the docs are accurate", "re-verify" | Run an audit pass per `agent_docs/process/loop.md` against the audit checklist. |
| author or edit a page directly | Read **[CONVENTIONS.md](CONVENTIONS.md)** and copy the right file from `templates/`. |

> **Bootstrapped yet?** `agent_docs/process/plan.md` and `backlog.md` ship in the
> scaffold with the management rules but no real content. If
> `agent_docs/stewardship/product.md` is missing — or `plan.md` still shows its
> `<product>` placeholder with no *Now* item — this product hasn't been
> bootstrapped; route to the bootstrap routine.

## Reading order

1. **This file.**
2. **[CONVENTIONS.md](CONVENTIONS.md)** — how we write docs (organic-first,
   confidence, progressive disclosure, the depth ladder, suspected-dead).
3. The routine for your task (bootstrap or loop, above).
4. `agent_docs/process/plan.md` for the current *Now* item; `templates/` for page shapes.

## Disciplines (the short version; CONVENTIONS.md is the authority)

- **Organic first, converge later** — write what's true and useful; don't force a
  rigid schema up front.
- **Confidence + provenance** — every page carries `reviewed_confidence` (1–100)
  and what it was derived from. Never assert what you didn't read in the source;
  lower confidence instead of inventing.
- **Ground truth is the code** — product docs and tickets are lower-confidence
  context you *link*, never merge over code-derived facts.
- **Record, don't discard** — suspected-dead code, drift, and contradictions get
  captured where you found them (callouts), not dropped.
- **Changes ripple** — when a fact changes, follow the links to the pages it
  affects (a new model field often surfaces in the owning service's contract and in
  features) and update or flag them; don't fix one page in isolation.

## Build

```bash
make build      # static site -> ./site  (offline, strict)
make serve      # preview at http://localhost:8000
```

## Autonomy

Work autonomously within scope: when something is ambiguous, research the source,
form a judgment, lower confidence if unsure, and proceed — don't stop to ask
permission for in-scope decisions. **The one exception is the new-project
bootstrap**, which must stop and ask the user the questions in its routine before
doing any work (the answers — especially how agents access the code — shape
everything after).
