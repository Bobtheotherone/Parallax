# Parallax glossary

This is a compact navigation aid. Owning documents define the precise behavior;
when a term is consequential, follow its link. The complete authority map is in
[ARCHITECTURE.md](architecture/ARCHITECTURE.md#source-of-truth-map).

## Task and acceptance

| Term | Working meaning | Authority |
|---|---|---|
| **Task contract** | Minimum sufficient definition of valid inputs/state, required observations, effects/errors/numerics, environment, constraints, and acceptance. | [CONTRACT](../core/CONTRACT.md) |
| **Hard invariant** | A fact a correct implementation cannot violate without changing the task, compatibility, safety, or trusted semantics. | [CONTRACT](../core/CONTRACT.md) |
| **Acceptance mechanism / oracle** | External procedure or source of expected observations used to decide task satisfaction. It is separate from parsing, typechecking, execution, or the candidate's own graph. | [CONTRACT](../core/CONTRACT.md), [EVIDENCE](../core/EVIDENCE.md) |
| **Task satisfaction** | The obligation that the candidate's externally observable behavior satisfies the frozen task policy. | [SEMANTICS](../core/SEMANTICS.md) |
| **Failure surface** | Realistic classes of semantic, integration, numerical, concurrency, resource, compatibility, or operational failure the design must consider. | [CONTRACT](../core/CONTRACT.md), [PROTOCOL](../core/PROTOCOL.md) |

## Representation and semantics

| Term | Working meaning | Authority |
|---|---|---|
| **Semantic pack** | Stable domain operations/types plus the observation, error, numerical, resource, and effect rules needed to give them meaning. | [SEMANTICS](../core/SEMANTICS.md); current [intseq pack](../packs/intseq/PACK.md) |
| **Primitive** | Semantic operation owned by a pack and implemented by trusted runtime/backend code. Generated content cannot create one merely by naming it. | [EVOLUTION](../core/EVOLUTION.md) |
| **Capsule** | Temporary task/model-facing interface over existing semantics: typically selected operations, restrictions, and checked compositions. It is data, not a privilege grant. | [CAPSULE](../core/CAPSULE.md) |
| **Macro** | Typed compositional abstraction whose current intseq meaning is its hygienic expansion into admitted primitives. | [CAPSULE](../core/CAPSULE.md), [intseq format](../packs/intseq/CAPSULE.md) |
| **Program** | Candidate data artifact expressed against a frozen capsule/interface and bound to its identity where the protocol requires it. | [intseq format](../packs/intseq/CAPSULE.md) |
| **Primitive IR** | Pack-level representation after supported expansion/lowering. It is stable enough for a backend, not claimed to be a universal compiler IR. | [SEMANTICS](../core/SEMANTICS.md) |
| **Representation preservation** | Obligation that expansion/lowering keeps observations within the pack's stated semantic relation. | [SEMANTICS](../core/SEMANTICS.md) |
| **Semantic relation** | Relation `R(source,target,assumptions)` defining acceptable equivalence when exact equality is inappropriate, e.g. floating-point or concurrent traces. | [SEMANTICS](../core/SEMANTICS.md) |
| **Representation leverage** | Reduction in search/engineering difficulty obtained by exposing the right structure, constraints, or reusable machinery—not by mere renaming. | [ECONOMICS](../core/ECONOMICS.md) |
| **Semantic dependency footprint** | Set of pack/runtime/backend/interface assumptions on which a candidate or empirical result depends. | [ECONOMICS](../core/ECONOMICS.md), [EVOLUTION](../core/EVOLUTION.md) |

## Runtime and authority

| Term | Working meaning | Authority |
|---|---|---|
| **Admission/checking** | Schema, allowlist, identity, scope, type, and bounded expansion checks. Admission says the artifact is meaningful/permitted, not task-correct. | [PROTOCOL](../core/PROTOCOL.md) |
| **Lowering / expansion** | Mapping from a higher-level representation to pack/backend-level form under a preservation obligation. | [SEMANTICS](../core/SEMANTICS.md) |
| **Backend / interpreter** | Trusted implementation that executes admitted semantics under a pinned numerical/resource policy. | [ARCHITECTURE](architecture/ARCHITECTURE.md) |
| **Host** | Trusted coordinator for context, tool/capability grants, pinned dependencies, budgets, execution, oracle custody, and retained evidence. The full host is not currently implemented. | [HOST](../runtime/HOST.md), [ARCHITECTURE](architecture/ARCHITECTURE.md) |
| **Capability** | Externally granted ability to perform an effect or use a tool/backend. A generated artifact may request or describe one but cannot self-grant it. | [HOST](../runtime/HOST.md), [EVOLUTION](../core/EVOLUTION.md) |
| **Resource policy** | Runtime/host limits such as depth, work, memory, vector size, process time, or tool budget. Resource rejection is not automatically task incorrectness. | [SEMANTICS](../core/SEMANTICS.md) |
| **Frozen identity** | Content/semantic dependency identity used to bind an episode or reconstruct an artifact. Identity is not correctness or authorship proof. | [CAPSULE](../core/CAPSULE.md), [EVIDENCE](../core/EVIDENCE.md) |

## Engineering and evidence

| Term | Working meaning | Authority |
|---|---|---|
| **Discriminating experiment** | Smallest reliable tool/check that produces different expected observations for competing failure hypotheses. | [PROTOCOL](../core/PROTOCOL.md), [EVIDENCE](../core/EVIDENCE.md) |
| **Counterexample** | Concrete input/state/trace that falsifies a candidate assumption or required property and helps localize the failure. | [EVIDENCE](../core/EVIDENCE.md) |
| **Evidence profile** | Claim-scoped record of what actually ran/was reviewed, on which artifacts and scope; not a universal confidence score. | [EVIDENCE](../core/EVIDENCE.md) |
| **Cold cost** | One-time cost to build/admit a pack, backend, representation, tutorial, or other reusable machinery. | [ECONOMICS](../core/ECONOMICS.md) |
| **Warm cost** | Cost of applying already-built machinery to a new task/attempt under compatible dependencies. | [ECONOMICS](../core/ECONOMICS.md) |
| **Recoverability** | Ability to localize a failure, retain useful diagnostics, repair the root cause, and re-evaluate without restarting blindly. | [PROTOCOL](../core/PROTOCOL.md) |

## Modes and outcomes

**`DIRECT`** uses the native language/tooling without synthesizing a capsule.
**`CAPSULE`** solves through a frozen task-adapted interface over supported
semantics. **`DESIGN_ONLY`** records a technically meaningful design when required
semantics, capability, or authority is unavailable for honest execution.

Compatible terminal outcomes are `ACCEPTED_UNDER_POLICY`, `REJECTED`,
`BUDGET_EXHAUSTED`, and `DESIGN_ONLY`; see [PROTOCOL](../core/PROTOCOL.md).

Keep these distinctions sharp: identity is not correctness; typechecked is not
task-correct; executed is not accepted; finite tests are not proof; a capsule is
not a sandbox; a tutorial is not semantics; a roadmap item is not an implemented
capability.
