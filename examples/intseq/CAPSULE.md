# Example capsule — minimal task-facing interface

This is a machine-readable fixture plus a compact explanation. The runtime consumes
the **single** `json` fence and ignores the prose.

The capsule exposes `filter_ge`, `mul`, `add`, and `sum`, plus one generic
`affine(v,a,b)` macro whose meaning is exactly the checked expansion

```text
["seq.add", ["seq.mul", "v", "a"], "b"]
```

The macro contains no task constants and no task oracle. A program still decides
the filter threshold, coefficients, operation order, and therefore the algorithm.

Canonical capsule SHA-256:
`2a340d75023574cd3b55590dfe5583700984ded258b1257f316dd7b6490e2ee9`.

The original archived Markdown wrapper had whole-file SHA-256
`33bd94fe2226635f81af35fe5b897f618d036d0d2341aac0e8694a6aaca812d8`.
That value is historical provenance; this rewrite changes the wrapper but preserves
the canonical JSON identity and meaning.

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

Read this fixture at three layers:

- **admission:** names, types, scope, fields, and macro body are permitted;
- **representation preservation:** expansion is hygienic and rechecks as the same
  primitive computation;
- **task satisfaction:** the external program chooses the right algorithm.

The last obligation is deliberately outside the capsule. For the worked task,
“originally nonnegative” requires filtering before the affine transform; the type
system cannot infer that intent. [FAILURE.md](FAILURE.md) shows the well-typed
counterexample.
