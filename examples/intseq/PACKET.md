# Programmer packet — `nonnegative-affine-sum`

This is a self-contained context for one program-generation call. It is a derived
view, not a new semantic authority. The runtime does not assemble or validate
packets.

## Solve the semantic dependency first

Input `x` is a list of 0..4,096 integers in `[-1000000,1000000]`.

Return:

```text
sum(3*v + 5 for each original element v where v >= 0)
```

The word **original** determines the dataflow. Eligibility must be decided before
the affine transform:

```text
x -> filter_ge(0) -> affine(3,5) -> sum
```

Filtering after the transform is wrong because a negative value can cross the
threshold. The public discriminator is `[-1,0]`: transform-then-filter produces
`7`, while the task requires `5`.

Duplicates contribute independently. Empty selection sums to `0`. Arithmetic is
exact. Performance is not scored.

## Available interface

Expression forms:

- integer literal -> `Int`;
- `"x"` -> `VecInt`;
- `["op", ...]` -> application.

No booleans, floats, vector literals, implicit casts, holes, assignments, or
ambient names.

| Callable operation | Signature | Meaning |
|---|---|---|
| `seq.filter_ge` | `VecInt, Int -> VecInt` | keep values at least the threshold; preserve order/duplicates |
| `seq.mul` | `VecInt, Int -> VecInt` | scalar multiply |
| `seq.add` | `VecInt, Int -> VecInt` | scalar add |
| `seq.sum` | `VecInt -> Int` | exact left-to-right sum; empty -> `0` |
| `macro.affine` | `VecInt, Int, Int -> VecInt` | checked expansion `add(mul(v,a),b)` |

Use only this frozen interface. The checker enforces names, arity, types, scope,
capsule identity, expansion, and resource bounds. It does **not** know whether the
algorithm satisfies the task.

## Frozen capsule

```json
{
  "protocol": "arl-capsule/0.1",
  "pack": "intseq/0.1",
  "input": {
    "x": "VecInt"
  },
  "output": "Int",
  "primitives": [
    "seq.filter_ge",
    "seq.mul",
    "seq.add",
    "seq.sum"
  ],
  "macros": [
    {
      "name": "affine",
      "params": [
        [
          "v",
          "VecInt"
        ],
        [
          "a",
          "Int"
        ],
        [
          "b",
          "Int"
        ]
      ],
      "returns": "VecInt",
      "body": [
        "seq.add",
        [
          "seq.mul",
          "v",
          "a"
        ],
        "b"
      ]
    }
  ]
}
```

Canonical capsule SHA-256:
`2a340d75023574cd3b55590dfe5583700984ded258b1257f316dd7b6490e2ee9`.

## Construction strategy

The task decomposes without search:

1. select the values whose **original** value is nonnegative;
2. apply `3*v + 5` to the survivors;
3. sum the resulting sequence.

The capsule already provides the exact generic composition needed for step 2.
There is no reason to invent another operation or reproduce the macro body manually
unless doing so answers a concrete engineering question.

Before emitting, mentally check the few cases that discriminate the algorithm:

| Input | Required result | Why it matters |
|---|---:|---|
| `[]` | `0` | empty reduction |
| `[-1]` | `0` | negative value must be rejected before transformation |
| `[0]` | `5` | threshold is inclusive |
| `[-2,-1,0,2]` | `16` | mixed values, transform, multiplicity, reduction |
| `[-1,0]` | `5` | catches transform-before-filter |

Do not infer task success from typechecking. If an actual checker/evaluator is
available, use its concrete diagnostic; do not invent a transcript.

## Output contract

Emit one program artifact with exactly the keys `protocol`, `capsule_sha256`,
`expr`. Use protocol `arl-program/0.1`, the exact capsule hash above, and an
expression whose result type is `Int`.

The program is data. It may not add permissions, primitives, source code, a new
backend, or an oracle. If an operation is absent, report that fact rather than
naming an imaginary one.

## Stable semantic bindings

This packet is derived context, so its exact prose version is identified by Git
rather than by recursively hashing other Markdown wrappers. Whole-file source hashes
remain preserved as bootstrap provenance in `docs/provenance/SOURCE-MAP.md`; they
are not live compatibility pins after those wrappers legitimately evolve.

The packet instead binds the facts that can change executable meaning:

- `task_id`: `nonnegative-affine-sum`
- `contract_version`: `0.1`
- `pack`: `intseq/0.1`
- `capsule_protocol`: `arl-capsule/0.1`
- `program_protocol`: `arl-program/0.1`
- `capsule_canonical_json_sha256`: `2a340d75023574cd3b55590dfe5583700984ded258b1257f316dd7b6490e2ee9`
- `reference_python_fence_sha256`: `4025a0043e958785196e35d6530ec4570dcedd36cf621b555249a1809649dc91`

The documentation checker recomputes the embedded capsule's canonical identity and
compares these bindings with the current task, canonical example, and preserved
reference source. A semantic mismatch makes the packet stale; a prose improvement
does not.
