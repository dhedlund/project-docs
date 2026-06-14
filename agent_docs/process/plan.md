# Plan

The rolling plan: *Now* plus the immediately-next item. Read every loop iteration,
so keep it small (target ≤ ~200 lines). The durable queue lives in `backlog.md`;
per-page detail lives on the pages themselves. See `agent_docs/process/loop.md`.

## Update protocol

- *Now* is the in-progress item plus, at most, the immediately-next one — not a
  running history of the milestone.
- *Last completed* is capped at one item and overwritten each time (the git log is
  the canonical history).
- *Recent discoveries* is distilled into durable destinations and **emptied** at
  each loop step; a non-empty section after a commit means the loop wasn't
  followed.
- Queued work behind *Now* goes to `backlog.md`. *Open questions* is for
  genuinely-undecided items only.

## Where <product> is

_(One paragraph: what's documented, what's stubbed, what's in flight.)_

## Now

_(The current work-unit and its definition of done — the page type's checklist in
`agent_docs/process/audit-checklist.md`. Name the source to work from.)_

## Up next

_(The immediately-next item.)_

## Last completed

_(One item; overwrite each time.)_

## Recent discoveries

_(Empty per the update protocol.)_

## Open questions

_(Genuinely-undecided items only.)_
