# Typed but wrong: localize the semantic error

A useful checker must reject malformed programs without pretending that types encode
the user's algorithm. This expression is the canonical counterexample:

```text
["seq.sum", ["seq.filter_ge", ["macro.affine", "x", 3, 5], 0]]
```

It is well-formed and well-typed under the example capsule. On `[-1,0]` it evaluates
to `7`; the frozen task requires `5`.

## Why it fails

Write the two meaningful operations as functions:

```text
F(x) = keep elements v where v >= 0
A(x) = map v -> 3*v + 5
```

The task requires:

```text
sum(A(F(x)))
```

The candidate computes:

```text
sum(F(A(x)))
```

`F` and `A` do not commute. In particular, the affine transform can move an
originally negative value across the filter boundary. For `v = -1`,
`3*v + 5 = 2`, so the wrong ordering admits a value that the contract excludes.

This is a high-information diagnosis because it identifies the violated invariant
and a boundary-crossing witness, rather than merely observing “expected 5, got 7.”

## Layer-by-layer result

| Layer | Result | What it tells us |
|---|---|---|
| parse/schema | pass | the artifact has a supported shape |
| capsule binding / allowlist | pass | it uses the frozen interface |
| type check | pass | every operation receives the right type |
| macro expansion / primitive recheck | pass | lowering preserves the represented program |
| evaluation | pass | the runtime can compute the represented behavior |
| task acceptance | **fail** | the represented algorithm is wrong |

The defect therefore belongs to **algorithm/order reasoning**, not the parser,
type system, macro mechanism, primitive semantics, or runtime capability.

## Root-cause repair

Move the filter to the original sequence before the affine transform:

```text
["seq.sum", ["macro.affine", ["seq.filter_ge", "x", 0], 3, 5]]
```

Do not respond to this counterexample by adding a primitive, changing
`seq.filter_ge`, weakening the task oracle, or claiming the capsule is
inexpressive. All required operations are already present.

## Diagnostic pattern to reuse

When a typed pipeline gives a wrong answer:

1. Compare the task's semantic predicates with the program's dataflow order.
2. Identify adjacent transforms whose order might change membership, rounding,
   state, ownership, or effects.
3. Construct the smallest input near that boundary that distinguishes the two
   orders.
4. Repair the earliest wrong semantic decision, then re-run the same witness.

Other observations route elsewhere: an unknown operation is an admission problem;
a hash mismatch is identity; a resource rejection is resource policy; an absent
backend is implementation capability. Do not funnel every failure into language
evolution.
