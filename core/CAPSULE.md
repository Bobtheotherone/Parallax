# Representation capsules

A capsule is a temporary interface to an existing semantic pack. It is not a
freestanding assertion that a compiler exists.

## General design object

A future full capsule may contain a pack/version reference, operation subset,
type restrictions, compositional macros, serialization, finite holes, tutorial,
capabilities required, verification obligations, and cost-model references.
Different fields have different authority. Tutorials suggest; operation semantics
define; checkers decide their documented properties; the host grants capabilities.

The executable v0.1 subset is intentionally smaller. Its exact format is in
[the intseq capsule specification](../packs/intseq/CAPSULE.md). Unsupported fields
are rejected, including arbitrary lowering source and permission requests.

## Admission obligations

Each exported operation has a fixed signature and defined semantics. Every macro
body is inspectable and typechecks using permitted primitives. The supported
runtime expands the macro to the stable primitive tree, then checks it again.
No hidden native implementation is generated during a normal capsule attempt.

A task-specific macro may encode a complete algorithm. That is not intrinsically
invalid, but its construction and validation must be charged to the system. Label
that result as macro/algorithm synthesis rather than crediting a one-token
programmer with the algorithmic work.

## Stable identity

In v0.1, a capsule hash is SHA-256 over UTF-8 JSON serialized with sorted object
keys, compact separators, ASCII escapes, and no non-JSON numeric constants.
Array order is preserved. Markdown prose is outside this JSON identity.
Therefore archive both the canonical JSON hash and the whole Markdown file hash.
The program must reference the canonical capsule hash. The runtime checks this
binding; it does not authenticate authorship or validate a task contract.

Hash the semantic pack and runtime source separately in a run record. A capsule
hash alone cannot detect a changed compiler, interpreter, or Python environment.

## No unnecessary novelty

Keep familiar operation names and one serialization initially. Introduce syntax
variants only through an explicit, measured experiment. Do not simultaneously
change syntax, semantics, search budget, examples, and compiler behavior and then
attribute the outcome to a better language.
