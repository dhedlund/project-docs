# Documentation working loop

How to make progress on the docs. Read end-to-end at session start; the loop is
short by design. This is the routine behind "work on what's next."

## At a glance

1. **Read context & re-ground.** `AGENTS.md`, this file, `plan.md`, `CONVENTIONS.md`.
   Read `agent_docs/stewardship/source-of-truth.md` to know how to reach the code.
   **At session start, if code access is configured, run `make drift SRC=…` and
   `make report`** and file any `STALE` / `[stale]` / `[unscored]` output as
   `DOC-VERIFY` entries before proceeding — this is how source changes re-enter the
   loop. `backlog.md` is read when choosing the next item and when checking whether
   the queue has thinned.
2. **Identify Now.** Find the *Now* item in `plan.md`. Confirm its definition of
   done (the page type's checklist in `audit-checklist.md`).
3. **Do the work.** Read the source (per source-of-truth access). Write/update the
   page(s) per `CONVENTIONS.md` — right template, the depth ladder, progressive
   disclosure. **Document only what you verify in the source; lower confidence
   rather than invent.**
4. **Verify.** `make ci` clean — that's `make build` (`--strict` links/nav) **plus
   `make check`** (frontmatter, provenance, cross-link lint). The page meets its
   type's checklist; `reviewed_confidence` set honestly and `last_reviewed` dated;
   provenance (`sources`) recorded — `make check` *requires* it on code-derived
   pages.
5. **Reflect & capture.** Answer the step-5 questions in writing, before commit.
6. **Route findings.** Distil answers into the right destinations (step-6 table).
7. **Commit.** Page work and plan update land together.
8. **Repeat.** Return to step 2. When *Now* is complete: move the chunk to *Last
   completed*, **delete the landed `backlog.md` entry** (record completion in the
   commit message — never leave a "DONE" tombstone), and pull the next item from
   *Up next* or the top-ranked fitting `backlog.md` entry into *Now*. If your
   context has faded, re-ground (step 1) first.
9. **Anti-coast: when the backlog thins, refill — then know when to stop.** If
   *Now*, *Up next*, and every regular `backlog.md` entry are resolved, don't stop
   yet: dispatch a standing **research thread** (see below); its output becomes the
   next *Now* candidate. **When to actually stop the session:**
   - if the user set an **iteration budget** ("work the next N items," "for an
     hour"), stop when it's spent;
   - otherwise, stop when you **run out of useful work** — the backlog is empty
     *and* the research threads turn up nothing actionable for a round or two *and*
     no source has changed since the last drift run.

   A full "done" is an ideal you rarely hold (any source change re-opens work), so
   don't manufacture make-work to avoid stopping, and don't claim a false done. A
   quiet steady state is a fine place to end a session.

If the plan is stale (the *Now* item's definition of done is already met, sections
don't match reality, or *Recent discoveries* is non-empty from a prior iteration),
**stop and reconcile before doing more work.**

This is an autonomous loop. Work the steps, commit when a page reaches its
definition of done and the build is green, move on. Don't stop to ask permission
for in-scope decisions; when something is ambiguous, read the source, form a
judgment, lower confidence if unsure, and proceed.

When a session dispatches work to subagents, `orchestration.md` governs dispatch
and integration; this loop still governs each unit of work.

## Why this exists

Agents drop discoveries when a task is "done." Drift noticed in passing gets lost;
follow-up pages never get recorded; uncertainty gets rounded up to confident. The
fix is forcing-function questions answered in writing, each with an explicit
destination. This loop is that — and it is how the backlog grows *as the system is
learned*.

## Step 5: Reflect & capture (the questions)

Answer each in writing before any commit. "N/A" is allowed with a one-line reason.
Skipping silently is the failure mode this loop exists to prevent.

1. **Found-but-not-fixed.** Did you hit anything broken, suspicious, or surprising
   in the code, the existing docs, or other sources — dead/unreachable code, drift,
   contradictions? List each with location. For each: captured where (a page
   callout, a backlog `FINDING`)?
2. **Self-review.** Walk your page changes. Is each accurate to the source and
   minimal? Did you assert anything you did **not** actually verify?
3. **Confidence honesty.** Is `reviewed_confidence` an honest gut-feel of accuracy
   and completeness? What lowered it? Did you date `last_reviewed`?
4. **Coverage, links & ripple.** Did you reference services/models/features that
   have no page? Create stubs and backlog them. Are backlinks owed elsewhere? **And
   does this change ripple to related pages?** A model gaining or changing a field
   often means the owning service's contract *dynamically* exposes it and features
   surface it — traverse `sources`, `owned_models`, `related_*` / `uses_*`, and the
   contract, then either update the tightly-coupled pages in this pass or open
   `DOC-VERIFY` entries naming the specific ripple.
5. **Goal-fit.** Does the page serve its reader top-to-bottom (business → technical
   for models)? Where would a reviewer push back?
6. **Provenance.** Did you record what source the page was derived from, and the
   ref, per `source-of-truth.md`?
7. **Learnings / forward-looking.** Did you learn something that affects other
   pages, or imply new pages/sections? Route to `backlog.md` or the page.
8. **New ideas.** Anything occur to you that didn't exist when you started? Worth
   recording?
9. **Step back.** Forget the structure: "anything else worth knowing before I move
   on?" "Nothing" needs a reason.
10. **Closure.** Are all answers routed to a durable destination? Could a cold
    agent pick up the page and plan and continue?

## Step 6: Route findings to destinations

| Finding | Destination |
|---------|-------------|
| Broken/suspicious code (dead, unreachable, drift) | Page `!!! danger "Suspected dead"` / `Discrepancy` callout **and** a `FINDING` backlog entry |
| A needed page that doesn't exist | `DOC-NEW` backlog entry (+ a stub page if cheap) |
| A thin / stub page | `DOC-DEEPEN` backlog entry |
| Stale or low-confidence existing page | `DOC-VERIFY` backlog entry |
| Missing / asymmetric cross-links | `DOC-LINK` backlog entry |
| A change that ripples to related pages (e.g. a model field the contract exposes) | Update the impacted page in-pass if verified; else `DOC-VERIFY` naming the ripple |
| Contradiction with product docs or tickets | Page `Discrepancy` callout + backlog (don't overwrite code-derived facts) |
| Contract (TypeSpec/OpenAPI/AsyncAPI) work | `CONTRACT` backlog entry |
| API / webhook / SDK / integration / surface / flow / options / roles / domain info | File it in that kind's home per `agent_docs/stewardship/information-architecture.md` |
| Durable domain learning | `agent_docs/stewardship/product.md` or the glossary |
| New idea (tactical) | `plan.md` *Open questions* or `backlog.md` |
| Decided out of scope | `backlog.md` *Out of scope* (named, so a cold reader sees the decline) |

After routing, *Recent discoveries* in `plan.md` should be empty.

## Research threads (the anti-coast engine)

Standing background sweeps that surface unknown-unknowns and manufacture new
backlog entries. Dispatch one whenever the regular backlog thins:

- **Coverage sweep** — which services/models/features have no page or only a stub?
  → emit `DOC-NEW` / `DOC-DEEPEN`.
- **Drift / freshness audit** — re-verify the N oldest / lowest-confidence pages
  against current source → emit `DOC-VERIFY` (and adjust confidence in place).
- **Orphan & dead-link lint** — pages nothing links to, links to missing pages,
  asymmetric relationships → emit `DOC-LINK`.
- **Dead-path trace** — pick a feature, trace UI → API → data, record
  non-exercisable code as `FINDING`s.
- **Glossary / consistency sweep** — terms named inconsistently across pages →
  reconcile, grow the glossary.

For a living system the threads rarely stay empty for long — a source or ticket
change refills them. But within a session they *can* come up dry; when they do (and
the backlog is empty and nothing has changed), that's your signal to stop, not to
invent work.

## Anti-rot

- **Plan length budget.** `plan.md` targets ≤ ~200 lines; queued work that would
  bloat it goes to `backlog.md`, not pruned away.
- **Stale plan = stop.** A stale plan is worse than no plan. Reconcile first.
- **Routine answers = skipping.** If reflection answers read like boilerplate,
  you're skipping. The answers are usually different.
- **Single stream at the plan level.** One *Now* item at a time; parallel dispatch
  is an execution detail (see `orchestration.md`), not a second plan stream.

## When to revise this loop

When the loop itself is the failure mode — the questions stop catching what they
were written to catch, or new failure modes appear that they miss. Loop revisions
land as ordinary commits with a brief rationale.
