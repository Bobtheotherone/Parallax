---
id: ADR-0001
status: accepted
date: 2026-09-05
---
# Stable semantics, adaptive surface

## Decision in one sentence

Parallax may adapt **how a solver sees and composes already-supported meaning**; it must not silently adapt the meaning being computed under the same semantic identity.

## Why this boundary exists

Representation search is useful only if there is a stable object underneath it. If a capsule can change primitive behavior, numerical policy, resource semantics, or task meaning while also changing syntax, then a successful result cannot be attributed to a better representation and old artifacts cannot be reconstructed.

The stable layer does not need to be one universal IR. Different domains may require different observations, effects, numerical relations, ownership rules, or concurrency models. What must be stable is the meaning of the selected pack and implementation for the episode being evaluated.

For a capsule `C`, let `E_C` lower a capsule program to the pack IR and let `S_K` give that IR its observable semantics under pinned semantic environment `K`. Representation adaptation changes `C`; it does not redefine `S_K`:

```text
program --E_C--> stable pack IR --S_K--> observable behavior
```

A representation-preservation claim is therefore about the mapping `E_C`. Task correctness remains a separate obligation against the frozen task contract; see [ADR-0003](0003-independent-task-acceptance.md).

## What may vary inside an episode

A capsule may vary dimensions that reorganize the solver's search space without adding new trusted meaning:

- which existing operations are exposed;
- tighter input/type restrictions that remain compatible with the task;
- transparent typed macros whose meaning is their checked expansion;
- serialization, naming, tutorial, examples, and other acquisition aids;
- future bounded parameters or schedule choices whose legal values and semantics are already defined by the pack/backend.

These are useful when they remove irrelevant choices, expose task structure, or make important invariants mechanically checkable. They are not useful merely because they create a novel DSL.

## What must remain pinned

For a measured or reconstructible episode, pin the semantic dependencies that can change observable behavior:

- task contract and acceptance policy;
- semantic pack/version and, when needed, content identity;
- primitive signatures and meanings;
- numerical, effect, error, and resource policy relevant to the task;
- checker/expander semantics;
- interpreter/backend implementation and target assumptions;
- host-granted capabilities.

A human-readable version string is not a content hash, and a content hash is not a correctness proof. Record the identity appropriate to the compatibility claim.

For `intseq/0.1`, preserve the seven primitive meanings, exact-integer behavior, resource policy, and legacy `arl-capsule/0.1` / `arl-program/0.1` identifiers. The project rename is not a wire-format migration.

## Change classification

Use the smallest class that matches the engineering change:

| Change | Same semantic identity? | Engineering obligation |
|---|---|---|
| Hide an existing primitive | Yes, if the remaining interface is valid for the task | Check expressibility/task coverage |
| Add a pure macro over admitted primitives | Yes for pack meaning; new capsule identity | Typecheck, hygienically expand, recheck, account for construction cost |
| Change tutorial or serialization | Yes for pack meaning | Treat as a representation/acquisition change in experiments |
| Optimize a backend while preserving the declared observation relation | Potentially | Demonstrate conformance for the relevant values, errors, effects, numerical relation, and resources |
| Change a primitive's mathematical behavior, effects, numerical relation, or externally meaningful failure behavior | **No** | Introduce an explicit versioned semantic change |
| Add a primitive or backend capability not already implemented | **No ordinary capsule authority** | Follow a separately reviewed extension/implementation path |
| Change the task or acceptance relation | **No** | Create a new task-contract version; do not score it as the old task |

Mathematical equivalence does not imply resource or floating-point equivalence. Compatibility is defined over the task-relevant observation model, not over function names alone.

## Engineering consequences

**Dependency direction.** Generated surfaces depend on stable semantics; stable semantics do not depend on a generated capsule. Backends implement pack meaning; they do not infer meaning from examples or generated prose.

**Macros are transparent leverage.** A macro may compress a difficult composition, even an entire algorithm, when that is useful. Its meaning must remain inspectable through expansion, and its design cost belongs to the system that created it. A one-token macro call does not make the algorithm free.

**Backend freedom is real but bounded.** A GPU backend may choose vectorization, tiling, reduction strategy, or memory schedule without exposing hardware details in the semantic layer, provided it preserves the declared observations. The [RMSNorm design case](../../../packs/gpu/RMSNORM.md) illustrates why semantic reduction scope must remain explicit while schedule is allowed to vary.

**Search failure is not a semantic license.** If the current interface is awkward, first try another composition or a direct/existing-library route. A missing primitive is an extension finding, not permission to reinterpret an existing one.

**Version when meaning changes.** Preserve old identities and their reconstructible sources. Do not silently edit a published meaning under the old identifier to simplify implementation or make a benchmark pass.

## Alternatives rejected

A self-contained generated language plus generated compiler maximizes freedom but mutates the trusted implementation on every attempt. A permanently fixed DSL is a valuable baseline but cannot test representation adaptation. A universal graph container can unify mechanics without defining every domain's observations. Parallax therefore keeps semantic packs plural and stable while allowing temporary solver-facing interfaces above them.

## Related authority

The detailed semantic obligations live in [SEMANTICS](../../../core/SEMANTICS.md), capsule behavior in [CAPSULE](../../../core/CAPSULE.md), versioned extensions in [EVOLUTION](../../../core/EVOLUTION.md), and the current executable example in the [intseq pack](../../../packs/intseq/PACK.md). This ADR records the architectural reason those responsibilities are separated.
