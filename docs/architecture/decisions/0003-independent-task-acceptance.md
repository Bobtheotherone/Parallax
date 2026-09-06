---
id: ADR-0003
status: accepted
date: 2026-09-05
---
# Task acceptance is separate from representation checking

## Decision in one sentence

Parallax evaluates **whether an artifact is valid in its representation** and **whether its behavior satisfies the task** as separate obligations, with task expectations fixed outside the generated candidate.

## Why this boundary exists

A parser can accept a wrong algorithm. A typechecker can accept a wrong algorithm. A compiler can faithfully lower a wrong algorithm. An interpreter can execute a wrong algorithm without error. If these observations are collapsed into one label such as “verified,” the system rewards internal consistency instead of task success.

The distinction is architectural:

```text
candidate
   |
   v
parse/admit/typecheck -----> representation-valid?
   |
   v
lower/expand --------------> preservation evidence
   |
   v
execute -------------------> runtime observation
   |
   +-----------------------> CheckTask(observation, frozen contract)
                                ^
                                |
                    external acceptance source
```

`CheckRepresentation(candidate, capsule)` and `CheckTask(observation, contract)` answer different questions. Neither substitutes for the other.

## Acceptance source

Task expectations must originate outside the candidate representation and the transformation being judged. Depending on the task, a useful acceptance source may be:

- an independently specified mathematical relation or executable reference;
- contract-derived examples plus properties/invariants;
- a separately implemented oracle;
- differential or metamorphic relations that do not merely replay the candidate computation;
- a proof obligation checked by an appropriate proof checker;
- target measurements for performance requirements;
- a combination of these when no single mechanism covers the contract.

“Independent” has several meanings and they must not be conflated. Different implementation paths reduce common-mode bugs. Independent authorship can reduce shared interpretation errors. Hidden inputs protect an empirical evaluation from direct adaptation. None automatically implies the others.

The current public intseq oracle is a hand-written loop distinct from the AST interpreter, but it shares project authorship and all tests are public. That is implementation diversity, not independent authorship or held-out validation.

## Choose evidence for the property being claimed

Do not demand the same mechanism for every task. Match the instrument to the failure mode:

| Claim | Useful evidence | What it still does not prove |
|---|---|---|
| Artifact obeys schema/types/scope | Parser, checker, static analysis | Correct algorithm |
| Macro/lowering preserves specified behavior | Expansion inspection, equivalence/property checks, proofs where warranted | Task satisfaction |
| Functional behavior matches contract | Independent oracle, properties, differential/metamorphic checks, bounded exhaustive checks | Behavior outside the checked/proved scope |
| Numerical implementation meets tolerance | High-precision/reference relation, adversarial cases, target measurements | Unmodeled numerical regimes |
| Concurrency/state machine is correct | Model/invariant checks, deterministic fault/stress cases, race tooling | All schedules unless coverage/proof establishes it |
| Performance target is met | Measurement on the actual target under a declared protocol | Correctness or portability |
| Security boundary holds | Threat-specific analysis/tests/isolation evidence | Unmodeled threats or untested deployment conditions |

Formal proof is powerful when the property and model justify it; it is not a mandatory ceremony for every prototype. Finite tests are useful when they discriminate plausible bugs; they are not upgraded into universal proof by quantity.

## Development feedback versus final evaluation

Public tests, examples, compiler diagnostics, traces, and counterexamples are development instruments. Feed them back when they help localize and repair the candidate.

A final held-out evaluation is different. Use it only when the experiment claims hold-out generalization, keep it outside candidate read/write capabilities when the host can enforce that separation, and do not repeatedly expose its failures while continuing to call it “final.” If the environment cannot protect a hold-out, report that limitation rather than simulating secrecy with instructions.

The requirement owner may revise the task, but an output-changing revision creates a new contract version. Do not weaken tolerances, delete cases, or reinterpret errors after seeing a candidate and count the result against the old task.

## Diagnostic consequence

Failures should be routed to the layer that owns them:

- schema/type/allowlist failure → repair the artifact or capsule;
- hash/identity failure → reload/rebind the intended frozen dependency;
- preservation/lowering failure → repair checker/expander/backend logic;
- execution/resource failure → diagnose runtime/environment or resource policy;
- structurally valid but wrong result → repair the algorithm;
- acceptance mechanism contradiction → investigate the contract/oracle independently rather than making the candidate pass by fiat.

The [worked intseq failure](../../../examples/intseq/FAILURE.md) is deliberately well typed: filtering after transformation returns `7` for `[-1,0]` while the task requires `5`. The correct response is an algorithm/order repair, not a new primitive or weaker oracle.

## Acceptance policy

A task's acceptance policy should state the properties that are hard gates and the evidence required for them. Performance, cost, elegance, or shorter output cannot compensate for a failed hard correctness or safety condition.

For engineering work, this does not imply exhaustive bookkeeping. Retain enough to reconstruct the claim: exact candidate revision, acceptance source, relevant environment/tool identity, tested or proved scope, and observed result. A test transcript that does not affect any engineering claim need not become permanent ceremony.

## Consequences

This decision adds some implementation and evaluation cost because the system cannot use its own successful execution as proof of success. That cost buys a critical property: Parallax can improve its representations, checkers, and backends without granting those components authority to redefine the problem.

It also enables better debugging. Because admission, preservation, execution, and task acceptance have separate observations, a failure carries localization information instead of collapsing into “the run failed.”

## Related authority

Task freezing and revision are defined in [CONTRACT](../../../core/CONTRACT.md); evidence language in [EVIDENCE](../../../core/EVIDENCE.md); semantic preservation in [SEMANTICS](../../../core/SEMANTICS.md); and experiment custody in the [benchmark protocol](../../benchmarking/PROTOCOL.md).
