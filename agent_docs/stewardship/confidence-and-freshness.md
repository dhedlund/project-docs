# Confidence & freshness

The single authority on how we express trust in a page and how we keep pages from
quietly rotting. Docs, unlike code, have no pass/fail gate — `reviewed_confidence`
and `last_reviewed` are how we make trustworthiness legible instead.

## The confidence scale (1–100)

`reviewed_confidence` is the reviewing pass's honest gut-feel of how **accurate and
complete** the page is *right now*. A number (not a bucket) so agents can express
nuance — they're bad at picking a bucket, fine at "about 70." Use the full range.
Rough bands, not strict thresholds:

- **80–100** — verified against the source recently; few or no known gaps.
- **50–79** — solid on the essentials; some corners unverified or known-incomplete.
- **1–49** — provisional or largely inferred; treat as a lead, not a fact.

Obligations that come with the number:
- **Never round up.** If unsure, lower confidence rather than assert.
- **Low confidence must say *what* is uncertain** (a note, a callout) — a bare low
  number isn't actionable.
- Confidence is meaningful only against a recorded source — see provenance in
  `source-of-truth.md`.

## Freshness

`last_reviewed` is the date of the most recent accuracy pass. Paired with
confidence, it's how staleness is judged. A page is **stale** when:

- the **source changed** since `last_reviewed` (drift — the primary signal; see
  `enrichment-and-currency.md`), or
- enough time has passed that re-verification is due regardless.

## Audit cadence

The drift/freshness research thread (`loop.md`) targets the **oldest
`last_reviewed`** and **lowest `reviewed_confidence`** pages first. Once coverage is
high, this thread is the main ongoing work — maintenance, not authoring. When a
code/ticket change-feed exists, changed-source pages become `DOC-VERIFY` entries
directly (`enrichment-and-currency.md`).

An audit pass re-verifies against the **current** source (not the old page, not
memory), updates drifted facts, and **re-sets both** `reviewed_confidence` and
`last_reviewed`. Confidence going *down* after an audit is a valid, useful outcome.

## Surfacing (make it actionable)

These fields earn their keep only when visible: render a confidence/freshness
**badge** on each page, and aggregate a **coverage/staleness report** so the next
audit knows where to look. (Tooling — see the mechanical-wins backlog.)
