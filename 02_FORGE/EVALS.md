# Capability Evaluations

**Owners:** Forge + deterministic runner

Evaluations are generic, reproducible, and versioned. They do not use production targets as hidden benchmarks.

## Eval record

```text
Eval ID:
Capability:
Version:
Commit/build:
Suite:
Seed set:
Environment:
Dataset/fixture digest:
Baseline:
Metrics:
Result:
Regressions:
Artifacts:
Decision:
```

## Minimum evaluation dimensions

As applicable:

- correctness/invariants;
- determinism;
- state coverage;
- rare-event discovery;
- false-equivalence rate;
- minimization quality;
- throughput;
- memory use;
- checkpoint fidelity;
- concurrency correctness;
- parser robustness;
- malformed-input behavior;
- telemetry completeness;
- adapter compatibility.

## Regression rule

A capability version is not `STABLE` if it improves one benchmark while silently regressing a previously accepted fixture.

## Results

_No evaluations recorded._
