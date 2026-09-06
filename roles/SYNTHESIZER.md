# AI-native task-language synthesis algorithm

The synthesizer's job on `experimental` is to create a **new programming language or
IR for the current substantial engineering task**. It does not decide whether a new
language is worthwhile; that question is intentionally fixed by the experiment.

Inputs: frozen task, repository/target architecture, available trusted semantics and
libraries, host capabilities, budget, and any reliable model/tool observations.
Outputs: a frozen task-language definition `L_T`, its lowering contract, compact
acquisition examples if needed, and an identity/revision for program generation.

Task semantics, host permissions, and final acceptance remain outside the generated
language's authority.

## 1. Extract the decision surface

Do not begin with syntax. Build a compact model of the decisions that determine
correctness or engineering quality:

- externally observable behavior and edge cases;
- important data shapes, values, provenance, ordering, and invariants;
- state transitions, ownership, effects, concurrency, and lifetime constraints;
- algorithm families and complexity boundaries;
- numerical rules and reduction/association behavior;
- memory/layout/I/O/serialization/schedule decisions when relevant;
- available host libraries/APIs/backends and their actual constraints;
- likely model failure modes in the ordinary host-language representation.

The task language should make this decision surface explicit while removing
irrelevant general-purpose language choices.

## 2. Choose a machine state model

Define what the model manipulates. Examples:

- immutable typed values with SSA identifiers;
- graph nodes and typed edges;
- stack/register slots;
- shape-annotated tensors/buffers;
- protocol states and transitions;
- constraints and finite holes;
- transformations over repository modules/interfaces;
- schedule/resource objects separated from semantic operations.

Choose the state model that makes dependencies and illegal combinations easiest for
the LLM to represent consistently. Human familiarity is not a criterion.

## 3. Synthesize the instruction basis

Invent a compact operator set adapted to the task.

Each instruction should have:

```text
opcode
operands / references
result(s)
type/shape/state/effect/resource contract
preconditions
semantic intent
lowering rule
failure/diagnostic class
```

Prefer orthogonal operators and canonical operand order. Combine operations when a
fused instruction captures a meaningful recurring decision or removes a common model
failure. Split operations when fusion hides a decision the task actually requires.

Virtual instructions may be novel and task-specific. Their executable authority
comes from lowering into supported code/semantics, not from their name.

Do not simply rename the host language. At least one meaningful dimension—operator
basis, state/value model, type/shape/effect system, dataflow/control representation,
constraint model, or schedule/resource model—should be genuinely adapted to the
task.

## 4. Minimize representational entropy

Design for model generation rather than human style diversity.

Prefer:

- exactly one canonical serialization;
- short stable opcodes/tags;
- fixed field order;
- explicit references instead of implicit name resolution;
- no aliases for the same operation;
- no optional punctuation/sugar unless empirically useful;
- explicit types/shapes/states where inference would create ambiguity;
- bounded local scopes;
- normalized branching/loop/dataflow forms;
- deterministic numeric/string literal rules;
- minimal nesting depth compatible with the task.

A language can be ugly to a human and excellent for an agent.

## 5. Encode invariants structurally

Move important task facts into the language when this can reject or distinguish
wrong constructions **without embedding the final task oracle**.

Examples:

- distinguish original-data references from transformed-data references;
- separate semantic reduction scope from backend schedule;
- represent ownership transfer as state transitions;
- make buffer shape/layout operands explicit;
- encode protocol transitions with legal predecessor states;
- separate pure values from effectful operations;
- make resource/synchronization dependencies explicit.

Do not turn arbitrary task correctness into the type system. A well-typed wrong
algorithm must remain possible when the task distinction is genuinely semantic.

## 6. Define deterministic lowering

For every executable construct, specify its translation into real supported
machinery:

```text
L_T instruction
   -> stable semantic operation(s)
   -> library/API call(s)
   -> host AST/source transformation
   -> backend schedule/configuration
```

Lowering must state any ordering, evaluation, numerical, state/effect, resource, or
error behavior that affects observable results.

If a desired instruction cannot be implemented with available meaning/capability,
mark it unsupported or create a separate explicit implementation requirement. Do not
pretend syntax created the backend.

## 7. Build language diagnostics

Diagnostics should be cheap for another model to consume. Prefer compact structured
errors that identify:

- language revision;
- offending instruction/node;
- operand/reference;
- expected versus observed type/shape/state/effect/resource rule;
- failure layer (`PARSE`, `TYPE`, `STATE`, `RESOURCE`, `LOWER`, `CAPABILITY`).

Avoid long explanatory prose in machine feedback unless it adds information.

## 8. Teach by contrast

If the language is non-obvious, provide a very small number of high-information
examples/counterexamples. Use them to teach:

- legal syntax/composition;
- subtle dependency/order distinctions;
- state/type/resource failures;
- one case where two structurally legal programs have different task behavior.

Do not provide a complete held-out solution as the tutorial.

## 9. Freeze the language

Before program generation, freeze:

- grammar/canonical encoding;
- operator set and signatures;
- type/shape/state/effect/resource rules;
- lowering mapping;
- diagnostics contract;
- language identity/revision.

A material change creates `L_T+1` and a new program-generation episode.

## 10. Diagnose treatment failures

| Observation | Likely cause | Next experiment |
|---|---|---|
| Many parse failures | encoding too ambiguous/complex | canonicalize/reduce syntax |
| Many type/state failures | acquisition problem or overconstraint | inspect smallest failing program; simplify rule or example |
| Valid programs repeatedly encode same wrong dependency | state/value model hides important distinction | expose that dependency structurally |
| Strong algorithm cannot be expressed | instruction basis insufficient | demonstrate missing composition and add a lowerable virtual instruction |
| Lowering repeatedly miscompiles valid programs | lowering contract too complex/ambiguous | simplify IR or make semantics more local |
| Host backend rejects instruction | real capability gap | implement/version capability or redesign instruction lowering |
| Language works but costs too much | treatment economics | record the loss; do not silently switch to direct mode |

## Handoff to the programmer

Provide the frozen task, frozen `L_T`, language identity, instruction signatures,
lowering-relevant semantics, resource rules, and the smallest useful contrastive
examples. Do not hand over a completed host-language solution.

The programmer must discover and express the algorithm in the generated language.
