# Evidence Ledger

**Mutation model:** append-only  
**Authority:** receipts outrank summaries

This Markdown file is the durable index. Large raw traces may live outside GitHub and be referenced by pack ID, digest, or immutable artifact locator.

## Receipt schema

```text
Evidence ID:
Timestamp:
Type: runtime | source | external | derived | closure | contradiction
Source pack / Run ID:
Scope revision:
Principal abstraction:
Capability/adapter versions:
Observation:
Confidence:
Raw artifact reference:
Digest:
Supports:
Contradicts:
Does not prove:
Reopen if:
Sanitization notes:
```

## Evidence classes

- `PROVEN_DIRECTLY`
- `SOURCE_PROVEN`
- `STRONGLY_SUPPORTED`
- `PLAUSIBLE`
- `UNKNOWN`
- `CONTRADICTED`
- `SUPERSEDED`

## Closure record

A closure is evidence about an exact tested proposition, not a universal statement.

```text
Closure ID:
Subject:
Exact tested conditions:
Evidence:
Status:
Does not prove:
Reopen if:
Epoch:
Scope revision:
```

## Contradictions

Do not resolve contradictions by deleting the older record. Link both evidence IDs, state the reconciliation hypothesis, and record the eventual decision.

## Receipts

_None._

## Closures

_None._

## Contradictions

_None._
