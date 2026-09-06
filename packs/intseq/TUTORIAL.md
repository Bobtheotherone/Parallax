# intseq problem-solving tutorial

`intseq` is easiest to use as a typed dataflow language. Start from the task's
mathematical structure, then map each step to operations exposed by the frozen
capsule. Do not start by permuting syntax until something passes.

One top-level input exists: `x: VecInt`. Bare JSON integers are `Int` literals;
bare strings are variable references; arrays are operation calls. Every called
primitive or macro must be admitted by the capsule, and the final expression type
must equal the capsule output type.

## 1. Compress the task into a pipeline

Most useful `intseq` tasks decompose into some combination of:

```text
select elements       -> seq.filter_ge
transform elements    -> seq.mul / seq.add
aggregate sequence    -> seq.sum / seq.count
combine scalar results-> int.add / int.mul
```

The critical question is **what each predicate observes**. If a requirement says
“original nonnegative values,” filtering must happen before any transformation that
can change sign. Types cannot recover that semantic fact for you.

For the worked task

\[
\sum_{v\in x, v\ge 0}(3v+5),
\]

the dataflow is `filter -> multiply -> add -> sum`.

```text
["seq.sum",
  ["seq.add",
    ["seq.mul",
      ["seq.filter_ge", "x", 0],
      3],
    5]]
```

On `[-1,0,2]` the result is `16`.

## 2. Build the typed tree inside-out

Before generation, annotate intermediate types:

```text
x                                      : VecInt
["seq.filter_ge", "x", 0]             : VecInt
["seq.mul", <VecInt>, 3]              : VecInt
["seq.add", <VecInt>, 5]              : VecInt
["seq.sum", <VecInt>]                 : Int
```

This catches local structural errors early and keeps algorithm reasoning separate
from serialization. A checker should confirm the result; the annotation is a
planning technique, not fabricated tool evidence.

A minimal sum is simply:

```text
["seq.sum", "x"]
```

`[2,-1,2] -> 3`, and `[] -> 0`.

## 3. Use macros for stable repeated structure

Suppose the capsule defines

```text
affine(v,a,b) = ["seq.add", ["seq.mul", "v", "a"], "b"]
(VecInt, Int, Int) -> VecInt
```

Then the worked task becomes:

```text
["seq.sum", ["macro.affine", ["seq.filter_ge", "x", 0], 3, 5]]
```

A macro is useful when it packages a meaningful reusable composition and reduces
surface search without hiding new authority. It is not a built-in operation and
cannot be called unless the frozen capsule defines it. In v0.1 macro bodies cannot
call other macros; program expressions may nest admitted macro calls.

## 4. Compose scalar summaries when the task needs them

If a capsule exposes `seq.sum`, `seq.count`, `int.add`, and `int.mul`, scalar
aggregates can be combined without inventing sequence literals or loops. For
example, the expression

```text
["int.add",
  ["seq.sum", "x"],
  ["int.mul", ["seq.count", "x"], 2]]
```

computes `sum(x) + 2*len(x)` and has type `Int`. This pattern is useful when a task
contains multiple reductions that feed a scalar formula. It also illustrates that
an operation implemented by the pack is still unavailable if the current capsule
did not select it.

## 5. Choose discriminating examples, not many redundant ones

A few boundary inputs can distinguish plausible algorithms better than a large set
of easy cases. For the worked filter/affine task, use at least:

| Input | Why it is informative |
|---|---|
| `[]` | reduction identity |
| `[-2,-1]` | no element qualifies |
| `[-1,0]` | distinguishes filter-before-transform from transform-before-filter |
| `[0,0,2]` | boundary value plus multiplicity |
| mixed positive/negative input | ordinary composition |

After the structural hypothesis is sound, broader differential/property testing
can increase confidence over a stated domain.

## 6. Diagnose by layer

### Ill-typed

```text
["seq.sum", 3]
```

`seq.sum` requires `VecInt`, so this is a local type/dataflow failure.

### Operation unavailable

```text
["seq.average", "x"]
```

There is no such `intseq/0.1` primitive. Do not infer its semantics from its name.
Likewise, `seq.count` is rejected if the current capsule did not select it.

### Well typed, wrong algorithm

For the worked task, this expression is structurally valid under the example
capsule:

```text
["seq.sum", ["seq.filter_ge", ["macro.affine", "x", 3, 5], 0]]
```

On `[-1,0]` it returns `7`, but the task requires `5`. The failure is predicate
provenance/order, so the repair is to filter the original sequence first. Adding a
primitive or weakening the oracle would treat the symptom at the wrong layer.

### Resource rejection

A valid expression can exceed document, tree, integer, vector, expansion, or work
limits. That does not prove the intended function is unexpressible. Inspect which
resource was exceeded and whether a permitted alternative representation avoids
the expensive intermediate while preserving required behavior.

Be careful with algebraic rewrites: exact mathematical equivalence does not imply
identical v0.1 resource behavior because evaluation is eager, integer intermediates
are checked, and sequence work is charged.

## 7. A high-information repair loop

When a tool rejects or a task example fails, use the diagnostic to choose the next
experiment:

```text
observe exact failure
  -> localize: schema | allowlist | hash | type | resource | task behavior
  -> form at least two plausible causes when unclear
  -> choose the smallest input/expression that distinguishes them
  -> repair the root dataflow or representation error
  -> recheck the affected property
```

Do not respond to every failure by expanding the language. A missing capability is
credible only after the required behavior is clear and reasonable compositions of
admitted operations have been ruled out within the actual search/budget—not merely
because one candidate failed.

For the exact wire format, macro restrictions, canonical hash, and rejection
classes, use [CAPSULE.md](CAPSULE.md). For primitive meanings and resource policy,
use [PACK.md](PACK.md). Those documents define behavior; this tutorial teaches how
to reason with it.
