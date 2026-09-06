---
id: ADR-0003
status: accepted
date: 2026-09-05
---
# Task acceptance is separate from representation checking

## Context and forces

An admitted program may compute the wrong answer. A capsule, compiler, and test
generator can also agree because they share the same mistake. Requiring full
formal proofs for every early task would prevent a useful bounded prototype;
collapsing all checks into “verified” would overstate what it establishes.

## Alternatives

Types and successful execution alone are cheap but cannot establish arbitrary
intent. Candidate-derived tests can help debug but provide circular task evidence.
An external task contract with scoped acceptance evidence is more work but exposes
the obligations that remain.

## Decision

Freeze task semantics and acceptance policy before representation search. Evaluate
representation preservation and task satisfaction separately, using an oracle or
acceptance procedure specified outside the generated representation. Report
orthogonal evidence fields and exact scopes. Reserve final held-out evaluation
from both synthesizers when claiming a held-out experiment.

## Consequences and follow-up

`EVALUATED` must not imply task acceptance. A well-typed wrong program is an
important regression case, not an embarrassing result to hide. The public
same-author direct-loop oracle provides implementation diversity, not independent
authorship or hidden validation. A host must enforce task bounds and final-test
access; the reference does neither. Statistical tests, formal proofs, native
backend checks, and timing measurements retain separate meanings and identities.

Source basis: [task contracts](../../../core/CONTRACT.md),
[evidence profiles](../../../core/EVIDENCE.md), and the
[typed-but-wrong example](../../../examples/intseq/FAILURE.md).
