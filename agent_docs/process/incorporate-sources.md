# Incorporate additional sources

Use when an **already-bootstrapped** product gains new material to document — another
repo, a newly-relevant service, a ticket system, a product-docs site. (For a brand
new product, use [new-project-bootstrap.md](new-project-bootstrap.md) instead.)

Triggered by e.g. *"incorporate these sources into the project: …"*.

## Steps

1. **Register the sources.** Add each to
   `agent_docs/stewardship/source-of-truth.md` with its location, **how to read it**
   (paths / commands — never secrets or tokens), and trust level (code = ground
   truth; tickets / product docs = enrichment). Note any access constraints, and
   confirm code is read-only.
2. **Explore them** — the same cheap, breadth-first sweep as
   [bootstrap Step 1](new-project-bootstrap.md): inventory the services, models,
   features, interfaces, surfaces, and integrations these sources add or touch.
3. **Create homes & stubs** for anything new, per the IA map
   (`agent_docs/stewardship/information-architecture.md`), and add any new section to
   `mkdocs.yml` nav (`--strict` requires it). Don't duplicate homes that already
   exist.
4. **Enqueue.** Add the coverage gaps to `backlog.md` (`DOC-NEW` / `DOC-DEEPEN`). If
   the new source shifts priorities or comes with a durable directive (e.g. "treat
   repo X as authoritative for Y"), record that — dated — in
   `agent_docs/stewardship/standing-instructions.md`.
5. **Verify & hand back.** `make ci` clean, then tell the user the new sources are
   in. They can resume **"work on what's next"** and the [loop](loop.md) picks up the
   new entries.

This is deliberately a slice of the bootstrap — registering + discovering + seeding —
not a re-bootstrap. Don't touch the parts of the docs the new sources don't affect.
