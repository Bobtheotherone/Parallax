# Frozen example capsule

Four primitives and one compositional macro; no task oracle is encoded in the primitive runtime. The macro parameters do not contain the task constants.

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
