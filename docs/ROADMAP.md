# Roadmap: build capability in vertical slices

This roadmap sequences **engineering unlocks**, not paperwork states or delivery
dates. A stage is complete only when the capability exists and its decisive checks
have actually run. [PROJECT](PROJECT.md) describes the current baseline; individual
implementation specs define bounded changes.

## Priority order

| Milestone | Engineering unlock | Exit evidence that matters |
|---|---|---|
| 0 — Executable semantic foundation | Extract the frozen intseq reference into ordinary importable/testable code ([SPEC-001](specs/001-intseq-reference.md)) | Fresh contract/reference parity, boundary tests, CLI behavior, and documented runtime identity; no semantic redesign |
| 1 — Minimal host vertical slice | Run one task through contract → representation choice → generation → checker/runtime → external acceptance → diagnostic repair | Reproducible real runs with pinned dependencies, capability control, bounded tool/model use, retained failures, and task acceptance kept outside candidate authority |
| 2 — Representation portfolio | Support direct code, existing-library/fixed-interface, and capsule routes under one host; add a small cache of reusable admitted abstractions | The host can choose among routes for concrete technical reasons and report cost/failure class without forcing every task through a capsule |
| 3 — Engineering task suite | Exercise multi-module repository changes, API compatibility, stateful/concurrent logic, numerical work, and performance-sensitive cases | Task-specific acceptance plus diagnostics show the system can localize realistic failures; strong native/library baselines exist |
| 4 — Adaptive selection and reuse | Learn/select representation components from prior tasks/models/environments without mutating semantics | Cold/warm accounting, dependency-aware cache validity, and held-out task-family evidence under the [benchmark protocol](benchmarking/PROTOCOL.md) |
| 5 — Rich backend domain | Add one genuinely harder domain/backend (for example a tensor/GPU slice) with semantic/schedule separation | Versioned pack semantics, real lowering, adversarial correctness/numerical checks, target profiling/benchmarks, and preserved old meanings |
| 6 — Research-scale evaluation | Test whether adaptation itself provides leverage beyond contracts, tools, libraries, and extra inference | Matched-budget ablations and reproducible results, including negative/inconclusive outcomes and false-acceptance analysis |

Milestones 1–3 are intentionally vertical: a small end-to-end system that can solve,
observe, diagnose, and recover is more valuable than many disconnected schemas or
mock components.

## Near-term implementation priorities

After SPEC-001, the highest-value work is the smallest host that exercises the
architecture rather than another documentation layer. It should provide:

- a compact `TaskContract`/problem model and pinned semantic environment;
- representation selection among direct/fixed/capsule routes;
- a tool broker with explicit granted capabilities;
- checker/runtime adapters that return structured diagnostics;
- an external task evaluator not derived from candidate code;
- a run state that records decisive artifacts, costs, failures, and evidence;
- a diagnostic loop that can choose the next experiment rather than blindly retry.

Prefer local standard interfaces and existing libraries until a real task proves a
new abstraction is needed. Do not build a generic plugin marketplace, distributed
scheduler, vector database, or model-training pipeline before the vertical slice
requires it.

## Harder engineering should drive the next abstractions

The task suite should progressively force useful machinery:

- **multi-module/legacy changes:** ownership, dependency direction, compatibility;
- **stateful protocols/services:** explicit state transitions, errors, retries,
  idempotency, observability;
- **concurrent systems:** ownership, synchronization, ordering, cancellation;
- **numerical code:** formats, reduction order, error relation, adversarial inputs;
- **performance work:** profiling, memory/layout, allocation, batching, I/O,
  synchronization, target-specific measurement;
- **backend work:** semantic scope separated from schedule/lowering choices.

Add a representation feature only when these tasks show that it compresses
repeated reasoning, rules out realistic failures, or unlocks real backend leverage.

## Research gates

Before claiming that adaptive representations improve engineering outcomes:

1. compare against competitive direct and library/fixed-interface routes;
2. separate gains from extra context, extra inference, better contracts, or extra
   tool use;
3. count cold construction and all failed candidates;
4. preserve held-out final acceptance when claiming generalization;
5. measure solution quality/performance on the real target after functional
   acceptance;
6. report task/model/backend heterogeneity rather than one pooled win rate.

Do not promote adaptation merely because syntax/type errors fall or generated
programs become shorter.

## Open technical decisions

Resolve these only when their milestone depends on them:

| Decision | Needed for |
|---|---|
| Model/provider adapter and token/cost accounting | Milestone 1 host implementation |
| Durable artifact/run storage | Reproducible multi-run host and later experiments |
| Process/filesystem/network isolation model | Hostile inputs, external tools, native backends |
| Final-oracle custody mechanism | Held-out experiments |
| Representation cache key/dependency graph | Milestone 4 reuse |
| Task-family suite and statistical design | Milestones 3/6 comparisons |
| Rich domain semantics and backend target | Milestone 5 |
| Project license | Distribution decision |

The GPU RMSNorm note remains [design-only](../packs/gpu/RMSNORM.md) until a versioned
pack and real backend exist. It is a useful semantic/schedule design case, not a
reason to skip the executable host foundation.
