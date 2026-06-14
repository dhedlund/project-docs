# Audit checklist — definitions of done

Docs have no compiler, so this checklist is the closest thing to "gates." It
serves two purposes: the **definition of done** when authoring a page (loop step 4)
and the **verification list** when running a drift/freshness audit pass.

## Every page (all types)

- `make build` is green (`--strict`) — no broken internal links, valid nav.
- Frontmatter: `title`, `type`, `status` present; `reviewed_confidence` is an
  honest 1–100; `last_reviewed` is today's date for this pass.
- **Provenance** recorded in `sources` frontmatter — `repo` / `branch` / `sha` /
  `committed` per source (see `CONVENTIONS.md` → Provenance); re-stamped this pass
  if verified against newer source.
- Leads with what matters now; nuance/history/cleanup pushed into collapsible
  blocks (progressive disclosure).
- Anything broken/unreachable found while writing is captured in a callout
  (`Suspected dead` / `Discrepancy`), not dropped.
- Cross-links: things this page references either exist as pages or have stubs +
  backlog entries; no dangling link text.
- Ripple checked: pages this change impacts (e.g. the contract that dynamically
  exposes a changed model field, or features that surface it) are updated, or have
  a `DOC-VERIFY` entry naming the ripple.

## Model pages

- **Business view** first (plain language, no field/table names); optional
  lifecycle diagram.
- **How it maps to storage** narrative present (the model-vs-physical gap).
- Technical ladder where applicable: **Schema → Defaults & derivations →
  Constraints & validation → Relationships**, each table ≤ ~4 columns.
- Every constraint/relationship marks **where it's enforced** (`DB` / `app` /
  `none`; `DB FK` / `app-only` / `cross-store`).
- Adapted to the store (a schemaless collection uses "present on" not nullability,
  and notes "no DB constraints").

## Service pages

- Treated as a **black box**: responsibilities and explicit non-responsibilities.
- Interface section links/embeds the formal contract (OpenAPI/AsyncAPI), or backlogs
  a `CONTRACT` entry if none exists yet.
- Owned models linked; dependencies (services, datastores, queues) named.
- At least one key-flow diagram (sequence).

## Feature pages

- Product-language summary and user journey first.
- A "how it works" walk-through connecting **UI → API(s) → data**, linking down to
  the relevant service and model pages at the right moments.
- Services and models involved listed.

## Decision pages (ADRs)

- Context, Decision, Consequences. Short — the value is the reasoning.

## Stub pages

- Allowed and expected early. `status: stub`, low `reviewed_confidence`, a
  one-line "what this is", and the right frontmatter `related_*` so the cross-link
  graph is real. A matching `DOC-DEEPEN` backlog entry exists.

## Running an audit pass

1. Pick targets: oldest `last_reviewed` and/or lowest `reviewed_confidence` first.
2. Re-verify the page against the **current** source (not memory, not the old
   page). Update facts that drifted.
3. Re-set `reviewed_confidence` and `last_reviewed` to reflect this pass.
4. Route anything found (drift, new dead code, missing pages) per the loop's
   routing table.
5. If the source changed materially since `last_reviewed`, that's expected — the
   audit is how the docs track a living system.
