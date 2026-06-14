# Orchestration: dispatching and integrating doc work

The outer loop: how a session drives doc work through subagents, and how all tool
work stays inside the portable sandbox. The inner loop (`loop.md`) still governs
each unit of work — a subagent writing a page owes the same reflection and routing
as a solo session.

Invariants here are stable; mechanisms (scripts, image tags) evolve. When they
conflict, the invariant wins and the mechanism gets fixed.

## Sandbox execution model

All tooling runs through the universal container image
(`localhost/project-docs-toolkit`), on **Podman or Docker** — never against
host-installed tools. This is what makes the setup portable (Linux and macOS alike)
and contained. See `TOOLKIT.md`.

- **Building docs is hermetic.** `make build` runs `--network none`,
  `--cap-drop=ALL`, `no-new-privileges`. A docs build needs no network; enforcing
  that proves no exfiltration.
- **Source code is read-only.** Mount the code per
  `agent_docs/stewardship/source-of-truth.md` as a **read-only** volume (or read it
  via whatever access that doc specifies). Agents document the code; they never
  modify it.
- **Reaching a live service stack is the exception.** Contract proxying /
  conformance (Prism, Schemathesis) needs network to the stack and is run
  deliberately, scoped per task, with only the network it needs — not by loosening
  the default build posture. See `TOOLKIT.md` → "Interacting with a live service
  stack."

## The main-branch invariant

The docs repo on `main` stays buildable at every commit:

- always on `main`, never a stray branch;
- never holds a broken `make ci`;
- `make ci` (build + check) green at every commit boundary.

Implementation work happens in isolated worktrees/branches; `main` integrates
finished work.

## Solo vs orchestrated

Single-stream is the default — cheaper to reason about. Orchestration earns its
overhead when the queue holds genuinely independent pages (different
services/domains, no shared cross-links being reshaped) or when an audit/research
thread can run alongside authoring.

Either way the plan stays single-stream: one *Now* item. Parallel dispatch is an
execution detail inside it, not a second plan stream. The real contention here is
**git on `plan.md` / `backlog.md`** — serialize edits to those.

## Dispatch protocol

- **One orchestrator owns `main`.** Subagents commit on their own branch/worktree;
  integration is the orchestrator's job.
- **Shared base.** Reset each worktree to current `main` before dispatch.
- **Disjoint only.** Two agents reshaping the same pages — or the same cross-link
  neighbourhood — serialize.
- **Ripple becomes a backlog entry, not a cross-agent edit.** The loop's ripple
  discipline (a change propagating to related pages) is a cross-link-neighbourhood
  operation, which fights disjointness. Under orchestration, a ripple that reaches
  into another in-flight agent's pages is filed as a `DOC-VERIFY` (the orchestrator
  reconciles overlapping ripple entries at integration), never edited in-pass.
  Parallelism trades ripple-immediacy for throughput.
- **Self-contained briefs.** A brief carries everything a cold agent needs: the
  page(s) and their definition of done (the `audit-checklist.md` type), how to
  reach the source, constraints, and where findings route. It doubles as the
  recovery contract if the agent dies.
- **Delete-on-completion, never tombstone.** The brief instructs the agent to
  **remove** the landed `backlog.md` entry and record completion in the commit
  message. Same rule binds the orchestrator at integration.

## Supervising dispatched work

- **Context exhaustion = triage.** If a result smells truncated, diff what shipped
  against the definition of done; whole sections can be missing.
- **Resume minimally.** An agent that hit a transient error resumes with
  "Continue.", not a re-prompt (re-explaining makes it redo finished work).
- **Harvest before discharge.** Collect the agent's found-but-not-fixed
  observations (loop Q1/Q9) and route them — discoveries die in closed transcripts.

## Integration protocol

Per merge batch, in order:

1. **Review first** — a fresh-eyes review (never self-review) has happened and its
   findings are addressed.
2. **Verify your own state** — `pwd` + `git log` before merging; after worktree
   hopping the CWD is often not where you think.
3. **Linear history** — ff-only / rebase / cherry-pick; no merge commits.
4. **CI gates the batch** — `make ci` (build + check) green on the integrated
   result before it counts as landed.
5. **Verify `main`'s state** — on `main`, clean, fast-forwarded.
6. **Clean up** — delete merged branches; reset/remove worktrees.

Work is "done" only when `make ci` is green on `main` and `plan.md` reflects it.
