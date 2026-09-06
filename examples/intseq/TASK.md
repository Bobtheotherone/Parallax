# Worked task: sum transformed original nonnegative integers

Compute the exact sum of `3*v + 5` for every input element `v` that is
**nonnegative in the original input**. Preserve multiplicity. If no element
qualifies, return zero.

This task is deliberately small enough that the contract, representation, lowering,
execution, and independent task check can all be inspected. Its direct solution is
also small; the example demonstrates Parallax's semantic boundaries, not an
assertion that capsule construction is economically preferable here.

## Contract compressed to invariants

For an in-domain sequence `x = [v_0, ..., v_{n-1}]`, define each element's
contribution independently:

\[
c(v)=\begin{cases}3v+5 & v\ge 0\\0 & v<0\end{cases},
\qquad F(x)=\sum_i c(v_i).
\]

A solver should preserve these properties:

- **predicate provenance:** qualification depends on the original `v`, not on a
  transformed value;
- **multiplicity:** repeated qualifying values contribute repeatedly;
- **empty identity:** `F([])=0`;
- **exact arithmetic:** no wrapping, saturation, or approximation;
- **decomposition:** `F(a ++ b) = F(a) + F(b)` for in-domain sequences;
- **order is observationally irrelevant to this particular scalar result**, even
  though the `intseq` sequence primitives themselves preserve order.

The most informative small counterexample for operation ordering is `[-1,0]`:
filter-then-transform gives `5`, while transform-then-filter gives `7`. A candidate
that passes typechecking but fails this case has an algorithm/dataflow error, not
a missing type rule.

## Domain versus runtime policy

The task domain is lists of length `0..4096` whose elements are integers in
`[-1000000,1000000]`. The `intseq` runtime also has pack-level resource limits.
Those are separate concerns: a host should enforce the task domain, while the
runtime may reject resource excess. A resource rejection is not permission to
change the mathematical result or weaken the contract.

## Frozen contract record

```json
{
  "task_id": "nonnegative-affine-sum",
  "contract_version": "0.1",
  "requirement_owner": "example author",
  "requirement_source": "this worked example",
  "input_domain": "list x of 0..4096 integers, each in [-1000000,1000000]",
  "output_relation": "sum(3*v+5 for each v in x satisfying v>=0)",
  "observable_effects": [],
  "error_behavior": "out-of-domain inputs are outside this task contract; runtime may additionally reject resource excess",
  "numerical_policy": "exact integers; zero for an empty sum",
  "target_environment": "bundled intseq interpreter on Python",
  "hard_constraints": ["exact result", "no task-data I/O within the expression"],
  "optimization_goal_after_acceptance": "none for this demonstration",
  "acceptance_policy": "public bounded exhaustive and randomized differential tests; no universal proof claim",
  "oracle_source_and_review": "direct-loop oracle in runtime/REFERENCE.md; same project authorship, different implementation path",
  "public_examples": [
    {"input": [], "output": 0},
    {"input": [-1,0], "output": 5},
    {"input": [-2,-1,0,2], "output": 16}
  ],
  "unresolved_assumptions": [],
  "total_budget": "demonstration tests only; no model search performed",
  "mode": "CAPSULE",
  "frozen": true
}
```

## Acceptance boundary

The public policy checks a bounded exhaustive region and randomized inputs against
a direct-loop oracle. It is useful finite evidence, not a proof over the whole
contract domain. The oracle and AST interpreter use different implementation paths
but share project authorship, and all inputs are public.

The capsule/program checker is intentionally **not** the task oracle. It should
accept structurally valid programs even when they implement the wrong operation
ordering. This keeps a valuable diagnostic distinction:

```text
schema / allowlist / hash / type / expansion  -> representation validity
execution under runtime limits                -> runtime result
comparison with this frozen contract           -> task acceptance
```

When constructing a solution, first derive the contribution rule and provenance
constraint above, then map that plan to the available operations. Do not infer the
contract from whichever expression happens to typecheck.
