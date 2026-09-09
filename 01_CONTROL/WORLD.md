# World

**Owner:** Daybreak + deterministic materializer  
**Purpose:** neutral factual model only  
**World revision:** `WORLD-REV-0000`

Do not put attack ranking or “what to try next” in this file.

## Fact schema

Each fact should have:

```text
ID:
Class:
Statement:
Confidence:
Evidence:
Valid since:
Supersedes:
Contradictions:
Does not prove:
```

## Health

- evidence index health: unknown
- unresolved contradictions: 0
- source-pack registry health: unknown
- stale materialized views: unknown

## Facts

_No campaign facts initialized._

## Entities and identities

_None initialized._

## Protocol / resource model

_None initialized._

## Capabilities observed in the environment

_None initialized._

## Constraints and invariants

_None initialized._

## State transitions

_None initialized._

## Unknowns that belong in world reconstruction

_None initialized._

## Projection rules

- A hypothesis is not promoted to World without evidence.
- Similar names are not equivalence proof.
- Client-side removal does not prove server-side removal.
- A successful operation does not establish broader authorization than the exact observed tuple.
- A failed operation does not establish global impossibility.
- Identity claims must preserve necessary namespace/parent/principal context.
- Generated summaries yield to receipts when they conflict.
