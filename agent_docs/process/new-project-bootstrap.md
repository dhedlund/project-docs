# New-project bootstrap

Run **once per product** to take it from an empty scaffold to a *seeded, loopable*
state. A product can span many repositories; this one docs repo will cover all of
them. After this completes, the user can say "work on what's next" and the
[loop](loop.md) takes over.

---

## Step 0 — STOP and ask. Do not skip this.

**Before changing any files, ask the user the questions below and wait for
answers.** Do not assume defaults — the answers (especially *code access*) shape
everything that follows. Ask them grouped, in your own words; let the user answer
in bulk. If the user defers a non-critical question, record the gap and proceed
with a low-confidence assumption. **Code access (group 3) must be answered.**

### 1. Product identity
- What is the product called, and in one paragraph, what does it do?
- What are its major domains / capabilities (rough is fine)?

### 2. Repositories (a product = many repos)
- Which repositories make up this product? For each: where it lives and its
  primary language / role.
- Which are in scope to document now vs. later?

### 3. Code access — REQUIRED
- **How should an agent read the source code?** e.g.:
  - a read-only local clone/mirror on this host (which path?),
  - mounted read-only into the toolkit container (which path?),
  - the agent runs on the host where the code already lives,
  - a per-session snapshot/export the user provides.
- Any access constraints — private repos, secrets, VPN, network rules?
- **Provenance:** should agents record the commit/snapshot they verified a page
  against? (Recommended yes — pick a ref format, e.g. `repo@<sha>` or
  `repo@<date>`.)
- Confirm the code is **read-only** to agents (we document, never modify it).

### 4. Stack (so we anticipate page types)
- Backend languages, datastores, message queues, frontends.

### 5. Boundaries & priorities
- Which layer or domain should we seed first?
- Anything explicitly out of scope?
- Existing product docs or ticket systems to fold in later? (Capture that they
  exist; don't ingest them now — they're lower-confidence enrichment.)

### 6. Build & hosting (mostly defaulted)
- Confirm a single docs repo (default: yes).
- Any CI or hosting target to keep in mind?

Write the answers down as you go (step 2 turns them into stewardship docs).

---

> **Shape reference.** `agent_docs/process/plan.md` and `backlog.md` already ship
> in the scaffold with the management rules and classification baked in — fill them
> **in place**. `example/agent_docs/` shows the whole thing filled in for the
> fictional Beacon product (stewardship + plan + backlog).

## Step 1 — Confirm the scaffold

Ensure the repo has `templates/`, `docs/{features,services,models,decisions}/`,
`CONVENTIONS.md`, the toolkit (`Containerfile`, `Makefile`, `TOOLKIT.md`), and
`agent_docs/process/{plan,backlog}.md` (present with the rules, ready to fill). If
anything is missing, create it from this repo's existing shape. Don't reinvent —
the scaffold already exists.

## Step 2 — Write stewardship (from the answers)

- `agent_docs/stewardship/product.md` — identity, domains, scope and non-goals.
- `agent_docs/stewardship/source-of-truth.md` — **the authoritative code-access
  model and provenance convention** captured from group 3. Every later pass reads
  this to know how to reach the code and how to cite it.

## Step 3 — Fill in product specifics

Update `AGENTS.md` with the product name, the repo list, and a one-line pointer to
`agent_docs/stewardship/source-of-truth.md` for code access.

## Step 4 — Inventory and stub

Using the agreed code-access method, cheaply enumerate the services, models, and
features you can identify (don't deep-dive). For each, create a **stub page** from
the matching `templates/` file under `docs/`, with `status: stub` and a low
`reviewed_confidence`. The goal is breadth and a real cross-link graph, not depth.

## Step 5 — Seed the queue

Fill in `agent_docs/process/plan.md` and `backlog.md` — they ship in the scaffold
with the management rules and classification already in place; replace the
placeholders and seed the queue:

- `agent_docs/process/plan.md` — the rolling plan with the first *Now* item
  (typically: complete the coverage inventory, or deepen the highest-value
  service plus its models).
- `agent_docs/process/backlog.md` — the durable queue: every coverage gap as a
  `DOC-NEW` / `DOC-DEEPEN` entry, plus the standing **research threads** that keep
  the loop fed (coverage sweep, drift/freshness audit, orphan & dead-link lint,
  dead-path trace, glossary/consistency). These are what make the loop
  self-sustaining — see [loop.md](loop.md).

## Step 6 — Verify it builds

```bash
make build
```

Fix anything `--strict` flags before handing off.

## Step 7 — Hand off

Tell the user bootstrap is complete and they can now say **"work on what's next"**
(or set working the backlog as a standing goal). From here, [loop.md](loop.md)
drives all work.

---

## Definition of done

A scaffold + stewardship docs + stub pages across the layers + a `plan.md` with a
*Now* item + a `backlog.md` of coverage gaps and standing research threads, that
**builds cleanly**. Seeded and loopable.
