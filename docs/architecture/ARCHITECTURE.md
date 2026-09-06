# Architecture: stable meaning, adaptive interface

**Consumer:** implementers and reviewers. **Status:** adopted design boundaries;
only the embedded intseq reference currently supplies product implementation code.
This document describes intended responsibilities, not deployed components.

## Information and authority flow

```text
requirement owner -> frozen task + acceptance policy -----------+
                                                               v
external host -> pinned capabilities + budget -> generator -> capsule/program DATA
      |                                                        |
      |                             parser -> admission/type checker
      |                                                        |
      |                           hygienic expansion -> primitive IR
      |                                                        |
      |                           pinned interpreter/backend -> result
      |                                                        |
      +-> external task oracle + task-domain enforcement <------+
      +-> evidence, diagnostics, cost ledger -> next bounded step
```

The task oracle does not derive expected answers from the generated capsule.
Only public diagnostics allowed by the experiment may return to the generator.
A checked lowering and a task-acceptable result remain distinct outputs.

## Components and dependency direction

| Component | Owns | Does not own |
|---|---|---|
| Task contract and owner | Intended observations, input domain, error/numerical policy, acceptance policy, approved revisions | Convenient reinterpretations by implementation |
| Semantic pack | Stable operation IDs, types, mathematical behavior, reference resource policy | A universal semantics for other domains |
| Capsule/program data | Selection of existing operations and typed compositional macros; capsule identity binding | Executable source, arbitrary privileges, new primitive authority |
| Parser/checker/expander | Document/schema admission, signatures/scope, bounded hygienic lowering, recheck of primitive IR | Whether the requested algorithm is correct |
| Interpreter/backend | Defined primitive behavior under its pinned resource/numerical policy | Task intent, LLM search, acceptance policy |
| Host (not implemented) | Trusted pack/backend selection, file/tool capabilities, task-domain enforcement, budgets, context routing, oracle access, evidence retention | Delegation of its authority to generated data |
| External acceptance mechanism | Expected observations under the frozen task | Merely reproducing the candidate's own computation |

The initial runtime is a local standard-library Python package, specified by
[SPEC-001](../specs/001-intseq-reference.md), extracted from the reference rather
than a redesign. Its evaluator must not depend on an LLM provider, task-specific
oracle, research document, or orchestration framework. The CLI is an adapter
around the semantic library; public self-test logic is separate from evaluation.
There is no package publishing/build backend decision in this first slice.

For intseq, the stable IR is a typed tree of seven primitives, not a native
compiler IR. Future domains must define their own observations, numerical
relations, effects, and dependency boundaries before sharing any container.

## Trust boundary and resource policy

Trusted implementation includes parser, checker, expander, evaluator, Python,
and the operating environment. A data-only AST narrows authority; it does not
prove absence of implementation defects or provide process isolation. The
reference CLI reads caller-selected local paths. Its integer/work/node limits
are not an operating-system sandbox or a hard wall-clock guarantee.

A host for hostile workloads must separately control process lifetime, filesystem,
network, native adapters, and final-oracle access. [HOST.md](../../runtime/HOST.md)
owns that integration boundary. Those controls are not supplied by `AGENTS.md`,
JSON fields, or a Markdown route.

Pack and runtime identities are pinned separately from canonical capsule JSON.
A human-readable ID such as `intseq/0.1` is not by itself a content pin. Frozen
artifacts remain reconstructible; a changed meaning requires a versioned decision.
Legacy `arl-capsule/0.1` and `arl-program/0.1` retain their exact spellings.

## Source-of-truth map

| Question | Authoritative home |
|---|---|
| What and why; maturity baseline | [PROJECT](../PROJECT.md) |
| Universal agent constraints | [AGENTS](../../AGENTS.md) |
| What to read next | [START](../../START.md) and [ROUTES](../../ROUTES.md) |
| Current design shape | This document; [ADRs](decisions/README.md) preserve rationale |
| Task semantics, freeze, oracle separation | [CONTRACT](../../core/CONTRACT.md) |
| Representation preservation and observations | [SEMANTICS](../../core/SEMANTICS.md) |
| General capsules and identity | [CAPSULE](../../core/CAPSULE.md) |
| intseq operations, syntax, resource behavior | [PACK](../../packs/intseq/PACK.md) and [formats](../../packs/intseq/CAPSULE.md) |
| Canonical JSON byte recipe for v0.1 | `canonical`/`digest` in [REFERENCE](../../runtime/REFERENCE.md), adopted by the formats document |
| Synthesis states, diagnostics, revision policy | [PROTOCOL](../../core/PROTOCOL.md) |
| Extension classes and retirement | [EVOLUTION](../../core/EVOLUTION.md) |
| What evidence establishes | [EVIDENCE](../../core/EVIDENCE.md); [verification guide](../development/VERIFICATION.md) applies it to development |
| Cost model and experiments | [ECONOMICS](../../core/ECONOMICS.md); [benchmark protocol](../benchmarking/PROTOCOL.md) defines comparisons |
| Implementation scope, acceptance, lifecycle | The selected file in `docs/specs/`; [workflow](../development/WORKFLOW.md) defines transitions |
| Migration history | [SOURCE-MAP](../provenance/SOURCE-MAP.md), not a second semantics |

README is a summary. Tutorials and packets are derived views. Templates are
construction aids, not new rules. Research notes, GPU proposals, historical run
reports, and BMAD material cannot override this authority map. Cross-document
contradictions require an explicit repair at the owning source, not last-read wins.

## Decisions and deliberate openings

Three adopted decisions preserve the archive's architecture:
[stable semantic packs](decisions/0001-stable-semantics.md),
[data without authority](decisions/0002-data-not-authority.md), and
[separate acceptance obligations](decisions/0003-independent-task-acceptance.md).
They are design decisions, not proof that an implementation enforces them.

Open host choices include model/provider adapters, durable run storage, isolation,
concurrency, final-oracle custody, and budget instrumentation. Open research
choices include task families, reuse horizons, syntax/tutorial variants, finite
holes, and richer backends. None blocks the bounded intseq extraction. A future
spec or RFC should resolve one consequential opening only when work depends on it.
