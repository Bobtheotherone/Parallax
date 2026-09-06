# Benchmark protocol: engineering capability under matched budgets

**Status:** proposed protocol. No LLM development comparison or adaptive-representation benchmark was executed during the 2026-09-05 bootstrap. The imported intseq run report is reference-runtime evidence, not a model benchmark.

The benchmark exists to answer engineering questions, not to validate that a workflow was followed. A run is informative when it fixes the thing being compared, measures the property that matters, and makes alternative explanations hard to confuse with the claimed effect.

## Two tracks with different claims

### Track A — engineering-agent capability

Question: **How effectively does a specified coding agent solve a bounded repository task?**

A useful Track A task can require repository comprehension, architecture, implementation, debugging, performance reasoning, compatibility work, or integration across modules. The public [SPEC-001](../specs/001-intseq-reference.md) is an initial development pilot: it exposes its reference and public cases, so it can characterize engineering behavior but cannot establish unseen-task generalization.

Track A should distinguish:

- **first-serious-candidate quality:** the candidate after the agent's own repository inspection, reasoning, implementation, and public tool use, but before feedback from a final evaluator;
- **final quality within budget:** the best candidate reached after permitted diagnostics/repairs;
- **engineering quality:** task-specific properties such as algorithmic complexity, architecture, compatibility, resource behavior, target performance, or maintainability after correctness gates.

This rewards agents that use tools intelligently before submission rather than agents that simply consume many evaluator-driven retries.

### Track B — representation efficacy

Question: **For the same model, task distribution, tools, acceptance policy, and total budget, does changing the model-facing representation improve the probability or quality of an acceptable solution?**

The principal quantity is not syntax validity or token count. It is an acceptance/cost curve such as:

```text
P(task accepted with required quality | total budget <= b)
```

and, when the task includes an optimization objective, target quality of **accepted** solutions as a function of full search cost.

Do not pool Track A and Track B. A good repository implementation demonstrates agent capability; it does not show that an adaptive capsule caused the improvement.

## Define the experimental unit before the tooling

The unit should normally be a **task family instance** with a frozen contract, repository/environment state, acceptance mechanism, and budget. Freeze only information that affects the claim:

- task/spec version and starting source revision;
- model/provider/decoder configuration that is under experimental control;
- available tools and target environment;
- candidate-visible context and examples;
- acceptance mechanism and final-evaluator access policy;
- total resource cap and permitted repair feedback;
- arm/treatment assignment;
- task-family split and repetition/seed policy;
- primary metrics and stopping/exclusion rules.

Do not preregister incidental prose or force every command into a schema. Record additional detail when it is needed to reproduce a result, explain a confound, or diagnose a failure.

If a required provider usage field is unavailable, record it as unavailable. Do not turn an estimate into a measured token count.

## Task-suite design

A benchmark that only measures toy syntax errors will optimize Parallax toward toy syntax errors. Select tasks whose difficulty matches the engineering capability being studied.

Useful dimensions include:

- cross-module data/control flow and legacy interfaces;
- ambiguous but recoverable local design choices;
- externally meaningful compatibility constraints;
- nontrivial algorithms or data structures;
- state machines, concurrency, ownership, resource lifetime, or failure recovery;
- performance-sensitive CPU/GPU/I/O/serialization paths;
- incomplete implementations with interacting defects;
- tasks where an existing library/API is a strong alternative to a new representation.

Split by **structural family or template**, not only random instances of one template. Development/validation families may inform representation design; final families used for a generalization claim must be frozen before the final comparison. Repeated attempts on public SPEC-001 do not become new unseen tasks.

Track likely prior exposure: public examples, tutorial solutions, source archives, cached capsules/programs, and prior attempts. Unknown model pretraining exposure is a limitation, not evidence of contamination-free evaluation.

## Competitive arms

Track B should compare against the strongest practical alternatives relevant to the task, not weak strawmen. Candidate arms include:

1. direct native-language generation;
2. direct generation using a strong existing library or typed API;
3. a fixed domain interface/DSL;
4. a restricted fixed interface using the same semantic inventory;
5. adaptive operation selection;
6. adaptive compositional macros/capsules.

Not every experiment needs every arm. Choose the minimal set that can answer the hypothesis and declare omissions before outcomes are known.

Keep task semantics, oracle access, model, tools, and total budget comparable. If an arm receives grammar-constrained decoding, extra retrieval, additional agents, a solver, or privileged implementation access, treat that capability as part of the treatment and account for it.

A useful existing library is a real baseline. Representation synthesis has not won if it recreates a weaker library at higher cost.

## Budget parity and economics

Use [ECONOMICS](../../core/ECONOMICS.md) as the accounting model. Charge all work causally required to obtain the candidate:

```text
contract/context work + retrieval + representation design
+ macro/tutorial construction + generation + tools
+ repairs + failed attempts + solver/compiler work
+ verification/review used by the method + target execution
```

Keep dimensions separate where possible: model input/output/reasoning/cache usage, money, wall time, host compute, external tool calls, and human intervention. Parallel work reduces wall time but does not make summed inference/compute free.

Report **cold** construction and **warm** reuse separately. If a pack, macro library, or cached capsule is amortized across tasks, state the reuse horizon and show both the up-front cost and marginal cost.

Compare methods across one or more fixed total budgets rather than granting a losing arm extra retries until it succeeds. Success-vs-budget curves are more informative than a single arbitrary cap when resources permit.

## Acceptance: hard gates first

The final evaluator is conceptually separate from the candidate pipeline, following [ADR-0003](../architecture/decisions/0003-independent-task-acceptance.md).

Hard gates are task-specific. Typical gates include functional behavior, compatibility, prohibited effects, safety constraints, resource limits, and required numerical tolerances. A lower latency, shorter program, elegant architecture, or high weighted score cannot compensate for a wrong result when correctness is a hard requirement.

After hard gates pass, measure the quality dimensions the task actually values. Examples:

- throughput/latency on a recorded target and workload;
- peak memory or allocation rate;
- asymptotic complexity under stated input growth;
- binary/API/protocol compatibility;
- recovery behavior under injected faults;
- architecture properties such as required dependency direction or state ownership;
- code-review findings under a predeclared technical rubric.

Avoid generic style scores as a primary engineering metric. Prefer observable constraints or expert judgments tied to concrete consequences.

### Final-evaluator custody

Public tests, compiler diagnostics, traces, and counterexamples are legitimate development feedback. A final held-out evaluator is different: when claiming hold-out performance, keep its code/inputs outside candidate read/write capability and do not feed its failures back into the same run.

If the environment cannot enforce that separation, report the limitation and make a public-evaluation claim instead. Do not simulate secrecy with a prompt instruction.

## Primary measurements

For each task/arm, record at minimum:

- first-serious-candidate acceptance;
- final acceptance within budget;
- total cost/resource usage available from the host;
- time to acceptable result, if meaningful;
- terminal failure class when no candidate is accepted.

Use task-specific quality metrics for accepted candidates. Useful secondary diagnostics include syntax/type/admission failure, functional failure, resource rejection, repair count, semantic dependency footprint, and performance distributions.

Do **not** optimize for test count, operation count, raw program count, token entropy, or a generic “verification percentage.” These may diagnose mechanisms but are not the product. Infinitely many padded programs do not imply useful strategy diversity, and a confidently wrong model has low entropy.

When a stronger post-hoc audit exists, report false acceptance: candidates that passed the declared public/primary policy but failed the stronger audit. If no stronger audit ran, the false-acceptance rate is unknown, not zero.

## Attribute gains instead of merely observing them

When Track B shows a difference, use the cheapest ablations that discriminate plausible causes. Important separations include:

- **representation vs extra context:** same contract/examples, different interface;
- **selection vs new algorithmic content:** same macro/algorithm inventory, vary only exposure/serialization;
- **syntax vs semantic inventory:** same operations/macros, vary syntax/tutorial;
- **constraints vs extra inference:** match total model/tool budget;
- **capsule design vs programmer benefit:** count synthesis work and measure both stages;
- **reuse vs cold-start engineering:** compare warm and cold accounting.

A whole-task macro may be useful engineering. Attribute the algorithmic work to macro construction rather than claiming that a trivial caller discovered the algorithm.

## Failure analysis should improve the system

A failed run is most useful when localized. Classify the earliest material cause, while retaining secondary contributors when needed:

- task/contract misunderstanding;
- representation acquisition error;
- representation too restrictive for the attempted strategy;
- algorithm/design error despite valid representation;
- implementation/integration defect;
- backend/tool capability missing;
- resource/budget exhaustion;
- performance design failure;
- evaluator/infrastructure failure.

Then ask what experiment would distinguish competing explanations. For example, a high typecheck rate with low task acceptance points toward algorithm/task reasoning, not necessarily a need for more type rules. Repeated timeouts with a correct asymptotic design may point to implementation constants or tool overhead rather than representation failure.

Search failure is not proof of unexpressibility. Claim bounded unexpressibility only with a complete finite search or a valid domain argument.

## Statistical analysis

Use paired comparisons when arms solve the same task instances. Treat tasks/families—not retries—as the independent sampling units. Report raw per-task outcomes and heterogeneity before pooled summaries.

For stochastic runs, predeclare repetition and seed/order policy. A task/family-clustered paired bootstrap is a reasonable default for uncertainty intervals when its assumptions match the design; hierarchical models may be useful with multiple task families/models. Do not choose sample size or stopping rules after inspecting significance.

A one-task or small public pilot can discover failure modes and estimate feasibility. It cannot support a general performance ranking.

## Stopping and infrastructure failures

Stop a run on the first result that meets the frozen acceptance/quality target, total budget exhaustion, user/operator cancellation, or a nonrecoverable capability/safety failure. Use symmetric, predeclared handling for infrastructure faults.

Do not erase rejected candidates from cost accounting. Do not replenish budget because an approach was inconvenient. A task-changing clarification starts a new task version rather than improving the old trial retrospectively.

## Minimal reproducibility record

Retain enough to reconstruct the comparison without turning the benchmark into a paperwork system:

- task/spec and source revision;
- arm/treatment and candidate-visible context identities;
- model/tool/environment identities that matter;
- budget and actual available usage;
- produced artifacts and terminal outcome;
- acceptance mechanism identity/custody and result;
- raw measurements needed for reported metrics;
- declared exclusions, infrastructure faults, and human interventions.

Use [RUN](../../templates/RUN.md) where it is convenient, but the record serves the experiment—not the reverse. Never fabricate missing tool output or historical execution.

## Promotion rule

Promote a representation family only when it demonstrates reproducible value against competitive alternatives for a named domain/model/backend/budget regime: higher acceptable-solution probability, lower cost to a target success level, better quality of accepted solutions, or an explicitly valued auditability property at an accepted cost.

Reevaluate after material model, decoder, semantic-pack, backend, task-distribution, or reuse-regime changes. A negative result is useful evidence. The protocol is designed to discover when direct code or an existing library is the better representation.
