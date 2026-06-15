# Voice & tone

How our docs should *feel* to read: friendly, clear, and respectful of the
reader's time. The goal is documentation people actually enjoy and trust, the way
the best language and library docs do.

**Prime directive: clarity and natural reading win.** Everything below is guidance
for getting there, not a rulebook to obey. If following a guideline makes a
sentence worse, break it. Awkward prose that satisfies every rule is worse than
natural prose that bends a few. Don't write in a narrow, stilted band trying to
stay "on style."

## The feel we're after

This voice is distilled from documentation widely regarded as friendly and
approachable. **Everything you need to write well is in this doc — it's
self-contained.** You don't need to go read anything, and you shouldn't fetch
remote sites mid-loop. (For human curiosity: the Elixir / HexDocs guides are a good
touchstone for the feel — warm, direct, example-first, never condescending — and we
borrow Diátaxis's idea of organizing by purpose. Inspiration and credit, not
required reading.)

Organize by purpose: a **guide** walks someone along a path (narrative, second
person, hands-on); **reference** states the shape precisely and scannably; our
model/service/feature pages run business → technical (the depth ladder in
`CONVENTIONS.md`). Match the mode you're in.

## The principles

- **Write to a person.** Second person, present tense, active voice. "You call
  `update/2`; the runtime renders the result," not "the result is rendered by the
  runtime upon invocation."
- **Lead with the concrete.** Show the thing first (an example, a command, a small
  table), then explain it. People learn from the specific and generalize.
- **Just enough, just in time.** Tell the reader what they need *here*, and link
  deeper rather than dumping everything at once. Depth is a click away, not in the
  way.
- **Rich, not padded — and not a stub.** "Just enough" is about cutting *filler*,
  never about being shallow. A good page tells the whole story: the *why*, the edge
  cases, the permutations, how it connects to the rest. The pages under `example/`
  are the depth bar — study them and match that richness. A short, sparse page is a
  *stub to finish*, not the standard to copy; don't mistake brevity for done.
- **Anticipate the reader.** Surface the gotcha or the "why" right before they'd
  hit it, and reassure where something looks scarier than it is ("a bad value here
  won't corrupt anything; it's rejected with a clear error").
- **Plain words, precise meaning.** Prefer the simple word; define a term the first
  time it appears; don't perform expertise. Precise and plain are not opposites.
- **Earn trust with specifics.** Name real things and real outcomes ("you'll see a
  `past_due` status"), not vague hand-waving. This is the same instinct as our
  confidence/provenance discipline: say what's true and verifiable.
- **Let it breathe.** Short paragraphs, lists, and headers beat dense walls. When
  in doubt, spread vertically.
- **Respect the reader.** No filler, no marketing, no condescension. Assume
  intelligence; supply context.

## It evolves

Tone is something we'll refine over time, not nail on the first try. Treat this as
a living starting point. If a pattern keeps working (or keeps grating), update this
doc. Consistency across pages matters more than any single rule, and a shared,
relaxed voice beats a rigid one.
