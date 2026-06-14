---
# Organic frontmatter — see templates/model.md for the philosophy.
# REQUIRED:  title · type (integration) · status
# SUGGESTED: reviewed_confidence · last_reviewed · sources · domain · tags
title: <Provider> integration
type: integration
status: unknown
reviewed_confidence:
last_reviewed:
sources:
  # - repo: <name>
  #   branch: main
  #   sha:
  #   committed:
tags: [integration]
---

# <Provider> integration

> A third-party system *we* depend on, and what we use it for. (Services list it in
> `depends_on`, so "Depended on by" is generated automatically.)

## What we use it for

The capability it provides us, and which of our flows/services rely on it.

## Interface

- **Direction** — what we send / what we receive (including their webhooks to us).
- **Auth & secrets** — how we authenticate (reference only, never values).
- **Environments** — sandbox vs production.

## Failure modes

How it fails and how we handle it — timeouts, retries, fallbacks, and what the user
sees.

## Notes & nuances

!!! danger "Suspected dead"
    Features of the integration we no longer use.
