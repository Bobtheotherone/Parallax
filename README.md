# Parallax

**Engineer the representation, keep the meaning fixed.**

Parallax is a research engineering system for giving a coding model the interface
that best exposes a problem's structure without letting that interface redefine the
problem. Sometimes the best interface is ordinary code or a mature library.
Sometimes it is a smaller typed API, schema, DSL, macro set, or schedule space.
Parallax exists to make that choice explicit, checkable, and measurable.

The objective is not “generate a language.” It is to increase the probability of a
high-quality accepted solution per unit of total engineering cost.

## The mechanism

```text
frozen task + acceptance
          |
          v
choose representation  ----> DIRECT / existing library
          |
          +------------> CAPSULE over a pinned semantic pack
                              |
                              v
                    program / implementation
                              |
                  check + expand/lower
                              |
                              v
                    interpreter / backend
                              |
                              v
                         behavior
                              |
                              v
                 external task acceptance
```

A capsule can select operations, constrain invalid choices, expose types, compose
checked macros, or present examples that reveal the right decomposition. It is
useful when those choices compress the model's search space or make important
invariants mechanically visible. It is unnecessary when native code already gives
the model the stronger interface.

The key separation is:

`representation validity != execution != task correctness`

A well-typed program can still implement the wrong algorithm. A generated artifact
can describe a capability without possessing it. A fast result is irrelevant if it
fails the task.

## Engineering principles

Parallax is built around a few hard boundaries:

- **Task meaning is external.** Representation search cannot quietly change the
  requested output, tolerated errors, input domain, side effects, or acceptance
  policy.
- **Semantics are stable and versioned.** Capsules adapt a surface over pinned
  domain meanings rather than inventing trusted primitives on every attempt.
- **Generated artifacts are data.** The host grants machine capabilities; a
  capsule/program cannot grant itself network, filesystem, process, model, native,
  or oracle access.
- **Acceptance is separate.** Typechecking, lowering, execution, public tests, and
  final task acceptance answer different questions.
- **Total cost matters.** Representation construction, examples, retries, tools,
  verification, and failed attempts count. A short final program is not evidence
  that the system solved the task cheaply.
- **Tools should reduce uncertainty.** Compilers, interpreters, debuggers,
  profilers, references, differential/property checks, and targeted tests are most
  valuable when they discriminate between plausible explanations.

See [core semantics](core/SEMANTICS.md), [capsules](core/CAPSULE.md),
[task contracts](core/CONTRACT.md), and [economics](core/ECONOMICS.md).

## Current repository

This is a **pre-production research prototype**, not a deployed coding platform.

Present today:

- the task/semantic/capsule/evidence model and architecture;
- the stable `intseq/0.1` example pack and legacy `arl-capsule/0.1` /
  `arl-program/0.1` artifact formats;
- an embedded standard-library Python reference implementation in
  [runtime/REFERENCE.md](runtime/REFERENCE.md);
- worked positive and well-typed-but-wrong examples;
- documentation integrity tooling;
- [SPEC-001](docs/specs/001-intseq-reference.md), a prepared engineering contract
  for extracting the embedded reference into an ordinary Python package.

Not present today: a packaged Parallax runtime, model-orchestration host, isolated
final oracle, native/GPU backend, production sandbox, or completed LLM
representation benchmark. The imported intseq run report is historical source
evidence, not a fresh validation of this repository state.

The project maturity baseline is owned by [docs/PROJECT.md](docs/PROJECT.md).

## A small example with a large lesson

The worked task sums `3*v + 5` only for values that were nonnegative **before** the
transformation. Under the intseq capsule, both of these ideas can be well-typed:

```text
filter original values -> transform -> sum     # task-correct
transform -> filter transformed values -> sum  # wrong on [-1, 0]
```

The second returns `7`; the task requires `5`. The type system should not be
“improved” to pretend it knows arbitrary task intent. The right diagnosis is an
algorithm/order error, found by a separate task oracle. This is the separation
Parallax is designed to preserve at larger scale.

## Navigate

- **Start engineering work:** [START.md](START.md)
- **Select context by question:** [ROUTES.md](ROUTES.md)
- **Understand project scope:** [docs/PROJECT.md](docs/PROJECT.md)
- **Understand system boundaries:** [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md)
- **Design a task-adapted interface:** [core/CAPSULE.md](core/CAPSULE.md)
- **Understand the synthesis loop:** [core/PROTOCOL.md](core/PROTOCOL.md)
- **Work with intseq:** [packs/intseq/PACK.md](packs/intseq/PACK.md) and
  [packs/intseq/CAPSULE.md](packs/intseq/CAPSULE.md)
- **Evaluate the research claim:** [docs/benchmarking/PROTOCOL.md](docs/benchmarking/PROTOCOL.md)
  and [research/THESIS.md](research/THESIS.md)
- **Contribute:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Security/trust model:** [SECURITY.md](SECURITY.md)

`python tools/check_docs.py` checks documentation structure, local links,
provenance coverage, selected frozen identities, and spec metadata. It does not
execute the intseq runtime or establish semantic/task correctness.

No project license has been selected.
