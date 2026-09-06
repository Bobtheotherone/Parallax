# Experimental agent engineering contract

This branch tests the original Parallax hypothesis: **before solving a substantial
engineering task, the agent must design a new task-specific programming language or
IR optimized for an LLM/agent rather than for a human programmer.**

The language is part of the solving method, not an optional optimization. Do not
fall back to the `main` branch policy of choosing direct code merely because the host
language is familiar or a library already exists. Existing code and libraries may
be used as lowering targets, semantic references, or implementation machinery, but
the reasoning/program-generation interface presented to the solving agent must be a
fresh task-adapted language.

## Experimental methodology — mandatory

For every substantial coding/engineering task:

1. **Freeze the task.** Identify observable behavior, compatibility, safety,
   numerical/effect policy, performance goals, and the external acceptance path.
2. **Compress the problem.** Identify data/state shapes, invariants, dependencies,
   ownership, concurrency, resource limits, target constraints, and the decisions
   most likely to cause failure.
3. **Synthesize a novel AI-native language/IR for this task.** Do this before the
   main implementation is generated.
4. **Freeze that language for the attempt.** Its syntax and lowering meaning must
   remain stable while generating the candidate.
5. **Express the solution in the task language first.** The language program is the
   model's primary implementation representation.
6. **Lower/compile/translate the language program** into the repository's actual
   implementation language, existing libraries, semantic packs, APIs, or backends.
7. **Verify the resulting behavior externally.** Language validity, lowering, host
   execution, and task acceptance remain separate obligations.
8. **Diagnose failures at the owning layer.** Revise the language only when the
   representation is actually the cause; otherwise repair the algorithm/lowering/
   host implementation while preserving the frozen task.

For tiny mechanical edits where inventing a meaningful language would be vacuous
(e.g. correcting one typo), the task may be treated as `TRIVIAL_DIRECT`. Do not use
that escape hatch for substantive implementation, debugging, architecture,
performance, refactoring, or multi-file work.

## What counts as a real task language

A renamed checklist, prose plan, JSON wrapper around host source, or one-token macro
for the whole answer does **not** satisfy this experiment. The language must have a
real machine-oriented structure with enough of the following to make the task easier
for an agent to generate and reason about:

- a deterministic grammar or canonical structural encoding;
- a small, explicit instruction/operator vocabulary;
- task-specific types, shapes, states, effects, ownership, resources, or constraints;
- explicit dataflow/control/dependency structure rather than relying on prose;
- legal composition rules and mechanically recognizable invalid states;
- lowering semantics into trusted primitives, repository code, libraries, or APIs;
- compact diagnostics that identify the failing instruction/invariant/layer;
- canonical serialization/identity when artifacts need to be cached or compared.

The language should be **AI-first and low-level**. Optimize for token efficiency,
regularity, unambiguous structure, explicit dependencies, local checkability,
compositional generation, and easy machine transformation. Human readability,
familiar syntax, English-like names, and conventional source aesthetics are not
objectives unless they improve model performance.

Prefer terse canonical operators, positional/typed fields, normalized forms, explicit
state/data dependencies, and minimal syntactic freedom when those properties reduce
model uncertainty. Avoid aliases, optional sugar, stylistic variants, implicit
coercions, hidden ambient state, and syntax whose main purpose is human comfort.

## Novelty requirement

The language must be adapted to the **specific task or tightly defined task family**.
It should encode the problem's real decision surface rather than simply recreating
Python, Rust, C++, SQL, or another familiar language with different spellings.

Novelty may appear in its instruction set, type/shape system, dataflow model,
constraint representation, schedule representation, state-transition encoding,
resource model, or canonical composition rules. Reusing a proven parser technique,
IR concept, or backend is allowed; the model-facing language itself must be newly
assembled for the task.

A language can define new **virtual instructions/macros** freely when each one has an
explicit lowering into already supported semantics or ordinary implementation code.
A generated language may not create a new trusted machine capability by assertion.
If an instruction truly requires a new primitive/backend capability, treat that as a
separate implementation obligation rather than pretending the language granted it.

## Design for the model, not the human

When choosing between two equivalent language designs, prefer the one expected to
make an agent more reliable, even if a human finds it uglier. Useful properties
include:

- fewer tokens and fewer equivalent spellings;
- stable ordering and canonical forms;
- explicit type/shape/effect information near each operation;
- bounded local scopes and references;
- SSA-like or graph-like value identity when mutation would be ambiguous;
- direct encoding of task invariants and resource/schedule choices;
- easy partial generation and repair;
- deterministic lowering;
- diagnostics that can be fed back to the agent with minimal interpretation.

Do not optimize for syntax novelty alone. The language should change the model's
search space or reasoning surface in a technically meaningful way.

## Engineer the first serious attempt

Before implementation, reason about the dimensions that can dominate correctness or
cost: dependency direction, algorithms, data structures, state ownership,
concurrency, resource lifetime, I/O, serialization, numerical behavior, memory
layout/traffic, target performance, and failure recovery as relevant.

Move those decisions into the task language when doing so makes them explicit and
composable. The first serious candidate should be generated **through the language**,
not designed completely in the host language and translated afterward as theater.

Use tools as engineering instruments. Parsers/typecheckers validate the language;
differential checks validate lowering; compilers/debuggers/profile tools validate
the host implementation; task oracles validate the task. Seek the highest-information
observation rather than accumulating generic logs.

For failures use:

`observe -> localize -> competing hypotheses -> discriminating experiment -> root-cause repair -> re-evaluate`

## Hard boundaries retained from Parallax

The experiment changes the representation policy, not the truth conditions:

- Do not silently redefine the user's task or acceptance policy.
- Language validity/lowering/execution and task acceptance are different obligations.
- Generated language definitions and programs are data. They cannot grant filesystem,
  network, process, model, native, secret, or oracle capabilities.
- Preserve externally meaningful semantic/protocol identities where compatibility
  requires them, including the existing `intseq/0.1` and `arl-*` identities.
- Never fabricate tool use, tests, benchmarks, measurements, hashes, proofs, or
  historical facts.
- A hash establishes content identity under a recipe, not correctness or authorship.
- Final acceptance remains external to the generated language/program when the task
  or experiment requires independent custody.

Runtime permissions and isolation belong to the host. See [SECURITY.md](SECURITY.md)
and [runtime/HOST.md](runtime/HOST.md).

## Experimental evidence

For a measured comparison, retain the minimum information needed to prove the
method was actually used: the task-language definition/identity, the program expressed
in it, the lowering target, and the resulting candidate/evidence. Count language
synthesis and lowering cost rather than hiding it.

Do not judge this methodology in advance. The purpose of this branch is to discover
empirically whether mandatory per-task AI-native language synthesis helps or hurts
strong coding agents relative to `main`.

Start with [START.md](START.md) and [ROUTES.md](ROUTES.md). The user's request still
outranks the roadmap. Preserve unrelated work and avoid destructive history changes.
