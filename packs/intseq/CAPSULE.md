# intseq capsule and program formats

This document defines the executable `intseq/0.1` artifact formats. It is a wire
contract, not a tutorial and not a capability request. Preserve the legacy protocol
identifiers: changing their meaning requires a new explicit version.

## Document extraction

A runtime input document contains exactly one lowercase `json` fenced block. Fence
markers occupy their own lines. Prose outside the block is ignored by the artifact
parser and has no authority.

Parsing is strict:

- the UTF-8 document/JSON byte limit is enforced;
- duplicate object keys are rejected;
- non-JSON constants such as `NaN` and `Infinity` are rejected;
- objects use exact key sets where specified below;
- unknown fields are errors, never forward-compatible permission grants.

## Capsule: `arl-capsule/0.1`

A capsule object has exactly these keys:

| Key | Required value |
|---|---|
| `protocol` | exactly `arl-capsule/0.1` |
| `pack` | exactly `intseq/0.1` |
| `input` | exactly `{"x":"VecInt"}` |
| `output` | `Int` or `VecInt` |
| `primitives` | nonempty duplicate-free array of stable IDs from [PACK.md](PACK.md) |
| `macros` | array of zero to 16 macro definitions |

The primitive list is an **allowlist**. A runtime knowing another `intseq` primitive
does not make that primitive callable from this capsule.

### Macro definition

Each macro has exactly `name`, `params`, `returns`, and `body`.

- `name` matches `[a-z][a-z0-9_]{0,31}` and is unique within the capsule.
- `params` contains 1–8 distinct `[name,type]` pairs. Types are only `Int` and
  `VecInt`.
- `returns` is `Int` or `VecInt` and must equal the statically inferred body type.
- `body` is an expression over integer literals, the macro's parameters, and only
  the capsule's selected **primitive** operations.
- A macro body cannot call itself or another macro. This makes every definition a
  bounded one-step abstraction over stable pack semantics.

Programs call a macro as `["macro.NAME", arg1, ...]`. Program expressions may nest
admitted macro calls because expansion recursively removes them. Macro definitions
are all checked before their callable signatures are added, which prevents body-to-
body calls and recursion by construction.

The macro's meaning is its hygienic expansion. Actual arguments are interpreted in
the caller's scope; substitution must not reinterpret a caller variable as a
callee parameter merely because the strings match. There are no arbitrary source
lowerings, imports, side effects, or hidden native implementations in this format.

## Program: `arl-program/0.1`

A program object has exactly:

| Key | Required value |
|---|---|
| `protocol` | exactly `arl-program/0.1` |
| `capsule_sha256` | canonical JSON SHA-256 of the exact capsule object |
| `expr` | expression whose inferred type equals the capsule output |

A hash mismatch is an identity failure, not something to repair by ignoring the
binding. Rebind only to an explicitly selected capsule and regenerate or recheck
the program against that capsule.

## Expression-checking algorithm

The executable contract is easiest to reason about as a small pipeline:

```text
read document
  -> strict JSON parse
  -> validate exact capsule schema/version/input/output
  -> build signatures for selected primitives
  -> for each macro:
       validate fields/names/params
       infer body using parameters + selected primitive signatures only
       require inferred type == declared return type
  -> add checked macro call signatures

check program
  -> validate exact program schema/version
  -> require capsule_sha256 == digest(capsule)
  -> infer program expr using input x + primitive/macro signatures
  -> require inferred type == capsule output
  -> expand macros by lexical substitution
  -> infer expanded tree again using selected primitive signatures only
  -> return primitive tree
```

The final primitive-only recheck is important: successful surface typing is not a
license for expansion to escape the allowlist or produce an ill-typed primitive
IR.

## Identity recipe

`runtime/REFERENCE.md`'s `canonical`/`digest` functions are normative for v0.1:
serialize JSON with sorted object keys, compact separators, ASCII escapes, and no
non-JSON numeric constants; encode as UTF-8; compute SHA-256 over those bytes.
Array order is preserved. There is no trailing newline in the canonical JSON bytes.

This is a project-local canonicalization recipe, not a claim of implementing an
external JSON canonicalization standard. Equivalent-looking source formatting can
hash identically after parsing; semantically equivalent but structurally different
expressions can hash differently. A digest binds content—it does not prove
correctness or authenticate authorship.

## Failure locality

The reference uses distinct rejection classes so diagnosis can target the right
layer:

| Code | Typical meaning |
|---|---|
| `SCHEMA` | malformed JSON/artifact shape, duplicate key/name, invalid expression form |
| `VERSION` | unsupported protocol or pack identifier |
| `OP_NOT_ALLOWED` | primitive/macro unavailable in the relevant scope |
| `TYPE` | unbound variable, arity mismatch, argument/result type mismatch |
| `HASH_MISMATCH` | program is not bound to this canonical capsule |
| `RESOURCE_LIMIT` | document/tree/integer/expansion/runtime policy exceeded |

These codes do not decide whether an admitted program implements a task correctly.
That requires the external task contract and acceptance mechanism.

## Capability boundary

The format can select supported primitives and compose them into checked macros. It
cannot invent a primitive, install a backend, grant filesystem/network/GPU access,
change resource policy, or choose an acceptance oracle. Those are host/runtime or
versioned pack decisions outside generated artifact authority.
