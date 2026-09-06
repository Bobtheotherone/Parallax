# Source map: archive → 2026-09-05 Parallax bootstrap

This document records how the original adaptive-representations Markdown corpus was
migrated into the Parallax bootstrap. It is **historical provenance**, not a live
semantic specification, capability registry, or instruction to restore the old
document layout.

Later edits are ordinary Git history. They do not change the source-input identities
recorded here.

## Historical input record

The bootstrap inventory describes an intended source ZIP with:

- historical declared archive SHA-256:
  `2ef132444533406479eb1ad54afe5bd5be364803aed166b4f3b15f41d5d0f0ca`;
- source prefix: `adaptive-representations/`;
- Markdown inputs: **36**;
- old manifest entries: **35** (the manifest did not list itself).

[source-inventory.json](source-inventory.json) is the machine-readable ledger for
every source path, original byte count, recorded SHA-256, migration disposition,
consumer, and target.

### Publication-recovery correction

During the later golden-integration QC, the ZIP blob actually present in Git was
found to be truncated inside `adaptive-representations/START.md`. Its published
corrupt SHA-256 is
`395880b60332513c0b50f6f00c9ed172b5f5669d5d35910fdddb52630bdddc77`.
It is therefore **not** valid evidence that all 36 original payloads were preserved
in the remote repository, despite the bootstrap's earlier local report.

A full-history blob search plus salvage of complete ZIP members independently
recovered the exact recorded bytes for **27 of the 36** source documents. The other
nine original payloads were not present as recoverable historical Git blobs and lie
beyond the published truncation point:

```text
START.md
examples/intseq/EVIDENCE.md
research/EVALUATION.md
research/RELATED-WORK.md
research/ROADMAP.md
research/THESIS.md
runtime/HOST.md
runtime/REFERENCE.md
templates/RUN.md
```

The file at `docs/provenance/adaptive-representations-source.zip` is now an explicit
**partial-recovery archive**, not a claim to be the missing historical container.
Its active SHA-256 is
`f1f443cc5e574b0b87bb4c45fe1e9d0a54613ed877cf635297e887e9db011398`.
It contains the 27 independently recovered original byte streams plus
`adaptive-representations/RECOVERY.md`, which names each unavailable original with
its previously recorded byte count and SHA-256. No replacement bytes were invented
to satisfy unavailable hashes.

The active status, both historical/published container hashes, recovered-source
count, unavailable-source list, and all 36 recorded source identities live in
[source-inventory.json](source-inventory.json). The original `MANIFEST.md` was among
the recovered inputs, so its 35 declarations remain independently checkable against
the inventory even when nine payload byte streams are unavailable.

Old source hashes identify **historical archive inputs**; they are not asserted over
later rewritten live files.

Important preserved executable/data identities:

- extracted Python fence SHA-256:
  `4025a0043e958785196e35d6530ec4570dcedd36cf621b555249a1809649dc91`;
- canonical example capsule JSON SHA-256:
  `2a340d75023574cd3b55590dfe5583700984ded258b1257f316dd7b6490e2ee9`;
- canonical example program JSON SHA-256:
  `db2dad5bd80762eb3fa6eeba57410027755dfdcc57d22ff212236b99613b1517`.

The programmer packet also froze five whole-file source identities at bootstrap:

| Source | Whole-file SHA-256 |
|---|---|
| `examples/intseq/TASK.md` | `f08bce72ad70d544409917c41af5b07dcb9a15c84731b733f32b40464a9b4f50` |
| `examples/intseq/CAPSULE.md` | `33bd94fe2226635f81af35fe5b897f618d036d0d2341aac0e8694a6aaca812d8` |
| `packs/intseq/PACK.md` | `1d3de58d8bbdb9334f2fee2d40135aada79e26b35decc9cbe146e0c099ff717b` |
| `packs/intseq/CAPSULE.md` | `f38fcb922a05528d1dc8db48127a6bb5eef4a5555420bf2f35f5886ef5a30029` |
| `roles/PROGRAMMER.md` | `6d13cda30c80161317b29ed7f450c8367b49072d8cd1de2839e2ecbd3f9736a9` |

Those whole-file packet hashes are retained here as bootstrap history. The live
packet now binds executable meaning through stable task/protocol/canonical
identities rather than recursively freezing explanatory Markdown prose.

A hash binds bytes under a recipe. It is not semantic correctness, provenance
authentication, or execution evidence.

## Migration dispositions

The migration used a few distinct operations. “Preserved” means the live bootstrap
file retained the source bytes. “Annotated” retained substantive source content
while adding maturity/authority framing. “Rewritten,” “split,” “moved,” and
“extended” deliberately changed the live presentation while recording the original
relationship here.

### Rewritten, split, moved, annotated, or extended inputs

| Original source | Bootstrap disposition | Live target(s) | What changed without changing the historical source |
|---|---|---|---|
| `AGENTS.md` | rewritten | `AGENTS.md`, `docs/development/WORKFLOW.md` | Universal constraints were compressed; development mechanics were routed out of ambient context. |
| `CHANGELOG.md` | superseded | `CHANGELOG.md` | Original 0.1 release note became source history; live changelog records Parallax history. |
| `MANIFEST.md` | retired-as-live | `docs/provenance/source-inventory.json`, `docs/provenance/SOURCE-MAP.md` | Static migrated-file manifest was replaced by source-input provenance plus Git history. |
| `README.md` | split | `README.md`, `docs/PROJECT.md`, `runtime/REFERENCE.md`, `START.md` | Branding/current-state summary, project intent, reference extraction, and agent entry were separated by purpose. |
| `ROUTES.md` | rewritten | `ROUTES.md` | Kept selective context assembly/identity ideas while separating development from task solving. |
| `START.md` | rewritten | `START.md` | Added deterministic implementation, synthesis, and research entry routes. |
| `examples/intseq/EVIDENCE.md` | annotated | `examples/intseq/EVIDENCE.md` | Source-author run report was explicitly labeled imported/not rerun; historical JSON/hashes were retained in the live migrated document. |
| `research/EVALUATION.md` | moved-and-expanded | `docs/benchmarking/PROTOCOL.md` | Evaluation ideas moved into an experiment protocol and were separated from repository-development pilots. |
| `research/RELATED-WORK.md` | annotated | `research/RELATED-WORK.md` | Bibliography/positioning retained with explicit historical/non-authoritative framing. |
| `research/ROADMAP.md` | moved-and-revised | `docs/ROADMAP.md` | Research sequencing moved into the project roadmap; an executable-reference extraction gate was inserted. |
| `research/THESIS.md` | annotated | `research/THESIS.md` | Research argument retained behind a non-authoritative route. |
| `runtime/HOST.md` | annotated | `runtime/HOST.md` | Clarified source-level reference capability versus an unimplemented orchestration/security host. |
| `runtime/REFERENCE.md` | wrapper-rewritten-source-preserved | `runtime/REFERENCE.md`, `docs/specs/001-intseq-reference.md` | Markdown framing/extraction guidance changed; the Python fence stayed byte-identical and a bounded implementation spec was added. |
| `templates/RUN.md` | extended | `templates/RUN.md` | Original evidence fields were retained and development/benchmark record fields were added. |

### Byte-preserved live inputs at bootstrap

The following **22** source documents were reported as migrated byte-for-byte to
the same live path at bootstrap:

```text
core/CAPSULE.md
core/CONTRACT.md
core/ECONOMICS.md
core/EVIDENCE.md
core/EVOLUTION.md
core/PROTOCOL.md
core/SEMANTICS.md
examples/intseq/CAPSULE.md
examples/intseq/FAILURE.md
examples/intseq/PACKET.md
examples/intseq/PROGRAM.md
examples/intseq/TASK.md
packs/gpu/RMSNORM.md
packs/intseq/CAPSULE.md
packs/intseq/PACK.md
packs/intseq/TUTORIAL.md
roles/PROGRAMMER.md
roles/REVIEWER.md
roles/SYNTHESIZER.md
templates/CAPSULE.md
templates/EXTENSION.md
templates/TASK.md
```

“Byte-preserved at bootstrap” is a historical migration result, not a rule that
these live paths can never evolve. Where an original payload is among the 27 exact
recoveries, the archive independently retains that historical byte stream; otherwise
the inventory retains only the original recorded identity and migration relation.
Externally meaningful semantic/version identities remain governed by their owning
contracts and explicit evolution rules.

## What the migration deliberately preserved

The Parallax rename did **not** rename or redefine:

- `intseq/0.1` primitive meanings;
- `arl-capsule/0.1` or `arl-program/0.1` wire identifiers;
- the canonical example capsule/program JSON identities;
- the worked task meaning;
- the extracted reference Python source fence.

The source corpus's public intseq execution report remained historical source-author
evidence; the bootstrap did not silently upgrade it into a fresh independent run.

GPU material remained design-only. Research claims and the related-work bibliography
were migrated rather than revalidated. The source corpus contained no project
license, so the bootstrap did not infer one. The BMAD study informed methodology but
did not install BMAD or import it as a runtime dependency.

## What the migration deliberately retired or changed

The old “every deliverable is Markdown” distribution convention was retired because
Parallax was intended to gain ordinary source and tests. The live `MANIFEST.md`
concept was retired in favor of source-input provenance plus Git identities.
README/startup duplication was separated by audience and action.

These were presentation/process changes, not permission to weaken semantic or
acceptance boundaries.

## New bootstrap artifacts

The 2026-09-05 bootstrap added engineering functions that were missing from the
source corpus, including:

- `docs/PROJECT.md` for current intent/maturity;
- `docs/architecture/ARCHITECTURE.md` and three ADRs;
- `docs/development/WORKFLOW.md` and `VERIFICATION.md`;
- `docs/benchmarking/PROTOCOL.md`;
- `docs/specs/001-intseq-reference.md` and `templates/SPEC.md`;
- this provenance map, source inventory, BMAD study, and bootstrap audit;
- `tools/check_docs.py` plus its regression tests.

Those additions were bootstrap decisions traceable to source concerns or explicitly
new project organization. They were not present as original source files and should
not be misdescribed as byte-preserved migration.

## How to use this map

For an implementation question, use the current authoritative document/code, not
this history. Use this map when you need to answer one of four questions:

1. **What did the historical source corpus claim to contain?** → use
   `source-inventory.json`, recovered `MANIFEST.md`, and the recovery status above.
2. **Which original bytes are independently available now?** → inspect the active
   partial-recovery ZIP and its `RECOVERY.md`; do not assume all 36 payloads exist.
3. **How did an old source path become the bootstrap layout?** → use the disposition
   tables above.
4. **Which identity must remain compatible?** → follow the current
   semantic/architecture authority and the preserved identity facts above; do not
   infer compatibility from path similarity alone.

The [bootstrap audit](BOOTSTRAP-AUDIT.md) records what checks were reported during
the migration episode. [BMAD-STUDY](BMAD-STUDY.md) records the pinned methodological
influence. Neither is a substitute for current implementation evidence.
