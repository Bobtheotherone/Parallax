# Experimental high-agency language-synthesis protocol

This branch tests a specific causal treatment: a substantial engineering task is not
implemented directly in the host language. The agent first synthesizes a new
AI-native task language/IR, solves the task in that representation, and lowers the
result into real implementation machinery.

This is a decision loop, not a reporting ritual. The language is mandatory; ceremony
is not.

## The loop

```text
frozen task
   -> compress problem and failure surface
   -> synthesize task-specific AI-native language L
   -> freeze L: grammar/types/instructions/lowering
   -> generate one serious program p in L
   -> check p and lower it to repository code / trusted semantics
   -> use tools to discriminate likely failures
   -> repair algorithm/lowering/implementation, or revise L between attempts
   -> external task acceptance
   -> retain only evidence needed to compare the method
```

For substantive work the normal route is `LANGUAGE`. `TRIVIAL_DIRECT` is reserved
for genuinely mechanical edits with no meaningful design/algorithmic decision.
`DESIGN_ONLY` applies when required meaning, implementation capability, permission,
or acceptance machinery cannot honestly be supplied.

Do not substitute `DIRECT` merely because a host language or library is familiar.
Those are lowering targets in this treatment arm.

## First serious attempt

Before inventing the language, establish:

- hard contract invariants and external acceptance mechanism;
- current repository architecture and lowering targets;
- data shapes/state transitions/ownership/effects;
- algorithm families and complexity constraints;
- numerical, concurrency, memory, I/O, protocol, and resource behavior as relevant;
- likely model failure modes in the ordinary host representation;
- the low-level decisions the new language should expose explicitly;
- which tools can answer high-risk unknowns cheaply.

Then synthesize `L` around the decision surface. The language should remove
irrelevant general-purpose freedom while preserving the choices that determine
solution quality.

## Language synthesis

A treatment-valid language normally defines:

```text
syntax / canonical encoding
value + reference model
instruction vocabulary
operand/result types and shapes
state/effect/resource/schedule rules as relevant
composition/control/dataflow rules
lowering for every executable construct
diagnostics
frozen language identity/revision
```

Optimize for LLM generation and transformation rather than conventional human source
style. Prefer canonical forms, small vocabularies, explicit dependencies, fixed
ordering, low ambiguity, minimal sugar, and local validity.

The language must be newly adapted to the task. A renamed copy of Python/Rust/C++,
a prose plan, or an opaque whole-solution macro is not sufficient.

## Program generation

After `L` is frozen, generate the actual candidate algorithm **in `L`**. Do not first
write the complete host-language solution and reverse-encode it.

Preflight the task-language program for:

- valid instructions/references;
- compatible types/shapes/states/effects/resources;
- explicit task-critical dependency/order invariants;
- implementable lowering targets;
- bounded structure where required;
- binding to the frozen language revision.

Only then lower/translate into host code or stable semantic artifacts.

## Lowering

Treat lowering as a real compiler boundary. A valid language program plus a wrong
translation is a lowering defect, not task failure.

Useful lowering strategies include:

- deterministic source generation;
- AST/IR generation into an existing compiler;
- calls into a mature API/library;
- lowering into a stable Parallax semantic pack;
- generation of repository edits from an explicit transformation IR;
- schedule/configuration emission into a backend toolchain.

Generated virtual instructions are allowed when their meaning is explicit through
lowering. A language declaration cannot create a trusted primitive or machine
permission by itself.

## Tool intelligence

Choose tools by the boundary/question they test:

| Question | Instrument |
|---|---|
| Is `L` deterministic/parseable? | generated parser, schema checker, bounded parser probe |
| Is `p` structurally legal in `L`? | language checker/type/shape/state validator |
| Does lowering preserve the intended construct? | IR/source inspection, differential microcase, compiler diagnostics |
| Does host code build/integrate? | native compiler, formatter/static analyzer where informative, integration run |
| Which hypothesis explains a failure? | minimal reproducer, debugger, trace, targeted instrumentation |
| Where is performance lost? | profiler, allocation/memory trace, benchmark/hardware counters |
| Does the final behavior satisfy the task? | external task acceptance mechanism |

Do not accumulate tool output for appearance. Seek the observation that can change
the next engineering decision.

## Diagnostic loop

```text
observe exact failure
-> localize layer
-> form competing hypotheses when needed
-> choose discriminating experiment
-> repair earliest root cause
-> re-evaluate affected boundary
```

| Observation | Likely owner | Do not infer |
|---|---|---|
| Language parse/schema failure | `L` definition or generated `p` | Host implementation is wrong |
| Language type/shape/state failure | `p` or language constraints | New trusted primitive required |
| Valid `p`, wrong lowered structure | lowerer/translation | Task semantics should change |
| Host build/integration failure | lowering target / repository implementation | Language necessarily failed |
| Host executes but task counterexample fails | algorithm/task understanding | Parser/type system should encode final oracle |
| Repeated agent mistakes caused by awkward `L` | language design | Task should be weakened |
| Missing backend/primitive | actual capability boundary | Generated instruction authorizes it |
| Resource/performance failure | algorithm/language schedule/lowering/backend | Syntax length identifies bottleneck |

A language revision occurs between attempts. Freeze each revision before generating
its dependent program.

## Budget behavior

For this experimental branch, **language synthesis cost is mandatory treatment cost,
not a reason to skip the treatment**. Count it honestly.

Within the language-design stage, spend budget where it increases information or
representation leverage. Do not create elaborate syntax for its own sake. Stop
adding language features when they do not encode a task-relevant decision or reduce
agent ambiguity.

For measured `main` vs `experimental` comparisons, freeze symmetric total budgets and
count language design, parser/checker/lowering work, program generation, host code,
tools, repairs, and failed attempts.

## Acceptance and terminal outcomes

Language validity is not execution; execution is not task acceptance.

Use:

- `ACCEPTED_UNDER_POLICY` — final required acceptance passed for the exact language,
  program, lowering, and candidate dependencies;
- `REJECTED` — a known requirement failed;
- `BUDGET_EXHAUSTED` — treatment budget ended without acceptance;
- `DESIGN_ONLY` — required semantics/capability/authority cannot honestly be made
  executable in scope;
- `TRIVIAL_DIRECT` — only a mechanical non-treatment edit with no meaningful
  language-design content.

Retain the generated language/program and decisive evidence when evaluating the
method. Do not produce a ceremonial transcript.
