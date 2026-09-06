# Task contracts: compress the engineering problem

A task contract fixes **what counts as success** before choosing code, tools, or a
representation. It is the boundary that prevents an implementation from becoming
"correct" by quietly changing the problem.

The contract should be as small as possible while preserving every fact that can
change an externally meaningful result, safety property, compatibility decision,
or optimization target. It is not a project diary and it is not a language spec.

## Minimum sufficient contract

For task `T`, capture the following when they matter:

| Dimension | Question the implementation must be able to answer |
|---|---|
| Inputs | What values/states are valid? What size, shape, ordering, aliasing, encoding, or lifetime constraints exist? |
| Required behavior | What relation must hold between inputs, prior state, outputs, and externally visible effects? |
| Errors | Which failures are required, permitted, retriable, or forbidden? |
| Numerical behavior | Exact, modular, saturating, floating-point, stochastic, tolerant, deterministic? What error relation is accepted? |
| State and effects | What may be read, written, emitted, persisted, or communicated, and in what order? |
| Environment | Which platform, language/runtime, libraries, hardware, protocols, and compatibility versions constrain the result? |
| Resources | Which latency, throughput, memory, allocation, I/O, work, energy, or cost limits are part of acceptance rather than merely preferences? |
| Prohibited behavior | What must never happen even if the main output looks correct? |
| Acceptance | What external observation decides success, and what evidence is required to trust that observation? |
| Change authority | Who may deliberately revise an output-changing part of the contract? |

Use [the task template](../templates/TASK.md) when a materialized record is useful.
Do not add fields merely to prove that a workflow happened.

A useful mental model is:

```text
T = (domain, observation_relation, errors, effects, numerics,
     environment, constraints, acceptance_policy)
```

The candidate is acceptable only if the external acceptance mechanism establishes
the required observations under that frozen `T`.

## Compress before coding

Before the first serious implementation attempt, reduce the task to four things:

1. **Hard invariants** — facts that a correct design cannot violate.
2. **Degrees of freedom** — choices the implementation may legitimately optimize.
3. **Unknowns** — facts not yet established that could alter the design.
4. **Failure surface** — the realistic ways the solution can be wrong: semantic,
   integration, concurrency, numerical, resource, compatibility, or operational.

This is problem compression, not paperwork. The result should make architecture
and algorithm choices easier. For a large codebase, include the existing ownership
and compatibility boundaries that constrain the change; for a small pure function,
a relation and a few edge conditions may be enough.

Do not infer the contract from the implementation that happens to compile. Existing
code and tests are evidence about intent and compatibility, not permission to erase
a contradictory requirement. When sources disagree, identify the smallest
observable disagreement and resolve or version that disagreement explicitly.

## Reversible autonomy

Not every ambiguity deserves a stop.

Proceed with a sensible default when the choice is local, reversible, inexpensive
to change, and does not alter externally visible semantics, security, compatibility,
or an irreversible architecture. Record the assumption only if a later engineer
would need it to understand the artifact.

Clarify or return `DESIGN_ONLY` when an unresolved choice can materially change:

- correct outputs or required error behavior;
- externally visible state/effects or security boundaries;
- compatibility with a published interface or stored artifact;
- a major resource/architecture commitment that is expensive to reverse;
- access to capabilities, secrets, destructive actions, or final acceptance data.

The goal is high-agency progress without silently inventing requirements.

## Program validity is not task validity

Keep these predicates separate:

```text
CheckProgram(program, capsule, pack) -> well_formed | rejected
CheckTask(observation, contract)     -> accepted | rejected | unknown
```

`CheckProgram` may establish schema, scope, types, allowed operations, identity
binding, expansion validity, and execution preconditions. `CheckTask` decides
whether the resulting behavior satisfies the user's task. A well-typed program
can be algorithmically wrong; a successfully executed candidate can still violate
an error, effect, performance, or compatibility requirement.

The intseq counterexample in [FAILURE.md](../examples/intseq/FAILURE.md) is the
canonical small example: filtering after the affine transformation is well-typed
but changes which original elements contribute.

## Acceptance mechanisms

Choose acceptance that discriminates plausible failures. Depending on the task it
may combine a mathematical specification, compatibility oracle, reference
implementation, property checks, differential comparison, target measurement,
review, or formal proof. More checks are not automatically stronger; evidence is
useful when it can separate competing implementations or hypotheses.

Keep the final acceptance mechanism conceptually outside generated representation
and program authority. Candidate-generated tests can be excellent development
tools, but they do not become independent ground truth merely because they pass.
A reference implementation can also be wrong; identify its origin and the property
for which it is being trusted.

When a contract changes in a way that can alter acceptance, it is a new contract
version for comparative purposes. Do not hide relaxed tolerances, narrowed domains,
new exclusions, or changed resource limits inside a representation revision.
