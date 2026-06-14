---
# Organic frontmatter — see templates/model.md for the philosophy.
# REQUIRED:  title · type (flow) · status
# SUGGESTED: reviewed_confidence · last_reviewed · sources · uses_services ·
#            uses_models · domain · surfaces · tags
title: <Flow name>
type: flow
status: unknown
reviewed_confidence:
last_reviewed:
sources:
  # - repo: <name>
  #   branch: main
  #   sha:
  #   committed:
uses_services: []
uses_models: []
domain:
tags: []
---

# <Flow name>

> What this flow accomplishes, and what makes it *vary* — the conditions that pick
> one path over another (payment method, payout config, resource type, account
> state, …). Use this shape when the behaviour is a combinatorial surface, not a
> single journey.

## Which variant applies (selector)

The decision surface: conditions → which variant runs. **Mark invalid / unsupported
combinations explicitly** — permutation spaces are full of illegal cells.

| <dimension A> | <dimension B> | → variant |
|---------------|---------------|-----------|
|  |  |  |

## Variants

A short section per distinct path: its trigger conditions and its flow.

### <Variant 1>

When: <conditions>.

```mermaid
sequenceDiagram
  %% this variant's path
```

## Worked scenarios

The genuinely tricky permutations, walked end to end — this is where the value is.

??? example "<a gnarly combination>"
    Step through what happens, and why.

## Notes & nuances

!!! danger "Suspected dead"
    Variants or branches that look unreachable.
