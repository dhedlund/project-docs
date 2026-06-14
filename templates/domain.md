---
# Organic frontmatter — see templates/model.md for the philosophy.
# REQUIRED:  title · type (domain) · status
# SUGGESTED: reviewed_confidence (1–100) · last_reviewed (YYYY-MM-DD) · tags
title: <Domain name>
type: domain
status: unknown
reviewed_confidence:
last_reviewed:
tags: []
---

# <Domain name>

> One paragraph, in product language: what this area of the product is about. A
> domain is the epic-level grouping above features — the hub and map for an area.

## Capabilities

What this domain lets users do — the breadth, in plain terms. Each links to where
it's documented in depth.

- **<Capability>** — one line; see [<feature / flow>](...).

## How it fits together

A short orientation: the main services, models, and flows in this domain and how
they relate.

```mermaid
flowchart LR
  %% the shape of this domain
```

<!-- Features / flows / services / models that declare `domain: <this>` are listed
     automatically under "In this domain" (generated from their frontmatter). -->

## Notes & nuances

??? info "Boundaries"
    What's in this domain, and what belongs to a neighbouring one.
