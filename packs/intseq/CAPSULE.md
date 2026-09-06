# intseq capsule and program formats

The runtime accepts exactly one `json` fenced block per Markdown input artifact.
Fence markers occupy their own lines. Surrounding prose is ignored by the parser
and cannot grant permissions. Duplicate JSON keys and non-JSON constants are
rejected. Unknown object fields are rejected rather than guessed.

## Capsule: arl-capsule/0.1

Exactly these keys: `protocol`, `pack`, `input`, `output`, `primitives`, `macros`.
`protocol` is `arl-capsule/0.1`; `pack` is `intseq/0.1`; `input` is exactly
`{"x":"VecInt"}`. `output` is `Int` or `VecInt`. `primitives` is a nonempty,
duplicate-free array of IDs from PACK.md. `macros` is an array, possibly empty.

Each macro has exactly `name`, `params`, `returns`, `body`. Names match
`[a-z][a-z0-9_]{0,31}`. Parameters are distinct `[name,type]` pairs; valid types are
`Int` and `VecInt`. There must be 1–8 parameters. Macro names are unique.
`returns` must match the type inferred for `body`. The body may use only its
parameters, integer literals, and selected primitives—not any macro calls.

Call a macro as `["macro.NAME", arguments...]`. Program expressions may nest
macro calls. Body-to-body macro calls and recursive definitions are not supported.
There are no implicit capabilities or source-code escape hatches.

## Program: arl-program/0.1

Exactly these keys: `protocol`, `capsule_sha256`, `expr`. The protocol is
`arl-program/0.1`; the hash is the actual canonical capsule JSON hash, not a file
hash or guessed identifier. The expression must typecheck to the capsule output.

The reference expands macros to primitive expressions and rechecks that result.
It does not parse a task contract, synthesize a program, infer a missing operation,
solve holes, or run a hidden test suite.

## Identity recipe

The normative recipe is `digest` in runtime/REFERENCE.md: sorted object keys,
compact JSON separators, ASCII escapes, strict JSON numeric values, UTF-8, then
SHA-256. This is a project-local canonical form, not a claim of implementing any
external JSON canonicalization standard. Equivalent macro spellings can have
different hashes. Semantic equivalence is not established by identity.
