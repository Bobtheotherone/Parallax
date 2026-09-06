# Roadmap and exit gates

**Consumer:** whoever selects the next implementation/research task. This is
sequencing, not implementation evidence. There are no promised delivery dates.
Current capability state is in [PROJECT](PROJECT.md); a selected spec owns its status.

| Stage | Work | Exit gate |
|---|---|---|
| 0 — Routed research baseline | Preserve semantics, distinguish evidence, prepare a bounded coding handoff | Context/identity audit plus a genuine implementation-ready spec; not an LLM-runtime validation |
| 0→1 — Executable project foundation | [SPEC-001](specs/001-intseq-reference.md): package and characterize existing intseq reference | Its acceptance checks and review completed with fresh recorded evidence |
| 1 — One actual agent loop | Host minimal context, one specified model, artifact checks, diagnostic routing, task-domain/oracle boundary, budgets, retained failures/costs | Reproducible bounded runs and honest failure handling; no automatic claim of benefit |
| 2 — Economic evidence | Matched direct/library/fixed-DSL/adaptive study with cold/warm accounting | Reproducible results under the [benchmark protocol](benchmarking/PROTOCOL.md), including negative outcomes; promotion only under declared criteria |
| 3 — Controlled extension | One richer domain/backend with explicit semantics and reference behavior; optional bounded hole search | Independently reviewed extension, regression evidence, per-candidate accounting, preserved old meanings |
| 4 — Richer domains and model conditioning | Syntax/tutorial experiments, learned selection, semantic/schedule separation, useful proof integration | Positive evidence for prerequisites; new domain-specific acceptance and backend evidence |

The source archive's Phase 0 gate included a fresh agent generating a valid
capsule/program and running it. That experiment remains **unperformed by this
bootstrap**. The new 0→1 extraction gate is inserted before host work rather than
pretending a Markdown reference is a packaged project.

The first coding episode can be observed as a public development pilot. It is
not a final held-out benchmark and does not test whether adaptive representations
improve task solving. A working host and an executed matched-budget study are
separate later gates.

Do not promote adaptation just because a type-error rate falls. Require advantage
over competitive direct/library approaches, or explicitly valued auditability at
an accepted extra cost. State the reuse/amortization horizon. Model, decoder,
backend, or semantic changes require reevaluation.

## Open questions and when they matter

| Question | Resolve before |
|---|---|
| Which provider, budgeting API, storage, isolation, and oracle custody? | A host-loop implementation spec |
| Which task families and statistical precision are meaningful? | A confirmatory preregistration |
| What gain is representation rather than extra inference/scaffolding? | Interpreting comparative results; preserve ablations |
| How much context/tutorial is sufficient for each model? | Claiming acquisition efficiency or learned profiles |
| When do macro libraries amortize, and which implementation families survive selection? | Promoting reuse or strategy-diversity claims |
| Which properties are construction guarantees and which remain empirical? | Adopting a richer pack or backend |
| How should success estimates transfer across models/backends? | Reusing prior empirical estimates |
| What license should govern the project and imported materials? | Owner's distribution/licensing decision |

None of these authorizes GPU/native/compiler work in SPEC-001. The GPU RMSNorm
note remains a [design critique](../packs/gpu/RMSNORM.md). Cryptographic code,
device drivers, and distributed systems are not early demonstrations of guarantees
this prototype has not established.
