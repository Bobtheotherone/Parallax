# Task-language program synthesis algorithm

This document governs the programmer stage on `experimental`. The programmer
receives a frozen task and a newly synthesized AI-native task language `L_T`, then
must produce the serious candidate **in that language before host-language code is
generated**.

Inputs: frozen task, frozen `L_T` definition/identity, instruction semantics and
lowering rules, available tools, remaining budget, and exact permitted diagnostics.

The programmer does not change the task, language semantics, host permissions, or
final oracle during one frozen attempt.

## 1. Compress the contract into language-level invariants

Extract the facts that determine correctness:

```text
input domain / shapes / initial states
required output relation
ordering and provenance
state/effects/ownership
numerical/error policy
resource/performance objective
language instruction/state model
```

Map task-critical phrases such as “original,” “before,” “stable,” “exactly once,”
“same buffer,” “after commit,” or “within tolerance” to explicit value/state/dataflow
relationships in `L_T`.

Do not begin by writing host code.

## 2. Design the algorithm in the generated language

Construct the solution using `L_T` values, instructions, nodes, states, constraints,
or schedules.

Reason explicitly about:

- which value/state each operation observes;
- dependency and control order;
- where information is transformed or discarded;
- ownership/effect boundaries;
- aggregation/reduction scope;
- expensive intermediates and resource pressure;
- target-specific schedule/layout choices exposed by the language.

The task-language program should be the actual algorithmic artifact from which the
host implementation follows.

## 3. Exploit the language's AI-native structure

Use the representation the synthesizer created instead of mentally translating back
to a familiar language.

If `L_T` uses canonical value IDs, graph edges, typed instruction tuples, explicit
states, or schedule objects, reason directly in those terms. Prefer the canonical
encoding and do not invent aliases/sugar locally.

The point of the experiment is to see whether the generated representation changes
the model's search/reasoning behavior. A host-language solution written first and
then transliterated into `L_T` invalidates that mechanism.

## 4. Preflight before lowering

Check cheap structural obligations first:

- every opcode exists in frozen `L_T`;
- operand/result references are valid and in scope;
- types/shapes/states/effects/resources compose;
- task-critical dependencies are represented explicitly;
- the final language-level output matches the required interface;
- every used instruction has an implemented lowering path;
- the program is bound to the intended language revision.

Use a real parser/checker if available. Do not claim a check that did not run.

## 5. Lower only after the language program is coherent

Translate the frozen task-language program through its declared lowering contract.
The lowered artifact may be:

- ordinary repository source code;
- an AST or compiler IR;
- calls to an existing library/API;
- a stable Parallax semantic artifact such as `arl-program/0.1`;
- a backend configuration/schedule;
- an explicit repository transformation plan that deterministically produces source
  edits.

Inspect high-risk lowering points such as evaluation order, state transitions,
resource lifetime, numerical association, shape/layout mapping, concurrency,
exceptions/errors, and API semantics.

A correct `L_T` program with incorrect host code is a lowering/implementation defect.
Do not redesign the task to make it pass.

## 6. Use tools by layer

Useful questions include:

```text
Does the task-language artifact parse canonically?
Which instruction violates a type/shape/state rule?
What host construct does this instruction lower to?
Does a tiny differential case show lowering equivalence?
Does the generated host source compile and integrate?
Which runtime state transition actually fails?
Which representation/schedule choice dominates time or memory?
Does the external task oracle accept the resulting behavior?
```

Run the cheapest discriminating check first.

## 7. Diagnose without thrashing

```text
observe
 -> language parse/check?
 -> algorithm in L_T?
 -> lowering?
 -> host implementation/backend?
 -> resource/performance?
 -> external task acceptance?
 -> repair earliest failing layer
```

| Observation | Primary hypothesis | Next move |
|---|---|---|
| parse/canonicalization failure | malformed `L_T` program | repair language encoding |
| type/shape/state rejection | invalid instruction composition | repair operands/dataflow |
| structurally valid but task counterexample fails | algorithm/invariant | trace `L_T` values/states |
| language semantics and lowered source disagree | lowerer | isolate instruction translation |
| host build/integration failure | lowering target/implementation | fix generated host artifact |
| unsupported lowered capability | environment/backend | report precise capability gap |
| runtime resource failure | algorithm/schedule/intermediate | profile and revise within `L_T` or next language revision |
| repeated mistake caused by awkward language | representation | return evidence to synthesizer for next frozen `L_T` revision |

A failed program search is not proof that no suitable task language can express the
solution.

## 8. Performance reasoning

When performance matters, reason in the low-level dimensions `L_T` exposes: work,
materialized values, layouts, memory traffic, allocation, vectorization, batching,
synchronization, launches, I/O, precision, and schedule choices.

Lowering must preserve the intended optimization. Benchmark the actual target only
after correctness gates; language syntax alone cannot establish performance.

## 9. Existing `intseq` artifacts

When the generated task language lowers into the repository's existing intseq
artifacts, preserve their compatibility rules. `arl-program/0.1` still contains
exactly its defined fields and binds the canonical capsule identity.

The experimental language may sit above that format; it may not silently mutate the
meaning of `intseq/0.1`.

## 10. Output

For a measured experimental run, retain at least:

- frozen task-language identity/definition;
- program expressed in `L_T`;
- lowering target and resulting host artifact;
- actual parser/checker/lowering/build/execution/task evidence that exists;
- important failure diagnostic if not accepted.

Keep the record compact. The language program and resulting implementation are the
substantive deliverables; process narration is not.
