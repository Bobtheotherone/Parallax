# Changelog

This file records repository history, not roadmap intent or validation claims.
Historical failures remain historical even when later work resolves them.

## 2026-09-05 — Parallax repository bootstrap and publication

The initial Parallax repository was established and the adaptive-representations
source corpus was migrated into a routed research/engineering layout. The bootstrap:

- preserved the source archive, stable `intseq/0.1` meaning, legacy
  `arl-capsule/0.1` / `arl-program/0.1` wire identifiers, canonical example
  identities, and the embedded Python reference source;
- added project intent, architecture and ADRs, development/verification guidance,
  a benchmark protocol, provenance mapping, documentation-integrity tooling, and
  the implementation-ready `SPEC-001` extraction contract;
- separated repository-development work from representation-synthesis experiments
  and kept task acceptance distinct from artifact checking/execution.

The bootstrap itself did **not** add a packaged runtime, orchestration host,
native/GPU backend, held-out benchmark, LLM comparison, performance result, or
formal proof. The source-author intseq run report remained imported historical
evidence rather than a fresh reproduction.

During the earlier local preparation recorded in
[BOOTSTRAP-AUDIT.md](docs/provenance/BOOTSTRAP-AUDIT.md), GitHub integration writes
returned 403 and no remote branch existed. That is a preserved fact about that
attempt, not the final repository state. The prepared bootstrap was subsequently
published and merged as PR #1 at commit
`ac221712d46a13162c420f6d393f15a832960e09`.

Later on the same local date, contributor, security, and terminology guides were
added and merged as PR #2 at commit
`00c3821b4b812a7e61e24968053059c7adabea30`. Those guides were derived project
documentation and did not change the frozen semantic/provenance artifacts.

## Source history — 0.1, dated 2026-09-05

The preserved source archive's 0.1 release note describes the original Markdown
starter: task/contract/capsule/evidence separation, a bounded agent protocol,
selective context routes, the exact-integer intseq reference/example, a GPU
reduction-scope design critique, and a matched-budget research plan.

That note is imported source history, not a later Parallax release. The original
bytes remain in
[adaptive-representations-source.zip](docs/provenance/adaptive-representations-source.zip),
with migration identities and dispositions in
[SOURCE-MAP.md](docs/provenance/SOURCE-MAP.md).
