# Related work: mechanisms Parallax must distinguish

**Status:** research positioning, not implementation authority. The source set is
selective and inherits the repository's 2026-09-05 literature notes; it is not an
exhaustive priority search. Consult primary sources before publication-quality
claims. Results reported by these projects are not evidence that Parallax improves
LLM engineering outcomes.

The useful question is not “has anyone generated a language before?” The useful
question is which **mechanism** changes, where semantic authority lives, what cost
is paid, and how success is evaluated.

## Comparison axes

Use these axes when comparing representation systems:

| Axis | Distinctions that matter |
|---|---|
| adaptation target | holes, grammar, abstraction library, operation subset, syntax, schedule, tutorial/context |
| adaptation granularity | global language, domain, task family, single task, single model/task episode |
| solver | enumerative/SAT/SMT/SyGuS, learned symbolic search, autoregressive model, compiler autotuner |
| semantic anchor | generated meaning, fixed primitives, reference implementation, compiler dialect, external specification |
| enforcement | prompt only, grammar/type constrained generation, post-hoc checker, proof/solver constraint, trusted backend |
| objective | synthesis time, likelihood, program length, acceptable-result probability, runtime performance, total cost |
| algorithm ownership | solver discovers algorithm, abstraction library supplies it, task-specific macro pre-encodes it |
| evaluation boundary | syntax/admission, semantic equivalence, task oracle, target performance |
| cost accounting | search only versus language/model/tool/repair/cold-start/warm-reuse cost |

Parallax is interesting only if its combination of choices produces measurable
engineering value beyond strong fixed interfaces and libraries.

## Program sketching: structure plus explicit holes

[Sketch / the sketching approach to program synthesis](https://people.csail.mit.edu/asolar/sketch2012/)
shows a mature division of labor: a programmer supplies partial structure and a
solver fills bounded unknowns subject to a specification.

**Transferable mechanism:** exposing the right finite decisions can shrink search
without moving every semantic obligation into the solver.

**Parallax discriminator:** future finite holes should be real solver/enumerator
inputs with legality and budget, not question-mark syntax that an LLM is expected
to resolve magically. Parallax additionally asks whether the *interface itself*
should vary with model/task while stable semantic implementations remain pinned.

## DreamCoder: learned abstraction and language growth

[Ellis et al., DreamCoder](https://arxiv.org/abs/2006.08381) learns reusable symbolic
abstractions together with search guidance over a task distribution.

**Transferable mechanism:** abstraction invention can move recurring structure into
a reusable library and reshape future search.

**Parallax discriminator:** a one-episode capsule/tutorial is a different regime
from learning a library across tasks. Experiments should separate gains from reused
algorithmic abstractions from gains caused by task-specific operation selection,
serialization, or instruction.

## AutoDSL: automated domain-specific representation construction

[Shi et al., AutoDSL, ACL 2024](https://aclanthology.org/2024.acl-long.659/) studies
automated construction of constrained domain-specific representations from domain
protocol information.

**Transferable mechanism:** semantic and syntactic constraints can themselves be an
automation target rather than a permanently hand-designed interface.

**Parallax discriminator:** do not claim automated DSL construction as a novel
category. Test the narrower hypothesis that a model/task-conditioned checked
interface over already implemented semantics improves difficult engineering under
full cost accounting and an external task oracle.

## AMaze: optimize a DSL for synthesis cost

[Ye et al., AMaze, POPL 2026](https://xinpl.github.io/papers/popl26b.pdf) optimizes
DSLs for syntax-guided synthesis using program-fragment features and estimated
synthesis cost, including grammar restriction and composition-oriented changes.

**Transferable mechanism:** the representation can be an optimization variable, and
removing or composing language constructs can alter solver search cost.

**Parallax discriminator:** SyGuS search and autoregressive model generation have
different priors and failure modes. A grammar transformation that helps a symbolic
synthesizer is a hypothesis—not evidence—that an LLM will acquire or use the same
surface effectively.

## Type-constrained language-model generation

[Mündler et al., Type-Constrained Code Generation with Language Models](https://arxiv.org/abs/2504.09246)
studies enforcing type constraints during generation.

**Transferable mechanism:** structural validity can be enforced during search rather
than merely requested in prose or rejected afterward.

**Parallax discriminator:** type validity is one axis. A representation experiment
must still measure algorithmic task acceptance, backend behavior, resource cost,
and repair dynamics. A higher valid-output rate is not sufficient if probability
mass moves toward well-typed wrong programs.

## MLIR: extensible implemented semantic infrastructure

[MLIR's language reference](https://mlir.llvm.org/docs/LangRef/) demonstrates an
extensible compiler infrastructure built around operations, dialects, regions,
types, and explicit lowering relationships.

**Transferable mechanism:** domain-specific interfaces are more useful when they
lower through stable implemented components rather than requiring a fresh compiler
for every generated surface.

**Parallax discriminator:** using an extensible IR does not define a domain's
observations, numerical relation, effects, ownership, or task acceptance. A future
Parallax backend could use such infrastructure, but generated syntax would still
need versioned semantics and checked lowering.

## Halide: algorithm/schedule separation

[Halide](https://halide-lang.org/) is a key precedent for separating the algorithm
from choices about execution schedule.

**Transferable mechanism:** keep “what is computed” stable while searching over
mapping, tiling, vectorization, parallelism, and storage decisions.

**Parallax discriminator:** the GPU RMSNorm case should adapt meaningful schedule
choices only after normalization semantics, layouts, numerical behavior, and
backend support are fixed. Exposing warp-level syntax as operator meaning would
collapse the distinction Halide helps clarify.

## NVIDIA warp primitives: implementation scope is not semantic scope

[NVIDIA's warp-level primitive documentation](https://developer.nvidia.com/blog/using-cuda-warp-level-primitives/)
provides the concrete hardware context for the reduction-scope issue discussed in
`packs/gpu/RMSNORM.md`.

**Transferable mechanism:** collective scope and participation rules are part of a
real lowering obligation.

**Parallax discriminator:** a row-wide semantic reduction must remain row-wide even
when its implementation is decomposed into warp collectives and a cross-warp
combination. Hardware convenience cannot silently narrow the meaning.

## Confounds a Parallax experiment must isolate

Several superficially similar “representation gains” are different mechanisms:

1. **Algorithm injection.** A task-specific macro can contain the hard algorithm.
   Keep its construction cost visible and compare with giving the same helper to a
   fixed-interface baseline.
2. **Constraint enforcement.** A grammar/type-constrained decoder may improve
   validity without any adaptive semantics. Compare it directly.
3. **Extra inference/tool budget.** Capsule design plus programmer repair can simply
   be more compute. Match total resources.
4. **Better specification.** Explicit contracts/examples may help even with native
   code. Include a contract-scaffolded baseline.
5. **Operation selection.** Removing irrelevant operations may help without changing
   syntax. Hold serialization/tutorial constant when testing this.
6. **Syntax/tutorial acquisition.** A new surface can help or hurt model priors.
   Hold semantic power constant when testing this.
7. **Reusable abstraction.** Warm cached helpers are different from per-task
   invention. Report cold and warm regimes separately.

Without these ablations, “adaptive representation won” is too coarse to teach us
why.

## Falsifiable Parallax research hypotheses

The strongest research program is comparative, not novelty-by-definition:

- **H1 — selection leverage:** with semantics and algorithm inventory fixed,
  model/task-conditioned operation selection increases acceptable-result probability
  within a matched total budget over the full fixed interface.
- **H2 — abstraction leverage:** reusable compositional helpers improve difficult
  task performance after charging their construction/amortization cost, beyond the
  same fixed library given without adaptation.
- **H3 — diagnostic leverage:** a representation with failure-localizing types,
  schemas, and lowering reduces time/attempts to repair semantic programs, not only
  syntax-error rate.
- **H4 — schedule leverage:** for implemented performance domains, exposing a small
  legal schedule space lets models reach better accepted target implementations
  than either unconstrained low-level code or one fixed schedule under comparable
  budget.
- **H5 — negative-domain boundary:** familiar native/library interfaces outperform
  adaptation when acquisition/design cost exceeds search-space reduction. A useful
  system should learn to choose DIRECT in those regimes.

Evidence against these hypotheses is informative. If fixed typed libraries match or
beat adaptive capsules once budgets and helper power are equalized, per-task
representation synthesis may not be the useful layer.

## Positioning worth defending

Parallax should not claim invention of DSLs, program synthesis, learned
abstractions, typed constrained generation, compiler dialects, or algorithm/schedule
separation. A defensible candidate contribution is narrower:

> a model-conditioned, cost-aware policy for selecting and composing **checked
> interfaces over stable implemented semantics**, evaluated by independent task
> acceptance against strong direct/library/fixed-interface baselines.

The contribution would be established by reproducible experiments and mechanism-
specific ablations, not by the existence of a generated mini-language.
