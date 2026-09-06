# Context router — experimental branch

Context is an engineering tool. On this branch every substantial coding task also
has a **task-language design phase**, so load the material needed both to understand
the real task and to build a correct lowering path.

Default route:

`task/request -> owning contract/implementation -> AI-native language synthesis -> frozen language program -> lowering target/tools -> external acceptance`

Read [AGENTS.md](AGENTS.md) first. The mandatory language treatment overrides any
older suggestion elsewhere that direct/native code should be the default model-facing
representation.

| Goal | Load first | What the context should help you decide |
|---|---|---|
| Implement a repository change | User request/spec; touched code/files; [AGENTS](AGENTS.md); [SYNTHESIZER](roles/SYNTHESIZER.md) | Task invariants plus the task-specific language vocabulary/types/dependencies that should encode the change before host code is written |
| Design the task language | Frozen task; touched architecture/code; [CAPSULE](core/CAPSULE.md); [SYNTHESIZER](roles/SYNTHESIZER.md) | Canonical grammar, operators, types/shapes/states/resources, legal compositions, lowering mapping, and diagnostics |
| Generate a candidate | Frozen task; frozen task-language definition/identity; [PROGRAMMER](roles/PROGRAMMER.md); lowering contract | Correct algorithm expressed in the generated language before host implementation |
| Lower into repository code | Task-language program; explicit lowering map; target APIs/libraries/modules/backends | Faithful deterministic translation without silently changing task or language semantics |
| Implement the prepared intseq extraction | [SPEC-001](docs/specs/001-intseq-reference.md), [reference](runtime/REFERENCE.md), intseq pack docs, touched code, experimental task language | Exact compatibility plus an AI-native representation of the extraction/refactor decisions before Python implementation |
| Debug a failing implementation | Exact failure/counterexample; task-language definition/program; lowering; failing host module | Whether the defect belongs to language acquisition, algorithm, lowering, host implementation, resource behavior, or acceptance |
| Review a repository change | Frozen task/spec, generated language/program, exact host diff, relevant architecture/semantics, actual verification | Whether the treatment was genuinely used and whether language→implementation preserved the contract |
| Check task satisfaction | Frozen task, candidate behavior, independent acceptance path, [EVIDENCE](core/EVIDENCE.md), [REVIEWER](roles/REVIEWER.md) | Whether requested behavior holds separately from language validity/lowering/execution |
| Add a real primitive/backend | [EVOLUTION](core/EVOLUTION.md), [SEMANTICS](core/SEMANTICS.md), [HOST](runtime/HOST.md), architecture | Whether a generated virtual instruction lowers to existing meaning or requires an actual trusted capability implementation/version change |
| Optimize performance | Frozen correctness contract, generated language/program, lowering/backend, target profile/measurements | Which low-level algorithm/layout/schedule/resource decisions the task language should expose and whether the backend realizes them |
| Reproduce embedded intseq reference | [REFERENCE](runtime/REFERENCE.md), worked task/capsule/program/evidence | Pinned compatibility behavior; this is a reference/lowering target, not a waiver of the experimental methodology for new work |
| Run the `main` vs `experimental` comparison | [benchmark protocol](docs/benchmarking/PROTOCOL.md), same frozen tasks, both branch SHAs, actual run artifacts | Whether mandatory AI-native language synthesis changes accepted-solution quality/cost relative to adaptive Parallax |
| Research the hypothesis | [PROJECT](docs/PROJECT.md), [THESIS](research/THESIS.md), benchmark protocol, actual experiment data | Mechanism, task families, useful language properties, and evidence that would support/refute the methodology |
| Maintain docs/provenance | Owning document via architecture map; touched sources; provenance/checker | Historical/current truth and link/identity coherence; trivial prose-only fixes may use `TRIVIAL_DIRECT` |

## Language-design packet

The synthesizer needs enough context to construct a genuinely task-specific language:

- frozen observable task and acceptance policy;
- current repository/target architecture that constrains lowering;
- relevant libraries/APIs/semantic packs as **implementation targets**;
- data shapes, state machines, ownership/effects, numerical/resource rules, and
  performance constraints that matter;
- likely algorithm families and failure surface;
- tool/compiler/backend capabilities actually available.

Do not include final held-out oracle material or secret capabilities. The language
may describe a requirement; generated text cannot grant it.

## Program-generation packet

Once the language is frozen, the programmer should receive:

- frozen task semantics;
- frozen language grammar/identity;
- operator/instruction signatures and lowering meaning;
- relevant type/shape/state/effect/resource rules;
- a small set of contrastive examples when needed;
- exact prior diagnostics permitted by the experiment;
- required task-language output form.

The programmer should not receive an already-written host-language solution and then
translate it into the new language. That would not test the proposed mechanism.

## Route by failure layer

1. Reproduce the exact observation.
2. Determine whether the earliest failing boundary is task understanding, language
   definition, task-language program, lowering, host implementation/backend,
   resource/performance behavior, or external acceptance.
3. Read the owning layer plus the smallest dependency that can falsify the leading
   explanation.
4. Run the smallest discriminating experiment.
5. Repair the root cause.

Only revise the frozen language between attempts when evidence says its representation
is the problem. A wrong algorithm expressed perfectly in the language is still a
wrong algorithm.

## When broad reading is correct

Whole-system reading is appropriate when the task language must span many components,
when changing architecture/trust boundaries, or when evaluating the methodology.
Ordinary implementation details should still be loaded because they constrain real
lowering—not because documentation links exist.
