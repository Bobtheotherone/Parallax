# Semantic boundaries: define what implementations must preserve

Parallax adapts interfaces over stable domain meaning. The permanent abstraction is
not one universal graph; it is a set of domain packs whose observable behavior is
precise enough that multiple representations and backends can be compared.

## Semantic object

For a semantic pack `K`, environment/backend `E`, and primitive program/IR `i`, use
an outcome model rather than a value-only function:

```text
⟦i⟧(K,E,x) -> Value(v)
             | Error(kind, detail)
             | ResourceReject(kind)
             | Effects(trace, final_state, v)
```

A domain may add nondeterminism, streams, distributed observations, timing classes,
or other structure. The observation model must say which distinctions matter.

For capsule `C`, let `Expand_C(p)` map a capsule program to the stable pack-level
representation. Let `Run_K,E` implement that representation. Let `Phi_T` be the
external task acceptance relation. Then:

```text
primitive_ir = Expand_C(program)
outcome      = Run_K,E(primitive_ir, input)
accepted     = Phi_T(input, outcome, evidence)
```

These are different obligations. A correct lowering of the wrong algorithm still
fails the task.

## Representation preservation

A representation transformation is valid only relative to a stated semantic
relation. For exact pure intseq, equality of mathematical outcomes is the natural
relation when both evaluations succeed. Other domains may require something else:

```text
R(source_observation, target_observation, assumptions)
```

Examples:

- floating-point lowering: bounded absolute/relative/ULP error plus NaN/Inf rules;
- concurrent system: allowed traces, ordering, atomicity, progress, retry/idempotency;
- protocol: externally visible state transitions and wire compatibility;
- storage: persisted schema, ordering, durability, migration behavior;
- accelerator kernel: tensor values within tolerance plus shape/layout/alias rules.

Do not call two implementations semantically equivalent until the relevant `R` is
defined. Matching function signatures or JSON fields is insufficient.

For a pure compositional macro, define its meaning by hygienic expansion into
admitted operations. This removes a competing informal macro semantics. It does
not prove that the expander or primitive implementation is correct.

## Semantic dimensions that engineering agents must surface

When a domain uses them, make these explicit at interfaces:

- **data:** type, shape, units, ordering, encoding, layout, aliasing;
- **state/effects:** reads, writes, external I/O, transactions, emitted events;
- **errors:** categories, partial results, retries, cancellation, idempotency;
- **ownership/lifetime:** who may mutate/free/share data and when;
- **concurrency:** synchronization, ordering, atomicity, progress assumptions;
- **numerics:** format, accumulation order, overflow, rounding, tolerance,
  determinism/reproducibility;
- **resources:** which limits are semantic/contractual versus host policy;
- **security/capabilities:** which effects require externally granted authority;
- **observability:** which outputs/traces/timing/resource facts acceptance may see.

A type system should encode dimensions that materially remove invalid programs;
do not turn every concern into a type merely because it can be named.

## Semantic scope is not execution schedule

Keep **what is computed** separate from **how a backend schedules it**. A reduction
over an entire feature axis does not become a warp-local reduction because a GPU
implementation uses warp primitives. A transaction's atomic semantic scope does
not become whatever lock granularity is convenient. A stream's ordering contract
does not become scheduler order by accident.

Backends may choose tiling, batching, vector width, thread mapping, memory layout,
reduction tree, caching, fusion, or other schedules only when the resulting
observation remains within the defined semantic relation.

This separation gives Parallax useful representation leverage: a capsule can expose
schedule choices to the model without forcing it to redefine the algorithm.

## Resource and failure semantics

Mathematical meaning and execution policy are related but distinct. A host/backend
may reject a semantically meaningful computation because it exceeds declared
limits. That is `RESOURCE_LIMIT`/resource rejection, not mathematical falsehood.
Two mathematically equivalent expressions can legitimately consume different
resources or hit different intermediate limits.

When resource behavior itself is externally required—for example latency SLO,
memory ceiling, bounded message count, or real-time deadline—it belongs in the task
contract and acceptance relation. Otherwise treat it as an implementation/search
constraint and report it separately.

## Numerical semantics

Never infer floating-point equivalence from algebraic equality. Specify operand and
accumulator formats, rounding, reduction order constraints, exceptional values,
allowed reassociation/approximation, and the composed error relation required by
the task. Measure or analyze the target behavior that actually matters.

## intseq/0.1 compatibility

The established intseq semantics remain exact mathematical integers and ordered
finite integer sequences with the seven primitive meanings in
[PACK.md](../packs/intseq/PACK.md). The reference may reject inputs or intermediate
computations under its fixed resource policy; it never silently wraps, saturates,
or approximates. Existing `intseq/0.1`, `arl-capsule/0.1`, and `arl-program/0.1`
meanings are preserved.
