# Decision Log

**Mutation model:** append-only

Record consequential strategy, architecture, scope-interpretation, and capability decisions so future models can distinguish deliberate choices from accidents.

## Decision schema

```text
Decision ID:
Date:
Epoch:
Decision:
Alternatives considered:
Evidence:
Rationale:
Expected consequence:
Revisit if:
Owner:
```

## Decisions

### DEC-0001 — Establish independent CTF control plane

- **Date:** 2026-09-09
- **Epoch:** pre-bootstrap
- **Decision:** Store the CTF Markdown system on the dedicated `CTF` branch as an independent project and keep it separate from Parallax main-project contents.
- **Alternatives considered:** ordinary feature-branch overlay; mixing CTF notes with existing project files.
- **Rationale:** preserve conceptual and retrieval isolation over the full project lifetime.
- **Revisit if:** the CTF project is moved to a dedicated repository.
- **Owner:** operator/initialization agent.
