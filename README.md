# Parallax — experimental language-synthesis branch

**Design the language for the task, then solve the task through that language.**

This branch tests the original Parallax idea: for every substantial engineering
task, the coding agent first invents a **new task-specific programming language or
IR optimized for LLM/agent cognition**, expresses the solution in that language,
and then lowers it into ordinary repository code, libraries, APIs, or trusted
backends.

The language is intentionally not optimized for human friendliness. It should be
compact, canonical, structurally regular, explicit about dependencies and
constraints, and easy for a model to generate, check, transform, and repair.

This is an experiment. The repository does not assume the methodology is superior;
it exists to test that question against the adaptive control methodology on
`main`.

## The experimental mechanism

```text
frozen task + external acceptance
          |
          v
compress task / failure surface
          |
          v
synthesize NEW AI-native task language / IR
          |
          v
freeze grammar + types + instructions + lowering
          |
          v
generate program in that language
          |
          v
parse / check / lower / translate
          |
          v
ordinary code / library calls / trusted semantic IR
          |
          v
execute / build / integrate
          |
          v
external task acceptance
```

The language is the model's **primary problem-solving representation**, not a
post-hoc transcription of a solution already designed in Python, Rust, C++, or
another host language.

## What the generated language should look like

A valid experimental language should provide a real machine-oriented representation,
not just renamed host syntax. Depending on the task it may include:

- a deterministic grammar or canonical structured encoding;
- a small task-specific instruction set;
- explicit types, shapes, states, ownership, effects, resources, schedules, or
  constraints;
- explicit dataflow/control/dependency edges;
- one canonical spelling for equivalent structures where practical;
- local legality rules that make invalid states easy to reject;
- deterministic lowering into supported repository code, APIs, libraries, semantic
  packs, or backends;
- terse diagnostics that identify the failing instruction or invariant.

Human readability is secondary. The preferred surface may resemble a compact typed
IR, SSA, graph serialization, bytecode-like instruction stream, constraint language,
or another representation that would be unpleasant to hand-author but efficient for
a model.

The design should minimize aliases, syntactic sugar, implicit coercions, ambient
state, and stylistic freedom. Novelty must be technically meaningful: the language
should encode the task's actual decision surface, not merely rename Python tokens.

## Meaning remains fixed

Language invention does **not** authorize task invention.

Parallax retains these boundaries:

- the user's requested behavior and final acceptance policy remain external;
- generated language definitions/programs are data, not machine authority;
- a virtual instruction must lower to supported semantics or create an explicit
  implementation obligation;
- language validity, lowering correctness, execution, and task correctness are
  separate questions;
- existing compatibility identities such as `intseq/0.1`, `arl-capsule/0.1`, and
  `arl-program/0.1` are not silently redefined;
- tool, benchmark, execution, and historical evidence is never fabricated.

A new language may contain task-specific virtual instructions/macros, but declaring
an instruction does not magically create a filesystem permission, GPU primitive,
network operation, compiler backend, or oracle.

## Why compare this with `main`?

`main` uses adaptive Parallax: direct code, existing libraries, fixed interfaces,
capsules, and new languages compete on engineering value and cost.

`experimental` intentionally removes that choice. Except for trivial mechanical
edits, **language synthesis is mandatory**. This lets experiments ask a clean
question:

> Does forcing a strong coding model to invent and use a low-level AI-native
> task language improve first-pass correctness, architecture, difficult-task
> capability, performance reasoning, repairability, or total accepted-solution cost?

Language-design and lowering cost must be counted. A result is interesting whether
this treatment wins, loses, or helps only on particular task families.

## Current repository

Parallax remains a **pre-production research prototype**. The experimental branch
changes the agent methodology and design documents; it does not pretend a general
language-synthesis host/compiler already exists.

Present today:

- the task/semantic/capsule/evidence model and architecture;
- this branch's mandatory AI-native language-synthesis method;
- the stable `intseq/0.1` example pack and legacy `arl-*` artifact formats;
- an embedded Python intseq reference implementation in
  [runtime/REFERENCE.md](runtime/REFERENCE.md);
- worked examples and documentation-integrity tooling;
- [SPEC-001](docs/specs/001-intseq-reference.md), still a prepared implementation
  contract rather than evidence of a packaged general runtime.

The existing intseq capsule is a compatibility example, not the upper bound on what
an experimental task language may look like.

## A small example with a large lesson

The worked intseq task sums `3*v + 5` only for values that were nonnegative **before**
the transformation. A task language for this case could make provenance/order an
explicit dataflow property so the model cannot casually collapse:

```text
FILTER(original >= 0) -> AFFINE(3,5) -> REDUCE_SUM
```

into the different computation:

```text
AFFINE(3,5) -> FILTER(result >= 0) -> REDUCE_SUM
```

Both can be structurally legal while only the first satisfies the task. This is why
external task acceptance remains separate even when the generated language makes
important invariants more explicit.

## Navigate

- **Experimental agent contract:** [AGENTS.md](AGENTS.md)
- **Start experimental work:** [START.md](START.md)
- **Select context:** [ROUTES.md](ROUTES.md)
- **Project intent:** [docs/PROJECT.md](docs/PROJECT.md)
- **Task-language/capsule design:** [core/CAPSULE.md](core/CAPSULE.md)
- **Synthesis loop:** [core/PROTOCOL.md](core/PROTOCOL.md)
- **Language synthesizer:** [roles/SYNTHESIZER.md](roles/SYNTHESIZER.md)
- **Program generator:** [roles/PROGRAMMER.md](roles/PROGRAMMER.md)
- **Matched comparison:** [docs/benchmarking/PROTOCOL.md](docs/benchmarking/PROTOCOL.md)
- **System boundaries:** [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)
- **Security/trust model:** [SECURITY.md](SECURITY.md)

`python tools/check_docs.py` checks repository/document identities and structure. It
is not a general compiler for newly synthesized task languages and does not establish
task correctness.

No project license has been selected.
