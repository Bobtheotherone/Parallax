# Experimental task-language / capsule template

Use this template to design the **new AI-native programming language or IR** required
for a substantial task on the `experimental` branch. The output may be ephemeral or
persisted with a measured run, but the design should be concrete enough that a model
can generate a program in it and that the program can be lowered into real code or
trusted semantics.

For the legacy `intseq/0.1` machine artifact itself, the exact JSON schema in
[packs/intseq/CAPSULE.md](../packs/intseq/CAPSULE.md) still applies. The experimental
language may sit above it and lower into it.

## 1. Language identity

```text
name/version:
task or task-family identity:
frozen task revision:
primary lowering target:
language identity/hash if used:
```

The language should be newly adapted to this task. State briefly what makes its
machine model materially different from simply writing the host language directly.

## 2. Machine state model

Define the objects programs manipulate.

```text
value/reference form:
mutation model: immutable SSA | explicit state transition | stack/register | other
scope/reference rules:
control/dataflow representation:
state/effect/ownership model:
shape/layout/resource/schedule model:
```

Include only dimensions that affect the task.

## 3. Canonical encoding

Specify one deterministic program representation.

```text
top-level form:
instruction form:
literal/reference form:
ordering rules:
allowed identifiers/opcodes:
forbidden aliases/sugar/implicit coercions:
```

Optimize for low ambiguity and easy machine generation, not human aesthetics.

## 4. Instruction set

For each opcode define:

| Op | Inputs | Outputs | Preconditions / state | Meaning | Lowering |
|---|---|---|---|---|---|
| `<op>` | `<refs/types>` | `<refs/types>` | `<rule>` | `<task-level meaning>` | `<real implementation target>` |

Prefer a small orthogonal basis. Add fused/virtual instructions when they make a
meaningful task pattern easier for the model and have explicit lowering.

## 5. Types / shapes / states / effects

Define the mechanically relevant legality rules.

```text
primitive/task-specific types:
shape/dimension rules:
state transitions:
ownership/alias rules:
effects/capabilities represented:
resource limits or symbolic resource fields:
schedule/layout constraints:
```

Do not pretend these rules enforce arbitrary task correctness. They should encode
representation invariants, not secretly contain the final oracle.

## 6. Lowering contract

For every executable construct, specify how it becomes real machinery.

```text
language op -> host AST/source/API/semantic primitive/backend action
```

Record behavior that can change observables: ordering, evaluation, numerical
association, errors, effects, lifetime, concurrency, resource use, and target
configuration.

A generated opcode cannot grant a missing capability. Mark unsupported lowering
explicitly.

## 7. Diagnostics

Choose compact structured errors useful to another model call.

```text
PARSE <node/ref> <code>
TYPE  <inst> <operand> <got> <need>
STATE <inst> <got-state> <allowed-states>
RES   <inst> <resource> <got> <limit>
LOWER <inst> <target> <reason>
CAP   <inst> <missing-capability>
```

Adapt the encoding to the language; preserve locality and determinism.

## 8. Contrastive acquisition cases

Give only a few high-information examples.

### Valid

```text
<small language program>
```

Why it is legal / what it teaches:

### Invalid representation

```text
<small invalid program>
```

Expected diagnostic:

### Structurally valid but task-wrong

```text
<small language program>
```

Counterexample / distinction:

This last case is important: it preserves the difference between language validity
and external task correctness.

## 9. Freeze check

Before giving the language to the programmer:

- grammar/serialization is unambiguous;
- operator signatures are complete;
- legality rules are internally consistent;
- every executable operation has a real lowering or an explicit unsupported status;
- task-critical distinctions intended to be structural are actually represented;
- the language does not silently grant host capabilities;
- the language revision is frozen for the attempt.

## 10. Program handoff

Give the programmer the frozen task plus this language definition. Do **not** give a
complete host-language solution. The programmer must generate the algorithm in the
task language first.

---

## Legacy `intseq/0.1` compatibility example

When the lowering target is the repository's current capsule format, the emitted
machine artifact still obeys the exact supported schema. A valid minimal legacy
capsule is:

```json
{
  "protocol": "arl-capsule/0.1",
  "pack": "intseq/0.1",
  "input": {"x": "VecInt"},
  "output": "Int",
  "primitives": ["seq.sum"],
  "macros": []
}
```

Only the fields/semantics permitted by the versioned intseq format may appear in
that artifact. The experimental task language is free to be richer **above** this
boundary, provided its lowering preserves the established `intseq/0.1` meaning.
