# Source of truth (Beacon)

> **Fictional reference** — shows what the bootstrap's code-access answers become.

The load-bearing axis: how agents reach the code, how they cite it, and what counts
as true.

## Code access

- The repos are kept as **read-only clones** on the build host at
  `~/code/beacon/<repo>` (`beacon-accounts`, `beacon-billing`, `beacon-messaging`,
  `beacon-web`, `beacon-sdks`).
- They are mounted **read-only** into the toolkit container at `/src/<repo>` for
  authoring/audit work (`-v ~/code/beacon:/src:ro`).
- Agents **read** the code; they never modify it. The clones are kept current by
  the maintainer, not by agents.
- No secrets are needed to read the source; live-stack interaction (Prism /
  Schemathesis) is a separate, scoped activity per `TOOLKIT.md` and is not part of
  normal authoring.

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
