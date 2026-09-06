---
id: ADR-0001
status: accepted
date: 2026-09-05
---
# Stable semantics, adaptive surface

## Context and forces

Parallax varies the problem-facing interface. If each variation can also change
primitive meaning, backend behavior, or task semantics, comparisons lose a fixed
object and old artifacts cannot be reconstructed. Conversely, freezing every
surface feature would prevent the adaptation being investigated.

## Alternatives

A self-contained generated language plus compiler offers maximum freedom but
changes the trusted implementation on every attempt. A permanently fixed DSL is
a useful baseline but cannot express the intended representation experiment.
A universal semantic graph would centralize syntax without resolving different
domains' observation models.

## Decision

Adapt operation selection, restrictions, and compositional syntax over a pinned
semantic pack and implementation. Begin with intseq and its fixed primitive tree.
A macro's meaning is its expansion, not a competing prose interpretation. Preserve
published semantic identities and their reconstructible sources. Keep `arl-*`
wire identifiers despite the project rename; no format migration is warranted.

## Consequences and follow-up

Normal generation cannot introduce a primitive to make an inconvenient task pass.
New domains/backends need separate specifications, implementations, tests, and
review under [evolution](../../../core/EVOLUTION.md). Resource-equivalent behavior
is not inferred from mathematical equivalence. Cold construction and warm reuse
costs must be measured separately. Future semantic changes require explicit
versioning, not edits under an old identity.

Source basis: [semantic boundaries](../../../core/SEMANTICS.md),
[capsules](../../../core/CAPSULE.md), and the
[intseq pack](../../../packs/intseq/PACK.md).
