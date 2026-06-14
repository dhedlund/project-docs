---
# Organic frontmatter — see templates/model.md for the full philosophy.
# REQUIRED:  title · type (datastore) · status
# SUGGESTED: reviewed_confidence (1–100) · last_reviewed (YYYY-MM-DD) ·
#            engine · sources · tags
title: <Datastore name>
type: datastore
status: unknown
reviewed_confidence:
last_reviewed:
engine:                   # e.g. MySQL 8 / PostgreSQL 16 / MongoDB 7 / RabbitMQ 3.13
tags: []
---

# <Datastore name>

> One or two sentences: what this store is and the role it plays.

## What lives here

The data this store holds, linked to the model pages it backs.

| Holds | Owned by | Notes |
|-------|----------|-------|
|  |  |  |

<!-- "Used by" (which services depend on this store) is generated automatically
     from each service's `depends_on` — you don't maintain it here. -->

## Notes & operations

??? info "Operational notes"
    Version, hosting, sizing, backup / retention — anything an operator needs.

!!! danger "Suspected dead"
    Tables / collections / queues that appear unused.
