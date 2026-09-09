# Capability Registry

**Primary owner:** Forge/registry  
**Consumer:** Daybreak via thin adapters

The registry records reusable engines, not one-off target scripts.

## Registry entry schema

```text
Capability ID:
Name:
Version:
Maturity:
Purpose:
Generic problem class:
Required hooks:
Optional hooks:
Core features:
Input contract:
Output contract:
Determinism:
Checkpoint/resume:
Concurrency model:
Telemetry:
Known limitations:
Crucible suites:
Latest eval:
Adapter ABI compatibility:
Supersedes:
Source/build reference:
```

## Expected mechanism families

Examples of reusable cores include:

- state-space exploration;
- sequence scheduling;
- differential comparison;
- grammar/structured mutation;
- constraint solving;
- graph search;
- concurrency orchestration;
- delta debugging;
- trace reduction;
- corpus management;
- structured parsing;
- protocol framing;
- response clustering;
- experiment prioritization;
- state equivalence / fingerprinting;
- reproducible transport/state stores.

These are mechanism classes, not mandatory implementations.

## Registered capabilities

_None._

## Adapter rule

Daybreak-owned adapters should be as thin as practical. Target knowledge belongs in hooks such as:

- `enumerate_actions`
- `encode_action`
- `normalize_observation`
- `extract_state`
- `interestingness`
- `goal_oracle`

The core should remain reusable outside the current target.
