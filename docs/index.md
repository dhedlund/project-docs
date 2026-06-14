---
title: Overview
type: overview
status: unknown
---

# Project Docs

The product-wide knowledge base. Start here and drill down into whichever layer
answers your question.

## The layers

- **[Features](features/index.md)** — what the product does, in product language,
  and how each capability works end to end.
- **[Services](services/index.md)** — each backend service as a black box: its
  responsibilities and its formal, testable contracts.
- **[Models](models/index.md)** — the data and domain models, and how they map to
  the databases and queues behind them.
- **[Datastores](datastores/index.md)** — the databases and queues the services
  depend on, and what each one holds.
- **[Glossary](glossary.md)** — the product's shared vocabulary.
- **[Decisions](decisions/index.md)** — the *why*: architecture decision records.

## How to read this

Pages link **up and down** between layers. A feature points down into the services
and models it uses; a model points up to the features and service that depend on
it. Follow the links to land at the right level of detail for your question.

Each page also carries a confidence score and the date it was last reviewed —
treat low-confidence or stale pages with appropriate caution.

> New here as an author? Read **CONVENTIONS.md** at the repo root first.
