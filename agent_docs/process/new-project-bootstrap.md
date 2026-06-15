# New-project bootstrap

Run **once per product** to take it from an empty scaffold to a *seeded, loopable*
state. A product can span many repositories; this one docs repo will cover all of
them. After this completes, the user can say "work on what's next" and the
[loop](loop.md) takes over.

**Principle: discover, don't interrogate.** The whole point is that the agent builds
the docs — so don't hand the user a questionnaire of things you can read from the
code. Ask only for what you genuinely *cannot* determine from the source — above
all, **how to access the code** — then go explore and figure out the rest, and
*propose* the judgment calls (where to start, what's out of scope) rather than
asking them cold.

---

## Step 0 — STOP and ask (the essentials only). Do not skip this.

**Before changing any files, ask the user just these, and wait — then proceed.**
Keep it short; this is not a survey.

1. **Sources & how to read them — REQUIRED.** What should I document *from*, and how
   do I read each? Take the list the user gives and pin down:
   - **Code repos** — the load-bearing source. Where each lives and how an agent
     reads it (read-only clone path? mounted at `/src`? the agent runs where the code
     is?). Confirm the code is **read-only** — we document it, never modify it.
   - **Other sources to fold in** *(optional)* — a ticket system (e.g. a JIRA project
     and the CLI to query it), a product-docs site, etc. These are *enrichment* (the
     "why") — linked, never merged over code.
   Note any access constraints (private repos, secrets, VPN).
2. **Product, in one line** — name + what it does. *Skip if it's obvious from the
   repos;* confirm what you infer.
3. **Anything off-limits or known out of scope?** *(Optional — you'll also propose
   scope yourself in Step 2.)*

Everything else — domains, languages, datastores, queues, public API, webhooks,
SDKs, auth, frontends, integrations, roles — **you will discover in Step 1. Don't
ask for it.** If the user can't answer something critical, record the gap and
proceed with a low-confidence assumption. **At least one code source must be
answered** before you touch files.

---

## Step 1 — Explore the source (discover, cheaply)

Using the agreed code-access method, do a **breadth-first sweep** across the repos —
fast and shallow, not a deep read. You're drawing a map, not writing the docs yet.
From manifests, config, directory layout, and entry points, identify:

- **Stack** — languages, frameworks, build/deps (`package.json`, `pom.xml`,
  `mix.exs`, `go.mod`, `Gemfile`, `requirements.txt`, …).
- **Datastores & queues** — databases, caches, brokers (from config / connection
  setup / migrations / schemas).
- **Domains / bounded contexts** — the major capability areas (from top-level
  module/service structure and naming).
- **Services** — the deployable/black-box units and roughly what each owns.
- **Data models** — the core entities and where they're persisted.
- **Integration surface** — public/partner **API** (REST / GraphQL?), **webhooks**
  it emits, client **SDKs** (which languages), and the **auth** model (API keys /
  OAuth / …). Look for route definitions, API specs, SDK packages.
- **Frontends / surfaces** — the apps that exist (B2C app, partner/admin portal,
  marketing/status site).
- **Third-party integrations** — payments, email/SMS, CRM, storage, etc. (from deps
  and client config).
- **Roles / access control** — if there's meaningful authz, the main roles.
- **Existing docs / tickets** — note if a product-docs site or ticket system exists;
  **don't ingest now** — they're lower-confidence enrichment for later.

Record what you find (it feeds Steps 2 and 6). Where the code can't tell you, say
so — that's a gap to confirm, not a guess to assert.

## Step 2 — Propose scope & starting point (confirm once)

Summarize what you discovered — domains, stack, surfaces, the integration surface —
and in **one short message** propose:

- which **homes** you'll create (per the IA map —
  `agent_docs/stewardship/information-architecture.md`),
- **where to start** (typically the highest-value service/domain plus its models),
- what looks **out of scope** for now.

Ask the user to confirm or adjust — a single round, not another questionnaire. Then
proceed.

---

> **Shape reference.** `agent_docs/process/plan.md` and `backlog.md` already ship
> in the scaffold with the management rules and classification baked in — fill them
> **in place**. `example/agent_docs/` shows the whole thing filled in for the
> fictional Beacon product (stewardship + plan + backlog).

## Step 3 — Confirm the scaffold

Ensure the repo has `templates/`, `docs/{features,services,models,decisions}/`,
`docs/datastores/`, `docs/glossary.md`, `contracts/` (interface specs), `CONVENTIONS.md`,
the toolkit (`Containerfile`, `Makefile`, `TOOLKIT.md`), and
`agent_docs/process/{plan,backlog}.md` (present with the rules, ready to fill). If
anything is missing, create it from this repo's existing shape. Don't reinvent —
the scaffold already exists.

## Step 4 — Write the facts (from discovery + the answers)

- `agent_docs/stewardship/source-of-truth.md` — the **sources registry**: every
  source from Step 0 (code = ground truth; tickets / product docs = enrichment),
  each with its location, **how to read it** (paths / commands — never secrets), and
  trust level, plus the **provenance convention** (default: cite as `repo@<short-sha>`
  — adopt unless the user wants another). Every later pass reads this to reach and
  cite the sources.
- `agent_docs/stewardship/standing-instructions.md` — seed it with any **durable
  directives** the user gave (priorities, preferences, "remember X"), each dated.
  Keep it short; it grows over time. If there are none yet, create it with a one-line
  note saying so.
- `agent_docs/stewardship/product.md` — identity, domains, scope and non-goals
  (from Step 1 plus the Step 2 confirmation).

## Step 5 — Fill in product specifics

Update `AGENTS.md` with the product name, the repo list, and a one-line pointer to
`agent_docs/stewardship/source-of-truth.md` for code access.

## Step 6 — Inventory and stub

From your Step 1 exploration, cheaply enumerate the services, models, and features
you identified (don't deep-dive). For each, create a **stub page** from the matching
`templates/` file under `docs/`, with `status: stub` and a low `reviewed_confidence`.
The goal is breadth and a real cross-link graph, not depth.

Then, for each zone the exploration found, **create its home and a stub** per the IA
map (`agent_docs/stewardship/information-architecture.md`): e.g. `docs/interfaces/`
(`api/`, `webhooks/`, `sdks/`, `auth.md`), `docs/integrations/`, `docs/surfaces/`,
`docs/access/`, plus `docs/domains/` for the domains you found. Add each new section
to `mkdocs.yml` nav as you create it (`--strict` requires it). Don't create homes
for zones the product doesn't have.

## Step 7 — Seed the queue

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

## Step 8 — Verify it builds

```bash
make ci
```

Fix anything `make ci` (build `--strict` + lint) flags before handing off.

## Step 9 — Hand off

Tell the user bootstrap is complete and they can now say **"work on what's next"**
(or set working the backlog as a standing goal). From here, [loop.md](loop.md)
drives all work.

---

## Definition of done

A scaffold + stewardship docs + stub pages across the layers + a `plan.md` with a
*Now* item + a `backlog.md` of coverage gaps and standing research threads, that
**builds cleanly**. Seeded and loopable.
