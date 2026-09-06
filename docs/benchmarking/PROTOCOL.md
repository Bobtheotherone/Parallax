# Benchmark protocol

**Consumer:** experiment operator and evidence reviewer. **Status:** proposed
protocol; no LLM trial or comparative benchmark has run in this bootstrap.
A run becomes an experiment only after its choices, budget, acceptance mechanism,
and stopping rules are fixed and its actual evidence is retained.

## Two questions, two tracks

**Track A — developing Parallax.** How well does a specified coding LLM/agent
implement a bounded repository specification? Start with
[SPEC-001](../specs/001-intseq-reference.md), a public reference-extraction and
conformance task. The source solution and public tests are disclosed. This is
not an unseen algorithm-synthesis task or a test of adaptive representations.
It may be used immediately as an observational development pilot, provided the
report says which checks/review were actually obtained.

**Track B — using Parallax.** At matched total inference/tool/compute budget and
required evidence policy, does an adaptive representation improve acceptable-
solution rate on held-out tasks? Separately, does it reduce cost/time to a target
rate, or improve performance of accepted implementations on a real target?
This requires a working host and an executed experiment; the reference test report
cannot answer it.

Do not pool Track A and Track B outcomes. A successful extraction is infrastructure
evidence, not evidence that adaptation helps.

## Freeze before any scored trial

Record run ID, track, hypothesis, task/spec revision and starting repository commit,
task distribution and exclusions, experimental arms, models/provider versions,
decoding settings, tools and versions, prompt/context assembly, seed policy,
repetitions, total budgets, acceptance policy/oracle identity and custody, metrics,
analysis, stopping rules, and retry/infrastructure-failure policy. Record unavailable
provider fields as unavailable rather than estimating them as measured usage.

For Track A, freeze the same source-only base and public spec for every compared
agent. Each gets an isolated clean checkout and the same available tools, docs,
public fixtures, and scope. Do not expose another arm's implementation or reviews.
A reviewer/evaluator assesses the resulting diff against frozen criteria; an
agent's `done` marker is not the evaluator's verdict. Record human interventions.
Do not score absence of a hidden suite as if a hidden suite passed.

A pilot can report “passes public checks; independent review pending.” A comparative
or confirmatory conclusion requires the preregistered acceptance policy to be met.
No dataset, isolated harness, or final evaluator is supplied by this bootstrap.

## Arms and strong baselines for Track B

Compare direct native generation, native generation with a good typed library,
a fixed domain DSL, a restricted fixed DSL without new macros, and adaptive
capsules. Include fixed-DSL grammar/type-constrained decoding where available.
Document omissions or unsupported arms before seeing outcomes. Allow each baseline
to spend its total budget competitively, including repair and public feedback;
do not compare one direct shot with an unlimited adaptive search team.

Keep tools, oracle access, examples, task definitions, and total resources comparable.
Any capability difference is either a declared treatment or a confound to remove.
A useful library is a real competitor, not something to withhold from the baseline.

Required interpretive ablations when attributing gains to representation:
keep macro/algorithm inventory identical while varying selection/serialization;
keep syntax fixed while varying selected operations; and compare contract/test
scaffolding without a new language. These distinguish useful abstraction,
constraints, extra compute, and actual adaptive representation. Count whole-task
macros as algorithm synthesis rather than free intelligence for the programmer.

## Development, validation, final evaluation

Split by task family or structural template, not merely random instances of the
same template. Separate capsule/profile development, validation/model selection,
and final held-out families. Freeze reusable packs and oracle implementations
before final evaluation. A new task-specific primitive during final testing is
additional development and belongs in a separately declared regime.

Track A's first public task is development material. Future confirmatory coding
benchmarks need new independently specified task families and private acceptance
cases; repeated attempts on SPEC-001 do not become independent unseen tasks.
A hold-out cannot be created simply by renaming a public example or choosing a
new random seed after studying its structure.

For a held-out claim, keep final acceptance code and inputs outside the read/write
capabilities of capsule and program synthesizers (or coding candidates in Track A).
An environment that cannot enforce this must report the limitation and cannot
claim protected hold-out evaluation. Public semantic specifications remain allowed;
record exactly what was exposed. Do not feed final failures back into repair and
continue calling the same evaluation final.

Track tutorial solutions, cached capsules/programs, source archive exposure,
prior attempts, model-training contamination where known, and provenance across
splits. Unknown pretraining exposure is a limitation, not evidence of cleanliness.

## Budget parity and cost accounting

Use the cost decomposition in [ECONOMICS](../../core/ECONOMICS.md). Charge contract
work, retrieval, capsule search, tutorials, all candidate languages/programs,
repairs, compilers/solvers, tests/proofs, review agents, and failed attempts.
Account for both the model designing a macro and the model calling it. Parallel
work consumes summed inference/compute even when wall time overlaps.

Record separate dimensions: provider input/output/reasoning/cache usage when
available, money under recorded pricing, wall time, host compute, tool calls,
human interventions, and number of attempts. Do not hide tradeoffs in one score.
Prompt bytes are not provider tokens. Unknown usage prevents a claimed strict
matched-token comparison unless a declared common cap was enforceably applied.

Report cold engine/pack construction, cold capsule generation, and warm reuse
separately. One-time engineering cost may be shared across arms but must remain
visible in cold-start accounting. State the amortization horizon for caching;
never erase its cost. Count all searched candidates, not just the selected winner.
The documentation-bootstrap cost is disclosed setup, not runtime performance.

Fix total caps before starting. The synthesis protocol's candidate/repair defaults
are starting policies, not optimized constants. Track A needs its own declared
episode cap. No arm receives free additional budget because its approach failed.

## Metrics and acceptance

Primary: acceptable-result rate per task within the full predeclared budget.
Hard gates are functional correctness under the chosen policy, permitted effects,
and required evidence. Lower latency or a weighted score cannot compensate for a
wrong answer or missing required verification.

Track A also reports acceptance-criterion coverage, regressions, unauthorized
scope/semantic changes, evidence completeness, reviewer findings, and terminal
spec state. A partial implementation remains in the denominator and is described
as partial, not rounded to success.

Secondary: time to acceptable result, usage/cost, wall/host time, failed attempts,
syntax/type/admission errors, functional errors, resource failures, repair count,
semantic dependency footprint, and evidence coverage. Distinguish static admission,
representation preservation, task satisfaction, and backend behavior. Syntax
success, low token entropy, short programs, or many padded variants are not the
objective. Diversity claims require a fixed length/equivalence or implementation-
family definition.

Audit a stronger acceptance set for false acceptance where available: report
candidates that pass the public policy but fail that audit separately. If the
stronger audit did not run, the false-acceptance rate is unknown, not zero.
Native performance must be measured on the actual target only after functional
acceptance, with environment, warm-up, repetitions, timing method, and distributions.
No performance inference follows from intseq operation counts.

## Stopping, failures, and analysis

Stop each run on the first acceptable result, declared budget exhaustion,
cancellation, or a nonrecoverable/unsafe capability failure, according to the
frozen policy. Account for all attempts up to stopping. Do not replenish a losing
arm's budget or extend the trial count until significance appears.

Retain rejected capsules, unsupported tasks, timeouts, unavailable evidence, and
infrastructure failures. Include them in denominators or apply symmetric,
predeclared exclusions. Report raw counts and reasons either way. Task-changing
clarification creates a new trial/version. Search failure is not proof of bounded
unexpressibility; insufficient evidence may warrant `UNKNOWN` reasoning or a
`DESIGN_ONLY`/`BUDGET_EXHAUSTED` workflow result, not invented success.

Predeclare paired task comparisons, uncertainty estimates, and repeated stochastic
runs. Use a task/family-clustered paired bootstrap when appropriate to the sampling
design; do not treat retries from one task as independent samples. Report model
and task heterogeneity, not only pooled averages. No arbitrary fixed sample count
guarantees adequate power. A one-task pilot yields observations, not a general
performance ranking.

When adaptation loses, distinguish design/instruction overhead, poor syntax
acquisition, insufficient expressivity, implementation defects, task confusion,
and resource limits. A higher typecheck rate alone does not establish useful gain.

## Reproducible record and promotion

Use [RUN](../../templates/RUN.md), including its benchmark extension. Preserve
contracts, prompts/context identities, artifacts, tool transcripts, all costs,
model/environment versions, random policies, raw results, rejected candidates,
and evaluator identity. Protect secrets/private final inputs in operator-controlled
storage and record durable identifiers instead of leaking them to candidates.
Self-reports and self-review are not independently specified ground truth.

Promote a capsule family only after reproducible gains for its intended domain,
model, backend, budget, and reuse regime—or a separately declared auditability
benefit at an accepted cost. Reevaluate after semantic/model/decoder/backend changes.
The expected direction of an effect is a hypothesis, not a promised product feature.
