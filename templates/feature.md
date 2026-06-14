---
# ─────────────────────────────────────────────────────────────────────────
# Organic frontmatter — see templates/model.md for the full philosophy.
#
# REQUIRED:  title · type (feature) · status
# SUGGESTED: reviewed_confidence (1–100) · last_reviewed (YYYY-MM-DD) ·
#            uses_services · uses_models · tags
# ─────────────────────────────────────────────────────────────────────────
title: <Feature name>
type: feature
status: unknown
reviewed_confidence:
last_reviewed:
sources:                  # provenance — see CONVENTIONS.md → Provenance
  # - repo: <name>
  #   branch: main
  #   sha:
  #   committed:
  #   paths: []
uses_services: []
uses_models: []
tags: []
---

# <Feature name>

> What the user can do and why it matters — product language first.

## User journey

Step-by-step from the user's perspective.

## How it works

The walk-through that connects **UI → API(s) → data**. Link down into the
relevant service and model pages at the moments they come into play, so a reader
can drop to the right level of detail exactly when they need it.

```mermaid
sequenceDiagram
  %% UI -> service(s) -> data
```

## Services & data involved

- **Services:** …
- **Models:** …

## Notes & nuances

??? note "Edge cases & historical behavior"
    Quirks, special cases, behavior that changed over time.

!!! danger "Suspected dead"
    Flows or options that appear no longer reachable.
