# Project intent: high-agency engineering through better representations

Parallax investigates and builds **task-adaptive representations over stable,
checkable semantics**. Its purpose is not to generate miniature languages for
their own sake. Its purpose is to make strong coding models better at difficult
engineering: stronger first-pass reasoning, better architecture and algorithms,
more effective tool use, faster diagnosis, and higher-quality implementations.

The central hypothesis is that the interface presented to a model can materially
change the probability of a good solution. A typed API, schema, capsule, DSL,
intermediate representation, tutorial, example set, or generated helper is useful
when it exposes the right structure or compresses the search space. Ordinary code
or an existing library is better when it already does that job.

## Engineering objective

Optimize roughly for:

```text
first-pass correctness × technical leverage × solution quality × recoverability
---------------------------------------------------------------------------
ceremony + unnecessary context + needless handoffs + process latency
```

This is a design objective, not a benchmark formula. The concrete acceptance and
cost metrics for an experiment remain task-specific.

Parallax should make an agent better at:

- compressing a task into invariants, degrees of freedom, unknowns, and failure
  surface before coding;
- selecting architecture, algorithms, data structures, libraries, and
  representations that fit the real constraints;
- using compilers, debuggers, profilers, analyzers, search, reference paths,
  property checks, and benchmarks as information-producing instruments;
- separating semantic intent from backend schedule/implementation choices;
- diagnosing failures by competing hypotheses and discriminating experiments;
- reasoning about memory, I/O, concurrency, numerical behavior, and target
  performance when those actually matter;
- making reversible local decisions autonomously while escalating contract,
  security, compatibility, or irreversible architecture ambiguity;
- learning reusable abstractions without silently changing the task or trusted
  capability boundary.

## Hard boundaries

Capability does not require semantic looseness. Parallax keeps several invariants
because violating them makes engineering results untrustworthy:

1. The user's task and externally meaningful compatibility are not silently
   weakened to make a candidate pass.
2. Program/type/representation validity stays distinct from task acceptance.
3. Generated artifacts are data and cannot self-grant machine capabilities,
   redefine primitives, or choose their own final oracle.
4. Semantic identities are versioned deliberately when meaning changes.
5. Execution, test, benchmark, performance, and historical claims are never
   fabricated or strengthened beyond their evidence.
6. Security and host trust boundaries are concrete implementation concerns, not
   properties created by Markdown instructions.

Everything else should earn its complexity by increasing engineering capability.

## Product shape

The target system is a small set of composable capabilities rather than a large
workflow framework:

```text
Task contract / repository state
        -> problem model
        -> representation choice (direct | library | fixed | capsule)
        -> candidate program/code
        -> checker/compiler/tools/runtime
        -> execution observation
        -> external acceptance
        -> diagnosis, repair, reusable learning
```

A future host coordinates this loop, pins semantic/runtime dependencies, controls
capabilities and final-oracle access, and accounts for cost. Domain packs provide
stable meanings. Capsules are replaceable interfaces. Backends implement pack
semantics. Evidence records answer specific engineering questions.

See [ARCHITECTURE](architecture/ARCHITECTURE.md) for ownership and dependency
direction, and [PROTOCOL](../core/PROTOCOL.md) for the high-agency solving loop.

## Current repository state

Parallax is still a **pre-production research prototype**. Do not infer deployed
capability from the target design.

| Present now | Not present yet |
|---|---|
| Routed documentation, contracts, templates, examples, provenance | General orchestration host or model/provider integration |
| `intseq/0.1` semantic pack and artifact format | General multi-domain pack/runtime framework |
| Embedded standard-library Python intseq reference | Packaged intseq runtime until SPEC-001 is implemented |
| Public worked task/capsule/program and imported historical run report | Protected final benchmark oracle or completed LLM comparison |
| Documentation-integrity checker and tests | Production sandbox/capability system |
| [SPEC-001](specs/001-intseq-reference.md), ready for implementation | Native/GPU backend, solver/hole engine, proof integration |

The imported intseq test report has not become fresh execution evidence merely by
being present in the repository. The runtime extraction task should establish a
real executable foundation before host or benchmark claims advance.

## What success looks like

Near-term engineering success is a vertical slice in which a capable agent can:

1. understand a bounded real task and repository;
2. choose a direct or adapted interface for good technical reasons;
3. produce an implementation/program against pinned semantics;
4. use real tools to localize and repair failures;
5. obtain external task acceptance with calibrated evidence;
6. retain enough signal to improve future representation choices.

Research success is a defensible positive, negative, or conditional result about
when representation adaptation beats strong direct/library/fixed-interface
baselines at comparable total cost. A negative result is useful if it reveals
that the better interface was a familiar library, stronger contract, or simpler
architecture.

## Non-goals

Parallax is not trying to become a universal IR, a general-purpose programming
language, a mandatory multi-agent workflow, a test-count maximizer, or a system
that replaces domain semantics with one abstract graph. It does not claim universal
correctness proofs, production isolation, GPU performance, autonomous semantic
extension, or research novelty that has not been demonstrated.

Project licensing remains an owner decision; public visibility does not imply a
license.
