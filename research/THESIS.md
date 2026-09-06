# A thesis for adaptive representation synthesis

**Status:** research argument and hypotheses, not implementation authority. No empirical claim here establishes Parallax effectiveness. Adopted boundaries are recorded in [architecture](../docs/architecture/ARCHITECTURE.md).

## 1. The instrument, not the vocabulary

A programming language is one interface through which a solver encounters a
problem. The interesting intervention is not inventing words. It is selecting
which distinctions are visible, which choices remain open, which invariants are
maintained, and which obligations become mechanically checkable.

The proposal is to synthesize a temporary **representation capsule** for a model,
task, environment, and budget, over a stable semantic implementation. The model
uses that capsule to construct a program. A separate checking/evaluation path
judges the result against a task contract fixed before representation search.

The capsule is an instrument of reasoning. Like a coordinate system, it can make
some relationships easier to see. Unlike a mathematical coordinate change,
restricting operations can remove solutions, and a model can misunderstand a new
encoding. Its value must therefore be measured, not inferred from elegance.

## 2. What must be removed from the original account

The equation “language = function(model, task, environment, constraints)” omits the
source of semantics, the acceptance oracle, construction cost, and authority to
extend the runtime. Those omissions hide the hardest work.

A compiler does not know how to implement a newly named operation because prose
says that it does. A language restriction does not enforce itself by appearing in
a prompt. A smaller grammar does not imply a correct algorithm. A changing
language cannot have both arbitrary mutable meaning and reproducible artifacts.

Other attractive claims need qualification. General-purpose languages are not
simply designed to maximize expressiveness: restrictions, abstractions, effects,
and safety have long been design goals. In-context acquisition is not free or
necessarily reliable. A model with excellent native-language priors may be harmed
by an unfamiliar miniature syntax. These are reasons to benchmark adaptation,
not to dismiss it or promise its success in advance.

## 3. The semantic obligation accounting principle

Hiding a choice is not the same as eliminating the obligation associated with it.
If an operator performs a parallel reduction, someone must still specify its
scope, numerical behavior, synchronization, and implementation. Those obligations
move into a pack and backend. They become cheaper only if the implementation is
reused, its properties can be checked, or it removes repeated errors.

This is an engineering accounting principle, not a proven conservation law.
Compression can genuinely reduce work through reuse. But a short model output is
not evidence that the total system did less work. Count language design, macro
construction, runtime development, tests, and failed attempts.

## 4. A corrected mathematical object

Let T be a frozen task contract, M a specified model/decoder configuration, E a
pinned environment, K the available semantic packs, and b the full budget. Let
C denote a capsule, A its program, and R the actual checked execution result.

\[
C \sim G(M,T,E,K,b),\quad A\sim M(T,C),\quad
I=\operatorname{Expand}_C(A),\quad B=\operatorname{Backend}_E(I).
\]

The task asks for `Phi_T(B)`, not merely well-formedness of A. A backend may be an
interpreter; native compilation is an optional implemented capability, not a
universal premise. An unsupported backend makes that route unavailable.

For an idealized research objective, maximize:

\[
\Pr[\Phi_T(B)\ \land\ \operatorname{Cost}_{all}\le b].
\]

In practice Phi is not directly observable in every domain. Record the actual
acceptance policy and its gaps. A passing test-based proxy is not silently
identified with mathematical truth. For performance tasks, optimize target
performance subject to acceptance and total search cost, not in exchange for
correctness. Report false acceptance whenever stronger later evaluation finds it.

The optimum also depends on the generator/checker/repair policy and the prior
task distribution. It is not an intrinsic property of a language in isolation.

## 5. Why a smaller search space is not enough

An LLM does not sample uniformly from all syntactically valid native programs.
It has a learned distribution. Removing many unlikely bad programs may matter
little; removing one familiar useful pattern may matter greatly.

For a fixed distribution p and an ideal restriction V preserving every correct
program G, exact conditioning gives:

\[
p(G\mid V)=p(G)/p(V),\qquad G\subseteq V.
\]

That observation explains why removing invalid mass can help under its explicit
assumptions. It does not prove that prompting an unfamiliar language helps.
Changing syntax changes the model's distribution; local token masking is also
not generally the same as exact whole-sequence conditioning. The real question is
where acceptable probability mass moves after the intervention.

Entropy is therefore a diagnostic, not the objective. A model that always emits
the same wrong answer has zero entropy. Token entropy changes with serialization
and tokenization. Prefer acceptable-result rate within a fixed total budget.

## 6. A bounded grammar is not a universal metalanguage

Begin with a familiar serialization and existing semantic atoms. Permit selection,
restrictions, and transparent macros. Avoid a fresh parser, effect system, and
compiler for every task. Search over interfaces to supported meanings before
searching over new meanings themselves.

A whole-task macro is not necessarily cheating. Many useful libraries expose
complete algorithms. It is misleading only when the macro's construction is not
counted or its authoring work is credited to a trivial final program. The research
experiment should distinguish representation assistance from algorithm synthesis.

Likewise, requiring many syntactically valid programs does not demonstrate
creativity. No-op padding yields arbitrarily many programs. For a fixed functional
task, all correct implementations may share the same extensional behavior while
differing importantly in schedule, storage, latency, or memory use. Evaluate the
relevant implementation families, not raw syntax counts.

## 7. The unit of trust is different from the unit of adaptation

A capsule can be temporary. A semantic primitive and its implementation need
stable identities. A model may select or compose capabilities but cannot grant
itself new capabilities by writing a rule. A task oracle must not be rewritten
by the same feedback loop that tries to satisfy it.

This suggests three distinct artifacts: the **contract** defining success, the
**capsule** exposing supported decisions, and the **evidence-bearing result**.
They may be stored together, but must not have interchangeable authority.

The system learns by changing representations between frozen episodes. A missing
operation produces an extension proposal. A failed test produces a counterexample.
A timeout produces a budget-exhausted result. These are not equivalent events.

## 8. Stable interfaces, plural semantic domains

A universal semantic graph is an attractive organizing picture but not a complete
semantics. Tensors, transactions, protocols, memory ownership, and user interfaces
have different observations and correctness obligations. A common graph format
can connect domain-specific dialects without pretending these distinctions vanish.
[MLIR][mlir] is relevant prior infrastructure for extensible compiler dialects;
it is not an automatic proof that any generated dialect is meaningful.

For a large project, keep component contracts stable and local capsules replaceable.
Specify data layout, effects, ownership, errors, concurrency, and numerical
relations at boundaries. Interface compatibility must be checked at the level
that matters, not just by matching a function signature's text.

## 9. Learning is a cost to measure, not assume away

A model may acquire a compact interface from context, but acquisition consumes
prompt capacity and can introduce misinterpretation. Tutorial examples can leak
solutions. Syntax experiments can overfit model versions. Repeated tuning on the
same held-out tasks stops being a held-out evaluation.

Cache supported capsules by domain and environment. Measure cold and warm starts.
Profile a model using repeated controlled tasks, not anecdotal claims that it
“likes prefix expressions.” Test syntax changes separately from changes in macro
power, budget, and examples. A novel representation earns its place empirically.

## 10. The research contribution to seek

There is substantial precedent: [Sketch][sketch] fills program holes;
[DreamCoder][dreamcoder] learns abstractions and languages;
[AutoDSL][autodsl] automates domain-language construction;
[AMaze][amaze] optimizes DSLs for syntax-guided synthesis; and
[type-constrained generation][typegen] enforces some structural properties during
model generation. This project should not claim that generated languages or
representation search were previously unknown.

A candidate contribution is a cost-aware, model-conditioned policy that selects
and incrementally adapts **checked task interfaces**, preserving independently
specified acceptance criteria, and beats strong fixed representations under
matched total budgets on held-out task families. Whether that contribution is
novel or effective requires deeper literature review and experiments.

## 11. A philosophical commitment that can survive failure

The goal is not the smallest language, the strangest language, or a language with
a ten-second lifespan. It is the right boundary between decisions the solver
should make and obligations the machinery should discharge.

A negative experiment can be useful: perhaps familiar library calls win, perhaps
stable domain capsules amortize but per-task syntax does not, or perhaps the value
comes from explicit contracts rather than language adaptation. The system should
be designed to discover those outcomes instead of defining success as “a language
was generated.”

The strongest enduring thesis is this: **representations can be optimized as part
of computation, while their meanings and evidence remain accountable.**

[mlir]: https://mlir.llvm.org/docs/LangRef/
[sketch]: https://people.csail.mit.edu/asolar/sketch2012/
[dreamcoder]: https://arxiv.org/abs/2006.08381
[autodsl]: https://aclanthology.org/2024.acl-long.659/
[amaze]: https://xinpl.github.io/papers/popl26b.pdf
[typegen]: https://arxiv.org/abs/2504.09246
