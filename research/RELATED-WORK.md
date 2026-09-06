# Selected primary sources and positioning

**Status:** source-archive literature notes, retained as historical positioning. Bibliographic and comparative claims have not been refreshed by this bootstrap. Consult the cited primary sources before relying on them in new research; this note is not an implementation dependency.

Literature check performed for this starter on 2026-09-05. This is a selective
map, not an exhaustive priority search. Links are to authors, proceedings,
research papers, or official project documentation. No reported speedup from
these sources is evidence that this starter improves LLM outcomes.

## Sketch: incomplete programs and synthesis holes

[The Sketching Approach to Program Synthesis, author tutorial](https://people.csail.mit.edu/asolar/sketch2012/)

Sketch lets a programmer supply partial implementation structure while a
synthesizer fills missing parts. Thus explicit holes and a division of labor
between a high-level author and solver are precedents, not new discoveries here.

## DreamCoder: learning languages and abstractions

[Ellis et al., DreamCoder](https://arxiv.org/abs/2006.08381)

DreamCoder grows symbolic abstractions and a language alongside neural search
guidance. It is directly relevant to the idea that a learned representation can
make later synthesis easier. It is not simply an LLM receiving a one-off Markdown
tutorial, which is the interface regime proposed in this starter.

## AutoDSL: automated DSL construction

[Shi et al., ACL 2024](https://aclanthology.org/2024.acl-long.659/)

AutoDSL uses domain-specific protocol corpora to design syntactic and semantic
constraints for procedural representations. It directly contradicts a blanket
priority claim that automated task/domain language design is wholly new. Its
domain, supervision, and evaluation are different from this executable capsule
prototype and must not be treated as interchangeable evidence.

## AMaze: optimizing languages to accelerate synthesis

[Ye et al., POPL 2026](https://xinpl.github.io/papers/popl26b.pdf)

AMaze optimizes DSLs for syntax-guided synthesizers, using program-fragment
features and estimated synthesis costs to guide modifications. Its operators
include grammar deletion and composition-based additions. This is especially
close prior work for representation-space optimization, though it is not a
measurement of LLM-specific syntax acquisition or Markdown orchestration.

## MLIR: extensible domain-aware compiler infrastructure

[Official language reference](https://mlir.llvm.org/docs/LangRef/)

MLIR supplies infrastructure for extensible operations and dialects in compiler
representations. It is relevant to implementing a future collection of domain
packs and lowering paths. It does not remove the need to define each operation's
semantics, implement it, and validate transformations.

## Halide: algorithms separated from schedules

[Official project and publications](https://halide-lang.org/)

Halide is a precedent for separating what is computed from execution-schedule
decisions. This is the appropriate foundation for the GPU case's semantic/schedule
split, rather than exposing warp primitives as the definition of normalization.

## Type-constrained code generation

[Mündler et al., Type-Constrained Code Generation with Language Models](https://arxiv.org/abs/2504.09246)

This work studies using type-system constraints during model code generation.
It motivates distinguishing prose guidance from actual structural enforcement.
Well-typedness is a specific property; it is not a guarantee of arbitrary task
satisfaction, numerical accuracy, or backend correctness.

## NVIDIA: scope of warp operations

[Using CUDA Warp-Level Primitives, official NVIDIA technical article](https://developer.nvidia.com/blog/using-cuda-warp-level-primitives/)

Warp collectives operate over participating warp threads. This supports the
concrete reduction-scope critique in packs/gpu/RMSNORM.md. It does not, on its own,
provide a complete or tested residual RMSNorm kernel for this repository.

## Honest proposed distinction

Study a model-conditioned, budget-accounted policy for generating compact checked
interfaces from pinned packs, with immutable task criteria and measured end-to-end
success. The integration may be worthwhile even where its components are established.
Any claim of a novel algorithm, theory, or research field requires more evidence
than this architecture document supplies.
