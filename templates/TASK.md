# Task contract template

Freeze **what makes a result correct** before choosing an implementation or
representation. Keep this record about external behavior and consequential
constraints; do not turn it into a project-management form. The current intseq
runtime does not parse this general record.

```json
{
  "task_id": "REPLACE",
  "contract_version": "REPLACE",
  "requirement_owner": "REPLACE",
  "requirement_source": "REPLACE",
  "intent": "REPLACE",
  "input_domain": "REPLACE",
  "output_relation": "REPLACE",
  "observable_effects": [],
  "error_behavior": "REPLACE",
  "numerical_policy": "REPLACE",
  "target_environment": "REPLACE",
  "hard_constraints": [],
  "optimization_goal_after_acceptance": "REPLACE",
  "acceptance_policy": "REPLACE",
  "oracle_source_and_review": "REPLACE",
  "public_examples": [],
  "unresolved_assumptions": [],
  "total_budget": "REPLACE",
  "mode": "DIRECT | CAPSULE | DESIGN_ONLY",
  "frozen": false
}
```

## Fill the fields as engineering constraints

`input_domain` should include shape, scale, validity, and important distributional
facts when they alter the algorithm or resource behavior. `output_relation` should
state the required relation or state transition, not a preferred implementation.
Use `observable_effects` for externally visible I/O, mutation, ordering, ownership,
or concurrency behavior; use an empty list only when there are truly no effects.

`error_behavior` should distinguish invalid input, unsupported capability, partial
failure, retry/idempotence, and cancellation when those are observable.
`numerical_policy` should state exactness or precision/tolerance, determinism,
rounding/reduction requirements, and special-value behavior where relevant.
`target_environment` and `hard_constraints` carry real platform, compatibility,
security, memory, latency, throughput, I/O, device, or other non-negotiable limits.

`optimization_goal_after_acceptance` is meaningful only with a workload and a way
to compare candidates. Correctness and prohibited behavior remain gates rather
than terms in a weighted score. `acceptance_policy` names the evidence required for
this task; `oracle_source_and_review` states where expected behavior comes from and
its independence or known limitations. Public examples should discriminate
semantics or boundaries, not substitute for the whole contract.

## Freeze test

Before setting `frozen: true`, ask whether two competent implementations could
produce observably different results because the contract is ambiguous. Resolve
uncertainty that can change outputs, effects, errors, numerical behavior, safety,
compatibility, or an irreversible architectural choice.

Do not block on local, reversible engineering choices—helper layout, internal
naming, equivalent data structures, or another choice whose consequences remain
inside the frozen behavior. Pick a sensible default and proceed. Record a remaining
assumption only when learning its true value could force a materially different
solution.
