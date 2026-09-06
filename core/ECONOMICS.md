# Adaptation economics

Do not minimize operation count. Minimize total cost at a fixed acceptance policy,
or maximize the probability of an acceptable result within a fixed total budget.
Use deployment latency only after correctness and required evidence gates pass.

```text
total_cost = contract_work + retrieval + capsule_search + tutorials
           + all_program_attempts + repairs + solver_and_compiler_work
           + tests_and_proofs + failed_attempts + deployment_cost
```

One-time pack/engine construction is reported separately and also in a cold-start
accounting. Warm reuse may amortize that cost, but cannot erase it. Count full
macro bodies and their development; a call to SOLVE_TASK is not free intelligence.
A whole-task macro is legitimate algorithm synthesis, just not evidence that the
programming model solved the task cheaply on its own.

## Decision rule

Choose adaptation when its estimated benefit exceeds design, instruction,
validation, and maintenance costs under the actual remaining budget. When evidence
is weak, prefer a familiar existing DSL/API or run a capped pilot. An already
suitable library can be better than any newly invented language.

Do not give the adapted route an unlimited search team and compare it with a
single-shot direct baseline. Account for total tokens, money, elapsed time, and
host compute separately rather than hiding tradeoffs in a single number.

## Search measurements

Measure success probability per fixed budget, time-to-acceptable-result, false
acceptance, grammar/type failure rate, functional failure rate, repair count, and
semantic dependency footprint. Track cold and warm runs separately.

A low next-token entropy is not the objective: one confidently wrong output has
zero entropy. The useful quantity is probability mass assigned to acceptable
solutions after paying the full cost. Entropy and description length may be
secondary diagnostics, but comparisons require a fixed measurement protocol.

Program counts are also misleading without a length bound and an equivalence
notion. Infinitely many padded copies of one algorithm are not strategy diversity.
Predeclare meaningful implementation families or use held-out task variation.
