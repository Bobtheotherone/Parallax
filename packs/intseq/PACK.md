# intseq/0.1 semantic pack

`intseq/0.1` is a deliberately small executable semantic domain for pure finite
integer-sequence transformations. Its reference implementation is embedded in
`runtime/REFERENCE.md`. There is no floating point, tensor semantics, I/O, mutable
state, pointers, native code generation, or implicit ambient capability.

This file owns the meaning of the seven stable primitive IDs. Representation
artifacts may select these operations; they do not redefine them.

## Semantic domains

`Int` is a mathematical integer. `VecInt` is an ordered finite sequence of
mathematical integers. The only program input is `x: VecInt`.

Expression leaves are:

- JSON integers, denoting `Int` literals;
- JSON strings, denoting variables in the current lexical environment.

An application is a JSON array `["op", arg1, ...]`. Arrays are never vector
literals in the expression grammar. Booleans and floats are not `Int`; there are
no implicit casts, overload resolution, assignments, loops, or arbitrary eval.

The mathematical domains are conceptually distinct from the prototype's resource
policy. When evaluation succeeds, integer results are exact. The runtime may reject
an otherwise meaningful computation because its configured limits are exceeded; it
never silently wraps, saturates, truncates, or approximates a value.

## Stable primitive semantics

For a sequence `v = [v_0, ..., v_{n-1}]` and integer `a`:

| Stable ID | Signature | Exact result |
|---|---|---|
| `seq.add` | `VecInt, Int -> VecInt` | `[v_0+a, ..., v_{n-1}+a]` |
| `seq.mul` | `VecInt, Int -> VecInt` | `[v_0*a, ..., v_{n-1}*a]` |
| `seq.filter_ge` | `VecInt, Int -> VecInt` | subsequence of elements `v_i >= a`, in original order with duplicates preserved |
| `seq.sum` | `VecInt -> Int` | left-to-right exact sum; empty sequence gives `0` |
| `seq.count` | `VecInt -> Int` | `n`, including duplicate elements |
| `int.add` | `Int, Int -> Int` | exact integer addition |
| `int.mul` | `Int, Int -> Int` | exact integer multiplication |

A capsule exposes a nonempty subset of these IDs. Calling an unselected operation
is rejected even when the runtime implements it globally. See
[CAPSULE.md](CAPSULE.md) for exact capsule/program syntax and macro rules.

## Observable evaluation behavior

The reference evaluates call arguments eagerly from left to right. For sequence
operations it first evaluates arguments, then performs element work. `seq.sum`
accumulates left to right and checks every intermediate integer. Elementwise
`seq.add` and `seq.mul` check every produced integer.

These details matter because the resource policy is observable. Mathematical
identities are therefore not automatically **resource-equivalence** identities.
For example, two expressions can denote the same unbounded integer function yet
one can hit an intermediate integer or work limit first. An optimizer must not
silently use algebraic equivalence as permission to change documented rejection
behavior.

Macros add no new primitive meaning. In `arl-capsule/0.1`, a macro is a typed
expression over selected primitives and its parameters; its meaning is the checked
hygienic expansion to a primitive tree.

## Prototype resource policy

The executable reference enforces these fixed v0.1 bounds:

| Resource | Limit | Where it matters |
|---|---:|---|
| UTF-8 document / JSON bytes | `65,536` | artifact admission |
| expression depth | `32` | inference and expansion |
| expression nodes | `4,096` | inference and expansion |
| input vector length | `4,096` | evaluation |
| integer magnitude bits | `256` | literals, inputs, intermediates, results |
| evaluation work | `250,000` | expression visits plus sequence-element work |
| macros per capsule | `16` | capsule admission |
| parameters per macro | `1..8` | capsule admission |

The work counter charges an expression visit and, for sequence primitives, the
number of sequence elements processed. Expansion has its own depth/node budget.
The limits are host/runtime policy for this prototype; they are not configurable
fields supplied by a capsule.

A `RESOURCE_LIMIT` rejection describes execution/admission under this policy. It is
not a statement that the mathematical function is undefined, that the task answer
is wrong, or that no alternative allowed expression could fit the budget.

## Type and scope model

Primitive calls use the signatures above exactly. There is no subtyping or
coercion. A variable reference must be bound in the current environment. At program
top level, the only bound variable is `x: VecInt`; during macro-body checking, only
the macro's declared parameters are bound.

Useful static reasoning is therefore local and compositional: infer child types,
check them against the operation signature, then assign the operation's result
type. This can rule out malformed dataflow but cannot establish that the chosen
operations implement the external task.

## Engineering laws and non-laws

The semantics provide several reliable reasoning facts:

- `seq.add`, `seq.mul`, and `seq.filter_ge` preserve relative order of retained
  sequence elements;
- `seq.filter_ge` preserves multiplicity for retained elements;
- `seq.count([])=0` and `seq.sum([])=0`;
- exact integer arithmetic has no overflow wraparound when evaluation succeeds.

Do **not** infer task-specific laws from the pack. In particular, filtering before
and after a transformation generally differs, even if both expressions typecheck.
Do not infer that algebraically equivalent trees consume equal work or fail at the
same resource boundary.

## Failure and assurance boundary

The parser/checker can establish documented schema, operation-selection, arity,
lexical scope, types, capsule binding, expansion structure, and resource checks on
the inspected artifact. The evaluator can produce a result under the pinned
runtime policy. Neither knows the user's task intent.

A strong debugging sequence is therefore:

```text
malformed / unavailable operation -> inspect schema or capsule
well-formed but ill-typed          -> inspect local dataflow/signatures
resource rejection                -> inspect representation and policy cost
successful evaluation, wrong task -> inspect algorithm against external contract
```

Tests can provide scoped implementation evidence for these semantics, but neither
typechecking nor a finite suite is a universal proof of pack implementation or
task correctness.
