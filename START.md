# Start here — experimental branch

This branch tests one methodology:

**substantial engineering work must be solved through a newly synthesized AI-native
task language/IR before host-language implementation is produced.**

Read [AGENTS.md](AGENTS.md) first. `main` uses adaptive representation choice;
`experimental` deliberately forces language synthesis so the two methods can be
compared.

## Sixty-second problem compression

Before designing the language, answer:

1. **What observable result is requested?** Identify the task/specification and
   external acceptance mechanism.
2. **What must not change?** Capture compatibility, semantics, permissions,
   numerical/effect behavior, and hard performance constraints.
3. **What structure dominates the task?** Identify data/state shapes, dependencies,
   ownership, concurrency, resources, schedules, protocol states, or algorithmic
   choices that determine success.
4. **What exists as a lowering target?** Inspect repository code, libraries, APIs,
   semantic packs, compilers, tools, and target environment.
5. **What should the generated language make explicit?** Identify the decisions that
   are error-prone or expensive for a model when expressed in the host language.

Proceed autonomously on reversible local choices. Escalate only uncertainty that
materially changes the contract, safety, compatibility, irreversible architecture,
or requested deliverable.

## Mandatory experimental pipeline

For every nontrivial engineering task:

```text
freeze task
  -> compress problem
  -> synthesize novel AI-native task language / IR
  -> freeze language semantics + lowering
  -> generate solution program in that language
  -> lower/translate to actual repository code
  -> build/run/use targeted tools
  -> external task acceptance
  -> diagnose language vs algorithm vs lowering vs implementation failures
```

The task language must be a real structured language as defined by
[AGENTS.md](AGENTS.md) and [core/CAPSULE.md](core/CAPSULE.md). Do not design the full
solution in Python/Rust/C++ first and translate it afterward merely to satisfy the
experiment.

A tiny mechanical edit with no meaningful algorithmic/design content may be marked
`TRIVIAL_DIRECT`. Substantial implementation, debugging, refactoring, architecture,
performance, integration, or multi-file work is not trivial.

## Build or change this repository

The experimental rule applies to repository coding too. Start from the request or
named spec, inspect touched implementation/dependencies, then synthesize a compact
task language that captures the change before editing host code.

For example, a repository refactor language might explicitly encode modules,
interfaces, invariants, state ownership, allowed dependency edges, transformations,
and acceptance obligations. A performance task language might expose memory regions,
loops/dataflow, vectorization/schedule choices, synchronization, and resource bounds.

Use [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) when the
change crosses component/trust boundaries and
[docs/development/WORKFLOW.md](docs/development/WORKFLOW.md) for ordinary repository
mechanics. Those documents do not waive the experimental language requirement.

The prepared [SPEC-001](docs/specs/001-intseq-reference.md) remains relevant only
when that implementation work is actually requested.

## Solve an external task

Read [core/CONTRACT.md](core/CONTRACT.md), [core/CAPSULE.md](core/CAPSULE.md), and
[core/PROTOCOL.md](core/PROTOCOL.md).

On this branch the route is:

- **LANGUAGE** — mandatory for substantial executable work: synthesize the task
  language, freeze it, generate the program, and lower it.
- **TRIVIAL_DIRECT** — only for genuinely mechanical edits where a language would
  encode no meaningful decision.
- **DESIGN_ONLY** — required semantics, backend, permission, or acceptance mechanism
  does not exist and cannot honestly be implemented in scope.

Existing libraries and native languages remain valuable **lowering targets**. They
are not substitutes for the generated model-facing task language in the treatment
arm.

## Design the task language

Use [roles/SYNTHESIZER.md](roles/SYNTHESIZER.md) as the language-design algorithm.
The result should normally specify:

- canonical syntax/serialization;
- instruction/operator vocabulary;
- type/shape/state/effect/resource model as relevant;
- legal composition/control/dataflow rules;
- task-specific invariants made structural where useful;
- lowering mapping to real supported machinery;
- diagnostics;
- identity/version for the frozen attempt.

Then use [roles/PROGRAMMER.md](roles/PROGRAMMER.md) to generate the candidate in the
frozen language.

## Diagnose or review a result

Start from the exact observation and classify it:

- language parse/type/shape/state failure -> task-language design or program;
- language program valid but lowering differs -> lowerer/translation defect;
- lowered implementation fails build/runtime -> repository/backend defect;
- implementation executes but task case fails -> algorithm/task-satisfaction defect;
- resource/performance failure -> algorithm, language-exposed schedule/resource
  choice, lowering, or backend after measurement;
- unsupported primitive/backend/capability -> explicit implementation boundary;
- final evaluator failure -> task correctness, not language validity.

Use the smallest discriminating experiment. Do not redesign the language merely to
hide an algorithm bug.

## Benchmark the hypothesis

Use [docs/benchmarking/PROTOCOL.md](docs/benchmarking/PROTOCOL.md) to compare this
branch with `main` under the same model/task/tools/acceptance and matched total
budget. Count language synthesis and lowering cost. The purpose is empirical: the
forced-language method may win, lose, or be conditional.
