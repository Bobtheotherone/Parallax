# Capsule synthesis algorithm

A synthesizer chooses the interface that gives a solver the highest chance of a
strong solution under the real budget. It is not a language-design persona. The
best answer may be `DIRECT`, an existing library/API, a restricted view of a pack,
or a capsule with a small number of compositional macros.

Inputs are the frozen task contract, selected semantic pack, actual host
capabilities, target environment, budget, and any trustworthy model/profile data.
Task semantics, primitive meanings, host permissions, and final acceptance remain
outside the synthesizer's authority.

## 1. Compress the engineering problem

Before inventing syntax, identify the decisions that determine solution quality:

- externally visible behavior, edge cases, errors, effects, numerical policy, and
  compatibility constraints;
- data shape and scale, state/ownership/concurrency boundaries, resource limits,
  and performance bottlenecks when they matter;
- plausible implementation families and the algorithmic choices separating them;
- available libraries, primitives, backends, and tools that already discharge
  difficult obligations;
- likely solver failure modes: irrelevant API surface, missing structure, awkward
  composition, hidden invariants, unfamiliar syntax, or an actually unsupported
  capability.

The capsule should expose the **decision frontier** the solver must reason about
and hide only machinery whose meaning is already fixed and checkable. Do not hide
an unresolved algorithmic choice merely to make the final program shorter.

## 2. Choose whether adaptation is worth buying

Compare four routes in this order: direct/native code, a strong existing API or
DSL, a restricted supported interface, and new compositional macros. Prefer the
simplest route that keeps competitive solutions easy to express.

Adaptation is justified when it removes high-cost irrelevant choices, packages a
reusable invariant, makes an important composition explicit, or turns common
structural mistakes into checker failures. It is weak when it mainly renames
operations, duplicates a familiar library, forces the model to learn gratuitous
syntax, or moves the entire solution into a one-off macro.

A whole-algorithm macro can still be useful, but count its design and validation as
algorithm synthesis. Do not attribute that work to a trivial downstream program.

## 3. Design the smallest sufficient interface

Select a primitive basis that supports the important implementation families, not
just the first solution you imagined. Remove operations only when the restriction
reduces confusion or excludes behavior the task truly does not need.

Add a macro only when all of the following are true:

1. its meaning is a mechanical composition of already admitted semantics;
2. it captures repeated or error-prone structure rather than a new trusted fact;
3. the checker can validate its signature, scope, expansion, and resource bounds;
4. it leaves the solver with meaningful algorithmic decisions; and
5. its construction cost is lower than the search or error cost it is expected to
   remove, under the intended reuse horizon.

Keep names and serialization familiar unless syntax itself is the experiment.
For larger domains, prefer semantic operations over hardware accidents: expose a
row reduction, ownership transfer, transaction, or protocol transition when that
is the real meaning; let a backend own warp layouts, register placement, syscalls,
or transport details unless the task explicitly optimizes them.

## 4. Teach by contrast, not by leaking the answer

Supply only the semantics and examples needed to acquire the interface. Favor
small contrastive examples that distinguish important cases: ordering, aliasing,
empty inputs, numerical boundaries, resource rejection, legal versus illegal
composition, or two well-typed programs with different task behavior.

Examples are diagnostics for model understanding, not substitute semantics. Avoid
examples that encode the full held-out solution when the evaluation claims the
solver must discover that structure.

## 5. Use tools to answer design questions

Tool use should discriminate between competing designs. Useful probes include:

- ask the real checker whether candidate capsules and boundary cases are admitted;
- enumerate signatures/dependencies to find the true minimal sufficient basis;
- run tiny counterexamples that distinguish order, scope, numerical, or resource
  interpretations;
- compare direct and capsule solutions on representative tasks when the adaptation
  cost is uncertain;
- profile or benchmark only when performance is part of the decision, and measure
  the actual bottleneck rather than proxying it with operation count.

Do not run tools merely to complete a ritual. Never report a checker, benchmark,
or execution result that did not occur.

## 6. Diagnose the failure before revising the representation

| Observation | Likely owner | High-information next move |
|---|---|---|
| Many syntax/type failures | interface acquisition or excessive surface | simplify names/examples or restrict irrelevant operations |
| Well-typed but wrong algorithms | solver reasoning | return a discriminating task counterexample; do not change semantics |
| Same structural mistake across solutions | missing reusable abstraction | consider a transparent macro or stronger existing API |
| Competitive algorithm cannot be expressed | representation sufficiency | demonstrate the missing composition before proposing extension |
| Runtime/resource failure | implementation or resource model | profile the real limit; do not infer semantic impossibility |
| Missing primitive/backend | trusted capability boundary | use [EXTENSION](../templates/EXTENSION.md) or choose another supported route |
| Capsule adds cost without reducing failures | adaptation economics | fall back to direct/library mode |

Revise between frozen episodes. A failed search is not proof of unexpressibility.
A new primitive or backend is a separately reviewed system change, never a clever
capsule field.

## Handoff to the programmer

Freeze the admitted capsule before program generation. Provide only the frozen
task, capsule identity, selected operation signatures/semantics, resource-relevant
rules, and the smallest useful examples/counterexamples. State the remaining
algorithmic decisions explicitly so the downstream solver knows what it still owns.

If no executable supported route exists, return a precise `DESIGN_ONLY` result or
extension proposal. Do not impersonate a checker or manufacture host capability.
