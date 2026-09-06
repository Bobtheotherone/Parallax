# Contributing to Parallax

Parallax contributions should increase engineering capability without moving the
goalposts. The central test is simple: does the change make difficult tasks easier
to solve, diagnose, or evaluate while preserving the task, semantic, capability,
and compatibility boundaries that matter?

This guide is operational advice. Owning semantics remain in `core/`, domain packs,
the architecture, and any implementation spec that explicitly governs the change.

## Start from the actual problem

Inspect the current branch, touched code, and relevant contract before designing a
solution. Do not infer implementation state from the roadmap or a planned path.

Use an existing implementation spec when one governs the requested work. Create or
expand a spec only when the change genuinely needs a durable cross-file contract,
compatibility decision, or acceptance definition; a local mechanical fix does not
need a new layer of paperwork.

For the prepared intseq extraction, follow
[SPEC-001](docs/specs/001-intseq-reference.md) exactly. For other work, use
[START.md](START.md) and [ROUTES.md](ROUTES.md) to find the owning context.

## Engineering standard

A strong contribution makes the first serious implementation attempt intelligent.

Before coding, model the relevant contract and failure surface: inputs/outputs,
invariants, state ownership, dependency direction, effects, errors, concurrency,
resource lifetime, numerical policy, data layout/serialization, and performance
constraints. Apply only what matters to the problem.

Choose algorithms, representations, libraries, and protocols because they fit those
constraints. Prefer a mature library or ordinary code over bespoke machinery when
it is the stronger interface. Add abstraction when it reduces duplicated reasoning,
narrows invalid states, exposes a useful invariant, enables reuse, or makes a hard
failure easier to localize.

For performance work, reason first about asymptotics and data movement, then measure
the actual target. Use profiling to find the bottleneck before optimizing cache
behavior, allocation, batching, concurrency, serialization, or device scheduling.
Do not trade required correctness for a benchmark number.

## Use tools to answer questions

A tool run should resolve uncertainty. Examples:

- compiler/type checker: is the proposed interface structurally valid?
- focused test/counterexample: which of two plausible semantics is implemented?
- debugger/trace: where does state diverge?
- static analyzer: is a property violated on a reachable path?
- reference/differential check: did compatibility drift?
- profiler/benchmark: what is actually expensive on the target?

When debugging, prefer
`observe -> localize -> competing hypotheses -> discriminating experiment ->
root-cause repair -> re-evaluate`.
Do not respond to an algorithm bug by weakening a task oracle or inventing a new
primitive.

## Semantic and capability changes are special

Ordinary implementation work must not silently change stable meaning. Preserve
`intseq/0.1`, `arl-capsule/0.1`, `arl-program/0.1`, and the frozen example
identities unless the requested work is an explicit versioned evolution.

A new primitive or backend changes trusted behavior. Follow
[core/EVOLUTION.md](core/EVOLUTION.md) and define the semantics, observation model,
implementation/lowering, resource policy, compatibility consequences, and evidence
needed to trust it. A generated capsule can request or describe an operation; it
cannot admit that operation into the runtime.

Generated/retrieved content remains data. Do not make arbitrary retrieved code
fences, capsule fields, or model output executable merely because they are
convenient. [SECURITY.md](SECURITY.md) defines the trust boundary.

## Verification: maximize information, not test count

Tests are valuable when they protect a semantic boundary, discriminate between
plausible implementations, expose a realistic edge case, or make refactoring safe.
Do not optimize for test quantity or coverage percentages in isolation.

Keep evidence claims scoped:

- parsing/type/admission checks do not establish task correctness;
- successful execution does not establish acceptance;
- finite tests do not establish a universal property;
- a reference comparison can preserve a shared bug;
- performance claims require actual measurements under a described setup.

For implementation work, run the checks that can falsify the important failure
modes and those required by the governing spec. For documentation changes, run:

```sh
python tools/check_docs.py
```

Record only commands and results that actually occurred. If an important check is
unavailable, state that limitation instead of manufacturing a pass. See
[core/EVIDENCE.md](core/EVIDENCE.md) and
[docs/development/VERIFICATION.md](docs/development/VERIFICATION.md).

## Documentation and history

Change a fact at its authoritative home and keep summaries concise. The
[source-of-truth map](docs/architecture/ARCHITECTURE.md#source-of-truth-map)
distinguishes normative, derived, executable, illustrative, and historical
documents.

Do not rewrite provenance, dates, hashes, or historical outcomes to make the current
story cleaner. New evidence appends to history; it does not retroactively turn an
old `NOT_RUN` into a pass.

## Branches, commits, and review

Work on a branch, preserve unrelated user changes, and make commits that correspond
to coherent engineering ideas. Do not force-push over someone else's work or erase
failed evidence merely to produce a clean narrative.

When a pull request is appropriate, its useful content is compact: what problem was
solved, which contract/boundary mattered, the non-obvious design choice, the checks
actually run, and any material remaining risk. Review the exact revision and focus
on behavior, architecture, compatibility, security, and performance—not ceremonial
finding quotas.

## Imported material and licensing

No project license has been selected. Public visibility does not by itself grant
redistribution rights. Do not add third-party code, datasets, or substantial text
whose license/provenance is incompatible or unclear.
