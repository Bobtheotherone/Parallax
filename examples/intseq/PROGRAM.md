# Worked intseq program: preserve predicate provenance

This is the canonical program artifact for the frozen `nonnegative-affine-sum`
example. The JSON remains an `arl-program/0.1` program bound to the canonical
example capsule. The surrounding explanation is a reasoning aid; it does not alter
the program or grant authority.

## Derive the dataflow before writing syntax

For input sequence `x`, the task is

\[
F(x)=\sum_{v\in x,\ v\ge 0}(3v+5).
\]

The predicate is about each **original** value. That gives an invariant before any
syntax is chosen:

```text
original x
  -> retain v where v >= 0
  -> transform retained v to 3*v + 5
  -> sum
```

The capsule's `affine(v,a,b)` macro expands to `seq.add(seq.mul(v,a),b)`, so the
program can express the same plan compactly. Expansion produces the primitive
dataflow

```text
seq.sum(
  seq.add(
    seq.mul(
      seq.filter_ge(x, 0),
      3),
    5))
```

Filtering after the affine transform would be well typed but would change which
original elements contribute. On `[-1,0]`, the frozen program returns `5`; the
wrong-order expression in [FAILURE.md](FAILURE.md) returns `7`. This is the useful
counterexample: types validate the interface, while the task contract validates
the algorithm.

## Frozen program

```json
{
  "protocol": "arl-program/0.1",
  "capsule_sha256": "2a340d75023574cd3b55590dfe5583700984ded258b1257f316dd7b6490e2ee9",
  "expr": [
    "seq.sum",
    [
      "macro.affine",
      [
        "seq.filter_ge",
        "x",
        0
      ],
      3,
      5
    ]
  ]
}
```

Canonical program JSON SHA-256:
`db2dad5bd80762eb3fa6eeba57410027755dfdcc57d22ff212236b99613b1517`.

## High-information checks

Before relying on broad randomized coverage, a few inputs discriminate the main
algorithmic hypotheses:

| Input | Required value | What it probes |
|---|---:|---|
| `[]` | `0` | empty reduction identity |
| `[-3,-1]` | `0` | all elements excluded |
| `[-1,0]` | `5` | filter-before-transform ordering |
| `[0,0,2]` | `21` | zero handling and multiplicity |
| `[-2,-1,0,2]` | `16` | mixed-path composition |

A successful parse, capsule-hash check, typecheck, expansion, or evaluation answers
a representation/runtime question. Task acceptance remains a separate comparison
against the frozen [task](TASK.md) and its oracle policy.
