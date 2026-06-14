---
# Organic frontmatter — see templates/model.md for the philosophy.
# REQUIRED:  title · type (surface) · status
# SUGGESTED: reviewed_confidence · last_reviewed · sources · audience · tags
title: <Surface name>
type: surface
status: unknown
reviewed_confidence:
last_reviewed:
sources:
  # - repo: <frontend-repo>
  #   branch: main
  #   sha:
  #   committed:
audience:                 # e.g. end-users (B2C) / partners (B2B) / internal admins
tags: []
---

# <Surface name>

> Which app this is, who uses it, and what it's for — a frontend the product exposes
> (B2C app, partner portal, admin console, marketing site, …). Features that declare
> `surfaces: [<this>]` are listed automatically under "Surfaced here".

## What it offers

The capabilities exposed on this surface, in product terms. A capability can appear
on more than one surface and behave differently between them.

## Key screens

The main views and what each is for — link down to the flows/options where the
detail lives.

## Roles

Who can use it and at what access level (link the [roles & permissions](...) page).

## Notes & nuances
