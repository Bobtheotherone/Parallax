# Experimental economics: measure the cost of forced language synthesis

On `experimental`, per-task AI-native language synthesis is the **treatment**, so it
is not skipped merely because direct code appears cheaper. The purpose of the branch
is to measure whether forcing that cost changes engineering outcomes enough to be
worth it.

Economics still matters. It determines how the method is evaluated and how much
complexity belongs inside the generated language; it does not decide whether to
avoid the experimental treatment.

## Experimental objective

A useful comparison quantity is:

```text
experimental_value ≈ P(acceptable result within budget)
                     × first_pass_quality
                     × engineering_quality
                     × reuse_or_performance_leverage
                     -------------------------------------------------
                     full_language_and_solution_cost
```

Keep the components separate in actual experiments when possible. A successful task
language has not “won” if its hidden design/compiler cost overwhelms the improvement.

## Full treatment cost

Count all work required by the experimental route:

```text
total_cost = task_understanding
           + repository/retrieval/tool use
           + task-language synthesis
           + grammar/schema/parser/checker work
           + task-language program generation
           + lowering/compiler/translation work
           + host implementation/integration
           + repairs and failed attempts
           + verification and performance measurement
           + deployment/runtime cost
```

Do not hide language-design work inside a prompt, macro, generated helper, or human
intervention and then compare only final program tokens.

Keep cold and warm costs separate. A language is allowed to become reusable across a
task family, but amortization must be demonstrated rather than assumed.

## Optimize the language, not the treatment away

Because language synthesis is mandatory, the engineering question inside one run is:

> What is the smallest, strongest AI-native language that exposes this task's real
> decision surface and can be lowered reliably?

Prefer language features that buy one or more of:

- smaller model search space;
- fewer equivalent spellings;
- explicit task-critical dependencies/invariants;
- stronger local type/shape/state/effect/resource checks;
- cleaner algorithm/schedule separation;
- lower repair ambiguity;
- better deterministic lowering;
- improved performance control where relevant.

Reject language complexity that mainly adds syntax novelty, human aesthetics,
redundant abstraction layers, or an opaque encoding of an already-finished answer.

A task language may be ugly and low-level. The relevant question is whether it makes
the model better, not whether a human would choose to maintain it manually.

## Virtual instructions and algorithmic cost

A virtual instruction can compress substantial reasoning. Attribute that work
correctly:

- if the instruction is a reusable lowering of a known pattern, count its synthesis
  and validation as language construction;
- if it encodes the entire task algorithm, count that algorithmic work in the
  language stage rather than crediting a trivial downstream program;
- if it requires a genuinely new trusted implementation capability, count the
  primitive/backend implementation separately.

Do not use accounting rules to forbid powerful generated instructions; use them to
make comparisons honest.

## Spend budget on information

Within a treatment run, choose tools by expected information gain:

```text
uncertainty
  -> highest-value question
  -> cheapest reliable parser/checker/compiler/debugger/profiler/oracle observation
  -> update language/program/lowering/implementation
```

A generated parser test can identify grammar ambiguity; a lowering microcase can
separate compiler error from algorithm error; a profiler can show whether a
language-exposed schedule actually reaches the hardware behavior expected.

Do not maximize test count or tool calls.

## Fair comparison with `main`

The principal methodology comparison is:

| Arm | Representation policy |
|---|---|
| `main` control | adaptively choose direct code, existing library/API/DSL, fixed interface, capsule, or new language |
| `experimental` treatment | require a new task-specific AI-native language/IR before substantive implementation |

Keep model, frozen task, starting repository state, available tools, acceptance
policy, and total budget as comparable as possible.

The control must be allowed to use strong libraries and ordinary host-language
reasoning. Do not cripple it to make generated languages look good. The treatment
must count language design/lowering cost. Do not give it free extra inference merely
because it has an additional required stage.

Measure properties that can answer the hypothesis:

- first-serious-candidate acceptance/quality;
- final acceptance within fixed budget;
- total cost/time to acceptable result;
- algorithm/architecture quality for accepted candidates;
- failure class and repair count;
- language acquisition/parse/type/lowering failure rates;
- context/token footprint where available;
- target performance for functionally accepted implementations;
- reuse gains separately when a language is reused.

Syntax validity, task-language length, host-code length, number of invented opcodes,
or novelty scores are diagnostics rather than success criteria.

## Performance economics

When performance matters, the generated language should expose the low-level
variables that determine real performance: asymptotic work, data layout, memory
traffic, allocation, cache locality, vectorization, batching, synchronization,
launch/transport costs, numerical format, and CPU/GPU scheduling as applicable.

Measure on the actual target after correctness gates. If the language exposes a
schedule but the backend does not implement it, syntax has not produced a speedup.

## Interpretation

A positive result means mandatory language synthesis improves a named class of tasks,
models, tools, and budgets enough to repay its total cost. A negative result means
forcing the language hurt or failed to help. A conditional result—e.g. benefits only
for high-complexity tasks or only after reuse—is equally valuable.

Do not change the experimental methodology mid-study because early results look
unfavorable. Change versions explicitly and treat the new rule as a new treatment.
