# Architecture: stable semantics, adaptive engineering interfaces

This document defines the target dependency structure and implementation boundaries
for Parallax. It is written for implementers: components should exist because they
own a technical responsibility, not because a workflow diagram needs another box.

**Current state:** only documentation, the embedded `intseq` reference, examples,
and documentation tooling exist. The host and most components below are target
architecture until implemented by explicit specs.

## System shape

```text
Requirement / repository state
          |
          v
+---------------------+
| Task + Problem Model|  invariants, domain, effects, numerics, constraints,
+---------------------+  failure surface, acceptance
          |
          v
+---------------------+       Semantic packs / existing libraries / tools
| Representation Plan |<-----------------------------------------------+
+---------------------+                                                |
   | direct/library/fixed/capsule                                      |
   +--------------------------+                                        |
                              v                                        |
                    +------------------+                               |
                    | Candidate        |  code or data program          |
                    +------------------+                               |
                              |                                        |
                    +------------------+       +--------------------+   |
                    | Check / Lower    |------>| Primitive IR       |---+
                    +------------------+       +--------------------+
                              |                         |
                              | diagnostics             v
                              |                +--------------------+
                              +--------------->| Runtime / Backend  |
                                               +--------------------+
                                                        |
                                                        v
                                               Execution Observation
                                                        |
                            +---------------------------+------------------+
                            |                                              |
                            v                                              v
                    +------------------+                          +----------------+
                    | External Task    |                          | Evidence / Cost|
                    | Acceptance       |                          | + Diagnostics  |
                    +------------------+                          +----------------+
                            |                                              |
                            +-------------------+--------------------------+
                                                v
                                         Host decision loop
                                  repair | replan | accept | stop
```

Generated candidates can influence future decisions through diagnostics. They do
not acquire the authority of the host, semantic pack, backend, or final acceptance
mechanism.

## Core data contracts

The host should pass small explicit artifacts between components. Concrete schemas
can evolve, but the conceptual separation should remain:

```text
TaskContract
  domain, required observations, effects/errors/numerics,
  environment/constraints, acceptance policy, revision identity

ProblemModel
  hard invariants, degrees of freedom, unknowns, failure surface,
  relevant repository/components, candidate implementation families

RepresentationPlan
  route = direct | library | fixed | capsule
  semantic dependencies, exposed decisions, hidden/reused machinery,
  expected leverage, acquisition/validation cost

Candidate
  source/program + representation/capsule binding + dependency identities

Diagnostic
  boundary/component, failure class, observation, implicated invariant,
  next discriminating experiment when known

ExecutionResult
  value/output, errors/effects/resource outcome, runtime/backend identity

AcceptanceResult
  accepted/rejected/unknown under named policy + claim-scoped evidence
```

Avoid turning every artifact into a verbose persistent form. Materialize only what
must cross a component boundary, survive a run, or support reproducibility.

## Components and dependency direction

### 1. Task and problem model

Owns the frozen externally meaningful problem: domain, observations, errors,
effects, numerical/resource constraints, compatibility, acceptance, and high-risk
unknowns. It may summarize repository structure but does not own implementation.

It must not depend on a candidate program. Candidate failures may reveal a contract
ambiguity, but changing an output-affecting contract creates a deliberate new
revision rather than retroactively making the candidate correct.

### 2. Representation planner

Chooses the strongest low-cost interface for this model/task/environment. Its search
space includes direct native code, existing libraries/APIs, fixed typed interfaces,
restricted packs, and capsules. It should prefer reuse over novelty.

The planner reasons about:

- which decisions the model should make versus trusted machinery should discharge;
- which invariants can become structural;
- semantic dependency/context footprint;
- model acquisition cost and familiarity;
- implementation/backend availability;
- expected search reduction and reuse horizon.

It proposes interfaces; it cannot introduce trusted semantics by assertion.

### 3. Capsule admission / representation compiler

For capsule routes, parses supported structured data, verifies operation selection,
signatures/scope/types, checks macros/compositions, enforces bounded expansion, and
lowers to stable pack-level IR. Expansion is rechecked.

The current intseq contract remains the exact `arl-capsule/0.1` /
`arl-program/0.1` format in [packs/intseq/CAPSULE.md](../../packs/intseq/CAPSULE.md).
Future representation features should be versioned when behavior changes.

### 4. Candidate generator

Produces code/programs against the frozen task and chosen interface. It may use
public diagnostics and permitted tools. It does not own the task contract, pack
semantics, capability grants, checker, backend, or final oracle.

For repository coding, the candidate can be an ordinary source diff rather than a
capsule program. Parallax's architectural ideas should improve native coding too.

### 5. Tool broker

The host-facing capability boundary for compilers, interpreters, shell, repository
search, debuggers, profilers, static analyzers, benchmarks, external services, and
other tools. Each tool invocation runs with explicit host-granted authority.

The broker should return structured observations sufficient for diagnosis and cost
accounting, while preserving raw logs only when they are useful for reproducibility
or review. Tool availability must never be inferred from generated prose.

### 6. Runtime/backend

Implements semantic pack operations or executes native candidates in the intended
environment. It owns operational details such as resource checks, numerical
formats, schedules, memory layout, device code, synchronization, and I/O adapters
only to the extent defined by its interface.

Backends may optimize aggressively, but their observations must remain within the
semantic relation specified by the pack/task. Performance claims belong to measured
backend artifacts on the actual target.

### 7. External task acceptance

Evaluates task satisfaction independently from structural program checking. It may
be tests, a compatibility oracle, reference path, formal checker, human review,
target measurement, or a combination.

Final held-out material must remain outside candidate read/write authority when a
held-out claim is made. Development diagnostics can be public; final acceptance
need not be.

### 8. Evidence/cost store

Retains the small set of identities, observations, counterexamples, tool results,
and costs needed to understand the outcome, compare routes, or resume diagnosis.
It is not an append-only bureaucracy for every thought.

### 9. Host decision loop

Owns orchestration: freeze dependencies, route context, grant capabilities, choose
or request a representation, schedule attempts/tools, enforce budgets/cancellation,
protect final acceptance, and decide whether to repair, replan, accept, or stop.

The host should implement the diagnostic loop in [PROTOCOL](../../core/PROTOCOL.md),
not merely enumerate states.

## State ownership and mutation

Keep authoritative mutation local:

- task owner/contract revision owns task semantics;
- pack version owns primitive meanings;
- capsule identity owns one admitted representation;
- candidate revision owns source/program bytes;
- runtime/backend version owns implementation behavior;
- acceptance policy/oracle identity owns the decision procedure;
- host run state owns budget, granted capabilities, diagnostics, and attempt history.

A component may reference another component's identity but should not silently
rewrite its state. This makes failures localizable and parallel attempts safe.

## Concurrency and parallel attempts

Independent candidate/tool attempts may run concurrently when they share immutable
contract/semantic snapshots. Sum their compute/inference cost even when wall time
overlaps. Keep per-attempt artifacts and cancellation scopes distinct.

Do not let one attempt mutate the capsule, oracle, or semantic pack underneath
another. Shared caches must be keyed by the dependencies that affect behavior.
For stateful external systems, the task contract must define isolation or permitted
interference; concurrency is not automatically safe because candidate files differ.

## Diagnostics and error model

Return errors at the boundary that can act on them. A useful taxonomy includes:

```text
CONTRACT_AMBIGUITY
SCHEMA / TYPE / OP_NOT_ALLOWED / HASH_MISMATCH
EXPANSION_OR_LOWERING_ERROR
UNSUPPORTED_CAPABILITY
EXECUTION_ERROR
RESOURCE_LIMIT
TASK_REJECTION
NUMERICAL_MISMATCH
COMPATIBILITY_MISMATCH
PERFORMANCE_MISS
INFRASTRUCTURE_ERROR
BUDGET_EXHAUSTED
```

Concrete implementations need not use these exact strings except where an existing
protocol already defines them. The important property is that a program bug,
resource limit, missing backend, and task rejection do not collapse into one
"failed" signal.

Diagnostics should include the smallest actionable observation: component/boundary,
violated invariant or expected relation when known, and a counterexample or tool
reference. The next step should target the root cause, not add undirected logging.

## Trust boundary and resource policy

Generated capsules, programs, code suggestions, retrieved examples, and tutorials
are **data** until a trusted component deliberately interprets or executes them.
They cannot grant filesystem/network/process/model/oracle/native-code privileges.

Trusted implementation includes the parser/checker/expander, runtime/backend,
tool broker, host, language/runtime environment, and operating-system isolation on
which the deployment relies. A data-only AST narrows the generated attack surface;
it does not make the interpreter, Python, compiler, or OS formally safe.

The host must control:

- process lifetime/cancellation and resource ceilings;
- filesystem, network, secret, and external-service access;
- native/backend adapters and device access;
- tool/model credentials and rate/budget limits;
- final-oracle custody;
- which generated artifacts are ever executed as native code.

Pack/runtime resource limits such as intseq depth/work/integer bounds are prototype
execution policies, not an OS sandbox. A resource rejection remains distinct from
task correctness unless the task contract itself makes the limit part of success.

## Performance architecture

Do not add an optimization subsystem before measurements demand it. When performance
is part of a task, preserve the boundary:

```text
semantic algorithm / required observation
        -> legal implementation family
        -> schedule/layout/backend parameters
        -> measured target artifact
```

Profilers and benchmarks should identify the real bottleneck before the planner
changes algorithm, memory layout, batching, vectorization, concurrency, or backend.
Expose schedule choices in a representation only when doing so gives the model
useful control without weakening semantic scope.

## Extension strategy

Add domains as packs plus one or more backends, not by growing a universal core
operation set. A new pack must define its observation model and relevant data,
effects, errors, ownership/concurrency, numerics, and resource semantics.

Add representation features orthogonally where possible: a new tutorial or
serialization should not require a semantic change; a new macro system should not
implicitly grant host effects; a new backend should implement a versioned semantic
contract. See [EVOLUTION](../../core/EVOLUTION.md).

## Current implementation map

| Repository artifact | Current role |
|---|---|
| [runtime/REFERENCE.md](../../runtime/REFERENCE.md) | Embedded Python implementation of intseq checking/expansion/evaluation and public self-tests |
| [packs/intseq/PACK.md](../../packs/intseq/PACK.md) | Stable seven-operation intseq semantics and resource policy |
| [packs/intseq/CAPSULE.md](../../packs/intseq/CAPSULE.md) | Exact v0.1 capsule/program format |
| [examples/intseq/](../../examples/intseq/TASK.md) | Frozen worked contract/capsule/program, failure case, packet, imported evidence |
| [SPEC-001](../specs/001-intseq-reference.md) | First implementation contract: extract/package the reference without semantic redesign |
| [tools/check_docs.py](../../tools/check_docs.py) | Documentation/provenance integrity checker only; not semantic runtime validation |
| Host/planner/tool broker/evidence store | Target architecture; not implemented yet |

## Source-of-truth map

| Question | Authoritative home |
|---|---|
| Project mission and maturity baseline | [PROJECT](../PROJECT.md) |
| Universal repository agent constraints | [AGENTS](../../AGENTS.md) |
| Entry/routing guidance | [START](../../START.md), [ROUTES](../../ROUTES.md) |
| Architecture/component ownership | This document; [ADRs](decisions/README.md) retain historical rationale |
| Task semantics, problem compression, ambiguity | [CONTRACT](../../core/CONTRACT.md) |
| Semantic relations and representation preservation | [SEMANTICS](../../core/SEMANTICS.md) |
| General capsule concept and identity | [CAPSULE](../../core/CAPSULE.md) |
| intseq semantics and artifact syntax | [PACK](../../packs/intseq/PACK.md), [formats](../../packs/intseq/CAPSULE.md) |
| Synthesis/diagnostic loop and terminal outcomes | [PROTOCOL](../../core/PROTOCOL.md) |
| Extension/versioning/retirement | [EVOLUTION](../../core/EVOLUTION.md) |
| Evidence claim language | [EVIDENCE](../../core/EVIDENCE.md) |
| Representation cost and route selection | [ECONOMICS](../../core/ECONOMICS.md) |
| Host/tool/capability boundary | [HOST](../../runtime/HOST.md) |
| Implementation scope/acceptance | Selected file in `docs/specs/` |
| Experimental comparison methodology | [benchmark protocol](../benchmarking/PROTOCOL.md) |
| Migration/history/input provenance | [SOURCE-MAP](../provenance/SOURCE-MAP.md) and preserved archive |

README is a summary. Tutorials, examples, packets, templates, research notes, and
historical evidence do not override the owning contracts above. A contradiction is
a defect to resolve at the owning boundary, not a "last document wins" rule.

## Compatibility decisions retained

The architecture preserves the three adopted decisions: stable semantics under an
adaptive surface, generated artifacts without self-authorizing execution authority,
and independent task acceptance. Existing `intseq/0.1`, `arl-capsule/0.1`, and
`arl-program/0.1` meanings and canonical example identities remain compatible.

Future versions may be more expressive, but they must not silently reinterpret
old artifacts.
