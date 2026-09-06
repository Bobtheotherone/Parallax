# Frozen programmer packet: nonnegative-affine-sum

A compact, materialized context view for one program-generation call. It is not a
new authority: the host should check the source identities before using it. The
bundled interpreter does not assemble or validate packets. No model call against
this packet has been measured. Do not load the full repository for this call.

## Task and boundary

Input `x` is a list of 0..4096 integers in [-1000000,1000000]. Return the exact sum
of `3*v + 5` over elements `v` that were nonnegative **before** transformation.
Duplicates contribute separately. An empty sum is zero. No I/O is part of the
program. Target: the bundled intseq interpreter. Performance is not scored.

The language checker is not the task oracle. Emit a candidate, then have the
actual tools check it. Do not claim tests or execution were performed without
their results. Do not change the task, capsule, permissions, or checker.

## Selected semantics

Expressions are JSON integers, variable strings, or application arrays
`["op", arg1, ...]`. Input variable `x` has type `VecInt`; integer literals have
type `Int`. No booleans, floats, implicit casts, literal vectors, or holes.

`seq.filter_ge(VecInt,Int)->VecInt` keeps values >= the threshold, with order and
duplicates preserved. `seq.mul(VecInt,Int)->VecInt` multiplies each value by the
scalar. `seq.add(VecInt,Int)->VecInt` adds the scalar to each value.
`seq.sum(VecInt)->Int` returns the exact sum, zero for an empty sequence.

The macro below means its primitive expansion. Bodies cannot call macros, while
programs can nest admitted macro calls. Only selected primitives and this macro
are callable. Resource excess may cause rejection; it does not authorize changing
the answer or silently wrapping integers.

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

Canonical capsule SHA-256: `2a340d75023574cd3b55590dfe5583700984ded258b1257f316dd7b6490e2ee9`.

## Micro-examples

`["seq.sum","x"]` on `[2,-1]` gives `1`.
`["seq.filter_ge","x",0]` on `[-1,0,2]` gives `[0,2]`.
`["macro.affine","x",2,1]` on `[1,3]` gives `[3,7]`.

`["seq.sum",3]` is ill-typed. `seq.count` is unavailable in this capsule, even
though another capsule might expose it. Structurally valid programs can still
violate the task's filtering-order requirement.

## Output

Emit one JSON fence containing exactly `protocol`, `capsule_sha256`, `expr`.
Use protocol `arl-program/0.1`, the exact hash above, and an expression of result
type `Int`. Outside that candidate, report only actual evidence or missing tools.
No unimplemented operation, guessed hash, or invented tool transcript is valid.

## Source file identities

The following are whole-file SHA-256 hashes, not canonical JSON hashes.

- `examples/intseq/TASK.md`: `f08bce72ad70d544409917c41af5b07dcb9a15c84731b733f32b40464a9b4f50`
- `examples/intseq/CAPSULE.md`: `33bd94fe2226635f81af35fe5b897f618d036d0d2341aac0e8694a6aaca812d8`
- `packs/intseq/PACK.md`: `1d3de58d8bbdb9334f2fee2d40135aada79e26b35decc9cbe146e0c099ff717b`
- `packs/intseq/CAPSULE.md`: `f38fcb922a05528d1dc8db48127a6bb5eef4a5555420bf2f35f5886ef5a30029`
- `roles/PROGRAMMER.md`: `6d13cda30c80161317b29ed7f450c8367b49072d8cd1de2839e2ecbd3f9736a9`
