# Confidence & freshness

The single authority on how we express trust in a page and how we keep pages from
quietly rotting. Docs, unlike code, have no pass/fail gate — `reviewed_confidence`
and `last_reviewed` are how we make trustworthiness legible instead.

## The confidence scale (1–100)

`reviewed_confidence` is the reviewing pass's honest gut-feel of the page's quality
*right now*, across three dimensions:

- **Accuracy** — is what it says correct against the source?
- **Completeness** — are the important parts present, or are there gaps?
- **Whole story** — does it tell the relevant story (the nuances, gotchas, and the
  "why" a reader needs), not just the bare facts?

A number, not a bucket, so you can express real nuance — "72" carries more than a
coarse high/medium/low. Use the full range. Rough bands, not strict thresholds:

- **80–100** — accurate, reasonably complete, tells the story; few known gaps.
- **50–79** — solid on the essentials; corners unverified, incomplete, or thin on
  the "why."
- **1–49** — provisional or largely inferred; treat as a lead, not a fact.

It's a **signal, not a gate.** Confidence guides where the next pass goes (deepen,
re-verify); it does **not** decide whether a page "counts" as covered — that's
structural (`scope-and-completeness.md`).

Obligations that come with the number:
- **Never round up.** If unsure, lower confidence rather than assert.
- **Low confidence must say *what* is uncertain or missing** (a note, a callout) — a
  bare low number isn't actionable.
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

These fields earn their keep only when visible — but they shouldn't shout. The
build hook renders a quiet confidence/freshness **footer** (with provenance) at the
very bottom of each content page, and **`make report`** aggregates a
coverage/staleness table — unscored and stalest pages first — so the next audit
knows where to look.
