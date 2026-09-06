# Thesis: optimize the interface to engineering problems

**Status:** research argument and falsifiable hypotheses, not implementation
authority. Nothing in this document establishes that Parallax improves model
performance. Adopted system boundaries live in the project architecture and core
semantic contracts.

## 1. Core claim

A coding model does not solve an abstract task directly. It solves the task through
a **representation**: source language, APIs, schemas, types, examples, repository
structure, compiler diagnostics, runtime tools, and whatever distinctions the
interface makes easy or hard to express.

That interface is therefore part of the computational problem. For some tasks, a
better interface can concentrate model effort on the decisions that determine a
correct implementation while moving repetitive or mechanically checkable
obligations into reusable machinery.

The research claim is not “smaller languages are better” or “generate a DSL for
every task.” It is:

> **Choose the representation that gives this solver the most useful structure for
> this task and environment, while keeping task success and semantic meaning fixed.**

Often the right representation will be ordinary code plus a good library. Sometimes
it may be a restricted API, typed schema, reusable macro set, schedule language,
intermediate representation, or task-specific capsule. Adaptation is valuable only
when its benefit exceeds acquisition, construction, validation, and maintenance
cost.

## 2. Representation changes where intelligence is spent

Every engineering solution has obligations: understand intent, choose an algorithm,
respect interfaces, manage state/effects, implement operations, satisfy resource
constraints, diagnose failures, and establish acceptance. A representation does not
make these obligations disappear; it **places** them.

| Obligation | Good placement |
|---|---|
| task intent and acceptance | frozen external contract/oracle |
| stable domain meaning | semantic pack or trusted library/backend |
| task-specific algorithmic choices | solver/program unless deliberately supplied as reusable abstraction |
| structural legality | types/schema/checker where practical |
| machine mapping/schedule | explicit schedule layer when performance requires it |
| permissions and isolation | trusted host/environment |
| diagnostics | checker/compiler/runtime with failure-localizing outputs |
| final evidence | independent acceptance/measurement path |

The design objective is to put routine, reusable, enforceable obligations in
machinery while leaving the solver the decisions where model reasoning has the
highest marginal value.

This is why a one-token `SOLVE_TASK()` macro is not automatically impressive. If
its implementation encodes the complete task algorithm, the hard reasoning was
performed during macro construction. That can still be useful abstraction, but its
cost and ownership belong in the accounting.

## 3. Stable semantics make representation search meaningful

Let `T` be a frozen task contract, `M` a specified model/decoder, `E` a pinned
execution environment, `K` a set of implemented semantic packs/capabilities, and
`b` a total budget.

Let a candidate representation `R` choose some combination of operation subset,
compositional helpers, structural constraints, serialization, tutorial/context,
and—where supported—finite legal implementation parameters. A program `p` generated
against `R` lowers through a fixed semantic path:

\[
R \sim G(M,T,E,K,b),\qquad
p \sim M(T,R),\qquad
I=\operatorname{Expand}_R(p),\qquad
B=\operatorname{Backend}_E(I).
\]

The external task asks whether

\[
\Phi_T(B)
\]

holds under its stated observation model. It does **not** ask whether `p` merely
parses, typechecks, or executes.

A useful primary objective is therefore

\[
\max_R\Pr[\Phi_T(B)\ \land\ \operatorname{Cost}_{all}\le b],
\]

where `Cost_all` includes representation design, context, generation, failed
attempts, repairs, tools, verification, compiler/solver work, and any cold-start
construction allocated to the regime.

When accepted implementations also have a performance objective, treat correctness
as a constraint and compare quality among accepted results. Do not trade task
correctness for a faster wrong program through a weighted score unless the task
contract explicitly defines that tradeoff.

Stable semantics are essential to interpreting this experiment. If a new surface
can silently redefine primitives or acceptance, then a “better representation” may
simply be an easier task.

## 4. Search-space size is only a proxy

A model does not sample uniformly from all syntactically valid programs. It has a
learned distribution shaped by training, syntax familiarity, examples, naming, and
context.

If a restriction `V` preserved all correct programs `G` and generation were exact
conditioning of a fixed distribution, then

\[
p(G\mid V)=p(G)/p(V),\qquad G\subseteq V.
\]

This idealized observation explains why removing invalid mass *can* help. But a new
syntax changes the model's distribution, and constrained token generation is not in
general equivalent to conditioning complete native programs on a property.
Removing many unlikely invalid programs may do little; removing one familiar useful
pattern may hurt badly.

Therefore grammar size, token entropy, or number of syntactically valid programs is
not the research objective. A model that emits one confidently wrong program has
low entropy and zero task value. Measure acceptable-result probability, repair cost,
and total resource use.

## 5. Properties of a high-leverage representation

A representation is promising when it changes engineering cognition, not merely
spelling.

### It exposes the task's invariants

Types, schemas, APIs, or examples should make critical distinctions visible:
original versus transformed values, ownership, effects, state transitions,
numerical precision, reduction scope, idempotency, compatibility, or resource
bounds. Hiding these distinctions invites first-pass errors.

### It removes irrelevant choices

A task-specific operation subset can prevent the model from spending probability
mass on unrelated APIs or invalid compositions. The restriction must preserve the
solution families that matter; arbitrary minimality is not a virtue.

### It packages reusable semantic work

A checked helper can compress a recurring algorithmic pattern, especially when its
construction cost is amortized across tasks. Reuse is real leverage; relabeling new
algorithm synthesis as “language design” is not.

### It makes decomposition explicit

Difficult engineering often fails at boundaries rather than inside individual
functions. Useful interfaces reveal dependency direction, component ownership,
data shape/layout, state machines, error propagation, concurrency scope, and
resource lifetime. A representation that turns implicit cross-module assumptions
into explicit contracts can improve the first serious solution even without
shrinking syntax much.

### It supports informative tools

The best checker error is not merely “invalid.” It localizes a violated assumption
well enough to choose the next discriminating experiment. A representation can be
valuable because compilers, static analyzers, profilers, solvers, or differential
runners become more precise instruments over it.

### It matches the solver's priors

Familiar names and compositional patterns can outperform theoretically elegant but
novel notation. Novel serialization needs a measured reason. A representation
should spend context on semantic distinctions the model needs, not on teaching an
arbitrary grammar.

### It preserves escape to stronger tools

A representation should not trap the solver inside a toy abstraction when the real
problem demands a database query planner, SAT solver, profiler, debugger, GPU
compiler, or mature library. Adaptation should expose the right machinery, not
reimplement it in miniature.

## 6. A capability-first adaptation policy

Before synthesizing a new interface, compare four routes:

1. **DIRECT:** native code and standard tools;
2. **LIBRARY/FIXED API:** native code plus a mature task-relevant abstraction;
3. **FIXED RESTRICTED INTERFACE:** known stable DSL/schema/type system;
4. **ADAPTIVE:** task/model-conditioned selection, macros, constraints, tutorial,
   or schedule choices over implemented semantics.

Choose the cheapest plausible route that preserves the contract. The adaptive route
has to earn its design cost.

A practical model for representation choice should extract task features such as:

```text
semantic domain
algorithm family / uncertainty
state/effect complexity
shape/layout/numerical constraints
available mature libraries
backend/tool capabilities
expected failure modes
performance bottleneck candidates
reuse horizon
model familiarity with candidate interfaces
remaining budget
```

Then predict whether a representation change will reduce expected search/repair
cost enough to justify acquisition and validation. This policy itself can improve
over time from measured outcomes; it should not define success as “a capsule was
produced.”

## 7. Representation leverage for difficult codebases

The strongest use case is not necessarily a tiny expression language. Large
engineering tasks contain search spaces at several levels.

### Architecture

A model may need to choose ownership boundaries, dependency direction, state
placement, extension points, and compatibility surfaces. A compact component graph
or typed service/module interface can make forbidden cycles and data ownership
obvious before code generation.

### State and concurrency

State-machine representations can expose legal transitions, idempotency, retry
semantics, cancellation, locks/ownership, message ordering, and failure recovery.
They are worthwhile when these constraints dominate correctness; they are ceremony
when the task is a pure function.

### Data and performance

Tensor layouts, batch dimensions, database cardinalities, memory ownership,
serialization boundaries, and I/O patterns often determine the right algorithm.
A representation that makes these quantities first-class can prevent a locally
clean but globally expensive implementation.

### Backend schedule

For kernels or compilers, separate semantic algorithms from mapping decisions such
as tiling, vectorization, threads, memory spaces, fusion, and reduction strategies.
Expose a small legality-checked schedule space when those choices are the actual
optimization problem. Do not make hardware scope define mathematical scope.

### Legacy compatibility

For mature systems, a representation can summarize external behavior, invariants,
and call/data dependencies while leaving existing code as the implementation. The
right abstraction reduces context without pretending the old system is simpler
than it is.

## 8. Tool intelligence is part of the representation

Parallax should optimize the **question-answering loop** between model and tools.
The preferred debugging pattern is:

```text
observe
  -> localize
  -> form competing hypotheses
  -> choose the experiment that best separates them
  -> repair the root cause
  -> re-evaluate the affected obligation
```

Representation quality affects every arrow. Types can localize a dataflow mismatch;
a stable IR can show whether lowering changed behavior; a profiler can reveal the
real bottleneck; a property test can distinguish two algorithm hypotheses; a
compiler diagnostic can expose an illegal schedule.

Tool calls without a question are process overhead. Conversely, prose reasoning
should not replace a cheap decisive tool result. A capable system chooses tools for
information gain.

## 9. Reversible autonomy reduces process latency

Engineering agents lose capability when every local uncertainty becomes a handoff.
A representation or task packet should distinguish:

- **contract-changing uncertainty:** can alter output, safety, compatibility,
  permissions, or an irreversible architecture choice; resolve externally;
- **implementation uncertainty:** several reversible internal choices satisfy the
  same contract; choose one, inspect the result, and adjust if evidence demands.

This keeps autonomy where experimentation is cheap while preserving human/task
owner authority where a guess would redefine success.

## 10. The unit of adaptation is not the unit of trust

A capsule can be disposable. The semantics it invokes cannot be disposable if old
artifacts must remain interpretable.

Generated data may select an existing capability; it cannot grant itself a new one.
A new primitive or backend changes the trusted implementation base and needs an
explicit versioned engineering change. A final task oracle must remain outside the
same adaptive loop that is trying to satisfy it.

This naturally produces three distinct objects:

```text
contract  -> what success means
interface/program -> how the solver expresses a candidate
result/evidence -> what the trusted machinery observed
```

Keeping these roles separate is not governance for its own sake. It prevents the
system from “improving” by changing the problem or accepting its own answer.

## 11. Semantic domains should stay plural

A universal graph container can be convenient, but it does not erase domain
semantics. Tensors, transactions, protocols, memory ownership, and distributed
state have different observations and correctness relations.

[MLIR](https://mlir.llvm.org/docs/LangRef/) is relevant as infrastructure for
extensible operations/dialects; it is not evidence that one generated dialect
automatically has sound semantics. [Halide](https://halide-lang.org/) demonstrates
the leverage of separating algorithms from schedules. These precedents support
modular semantic packs rather than a claim that Parallax should invent one universal
meaning for every engineering object.

A future cross-domain system should connect components through explicit interfaces
for data, effects, errors, ownership, concurrency, numerical relations, and
versioning. Textually matching signatures are not enough when observable behavior
differs.

## 12. Learning and reuse are empirical resources

Models can acquire interfaces in context, but instruction consumes tokens and can
introduce misinterpretation. Syntax/tutorials may overfit a model version. Repeated
adaptation on the same benchmark can leak task structure into the representation
policy.

Measure:

- cold interface construction versus warm reuse;
- instruction/context cost;
- acquisition failures and syntax/type errors;
- functional failures after structural admission;
- repair attempts and tool cost;
- model/decoder sensitivity;
- semantic dependency footprint;
- cache reuse horizon and invalidation conditions.

Cache useful domain capsules or helper sets when their semantic/backend dependencies
still match. Do not carry empirical success rates across changed models or targets
as if they were guarantees.

## 13. Research hypotheses that can fail

Parallax should pursue hypotheses with discriminating experiments rather than a
philosophy that is true by definition.

**H1 — invariant exposure improves first-pass correctness.** Interfaces that make
critical dataflow/state/numerical invariants explicit increase acceptable first
serious attempts relative to equally informed native-code prompts.

**H2 — adaptive selection beats full fixed surfaces in some regimes.** With syntax,
algorithm inventory, and total budget controlled, task/model-conditioned operation
selection improves acceptable-result probability for domains with large irrelevant
API surface.

**H3 — reusable abstraction pays after amortization.** Checked compositional helpers
reduce total solve cost over a declared task horizon after charging construction,
validation, and cache invalidation.

**H4 — diagnostic structure improves recovery.** Type/schema/IR boundaries reduce
attempts or time to root-cause repair on semantic failures, beyond merely reducing
parse errors.

**H5 — legal schedule spaces improve systems code.** Given a real backend and fixed
operator semantics, models selecting among legality-checked schedule choices reach
better accepted target performance than unconstrained low-level generation or a
single fixed schedule under comparable budget.

**H6 — adaptation has a negative region.** For familiar tasks with strong native
libraries or low search complexity, DIRECT/fixed interfaces win because adaptation
overhead and unfamiliarity dominate. A good policy should predict this region and
avoid capsule synthesis.

Mechanism-specific ablations are essential. Hold macro power constant while varying
syntax; hold syntax constant while varying operation selection; give equivalent
helpers to fixed baselines; compare contract scaffolding without representation
change; match total inference/tool budget.

## 14. What would count as a contribution

There is substantial precedent for program holes and synthesis
([Sketch](https://people.csail.mit.edu/asolar/sketch2012/)), learned abstraction
([DreamCoder](https://arxiv.org/abs/2006.08381)), automated DSL construction
([AutoDSL](https://aclanthology.org/2024.acl-long.659/)), DSL optimization for
synthesis ([AMaze](https://xinpl.github.io/papers/popl26b.pdf)), and constrained
model generation
([type-constrained code generation](https://arxiv.org/abs/2504.09246)). Parallax
should not claim these categories as inventions.

A defensible contribution would be an end-to-end policy that:

- identifies which engineering distinctions should be exposed to a given model;
- constructs or selects a compact checked interface over existing semantics;
- uses real tool feedback to localize failures;
- preserves task/oracle independence and host capability boundaries;
- chooses direct/fixed routes when adaptation is not worth its cost;
- demonstrates reproducible gains over competitive baselines under matched total
  budgets on held-out task families;
- explains *which mechanism* produced the gain through ablation and failure analysis.

A negative result is equally capable of improving the design. Perhaps stable typed
libraries dominate per-task surfaces; perhaps explicit contracts and diagnostics
matter more than syntax; perhaps adaptation only pays for schedule search or warm
reuse. The system should be designed to discover those boundaries.

## 15. Enduring thesis

The lasting idea is not a ten-second programming language. It is a broader
engineering principle:

> **Representations allocate reasoning. Optimize that allocation, but keep meaning,
> capability, and acceptance anchored outside the representation being optimized.**

If Parallax can make that choice empirically—selecting the interface that improves
first-pass correctness, technical leverage, solution quality, and recoverability at
lower total cost—it becomes useful even when the winning interface is conventional
code.
