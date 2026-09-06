# Source map: archive → 2026-09-05 Parallax bootstrap

This document records how the original adaptive-representations Markdown archive was migrated into the Parallax bootstrap. It is **historical provenance**, not a live semantic specification, capability registry, or instruction to restore the old document layout.

Later edits are ordinary Git history. They do not change the source-archive facts recorded here.

## Immutable input record

The original ZIP remains at `docs/provenance/adaptive-representations-source.zip`.

- archive SHA-256: `2ef132444533406479eb1ad54afe5bd5be364803aed166b4f3b15f41d5d0f0ca`
- source prefix: `adaptive-representations/`
- Markdown inputs: **36**
- old manifest entries: **35** (the manifest did not list itself)

[source-inventory.json](source-inventory.json) is the machine-readable ledger for every source path, original byte count, computed SHA-256, migration disposition, consumer, and target. The bootstrap checked those identities against the preserved ZIP. Old source hashes identify **archive inputs**; they are not asserted over later rewritten live files.

Important preserved executable/data identities:

- extracted Python fence SHA-256: `4025a0043e958785196e35d6530ec4570dcedd36cf621b555249a1809649dc91`
- canonical example capsule JSON SHA-256: `2a340d75023574cd3b55590dfe5583700984ded258b1257f316dd7b6490e2ee9`
- canonical example program JSON SHA-256: `db2dad5bd80762eb3fa6eeba57410027755dfdcc57d22ff212236b99613b1517`

The programmer packet also froze five whole-file source identities at bootstrap:

| Source | Whole-file SHA-256 |
|---|---|
| `examples/intseq/TASK.md` | `f08bce72ad70d544409917c41af5b07dcb9a15c84731b733f32b40464a9b4f50` |
| `examples/intseq/CAPSULE.md` | `33bd94fe2226635f81af35fe5b897f618d036d0d2341aac0e8694a6aaca812d8` |
| `packs/intseq/PACK.md` | `1d3de58d8bbdb9334f2fee2d40135aada79e26b35decc9cbe146e0c099ff717b` |
| `packs/intseq/CAPSULE.md` | `f38fcb922a05528d1dc8db48127a6bb5eef4a5555420bf2f35f5886ef5a30029` |
| `roles/PROGRAMMER.md` | `6d13cda30c80161317b29ed7f450c8367b49072d8cd1de2839e2ecbd3f9736a9` |

A hash binds bytes under a recipe. It is not semantic correctness, provenance authentication, or execution evidence.

## Migration dispositions

The migration used a few distinct operations. “Preserved” means the live bootstrap file retained the source bytes. “Annotated” retained substantive source content while adding maturity/authority framing. “Rewritten,” “split,” “moved,” and “extended” deliberately changed the live presentation while preserving the original in the ZIP and recording the relationship here.

### Rewritten, split, moved, annotated, or extended inputs

| Original source | Bootstrap disposition | Live target(s) | What changed without changing the historical source |
|---|---|---|---|
| `AGENTS.md` | rewritten | `AGENTS.md`, `docs/development/WORKFLOW.md` | Universal constraints were compressed; development mechanics were routed out of ambient context. |
| `CHANGELOG.md` | superseded | `CHANGELOG.md` | Original 0.1 release note stayed in the ZIP; live changelog began recording Parallax history. |
| `MANIFEST.md` | retired-as-live | `docs/provenance/source-inventory.json`, `docs/provenance/SOURCE-MAP.md` | Static migrated-file manifest replaced by source-input provenance plus Git history. |
| `README.md` | split | `README.md`, `docs/PROJECT.md`, `runtime/REFERENCE.md`, `START.md` | Branding/current-state summary, project intent, reference extraction, and agent entry were separated by purpose. |
| `ROUTES.md` | rewritten | `ROUTES.md` | Kept selective context assembly/identity ideas while separating development from task solving. |
| `START.md` | rewritten | `START.md` | Added deterministic implementation, synthesis, and research entry routes. |
| `examples/intseq/EVIDENCE.md` | annotated | `examples/intseq/EVIDENCE.md` | Source-author run report was explicitly labeled imported/not rerun; historical JSON/hashes were retained. |
| `research/EVALUATION.md` | moved-and-expanded | `docs/benchmarking/PROTOCOL.md` | Evaluation ideas moved into an experiment protocol and were separated from repository-development pilots. |
| `research/RELATED-WORK.md` | annotated | `research/RELATED-WORK.md` | Bibliography/positioning retained with explicit historical/non-authoritative framing. |
| `research/ROADMAP.md` | moved-and-revised | `docs/ROADMAP.md` | Research sequencing moved into the project roadmap; an executable-reference extraction gate was inserted. |
| `research/THESIS.md` | annotated | `research/THESIS.md` | Research argument retained behind a non-authoritative route. |
| `runtime/HOST.md` | annotated | `runtime/HOST.md` | Clarified source-level reference capability versus an unimplemented orchestration/security host. |
| `runtime/REFERENCE.md` | wrapper-rewritten-source-preserved | `runtime/REFERENCE.md`, `docs/specs/001-intseq-reference.md` | Markdown framing/extraction guidance changed; the Python fence stayed byte-identical and a bounded implementation spec was added. |
| `templates/RUN.md` | extended | `templates/RUN.md` | Original evidence fields were retained and development/benchmark record fields were added. |

### Byte-preserved live inputs at bootstrap

The following **22** source documents were migrated byte-for-byte to the same live path at bootstrap:

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

“Byte-preserved at bootstrap” is a historical migration result, not a rule that these paths can never evolve. Externally meaningful semantic/version identities remain governed by their owning contracts and explicit evolution rules.

## What the migration deliberately preserved

The Parallax rename did **not** rename or redefine:

- `intseq/0.1` primitive meanings;
- `arl-capsule/0.1` or `arl-program/0.1` wire identifiers;
- the canonical example capsule/program JSON identities;
- the frozen worked task meaning;
- the extracted reference Python source fence.

The source archive's public intseq execution report remained historical source-author evidence; the bootstrap did not silently upgrade it into a fresh independent run.

GPU material remained design-only. Research claims and the related-work bibliography were preserved rather than revalidated. The archive contained no project license, so the bootstrap did not infer one. The BMAD study informed methodology but did not install BMAD or import it as a runtime dependency.

## What the migration deliberately retired or changed

The old “every deliverable is Markdown” distribution convention was retired because Parallax was intended to gain ordinary source and tests. The live `MANIFEST.md` concept was retired in favor of source-input provenance plus Git identities. README/startup duplication was separated by audience and action.

These were presentation/process changes, not permission to weaken semantic or acceptance boundaries.

## New bootstrap artifacts

The 2026-09-05 bootstrap added engineering functions that were missing from the source archive, including:

- `docs/PROJECT.md` for current intent/maturity;
- `docs/architecture/ARCHITECTURE.md` and three ADRs;
- `docs/development/WORKFLOW.md` and `VERIFICATION.md`;
- `docs/benchmarking/PROTOCOL.md`;
- `docs/specs/001-intseq-reference.md` and `templates/SPEC.md`;
- this provenance map, source inventory, BMAD study, and bootstrap audit;
- `tools/check_docs.py` plus its regression tests.

Those additions were bootstrap decisions traceable to source concerns or explicitly new project organization. They were not present as original archive files and should not be misdescribed as byte-preserved migration.

## How to use this map

For an implementation question, use the current authoritative document/code, not this history. Use this map when you need to answer one of three questions:

1. **What did the source archive contain?** → inspect the preserved ZIP and `source-inventory.json`.
2. **How did an old source path become the bootstrap layout?** → use the disposition tables above.
3. **Which identity must remain compatible?** → follow the current semantic/architecture authority and the preserved identity facts above; do not infer compatibility from path similarity alone.

The [bootstrap audit](BOOTSTRAP-AUDIT.md) records what checks actually ran during the migration. [BMAD-STUDY](BMAD-STUDY.md) records the pinned methodological influence. Neither is a substitute for current implementation evidence.
