# GPU design case: residual RMS normalization

**Status: DESIGN_ONLY.** Parallax currently has no supported GPU semantic pack,
GPU checker, native lowering, device test, or GPU benchmark. `intseq` cannot execute
this material. All operation and schedule spellings below are design notation, not
implemented APIs.

The value of this case is architectural: a good representation should expose the
normalization semantics and the schedule decisions that matter, while refusing to
confuse a hardware primitive such as a warp shuffle with the mathematical scope of
the reduction.

## 1. Freeze the operator before optimizing it

One concrete variant is residual-before-normalization with per-feature gain. For
row `i`, feature `j`, and width `D`:

\[
u_{ij}=x_{ij}+r_{ij},\qquad
q_i=\frac{1}{D}\sum_{j=0}^{D-1}u_{ij}^{2},\qquad
out_{ij}=\gamma_j u_{ij}(q_i+\epsilon)^{-1/2}.
\]

This real-valued equation is only the algorithmic center. An executable contract
must additionally fix all observations that can change real behavior:

| Concern | Contract questions |
|---|---|
| shapes | batch/row dimensions, exact normalization axis, legal `D`, broadcasting |
| layout | element/row strides, contiguity, alignment, tensor offsets, tail rules |
| storage | dtype of `x`, residual, gain, output, optional residual output |
| arithmetic | cast points, accumulation dtype, square/mean rounding, `rsqrt` policy, epsilon representation |
| exceptional values | NaN/Inf/subnormal behavior and any finite-input precondition |
| aliasing | whether output may overlap `x`, residual, or gain; read-before-write requirements |
| effects | whether the residual sum must also be materialized and in what dtype |
| accuracy | absolute/relative/ULP policy, reference computation, shape/value domain |
| target | device family, compiler/runtime, launch and synchronization capabilities |

Do not choose a schedule while these questions are still capable of changing the
answer. A reversible local choice such as block size can remain a schedule hole; a
choice such as residual placement cannot.

## 2. Keep semantic scope independent of hardware scope

A semantic sketch for the chosen variant is:

```text
u = add(cast(x, acc_dtype), cast(residual, acc_dtype))
s = reduce_sum(square(u), axis=features, accumulate=acc_dtype)
inv = rsqrt(s / D + epsilon)
y = multiply(multiply(u, inv), gamma)
```

The reduction domain is the complete features axis. NVIDIA warp collectives operate
among participating threads of a warp; they do not automatically combine partials
from multiple warps.[^nvidia] Therefore `WARP_SUM` is a valid implementation step
only when the mapping proves that its participating lanes cover the entire semantic
reduction domain, or when a higher-level reduction combines all warp partials.

This distinction is a general Parallax design rule: expose semantic scope in the
stable layer; expose machine mapping in the schedule layer. Never encode “warp” as
the meaning of “row reduction.”

## 3. Candidate row-reduction implementations

### One warp per row

Attractive when one warp can cover `D` efficiently. Each lane accumulates a strided
subset, a warp all-reduce combines lane partials, and the result is broadcast within
the warp. The design still needs a tail mask when `D` is not an exact multiple of
the lane/vector coverage.

This route minimizes synchronization machinery, but it can underutilize hardware or
increase per-lane serial work for larger `D`. It is a schedule candidate, not a
universal rule.

### One block per row

A common general plan is:

```text
thread t:
  local = 0
  for j in elements_assigned_to(t):
      u = x[j] + residual[j]
      local += u*u

within each warp: reduce local
warp leaders: write partials to shared memory
synchronize block
one warp: reduce all warp partials
synchronize/broadcast row statistic
all threads: normalize and write assigned elements
```

Correctness requires complete, non-overlapping element coverage, inclusion of every
warp partial, and synchronization where shared partials cross warp boundaries.
The exact mechanism can use shuffles, shared memory, cooperative-group helpers, or
compiler-generated reductions; the semantic obligation is the same.

### Multiple blocks per row

Ordinary independent blocks cannot complete a row-wide reduction by assuming a
cross-block barrier exists. A multi-block design needs an implemented mechanism:
for example a first kernel writing partials followed by a second reduction/kernel,
or a supported cooperative launch with precisely specified synchronization.

This can become worthwhile for very large rows, but it changes launch structure,
intermediate storage, and latency. It should be selected because a measured target
needs it, not because the representation offers the knob.

## 4. Decide how the second pass obtains `u`

Normalization needs `u` after the row statistic is known. That creates a real
storage/recomputation decision:

- **reload/recompute:** read `x` and residual again after the reduction;
- **materialize residual:** if the API requires an output residual, write `u` in the
  first pass and read it for normalization;
- **retain on chip:** for sufficiently small rows, keep some/all `u` in registers or
  shared memory, subject to occupancy and capacity limits;
- **split kernels:** materialize an intermediate and normalize in a later kernel.

These plans trade global-memory traffic against register/shared-memory pressure,
occupancy, launch overhead, and implementation complexity. A useful cost model
counts bytes moved and on-chip storage before guessing which one is fastest, then
uses profiling to identify the actual bottleneck.

For example, a nominally “fused” kernel that cannot retain `u` may still read `x`
and residual twice. The word fused does not establish low memory traffic.

## 5. Vectorization is a legality problem before a speed problem

A placeholder such as `READ_VEC(input,row,width)` is underspecified. A vectorized
load/store plan must define:

```text
base address + row stride + column offset
lane -> feature indices
vector width
required alignment
valid lanes/elements for the final partial vector
behavior for noncontiguous strides
```

A vector width of 4 or 8 is legal only when the address/layout contract and tail
handling support it. The schedule search space should encode these predicates so an
agent does not spend attempts on impossible combinations.

A better schedule object is therefore not just

```text
threads = hole{128,256,512}
vector_width = hole{1,2,4,8}
```

but conceptually

```text
candidate = (threads, vector_width, reduction_plan, retention_plan)
legal(candidate, shape, layout, dtype, device) -> bool
```

with illegal candidates pruned before code generation.

## 6. Numerical policy belongs in semantics/acceptance

Floating-point RMSNorm does not inherit the exact-integer simplicity of `intseq`.
A future contract should identify the reference arithmetic and the allowed relation
to it. Important choices include:

- whether low-precision inputs are promoted before residual addition;
- accumulation precision for `sum(u*u)`;
- reduction association and whether deterministic results are required;
- overflow/underflow behavior for large or tiny magnitudes;
- exact versus approximate reciprocal square root;
- epsilon dtype and placement;
- output rounding and optional residual-output rounding;
- NaN/Inf propagation or input exclusions.

Changing the reduction tree can change floating-point results. Therefore two GPU
schedules may be semantically acceptable under a tolerance relation without being
bitwise equal. The tolerance must be fixed before benchmarking; it cannot be widened
because a fast kernel missed the original target.

## 7. Performance reasoning: identify the limiting resource

Before micro-optimizing syntax, estimate the shape of the work:

- bytes loaded/stored per feature for the chosen retention plan;
- arithmetic per feature plus row-level reduction work;
- number of synchronization points and kernel launches;
- register/shared-memory footprint per block;
- active blocks/warps permitted by those resources;
- parallelism available across rows and within a row.

Then profile the real target. Small `D` can be launch/underutilization dominated;
large rows can become bandwidth or reduction dominated; aggressive on-chip
retention can lower traffic while reducing occupancy. These are hypotheses to
measure, not performance claims supplied by this document.

A representation helps when it makes the meaningful choices explicit—row mapping,
reduction strategy, vector width, retention plan—while deriving or hiding incidental
syntax. It hurts when it exposes every backend knob without structure.

## 8. High-information correctness experiments

Use an independent reference implementation and choose shapes/values that attack
mapping and numerical assumptions, not just comfortable powers of two:

- `D` below, equal to, and just above a warp-sized coverage boundary;
- `D` around block/thread/vector-width boundaries, including odd tails;
- unaligned offsets and permitted non-unit strides;
- one row versus many rows;
- zero input/residual, constant rows, mixed signs, very small and large magnitudes;
- gain values that make indexing mistakes visible;
- any legal alias configuration;
- NaN/Inf/subnormal cases when they are in contract.

When a mismatch appears, localize before patching:

```text
wrong only at tails        -> coverage/masking hypothesis
wrong only when >1 warp    -> cross-warp reduction/synchronization hypothesis
row-to-row contamination   -> indexing/ownership hypothesis
small numeric drift        -> accumulation/association/rsqrt hypothesis
shape-dependent launch fail-> legality/resource hypothesis
```

Choose the next experiment that separates competing causes. Do not accumulate
benchmark runs around a kernel whose semantic bug is already localized.

## 9. Evidence required before this becomes an executable pack

A future implementation must supply, at minimum:

1. a versioned operator contract covering the semantic questions above;
2. checked shape/layout/ownership/alias and schedule-legality rules;
3. an actual lowering/backend for every admitted operation/schedule construct;
4. a reference path independent of the generated kernel;
5. adversarial-shape and numerical correctness evidence on named devices;
6. actual target compilation and launch evidence;
7. performance measurements only for accepted kernels, with compiler/device/flags,
   workloads, warm-up, synchronization, repetitions, and timing method recorded.

A generated schedule cannot grant itself GPU access or introduce a backend. Until
those dependencies exist, this file remains a design case.

The reusable lesson is not “add a better warp primitive.” It is: **keep the
semantic reduction domain, data ownership, numerical relation, and schedule
legality explicit enough that a model can choose an efficient implementation
without guessing what correctness means.** This follows the established
algorithm/schedule separation exemplified by Halide.[^halide]

[^nvidia]: https://developer.nvidia.com/blog/using-cuda-warp-level-primitives/
[^halide]: https://halide-lang.org/
