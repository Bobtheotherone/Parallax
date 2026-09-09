# IDs and Status Vocabulary

Stable IDs make the Markdown network resilient to file moves and compaction.

## ID namespaces

| Object | Format | Example |
|---|---|---|
| scope revision | `SCOPE-REV-NNNN` | `SCOPE-REV-0001` |
| strategy epoch | `EPOCH-YYYYMMDD-NNN` | `EPOCH-20260909-001` |
| evidence receipt | `EVID-NNNNNN` | `EVID-000001` |
| hypothesis | `HYP-NNNN` | `HYP-0001` |
| run | `RUN-YYYYMMDD-NNNN` | `RUN-20260909-0001` |
| forge need | `NEED-NNNN` | `NEED-0001` |
| capability | `CAP-<slug>` | `CAP-sequence-explorer` |
| evaluation | `EVAL-NNNNN` | `EVAL-00001` |
| source pack | `PACK-NNNN` | `PACK-0001` |
| decision | `DEC-NNNN` | `DEC-0001` |
| lesson | `LESSON-NNNN` | `LESSON-0001` |
| closure | `CLOSE-NNNN` | `CLOSE-0001` |

Never reuse an ID.

## Evidence confidence classes

Use the strongest class actually supported.

- `PROVEN_DIRECTLY` — observed in a controlled, attributable run.
- `SOURCE_PROVEN` — explicit static/public/source contract.
- `STRONGLY_SUPPORTED` — inference with multiple independent supports.
- `PLAUSIBLE` — useful hypothesis-level inference, not world truth.
- `UNKNOWN` — unresolved.
- `CONTRADICTED` — evidence conflicts; requires reconciliation.
- `SUPERSEDED` — replaced by better evidence while preserving history.

## Hypothesis status

- `ACTIVE`
- `WATCH`
- `BLOCKED`
- `FALSIFIED`
- `SUPPORTED`
- `CLOSED`
- `SUPERSEDED`

## Run status

- `DRAFT`
- `SCOPE_PENDING`
- `READY`
- `CLAIMED`
- `IN_FLIGHT`
- `OBSERVED`
- `FINALIZED`
- `DENIED`
- `CANCELLED`
- `FAILED`
- `STALE`

A run must not skip directly from `DRAFT` to `IN_FLIGHT`.

## Forge need status

- `OPEN`
- `SPEC_READY`
- `BUILDING`
- `EVALUATING`
- `DELIVERED`
- `REJECTED`
- `BLOCKED`
- `SUPERSEDED`

## Capability maturity

- `EXPERIMENTAL`
- `QUALIFIED`
- `STABLE`
- `DEPRECATED`
- `RETIRED`

## Closure semantics

A closure is always bounded. It must state:

- exact subject/tuple;
- evidence supporting closure;
- `DOES_NOT_PROVE`;
- `REOPEN_IF`;
- epoch and scope revision.

“Closed” never means “globally impossible.”
