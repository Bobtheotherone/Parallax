# Failure that the language must not hide

This alternative expression is well-typed under the example capsule:

```text
["seq.sum", ["seq.filter_ge", ["macro.affine", "x", 3, 5], 0]]
```

On `[-1,0]` it returns `7`; the frozen task requires `5`. Filtering after the
transformation admits the transformed value of an originally negative input.
The static checker should not pretend its type rules know the task contract.

Correct diagnosis: algorithm/order error. Repair the program by filtering the
original values first. Do not add a primitive, change the meaning of filter,
weaken the oracle, or claim the language cannot express the task.

Other failures have different owners: an unknown operation is a capsule/program
issue; a hash mismatch is an identity issue; a runtime limit is a resource issue;
a missing GPU backend is an implementation-capability issue. Route them using
core/PROTOCOL.md rather than handling every failure through language evolution.
