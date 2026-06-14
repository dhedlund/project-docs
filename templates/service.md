---
# ─────────────────────────────────────────────────────────────────────────
# Organic frontmatter — see templates/model.md for the full philosophy.
#
# REQUIRED:  title · type (service) · status
# SUGGESTED: reviewed_confidence (1–100) · last_reviewed (YYYY-MM-DD) ·
#            language · provides_contracts · consumes_contracts ·
#            owned_models · depends_on · tags
# ─────────────────────────────────────────────────────────────────────────
title: <Service name>
type: service
status: unknown
reviewed_confidence:
last_reviewed:
sources:                  # provenance — see CONVENTIONS.md → Provenance
  # - repo: <name>
  #   branch: main
  #   sha:
  #   committed:
  #   paths: []
language:                 # java | ruby | elixir
provides_contracts: []    # TypeSpec/OpenAPI/AsyncAPI specs this service exposes
consumes_contracts: []    # contracts it depends on
owned_models: []          # model pages this service owns
depends_on: []            # other services, datastores, queues
tags: []
---

# <Service name>

> Treat this service as a **black box**: what it's responsible for, in one
> paragraph. What goes in, what comes out.

## Responsibilities & boundaries

What this service owns — and, just as important, what it explicitly does **not**.

## Interface (contracts)

The formal, validatable surface. The spec lives in `contracts/<this-service>/`
(start it from `templates/contract/`); link/embed the compiled OpenAPI (HTTP) and
AsyncAPI (events) here. See `contracts/README.md`.

- **Provides:** …
- **Consumes:** …

## Data it owns

Links to the model pages backed by this service.

## Key flows

Sequence diagrams for the important paths (UI → this service → data / downstream).

```mermaid
sequenceDiagram
  %% sketch a representative flow
```

## Notes & nuances

??? info "Operational notes / debt"
    Deployment quirks, scaling notes, known weak spots.

!!! danger "Suspected dead"
    Endpoints or branches that look unreachable. Record for confirmation.
