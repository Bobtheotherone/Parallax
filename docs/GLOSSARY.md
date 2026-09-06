# Parallax glossary

This is a **derived navigation aid**, not a new semantic specification. Parallax
intentionally keeps authority distributed by concern; when a short definition here
is insufficient, follow the linked owning document. The complete authority map is
in [ARCHITECTURE.md](architecture/ARCHITECTURE.md#source-of-truth-map).

## Core terms

| Term | Working meaning | Authority / detail |
|---|---|---|
| **Task contract** | The frozen statement of intended inputs, outputs/relations, effects, errors, numerical policy, prohibited behavior, and acceptance method. Representation search does not get to redefine it. | [CONTRACT.md](../core/CONTRACT.md) |
| **Requirement owner** | The authority allowed to approve a task-semantic revision. An implementation or generated artifact cannot silently assume this role. | [CONTRACT.md](../core/CONTRACT.md) |
| **Acceptance oracle / mechanism** | An externally fixed source of expected task observations used to decide whether an artifact satisfies the task. It is distinct from parsing, typechecking, lowering, or execution. | [CONTRACT.md](../core/CONTRACT.md), [EVIDENCE.md](../core/EVIDENCE.md) |
| **Semantic pack** | A stable, domain-specific set of operation IDs, types, behavior, and relevant resource/numerical policy. A pack is not a universal IR. | [SEMANTICS.md](../core/SEMANTICS.md); current example: [intseq/0.1](../packs/intseq/PACK.md) |
| **Primitive** | An operation whose meaning belongs to the selected semantic pack and whose implementation belongs to the trusted runtime/backend. Generated content cannot create a new primitive merely by naming one. | [EVOLUTION.md](../core/EVOLUTION.md), [intseq pack](../packs/intseq/PACK.md) |
| **Capsule** | A temporary task-adapted interface to an existing semantic pack: typically a selected operation subset plus checked compositional macros and related metadata. It does not by itself grant execution authority. | [CAPSULE.md](../core/CAPSULE.md) |
| **Macro** | A typed compositional expression over admitted operations. In the current intseq subset, its mathematical meaning is its hygienic expansion to permitted primitives. | [CAPSULE.md](../core/CAPSULE.md), [intseq format](../packs/intseq/CAPSULE.md) |
| **Program** | A generated or authored data artifact expressed against a frozen capsule and bound to its identity. Passing program checks is not the same as satisfying the task. | [intseq format](../packs/intseq/CAPSULE.md), [CONTRACT.md](../core/CONTRACT.md) |
| **Admission / checking** | Structural, schema, allowlist, signature, scope, identity, type, and documented resource checks performed before/around evaluation. `ADMIT` does not mean “correct solution.” | [PROTOCOL.md](../core/PROTOCOL.md) |
| **Expansion / lowering** | The checked mapping from capsule-level expressions/macros to the stable primitive representation used by the interpreter/backend. | [SEMANTICS.md](../core/SEMANTICS.md), [CAPSULE.md](../core/CAPSULE.md) |
| **Primitive IR** | The stable operation tree after supported macro expansion for the current intseq design. It is not claimed to be a native compiler IR or a universal cross-domain representation. | [ARCHITECTURE.md](architecture/ARCHITECTURE.md), [intseq pack](../packs/intseq/PACK.md) |
| **Representation preservation** | The obligation that expansion/lowering preserves the capsule-specified behavior under stated assumptions. | [SEMANTICS.md](../core/SEMANTICS.md) |
| **Task satisfaction** | The separate obligation that the resulting behavior satisfies the frozen external task contract. A correctly lowered wrong algorithm still fails here. | [SEMANTICS.md](../core/SEMANTICS.md), [CONTRACT.md](../core/CONTRACT.md) |
| **Host** | The trusted external integration layer that selects pinned capabilities/backends, routes context, enforces budgets and task-domain policy, controls oracle access, and retains evidence. The full host is not currently implemented. | [HOST.md](../runtime/HOST.md), [ARCHITECTURE.md](architecture/ARCHITECTURE.md) |
| **Interpreter / backend** | Trusted implementation that gives operational behavior to admitted primitive IR under a pinned resource/numerical policy. It does not own task intent. | [ARCHITECTURE.md](architecture/ARCHITECTURE.md) |
| **Evidence profile** | Orthogonal records of what was actually checked—parsing, type/admission, expansion, execution, tests, proofs, backend validation, performance, etc.—with scope and identity. It is not one generic confidence score. | [EVIDENCE.md](../core/EVIDENCE.md), [VERIFICATION.md](development/VERIFICATION.md) |
| **Frozen identity** | A recorded content/semantic dependency identity used to reconstruct an episode. A hash can bind bytes but is not a correctness proof or an authorship signature. | [CAPSULE.md](../core/CAPSULE.md), [EVIDENCE.md](../core/EVIDENCE.md) |
| **Resource policy** | Limits applied by the pack/runtime/host to admitted artifacts or execution, such as depth, nodes, integer size, vector length, or work. Rejection under a resource policy is not mathematical incorrectness. | [intseq pack](../packs/intseq/PACK.md), [PROTOCOL.md](../core/PROTOCOL.md) |
| **Budget** | The predeclared total allowance for retrieval, design, generation, repairs, tools, verification, compute, time, or money in an attempt/experiment. It is broader than evaluator resource limits. | [ECONOMICS.md](../core/ECONOMICS.md), [PROTOCOL.md](../core/PROTOCOL.md) |

## Modes and terminal outcomes

**`DIRECT`** solves the frozen task without first synthesizing a capsule. It is the
preferred route when adaptation does not justify its added cost.

**`CAPSULE`** constructs/adopts a bounded representation, freezes it, generates a
program against it, checks/executes that program, and then performs separate task
acceptance.

**`DESIGN_ONLY`** records unresolved obligations without pretending an executable
solution exists. It is appropriate when required semantics, permissions, or
capabilities are unavailable or unsafe to assume.

The protocol's terminal outcomes—`ACCEPTED_UNDER_POLICY`, `REJECTED`,
`BUDGET_EXHAUSTED`, and `DESIGN_ONLY`—describe an episode under a declared policy;
they are not universal proof labels. See [PROTOCOL.md](../core/PROTOCOL.md).

## Terms that should not be collapsed

- **Identity is not correctness.** Matching a hash establishes content identity
  under a recipe, not semantic validity, provenance/authorship, or task success.
- **Typechecked is not task-correct.** A well-typed program may implement the wrong
  algorithm.
- **Executed is not accepted.** Producing a result is distinct from an external
  task oracle accepting it.
- **Finite tests are not proof.** State the exact tested scope and oracle.
- **A capsule is not a sandbox.** Data-only syntax narrows generated authority, but
  operating-system isolation and capability enforcement belong to the host.
- **A tutorial is not semantics.** Examples and tutorials aid acquisition; the pack
  and owning contracts define meaning.
- **A roadmap item is not an implemented capability.** Capability claims require
  current implementation evidence.

When uncertain which document owns a term or claim, start from the
[architecture source-of-truth map](architecture/ARCHITECTURE.md#source-of-truth-map)
rather than choosing whichever definition was read most recently.
