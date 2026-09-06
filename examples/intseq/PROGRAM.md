# Frozen example program

The program chooses the filtering order, transformation coefficients, and reduction. Its hash binds it to the capsule JSON.

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
