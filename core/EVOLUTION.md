# Evolution: extend capability without erasing meaning

Parallax should evolve quickly where change is cheap and explicitly where change
alters trusted semantics. The representation surface may be temporary; published
meaning and executable artifacts must remain reconstructible for as long as they
matter.

## Extension classes

| Class | What changes | Default authority/risk |
|---|---|---|
| Selection/restriction | Which existing operations or values are exposed | Low; verify the task remains expressible |
| Serialization/tutorial | How existing meaning is presented to a model | Low semantic risk; can strongly change acquisition/search behavior |
| Compositional macro | A typed reusable expression over admitted operations | Medium; expansion must be inspectable and bounded |
| Representation feature | New holes, combinators, effect/type annotations, scheduling choices, etc. over existing semantics | Medium; checker/compiler behavior changes |
| New primitive | New semantic atom not reducible to the current pack | High; expands trusted meaning |
| New backend/lowering | New implementation of existing or new semantics | High; can alter errors, resources, numerics, effects, or security |

The current `intseq/0.1` design supports selection and bounded compositional macros.
Its established mathematical semantics and legacy `arl-capsule/0.1` /
`arl-program/0.1` identifiers remain unchanged unless a future explicit versioned
design says otherwise.

## Prefer composition before new authority

Before adding a primitive or backend, demonstrate the missing capability. Ask:

1. Can direct/native code solve this more cleanly?
2. Does an existing library or primitive already encode the needed behavior?
3. Can a checked composition expose the useful abstraction without new trusted
   semantics?
4. Is the problem actually a bad algorithm, missing context, or backend limitation?
5. Would the proposed extension be reused enough to repay implementation and
   verification cost?

A failed search is not proof of unexpressibility. A new primitive is justified by
an actual semantic or implementation gap, not by model frustration.

## Meaning changes require versions

An externally meaningful identifier owns a contract. Do not keep the identifier
while changing any behavior on which compatible consumers may rely, including:

- values, ordering, state transitions, or side effects;
- error classes/retry semantics;
- numerical relation or determinism guarantees;
- ownership/lifetime/concurrency rules;
- wire/storage format when compatibility depends on it;
- security/capability assumptions;
- resource semantics when those are contractual rather than incidental.

A pure performance improvement can remain compatible when observations stay within
the same contract. A different floating-point reduction order may **not** be purely
performance if the numerical contract makes the difference observable.

For approximate or cross-backend implementations, define a relation `R(old,new)`
rather than assuming byte/value equality. State the assumptions under which `R`
holds and test or prove the properties that matter.

## Compositional extensions

A macro should buy one of three things: repeated reasoning compression, stronger
construction invariants, or a clearer decomposition for search. Its meaning should
be reducible to existing semantics whenever possible.

Use hygienic substitution, explicit input/output types, bounded expansion, and a
post-expansion check. Avoid recursive or mutually recursive macro systems unless a
real use case justifies the termination/resource machinery. Whole-task macros are
allowed as reusable algorithms, but charge their design and validation cost where
it occurred.

## New primitives and backends

These change trusted implementation and deserve engineering depth, not ceremony.
A credible addition specifies:

- signature and semantic observation model;
- errors, effects, ownership/concurrency, numerical behavior, and resource model;
- reference behavior or other independent acceptance path;
- implementation/lowering strategy and dependency direction;
- realistic edge/adversarial cases and compatibility consequences;
- target-specific validation/performance evidence when claimed;
- version/identity and migration story.

Generated artifacts may propose such an extension but cannot authorize or install
it by naming it. Host capabilities remain externally granted.

## Cache and reuse validity

A cached capsule or empirical success estimate is reusable only across dependencies
that preserve the relevant behavior. At minimum consider task domain, pack/version,
checker/compiler, backend/runtime, environment/hardware, model/decoder, tutorial,
and acceptance policy.

Do not invalidate caches merely because prose changed; do invalidate them when a
semantic, implementation, acquisition, or measurement dependency that matters to
the claim changed.

## Retirement

Retirement should remove active complexity without destroying reconstructibility.
Preserve the contract/version, original representation, canonical program/IR when
needed, semantic/runtime identities, migration notes, and the evidence required to
debug or audit important historical artifacts.

For large systems, compatibility is an interface relation over data, state,
effects, errors, ownership, concurrency, and observations—not matching names or
JSON shapes. Retire or replace components along those real boundaries.
