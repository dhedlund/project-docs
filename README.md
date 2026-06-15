# Project Docs

**An agent-driven system for building and maintaining comprehensive, code-true
documentation of large multi-service, multi-language systems.**

You fork this repo, point an AI coding agent at it, and it documents your product —
across many repositories, over many passes — as Markdown + diagrams rendered with
[MkDocs Material](https://squidfunk.github.io/mkdocs-material/). The docs stay honest
about *what they know*: every page carries a confidence score and a provenance ref to
the source it was verified against, and a drift checker flags pages whose code has
since changed.

> It's a scaffold + process harness, not a finished site. The docs are authored by
> agents from your source code; trust is made legible (confidence, provenance, drift,
> audits), not assumed.

**▶ See it live:** the bundled [`example/`](example/) — a fictional product, "Beacon" —
is published as a worked demo at **<https://dhedlund.github.io/project-docs/>**, a
complete picture of what this produces (rich pages, diagrams with a fullscreen viewer,
confidence/provenance footers).

## Why

Big systems drift out of understanding: nobody holds the whole picture, product docs
go stale, and the "why" lives in tickets nobody re-reads. This rebuilds that
understanding **layer by layer from the code** — services as black boxes with
testable contracts, data models and how they really map to storage, the product
surface (features, flows, options), and the integration surface (public API,
webhooks, SDKs) — and keeps it current as the code changes.

## Quick start

**Requirements:** [Podman](https://podman.io) or Docker, plus `make`. (And an AI
coding agent — e.g. Claude Code — to drive it.)

> **Model choice.** The system is model-agnostic — any capable coding agent works.
> The work here is highly structured (clear templates, well-scoped loop steps,
> explicit conventions), so you don't need a frontier model for most of it: cheaper,
> faster, open-weights models like **DeepSeek V4 Flash** — a fraction of frontier
> pricing — tend to give strong value, which adds up when you're running long
> autonomous loops. A common split: a budget model for the bulk authoring and
> maintenance, a stronger model for the gnarly bits (tricky permutation flows,
> architecture decisions).

1. **Fork or copy** this repo into a repo for your product (see [Starting a new
   product](#starting-a-new-product) for the tradeoffs).
2. **Open your agent in the directory** so it reads `AGENTS.md` (and `CLAUDE.md`,
   which points to it).
3. **Paste a bootstrap prompt** (below). The agent stops and asks about anything it
   needs, then scaffolds and seeds your docs.
4. Drive it with **"work on what's next"** (optionally on a loop).
5. Preview anytime: `make serve` → http://localhost:8000.

No host tooling beyond Podman/Docker + `make` — everything runs in one portable
toolkit image (see [TOOLKIT.md](TOOLKIT.md)).

### The bootstrap prompt

Paste this and replace the `<PLACEHOLDERS>` with your product's details:

```text
Read AGENTS.md, then follow the new-project bootstrap to set up documentation for
my product. Here are answers to its questions:

- Product: <NAME> — <one sentence on what it does>.
- Domains (rough is fine): <e.g. accounts, billing, messaging>.
- Repositories (a product = many repos):
    - <repo-name> — <git URL or local path>, <language/stack>, <role>
    - <repo-name> — <...>
- Code access: <how an agent should read the source, e.g. read-only clones at
  ~/code/<product>/<repo>, mounted read-only at /src>. Treat the code as read-only.
- Provenance: cite sources as <repo>@<short-sha>.
- Stack: <backend languages> · <datastores> · <queues> · <frontends>.
- Public interfaces: API <none / REST / GraphQL>; webhooks <yes/no>;
  SDKs <languages>; auth <API keys / OAuth / ...>.
- Surfaces (frontends): <B2C app / partner portal / admin console / marketing>.
- Third-party integrations: <payments / email / SMS / CRM / ...>.
- Start with: <which domain or area to seed first>.
- Out of scope: <anything to skip>.

Stop and ask me about anything unclear, then seed the plan and backlog and tell me
when it's ready for "work on what's next".
```

Prefer to answer interactively? Just paste **`Read AGENTS.md and set up a new
project.`** — the bootstrap asks you these questions itself.

## What's in the box

- **Page types + templates** for every kind of documentation: domains, features,
  flows (permutation-heavy behaviour), options/configuration, services, models,
  datastores, decisions (ADRs), glossary, the integration surface (API, webhooks,
  SDKs, auth), third-party integrations, frontend surfaces, roles, and machine-
  readable contracts.
- **A portable toolkit image** (Podman or Docker): MkDocs Material, Mermaid + D2
  diagrams, TypeSpec → OpenAPI, oasdiff, Schemathesis, Prism, AsyncAPI CLI, Swagger
  UI — plus the repo's own `docs-check` / `docs-report` / `docs-drift` tools.
- **A `make` front door**: `make` (help), `build`, `serve`, `check`, `report`,
  `drift`, `ci`, `test`.
- **An agent harness** (`agent_docs/`): a self-sustaining working loop (reflection,
  routing, research threads), a bootstrap routine, and stewardship docs (scope,
  confidence/freshness, source-of-truth, enrichment, voice, information architecture).
- **A worked example product** ("Beacon") under [`example/`](example/) — a complete,
  buildable reference for what good looks like. Delete it once you don't need it.

## Starting a new product

This repo is the reusable scaffold. To document a product with it:

1. **Get the scaffold into a repo for your product**, either way:
   - **Fork it** — keeps a link to upstream, so you can pull scaffold improvements
     later (and contribute fixes back).
   - **Copy the files** — clean history, no upstream link. Drop them at the root of a
     new repo, or into a subdirectory of an existing one if you're adding docs
     alongside code (run `make` from that directory; for CI, set the workflow's
     working directory).

   It's self-contained either way — no submodules or external state.
2. **Keep `example/` as a reference** while you find your feet; delete it when you no
   longer need it (it's disposable and nothing depends on it).
3. From the new repo, run an agent and use the **bootstrap prompt** above. After
   bootstrap, **"work on what's next"** drives the rest.

## How it's organized

```
project-docs/
├── AGENTS.md          # agent entry point (CLAUDE.md symlinks to it)
├── CONVENTIONS.md     # how pages are written (read before authoring)
├── TOOLKIT.md         # the Podman/Docker toolkit
├── docs/              # the rendered site content (features, services, models, …)
├── contracts/        # machine-readable interface specs (TypeSpec/OpenAPI/AsyncAPI)
├── templates/         # starting points for new pages + a contract project skeleton
├── agent_docs/        # the agent harness: process/ (loop, bootstrap) + stewardship/
├── example/           # a complete worked example product (disposable reference)
├── Containerfile · Makefile · compose.yaml · mkdocs.yml
```

The layers are levels of understanding, not separate systems — one site holds them
all, and pages link up and down so readers drop to the right level at the right time.
The full map of where each kind of doc lives is
[`agent_docs/stewardship/information-architecture.md`](agent_docs/stewardship/information-architecture.md).

## Building

```
make            # list all targets
make build      # static site -> ./site  (offline, strict)
make serve      # live preview at http://localhost:8000 (localhost-only; BIND=0.0.0.0 to expose)
make check      # lint frontmatter + cross-link graph
make report     # coverage / staleness report
make ci         # build + check (the local gate)
make test       # the tooling test suite
make publish-to-branch  # build docs + commit ./site to a local branch (push separately)
```

## Publishing your docs

`make build` produces a self-contained static site in `./site/` — host it anywhere
(GitHub Pages, GitLab Pages, Cloudflare Pages, Netlify, an object store, your own
server). Two convenient paths are built in:

**1. Commit to a branch (host-agnostic, manual).** `publish-to-branch` builds your
docs and commits the site to a local branch (default `gh-pages`) — nothing auto-runs,
and you push it yourself:

```
make publish-to-branch       # builds ./site and commits it to the gh-pages branch (local only)
git push <remote> gh-pages   # push when you're ready
```

Then point your host at that branch. **If you're on GitHub Pages:** Settings → Pages →
Source: Deploy from a branch → `gh-pages` / `(root)`. Override the branch with
`make publish-to-branch BRANCH=docs-site` (or set `BRANCH=` in `.env`).

**2. CI deploy (GitHub Actions, opt-in).** An inert
`.github/workflows/docs-publish.yml.example` builds and deploys on every push to
`main`. Rename it to `docs-publish.yml` and set the Pages source to **GitHub Actions**
to enable. Pick one path — a repo has a single Pages source — and nothing auto-runs
until you rename it.

## Contributing

Issues and PRs welcome. The system is meant to evolve: new page types are a template
+ a `PAGE_TYPES` entry in `tools/check.py` + an entry in the IA map. Run `make ci`
and `make test` before submitting.

## Licensing

**The scaffolding is offered under the MIT license** — that's everything in *this*
repo: the templates, the tools under `tools/`, the agent harness (`agent_docs/`), the
config (`Containerfile`, `Makefile`, `mkdocs.yml`), and the docs about the system
itself. The `example/` Beacon content is illustrative and fictional, also MIT.

**The documentation you author in a fork is yours.** When you fork this to document
your product, the pages your agents write under `docs/` are *your* content, under
whatever license you choose — the scaffolding's MIT terms don't claim them.

> There is deliberately **no top-level `LICENSE` file**: in a fork it would look like
> it covered your content. The scaffolding's terms are stated here instead. If you
> publish a fork, add your own `LICENSE` for *your* docs.

### Bundled tools

The toolkit image (`make build` etc.) installs third-party tools — invoked as tools,
not vendored into this repo's source — each under its own license:

| Tool | License |
|------|---------|
| MkDocs | BSD-2-Clause |
| Material for MkDocs · PyMdown Extensions · mkdocs-d2-plugin · mkdocs-glightbox · mkdocs-swagger-ui-tag | MIT |
| Mermaid (loaded by Material) | MIT |
| Swagger UI (via mkdocs-swagger-ui-tag) | Apache-2.0 |
| TypeSpec (`@typespec/*`) · Schemathesis · pytest | MIT |
| Prism (`@stoplight/prism-cli`) · AsyncAPI CLI · oasdiff | Apache-2.0 |
| **D2** | **MPL-2.0** |
| Base images (`python:3.12-slim`, `node:20-bookworm-slim`) | Debian + upstream (many) |

Everything is permissive (MIT / BSD / Apache-2.0) **except D2, which is MPL-2.0**
(weak, file-level copyleft) — fine for use as a rendering tool; worth knowing if you
redistribute the built image or modify D2 itself. Check each project for the
authoritative terms.
