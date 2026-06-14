# Backlog

The durable queue of decided-but-not-done documentation work, behind the rolling
plan (`plan.md`). Consulted when choosing the next item — not every loop iteration.
See `agent_docs/process/loop.md` for how work flows through it.

> **RULE — delete-on-completion (no tombstones).** When an item lands, **remove**
> its entry from this file. The durable record is the git commit plus the page
> itself — never a "DONE" / "LANDED" / "RESOLVED" marker left in place. This file
> is forward-looking only and carries no history. An entry MAY name a landed
> prerequisite when it genuinely sharpens the remaining work ("build X on the
> now-landed Y"), but a past-tense done-record is not a forward entry.

> **Exception — `FINDING`s.** A finding that resolves *without* a doc change (e.g.
> "looked again, the code is live, not dead") has no commit or page artifact to be
> its record. Before removing it, record the resolution where it's reachable — update
> the relevant page's `Suspected dead` / `Discrepancy` callout ("confirmed live" /
> "confirmed dead, removed upstream in [ticket]"). The page, not the deletion
> commit, is the durable home.

**Grooming** rides chunk boundaries: delete done, reclassify stale, promote ripe.
No line budget here (unlike `plan.md`) — the queue may grow. The **Research threads**
section below is *standing*: grooming and delete-on-completion apply to work items,
never to the threads themselves.

## Classification

- **`DOC-NEW`** — a needed page that doesn't exist.
- **`DOC-DEEPEN`** — a stub to flesh out.
- **`DOC-VERIFY`** — an existing page that's stale or low-confidence; re-verify
  against source.
- **`DOC-LINK`** — missing / asymmetric cross-links.
- **`CONTRACT`** — TypeSpec / OpenAPI / AsyncAPI work.
- **`FINDING`** — broken / suspicious code surfaced while documenting; needs
  confirmation (and likely an upstream ticket).
- **`OUT`** — explicitly out of scope, named so a cold reader sees the decline.

---

## DOC-NEW

_(none yet)_

## DOC-DEEPEN

_(none yet)_

## DOC-VERIFY

_(none yet)_

## DOC-LINK

_(none yet)_

## CONTRACT

_(none yet)_

## FINDING

_(none yet)_

## OUT

_(none yet)_

---

## Research threads (anti-coast — dispatch when the queue thins)

Standing sweeps that surface unknown-unknowns and refill the queue. Detail in
`agent_docs/process/loop.md` → "Research threads."

- **Coverage sweep** — undocumented / stub services, models, features → `DOC-NEW` / `DOC-DEEPEN`.
- **Drift / freshness audit** — oldest / lowest-confidence pages → `DOC-VERIFY`.
- **Orphan & dead-link lint** → `DOC-LINK`.
- **Dead-path trace** — a feature, UI → API → data → `FINDING`.
- **Glossary / consistency sweep** across pages.
