# Bootstrap audit — historical record from 2026-09-05

This file records the **documentation bootstrap as it actually happened**. It is not
a live report of the repository's current remote state, implementation maturity,
or later verification.

- **Task date:** 2026-09-05 (America/Anchorage)
- **Reviewer:** bootstrap agent; document-level self-audit
- **Scope:** local documentation/provenance preparation, not independent
  implementation review or a coding/LLM benchmark

## Remote-publication result at the time

The bootstrap prepared a local repository with `main` as a minimal initial history
commit and `docs/bootstrap-parallax` as a local documentation branch with grouped
commits. Those refs were local artifacts during the audit.

Two GitHub write paths were attempted and both returned HTTP 403
`Resource not accessible by integration`:

1. `GitHub.create_file` for `README.md`;
2. `GitHub.create_blob` as a Git-data write-path check.

Repository metadata reported account push permission, but that did not make the
integration writes succeed. No permissions were changed. The final branch-list read
performed by the bootstrap returned `[]`.

Therefore, for **that bootstrap episode**:

- successful remote writes: **0**;
- remote pull requests created: **0**;
- remote publication/readback of the prepared branch: **not performed because
  publication was blocked**.

The exact attempt record is [publication-attempts.json](publication-attempts.json).
Later Git history or later connector capabilities supersede this as a statement
about current remote state; they do not change what happened in the bootstrap.

## Checks actually executed in the bootstrap

Environment: Python `3.13.5`.

```sh
python --version
python tools/check_docs.py
python -m unittest discover -s tools -p 'test_check_docs.py' -v
git diff --cached --check
```

Reported outcomes:

- documentation checker: **PASS**;
- documentation-tool regression suite: **7 tests, PASS**;
- staged whitespace check: **PASS**.

[doc-integrity.json](doc-integrity.json) records the checker result: 48 live Markdown
files, 189 local links checked, 36 archive Markdown inputs covered, 35 old-manifest
entries checked, five programmer-packet source identities checked, and no runtime
semantic execution by that checker. [doc-checker-tests.txt](doc-checker-tests.txt)
preserves the seven test names/results.

The checker validated routing/provenance structure and selected frozen identities.
It did **not** establish semantic correctness of the intseq implementation or any
LLM/research claim.

## What the bootstrap established

The audit found the prepared documentation internally coherent for its intended
bootstrap role:

- a routed entry from README/START to one bounded implementation spec;
- separation between repository development, representation synthesis, and research
  routes;
- an architecture/source-of-truth map with three explicit decisions;
- preserved `intseq/0.1` meanings, legacy `arl-*` identifiers, canonical example
  identities, and the byte-identical extracted Python fence;
- all 36 source Markdown documents assigned migration dispositions, with the local
  bootstrap reporting originals present in its source ZIP;
- historical source-reported intseq execution clearly labeled as imported rather
  than newly run evidence;
- research/GPU material kept non-authoritative for the first implementation task;
- SPEC-001 supplied a compatibility baseline, interfaces, edge cases, acceptance
  criteria, and planned verification sufficient for a bootstrap-author
  `ready-for-dev` judgment.

The bootstrap also reported that 22 migrated live Markdown documents were
byte-identical to their corresponding source inputs; rewritten or annotated
documents were accounted for separately in the [source map](SOURCE-MAP.md).

## What the bootstrap did not establish

No claim was made that any of the following ran or existed as a completed capability
during the bootstrap:

- packaged Parallax runtime;
- intseq self-test or new implementation test suite;
- LLM synthesis/development trial;
- orchestration host or isolated final oracle;
- native/GPU compilation or execution;
- performance comparison;
- formal proof.

The source-author public intseq result report was not independently reproduced.
Reading/hashing the embedded Python source was not treated as runtime validation.

SPEC-001's `ready-for-dev` state was a document-level planning judgment by the
bootstrap author, not a result of the metadata checker and not evidence that
implementation acceptance had already passed.

## Historical limitations and next action

At the end of that episode, host/provider/storage/isolation choices, benchmark task
distributions, concrete research promotion criteria, and project licensing remained
unresolved future work. None was required to begin the bounded intseq extraction
task.

The recorded next engineering action **at that time** was to implement
[SPEC-001](../specs/001-intseq-reference.md), produce fresh implementation evidence,
and publish the prepared repository once GitHub write access worked. This statement
is retained as history; current work should determine its next action from current
source, specs, and repository state rather than treating this audit as a live
roadmap.

## Later publication-recovery correction

A later repository-wide QC pass discovered that the source ZIP blob that ultimately
reached GitHub was truncated and did **not** match the archive SHA-256 recorded by
the bootstrap inventory. This does not rewrite the bootstrap's contemporaneous
local report; it corrects what can be established about the later published
artifact.

The published truncated blob has SHA-256
`395880b60332513c0b50f6f00c9ed172b5f5669d5d35910fdddb52630bdddc77`.
A full-history Git-blob search plus salvage of complete ZIP records recovered exact
recorded bytes for **27 of 36** original source documents. Nine original payloads
were not recoverable from the published blob or Git history. No replacement bytes
were fabricated.

The current source archive is therefore an explicit partial-recovery container with
SHA-256
`f1f443cc5e574b0b87bb4c45fe1e9d0a54613ed877cf635297e887e9db011398`.
The active inventory and [source map](SOURCE-MAP.md) record the unavailable paths,
historical intended archive SHA, published corrupt SHA, and recovery semantics.

This correction is later evidence about publication integrity. It does not turn the
bootstrap's historical `PASS` into a current pass or retroactively claim that the
bootstrap agent observed the remote corruption.

## Interpretation rule

Use this document to answer historical questions such as “what did the bootstrap
actually check?” or “was the imported intseq report rerun?” Do not use it as
evidence for a later commit merely because the file remains in the repository. New
claims require evidence against the new artifact/revision.
