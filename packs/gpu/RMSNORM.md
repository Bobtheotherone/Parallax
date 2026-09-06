# GPU case study: residual RMS normalization

**Status: DESIGN_ONLY. No supported GPU pack, kernel, GPU test, or benchmark is
included.** intseq cannot execute this example. Proposed operation spellings below
are notation, not implemented APIs.

## Diagnose the original miniature kernel

A warp reduction combines participating values within a warp; it does not by
itself complete a row-wide reduction distributed across several warps. This scope
is explicit in NVIDIA's [warp primitive documentation][nvidia]. Therefore a row
mapped over a 128/256/512-thread block cannot simply assume that `WARP_SUM` gives
every output the full row statistic. It could be correct under a different mapping,
but that mapping and its coverage rules must be specified.

`READ_VEC(input,row,width)` does not specify the column offset, stride, alignment,
which elements belong to each lane, or how tails are masked. A rule saying writes
are unique is not an implemented uniqueness check. Also resolve normalization
axis, residual placement, optional gain, intermediate rounding, aliasing, output
residual requirements, and numerical tolerance before designing the kernel.

## Fix semantics before schedule

For one explicitly chosen variant, define over real reference values:

\[
u_{ij}=x_{ij}+r_{ij},\qquad
q_i=\frac{1}{D}\sum_{j=0}^{D-1}u_{ij}^{2},\qquad
out_{ij}=\gamma_j u_{ij}(q_i+\epsilon)^{-1/2}.
\]

This chooses residual-before-normalization and a per-feature gain. It is not the
only interpretation of the original request. An actual contract must specify
whether gamma exists, how x+r is rounded, accumulation format, exact/approximate
reciprocal square root, finite input bounds, tails, strides, storage formats,
NaN/Inf handling, aliasing, and accepted absolute/relative error. No particular
floating-point implementation follows uniquely from this real-valued formula.

## Proposed semantic layer

```text
u = add(cast(x,acc_dtype), cast(residual,acc_dtype))
s = reduce_sum(square(u), axis=features, accumulate=acc_dtype)
y = multiply(multiply(u, rsqrt(s / D + epsilon)), gamma)
```

The defining scope is the **whole features axis**, not a hardware warp. Lowering
must implement that meaning through complete element coverage, combination of
partials, and distribution of the result to consumers. A backend may use warp
operations internally; that does not change the semantic scope.

## Proposed schedule layer

```text
mapping = one_block_per_row
threads = hole{128,256,512}
vector_width = hole{1,2,4,8}
reduction_plan = backend_selected_complete_row_reduction
```

These are candidate parameters, not universally legal choices. Actual device,
shape, alignment, tail behavior, register/shared-memory limits, and backend
support constrain the search. Resolve and validate every instantiation. A solver
that chooses a number has not proved a kernel correct.

Separating algorithm from schedule is established compiler practice, notably in
[Halide][halide]. The proposed contribution is to select the exposed schedule
choices and tutorial for a model/task while preserving the semantic contract.

## Required evidence before admission

Provide an independent reference; checker rules for shapes, scope, coverage,
ownership, and aliasing; an implemented lowering; numerical and adversarial-shape
tests; device-specific correctness checks; actual target compilation; and measured
performance only after correctness gates. Preserve the compiler, device, flags,
workloads, warm-up, synchronization, and timing method in the run record.

Do not move this document to an executable route until those dependencies exist.
The lesson is not “invent a better warp instruction.” It is “keep the semantic
reduction domain explicit until a real backend has implemented it.”

[nvidia]: https://developer.nvidia.com/blog/using-cuda-warp-level-primitives/
[halide]: https://halide-lang.org/
