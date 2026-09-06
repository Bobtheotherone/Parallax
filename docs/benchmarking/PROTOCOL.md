# Benchmark protocol: `main` vs mandatory AI-native language synthesis

**Status:** proposed protocol. No completed `main` versus `experimental` LLM
comparison is claimed by this repository.

This branch exists to test one primary question:

> For the same coding model, engineering task, starting repository state, tools,
> acceptance policy, and total budget, does forcing the model to invent and use a
> new low-level AI-native task language before implementation improve engineering
> outcomes relative to adaptive Parallax on `main`?

The benchmark must be capable of saying **yes, no, or only under certain conditions**.
Do not design the comparison so the experimental branch is guaranteed to win.

## The two principal arms

### Control — `main`

The model follows the `main` `AGENTS.md` contract. It must reason about
representation choice but may use whichever interface appears strongest:

- ordinary native-language coding;
- mature library/API/DSL;
- fixed typed/schema interface;
- Parallax capsule/macros;
- a novel language if it independently chooses one.

Do not force the control to avoid good libraries or direct code.

### Treatment — `experimental`

The same model follows the `experimental` `AGENTS.md` contract. For every
substantial task it must:

1. freeze/compress the task;
2. synthesize a new task-specific AI-native language/IR;
3. freeze its grammar/instruction/type/state/resource/lowering model;
4. generate the serious candidate in that language;
5. lower/translate it into real repository code or trusted semantics;
6. use normal tools and external task acceptance.

Language synthesis and lowering cost are part of the treatment budget.

## What must be held comparable

Within a paired comparison, hold constant or record unavoidable differences in:

- task/specification and acceptance mechanism;
- starting repository commit/state;
- model/provider/version and decoding configuration;
- available context and retrieval mechanism;
- tools, shell/compiler/debugger/profiler access;
- target environment/hardware;
- final-evaluator access/custody;
- total inference/tool/compute/time budget;
- number and form of evaluator-driven repair opportunities;
- task-family split and repetition/seed policy.

The branch-specific Markdown instructions are the intended treatment difference.
Do not quietly give the experimental arm additional hidden tools or a larger budget.

## Task selection

Use tasks difficult enough that representation choice could plausibly matter.
Include several structural families rather than many trivial variants of one toy.

Useful task dimensions include:

- multi-module architecture/refactoring with real compatibility constraints;
- nontrivial algorithms/data structures;
- protocol/state-machine implementation;
- ownership/concurrency/resource lifetime;
- numerical or scientific computation;
- CPU/GPU/I/O/performance-sensitive work;
- serialization/compiler/IR transformations;
- interacting defects where diagnosis matters;
- tasks with large distracting host-language/library surfaces;
- tasks where compact task-specific types, dataflow, constraints, or schedules could
  plausibly help an agent.

Also include some tasks where a mature library or straightforward host-language
solution is expected to be strong. Those are important negative controls: forced
language synthesis may be harmful there.

Do not treat typo fixes or trivial constant changes as substantive evidence for the
methodology.

## First-shot versus repaired performance

Measure both:

**First serious candidate** — the first host implementation produced after the
method's own permitted task analysis, language synthesis (treatment only), program
generation, lowering, repository inspection, and public tool use, but before
feedback from the final evaluator.

**Final candidate within budget** — the best result after permitted diagnostics and
repairs without exceeding the fixed total budget.

This distinction tests the intended claim that a task language may make the model
**stronger before evaluator-driven retries**, not merely easier to repair afterward.

## Required treatment artifacts

For the experimental arm retain enough evidence to establish that the methodology
actually occurred:

- task-language definition/revision/identity;
- canonical grammar/encoding or sufficient machine specification;
- instruction/operator vocabulary and relevant types/states/resources;
- lowering contract/target;
- candidate program expressed in that language;
- resulting host implementation/artifact.

Do not require long narration. These artifacts are necessary because an experimental
run where the agent wrote Python first and invented a DSL afterward is not the
specified treatment.

For the control arm retain its actual chosen representation and implementation.

## Cost accounting

Charge all causally required work.

### Control

```text
problem understanding
+ representation decision/adaptation actually used
+ program/host implementation
+ tools
+ repairs
+ verification/execution
```

### Treatment

```text
problem understanding
+ task-language synthesis
+ parser/checker/spec acquisition work
+ program generation in task language
+ lowering/compiler/translation
+ host implementation/integration
+ tools
+ repairs
+ verification/execution
```

Keep available dimensions separate: model tokens/requests, wall time, money, host
compute, tool calls, compiler/runtime work, and human intervention.

If exact provider token fields are unavailable, report them unavailable rather than
inventing values.

## Hard acceptance gates

A method has not succeeded merely because it generated a clever language.

Task-specific hard gates may include:

- functional correctness;
- compatibility/protocol behavior;
- prohibited side effects;
- safety/resource constraints;
- numerical tolerances/order requirements;
- build/integration correctness;
- required performance threshold.

The final evaluator remains conceptually separate from candidate generation.
Language validity, lowering validity, host execution, and task correctness are
different observations.

## Primary metrics

At minimum record per paired task:

- first-serious-candidate accepted: yes/no;
- final accepted within budget: yes/no;
- total measured cost/resource usage;
- time to accepted result where meaningful;
- terminal failure class if rejected.

For accepted candidates, add task-specific engineering quality measures such as:

- algorithmic complexity;
- target latency/throughput;
- memory/allocation behavior;
- architecture/dependency correctness;
- compatibility surface;
- fault/recovery behavior;
- numerical accuracy/stability;
- expert technical review tied to concrete consequences.

## Language-specific secondary metrics

These explain mechanism but are not success by themselves:

- language-definition size/token cost;
- program size/token cost;
- number of opcodes/types/states;
- parser/type/state/resource rejection rate;
- lowering failure rate;
- proportion of host defects traceable to lowering;
- model repair edits per accepted result;
- number of equivalent spellings/canonicalization rate;
- context reduction relative to host representation;
- reuse rate on related tasks.

Do not optimize for language novelty, maximum opcode count, shortest syntax, or
highest grammar-valid rate at the expense of actual task outcomes.

## Failure taxonomy

Classify the earliest material failure:

- task/contract misunderstanding;
- **language synthesis/acquisition failure**;
- **language too restrictive or poorly structured**;
- **task-language algorithm error despite valid representation**;
- **lowering/translation defect**;
- host implementation/integration defect;
- backend/tool capability missing;
- resource/budget exhaustion;
- performance design failure;
- final evaluator/infrastructure failure.

This taxonomy matters because a treatment can fail for very different reasons. A
well-designed language with a bad algorithm is evidence about solver reasoning; a
good language program with a broken lowerer is evidence about compiler complexity.

## Mechanism ablations

If the treatment shows a difference, use targeted ablations to understand why.
Useful follow-ups include:

1. same experimental instruction inventory but human-friendly versus AI-native
   canonical syntax;
2. same language but inferred versus explicit types/shapes/states;
3. same semantics but canonical single spelling versus syntactic aliases/sugar;
4. same language program with deterministic generated lowering versus model-written
   lowering;
5. low-level task-specific IR versus a generic generated DSL;
6. cold per-task language versus a warm reused task-family language;
7. language-only context versus language plus full host-library documentation.

Do these only after the primary branch comparison; do not multiply arms before the
basic treatment is understood.

## Model dependence

The central idea is specifically about **how LLMs/agents operate**, so model
heterogeneity matters. A representation that helps one model may hurt another.

When resources permit, repeat across models with different training, context,
reasoning, code-generation, and tool-use characteristics. Do not generalize a result
from one model family to “LLMs” without qualification.

## Statistical analysis

Use paired tasks: both arms solve the same task instance from the same starting
state. Treat task/family—not retries—as the independent unit.

Report raw per-task outcomes and heterogeneity before pooled summaries. For
stochastic runs, freeze repetition/seed/order policy before inspecting results.
Paired bootstrap or hierarchical task-family analysis can be used when sample size
supports it.

A one-task experiment is a pilot, not proof of a universal methodology.

## Stop rules

Stop a run on:

- accepted result meeting the frozen quality target;
- fixed total budget exhaustion;
- user/operator cancellation;
- nonrecoverable safety/capability/infrastructure failure.

Do not replenish the experimental budget because it had to synthesize a language;
that cost is the treatment. Do not replenish the control because its chosen
representation performed poorly.

## Interpretation

Possible valid conclusions include:

- mandatory AI-native task languages substantially improve difficult engineering;
- they improve first-shot quality but lose on total cost;
- they mainly help performance/state/constraint-heavy tasks;
- they help only after language reuse;
- they help some model families but not others;
- they reduce syntax/implementation errors but not algorithm errors;
- lowering complexity erases their benefit;
- direct/library coding on `main` is better for most tasks.

Any of these would answer the experiment more honestly than changing the methodology
after seeing results.

The experiment should reward accepted engineering quality, not methodological
obedience by itself.
