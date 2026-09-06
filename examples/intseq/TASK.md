# Worked task: sum transformed original nonnegative integers

Compute the sum of `3*v + 5` for every element `v` of the input that is originally
nonnegative. Preserve multiplicity. Return zero when no elements qualify.

This task is intentionally simpler than a GPU kernel so the entire supported
semantic path can be inspected and run. Its direct implementation is short; no
claim is made that inventing a capsule is economically preferable on this task.

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

The interpreter checks pack-level bounds, not the example's narrower task domain.
The example's tests supply in-domain inputs. A general harness must enforce its
own task domain and oracle separately.
