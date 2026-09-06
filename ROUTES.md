# Context router

Load the selected row and the explicit dependencies it names. Reuse unchanged
context by identity; do not recursively follow every reference. A file's presence
does not make it applicable. For cross-cutting work, take the union of necessary
rows and state why.

| Activity | Minimum reading, in order | Do not load by default |
|---|---|---|
| First implementation | [SPEC-001](docs/specs/001-intseq-reference.md), its context list, [workflow](docs/development/WORKFLOW.md) | Thesis, GPU, BMAD study, other roles |
| Implement another approved spec | Named spec, its authority/context links, [workflow](docs/development/WORKFLOW.md), touched code | Entire backlog/research corpus |
| Review implementation | Spec, diff, exact verification record, [verification](docs/development/VERIFICATION.md) | Unrelated examples; author self-review as truth |
| Understand project/architecture | [Intent](docs/PROJECT.md), [architecture](docs/architecture/ARCHITECTURE.md); ADR only for relevant rationale | Whole reference implementation |
| Choose adaptation | [Contract](core/CONTRACT.md), [economics](core/ECONOMICS.md), [task template](templates/TASK.md) | Research history |
| Construct capsule | [Synthesizer](roles/SYNTHESIZER.md), [capsule rules](core/CAPSULE.md), selected pack and schema | Other domain packs, final evaluation oracle |
| Generate program | [Programmer](roles/PROGRAMMER.md), frozen task + capsule, selected pack/tutorial | Oracle implementation, rejected capsules, research |
| Review task result | [Reviewer](roles/REVIEWER.md), [evidence](core/EVIDENCE.md), frozen task and run record | Unrelated cases |
| Diagnose task-run failure | [Protocol](core/PROTOCOL.md), exact diagnostic, relevant operation | Whole attempt history |
| Add primitive/backend | [Evolution](core/EVOLUTION.md), [semantics](core/SEMANTICS.md), [host](runtime/HOST.md), architecture, a new approved spec | Permission to extend from a generated capsule |
| Reproduce embedded reference | [Reference](runtime/REFERENCE.md), [task](examples/intseq/TASK.md), [capsule](examples/intseq/CAPSULE.md), [program](examples/intseq/PROGRAM.md), [imported evidence](examples/intseq/EVIDENCE.md) | GPU |
| Study GPU proposal | [RMSNorm design case](packs/gpu/RMSNORM.md), semantics and host boundary | Any assumption of a supported GPU pack |
| Run an experiment | [Benchmark protocol](docs/benchmarking/PROTOCOL.md), relevant frozen task/spec, [run template](templates/RUN.md) | Final oracles in agent context |
| Research | [Thesis](research/THESIS.md), [related work](research/RELATED-WORK.md), benchmark protocol, [roadmap](docs/ROADMAP.md) | Automatic execution action |
| Maintain documentation/provenance | Authority map, [source map](docs/provenance/SOURCE-MAP.md), touched sources, [audit](docs/provenance/BOOTSTRAP-AUDIT.md) | BMAD unless reviewing methodological influence |

## Packet assembly boundary

For solution generation, always include frozen task semantics, capsule identity,
permitted operations with their preconditions, and the output shape. Do not save
context by dropping meaning. Tutorials supplement rather than replace semantics.

The v0.1 capsule is small enough to include whole. For future larger packs,
include the transitive closure of used definitions under stable IDs. Exact-content
caching is a host responsibility. Prompt bytes and provider token usage are
separate measurements; no tokenizer-independent optimum is asserted.

[The frozen example packet](examples/intseq/PACKET.md) is a derived one-call view,
not a second specification. Its listed whole-file hashes still bind the preserved
sources. The embedded interpreter neither builds nor freshness-checks packets.
The doc checker can check this one packet's identities; that is not a runtime
context-assembly service.
