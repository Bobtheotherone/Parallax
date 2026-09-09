# System Contracts

This file defines stable interfaces. Change it rarely and record contract changes in `03_EVIDENCE/DECISIONS.md`.

## Artifact ownership

| Artifact | Primary owner | Mutation model |
|---|---|---|
| `SCOPE.md` | Human/operator | controlled amendment |
| `NOW.md` | Daybreak | replace-in-place current view |
| `WORLD.md` | Daybreak + deterministic materializer | fact updates with evidence |
| `HYPOTHESES.md` | Daybreak | ranked mutable set |
| `RUN_QUEUE.md` | Daybreak | state machine |
| `CAPABILITIES.md` | Forge/registry | versioned append/supersede |
| `FORGE_QUEUE.md` | Daybreak → Forge | state machine |
| `EVALS.md` | Forge + deterministic runner | append results |
| `EVIDENCE.md` | deterministic recorder | append-only |
| `DECISIONS.md` | Daybreak/operator | append-only |
| `LESSONS.md` | Daybreak/Forge | append-only, distilled |
| `ARCHIVE.md` | materializer/operator | append-only index |

## Generic capability ABI

Every reusable capability should conform conceptually to one extension model, even when exact hooks differ.

```yaml
capability:
  id: CAP-<slug>
  version: <semver>

inputs:
  state: opaque
  actions: iterable
  observations: history

hooks:
  enumerate_actions: optional
  encode_action: optional
  execute_action: adapter_owned
  normalize_observation: required
  extract_state: optional
  fingerprint_state: optional
  score_observation: optional
  goal_oracle: optional

core_expectations:
  - deterministic_seed
  - structured_telemetry
  - checkpoint_resume_when_relevant
  - bounded_concurrency
  - traceable_version
  - reproducible_eval

outputs:
  - candidates
  - novel_states
  - minimized_traces
  - statistics
  - machine_readable_receipts
```

The **core** is generic. Target-specific `execute_action`, semantic normalizers, scoring logic, or goal oracles belong in Daybreak-owned adapters.

## Forge request boundary

`FORGE_QUEUE.md` entries describe:

- computational deficiency;
- abstract data model;
- required hooks;
- performance envelope;
- failure modes;
- deterministic acceptance tests;
- synthetic benchmark requirements.

They do not describe a target-specific exploitation objective or ask Forge to conceal the target semantics behind euphemisms.

## Scope-executor contract

Every proposed live run must provide:

```yaml
run_id: RUN-...
principal_id: PRINCIPAL-...
destination_id: DEST-...
operation_class: ...
estimated_requests: ...
concurrency: ...
destructive: false
requires_human_action: false
scope_revision: SCOPE-REV-...
```

The executor returns one of:

- `ALLOW`
- `DENY`
- `REQUIRE_HUMAN`
- `BUDGET_EXHAUSTED`
- `RATE_DEFER`
- `INVALID_REQUEST`

No target request is transmitted before an `ALLOW` decision.

## Evidence contract

Every observation receipt must include:

- stable evidence ID;
- run ID or source-pack ID;
- timestamp;
- actor/principal abstraction;
- capability/adapter versions;
- normalized observation summary;
- raw artifact reference or hash when available;
- confidence class;
- `DOES_NOT_PROVE`;
- contradictions;
- closure or reopen conditions when relevant.

## Derived-state contract

`NOW.md`, `WORLD.md`, and rankings in `HYPOTHESES.md` are materialized views. They may change.

Receipts, source hashes, completed decisions, and archived epoch snapshots are durable history. They are not rewritten to make current strategy look cleaner.

## No-secret contract

Never store raw bearer tokens, cookies, passwords, API keys, presigned URLs, private keys, or private personal identifiers in Markdown. Use typed redactions such as:

`<BEARER sha256:... shape:... expiry:...>`

## Reference contract

Prefer stable IDs over paths. Paths may move; IDs must remain resolvable through indexes.
