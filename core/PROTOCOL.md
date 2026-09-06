# High-agency synthesis protocol

This protocol describes how a host or engineering agent should solve a task using
Parallax. It is a **decision loop**, not a ritualized sequence of reports. The
standalone intseq reference checks and evaluates artifacts; it does not implement
this orchestration.

## The loop

```text
frozen task
   -> compress problem and failure surface
   -> choose the strongest low-cost representation
   -> build one serious candidate
   -> use tools to discriminate likely failures
   -> repair the root cause or revise the representation between attempts
   -> external task acceptance
   -> retain the result and the evidence that changes future decisions
```

`DIRECT`, existing-library/fixed-interface, and `CAPSULE` routes are peers. Use
`DESIGN_ONLY` when required meaning, authority, or executable capability genuinely
does not exist. A capsule is not the default merely because Parallax can build one.

## First serious attempt

Before generating code/programs, establish enough structure to avoid blind retry:

- hard contract invariants and acceptance mechanism;
- relevant existing architecture and dependency direction;
- data shapes/state transitions and ownership;
- error, numerical, concurrency, and resource semantics when relevant;
- the highest-risk unknowns;
- a plausible algorithm/implementation family and expected complexity;
- which tools can answer the unknowns cheaply.

For a difficult repository task, inspect the implementation paths that own the
behavior before editing. For a performance task, identify the expected bottleneck
before optimizing. For a protocol or compatibility task, identify the externally
observable state machine before changing representation.

This is not a requirement for a long plan. A few precise invariants and a correct
mental model are more valuable than a page of status prose.

## Representation selection

Choose the representation that exposes the right decisions and hides only work
that a trusted reusable implementation can actually discharge.

Use a capsule when it materially:

- removes invalid or irrelevant choices;
- exposes a useful decomposition not obvious in the native surface;
- makes important invariants structural/checkable;
- enables reusable domain machinery or backend expertise;
- reduces context/search enough to repay acquisition and validation cost.

Prefer direct code or an existing library when it already provides those benefits.
Do not invent syntax to make the output look specialized.

Freeze a capsule during one program attempt. If its semantics or identity changes,
that is a new representation episode; regenerate or explicitly migrate dependent
programs.

## Tool intelligence

Tools are engineering instruments. Select them by the question they answer:

| Question | Useful instrument |
|---|---|
| What code owns this behavior? | repository search, call graph, history, reference implementation |
| Is the candidate structurally valid? | parser, compiler, type checker, schema/static analyzer |
| Which hypothesis explains the failure? | minimal reproducer, debugger, trace, targeted instrumentation |
| Is behavior compatible? | differential test against a pinned path plus contract-derived cases |
| Where is time/memory going? | profiler, allocation trace, benchmark, hardware counters when justified |
| Does an invariant hold broadly? | property/model checking, fuzzing, bounded enumeration, formal tool as appropriate |
| Is the optimization real? | controlled target benchmark after correctness acceptance |

Do not accumulate tool output. Seek the highest-information observation that can
change the next decision.

## Diagnostic loop

When a candidate fails:

```text
observe exact failure
-> localize boundary/component
-> form at least two plausible hypotheses when ambiguity remains
-> choose an experiment whose outcomes distinguish them
-> repair the earliest root cause
-> re-run the smallest affected acceptance slice, then broader checks as needed
```

Route by failure class:

| Observation | Likely owner / next move | Do not infer |
|---|---|---|
| Parse/schema/type/arity rejection | Program or representation shape | New primitive needed |
| Capsule/program identity mismatch | Frozen artifact binding | Safe to ignore identity |
| Typed result fails task case | Algorithm or contract understanding | Type system should encode the oracle |
| Wrong state/effect/order | Algorithm/architecture boundary | More syntax will fix semantics |
| Unsupported lowering/backend | Implementation capability | Imagined compilation is evidence |
| Runtime resource rejection | Algorithm, schedule, or declared limit | Mathematical result is wrong |
| Slow accepted result | Profile real bottleneck; revise algorithm/layout/schedule | Operation count identifies bottleneck |
| Numerical drift | Numerical relation/order/format/backend | Algebraic equality guarantees FP equality |
| Repeated failures trace to awkward interface | Representation revision between attempts | Rewrite the task or final oracle |
| Demonstrated missing semantic capability | Versioned extension proposal | Generated data may self-authorize it |

Search exhaustion establishes only that the selected search failed under its
budget. Claim bounded unexpressibility only with a complete argument over a stated
finite/structured space.

## Budget behavior

For ordinary engineering, allocate budget adaptively: spend more where uncertainty
and failure cost are high, less on already-settled mechanics. Stop retrying a route
when another representation or algorithm has higher expected value.

For measured experiments, freeze total budgets/stopping rules before scoring and
apply them symmetrically across arms. The historical small candidate-count defaults
may be useful pilot settings, but they are not universal engineering constants.

## Acceptance and terminal outcomes

Execution is not acceptance. After a candidate is checked and run, evaluate it
against the frozen external task policy. Preserve the final oracle outside generated
artifact authority.

The compatible terminal labels remain:

- `ACCEPTED_UNDER_POLICY` — required acceptance evidence passed for the exact
  candidate/dependencies;
- `REJECTED` — a known requirement failed;
- `BUDGET_EXHAUSTED` — the allotted search/engineering budget ended without
  acceptance;
- `DESIGN_ONLY` — execution cannot honestly proceed because required semantics,
  capability, or authority is unavailable.

Retain failures and decisive diagnostics that improve future decisions. Do not
produce a ceremonial transcript of every step.
