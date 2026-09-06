# Changelog

This file records repository history, not roadmap intent or validation claims.
Historical failures remain historical even when later work resolves them.

## 2026-09-05 — Capability-first golden integration

Six independent branches rewrote the repository's **51 live Markdown files** from
the same `main` baseline, then were composed on an isolated integration branch and
reviewed as one system before any change reached `main`.

The redesign shifts Parallax toward high-agency engineering: problem compression,
architecture and algorithm selection, useful representation design, discriminating
tool use, debugging by information gain, performance reasoning, and stronger
first-pass solutions. Process that does not materially change engineering outcomes
was compressed or removed. This is not permission to weaken the hard boundaries
that still protect correctness.

The unified documentation preserves these compatibility/trust invariants:

- task semantics are not silently rewritten to favor a candidate;
- program/type validity remains distinct from task acceptance;
- generated artifacts remain data rather than self-granted host authority;
- `intseq/0.1`, `arl-capsule/0.1`, and `arl-program/0.1` retain their established
  meanings/identifiers;
- canonical example capsule/program identities remain unchanged;
- the embedded reference Python fence remains byte-identical;
- security, oracle custody, and actual tool evidence are not replaced by prose.

Integration QC also removed two recursively fragile documentation conventions. The
documentation checker now protects executable/canonical semantic boundaries rather
than requiring explanatory Markdown wrappers to remain byte-identical forever, and
the programmer packet binds task/protocol/canonical identities rather than live
whole-Markdown hashes.

### Provenance publication correction

The repository-wide QC discovered an inherited publication defect: the source ZIP
blob in Git was truncated and did not match the archive SHA-256 recorded by the
bootstrap inventory. The published corrupt blob SHA-256 is
`395880b60332513c0b50f6f00c9ed172b5f5669d5d35910fdddb52630bdddc77`.

A full-history Git-blob scan plus salvage of complete ZIP records independently
recovered exact recorded bytes for **27 of 36** original source documents. Nine
original source payloads were not recoverable. No bytes were fabricated to satisfy
their recorded hashes.

`docs/provenance/adaptive-representations-source.zip` is now an explicit
partial-recovery container with SHA-256
`f1f443cc5e574b0b87bb4c45fe1e9d0a54613ed877cf635297e887e9db011398`.
It contains the 27 exact recovered originals plus `RECOVERY.md`, which records the
nine unavailable paths with their historical byte counts and SHA-256 identities.
`source-inventory.json` retains the historical intended archive SHA, the corrupt
published SHA, the active recovery SHA, and the full 36-source ledger.

### Integration verification

The composed repository was exercised on GitHub Actions using CPython 3.13.15.
The QC gates include:

- `python tools/check_docs.py` over live routing, local links, recovery provenance,
  canonical JSON identities, the reference fence, intseq signatures, packet
  semantic bindings, and spec metadata;
- `python -m unittest discover -s tools -p 'test_check_docs.py' -v` against positive
  and negative documentation-integrity cases;
- `git diff --check` against the six-agent baseline;
- extraction of the preserved reference Python fence after verifying its SHA-256;
- the reference's public `--selftest`;
- the worked capsule/program on `[-2,-1,0,2]`, requiring value `16`, status
  `EVALUATED`, and `task_correctness: NOT_CHECKED`.

The final merge is permitted only after these gates pass against the committed
integration tree. They establish the properties named above, not universal
correctness of future implementations or research claims.

Project maturity is otherwise unchanged: SPEC-001 remains the current
implementation-ready task, and this documentation integration does not itself add
a packaged Parallax runtime, orchestration host, native/GPU backend, held-out
benchmark, production sandbox, performance result, or formal proof.

## 2026-09-05 — Parallax repository bootstrap and publication

The initial Parallax repository was established and the adaptive-representations
source corpus was migrated into a routed research/engineering layout. The bootstrap:

- recorded the source-corpus identities and preserved the stable `intseq/0.1`
  meaning, legacy `arl-capsule/0.1` / `arl-program/0.1` wire identifiers, canonical
  example identities, and embedded Python reference source;
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
documentation and did not change semantic/protocol identities.

## Source history — 0.1, dated 2026-09-05

The historical 0.1 release note describes the original Markdown starter:
task/contract/capsule/evidence separation, a bounded agent protocol, selective
context routes, the exact-integer intseq reference/example, a GPU reduction-scope
design critique, and a matched-budget research plan.

That note is imported source history, not a later Parallax release. The active
partial-recovery archive and complete recorded source ledger are described in
[SOURCE-MAP.md](docs/provenance/SOURCE-MAP.md) and
[source-inventory.json](docs/provenance/source-inventory.json).
