# Forge Queue

**Owner of need:** Daybreak  
**Builder:** Forge  
**Rule:** describe computational deficiencies, not target-specific offensive outcomes.

## Need schema

```text
Need ID:
Status:
Problem:
Why current capability is insufficient:
Needed generic capability:
Abstract inputs:
Required hooks:
Required outputs:
Performance envelope:
Determinism requirements:
Failure modes to avoid:
Acceptance tests:
Crucible suites:
Compatibility constraints:
Deliverables:
Requested by epoch:
Delivered capability/version:
Eval result:
```

## Queue

_None._

## Good abstraction example

```text
NEED-XXXX

Problem:
A system exposes a large action-sequence space and exhaustive
exploration becomes infeasible at moderate depth.

Needed capability:
A generic stateful sequence explorer supporting approximate
state equivalence and information-gain-guided branch selection.

Required hooks:
- enumerate_actions(state)
- execute(action)
- state_fingerprint(observation)
- score(observation)

Acceptance:
On synthetic hidden-state mazes, recover all rare terminal
states within a bounded fraction of exhaustive exploration cost.

Deliverables:
- library
- stable API/CLI
- property tests
- benchmark
- checkpoint/resume
- deterministic seed support
```

The acceptance test should be strong enough that Forge can improve the engine without knowing why Daybreak needs it.
