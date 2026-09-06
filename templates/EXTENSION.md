# Semantic/backend extension proposal

Use this only when the existing supported semantics or backend genuinely cannot
provide an important capability. A generated proposal is design data, not a
capability grant. Restrictions and compositional macros should normally stay within
an ordinary capsule; a `NEW_PRIMITIVE` or `NEW_BACKEND` changes trusted machinery
and requires explicit versioned implementation work.

## First prove this is the right layer

Before proposing new semantics, record the strongest existing alternative: direct
code, library/API, current primitives, a transparent macro, or another supported
backend. A failed model attempt is not evidence that the capability is missing.
Prefer an extension only when the limitation is structural and the expected
engineering leverage justifies a larger trusted surface.

## Proposal record

```json
{
  "proposal_id": "REPLACE",
  "base_pack_or_backend_identity": "PIN",
  "class": "NEW_PRIMITIVE | NEW_BACKEND",
  "problem": "WHAT IMPORTANT IMPLEMENTATION FAMILY OR PROPERTY IS CURRENTLY UNSUPPORTED",
  "best_existing_alternative": "WHAT WAS TRIED OR RULED OUT AND WHY",
  "interface": "STABLE ID/SIGNATURE OR BACKEND ENTRY POINT",
  "semantics": "OBSERVABLE BEHAVIOR, INCLUDING ERRORS/EFFECTS/ORDERING",
  "preconditions_and_invariants": "SHAPES, OWNERSHIP, STATE, CONCURRENCY, ALIASING, ETC.",
  "numerical_policy": "EXACT/APPROXIMATE RELATION, FORMATS, ERROR BUDGET, SPECIAL VALUES",
  "resource_model": "ASYMPTOTICS, LIMITS, ALLOCATION/WORK/DEVICE REQUIREMENTS",
  "lowering_or_implementation": "HOW THE MEANING IS REALIZED WITHOUT DELEGATING AUTHORITY TO GENERATED DATA",
  "failure_semantics": "UNSUPPORTED/INVALID/RESOURCE/BACKEND FAILURE BEHAVIOR",
  "compatibility_and_versioning": "OLD IDENTITIES PRESERVED; NEW IDENTITY/MIGRATION IF NEEDED",
  "reference_or_independent_model": "SOURCE OF EXPECTED BEHAVIOR THAT IS NOT THE CANDIDATE LOWERING",
  "discriminating_validation": "SMALLEST TESTS/PROPERTIES/MEASUREMENTS THAT WOULD FALSIFY THE DESIGN",
  "expected_leverage": "WHY THIS REDUCES SEARCH, IMPROVES QUALITY/PERFORMANCE, OR ENABLES A REAL CAPABILITY",
  "status": "PROPOSED_NOT_ADMITTED"
}
```

## Admission bar

A primitive is ready only when its semantics are precise enough that two independent
implementers could disagree in an observable way and the contract would decide
which is wrong. A backend is ready only when its supported domain, ABI/data layout,
resource behavior, failure modes, and semantic relation to its input IR are explicit.

Use the strongest verification mechanism appropriate to the risk: reference or
differential execution, boundary/property tests, sanitizer/static analysis,
numerical error analysis, proof obligations, target-device checks, or performance
measurement. Do not require every mechanism by default; each check should answer a
specific uncertainty.

For performance-motivated extensions, measure the actual target bottleneck after
functional acceptance. Specify asymptotic and memory/resource consequences so a
fast microbenchmark cannot hide a pathological scaling or allocation regime.

Admission produces a new reviewed implementation/version where required. It never
happens because a capsule names the proposed operation or asks for more permission.
