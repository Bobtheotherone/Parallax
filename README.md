# CTF Capability Foundry Control Plane

> **Repository isolation:** this branch is an independent project stored inside the Parallax repository only for durable GitHub storage. It is not a Parallax feature branch and must not be merged into `main`.

## Mission

This Markdown network is the durable control plane for a long-running, authorized CTF/security-research campaign in which:

- **Forge** manufactures reusable, target-agnostic capability engines.
- **Daybreak** is the persistent campaign brain: it owns target semantics, hypotheses, adapter logic, experiment selection, and objective pursuit.
- **Workers** are disposable artifact producers.
- **Scope Executor** deterministically enforces competition boundaries before any target-side action.
- **Evidence** is authoritative; conversation is not.
- **Failures** are converted into permanent generic regression tests so capability quality compounds over time.

The framework is intentionally independent of any one handoff ZIP, target generation, model version, current blocker, or competition phase. Current state lives in small mutable views; durable history lives in append-only ledgers and archived epochs.

## Non-negotiable invariants

1. **Capability and compliance are orthogonal.** The reasoning layer is not weakened by repeated caution prose. Scope is enforced mechanically by the executor.
2. **Forge receives computational deficiencies, not target-specific offensive instructions.**
3. **Daybreak remains the single strategic owner.** Workers do not form competing campaign brains.
4. **Facts and hypotheses never share the same status.**
5. **Evidence references are stable IDs, not ephemeral chat links or absolute local paths.**
6. **Every live action has a scope decision, run ID, observation receipt, and final disposition.**
7. **Current-state files stay small.** History is archived, not accumulated into `NOW.md`.
8. **No silent deletion.** Superseded, falsified, closed, and failed artifacts remain traceable.
9. **No raw secrets in Markdown.** Store typed redactions, hashes, shapes, expiry classes, and provenance instead.
10. **The CTF branch is its own project.** Do not open a merge PR from `CTF` into Parallax `main`.

## Read order

1. `00_SYSTEM/OPERATING_MODEL.md`
2. `00_SYSTEM/CONTRACTS.md`
3. `01_CONTROL/SCOPE.md`
4. `01_CONTROL/NOW.md`
5. `01_CONTROL/WORLD.md`
6. `01_CONTROL/HYPOTHESES.md`
7. `02_FORGE/CAPABILITIES.md`
8. `02_FORGE/FORGE_QUEUE.md`
9. `01_CONTROL/RUN_QUEUE.md`
10. `03_EVIDENCE/EVIDENCE.md`

For a cold handoff, also read `00_SYSTEM/LIFECYCLE.md` and `templates/EPOCH_HANDOFF.md`.

## Directory map

| Plane | Purpose |
|---|---|
| `00_SYSTEM/` | Stable architecture, lifecycle, IDs, ingestion, contracts |
| `01_CONTROL/` | Small current campaign state and target-side work queue |
| `02_FORGE/` | Generic capability registry, build queue, evals, Crucible |
| `03_EVIDENCE/` | Append-only evidence, decisions, source packs, distilled lessons |
| `04_ARCHIVE/` | Index of retired epochs and compacted artifacts |
| `templates/` | Canonical record shapes used by agents |

## Canonicality

GitHub on branch `CTF` is canonical for this Markdown control plane. Large knowledge archives, raw source corpora, traces, binaries, and generated databases may live elsewhere; this framework refers to them by stable source-pack and evidence IDs.

Markdown is the human/LLM coordination layer, not the raw evidence warehouse.
