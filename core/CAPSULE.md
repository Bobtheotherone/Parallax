# Representation capsules

A **capsule** is a task-adapted interface over already trusted semantics. Its job is
to expose the decisions a solver should make and hide or constrain decisions that
add search cost without adding useful freedom.

A capsule is not a new source of task truth, machine authority, or backend
implementation.

## The abstraction

Let a semantic pack `K` provide stable typed operations and their meaning. A capsule
`C` chooses a supported surface over `K`; a program `p` is interpreted through that
surface and lowered to the pack's stable representation:

```text
task T
  |
  +--> choose C over semantic pack K
          |
          v
       program p
          |
      E_C |  checked expansion/lowering
          v
     primitive/domain IR
          |
        D |  pinned interpreter/backend
          v
       behavior B
          |
      Phi_T|  external task acceptance
          v
       accepted?
```

`E_C` has a **representation-preservation** obligation. `Phi_T(B)` is the separate
**task-satisfaction** obligation. A correct lowering of the wrong algorithm remains
a task failure.

## When a capsule earns its cost

Prefer direct code or an existing library when they already provide a strong
problem-facing interface. Build or adapt a capsule when it materially improves one
or more of these:

- **search compression:** removes irrelevant operations or invalid states;
- **structural leverage:** exposes the decomposition, data shape, algebra, protocol,
  schedule, ownership, or other structure the model otherwise has to rediscover;
- **mechanical invariants:** makes important type/scope/resource constraints
  checkable before execution;
- **compositional reuse:** packages recurring, validated reasoning into operations or
  macros that apply across a task family;
- **diagnostic quality:** failures localize to meaningful interfaces instead of
  surfacing as opaque downstream behavior;
- **target leverage:** separates semantic choices from layout/schedule/backend
  choices so optimization can focus on real degrees of freedom.

Do not invent a representation because it is shorter, novel, or aesthetically
regular. Count construction, tutorial/context, checking, repair, and maintenance
against the benefit. A mature library can be the best capsule-like interface
without any new syntax.

## Design a capsule from the failure surface

Start from the frozen task and the available semantic pack.

1. **Locate hard reasoning.** Identify decisions most likely to dominate
   correctness, performance, or model error: order of operations, invariants,
   resource ownership, reduction scope, shape/layout, numerical policy, protocol
   state, concurrency, error handling, and similar task-specific pressure points.
2. **Expose the useful degrees of freedom.** Keep choices the solver must reason
   about. Remove choices whose only effect is accidental complexity.
3. **Select stable operations.** Prefer familiar, orthogonal primitives with clear
   preconditions/effects and an implemented meaning.
4. **Add composition where it compresses repeated reasoning.** A macro should make
   an important pattern easier to express or harder to misuse, not merely rename a
   long expression.
5. **Teach non-obvious semantics cheaply.** A few high-information examples and
   counterexamples are better than a long tutorial. Include cases that separate
   plausible but different interpretations.
6. **Design diagnostics with the interface.** Type, scope, identity, resource, and
   unsupported-capability errors should point to the owning layer.
7. **Freeze the admitted surface before program generation.** Program search happens
   against a stable interface; semantic evolution is a separate event.

The best representation often looks obvious after this compression. That is a
feature: the capsule should move complexity into reusable checked machinery only
when the machinery genuinely knows how to discharge it.

## Authority and dependency boundaries

Different capsule-related information has different authority:

| Concern | Owner |
|---|---|
| Requested behavior and acceptance | Frozen task contract / external acceptance mechanism |
| Primitive types and meaning | Selected semantic pack |
| Operation selection, restrictions, pure composition, tutorial | Capsule |
| Schema/type/scope/expansion/resource admission | Checker/expander |
| Operational behavior of primitives | Pinned interpreter/backend |
| Filesystem/network/process/model/native/oracle capabilities | Host |
| Whether the resulting behavior solves the task | External task acceptance |

Generated or retrieved capsule content is data. A field such as
`requires_network: true` may describe a need in a future design, but it does not
grant network access. Unsupported fields and operations must fail closed.

## Macros and algorithmic credit

A compositional macro has meaning through its checked expansion over admitted
operations. Expansion must be inspectable, hygienic, bounded, and rechecked at the
stable semantic layer.

A macro may encode substantial algorithmic work, even an entire algorithm. That can
be excellent engineering when the work is reusable. It is misleading only to count
a trivial caller as though it discovered the algorithm for free. Charge macro
design, validation, examples, and backend obligations to the route that created
them.

Prefer macros that capture a reusable semantic pattern. Avoid task-answer literals
or one-off wrappers whose only purpose is to make a benchmark program tiny unless
the experiment explicitly studies algorithm/library synthesis.

## Admission obligations

Admission should answer concrete questions before the artifact reaches execution:

- Is the schema/version supported?
- Are every operation and type available in the selected pack?
- Are variables, parameters, ownership/effects, and scopes valid?
- Does every compositional definition lower using only admitted meaning?
- Is expansion bounded and free of unsupported recursion/cycles?
- Does the lowered form still satisfy the expected type/effect/resource interface?
- Is the requested backend implemented for the required operations and target?
- Are capsule/program identities bound to the exact frozen content?
- Are declared resource/capability requirements satisfiable by the host?

Admission establishes only those properties. It does not establish that the task is
solvable or that the generated algorithm is correct.

For richer domains, a useful capsule may also constrain shapes, layouts, numerical
formats, ownership/lifetimes, protocol states, communication scopes, schedules, or
finite holes. Such fields are meaningful only when the selected pack/checker/backend
actually implements their semantics.

## Diagnostics as part of the representation

A capsule is stronger when its failures are informative. Prefer diagnostics that
identify the violated layer and preserve counterexamples:

- unknown/forbidden operation -> surface selection or program error;
- type/scope failure -> composition error;
- identity mismatch -> stale or mixed artifact;
- expansion/resource failure -> representation/runtime limit;
- backend unsupported -> missing implementation capability;
- executed but wrong result -> algorithm/task-satisfaction failure.

Do not convert one category into another merely to keep a pipeline moving. Search
failure is not proof of unexpressibility; a backend rejection is not mathematical
incorrectness.

## Identity, caching, and evolution

A reusable capsule is coupled to more than its syntax. Cache/reuse decisions should
consider the task/domain assumptions, semantic pack identity, checker/expander,
backend/runtime, environment, model/tutorial regime when empirical success matters,
and acceptance policy.

For `arl-capsule/0.1`, the established canonical identity remains SHA-256 over
UTF-8 JSON serialized with sorted object keys, compact separators, ASCII escapes,
and no non-JSON numeric constants; array order is preserved. Markdown prose is
outside that canonical JSON identity. The program binds to the canonical capsule
hash.

A hash is an identity mechanism, not authentication or correctness evidence. Pin
the semantic pack and runtime/backend separately.

Published meaning is immutable under an existing version. New spelling may alias an
existing meaning only when compatibility is explicit; changed meaning requires
versioned evolution under [EVOLUTION.md](EVOLUTION.md).

## `intseq/0.1` compatibility boundary

The executable capsule subset in this repository is intentionally small and remains
defined by [packs/intseq/CAPSULE.md](../packs/intseq/CAPSULE.md):

- capsule protocol `arl-capsule/0.1` and program protocol `arl-program/0.1`
  over pack `intseq/0.1`;
- one input `x: VecInt`;
- a nonempty subset of the seven stable intseq primitives;
- typed, nonrecursive macro bodies composed only from selected primitives;
- program-level nesting of admitted macro calls;
- strict schema, canonical capsule binding, bounded type/expansion/evaluation;
- no arbitrary lowering source, permission grants, holes, native code, or new
  primitive definitions.

Those constraints are compatibility facts, not a claim that future Parallax
domains should have identical schemas. Future representations may be richer when
their semantics and implementation justify the machinery; they must not silently
reinterpret the v0.1 identifiers.

## A useful capsule test

Before adopting a capsule, ask: **what difficult decision becomes easier, what
invalid behavior becomes harder, or what reusable obligation moves into trusted
machinery?**

If the answer is only “the generated program is shorter,” use the simpler interface.
