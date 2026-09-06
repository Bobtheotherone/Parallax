# Adaptation economics: spend complexity where it buys capability

Parallax should optimize engineering outcomes, not operation count, prompt
novelty, or process completion. Representation work is worthwhile only when it
improves the probability or quality of an acceptable solution enough to repay its
construction, learning, validation, and maintenance cost.

A useful objective is:

```text
engineering_value ≈ P(acceptable result within budget)
                    × solution_quality
                    × reuse_or_performance_leverage
                    -------------------------------------------------
                    total_design_search_tooling_verification_cost
```

The factors need not be collapsed into one score in measurements. The formula is
a decision aid: a tiny program is not cheap if a large hidden macro, compiler, or
search process had to be invented first.

## Full cost

Count work wherever it occurs:

```text
total_cost = task_understanding
           + repository/retrieval/tool use
           + representation design and acquisition
           + all candidate generation and repair
           + compiler/solver/backend work
           + verification and performance measurement
           + failed attempts
           + deployment/runtime cost
```

Report model usage, money, wall time, host compute, and human effort separately
when they matter; they trade off differently. Parallel work can reduce latency
without reducing summed compute or inference cost.

Keep **cold** costs (new pack/backend/capsule construction) separate from **warm**
reuse costs. State the reuse horizon before claiming amortization.

## Choose the cheapest interface that exposes the right structure

Prefer, in order of increasing adaptation cost, whichever route is technically
strongest for the task:

| Route | Good default when | Warning sign |
|---|---|---|
| Direct code | The native language already exposes the relevant structure and the solution is short or familiar | Repeated semantic mistakes or huge irrelevant API/search surface |
| Existing library/API | A mature abstraction already owns the hard algorithm, protocol, or hardware behavior | Wrapper code starts rebuilding the library's semantics |
| Fixed typed/schema interface | The domain benefits from constrained construction across many tasks | The interface hides decisions the task must still make |
| Restricted capsule | Selecting a small subset materially reduces invalid choices or context | Restriction removes common useful strategies |
| New compositional macro | A reusable pattern compresses repeated reasoning while preserving inspectable semantics | The macro simply hides a one-off whole solution whose construction is not counted |
| New primitive/backend | The required meaning or implementation capability truly does not exist | A local program bug is being misdiagnosed as a language deficiency |

Representation leverage is high when the interface makes important invariants hard
to violate, exposes the right decomposition, or moves recurring expert work into a
reusable checked implementation. It is low when it merely renames operations.

## Spend the next unit of budget on information

During implementation or debugging, choose tools by expected information gain.
A compiler error, minimal reproducer, profiler sample, static-analysis finding,
differential check, or targeted benchmark is valuable when it discriminates
between plausible hypotheses and changes the next action.

Prefer one experiment that distinguishes two likely root causes over ten redundant
tests that all exercise the same path. Do not run a tool because a checklist says
to; know the question it should answer.

A useful budgeting loop is:

```text
remaining uncertainty -> highest-value question -> cheapest reliable instrument
                      -> update design/search -> repeat
```

Stop adding machinery when the marginal reduction in engineering risk is smaller
than the cost and maintenance burden it introduces.

## Compare routes fairly

For research or selection decisions, compare routes under the same frozen task and
acceptance policy. Give strong baselines realistic tools and repair budgets. A good
library is a competitor, not something to withhold so a generated DSL looks better.

Measure at least what is needed to answer the decision:

- acceptable-result rate within the declared budget;
- time/cost to an acceptable result;
- false acceptance when a stronger later check exposes it;
- failure class and repair count when recoverability matters;
- context/semantic dependency footprint when interface compression is the claim;
- target performance only for functionally accepted implementations.

Grammar-valid rate, test count, token entropy, source length, or number of distinct
spellings are diagnostics, not the product. Infinitely many padded programs do not
create strategy diversity.

## Performance economics

When performance is part of the task, reason about the real bottleneck: asymptotic
work, memory traffic/layout, allocations, cache behavior, vectorization, batching,
serialization, I/O, synchronization, contention, numerical format, and CPU/GPU
boundaries as applicable. Measure on the actual target after correctness gates.

A representation can justify its cost by exposing optimization decisions cleanly—for
example, separating a reduction's semantic scope from a backend schedule—but the
speedup belongs to the implemented and measured backend, not to the syntax alone.
