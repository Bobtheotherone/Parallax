# Project intent: AI-native languages for difficult engineering

This branch investigates a deliberately stronger version of the Parallax hypothesis:
**a coding agent should synthesize a new low-level programming language or IR for the
specific engineering task before generating the implementation.**

The generated language is optimized for LLM/agent operation rather than for human
source-code ergonomics. It should compress the task's search space, encode important
invariants and dependencies explicitly, reduce ambiguous equivalent spellings, and
provide a deterministic bridge into ordinary implementation code or trusted semantic
machinery.

This methodology is mandatory on `experimental` except for trivial mechanical edits.
The `main` branch remains the control methodology where direct code, libraries, fixed
interfaces, capsules, and language synthesis compete adaptively.

## Experimental hypothesis

For a fixed model, task, tools, acceptance policy, and total budget, mandatory
per-task AI-native language synthesis may improve difficult engineering by giving the
model a representation better matched to its own generation and reasoning behavior
than human-designed general-purpose languages.

The mechanism being tested is not “novel syntax is good.” The proposed mechanism is:

```text
problem structure
  -> task-specific typed/structured language
  -> smaller and more explicit model decision surface
  -> stronger first serious program
  -> deterministic lowering into real implementation machinery
  -> better accepted engineering result
```

The hypothesis is allowed to fail. Language design and lowering cost count against
the method.

## What the task language optimizes

A good experimental language should favor properties useful to a model/agent:

- canonical, deterministic serialization;
- a small task-specific operator vocabulary;
- explicit values, dependencies, types, shapes, states, effects, ownership,
  resources, or schedules where relevant;
- minimal syntactic sugar, aliases, implicit coercion, and ambient state;
- local structural validity and easy partial repair;
- compact machine-facing diagnostics;
- straightforward lowering to repository code, libraries, APIs, semantic packs, or
  backends;
- enough low-level control to expose the engineering choices that matter without
  importing irrelevant general-purpose language surface.

The surface may be bytecode-like, graph-like, SSA-like, constraint-oriented,
stack/register-oriented, declarative, or another form. Human familiarity is not a
promotion criterion.

A language that simply renames host-language constructs or hides the entire solution
behind one macro does not satisfy the experimental treatment.

## Engineering objective

Optimize roughly for:

```text
first-pass correctness × technical leverage × solution quality × recoverability
---------------------------------------------------------------------------
language synthesis + lowering + search + tooling + verification + execution cost
```

This is a design aid, not the benchmark formula. The treatment is interesting only
if the language changes engineering outcomes enough to justify its full cost.

The branch should make an agent better at:

- compressing difficult tasks into explicit machine-representable invariants;
- inventing instruction sets and composition rules matched to the task;
- representing algorithms, dataflow, state machines, ownership, concurrency,
  numerical policy, memory/schedule decisions, or constraints in forms that are
  easy for an LLM to manipulate;
- generating a serious solution in that task language before host code exists;
- lowering the task program faithfully into real repository code;
- using parsers/checkers/compilers/debuggers/profilers/reference paths as
  discriminating instruments;
- localizing failure to language acquisition, algorithm, lowering, implementation,
  resource behavior, or external task acceptance.

## Hard boundaries

The experimental representation policy does not weaken correctness:

1. The user's task and externally meaningful compatibility are not silently changed.
2. Language/program validity stays distinct from task acceptance.
3. Generated languages and programs are data and cannot self-grant machine
   capabilities, secrets, native operations, or oracle access.
4. New virtual instructions must lower to supported meaning; genuinely new trusted
   primitives/backends remain explicit implementation work.
5. Published semantic identities are versioned deliberately when meaning changes.
6. Execution, test, benchmark, performance, and historical claims are never
   fabricated or overstated.
7. Security and host isolation remain implementation concerns, not properties
   created by a language definition.

Everything else may be redesigned to improve the experimental language method.

## Product shape

```text
Task contract / repository state
        -> compressed problem model
        -> NEW task-specific AI-native language / IR
        -> frozen grammar + semantics + lowering
        -> task-language program
        -> parser/checker/lowerer
        -> ordinary repository implementation / trusted backend
        -> execution observation
        -> external acceptance
        -> diagnosis and language/algorithm learning
```

The task language may be ephemeral for one task or reusable for a tightly related
family. Reuse is an empirical outcome, not a requirement.

## Current repository state

Parallax is still a **pre-production research prototype**. This branch specifies and
enforces the experimental agent methodology; it does not claim that a universal
language-synthesis host/compiler is already implemented.

| Present now | Not present yet |
|---|---|
| Experimental methodology in agent/core/role docs | General automated language-synthesis host |
| Task/semantic/capsule/evidence architecture | Universal parser/compiler generator |
| `intseq/0.1` semantic pack and artifact example | General multi-domain task-language runtime |
| Embedded Python intseq reference | Packaged intseq runtime until SPEC-001 is implemented |
| Documentation-integrity checker/tests | Production sandbox/capability system |
| Benchmark methodology | Completed `main` vs `experimental` LLM comparison |

The existing intseq format is a compatibility example. Experimental task languages
may be much richer as long as their lowering and authority boundaries are explicit.

## What success looks like

For a substantial task, an experimental agent should:

1. freeze the real task;
2. design a novel AI-native language that exposes the task's difficult decisions;
3. express the solution in that language;
4. lower it into a real implementation;
5. use tools to validate language/lowering/implementation boundaries;
6. obtain external task acceptance;
7. retain enough information to compare the method fairly with `main`.

Research success is a defensible result about whether mandatory AI-native language
synthesis improves accepted-solution probability, first-pass quality, difficult-task
capability, repairability, implementation quality, or performance at comparable full
cost. A negative or conditional result is equally valid.

## Non-goals

The generated language is not allowed to redefine the task, manufacture trusted
capabilities, bypass host security, own its final oracle, or create evidence by
assertion. The experiment is not a contest for prettiest syntax, maximum language
complexity, maximum test count, or shortest final host code.

Project licensing remains an owner decision; public visibility does not imply a
license.

See [AGENTS](../AGENTS.md), [CAPSULE](../core/CAPSULE.md),
[PROTOCOL](../core/PROTOCOL.md), and the
[benchmark protocol](benchmarking/PROTOCOL.md).
