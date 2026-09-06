# Capsule template: supported intseq subset

This is a valid minimal capsule, not a general-purpose metalinguistic grammar.
It exposes sum only. Modify its permitted primitives and checked macro definitions
using packs/intseq/CAPSULE.md, then compute its canonical JSON hash with the host.
The runtime cannot execute future conceptual fields described in core/CAPSULE.md.

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
