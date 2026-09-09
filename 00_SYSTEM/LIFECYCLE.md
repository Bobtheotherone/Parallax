# Project Lifecycle

The control plane must survive model swaps, target-version changes, new competitions, long pauses, and large handoffs without accumulating an unreadable current state.

## Stage 0 — Bootstrap

1. Establish `SCOPE.md`.
2. Register source packs in `SOURCE_PACKS.md`.
3. Initialize `WORLD.md` with only evidence-supported facts.
4. Create a fresh strategy epoch.
5. Seed `CAPABILITIES.md` from reusable engines already available.
6. Leave inherited strategy out unless explicitly imported as historical context.

## Stage 1 — Active campaign

Maintain the hot set:

- `NOW.md`: ≤100 lines;
- `HYPOTHESES.md`: only active or recently falsified hypotheses;
- `RUN_QUEUE.md`: pending/in-flight/recently completed runs;
- `FORGE_QUEUE.md`: open/recently delivered needs.

Everything else can grow through append-only ledgers and archives.

## Stage 2 — Epoch transition

Create a new epoch when one of these changes materially:

- objective or challenge phase;
- target generation or protocol family;
- scope;
- principal model;
- major world-model correction;
- strategic framing;
- handoff to a materially different reasoning model;
- previous strategy becomes a retrieval hazard.

At transition:

1. freeze the old epoch;
2. write an `EPOCH_HANDOFF` record;
3. archive old ranked hypotheses;
4. carry forward only evidence-backed world facts;
5. explicitly list unresolved unknowns;
6. start a new `NOW.md` and active hypothesis set;
7. retain old strategy as opt-in history.

## Stage 3 — Handoff / epistemic reset

A strong handoff minimizes inherited conclusions and maximizes reconstructable evidence.

Recommended cold-start order:

1. scope;
2. current neutral world state;
3. current objective/blocker;
4. anomalies/contradictions;
5. closures with `DOES_NOT_PROVE` and `REOPEN_IF`;
6. capability registry and open Forge needs;
7. source-pack inventory;
8. raw evidence only as needed;
9. historical strategy last.

A handoff is a snapshot, not a new source of truth by itself.

## Stage 4 — Compaction

When a hot file becomes noisy:

- move completed entries into archive indexes;
- retain stable IDs;
- keep a one-line tombstone or supersession pointer;
- never renumber IDs;
- never delete receipts solely because the conclusion changed.

## Stage 5 — Capability maturation

A campaign-specific failure should become:

1. a minimized generic fixture;
2. a regression test;
3. a capability version bump;
4. an `EVALS.md` result;
5. a `LESSONS.md` entry if the lesson generalizes.

This is how the system compounds across competitions.

## Stage 6 — Campaign retirement

At retirement:

- close or expire queued runs;
- record cleanup obligations and their disposition;
- freeze final scope revision;
- freeze final world revision;
- freeze capability versions used;
- write final unresolved questions;
- archive active strategy;
- mark whether evidence can be safely reused in future campaigns.

## Long-term rules

- Never depend on one ZIP layout.
- Never depend on one model name.
- Never depend on current local filesystem paths.
- Never assume a prior target namespace will exist forever.
- Never let a generated materialized view outrank its receipts.
- Never import historical strategy into default retrieval without an explicit reason.
