# Run Queue

**Owner:** Daybreak  
**Execution gate:** Scope Executor

Concrete target-side experiments live here. Generic software requests belong in `02_FORGE/FORGE_QUEUE.md`.

## Run schema

```text
Run ID:
Status:
Hypothesis:
Objective:
Principal:
Destination:
Operation class:
Adapter:
Capability versions:
Estimated requests:
Concurrency:
Destructive:
Human-only:
Scope revision:
Preconditions:
Expected discriminating outcomes:
Stop conditions:
Evidence receipt:
Final disposition:
```

## State transition

```text
DRAFT
  -> SCOPE_PENDING
  -> READY
  -> CLAIMED
  -> IN_FLIGHT
  -> OBSERVED
  -> FINALIZED
```

Exceptional terminals:

`DENIED | CANCELLED | FAILED | STALE`

`CLAIMED` reserves budget before transmission. A durable pending record should exist before the live action begins.

## Queue

_No runs queued._

## Completed recently

_None._

## Scheduling discipline

Prefer runs that maximize decision value per request. Avoid batches whose outcomes would not change the hypothesis ranking.

Every completed run should either:

- update World;
- update/falsify a hypothesis;
- produce a closure;
- expose a capability deficiency;
- or explicitly record that it produced no new information.
