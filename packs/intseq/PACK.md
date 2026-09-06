# intseq/0.1 semantic pack

Status: executable reference available in runtime/REFERENCE.md. Pure finite integer
sequences; no floating point, tensors, I/O, pointers, or native code generation.

## Types and inputs

`Int` denotes a mathematical integer. `VecInt` denotes an ordered finite sequence
of integers. The only program input is `x: VecInt`. Integers and variable names
are expression leaves; a literal vector is not part of the expression grammar.
Booleans and floats are not integers in this pack.

An input/output belongs to the mathematical semantics independently of host
resources. The reference rejects inputs or computations exceeding its resource
limits; it never silently wraps, saturates, or approximates an integer.

## Operation table

| Stable ID | Signature | Meaning |
|---|---|---|
| seq.add | VecInt, Int -> VecInt | Add the scalar to every element, preserving order |
| seq.mul | VecInt, Int -> VecInt | Multiply every element by the scalar, preserving order |
| seq.filter_ge | VecInt, Int -> VecInt | Keep elements greater than or equal to the threshold; preserve order and duplicates |
| seq.sum | VecInt -> Int | Sum all elements; empty sum is zero |
| seq.count | VecInt -> Int | Number of elements, including duplicates |
| int.add | Int, Int -> Int | Exact integer addition |
| int.mul | Int, Int -> Int | Exact integer multiplication |

Every capsule exposes a nonempty subset. Using an operation outside that subset
is rejected even if the reference runtime knows how to implement it.

## Expression syntax

A JSON integer is an `Int` literal. A JSON string is a variable reference. A JSON
array `["operation", arg1, ...]` applies a primitive or admitted macro. Arrays are
not data literals. There are no implicit casts, overloaded arithmetic, loops,
assignments, arbitrary evaluation, or ambient names.

A macro is a typed expression over permitted primitives and its named parameters.
No free variables are permitted. Its meaning is its hygienic expansion. See
[CAPSULE.md](CAPSULE.md) for the exact format and [TUTORIAL.md](TUTORIAL.md) for
three examples and two counterexamples.

## Reference limits and behavior

Maximum document/JSON input size is 65,536 UTF-8 bytes; input vectors have at most
4,096 elements; expression checking and expansion have depth 32/node 4,096
budgets; integers have at most 256 magnitude bits. Evaluation charges expression
visits plus sequence-element work and rejects above 250,000 work units. There are
at most 16 macros and at most 8 parameters per macro. These are prototype host
policies, not parameters supplied by a capsule.

The interpreter evaluates arguments eagerly, left to right. `seq.sum` accumulates
left to right and checks each intermediate integer. Exceeding an intermediate
limit is `RESOURCE_LIMIT`, even if a mathematically equivalent expression could
finish within the budget. It is not a task-correctness result.

## Assurance scope

Structural checks enforce the selected operation set, arity, variable scope,
types, capsule binding, and expansion limits. Tests support implementation
confidence. Neither validates arbitrary task intent or constitutes formal proof.
