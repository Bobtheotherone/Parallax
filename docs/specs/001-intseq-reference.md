---
id: SPEC-001
status: ready-for-dev
spec_version: 2
created: 2026-09-05
depends_on: []
---
# SPEC-001 — Extract `intseq/0.1` into an importable reference runtime

## Intent

Turn the embedded `intseq/0.1` reference into ordinary local Python modules that are
easy to import, execute, inspect, and test **without changing its semantics**.

The desired result is a transparent reference runtime, not a framework. A coding
agent should be able to understand the entire semantic path, make a faithful first
implementation, and localize failures quickly:

```text
Markdown artifact
  -> strict JSON document parsing
  -> capsule admission
  -> program binding + type checking
  -> hygienic macro expansion
  -> primitive-only recheck
  -> bounded exact evaluation
  -> CLI result
  -> separate task acceptance
```

This spec packages existing behavior. It does not authorize a new primitive,
optimizer, host, task oracle, or protocol meaning.

## Required context

Read the sources that define behavior, not every research document:

- [intseq semantics](../../packs/intseq/PACK.md) and
  [capsule/program formats](../../packs/intseq/CAPSULE.md);
- the frozen [embedded Python reference](../../runtime/REFERENCE.md) and
  [host boundary](../../runtime/HOST.md);
- [semantic obligations](../../core/SEMANTICS.md) and
  [evidence meanings](../../core/EVIDENCE.md);
- the public [task](../../examples/intseq/TASK.md),
  [capsule](../../examples/intseq/CAPSULE.md),
  [program](../../examples/intseq/PROGRAM.md), and
  [typed-but-wrong counterexample](../../examples/intseq/FAILURE.md).

The pack and format documents own meaning. The Python fence is the compatibility
baseline for observable reference behavior. If they disagree on a concrete case,
preserve the minimal reproducer and surface the conflict instead of silently
choosing whichever behavior is easier to implement.

## Approach and tooling choice

Use CPython 3.11+ and only the standard library. Keep the implementation small
enough that semantic behavior is visible in code review.

The intended decomposition is:

- `parallax.intseq`: constants, `Rejection`, strict parsing/canonicalization,
  capsule admission, type inference, macro expansion, program checking, evaluation;
- `parallax.selftest`: public fixtures, the direct-loop task oracle, and the
  archived-style public self-test;
- `parallax.__main__`: argument parsing, artifact I/O orchestration, result/exit
  adaptation;
- `tests/`: contract-derived tests plus differential checks against the pinned
  reference.

Prefer a direct extraction with explicit seams over a redesign. Refactoring is
welcome when it makes data flow, error ownership, or testability clearer, but it
must not alter rejection precedence, evaluation order, resource charging, or
protocol identity.

No installation step is required for acceptance. Do not add a build backend,
dependency manager, external test framework, or CI workflow merely to package this
slice.

## Invariants

### Semantic behavior

`Int` is a mathematical integer; `VecInt` is an ordered finite sequence of
integers. Booleans and floats are not integers. There are seven primitives with
the exact signatures and meanings in `packs/intseq/PACK.md`.

Evaluation is eager and left-to-right. Sequence order and multiplicity are
preserved. `seq.sum` accumulates left-to-right and checks every intermediate.
Integer overflow means exceeding the configured magnitude-bit budget; values never
wrap, saturate, or approximate.

A mathematically equivalent expression may consume different resources or reject
at a different intermediate point. Preserve the reference behavior rather than
algebraically “simplifying” it.

### Artifact and expansion behavior

Keep these externally meaningful identifiers unchanged:

- pack: `intseq/0.1`;
- capsule protocol: `arl-capsule/0.1`;
- program protocol: `arl-program/0.1`;
- example capsule canonical SHA-256:
  `2a340d75023574cd3b55590dfe5583700984ded258b1257f316dd7b6490e2ee9`.

Canonical JSON uses sorted object keys, compact separators, ASCII escaping,
`allow_nan=False`, UTF-8, then SHA-256.

Macro bodies may reference only their parameters, integer literals, and selected
primitives. Program expressions may call admitted macros. Expansion is lexical and
hygienic: substituting a caller expression for a macro parameter must not reinterpret
names inside that caller expression in the callee's parameter environment. Expanded
primitive IR is typechecked again.

### Authority and side effects

Capsules and programs are data. They cannot add permissions, code execution,
imports, primitives, backends, or oracle access. Imports of `parallax` must not run
the CLI, self-tests, or file reads.

`evaluate` must not mutate the capsule, program, or caller input. Task acceptance
remains outside the evaluator: successful evaluation reports behavior, not whether
that behavior solves an arbitrary task.

### Resource limits

Preserve the reference limits and the points at which they are charged:

| Limit | Value | Meaning |
|---|---:|---|
| document / JSON UTF-8 bytes | 65,536 | enforced before parsing/reading beyond the supported artifact size |
| expression depth | 32 | checked during inference and expansion |
| expression / expansion nodes | 4,096 | visit budget, not merely final IR size |
| input vector length | 4,096 | evaluator input bound |
| integer magnitude bits | 256 | applies to literals, input values, and intermediates |
| evaluation work | 250,000 | expression visits plus sequence-element work |
| macros per capsule | 16 | schema/admission bound |
| parameters per macro | 1..8 | schema/admission bound |

Do not make these capsule-configurable in this slice.

## Non-goals

No model/agent orchestration, packet service, task-contract parser, hidden-test
harness, optimizer, native/GPU backend, hole solver, generalized IR, sandbox,
formal proof, performance project, package publication, or new semantic feature.

Do not “improve” the grammar with vector literals, implicit casts, alternate JSON
forms, recursive macros, arbitrary Python lowering, or friendlier behavior that
changes a stable rejection code.

## Interfaces and observable behavior

### Library API

Expose these names from `parallax.intseq`:

| Interface | Required behavior |
|---|---|
| `Rejection` | `ValueError` subtype with stable `.code`; message contains code and useful detail |
| `strict_json(text)` | enforce byte bound; reject duplicates, NaN/Infinity, malformed/deep JSON |
| `canonical(obj)` | canonical UTF-8 JSON bytes, no trailing newline |
| `digest(obj)` | lowercase SHA-256 hex of `canonical(obj)` |
| `read_document(path)` | bounded UTF-8 Markdown; exactly one lowercase `json` fence; prose has no authority |
| `validate_capsule(cap)` | return `(signatures, definitions)` or reject |
| `check_program(cap, prog)` | validate capsule, binding, types, expansion, primitive-only recheck; return lowered IR |
| `evaluate(cap, prog, x)` | return `(value, lowered_ir)` or a stable rejection |

Use ordinary Python built-ins as parsed JSON values. Supporting arbitrary custom
objects is outside the contract.

### Failure taxonomy

The stable rejection codes are part of the debugging interface:

- `SCHEMA`: shape/field/JSON/literal-form violations;
- `VERSION`: unsupported protocol or pack;
- `OP_NOT_ALLOWED`: operation is unknown or not admitted in this capsule;
- `TYPE`: scope, arity, type, or input-element mismatch;
- `HASH_MISMATCH`: program is bound to a different capsule identity;
- `RESOURCE_LIMIT`: a configured bound is exceeded.

Preserve the reference's check ordering where multiple defects coexist. For
example, a primitive list longer than seven is rejected as `OP_NOT_ALLOWED` before
duplicate detection is reached.

### CLI

`python -m parallax` replaces only the invocation prefix of the embedded reference.
Support `--capsule PATH`, `--program PATH`, `--input JSON` (default `[]`), and
`--selftest`.

Ordinary evaluation success:

- exit `0`;
- one JSON object on stdout;
- empty stderr;
- exactly the keys `status`, `value`, `expanded_ir`, `capsule_sha256`,
  `program_sha256`, `task_correctness`;
- `status` is `EVALUATED`;
- `task_correctness` is `NOT_CHECKED`.

Handled artifact/I/O/UTF-8 failure:

- exit `2`;
- empty stdout;
- one JSON object on stderr with exactly `status: REJECTED` and `detail`;
- a `Rejection` detail includes its stable code.

Keep normal `argparse` behavior for parser-level usage errors and `--help`.
`--selftest` takes precedence over artifact evaluation and needs no paths.

### High-information conformance cases

These cases target distinct mechanisms; they are not a request for maximal test
count.

| Question | Discriminating case | Required observation |
|---|---|---|
| Did the happy path preserve semantics? | example program on `[-2,-1,0,2]` | value `16`; exact primitive IR `['seq.sum',['seq.add',['seq.mul',['seq.filter_ge','x',0],3],5]]` |
| Is empty/rejected selection correct? | `[]`, `[-3,-1]`, `[0,0,2]` | `0`, `0`, `21` |
| Are types separate from task intent? | wrong-order expression on `[-1,0]` | admitted and evaluates to `7`; task oracle says `5` |
| Is capsule binding real? | wrong digest | `HASH_MISMATCH` |
| Are scope/arity/types enforced? | `seq.sum(3)`, extra arg, unbound `y` | `TYPE` |
| Is the allowlist authoritative? | `seq.count` in example capsule; unknown op | `OP_NOT_ALLOWED` |
| Are Python bools kept out of `Int`? | boolean expression leaf / boolean input element | `SCHEMA` / `TYPE` |
| Are inputs bounded? | non-list or vector length 4,097 | `RESOURCE_LIMIT` |
| Are intermediates checked, not just final values? | multiply a 256-bit-magnitude value by `2` inside a larger expression | `RESOURCE_LIMIT` at the overflowing intermediate |
| Is parsing strict? | duplicate key, NaN, extra object field | `SCHEMA` |
| Are macro bodies primitive-only? | body calls itself or another macro | `OP_NOT_ALLOWED` |
| Is expansion hygienic? | nested `shift(x,v)` with offsets 2 then 3 on `[1,2]`, then sum | `13` |
| Are expansion limits about visits? | nested expansion that crosses depth/node budget | `RESOURCE_LIMIT` |

For byte/depth/node/work boundaries, construct cases that actually reach the
intended check rather than failing earlier for an unrelated reason.

## File map

| Path | Job |
|---|---|
| `runtime/REFERENCE.md` | frozen embedded Python compatibility baseline; do not edit its source fence |
| `packs/intseq/{PACK,CAPSULE,TUTORIAL}.md` | existing semantic/schema/tutorial authority |
| `examples/intseq/{TASK,CAPSULE,PROGRAM,FAILURE,EVIDENCE,PACKET}.md` | public fixtures and historical evidence |
| `parallax/__init__.py` | side-effect-free package entry |
| `parallax/intseq.py` | semantic library |
| `parallax/__main__.py` | CLI adapter |
| `parallax/selftest.py` | public demonstration and direct-loop oracle |
| `tests/test_intseq.py` | semantic, admission, expansion, resource, and task-negative checks |
| `tests/test_cli.py` | subprocess contract and reference-parity checks |

The `parallax/` and `tests/` paths are planned implementation files, not evidence
that the package already exists.

## Implementation tasks

1. **Pin and characterize the baseline.** Verify the embedded Python fence SHA-256
   `4025a0043e958785196e35d6530ec4570dcedd36cf621b555249a1809649dc91`.
   Run only this reviewed source when obtaining parity observations.
2. **Extract the semantic core.** Move behavior into `parallax.intseq` with the
   same signatures, check ordering, lexical expansion, eager evaluation, and
   resource charging. Keep imports inert.
3. **Separate demonstration from evaluation.** Put fixture builders, the direct-loop
   oracle, and public self-test in `parallax.selftest`; the evaluator must not use
   that oracle.
4. **Add the CLI adapter.** Make streams, exits, JSON shapes, help, and `--selftest`
   behavior match the interface above.
5. **Test by defect class.** Use contract-derived expectations for semantics and
   independent task answers; use differential reference checks for compatibility.
   Keep tests that distinguish plausible wrong implementations.
6. **Update capability prose only after evidence exists.** Do not turn a passing
   parser/type suite into a claim of task correctness, sandboxing, performance, or
   benchmark success.

## Acceptance criteria

| ID | Acceptance condition | Evidence that answers it |
|---|---|---|
| AC1 | Package imports under ordinary Python and `python -S` without third-party dependencies or import-time I/O/execution | import/subprocess tests |
| AC2 | All seven primitive meanings, exact arithmetic, eager order, and resource charging match the pack/reference | contract-derived boundary tests plus differential parity |
| AC3 | Strict parsing, capsule admission, allowlist, stable codes, capsule digest binding, typing, macro hygiene, and expansion bounds are preserved | targeted rejection and expansion tests |
| AC4 | CLI exits, stdout/stderr separation, success/rejection shapes, defaults, help, and self-test precedence match the documented contract | subprocess tests |
| AC5 | The public self-test retains the historical scopes—2,801 exhaustive task inputs, 1,000 seeded random inputs, 700 primitive checks, 17 rejection checks, one macro-scope check—and retains the `7` vs `5` typed-but-wrong counterexample | self-test output and task-negative regression |
| AC6 | Task expectations are computed by the direct-loop oracle rather than the candidate AST/expander, while reference parity independently detects extraction drift | inspection plus tests using both paths |
| AC7 | No protocol, semantic, authority, or maturity expansion is introduced | diff review and documentation check, with any checker-version mismatch called out explicitly |

## Verification plan

Run from the repository root with non-optimized CPython 3.11+:

```sh
python --version
python -m unittest discover -s tests -v
python -S -m parallax --help
python -m parallax --selftest
python -m parallax --capsule examples/intseq/CAPSULE.md --program examples/intseq/PROGRAM.md --input '[-2,-1,0,2]'
python -m parallax --capsule examples/intseq/CAPSULE.md --program examples/intseq/PROGRAM.md --input '[true]'
python tools/check_docs.py
```

The boolean-input command is an intentional negative case and should exit `2` with
`TYPE` in the rejection detail. The example command should evaluate to `16` with
`task_correctness: NOT_CHECKED`.

The implementation test suite should also execute the unchanged embedded reference
in a temporary location after verifying its source hash, then compare representative
success and rejection behavior. Reference agreement is compatibility evidence;
contract-derived expectations remain necessary because two implementations can
share a defect.

This golden documentation branch intentionally rewrites a formerly whole-file-frozen
example wrapper while preserving its canonical JSON. Until the legacy documentation
checker is versioned for that policy, a failure whose sole cause is that obsolete
whole-file hash is an expected checker incompatibility, not a reason to revert the
rewrite. Any canonical JSON, reference-fence, link, schema, or packet-binding failure
remains a real defect.

## Readiness and history

`ready-for-dev` means the implementation contract is sufficiently concrete to
start; it is not implementation evidence.

| Date | Actor | Entry |
|---|---|---|
| 2026-09-05 | bootstrap | version 1 established the extraction/conformance task; runtime checks had not run |
| 2026-09-05 | golden capability rewrite | version 2 compresses process language and strengthens module boundaries, failure semantics, diagnostic tests, and first-pass implementation guidance; no runtime implementation or new execution evidence |
