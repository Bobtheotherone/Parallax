# Development workflow: solve the engineering problem

This guide is for implementing or reviewing Parallax itself. It is deliberately different from the [task-synthesis protocol](../../core/PROTOCOL.md): repository development should optimize for a strong engineering result, not for performing a fixed sequence of roles or status transitions.

The goal of an episode is a coherent change that satisfies the real contract with good architecture, appropriate technical leverage, and evidence for the claims that matter.

## 1. Compress the problem before changing code

Read the requested spec/task and the code that owns the behavior. Build a compact working model:

```text
required outcome
  -> observable interfaces / callers
  -> invariants and compatibility constraints
  -> data and state transitions
  -> resource / performance constraints
  -> unknowns that can change the design
  -> acceptance mechanism
```

Before implementation, you should be able to answer:

- What externally observable behavior must become true?
- What must remain unchanged?
- Which module/component owns each relevant invariant?
- Where do data, control, state, errors, and capabilities cross boundaries?
- Which constraints are hard gates versus optimization goals?
- What assumptions are genuinely unresolved?
- What evidence would distinguish a correct solution from a plausible-looking one?

Do not turn this into a required planning document. The output is a better mental model and, where useful, a short implementation plan.

## 2. Inspect the system at the level the task requires

Start from the narrow route, then widen context when a concrete dependency demands it. Follow actual call/data flow rather than recursively reading documentation because it exists.

For difficult changes, inspect enough surrounding code to understand:

- dependency direction and public interfaces;
- ownership of mutable state and lifecycle;
- concurrency/async boundaries and synchronization;
- error propagation, retries, cancellation, and partial failure;
- allocation, I/O, serialization, caching, and resource lifetime;
- numerical/data-layout assumptions;
- observability needed to diagnose production or benchmark failures;
- compatibility constraints with persisted data, protocols, callers, or external tools.

A small diff can still be architecturally wrong. Prefer the smallest **coherent** change, not the smallest number of edited lines.

## 3. Choose the strongest existing leverage

Before inventing machinery, compare the plausible implementation routes:

- ordinary code in the existing architecture;
- a mature library/API already suited to the problem;
- a small local abstraction that removes repeated complexity;
- an existing Parallax semantic interface;
- a new representation or backend only when it exposes useful structure unavailable elsewhere.

Select algorithms and data structures from the actual constraints: asymptotics, data volume, mutability, access pattern, memory pressure, concurrency, latency, target hardware, and failure semantics. Do not choose a framework or DSL merely because it appears more sophisticated.

For performance-sensitive work, reason about the likely bottleneck before coding: compute complexity, allocations, cache locality, vectorization/batching, synchronization, I/O, serialization, device transfer, or numerical precision. A benchmark should test that hypothesis later.

## 4. Use reversible autonomy

Proceed without blocking when an ambiguity is local, reversible, and does not materially alter externally visible semantics, safety, compatibility, or an irreversible architecture decision. Choose the simplest conventional default consistent with the repository and keep the choice easy to replace.

Stop or seek an explicit decision when uncertainty can materially change:

- task/output semantics or acceptance;
- a stable protocol/semantic identity;
- security or capability boundaries;
- externally meaningful compatibility;
- destructive/irreversible data or repository behavior;
- an architectural commitment whose reversal would be expensive or unsafe.

First search the repository and available authoritative sources. Do not ask a human to answer a question the code, spec, compiler, or a small experiment can answer directly.

## 5. Implement along real boundaries

Plan work around dependencies rather than document sections. A good sequence often establishes interfaces/invariants first, then the core mechanism, then adapters/integration, then task-specific verification.

During implementation:

- keep dependency direction explicit;
- make invalid states unrepresentable where practical;
- keep state ownership and mutation sites obvious;
- preserve useful source/debug correspondence across transformations;
- return errors with enough information to localize the violated boundary;
- avoid hidden global behavior and convenience coupling;
- expose observability where failure diagnosis would otherwise require guesswork;
- preserve caller data/compatibility when the contract requires it.

When touching legacy or partially implemented systems, prefer compatibility adapters and incremental seams over a broad rewrite unless the existing abstraction is the root cause and the requested scope can safely replace it.

Generated capsules/programs remain data under [ADR-0002](../architecture/decisions/0002-data-not-authority.md). A repository implementation episode cannot grant generated artifacts new host authority as a convenience.

## 6. Use tools as experiments

A compiler, test runner, debugger, profiler, static analyzer, reference implementation, search tool, trace, or benchmark is valuable when it resolves uncertainty.

Use the loop:

```text
observe -> localize -> competing hypotheses -> discriminating experiment
        -> root-cause repair -> focused recheck -> relevant regression
```

Examples:

- compiler/type error: inspect the interface/invariant it exposes before suppressing it;
- behavioral mismatch: minimize the counterexample and compare state at the first divergence;
- performance regression: profile before rewriting; measure the changed bottleneck afterward;
- concurrency failure: isolate ownership/order assumptions and use deterministic/fault/race tools where possible;
- compatibility failure: compare exact serialized/API/CLI observations at the boundary;
- missing capability: prove the missing mechanism is actually required before expanding the trusted surface.

Avoid blind cycles of “edit → entire suite → edit.” Broad suites are useful final regression instruments; narrow experiments are usually better diagnostic instruments.

See [VERIFICATION](VERIFICATION.md) for choosing evidence by claim.

## 7. Verification is part of design

Derive checks from the contract and architecture while implementing, not only after. Tests should distinguish plausible mistakes; static structure should enforce invariants it can express; benchmarks should test real bottlenecks; reference/differential paths should be independent enough to expose shared assumptions.

Keep these questions separate where Parallax semantics are involved:

1. Is the artifact structurally admitted?
2. Does lowering/expansion preserve its declared meaning?
3. Does execution produce the intended runtime observation?
4. Does the external task contract accept that observation?

A green typecheck or execution result does not answer question 4.

After a repair, rerun the smallest checks that cover the repaired mechanism and its likely regressions. Before completion, run the spec's required acceptance checks and any additional checks justified by changed behavior.

## 8. Review for mechanism, not style theater

Review the exact diff and ask what can still be wrong.

Prioritize:

- contract violations or missing cases;
- incorrect algorithms or complexity;
- broken dependency direction/state ownership;
- compatibility drift;
- race/resource/error-path defects;
- unsupported security or numerical assumptions;
- performance regressions or unmeasured claims;
- tests that only mirror the implementation;
- scope changes that quietly alter semantics or authority.

A useful review finding identifies consequence and mechanism. There is no minimum finding quota. Self-review and same-model review can catch defects but do not become an independent task oracle by renaming the role.

Fix root causes when practical. If a finding is intentionally deferred, state the remaining risk rather than burying it in process history.

## 9. Status and records are bookkeeping, not the algorithm

Implementation specs currently use YAML states:

| State | Meaning |
|---|---|
| `draft` | contract is not yet sufficient for the intended work |
| `ready-for-dev` | implementation can begin without a known blocking contract decision |
| `in-progress` | implementation work is underway |
| `in-review` | a candidate exists and awaits required review/acceptance work |
| `done` | the spec's required acceptance/review policy is satisfied |
| `blocked` | a material unresolved dependency prevents safe progress |

Keep the state truthful when the selected spec/workflow requires it, but do not perform status changes as a substitute for engineering. A failed check is information; preserve it when it matters, fix the system, and continue. Do not erase history to make an episode look cleaner.

For measured trials, changing the task or acceptance policy after seeing results creates a new version/trial. For ordinary development, Git already preserves prior revisions; do not duplicate a narrative of every edit unless it aids future diagnosis or a spec explicitly requires it.

## 10. Completion criterion

Finish when the requested outcome is implemented, required hard constraints are satisfied, relevant acceptance checks pass, and no unresolved high-impact finding is being disguised as success.

A missing optional tool is not a reason to fabricate evidence. A missing required oracle/security/performance environment may leave the corresponding claim unestablished even if the code is otherwise reviewable. Report that precise boundary.

Commit coherent changes on the intended branch. Do not modify unrelated files, rewrite concurrent user work, force-push over others, or broaden the roadmap because adjacent work looks interesting.

## Documentation and durable lessons

Update an authoritative document only when the implementation changes the truth it owns. Keep historical/provenance records historical. Run `python tools/check_docs.py` when live documentation or links change.

A lesson deserves durable guidance when it captures a recurring engineering invariant, failure mode, or decision rule. Do not paste an episode transcript into agent instructions. The point of documentation is to improve the next solution, not to prove that the previous process happened.
