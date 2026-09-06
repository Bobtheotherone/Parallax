# Experimental task languages and representation capsules

On this branch, a **capsule is a newly synthesized task-specific programming language
or IR** used as the model's primary implementation surface for a substantial
engineering task.

Unlike `main`, the agent does not first ask whether direct/native code is cheaper.
The experiment intentionally requires language synthesis so its effect can be
measured. The language may lower to native code, existing libraries, APIs, stable
semantic packs, or other trusted implementation machinery.

A generated language is not a new source of task truth or machine authority.

## The abstraction

Let `T` be the frozen task, `K` the available trusted semantics/implementation
surface, `L_T` the novel language synthesized specifically for the task, `p_T` a
program expressed in that language, and `E_T` its checked lowering:

```text
frozen task T
    |
    v
synthesize AI-native language L_T
    |
    v
freeze grammar + typing/state/resource model + lowering
    |
    v
generate task program p_T
    |
   E_T   checked lowering / translation
    v
trusted IR / repository code / library calls
    |
    D    compiler/interpreter/backend/runtime
    v
behavior B
    |
  Phi_T  external task acceptance
    v
accepted?
```

`E_T` has a **representation-preservation** obligation. `Phi_T(B)` is the separate
**task-satisfaction** obligation. A perfectly valid task-language program can still
encode the wrong algorithm.

## Mandatory language properties

The synthesized representation must be language-like enough to be a genuine
experimental treatment. It should define, as appropriate:

- a deterministic grammar or canonical structural encoding;
- an instruction/operator vocabulary adapted to the task;
- value identity and dataflow/control structure;
- types, shapes, dimensions, states, effects, ownership, resources, schedules,
  constraints, or protocol states that matter to the task;
- legal composition rules;
- explicit lowering semantics for every executable construct;
- invalid-state/admission rules;
- concise diagnostics;
- a frozen identity/version for the attempt when artifacts depend on it.

A prose checklist is not a language. A JSON object containing arbitrary host source
is not a language. Renaming every Python/Rust/C++ token is not meaningful adaptation.
A single `solve_everything` macro is not a useful treatment unless the experiment is
explicitly measuring whole-algorithm library synthesis and charges all of that work.

## AI-first, not human-first

Optimize `L_T` for the model that will generate and repair programs in it.
Human source ergonomics are secondary.

Useful design biases include:

- one canonical encoding rather than many stylistic spellings;
- small vocabularies and short stable symbols;
- fixed field/order conventions;
- explicit references instead of name-resolution magic;
- SSA-like immutable values or graph edges when mutation would add ambiguity;
- explicit shape/state/effect/resource annotations near the operation that uses them;
- local scopes and bounded references;
- normalized control/dataflow;
- no optional syntactic sugar unless it measurably helps the model;
- deterministic parsing and lowering;
- diagnostics whose output can be returned to an agent with little interpretation.

Terseness alone is not enough. The language should expose the engineering decisions
that determine correctness or quality while deleting irrelevant general-purpose
language freedom.

## Design from the task's decision surface

Start from the frozen task and actual lowering targets.

1. **Locate hard decisions.** Identify order/provenance, algorithms, data layout,
   ownership, state transitions, concurrency, numerical policy, memory traffic,
   schedules, resources, interfaces, error behavior, or other pressure points.
2. **Choose the machine state model.** Decide what values/nodes/states exist and
   which dependencies must be explicit.
3. **Invent the smallest task-specific instruction basis** that can express strong
   candidate solutions. Operations may be virtual instructions with defined lowering.
4. **Move invariants into structure.** Encode important distinctions in types,
   operands, states, schedules, effects, or legality rules when doing so reduces
   agent ambiguity.
5. **Minimize representational entropy.** Remove aliases, sugar, implicit coercions,
   ambient behavior, and equivalent serializations unless they add measurable value.
6. **Define lowering with the language.** Every executable instruction must map to
   actual supported repository/library/semantic machinery or to an explicit missing
   implementation obligation.
7. **Design diagnostics.** Failures should identify instruction, operand/value,
   expected rule, and owning layer compactly.
8. **Freeze before program generation.** Do not change the language mid-candidate and
   pretend the program used one stable representation.

The language may be deeply task-specific and ephemeral. Generality is not a goal.

## Virtual instructions versus trusted primitives

The experimental branch deliberately encourages novel instruction sets, but there is
an important distinction:

- A **virtual instruction** is generated language content with explicit lowering into
  already implemented behavior. It is safe to invent within the experiment.
- A **trusted primitive/backend capability** is implementation authority. Generated
  text cannot create it merely by naming it.

For example, an agent may invent `m7` as a fused language instruction whose lowering
is a known sequence of repository operations. It may not invent `gpu.flash.magic`
and assume a backend exists. If the best language requires a genuinely new primitive,
record and implement that capability explicitly under [EVOLUTION.md](EVOLUTION.md).

## Lowering is part of the experiment

A task language that cannot be translated faithfully into executable machinery is a
design artifact, not a completed solution route.

Lowering should be:

- explicit enough to inspect;
- deterministic for a frozen language/program where practical;
- type/shape/effect/resource preserving for the modeled properties;
- free of undeclared host capabilities;
- testable by small differential or structural checks;
- capable of reporting unsupported constructs precisely.

For repository coding tasks, lowering may generate or guide ordinary source edits.
The model should still solve in `L_T` first; host code is the compiled artifact.

## Admission obligations

Before trusting a generated task-language program, answer the relevant questions:

- Is the language definition syntactically complete and frozen?
- Does every instruction have defined operands/results and lowering meaning?
- Are references/scopes/value identities valid?
- Do types/shapes/states/effects/resources compose?
- Are required capabilities actually implemented by the lowering target?
- Is lowering bounded and structurally valid?
- Does the lowered artifact preserve modeled invariants?
- Is the program bound to the intended language revision?

Admission establishes only those properties. It does not prove task satisfaction.

## Diagnostics as language design

Prefer errors that are useful to another model invocation:

```text
E21 op=m7 arg=2 got=v14:Vec<F32,128> need=Vec<F32,256>
E34 node=n8 state=OPEN op=commit allowed={PREPARED}
E52 inst=i19 lower=UNSUPPORTED target=cuda-sm90 capability=atomic128
```

The exact encoding is task-specific. The principle is compact locality and low
interpretive ambiguity rather than human-friendly prose.

## Identity and iteration

Freeze a language definition for one attempt. A material grammar/type/instruction/
lowering change creates a new language revision and requires dependent programs to
be regenerated or explicitly migrated.

For measured runs, retain enough identity to distinguish language revisions and to
account for synthesis/lowering cost. A cryptographic hash is useful for content
binding but does not establish correctness.

## `intseq/0.1` compatibility boundary

The existing `arl-capsule/0.1` / `arl-program/0.1` artifacts over `intseq/0.1` remain
unchanged compatibility examples. They demonstrate checked composition and canonical
binding; they do **not** constrain all experimental task languages to that JSON
schema or primitive set.

When working specifically with those artifacts, preserve their established meanings
and hashes. An experimental task language may sit above them and lower into them; it
must not silently reinterpret their versioned semantics.

## Experimental acceptance question

The language is successful only if it helps produce a better accepted engineering
result under the comparison policy. Novelty, ugliness, compactness, grammar validity,
or a short host program are not sufficient by themselves.
