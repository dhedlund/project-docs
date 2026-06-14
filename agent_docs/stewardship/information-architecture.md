# Information architecture

The map of *where each kind of information lives*. When you have something to
document, find its home here and put it there, in that shape. This is the routing
authority the loop points to.

Two rules:

- **One home per kind.** Don't scatter the same kind of information across places.
- **Not every product has every home.** The bootstrap creates the homes that apply
  (and adds them to nav); the near-universal ones ship in the scaffold. A home that
  doesn't apply simply doesn't exist — that's fine.

## The zones

### Product — what users can do
- **Domain** — `docs/domains/` · `templates/domain.md`. The epic-level grouping and
  hub for an area; lists its capabilities. Features/flows declare `domain:` and are
  listed back automatically. Use these to keep `features/` navigable as it grows.
- **Feature** — `docs/features/`. A vertical journey (UI → API → data).
- **Flow** — `docs/flows/` · `templates/flow.md`. Behaviour that *varies*: a selector
  matrix + per-variant paths + worked permutations. For payment variations,
  availability rules — anything combinatorial.
- **Options / configuration** — `docs/options/` · `templates/options.md`. Settings,
  their meanings/values/defaults, and crucially their *interactions*.
- **Glossary** — `docs/glossary.md`. Shared vocabulary.

### Surfaces — which apps expose it, and to whom
- **Surface** — `docs/surfaces/` · `templates/surface.md`. Each frontend (B2C app,
  partner/B2B portal, admin console, marketing/status site). Features tag
  `surfaces:`; the surface page lists them back. A capability can appear on several
  surfaces and differ between them.
- **Roles & permissions** — `docs/access/` · `templates/roles.md`. Who can do what.

### Interfaces — the programmatic surface for integrators
- **API** — `docs/interfaces/api/` · `templates/api.md`. Public/partner API: overview
  + auth/pagination/errors/versioning guides + the rendered reference (Swagger UI
  from the OpenAPI; enable the `swagger-ui-tag` plugin, already in the image).
- **Webhooks** — `docs/interfaces/webhooks/` · `templates/webhook.md`. Outbound
  events: catalog + delivery semantics (at-least-once, idempotency, signing, order).
- **SDKs** — `docs/interfaces/sdks/` · `templates/sdk.md`. Per-language clients.
- **Auth** — `docs/interfaces/auth.md`. API auth methods, scopes, app registration.

### Internals — how it's built (engineer-facing)
- **Service** `docs/services/` · **Model** `docs/models/` · **Datastore**
  `docs/datastores/` · **Decision / ADR** `docs/decisions/`.

### Integrations — third parties we consume
- **Integration** — `docs/integrations/` · `templates/integration.md`. Each external
  system we call (payments, email/SMS, CRM, storage). Services list it in
  `depends_on`; the integration page lists them back.

### Specs — the machine-readable substrate
- **Contracts** — `contracts/` · `templates/contract/`. TypeSpec → OpenAPI/AsyncAPI
  for both internal service boundaries and public APIs/webhooks. The specs, not the
  prose; verified by `oasdiff` / `schemathesis` / `prism`.

## Relationships to keep straight

- **Specs vs docs.** `contracts/` holds specs; `docs/interfaces/` explains the
  *public* ones; `docs/services/` link the *internal* ones. The same OpenAPI can be
  both an internal contract (verified) and the basis of public API docs.
- **Internal events ≠ webhooks.** Messaging between *our* services is internals;
  events we send to *customers* are webhooks. Both AsyncAPI, different homes.
- **Integrations (inbound: we call them) ≠ interfaces (outbound: they call us).**
  Opposite directions; separate zones.
- **Surfaces cross-cut features.** Don't duplicate a feature per surface; tag
  `surfaces:` and note the per-surface differences.

## Adding a home

When a product first has (say) a public API, the bootstrap — or any later pass —
creates `docs/interfaces/api/`, an index page, the nav entry, and a stub from the
template, then deepens it. New pages must be added to nav (`mkdocs --strict`
enforces it).
