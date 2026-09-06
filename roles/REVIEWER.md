# Result review algorithm

Review the candidate against the frozen task, not against the story told by the
candidate. Inputs are the task contract, selected semantic pack, capsule/program
identities, implementation/runtime identity, diagnostics, and the evidence that was
actually produced.

The central discipline is to keep four questions distinct:

```text
1. Is the artifact meaningful and permitted in its representation?
2. Does lowering/execution preserve the representation's specified behavior?
3. Does the resulting behavior satisfy the external task contract?
4. Does it meet required resource/performance properties on the named target?
```

A pass at an earlier layer never answers a later question automatically.

## 1. Reconstruct the required behavior first

Compress the contract into independently checkable invariants before relying on the
candidate's structure. Identify:

- input partitions and boundary values;
- required output relation and conservation/provenance rules;
- ordering/state/effect semantics;
- error and exceptional behavior;
- numerical tolerances and association-sensitive operations;
- aliasing/ownership/concurrency constraints where relevant;
- performance conditions that are hard requirements versus optimization goals.

For a difficult codebase, also map component ownership, dependency direction,
state transitions, data movement, retry/idempotency behavior, and external
interfaces. Many severe defects live between individually reasonable functions.

## 2. Build a semantic risk map

Prioritize places where a plausible implementation can be locally valid yet
globally wrong:

- predicates applied before versus after a transformation;
- dropped/duplicated elements or requests;
- boundary inclusivity (`<` versus `<=`);
- empty/zero/one-element cases;
- integer overflow, floating-point reduction order, NaN/Inf policy;
- stale cache or identity binding;
- aliasing and mutation of caller-owned data;
- partial failures, retries, transaction boundaries, cancellation;
- thread/warp/process scope confused with semantic scope;
- serialization/version compatibility;
- resource cleanup and backpressure.

Spend review effort in proportion to consequence and plausibility, not line count.

## 3. Inspect representation and lowering separately

Confirm exact artifact identity, selected operations, scope, types, and required
checker results. For macros or generated helpers, inspect the lowered/expanded form
when available. Ask whether the lowering can introduce behavior not present in the
surface contract or omit a required effect.

A signature, hash, successful parse, or type judgment is structural evidence. It
is useful because it removes classes of failure; it is not proof of the task
algorithm.

For `intseq`, a well-typed expression that filters after an affine transformation
is the canonical reminder: the checker should accept the dataflow, while the task
oracle rejects its result on `[-1,0]`.

## 4. Derive high-information counterexamples

Prefer cases that distinguish competing implementations. A review test should have
a reason to exist beyond increasing a count.

Useful techniques:

- **boundary partitioning:** just below/at/above thresholds and size limits;
- **metamorphic relations:** transformations that imply a predictable output
  relation without duplicating the candidate algorithm;
- **differential checking:** compare against a genuinely separate reference path;
- **adversarial structure:** empty, singleton, duplicates, odd tails, unaligned or
  maximum-size inputs, depending on the domain;
- **state sequences:** reorder/retry/cancel operations to expose lifecycle bugs;
- **fault injection:** make dependency failures occur at ownership boundaries;
- **performance probes:** use workloads that separate latency, bandwidth, memory,
  contention, and asymptotic hypotheses.

When a failure appears, minimize it. A small counterexample usually localizes a
root cause better than a large log.

## 5. Use a diagnostic loop, not a checklist loop

```text
observe
  -> localize failing layer/component
  -> form competing hypotheses
  -> select experiment with maximum discriminating value
  -> confirm or eliminate causes
  -> assess the proposed root fix
  -> rerun the obligations that the fix could affect
```

Do not demand a tool invocation that cannot change the decision. Conversely, do
not rely on prose confidence where a cheap compiler, interpreter, static analyzer,
profile, property check, or targeted test can settle the question.

## 6. Evaluate evidence for scope and independence

For every consequential claim, ask what produced it and what it actually covers.
Keep these dimensions separate:

- **authorship independence:** who specified the expectation;
- **implementation diversity:** whether expected and actual results use different
  mechanisms;
- **hold-out status:** whether evaluation inputs were unavailable to the generator;
- **coverage scope:** exact finite domain, property family, theorem assumptions, or
  measured workload;
- **artifact identity:** which candidate/runtime/environment the result applies to.

A same-model second pass can find bugs but is not independent ground truth. A
candidate-derived test can be useful for debugging but is circular as the sole
acceptance oracle. Historical or source-reported evidence remains historical until
rerun against the reviewed revision.

## 7. Review performance as an engineering property

Only optimize or endorse performance after functional gates required by the task
pass. Check whether the implementation targets the actual bottleneck rather than a
proxy metric.

Depending on the system, inspect asymptotic complexity, allocation lifetime,
memory layout/cache locality, I/O batching, serialization, synchronization,
contention, accelerator transfers, launch overhead, and numerical precision. A
larger test suite does not compensate for an algorithm with the wrong complexity
or a design that serializes the critical path.

Require measurements on the stated target for quantitative performance claims.
Estimated cost and measured cost must remain distinguishable.

## 8. Classify findings by consequence

A useful finding states the violated contract, a concrete triggering condition,
the observed or logically implied consequence, and the smallest convincing repair
direction. Distinguish:

- task-semantic defect;
- representation/lowering defect;
- backend/runtime defect;
- resource/performance defect;
- missing required evidence;
- unsupported capability or environment limitation.

Do not inflate stylistic preferences into correctness findings. Do not downgrade a
contract violation because the implementation is otherwise elegant.

## 9. Acceptance decision

Accept only under the predeclared task policy for the exact reviewed artifacts.
If a required check is unavailable, say that it is unavailable. If evidence is
insufficient, return the narrow unresolved obligation or counterexample rather than
a generic confidence label.

Preserve task acceptance outside generated authority. Never repair a failing
candidate by silently changing the oracle, tolerance, input bounds, semantic pack,
or required behavior.
