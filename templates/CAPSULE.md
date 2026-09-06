# Capsule template: make the solver's decisions smaller, not hidden

Use this template only for the currently supported `intseq/0.1` capsule format.
The JSON fence must follow [the exact schema](../packs/intseq/CAPSULE.md); fields
invented in prose are not executable. A host/checker computes the canonical hash
after the capsule is finalized.

## Design the interface before editing the JSON

Choose the narrowest interface that still supports strong implementations:

- **Primitives:** include operations the solver genuinely needs. Removing irrelevant
  surface can help; removing a competitive algorithmic route can hurt.
- **Macros:** add only transparent, typed compositions that eliminate repeated or
  error-prone structure. Their meaning is their primitive expansion, and their
  construction cost is part of the solution cost.
- **Output type:** make it match the task-facing value produced by programs; the
  capsule still does not define task correctness.
- **Examples:** keep them outside the machine artifact. Prefer tiny contrastive cases
  that teach composition or edge semantics without embedding the whole solution.

Before freezing, ask: what important decision remains for the programmer? If the
answer is “none; the macro already encodes the task,” treat the macro as algorithm
synthesis and account for it accordingly.

## Supported artifact

This valid minimal starting point exposes only `seq.sum`:

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

Edit only `output`, `primitives`, and `macros` within the supported schema. The
input remains exactly `{"x":"VecInt"}` in v0.1. Macro bodies may use selected
primitives and their own parameters, not other macros or host capabilities.

## Freeze check

Use the actual checker to validate the final capsule, then compute its canonical
JSON SHA-256 with the reference/runtime recipe. Freeze that identity before program
generation. Do not hand-edit a hash, infer admission from visual inspection, or
change the capsule under an existing identity.
