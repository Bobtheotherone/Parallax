# Run record: evidence needed for the next decision

A run record is a compact reconstruction of consequential facts, not a transcript.
Record an item when it affects reproducibility, diagnosis, acceptance, cost, or a
comparative claim. Aggregate routine tool chatter. Never replace an unexecuted
measurement with a prediction.

```json
{
  "run_id": "REPLACE",
  "snapshot": {
    "task_contract": "PIN",
    "capsule": "PIN_OR_NOT_APPLICABLE",
    "program_or_candidate": "PIN_OR_NOT_APPLICABLE",
    "pack_runtime_backend": "PIN_RELEVANT_IDENTITIES",
    "environment": "RECORD_RELEVANT_ACTUALS"
  },
  "method": {
    "mode": "DIRECT | CAPSULE | DESIGN_ONLY",
    "model_decoder": "ACTUAL_OR_NO_MODEL_CALL",
    "context_and_capabilities": "IDENTITIES_OR_COMPACT_DESCRIPTION",
    "budget": "DECLARED_LIMITS_AND_ENFORCEMENT"
  },
  "attempts": [],
  "evidence": [],
  "terminal": {
    "outcome": "ACCEPTED_UNDER_POLICY | REJECTED | BUDGET_EXHAUSTED | DESIGN_ONLY | NOT_FINISHED",
    "acceptance_policy": "PIN_OR_DESCRIBE",
    "remaining_obligations": []
  }
}
```

## Attempt entries

Add an attempt only when it produced a candidate, changed the diagnosis, or consumed
material budget. A useful shape is:

```json
{
  "candidate": "IDENTITY_OR_DESCRIPTION",
  "question": "WHAT UNCERTAINTY THIS ATTEMPT/TOOL WAS MEANT TO RESOLVE",
  "action": "MODEL/COMPILER/TEST/PROFILE/REVIEW COMMAND OR METHOD",
  "result": "ACTUAL STATUS AND DECISIVE OBSERVATION",
  "cost": "TOKENS/TIME/COMPUTE/MONEY WHEN MATERIAL"
}
```

Preserve failed candidates when they explain the final choice or are part of a
measured comparison. Do not create one record per trivial shell command.

## Evidence entries

Evidence is a list because different tasks require different instruments. Each
entry should state the property, status, scope, method/source, and artifact identity:

```json
{
  "property": "EXAMPLE: task behavior on bounded domain",
  "status": "PASS | FAIL | NOT_RUN | NOT_APPLICABLE",
  "scope": "EXACT CASES/DOMAIN/TARGET/ASSUMPTIONS",
  "method": "TOOL, ORACLE, PROOF CHECKER, REVIEW, OR MEASUREMENT",
  "artifact": "IDENTITY OR LOG/RESULT LOCATION"
}
```

Keep representation admission, execution, task acceptance, backend validation, and
performance as separate properties when they are relevant. A hash is identity, not
an evidence entry saying the behavior is correct.

## Additional fields for comparisons

For a development or representation benchmark, add only fields needed to interpret
the comparison: arm/treatment, task family/split, model/provider version, seed/order,
matched budget dimensions, cold-versus-warm reuse, stopping/retry policy, oracle
custody, preregistered metrics/exclusions, and aggregate usage including failures.

Private final-oracle inputs stay in operator-controlled storage; record their durable
identity/custodian rather than copying secrets into this file. A public development
pilot must not be relabeled as held-out evidence.
