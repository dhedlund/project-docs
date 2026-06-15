---
title: Reading the diagrams
type: overview
status: active
---

# Reading the diagrams

Our docs lean on diagrams to show how things fit together. This is a quick legend
for the symbols you'll see, plus how to drive the diagram viewer. You don't need to
read it end to end — jump to the type you're looking at. (In the fullscreen viewer,
the **How to read this diagram** link brings you straight to the right section, and
**Key** shows the same legend right beside the diagram.)

## Getting around a diagram {#controls}

Every diagram has an **expand** button (top-right, on hover) that opens a fullscreen
viewer:

- **Scroll or pinch** to zoom; **drag** to pan.
- **Esc**, the **✕**, or a click on the dark backdrop closes it. Clicking the
  diagram itself never closes it.
- **Key** shows the legend for that diagram's type without leaving the viewer.

Diagrams follow the site's light/dark theme automatically.

## Flowcharts {#flowchart}

Flowcharts show **steps and how control or data moves between them**.

- **Boxes** are steps or components; a **rounded box** is often a start/end or a
  process, and a **diamond** is a decision or branch.
- **Arrows** show direction of flow. A **label on an arrow** is the condition or
  event that takes you down that path ("yes" / "no", a triggering action).
- A **dotted arrow** usually means a weaker, optional, or asynchronous link.
- A **labelled box around several nodes** (a subgraph) groups things that belong
  together — a service, a subsystem, a phase.

[Full syntax reference →](https://mermaid.js.org/syntax/flowchart.html)

## Sequence diagrams {#sequence}

Sequence diagrams show **a conversation over time** — who calls whom, in order.

- Each **vertical line (lifeline)** is a participant; **time flows top to bottom**.
- A **solid arrow with a filled head** is a call or message; a **dashed arrow with
  an open head** is the reply or return.
- A **narrow bar** on a lifeline shows when that participant is busy handling
  something (an activation).
- Boxes labelled **`alt` / `opt` / `loop` / `par`** wrap steps that are
  alternative, optional, repeated, or parallel.
- An arrow that loops back to the same lifeline is an internal step.

[Full syntax reference →](https://mermaid.js.org/syntax/sequenceDiagram.html)

## Entity-relationship diagrams {#er}

ER diagrams show **data entities (think tables) and how they relate**.

- **Boxes** are entities; the rows inside are their fields, often with a type and a
  key marker (PK = primary key, FK = foreign key).
- **Lines** connect related entities.
- The **"crow's-foot" ends** give the cardinality: a bar `|` means *one*, a circle
  `o` means *zero (optional)*, and the splayed foot means *many*. So a line ending
  `||--o{` reads "exactly one … to … zero-or-many".

[Full syntax reference →](https://mermaid.js.org/syntax/entityRelationshipDiagram.html)

## State diagrams {#state}

State diagrams show **the states something moves through and what triggers each
move**.

- **Rounded boxes** are states.
- **Arrows** are transitions; the label is the trigger or event that causes it.
- A **filled dot** marks the start; a **dot inside a ring** marks an end state.
- A box **nested inside another** is a composite (sub-)state.

[Full syntax reference →](https://mermaid.js.org/syntax/stateDiagram.html)

## Class diagrams {#class}

Class diagrams show **types and their relationships** — structure, not time.

- **Boxes** have up to three compartments: name, attributes, methods.
- **Lines** show relationships: a **hollow triangle** points to a parent
  (inheritance); a **plain line or arrow** is an association; a **diamond** is
  aggregation or composition (a whole–part relationship).
- **Numbers** at the ends are multiplicities (`1`, `0..*`, `1..*`).

[Full syntax reference →](https://mermaid.js.org/syntax/classDiagram.html)

## Architecture ("hero") diagrams — D2 {#d2}

We use **D2** for larger architecture diagrams where layout quality matters.

- **Boxes** are services or components; a **box nested inside another** means
  containment — a system and the parts inside it.
- **Connections** are calls or data flow; their labels say what flows.
- **Shapes carry meaning** — for example a cylinder is a datastore and a queue
  shape is a message queue.
- Light and dark variants follow the site's theme.

[Full syntax & shapes →](https://d2lang.com/)
