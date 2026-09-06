# Start here

Parallax has two distinct engineering loops:

`build Parallax` and `solve a task through Parallax`.

Do not confuse them. Repository implementation work changes the machinery; a
capsule/program episode uses pinned machinery to solve an external task.

## Sixty-second problem compression

Before choosing a route, answer five questions:

1. **What observable result is requested?** Identify the task/specification and the
   acceptance mechanism that owns correctness.
2. **What must not change?** Capture compatibility, semantics, permissions,
   numerical behavior, side effects, and performance constraints.
3. **What already exists?** Inspect the actual repository, libraries, tools,
   runtimes, examples, and target environment.
4. **Where is the uncertainty?** Separate semantic uncertainty from implementation,
   algorithm, integration, resource, or performance uncertainty.
5. **What experiment would resolve the most important uncertainty?** Prefer a
   compiler, debugger, reference comparison, focused test, profiler, or small
   executable probe over speculative process.

Proceed autonomously on reversible local choices. Stop for clarification only when
the unresolved choice can materially change the contract, safety, compatibility,
irreversible architecture, or requested deliverable.

## Build or change Parallax

Start from the user's request or the named implementation spec, then inspect the
touched code and its dependencies. Use
[docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) when the
change crosses component or trust boundaries and
[docs/development/WORKFLOW.md](docs/development/WORKFLOW.md) for the repository's
development conventions.

The currently prepared implementation slice is
[SPEC-001](docs/specs/001-intseq-reference.md), which packages the embedded
`intseq` reference without changing its semantics. It is relevant only when that
work is actually requested.

Implementation priorities are: understand the contract, choose the right
architecture/algorithm, make the change, then use the most informative available
checks. Tests are evidence, not the product.

## Solve a task

Read [core/CONTRACT.md](core/CONTRACT.md) and
[core/ECONOMICS.md](core/ECONOMICS.md), then choose the cheapest strong route:

- **DIRECT** — ordinary code or an existing library already exposes the right
  abstractions.
- **CAPSULE** — a checked task-specific interface materially compresses the search
  space, exposes useful structure, or prevents realistic classes of mistakes.
- **DESIGN_ONLY** — the required semantics, backend, permission, or acceptance
  mechanism is unavailable.

For capsule work, use [core/CAPSULE.md](core/CAPSULE.md),
[core/PROTOCOL.md](core/PROTOCOL.md), and the selected semantic pack. Freeze the
task and capsule before program generation. The generated artifact does not own
machine capabilities or task acceptance.

## Diagnose or review a result

Start from the exact observation, not a generic checklist. Use the failure layer to
choose context:

- schema/type/operation failures -> capsule/program format and checker;
- wrong accepted output -> task contract, algorithm, and independent oracle;
- resource rejection -> runtime policy and algorithm/resource behavior;
- missing primitive/backend -> supported capabilities and
  [core/EVOLUTION.md](core/EVOLUTION.md);
- performance shortfall -> actual target, profiler/measurement, data movement, and
  algorithm/schedule.

[core/EVIDENCE.md](core/EVIDENCE.md) defines what different checks establish.
A successful execution is not task acceptance.

## Extend, research, benchmark, or maintain docs

Use [ROUTES.md](ROUTES.md) for the smallest authoritative context. New primitives
or backends require explicit semantics, implementation, resource policy, and
versioning; research hypotheses do not grant those capabilities. Benchmarks belong
under the matched-budget methodology in
[docs/benchmarking/PROTOCOL.md](docs/benchmarking/PROTOCOL.md).

For a broad architectural redesign, it is legitimate to read the whole system.
For ordinary work, context should be selected because it changes a decision, not
because a link exists.
