---
# Organic frontmatter — see templates/model.md for the philosophy.
# REQUIRED:  title · type (api) · status
# SUGGESTED: reviewed_confidence · last_reviewed · sources · domain · tags
title: <API name>
type: api
status: unknown
reviewed_confidence:
last_reviewed:
sources:
  # - repo: <name>      # and the spec project in contracts/<api>/
  #   branch: main
  #   sha:
  #   committed:
tags: [api]
---

# <API name>

> What this API is for and who uses it (customers / partners / internal). One
> paragraph, integrator-facing.

## Basics

- **Base URL / environments** — sandbox vs production.
- **Auth** — how to authenticate (link the auth page).
- **Versioning & deprecation** — the policy and how breaking changes are signalled.
- **Pagination, rate limits, errors** — the conventions every endpoint follows.

## Reference

The endpoint reference is rendered from the OpenAPI spec. Put the compiled spec at
`docs/interfaces/api/openapi.yaml` (from `contracts/<api>/`), enable the
`swagger-ui-tag` plugin in `mkdocs.yml` (it's already in the toolkit image), then
embed it:

```html
<swagger-ui src="openapi.yaml"/>
```

## Guides

Link the how-to guides (auth, common tasks, webhooks, SDKs).

## Notes & nuances

??? info "Changelog"
    Notable changes; link the full changelog.
