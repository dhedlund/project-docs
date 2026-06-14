---
# Organic frontmatter — see templates/model.md for the full philosophy.
# REQUIRED:  title · type (glossary) · status
# SUGGESTED: reviewed_confidence (1–100) · last_reviewed (YYYY-MM-DD) · tags
title: Glossary
type: glossary
status: unknown
reviewed_confidence:
last_reviewed:
tags: []
---

# Glossary

The product's shared vocabulary — its *ubiquitous language*. Define each domain
term **once** here, link to the page that owns the concept, and use the same term
consistently everywhere else. Keep definitions to a sentence or two; depth lives on
the linked page. This is what stops agents (and people) from naming the same thing
three different ways across passes.

For a hover **tooltip** on a term anywhere in the docs, also add a one-line
`*[term]: short def` to `includes/abbreviations.md` (auto-appended to every page).

<!-- One entry per term, alphabetical. Each `### Term` gets a #term anchor you can
     link to. End with the canonical page that owns the concept. -->

### <Term>

Plain-language definition in one or two sentences. See: [<page>](<path>.md).
