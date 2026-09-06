# Bootstrap audit — local preparation, publication blocked

**Task date:** 2026-09-05 (America/Anchorage).
**Reviewer:** bootstrap agent, document-level self-audit. This was not an
independent implementation review or a fresh coding-agent benchmark trial.

## Delivery and remote state

The prepared local repository has `main` as a minimal initial history commit and
`docs/bootstrap-parallax` as the documentation branch, with conceptually grouped
commits. These are **local** refs, not claims of GitHub publication.

GitHub's Contents write and Git-data blob write both returned HTTP 403,
`Resource not accessible by integration`. Repository metadata reported account
push access, but it did not make these integration writes succeed. No permissions
were changed. A final GitHub branch-list read still returned `[]`. There were zero
successful remote writes and no PR was created.

The requested audit of populated remote files could therefore **not** be performed.
Local integrity/readiness checks below are not described as a GitHub readback.
See [publication-attempts.json](publication-attempts.json) for the recorded blocker.
Do not infer a remote branch from the local branch name.

## Executed documentation checks

Environment: Python `3.13.5`. These commands check documentation/tooling only:

```sh
python --version
python tools/check_docs.py
python -m unittest discover -s tools -p 'test_check_docs.py' -v
git diff --cached --check
```

The documentation checker passed; its exact counts and scope are in
[doc-integrity.json](doc-integrity.json). It covers 48 live Markdown files, source
coverage for all 36 archive Markdown inputs, all 35 old manifest entries, frozen
reference/JSON identities, and the five programmer-packet source identities.
Twenty-two migrated live documents are byte-identical to their original source;
rewritten/annotated documents are separately accounted for by the source map.

The documentation-tool suite passed **7 tests**: one clean repository plus six
negative cases (broken local link, frozen pack drift, changed reference fence,
invalid spec state, unclosed fence, and omitted provenance entry). Raw unittest
output is in [doc-checker-tests.txt](doc-checker-tests.txt). These are not intseq
runtime tests. Staged whitespace checks passed for the grouped documentation
commits; they do not assess semantics.

## Readiness and integrity review

| Concern | Finding |
|---|---|
| Routing | README → START → SPEC-001 is explicit. Implementation and solution-generation routes differ; research/other packs do not enter default coding context |
| Authority | Architecture maps each truth to an owning artifact. ADRs explain decisions; templates, examples, packets, and research do not override specifications |
| Duplication | The packet is intentional, identity-bound derived context. Full source duplication is contained inside the provenance ZIP, not competing live AGENTS files |
| Contradictions | Historical source-reported execution is framed as imported evidence. Planned package/host paths are not represented as implemented capabilities |
| Semantic integrity | Core meaning and wire identifiers retained. Python fence, canonical capsule/program hashes, frozen task/pack/schema files, and packet dependencies match |
| ADR quality | Three actual source-derived decisions: stable meaning/adaptive surface, generated data without authority, and separate task acceptance |
| Research boundary | Thesis, bibliography, GPU design critique, and future hypotheses remain routed and non-authoritative for implementation |
| Evidence | No runtime execution, held-out test, LLM trial, native/GPU measurement, or formal proof was claimed as performed by this bootstrap |
| Links | Current inline local Markdown links resolve; the checker also checks local heading fragments. External URLs and plain-text planned file names are not network/path-validated |
| Source coverage | All 36 Markdown sources have dispositions and computed input identities; originals remain in the byte-identical ZIP |
| Implementation readiness | SPEC-001 has a frozen compatibility baseline, supported tooling, existing/planned paths, library/CLI contract, edge cases, nine acceptance criteria, and a verification plan |
| Agent usability | Document-level dry run reaches one bounded task without a model API, BMAD install, GPU toolchain, or author restatement. No fresh agent has implemented it yet |
| Remote publication/readback | Blocked by integration 403; remote repository remained without branches at the last check |

SPEC-001's `ready-for-dev` state is a planning judgment by the bootstrap author,
not a consequence of merely passing the metadata checker. Its runtime verification
commands are still **unexecuted**. `tools/check_docs.py` checks a small supported
Markdown/frontmatter subset; it is neither a full Markdown/YAML parser nor proof
of absence of semantic/documentation defects.

## Deliberate remaining limits

The project has no packaged runtime, actual synthesis host, isolated final oracle,
benchmark task distribution, or comparative results. Host/provider/storage/isolation
choices, research promotion criteria for a concrete dataset, and licensing remain
future decisions. The source author's public result report was not independently
reproduced. These limits do not prevent starting the bounded extraction task.

The next engineering action is to implement
[SPEC-001](../specs/001-intseq-reference.md) using its specified context and record
new evidence. Publishing the local bootstrap still requires functioning GitHub
write access; this audit does not claim that the remote-delivery exit condition
has been met.
