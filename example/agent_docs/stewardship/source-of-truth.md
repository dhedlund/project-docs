# Source of truth (Beacon)

> **Fictional reference** — shows what the bootstrap's source answers become.

The load-bearing axis: where agents get content, how they read each source, how they
cite it, and what counts as true.

## Sources

**Code — ground truth.**
- Read-only clones on the build host at `~/code/beacon/<repo>`
  (`beacon-accounts`, `beacon-billing`, `beacon-messaging`, `beacon-web`,
  `beacon-sdks`), mounted **read-only** into the toolkit container at `/src/<repo>`
  (`-v ~/code/beacon:/src:ro`).
- Agents **read** the code; they never modify it. The clones are kept current by the
  maintainer, not by agents. No secrets are needed to read the source.

**Tickets — enrichment (the "why").**
- JIRA project **`BCN`**, read via the `jira` CLI — e.g.
  `jira issue list -p BCN -q "updated >= -90d"`, `jira issue view BCN-123`.
- Used to explain *why* something is the way it is; **linked, never merged over**
  code-derived facts. Lower confidence.

**Product docs — enrichment.**
- Public help center at `https://help.beacon.example` and the internal product wiki.
  Linked for intent/background; lower confidence than code.

> Record *how* to reach each source (paths, commands), **never secrets or tokens** —
> those live in the environment, not in this repo. Live-stack interaction (Prism /
> Schemathesis) is a separate, scoped activity per `TOOLKIT.md`, not normal authoring.

## Provenance / citing the source

Each page records, in its `sources` frontmatter, the repo / branch / sha /
committed-date it was last verified against (see `CONVENTIONS.md` → Provenance) —
always against the canonical branch (`main`). The human-readable "Sources &
confidence" section can still call out specifics in prose. This is what lets a drift
audit ask "has the backing source changed since this page was verified?" and diff
precisely — by sha range when reachable, else since the committed date.

## What counts as true

1. **Code is ground truth.** Code-derived facts outrank everything else.
2. **Secondary sources fold in, never over.** Product docs, tickets, and git
   history are linked for "why," never merged over a code-derived fact — see the
   generic `enrichment-and-currency.md`.
3. **Confidence & freshness** follow the generic `confidence-and-freshness.md` (the
   1–100 scale, staleness, and audit cadence).
