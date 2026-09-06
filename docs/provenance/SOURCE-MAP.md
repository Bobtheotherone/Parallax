# Source map and migration provenance

**Consumer:** maintainer or reviewer checking that migration did not erase meaning.
This is history and identity data, not implementation authority or a live capability
registry. The source archive's 36 Markdown documents were recursively inventoried
and read in full, including the embedded Python reference.

## Input and identity

The [original source ZIP](adaptive-representations-source.zip) is preserved
byte-for-byte, including its old entry points, manifest, and release note.
Archive SHA-256: `2ef132444533406479eb1ad54afe5bd5be364803aed166b4f3b15f41d5d0f0ca`.

[source-inventory.json](source-inventory.json) records every original path, byte
count, actually computed SHA-256, disposition, consumer, and destination. The old
manifest's 35 entries (it excluded itself) matched the supplied archive. Its
hashes are **not** asserted over rewritten live documents. All 36 originals,
including the manifest itself, have input identities in the inventory.

The runtime Python fence remains byte-identical under extraction with a final LF:
`4025a0043e958785196e35d6530ec4570dcedd36cf621b555249a1809649dc91`.
Canonical JSON identities and the five whole-file sources used by the frozen
programmer packet also remain unchanged. Documentation prose outside a JSON
fence is not part of that canonical JSON identity. Git/checksum identity is not
correctness, authorship authentication, or runtime evidence.

## Dispositions

“Preserved” means live source bytes were retained at bootstrap. “Annotated” keeps
the substantive source and adds maturity/authority framing. Rewrites and splits
move authority deliberately; originals remain in the ZIP, not as competing active
agent instructions. Only AGENTS is ambient; every other consumer follows a route.

| Original path | Disposition | Live destination | Kind / consumer / retained truth |
|---|---|---|---|
| `AGENTS.md` | rewritten | [AGENTS.md](../../AGENTS.md), [docs/development/WORKFLOW.md](../development/WORKFLOW.md) | procedural; all agents. Compact universal boundaries; development mechanics routed, not always loaded. |
| `CHANGELOG.md` | superseded | [CHANGELOG.md](../../CHANGELOG.md) | historical; maintainer. Original 0.1 release note retained in source ZIP; current changelog records actual bootstrap changes separately. |
| `MANIFEST.md` | retired-as-live | [docs/provenance/source-inventory.json](source-inventory.json), [docs/provenance/SOURCE-MAP.md](SOURCE-MAP.md) | historical identity; auditor. Original 35-entry manifest checked against archive bytes; never asserted over migrated paths. |
| `README.md` | split | [README.md](../../README.md), [docs/PROJECT.md](../PROJECT.md), [runtime/REFERENCE.md](../../runtime/REFERENCE.md), [START.md](../../START.md) | explanatory/procedural; human and implementer. Parallax identity/current state replaces old branding; extraction moved beside reference; scope/license retained. |
| `ROUTES.md` | rewritten | [ROUTES.md](../../ROUTES.md) | procedural; agent/context host. Keep minimum-context assembly, identity caching, and packet limitations; separate development from solution generation. |
| `START.md` | rewritten | [START.md](../../START.md) | procedural; new agent. Deterministic first coding task plus distinct synthesis/research entries; preserve modes and contract-first behavior. |
| `core/CAPSULE.md` | preserved | [core/CAPSULE.md](../../core/CAPSULE.md) | normative design; capsule implementer. Capsule authority, admission, identity, full algorithm cost, no unsupported novelty. |
| `core/CONTRACT.md` | preserved | [core/CONTRACT.md](../../core/CONTRACT.md) | normative design; task owner/evaluator. Frozen task, two checks, acceptance independence, ambiguity stop condition. |
| `core/ECONOMICS.md` | preserved | [core/ECONOMICS.md](../../core/ECONOMICS.md) | normative experimental policy; experiment operator. Full cost decomposition, direct fallback, cold/warm accounting, honest success/diversity measures. |
| `core/EVIDENCE.md` | preserved | [core/EVIDENCE.md](../../core/EVIDENCE.md) | normative evidence policy; reviewer/operator. Orthogonal evidence and independence properties; no universal verification label. |
| `core/EVOLUTION.md` | preserved | [core/EVOLUTION.md](../../core/EVOLUTION.md) | normative design; extension author. Extension classes, versioning, retirement, cache dependencies and interfaces. |
| `core/PROTOCOL.md` | preserved | [core/PROTOCOL.md](../../core/PROTOCOL.md) | normative proposed host protocol; host/synthesis agent. State machine, default attempt policy, diagnostics, revision and honest terminal outcomes. |
| `core/SEMANTICS.md` | preserved | [core/SEMANTICS.md](../../core/SEMANTICS.md) | normative design; semantic implementer. Preservation vs task satisfaction, observation models, numerical/effect/resource boundaries. |
| `examples/intseq/CAPSULE.md` | preserved | [examples/intseq/CAPSULE.md](../../examples/intseq/CAPSULE.md) | illustrative frozen data; implementer/program generator. Canonical capsule identity and source bytes unchanged. |
| `examples/intseq/EVIDENCE.md` | annotated | [examples/intseq/EVIDENCE.md](../../examples/intseq/EVIDENCE.md) | historical evidence; reviewer. Report explicitly attributed to archive author; JSON output and historical hashes retained; no bootstrap execution claim. |
| `examples/intseq/FAILURE.md` | preserved | [examples/intseq/FAILURE.md](../../examples/intseq/FAILURE.md) | illustrative negative case; implementer/reviewer. Typed wrong algorithm and diagnostic ownership preserved. |
| `examples/intseq/PACKET.md` | preserved | [examples/intseq/PACKET.md](../../examples/intseq/PACKET.md) | derived frozen context; program-generation host. One-call view retained; its five source-file identities still match; not a semantic authority. |
| `examples/intseq/PROGRAM.md` | preserved | [examples/intseq/PROGRAM.md](../../examples/intseq/PROGRAM.md) | illustrative frozen data; implementer/program generator. Program JSON and capsule binding unchanged. |
| `examples/intseq/TASK.md` | preserved | [examples/intseq/TASK.md](../../examples/intseq/TASK.md) | frozen example contract; task evaluator. Input domain, relation, public policy, examples and owner unchanged. |
| `packs/gpu/RMSNORM.md` | preserved | [packs/gpu/RMSNORM.md](../../packs/gpu/RMSNORM.md) | design-only proposal/critique; future pack researcher. Numerical/reduction-scope/ABI ideas retained without adopting a GPU implementation. |
| `packs/intseq/CAPSULE.md` | preserved | [packs/intseq/CAPSULE.md](../../packs/intseq/CAPSULE.md) | normative format; parser/checker implementer. Exact legacy wire format, macro rules, and canonical identity reference retained. |
| `packs/intseq/PACK.md` | preserved | [packs/intseq/PACK.md](../../packs/intseq/PACK.md) | normative semantics; runtime implementer. Seven primitives, exact integer and resource/evaluation policy unchanged. |
| `packs/intseq/TUTORIAL.md` | preserved | [packs/intseq/TUTORIAL.md](../../packs/intseq/TUTORIAL.md) | illustrative; program generator. Three examples and two counterexamples; no extra authority. |
| `research/EVALUATION.md` | moved-and-expanded | [docs/benchmarking/PROTOCOL.md](../benchmarking/PROTOCOL.md) | proposed experimental methodology; experiment operator. All baseline/split/budget/metric/failure/promotion ideas retained; separate repository-development pilots added. |
| `research/RELATED-WORK.md` | annotated | [research/RELATED-WORK.md](../../research/RELATED-WORK.md) | historical research notes; researcher. Bibliography retained; no new literature verification or priority claim. |
| `research/ROADMAP.md` | moved-and-revised | [docs/ROADMAP.md](../ROADMAP.md) | planned sequencing/research; maintainer. Original phases/open questions retained; explicit reference-extraction gate inserted before host work. |
| `research/THESIS.md` | annotated | [research/THESIS.md](../../research/THESIS.md) | research hypotheses; researcher. Full argument preserved behind route; not implementation authority. |
| `roles/PROGRAMMER.md` | preserved | [roles/PROGRAMMER.md](../../roles/PROGRAMMER.md) | procedural; solution generator. Frozen episode role; whole-file identity preserved for packet. Not the repository-coding role. |
| `roles/REVIEWER.md` | preserved | [roles/REVIEWER.md](../../roles/REVIEWER.md) | procedural; task-result reviewer. Evidence and failure review obligations retained. |
| `roles/SYNTHESIZER.md` | preserved | [roles/SYNTHESIZER.md](../../roles/SYNTHESIZER.md) | procedural; capsule designer. Adapt only when justified; no new trusted primitive authority. |
| `runtime/HOST.md` | annotated | [runtime/HOST.md](../../runtime/HOST.md) | intended architecture boundary; host implementer. Source-level reference capabilities vs unimplemented orchestration clarified; host obligations retained. |
| `runtime/REFERENCE.md` | wrapper-rewritten-source-preserved | [runtime/REFERENCE.md](../../runtime/REFERENCE.md), [docs/specs/001-intseq-reference.md](../specs/001-intseq-reference.md) | embedded executable reference; runtime implementer. Python fence byte-identical; claims attributed and extraction routed locally; actionable extraction spec added. |
| `templates/CAPSULE.md` | preserved | [templates/CAPSULE.md](../../templates/CAPSULE.md) | template; capsule author. Structured proposal fields retained without changing supported schema. |
| `templates/EXTENSION.md` | preserved | [templates/EXTENSION.md](../../templates/EXTENSION.md) | template; extension author. Evidence/semantics/implementation obligations for new authority retained. |
| `templates/RUN.md` | extended | [templates/RUN.md](../../templates/RUN.md) | template; operator/reviewer. Original record fields retained; development/benchmark provenance and custody extension added. |
| `templates/TASK.md` | preserved | [templates/TASK.md](../../templates/TASK.md) | template; task owner. Frozen requirement/oracle/budget fields retained. |

## Adopted changes, non-migrations, and uncertainties

Parallax replaces the project branding, not protocol semantics. No `arl-*` wire
identifier, primitive meaning, canonical capsule/program identity, or frozen task
was renamed. The old “every deliverable is Markdown” distribution rule is retired:
the project is now intended to acquire ordinary source/tests, and the bootstrap
includes only a documentation checker as executable tooling.

The old live MANIFEST is retired in favor of input provenance, Git identities,
and targeted integrity checks. The old README/startup duplication is replaced by
human entry plus a task router. Historical proof/benchmark/performance language is
not strengthened; imported source-reported results remain imported. No source
artifact is lost: even retired live presentations remain in the original ZIP.

Research claims and the related-work bibliography are preserved, not newly
validated. GPU work remains design-only. Licensing remains unselected; the archive
contains no license, and no BMAD license is transplanted to Parallax.

New artifacts fill missing engineering functions: project intent, architecture and
three ADRs, development/evidence guides, benchmark track separation, the bounded
first implementation spec, a reusable spec template, and this provenance/audit.
Their decisions are traceable to the source or explicitly identified bootstrap
choices. [BMAD-STUDY](BMAD-STUDY.md) pins the methodological reference; BMAD is
neither installed nor a runtime dependency. [BOOTSTRAP-AUDIT](BOOTSTRAP-AUDIT.md)
records actual checks and the GitHub publication blocker.
