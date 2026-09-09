# Crucible

Crucible is the synthetic adversarial benchmark factory for generic capability engines.

## Purpose

Forge should be optimized against hard computational structure, not merely “code runs.”

Synthetic systems may contain combinations of:

- hidden state;
- non-commutative action sequences;
- rare transitions;
- delayed effects;
- false-equivalent observations;
- ambiguous identifiers;
- multiple principals as abstract actors;
- state aliasing;
- partial observability;
- concurrency/race-dependent transitions;
- noisy or nondeterministic observations;
- schema/version drift;
- malformed but validly framed inputs;
- resource limits;
- adversarially similar traces.

These properties are generic. They do not require target semantics.

## Suite contract

Every suite records:

- suite ID and version;
- generator version;
- seeds;
- expected invariants;
- hidden ground truth;
- success metrics;
- baseline implementation/results;
- allowed compute budget;
- fixture digest.

## Improvement loop

```text
campaign failure
   -> minimize failure
   -> strip target semantics
   -> add synthetic/generic fixture
   -> reproduce regression
   -> improve capability
   -> run all prior suites
   -> version bump
   -> publish eval
```

## Current suites

_None._
