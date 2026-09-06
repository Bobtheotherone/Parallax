---
id: SPEC-001
status: ready-for-dev
spec_version: 1
created: 2026-09-05
depends_on: []
---
# Package and characterize the intseq reference

## Intent

Turn the existing embedded intseq reference into an importable, locally runnable,
tested Python project **without redesigning its semantics**. A fresh checkout
should support library calls and a documented CLI without extracting Markdown
by hand or installing third-party packages.

This is one reference-extraction/conformance episode, not a host-loop project.
It is the first public Parallax LLM-development task. The repository supplies the
reference source openly; the task measures engineering against a contract, not
unaided invention of the algorithm. No implementation is included in this spec.

## Required context

Read these authoritative inputs; do not recursively load research or unrelated
routes:

- [Development workflow](../development/WORKFLOW.md) and
  [verification strategy](../development/VERIFICATION.md).
- [Semantic obligations](../../core/SEMANTICS.md),
  [evidence meanings](../../core/EVIDENCE.md),
  [intseq operations/limits](../../packs/intseq/PACK.md), and
  [capsule/program formats](../../packs/intseq/CAPSULE.md).
- [Embedded reference](../../runtime/REFERENCE.md) in full and
  [host boundary](../../runtime/HOST.md). The Python fence is the compatibility
  reference, not an independently established correctness oracle.
- The public [task](../../examples/intseq/TASK.md),
  [capsule](../../examples/intseq/CAPSULE.md),
  [program](../../examples/intseq/PROGRAM.md), and
  [typed-but-wrong case](../../examples/intseq/FAILURE.md).
  [Imported evidence](../../examples/intseq/EVIDENCE.md) supplies historical
  expected report shape/counts, not proof that a new implementation passes.

If the prose semantics and reference contradict each other on an observed case,
record the minimal case and block the affected work pending an explicit decision.
Do not silently choose a new semantic interpretation. No such unresolved conflict
is required to implement the specified slice as reviewed at bootstrap.

## Approach and tooling choice

Use a flat local package named `parallax`, CPython 3.11 or newer, and standard-library
`unittest`. Run from the repository root; installation is not required. Keep
semantic mechanisms in `parallax.intseq`, command adaptation in `parallax.__main__`,
and public demonstration/self-test logic in `parallax.selftest`.
Private helpers may be organized intelligently; a large framework is unnecessary.

No wheel/build backend, dependency manager, external testing package, CI workflow,
or supported-version matrix is required in this episode. Record the exact Python
version actually exercised. Acceptance commands use ordinary, **non-optimized**
Python; do not run the assert-based reference self-test with `-O` or
`PYTHONOPTIMIZE`. Compatibility with every Python version is not established by
one environment's pass.

## Invariants

The normative intseq signatures, exact integer operations, left-to-right eager
argument evaluation and sum accumulation, intermediate resource checks, operation
allowlist, macro scope, and limits remain unchanged. Resource equivalence is not
inferred from mathematical equivalence.

Keep `intseq/0.1`, `arl-capsule/0.1`, `arl-program/0.1`, the canonical JSON recipe,
and the example capsule/program identities unchanged. Do not rewrite frozen pack,
schema, task, capsule, program, or programmer-packet sources to accommodate code.
The reference Python fence remains the frozen baseline, not a second actively
edited runtime.

Generated artifacts remain data. No generated Python execution, arbitrary imports,
permission grants, network calls, model calls, new primitive, new macro-body
capability, or oracle access is introduced. Imports must not execute the CLI,
run self-tests, or access files. Evaluation must not mutate caller artifacts/input.

A successful ordinary CLI invocation still reports `task_correctness: NOT_CHECKED`.
The wrong but well-typed example must remain structurally accepted and functionally
wrong, demonstrating the distinction rather than making the type checker an oracle.

## Non-goals

No LLM host/orchestration, context-packet service, experiment scheduler, task-contract
parser, hidden-test harness, native/GPU backend, optimizer, hole solver, configurable
semantic limits, generalized JSON language, formal proof, sandbox, performance
optimization, or package publication. Do not add semantic features or “improve”
the reference's intentionally limited grammar. Documentation updates must stay
within what this implementation actually establishes.

## Interfaces and observable behavior

### Library

Expose these names from `parallax.intseq`, retaining their reference contracts:

| Interface | Observable contract |
|---|---|
| `Rejection` | A `ValueError` subtype with stable `.code`; its message includes code and diagnostic detail |
| `strict_json(text)` | Bounded UTF-8 JSON parsing; duplicate keys and NaN/Infinity rejected |
| `canonical(obj)` / `digest(obj)` | Canonical JSON bytes / lowercase SHA-256 hex using the reference recipe; no trailing newline in canonical bytes |
| `read_document(path)` | Read a bounded UTF-8 Markdown file with exactly one supported lowercase `json` fence; surrounding prose has no authority |
| `validate_capsule(cap)` | Return `(signatures, macro_definitions)` or reject; signature values remain `(argument-type tuple, result type)` and definitions are keyed by `macro.NAME` |
| `check_program(cap, prog)` | Validate binding/types, expand, recheck, and return the primitive expression tree |
| `evaluate(cap, prog, x)` | Return `(value, expanded_ir)` or reject under the original resource policy |

Public inputs are ordinary Python built-ins representing parsed JSON; supporting
custom objects or arbitrary Python code is outside the contract. Diagnostic prose
need not be byte-identical, but the specified rejection codes and result shapes
must be. Preserve the original literal-vs-variable-vs-call grammar: arrays in
expressions are applications, not vector literals; booleans/floats are not ints.

### CLI

`python -m parallax` replaces only the invocation prefix `python reference.py`.
Preserve `--capsule PATH`, `--program PATH`, `--input JSON` (default `[]`), and
`--selftest`. Paths may be ordinary caller-authorized local paths; no new sandbox
or restriction to the examples directory is implied.

On ordinary success: exit `0`, one JSON object on stdout, no diagnostic on stderr,
with exactly `status`, `value`, `expanded_ir`, `capsule_sha256`, `program_sha256`,
and `task_correctness`. Their semantics are the reference's: `EVALUATED` and
`NOT_CHECKED`, not task acceptance. JSON whitespace/key ordering in stdout is not
a compatibility requirement.

On handled artifact, I/O, or UTF-8 rejection: exit `2`, stdout empty, one JSON
object on stderr with exactly `status: REJECTED` and a useful `detail`. Rejection
details include the stable code when a `Rejection` caused them. Missing required
capsule/program flags follow this path (`SCHEMA`). Argument-parser usage errors
(e.g. an unknown flag) retain argparse's text stderr/exit `2`; they are not
required to become JSON. `--help` exits `0` without reading artifacts.

`--selftest` needs no paths and takes precedence over artifact evaluation, as in
the reference. Successful normal-mode output retains the reference JSON shape:
`status: PASS`, counts, Python version, capsule/program hashes, and the
`typed_but_wrong_counterexample`. Failed checks must not be suppressed or reported
as a pass. The self-test is public demonstration evidence, not an acceptance
oracle for arbitrary user tasks.

### Cases that must stay distinguishable

| Case | Required observation |
|---|---|
| Example program with `[-2,-1,0,2]` | Value `16`; primitive IR is `['seq.sum',['seq.add',['seq.mul',['seq.filter_ge','x',0],3],5]]` |
| Example with `[]`, `[-3,-1]`, `[0,0,2]` | Values `0`, `0`, `21` respectively |
| Wrong-order expression from FAILURE on `[-1,0]` | Admitted; value `7`; separately specified task answer `5` |
| Wrong capsule digest | `HASH_MISMATCH` |
| `seq.sum` applied to `3`, wrong arity, or unbound `y` | `TYPE` |
| Known but non-allowlisted `seq.count`, or an unknown primitive | `OP_NOT_ALLOWED` |
| Boolean expression leaf | `SCHEMA`; no implicit bool-to-int coercion |
| Boolean/float element in input | `TYPE` |
| Non-list input or more than 4,096 elements | `RESOURCE_LIMIT`, as in the reference |
| Parsed integer with more than 256 magnitude bits; overflowing intermediate | `RESOURCE_LIMIT`, not wrapping or approximation |
| Extra capsule/program/macro fields, duplicate JSON keys, non-JSON constants | `SCHEMA` |
| Macro body calls itself or another macro | `OP_NOT_ALLOWED`; nested macro calls in a program remain permitted |
| Duplicate primitive within the allowed list length | `SCHEMA`; a list exceeding seven entries is rejected earlier as `OP_NOT_ALLOWED` |
| Nested `shift` macro with parameters `x:VecInt,v:Int`, applied with offsets 2 then 3 to `[1,2]`, then summed | Value `13`; lexical substitution does not capture the caller's `x` |

Maintain MAX_BYTES=65,536, MAX_DEPTH=32, MAX_NODES=4,096, MAX_VECTOR=4,096,
MAX_BITS=256, MAX_WORK=250,000, at most 16 macros, and 1–8 parameters. Preserve
where the reference charges visits/intermediates; an expansion budget is not
merely a final-IR-size check. Tests should isolate these budgets rather than
mistaking an earlier type/depth rejection for the intended boundary check.

## File map

| Path | State / work |
|---|---|
| `runtime/REFERENCE.md` | Existing frozen Python baseline; source fence unchanged |
| `packs/intseq/{PACK,CAPSULE,TUTORIAL}.md` | Existing meaning/schema/example context; no semantic edits |
| `examples/intseq/{TASK,CAPSULE,PROGRAM,FAILURE,EVIDENCE,PACKET}.md` | Existing public fixtures/history; preserve historical evidence and identities |
| `parallax/__init__.py` | New local package, import without side effects |
| `parallax/intseq.py` | New semantic library and public interfaces above |
| `parallax/__main__.py` | New CLI adapter |
| `parallax/selftest.py` | New public sample builders, direct-loop oracle, self-test; evaluator must not import its oracle |
| `tests/test_intseq.py` | New primitive, admission, scope, expansion, limits, and independently expected task checks |
| `tests/test_cli.py` | New subprocess CLI, rejection, import, and frozen-reference parity checks |
| `.gitignore` | Existing documentation-tool cache/environment exclusions; extend only if needed and do not ignore evidence by default |
| `README.md`, `docs/PROJECT.md`, `runtime/HOST.md` | Update only demonstrated capability/usage facts; retain historical-vs-current distinction |
| `runs/<run-id>/` | New actual development evidence/logs; use the run template, not fabricated fixtures presented as results |

No files under `parallax/` or `tests/` exist at the bootstrap baseline. Test fixtures
may be constructed in tests or stored under `tests/fixtures/`; the public Markdown
artifacts must also be exercised directly to catch integration drift.

## Implementation tasks

- Characterize the frozen reference in a temporary directory using its documented
  extraction recipe; retain the source hash, environment, command results, and
  any discrepancy. Never execute an arbitrary fence or modify the baseline.
- Extract and separate library, CLI, and demonstration concerns. Preserve observable
  behavior; do not import/read the Markdown reference at production runtime.
- Add contract-derived tests, resource/admission/scope cases, reference parity, and
  subprocess coverage. Separate the demonstration's legacy counters from new tests.
- Run the acceptance plan, record new evidence, update demonstrated usage/maturity,
  and submit the spec/diff/evidence for review. Leave unavailable checks explicit.

## Acceptance criteria

| ID | Acceptance condition | Required verification |
|---|---|---|
| AC1 | Local import and CLI work without third-party packages or import side effects | Import/subprocess tests; run CLI with `python -S`; no packaged runtime reads Markdown source |
| AC2 | Library contracts, all seven primitives, ordering/duplicates/empty cases, and exact arithmetic match pack semantics | Contract-derived unit tests, including intermediate overflow despite a bounded final mathematical result |
| AC3 | Schema, allowlist, hash, type, macro naming/count/parameter, scope, and resource rejection behavior is preserved | Tests for the table above and each documented bound; assert rejection **codes**, not just that any exception occurred |
| AC4 | Macro lowering is hygienic, rechecked, and bounded; caller data is not mutated | Exact expanded example IR; nested shadowing gives `13`; reject macro-body chaining/recursion and expansion over budget |
| AC5 | Public demonstration behavior is preserved without conflating task success | Self-test counts are 2,801 bounded inputs, 1,000 seeded random inputs, 700 primitive checks, 17 rejection checks, 1 macro-scope check; wrong-case 7 vs 5 retained |
| AC6 | Expected task values come from a direct-loop implementation, not the candidate AST or its lowering | Enumerate lengths 0..4 over -3..3; randomized seed 20260905/1,000 vectors of length 0..64 in ±1,000,000; report these exact finite scopes |
| AC7 | CLI success and failure streams/exits/shapes match the interface | Subprocess tests for example, defaults, self-test, help, missing flags/files, invalid UTF-8/JSON, and typed rejection |
| AC8 | Compatibility is demonstrated against the unchanged original source, not assumed from extraction | Compare reference and package self-test JSON except environment version; compare example and representative rejected CLI cases, exits and stable codes |
| AC9 | No semantic/identity/authority expansion or invented maturity claim is introduced | Documentation check, diff review of invariants/non-goals, fresh evidence with missing checks marked |

For byte-size limits, exercise a supported document/JSON value at the limit and
just beyond it. For tree/work/expansion limits, exercise feasible near-boundary
and over-bound cases while satisfying earlier checks. Explicitly cover maximum
vector length and positive/negative magnitude boundaries. A good program that
passes public tests and a wrong program that passes typechecking must both exist
in the suite. Do not “fix” AC6 by deriving its oracle from `evaluate`.

## Verification plan

The following **runtime commands are planned and have not run in the bootstrap**.
Execute from the repository root on the implementation branch:

```sh
python --version
python -m unittest discover -s tests -v
python -S -m parallax --help
python -m parallax --selftest
python -m parallax --capsule examples/intseq/CAPSULE.md --program examples/intseq/PROGRAM.md --input '[-2,-1,0,2]'
python -m parallax --capsule examples/intseq/CAPSULE.md --program examples/intseq/PROGRAM.md --input '[true]'
```

Expected: discovery reports a nonzero suite with all required tests passing;
help exits 0; self-test has AC5's scoped counts; ordinary evaluation has value 16,
`EVALUATED`/`NOT_CHECKED`; boolean input exits 2 with `REJECTED`/`TYPE` on stderr.
The last command is an intentional negative test, not a failing acceptance run.

Also run the existing `python tools/check_docs.py`. Capture reference subprocess
parity inside tests or the evidence run, with the frozen fence SHA-256
`4025a0043e958785196e35d6530ec4570dcedd36cf621b555249a1809649dc91`
checked before executing the temporary baseline. Do not count baseline extraction
or matching hashes as task-correctness evidence.

Record command results, exact source commits, artifact identities, environment,
stdout/stderr, unittest count, known failures, and NOT_RUN fields. Unit and
reference passes are insufficient for an LLM performance, hidden-test, security,
or formal-proof claim. Independent review is required before marking this spec
`done`; its absence does not prevent beginning implementation or ending a coding
pilot with a reviewable candidate in `in-review`.

## Readiness and history

**Readiness assessment:** bootstrap-author document review only. Intent, compatibility
baseline, dependency direction, supported environment, new/existing file map,
observable cases, acceptance checks, and exclusions are specified. No external
service or unresolved architecture choice is needed for this slice. Tooling and
runtime checks are not yet executed. This is a planning gate, not an implementation
or independent-review result.

| Date | Actor | Entry |
|---|---|---|
| 2026-09-05 | Bootstrap agent under project-owner instruction | Created version 1; marked ready-for-dev after the document-level readiness review; no runtime implementation or execution |

Once development begins, append baseline commit, revision decisions, acceptance
evidence, and review dispositions. Do not erase failed attempts or silently
rewrite the trial's frozen acceptance criteria.
