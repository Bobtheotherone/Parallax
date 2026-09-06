# Context router

Context is an engineering tool. Load the material that can change the next
technical decision; do not optimize for either minimum file count or maximum
repository coverage.

A useful default is:

`task/request -> owning semantics/spec -> touched implementation -> discriminating tools`

Follow transitive dependencies only when their meaning is needed. Stable definitions
can be reused by identity. When a task is genuinely cross-cutting, take the union of
the relevant routes.

| Goal | Load first | What the context should help you decide |
|---|---|---|
| Implement a repository change | User request or named spec; touched code/files; [AGENTS](AGENTS.md) | Observable contract, dependency direction, data/state ownership, error behavior, algorithm/library choice, highest-value checks |
| Implement the prepared intseq extraction | [SPEC-001](docs/specs/001-intseq-reference.md), [reference](runtime/REFERENCE.md), selected `intseq` pack docs, touched code | Exact compatibility surface, separation of library/CLI/self-test, resource behavior, conformance checks |
| Debug a failing implementation | Exact failure/counterexample; owning contract/spec; failing module | Which layer owns the defect and which experiment separates the leading hypotheses |
| Review a repository change | Contract/spec, exact diff, relevant architecture/semantics, actual verification output | Contract drift, architectural errors, missed edge cases, unsafe capability changes, performance/regression risk |
| Choose direct vs adapted solving | [CONTRACT](core/CONTRACT.md), [ECONOMICS](core/ECONOMICS.md), available libraries/packs | Whether representation work removes meaningful search or error surface after full cost |
| Design a capsule | Frozen task, [CAPSULE](core/CAPSULE.md), selected pack, [synthesis algorithm](roles/SYNTHESIZER.md) | Which decisions the model should see, which should be constrained, and how admission/diagnostics expose mistakes |
| Generate a program | Frozen task, admitted capsule + identity, selected pack/tutorial, [PROGRAMMER](roles/PROGRAMMER.md) | Correct algorithm in the available operations; no semantic or capability invention |
| Check task satisfaction | Frozen task, candidate result, independent acceptance path, [EVIDENCE](core/EVIDENCE.md), [REVIEWER](roles/REVIEWER.md) | Whether the requested behavior holds, separately from parsing/type/lowering/execution |
| Diagnose a capsule/program run | Exact diagnostic, [PROTOCOL](core/PROTOCOL.md), owning format/operation | Program bug, capsule bug, identity mismatch, resource limit, missing capability, or task failure |
| Add a primitive or backend | [EVOLUTION](core/EVOLUTION.md), [SEMANTICS](core/SEMANTICS.md), [HOST](runtime/HOST.md), architecture, implementation spec | New meaning, observation model, lowering/backend obligations, resources, compatibility/version boundary |
| Optimize performance | Frozen correctness contract, actual implementation/backend, target measurements; domain pack as needed | Real bottleneck, asymptotics, allocation/layout, batching, concurrency, I/O/serialization, numerical/schedule tradeoffs |
| Reproduce embedded intseq reference | [REFERENCE](runtime/REFERENCE.md), worked [task](examples/intseq/TASK.md), [capsule](examples/intseq/CAPSULE.md), [program](examples/intseq/PROGRAM.md), imported [evidence](examples/intseq/EVIDENCE.md) | Whether a fresh run matches the pinned public reference and exactly what that does or does not establish |
| Study the GPU design case | [RMSNorm](packs/gpu/RMSNORM.md), [SEMANTICS](core/SEMANTICS.md), [HOST](runtime/HOST.md) | Algorithm vs schedule, reduction scope, numerical/ABI obligations, missing backend evidence |
| Run a representation experiment | [benchmark protocol](docs/benchmarking/PROTOCOL.md), [ECONOMICS](core/ECONOMICS.md), frozen task(s), actual host/run artifacts | Fair arms, total cost, acceptance custody, causal ablations, meaningful metrics |
| Research the thesis | [THESIS](research/THESIS.md), [RELATED-WORK](research/RELATED-WORK.md), benchmark protocol, [PROJECT](docs/PROJECT.md) | Mechanism, falsifiable hypothesis, prior work, experiment that would change the design |
| Maintain docs or provenance | Owning document via the [architecture map](docs/architecture/ARCHITECTURE.md#source-of-truth-map), touched sources, [SOURCE-MAP](docs/provenance/SOURCE-MAP.md), checker source | Whether a statement is authoritative, derived, historical, frozen, or executable; whether links/identities stay coherent |

## Route by failure layer

When a result is wrong, do not immediately broaden context or redesign the
representation.

1. Reproduce the observation on the exact artifact/revision.
2. Localize it to contract, representation, checker/lowering, backend/runtime,
   integration/host, or task acceptance.
3. Read the owning layer plus the narrow dependency that can falsify your leading
   explanation.
4. Run the smallest discriminating experiment.
5. Repair the root cause and re-evaluate affected boundaries.

This is usually faster and safer than accumulating logs or escalating every failure
to language evolution.

## Program-generation packet boundary

A solution-generating model needs enough information to solve the task correctly:

- frozen task semantics and input/output/error constraints;
- the admitted capsule identity and callable operations/macros with preconditions;
- relevant resource/numerical behavior;
- compact examples or counterexamples that teach non-obvious composition;
- exact diagnostics from prior public attempts when permitted;
- the required output form.

Do not save tokens by deleting semantic meaning. Conversely, architecture history,
unrelated packs, workflow prose, and final held-out oracle material should not enter
the packet unless they answer a real question.

The current [intseq packet](examples/intseq/PACKET.md) is a frozen derived view for
one example. Its source hashes bind that view; it is not a second specification or
a general context-assembly service.

## When broad reading is correct

Whole-system reading is appropriate for architecture changes, authority/routing
redesigns, semantic evolution, security-boundary work, and research that compares
system mechanisms. Ordinary implementation and debugging should stay local until
evidence says the problem crosses a boundary.
