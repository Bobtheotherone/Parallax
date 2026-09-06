# Architectural decisions

These ADRs adopt boundaries already present in the source archive. “Accepted”
means the design decision is adopted; it does not claim implementation validation.
The [architecture](../ARCHITECTURE.md) is the current coherent design, not this index.

| Decision | Status | Rationale worth retaining |
|---|---|---|
| [0001 — Stable semantics, adaptive surface](0001-stable-semantics.md) | accepted | Keep representation experiments from changing the meaning being compared |
| [0002 — Generated data has no execution authority](0002-data-not-authority.md) | accepted | Macros must not become self-authorizing semantic or host extensions |
| [0003 — Independent task acceptance obligation](0003-independent-task-acceptance.md) | accepted | Correctly lowering the wrong algorithm must remain a visible failure |

Supersede an ADR with a new decision and cross-links; do not rewrite its historical
reasoning. Minor module/file choices belong in the relevant spec, not a new ADR.
