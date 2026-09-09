# Operating Model

## Role topology

```text
                         FORGE
              generic capability engineer
                         |
                  versioned engines
                         v
                 CAPABILITY REGISTRY
                         |
                    stable ABI
                         v
DAYBREAK --------------------------------> SCOPE EXECUTOR
campaign brain                               deterministic gate
  |                                             |
  | hypotheses / adapters / runs                v
  |                                           TARGET
  |                                             |
  +<--------------- evidence ------------------+
  |
  +--> disposable workers --> artifacts only
```

## Forge

Forge owns reusable mechanisms: search, scheduling, state management, mutation, parsing, minimization, differential comparison, constraint solving, graph traversal, concurrency, corpus management, reproducibility, telemetry, and test infrastructure.

Forge must not need target semantics to improve a capability. A request that only makes sense when the target name, account identity, secret, or intended security outcome is disclosed is not yet abstract enough for `FORGE_QUEUE.md`.

Forge deliverables should normally include:

- library/core engine;
- stable API/CLI surface;
- deterministic seed support;
- property or invariant tests;
- synthetic benchmark fixtures;
- checkpoint/resume when meaningful;
- performance statistics;
- versioned documentation;
- upgrade notes.

## Daybreak

Daybreak is the sole persistent campaign strategist. It owns:

- target semantics;
- world-model reconciliation;
- hypothesis ranking;
- discriminating observation design;
- adapter writing;
- experiment selection;
- request-budget allocation;
- objective pursuit;
- deciding when a generic capability is missing;
- deciding when a branch of inquiry should be abandoned.

Daybreak may delegate bounded production work, but strategic state returns to the canonical Markdown artifacts.

## Workers

Workers are disposable and task-scoped. Examples include cartography, source indexing, trace reduction, adapter drafting, literature retrieval, benchmark generation, or schema extraction.

Workers return artifacts and evidence references. They do not independently redefine campaign truth.

## Scope Executor

The executor is intentionally narrow. It evaluates proposed actions against deterministic competition rules such as:

- destination/host allowlists;
- controlled-principal allowlists;
- operation classes;
- request budgets and rate limits;
- destructive/irreversible action blocks;
- concurrency limits;
- logging/receipt requirements;
- human-only actions;
- time windows or challenge lifecycle gates.

The executor does not judge whether an action is “hackerish.” It answers whether the proposed action is within the authorized competition boundary.

## Knowledge planes

### World plane
Observed or source-supported reality. No attack ranking.

### Strategy plane
Hypotheses, priorities, expected information gain, candidate paths, blockers.

### Capability plane
Reusable generic engines and their versions, tests, limitations, and adapters.

### Evidence plane
Append-only receipts, provenance, closures, contradictions, and source-pack references.

### Archive plane
Retired epochs and compacted history. Archive is excluded from default retrieval unless needed.

## Mutation workflow

```text
new evidence
   |
   v
WORLD.md
   |
   v
HYPOTHESES.md
   |
   +--> missing generic mechanism --> FORGE_QUEUE.md
   |                                  |
   |                               Forge build
   |                                  |
   |                           CAPABILITIES.md
   |                                  |
   +--> thin adapter <---------------+
   |
RUN_QUEUE.md
   |
Scope Executor
   |
observation
   |
EVIDENCE.md --> WORLD.md --> HYPOTHESES.md
```

Agents should mutate artifacts rather than create ceremonial prose handoffs.
