# intseq programmer tutorial

One input: `x`, an ordered integer sequence. Write JSON expression arrays; bare
strings refer to variables and bare integers are scalar literals. Every operation
used must appear in the frozen capsule. Return the capsule's declared type.

## Example 1: sum

```text
["seq.sum", "x"]
x = [2,-1,2]  -> 3
x = []       -> 0
```

## Example 2: filter before transforming

```text
["seq.sum", ["seq.add", ["seq.mul", ["seq.filter_ge", "x", 0], 3], 5]]
x = [-1,0,2] -> 16
```

Only original nonnegative elements contribute. The zero contributes five.
Changing the filter's position can change the task, despite identical types.

## Example 3: compositional macro

A capsule may define `affine(v,a,b)` as
`["seq.add", ["seq.mul", "v", "a"], "b"]`, with `(VecInt,Int,Int)->VecInt`.
Then the previous program can be written:

```text
["seq.sum", ["macro.affine", ["seq.filter_ge", "x", 0], 3, 5]]
```

The macro is not built in: it must be present and checked in this capsule.

## Counterexample 1: structural rejection

```text
["seq.sum", 3]
```

Rejected: sum requires a sequence, not an integer. An unsupported `seq.average`
would also be rejected rather than invented.

## Counterexample 2: well-typed but wrong for Example 2's task

```text
["seq.sum", ["seq.filter_ge", ["macro.affine", "x", 3, 5], 0]]
x = [-1,0] -> 7, but the required result is 5
```

The interpreter should accept this expression structurally. The task oracle must
reject it functionally. A small language is not an oracle for algorithmic intent.
