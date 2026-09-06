# Program synthesis algorithm

This document is for generating a solution **against an already frozen task and
admitted capsule**. It is not a repository-coding persona and it does not authorize
changes to the task, semantic pack, checker, backend, or host capabilities.

Inputs: frozen task contract, admitted capsule plus identity, selected operation
semantics/tutorial, available tools, total remaining budget, and exact diagnostics
from prior attempts.

## 1. Compress the contract before generating syntax

Extract the smallest internal model that can determine correctness:

```text
input domain and shapes
required output relation
state/effects and prohibited behavior
ordering/provenance invariants
numerical/error policy
performance objective after correctness
capsule operations and restrictions
```

For each task phrase that can change dataflow—“original,” “after,” “exactly once,”
“stable,” “in order,” “at least,” “before commit,” etc.—translate it into an
explicit invariant. If the task is locally ambiguous but a reversible choice does
not change externally visible semantics, choose a sensible default and continue.
Escalate only ambiguity that can change the contract, safety, compatibility, or an
irreversible architecture decision.

## 2. Design the semantic plan outside the surface syntax

Write the algorithm first as transformations and dependencies. Identify:

- what data each decision observes;
- which values must remain distinguishable;
- where aggregation/reduction occurs;
- state transitions or effects, if the pack has them;
- boundaries where ordering, aliasing, concurrency, or numerical association matter;
- the expensive intermediates likely to dominate resource use.

Then map each step to admitted operations. Prefer an existing operation or macro
whose semantics match directly. Do not contort the task to fit the available
surface.

For `intseq`, this often means a sequence pipeline followed by scalar reductions.
Annotate intermediate types before emitting JSON; build the expression inside-out.

## 3. Use representation leverage deliberately

A macro or restricted interface is useful when it removes irrelevant search while
preserving the choices that determine the algorithm. Treat an opaque whole-task
macro as pre-synthesized algorithmic work, not as evidence that the final one-token
call solved the task cheaply.

Prefer familiar composition over gratuitous novelty. Do not request a new primitive
just because its spelling would shorten the candidate. A missing capability claim
should identify the exact required behavior that cannot be constructed from the
admitted semantics under the real constraints.

## 4. Preflight the candidate

Before spending an execution/test attempt, inspect the candidate for the cheap
failure classes:

- every operation is admitted by the capsule;
- arities and intermediate types compose;
- variables are in scope;
- the final type matches the capsule output;
- task-critical ordering/provenance invariants are visible in the dataflow;
- obvious resource-expensive intermediates are understood;
- the candidate is bound to the exact frozen capsule identity.

For `intseq`, emit one `arl-program/0.1` JSON object with exactly
`protocol`, `capsule_sha256`, and `expr`. Obtain the canonical capsule digest from a
real tool or trusted supplied identity; never invent a hash.

## 5. Use tools to answer specific questions

A compiler/checker/test runner is an engineering instrument, not a ritual. Before
each tool call, know what uncertainty it should reduce.

Useful questions include:

```text
Does this candidate parse and typecheck against the exact capsule?
What primitive IR does macro expansion produce?
Which smallest input distinguishes my two algorithm hypotheses?
Is the failure semantic, resource-related, or merely representational?
Does the candidate agree with an independent reference on this boundary family?
Which expression actually dominates work or intermediate magnitude?
```

Run the cheapest discriminating check first. Broad randomized testing is valuable
after the structural hypothesis is plausible; it is a poor substitute for a
one-element counterexample that already identifies the broken ordering rule.

## 6. Diagnose, do not thrash

Use the loop:

```text
observe exact result
  -> localize the failing layer
  -> form competing causes when necessary
  -> choose the smallest discriminating experiment
  -> repair root cause
  -> re-evaluate the affected obligation
```

| Observation | Primary hypothesis | Next move |
|---|---|---|
| schema/version rejection | artifact encoding/format | fix the document, not the task |
| unavailable op / bad arity / type | local representation/dataflow | repair composition or scope |
| capsule hash mismatch | stale/wrong identity | reload and explicitly rebind |
| typechecks but task counterexample fails | algorithm/invariant | trace values and operation order |
| resource rejection | representation/intermediate/policy cost | localize the expensive structure; seek a semantics-preserving allowed alternative |
| unsupported backend/capability | environment boundary | report precise missing capability |
| search budget exhausted | insufficient search evidence | stop honestly; do not infer unexpressibility |

A failed search is not a proof that the language cannot express the task. Bounded
unexpressibility needs a complete finite search or another valid argument.

## 7. Reason about performance only after preserving semantics

When performance matters, estimate the actual cost driver: asymptotic work, number
and size of materialized intermediates, memory traffic/layout, synchronization,
serialization, backend launches, or numerical precision. Optimize the bottleneck
that the target exposes, not the prettiness of the expression.

Remember that mathematically equivalent programs can have different observable
resource behavior under a concrete runtime. In `intseq`, eager evaluation,
intermediate integer bounds, and work accounting make this explicit.

## 8. Output contract

Return the candidate program plus only evidence that actually exists. Distinguish:

- checker/admission results;
- expansion/lowering results;
- execution results;
- task-oracle results;
- performance measurements.

Do not turn one into another. If no acceptable candidate is found, return the most
useful exact diagnostic: failed counterexample, resource/capability boundary, or
budget exhaustion. Preserve uncertainty instead of fabricating execution, tests,
benchmarks, or an unsupported semantic extension.
