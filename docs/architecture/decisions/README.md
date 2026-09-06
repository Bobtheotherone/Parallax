# Architectural decisions

These ADRs record the few cross-cutting boundaries that materially constrain how Parallax is built. They are not a backlog, process checklist, or substitute for the current [architecture](../ARCHITECTURE.md).

`accepted` means the decision is part of the adopted design. It does **not** mean an implementation has been validated or a research hypothesis has been confirmed.

| Decision | Engineering question it answers | Invariant |
|---|---|---|
| [0001 — Stable semantics, adaptive surface](0001-stable-semantics.md) | What may representation search change? | Solver-facing structure may adapt; published semantic meaning changes only through explicit versioned evolution. |
| [0002 — Generated artifacts are data, not authority](0002-data-not-authority.md) | Where do execution privileges and trusted implementations come from? | The host/reviewed runtime grants capabilities; generated text cannot grant itself new authority. |
| [0003 — Task acceptance is separate from representation checking](0003-independent-task-acceptance.md) | What establishes that a candidate actually solved the task? | Admission/lowering/execution and external task satisfaction remain distinct observations. |

Together they define the main dependency direction:

```text
frozen task + acceptance policy
             |
             v
generated representation/program DATA
             |
             v
checker / lowering over pinned semantics
             |
             v
trusted runtime/backend under host capabilities
             |
             v
external task acceptance
```

A change that preserves this direction usually belongs in ordinary implementation/spec work. A change that reverses an arrow, mutates an externally meaningful semantic identity, grants new privilege, or changes how task success is defined is architectural and should be treated explicitly.

## When an ADR is worth writing

Use an ADR for a durable decision whose alternatives would materially change compatibility, trust boundaries, dependency direction, semantic meaning, or the interpretation of evidence across multiple components. Local module layout, naming, helper choice, and other reversible implementation details belong in code or the relevant spec.

Record the decision when the engineering tradeoff becomes consequential; do not create records merely to prove that a process step happened.

## Evolution

When a future design replaces one of these decisions, preserve the old decision as history and add a superseding ADR with explicit compatibility and migration consequences. Do not silently change a stable protocol meaning under an old identifier. Minor clarifications that do not alter the decision can improve an existing ADR, but historical dates, outcomes, and externally meaningful identifiers remain facts.
