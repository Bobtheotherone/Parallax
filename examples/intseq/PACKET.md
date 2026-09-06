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

## Source bindings

These are whole-file SHA-256 bindings for the packet's five source dependencies,
not canonical JSON hashes. They allow a host to detect stale derived context.

- `examples/intseq/TASK.md`: `f08bce72ad70d544409917c41af5b07dcb9a15c84731b733f32b40464a9b4f50`
- `examples/intseq/CAPSULE.md`: `344028890a820dc74b7c4b9d82180d39111fb39db95b4e9720ca419e454268f2`
- `packs/intseq/PACK.md`: `1d3de58d8bbdb9334f2fee2d40135aada79e26b35decc9cbe146e0c099ff717b`
- `packs/intseq/CAPSULE.md`: `f38fcb922a05528d1dc8db48127a6bb5eef4a5555420bf2f35f5886ef5a30029`
- `roles/PROGRAMMER.md`: `6d13cda30c80161317b29ed7f450c8367b49072d8cd1de2839e2ecbd3f9736a9`
