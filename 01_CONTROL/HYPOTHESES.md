# Hypotheses

**Owner:** Daybreak  
**Strategy epoch:** `EPOCH-UNSET`

Only active/recent strategic hypotheses belong here. Archive stale epochs rather than growing this file indefinitely.

## Ranking heuristic

Use disciplined estimates rather than false precision:

```text
priority ≈
    estimated_goal_probability
  × expected_information_gain
  × evidence_quality
  × capability_reuse
  --------------------------------
    execution_cost
  × uncertainty_penalty
```

A technically interesting path is not automatically a high-priority path.

## Required fields

```text
ID:
Status:
Claim:
Why plausible:
Supporting evidence:
Contradicting evidence:
Key unknown:
Discriminating observation:
Required capability:
Estimated request cost:
Expected information gain:
Goal relevance:
Stop condition:
Reopen condition:
Last updated:
```

## Active

_None._

## Watch

_None._

## Recently falsified / closed

_None._

## Strategy discipline

Daybreak should continually ask:

- What do we currently believe?
- What observation would most change the ranking?
- What is the shortest plausible path to the objective?
- Which branch is consuming requests without changing belief?
- What generic capability would materially improve the search?
- What should be abandoned now?
