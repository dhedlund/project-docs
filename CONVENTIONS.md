# Conventions

How we write and maintain these docs. This is itself a living document — improve
it as patterns emerge.

## Guiding philosophy: organic first, converge later

Do **not** over-standardize up front. Write the content that's true and useful for
each page, let the structure and frontmatter evolve to fit what you actually find,
and trust that a later **convergence pass** will standardize the patterns that
prove valuable across many pages. Forcing a rigid schema before we know the shape
of the content wastes effort and produces empty fields.

Concretely:

- Templates in `templates/` are **starting points, not contracts.** Add, drop, or
  rename sections and frontmatter fields when a page calls for it.
- Prefer writing the real content first; **backfill** metadata (links, scores,
  storage mappings) afterward, once the content tells you what's worth recording.
- When you notice the same new field or section appearing across many pages, note
  it — that's a candidate for the next convergence pass.

## The layers

| Layer | Directory | What lives here |
|-------|-----------|-----------------|
| L0 Overview | `docs/index.md` | The map — domains, how to navigate |
| L1 Features | `docs/features/` | Product-facing capabilities & user journeys (the "what" and "why") |
| L2 Services | `docs/services/` | Each service as a **black box**: responsibilities + formal contracts |
| L3 Models | `docs/models/` | Data/domain models and how they map to physical storage |
| L4 Decisions | `docs/decisions/` | ADRs — why things are the way they are |

Plus a cross-cutting **Glossary** (`docs/glossary.md`, from `templates/glossary.md`)
— the product's shared vocabulary; define each term once and link to the page that
owns it.

And **Datastore** pages (`docs/datastores/`, from `templates/datastore.md`) for the
databases and queues services depend on. You only list what each store *holds*;
each store's "Used by" is generated automatically from the services' `depends_on`.

Pages link **up and down** between layers: a feature links down into the services
and models it touches; a model links up to the features and service that use it.
Start by maintaining links in whichever direction is natural to write; deriving
the reverse direction automatically is a convergence-pass task, not a now task.

## Progressive disclosure

Lead with what matters **now**. Push detail into collapsible blocks so a reader
gets the essentials immediately and can expand for depth:

```markdown
??? note "Deprecated / historical"
    Old fields, legacy behavior, and why they still exist.

??? info "Future / cleanup"
    Known debt and planned changes.
```

(`???` = collapsible, starts closed. `!!!` = always-open callout. These come from
the `admonition` + `pymdownx.details` extensions.)

## Model pages: the depth ladder

Model pages run **business → technical from top to bottom**, so a product reader
gets value from the first screen and engineers keep scrolling for detail:

1. **Business view** — plain-language attribute table (no field or table names) and,
   if useful, a lifecycle diagram in business terms.
2. **How it maps to storage** — the narrative bridge: what's a real column, what's
   view-derived, what lives only in app code.
3. **Schema → Defaults & derivations → Constraints & validation → Relationships** —
   progressively more technical reference tables.

Two rules keep this from becoming a wall of data:

- **Keep tables narrow** (≤ ~4 columns). Split concerns into separate sections
  rather than one wide mega-table.
- **Always mark where a rule or relationship is enforced** — `DB` · `app` · `none`
  (and for relationships, `DB FK` · `app-only` · `cross-store`). Surfacing
  *app-only* and *unenforced* rules is the highest-value thing these pages do.

Apply the ladder **organically**: drop sections a model doesn't need (a simple
lookup table needs no Defaults section), and adapt them to the store — a schemaless
MongoDB collection replaces "nullability" with "present on" and has no DB
constraints. See the worked examples: `example/docs/models/subscription.md` (rich,
relational), `delivery-event.md` (schemaless), `organization.md` (minimal).

## Confidence

Pages carry a `reviewed_confidence` score from **1–100** — the reviewing pass's
honest gut-feel of how accurate and complete the page is *right now*. Use the full
range; a percentage captures "fairly sure but not certain" better than coarse
buckets. Pair it with `last_reviewed` (the date of that pass) so staleness is
visible. There is intentionally **no reviewer identity** — agents are anonymous.

## Recording dead / non-exercisable code

We are not tooling dead-code detection. But while tracing a flow (UI → API →
data), you will find paths, endpoints, or fields that appear unreachable. Don't
discard that finding — record it where you found it:

```markdown
!!! danger "Suspected dead"
    `users.trial_source` is written nowhere we can locate. Flagged while
    tracing the signup flow; needs confirmation.
```

## Diagrams

- **Mermaid** by default — inline, reviewable, well-understood. Use fenced
  ` ```mermaid ` blocks. Good for sequence (flows), `erDiagram` (models),
  `flowchart`, `stateDiagram`.
- **D2** for large "hero" architecture diagrams where auto-layout quality matters.
  Use a fenced ` ```d2 ` block; it renders to SVG at build time, with light and
  dark variants that follow the site's theme toggle. Mermaid stays the default for
  inline, sequence, and ER diagrams.

## Voice

How our docs should *read* — friendly, clear, example-first — lives in
`agent_docs/stewardship/voice-and-tone.md`. It's guidance, not a rulebook: clarity
and natural reading always win over staying "on style."

## Frontmatter

See the header comment in each `templates/*.md` file for the per-type fields.
Only `title`, `type`, and `status` are required everywhere; everything else is a
**suggested candidate** — include it when it's meaningful, omit it when it isn't.

### Provenance: the `sources` field

Pages that document code carry a `sources` list in frontmatter — the source state
each page was last verified against. It's what lets a re-sweep diff "what changed
since we last looked" and flag stale pages. One entry per source repo:

```yaml
sources:
  - repo: <name>          # as named in stewardship/source-of-truth.md
    branch: main          # ALWAYS the canonical branch — never a feature branch
    sha: a1b2c3d          # the commit this page was last verified against
    committed: 2026-05-30 # that commit's date — the durable fallback if the sha is
                          # later rewritten away (squash / rebase / force-push)
    paths:                # optional: the files/dirs this page actually depends on
      - app/models/subscription.rb
```

- **A list** — a page may derive from several repos.
- **Canonical branch only.** Recording a feature-branch sha is a process error —
  its commits get squashed/rebased away and you lose your place.
- **Keep both `sha` and `committed`.** The sha is the precise diff anchor while it's
  reachable; the timestamp bounds a `--since` diff when it isn't.
- **`paths` is optional but valuable** — it scopes drift detection to the files a
  page depends on, so a re-sweep flags only genuinely-affected pages.
- **Re-stamp** `sha` + `committed` (and `last_reviewed`) whenever you verify against
  newer source.

The diff procedure that consumes this lives in
`agent_docs/stewardship/enrichment-and-currency.md`.
