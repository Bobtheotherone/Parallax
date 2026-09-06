# Project intent

**Consumer:** people setting scope and agents writing implementation specifications.
**Authority:** what Parallax is trying to provide and the bootstrap maturity baseline.
Detailed semantics belong to `core/` and the selected pack; implementation work
belongs to a spec. This is not a list of software already delivered.

## Problem and mission

An LLM's programming interface can be poorly matched to a task: too much irrelevant
surface area, too little useful structure, or abstractions whose meaning is hard
to check. Inventing an interface can also cost more than solving the task directly,
or hide algorithmic work inside a macro.

Parallax's mission is to make **task-adaptive representations over stable,
checkable semantics** practical to investigate. The product should make a direct
solution, a restricted interface, and a compositional capsule comparable without
letting the generator redefine success. Better outcomes are a hypothesis, not a
requirement assumed to have been met.

Primary users are engineering researchers running controlled experiments and
coding agents implementing the checker/runtime/host that those experiments need.
There is no validated market or end-user adoption claim.

## Present scope and state

| Item | Bootstrap state |
|---|---|
| Routed documentation, semantic contracts, examples, templates | Present |
| `intseq/0.1` primitives, artifact schema, embedded Python reference | Present in Markdown; not a packaged runtime |
| Public reference test report | Imported from the archive; not independently rerun here |
| Documentation-integrity tooling | Present; results and limitations in the [audit](provenance/BOOTSTRAP-AUDIT.md) |
| First runtime engineering task | [SPEC-001](specs/001-intseq-reference.md); consult its frontmatter for lifecycle state |
| Host orchestration, model calls, budget enforcement, isolated final oracle | Not implemented |
| LLM development trials or adaptive-representation comparisons | Not yet benchmarked |
| Native/GPU backend, hole solver, proof integration | Design-only or later research |

This table is a baseline, not a live capability registry. Update it only when a
completed change has evidence. A referenced protocol is not an implemented host.

## Target capabilities

| ID | Externally meaningful capability | Success condition |
|---|---|---|
| P1 | Bind work to a frozen task and semantic environment | An evaluator can reconstruct the contract, pack, implementation, and policy used, including revisions and failures |
| P2 | Check and evaluate supported data artifacts | A user can distinguish malformed, inadmissible, resource-rejected, and evaluated artifacts without treating evaluation as task acceptance |
| P3 | Keep execution and acceptance outside generated authority | Generated artifacts cannot add primitives, permissions, or an oracle merely by describing them |
| P4 | Run bounded, auditable attempts with a direct fallback | Actual attempts, diagnostics, resource spending, and terminal outcomes are retained; budget exhaustion is visible |
| P5 | Compare methods fairly | Direct/library/fixed-interface/adaptive arms receive declared comparable resources and independent task acceptance under a predeclared protocol |
| P6 | Extend domains without erasing old meaning | A separately reviewed extension records semantics, implementation, tests, resource policy, and compatibility consequences |

P1–P6 describe intended capabilities, not a mandate to implement all of them in
one episode. SPEC-001 addresses the smallest part of P2 and establishes a public
conformance baseline; it does not deliver P4 or P5.

## Success and non-goals

The first engineering success is a reproducible, testable runtime extraction that
preserves the reference's observable contract. The next is an actual host that
records costs and failures. Research success is a defensible result—positive,
negative, or inconclusive—about adaptation under named conditions. Promotion of
adaptation requires reproducible benefit or explicitly valued auditability at an
accepted cost; “more type-correct outputs” alone is insufficient.

Near-term non-goals are a universal IR, a new general-purpose language, native
code generation, GPUs, autonomous invention of semantic primitives, training a
model, production sandboxing, universal correctness proofs, and claims about
cryptographic, driver, or distributed-system safety.

There is no requirement that every task use a capsule or that experiments favor
adaptation. Project licensing remains an owner decision; no license is inferred
from the archive or from studying another project.
