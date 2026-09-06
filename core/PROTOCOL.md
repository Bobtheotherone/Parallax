# Bounded synthesis protocol

This is an agent/host protocol. The standalone intseq runtime implements artifact
checking and evaluation, not orchestration or model calls.

## State machine

```text
INTAKE -> CONTRACT_FROZEN -> CAPABILITIES_KNOWN -> MODE_SELECTED
  DIRECT  -> GENERATE -> CHECK_TASK -> RECORD
  CAPSULE -> BUILD -> ADMIT -> FREEZE -> GENERATE -> CHECK_PROGRAM
          -> EXECUTE -> CHECK_TASK -> RECORD
  DESIGN_ONLY -> RECORD_UNIMPLEMENTED_OBLIGATIONS
```

Every transition records its input identities, actual tool call when applicable,
result, and budget consumed. Do not advance on a natural-language claim of success.
`ADMIT` means the available checker accepted the capsule's documented structural
properties. It does not mean the task is solvable or the backend is verified.

## Default experiment budget

Defaults are starting policies, not optimized constants: at most two capsule
candidates, two program attempts per capsule, one approved capsule revision, and
one fixed total wall-time/token/tool budget declared before beginning. Use the
same total budget for baselines. Stop on user cancellation or budget exhaustion.
Change defaults before a measured run, never retrospectively to improve results.

## Diagnostic routing

| Observation | Appropriate action | Invalid inference |
|---|---|---|
| Unknown spelling / arity / type | Repair the program or capsule schema | A new primitive is necessary |
| Capsule hash mismatch | Reload the frozen capsule and rebind explicitly | Ignore the mismatch |
| Typed program fails a task test | Repair algorithm using counterexample | Rewrite the task oracle |
| A lowering is unsupported | Select a supported backend or stop | Ask the LLM to imagine successful compilation |
| Search times out | Record budget exhaustion; optionally compare another route | Prove the language lacks a solution |
| Missing capability is demonstrated | Submit an extension proposal | Increase host privileges inside the capsule |
| Runtime resource rejection | Report limits; revise within approved task/environment | Claim mathematical incorrectness |

## Revision discipline

Language revisions occur between program episodes, not in the middle of a parse
or a test run. Preserve the old capsule, program, diagnostics, and evidence.
Recompute identity and regenerate or explicitly migrate the program. Re-run
checks after any semantic dependency changes.

To assert bounded unexpressibility, use a complete search over a declared finite
space or a domain-specific argument. An LLM's inability to find a solution is
not that argument. Where evidence is insufficient, record `UNKNOWN`.

## Final result

Return `ACCEPTED_UNDER_POLICY`, `REJECTED`, `BUDGET_EXHAUSTED`, or `DESIGN_ONLY`.
Attach a [run record](../templates/RUN.md) with its evidence profile. These are
workflow outcomes, not universal proof labels.
