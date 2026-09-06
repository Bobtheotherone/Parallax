# Verification strategy and current evidence

**Consumer:** implementer, reviewer, experiment operator.
[Core evidence profiles](../../core/EVIDENCE.md) define the meaning of evidence;
this guide defines how development produces and records it. A spec supplies its
own exact cases and required checks.

## Bootstrap evidence baseline

Documentation checks are recorded in the [bootstrap audit](../provenance/BOOTSTRAP-AUDIT.md).
The [imported example report](../../examples/intseq/EVIDENCE.md) describes source-
author execution of public reference checks. During this bootstrap, no intseq
runtime, self-test, implementation test suite, or LLM experiment was executed.
The Python source was read and hashed, not independently validated.

| Evidence | Establishes when actually obtained | Does not establish |
|---|---|---|
| Parsing/schema tests | Recorded accepted/rejected document forms | Types, permissions beyond the parser, task correctness |
| Admission/type checks | Allowed operations, signatures, scope, capsule binding on checked inputs | Correct task algorithm or correct backend |
| Expansion checks | Recorded substitution/lowering behavior and bounds | Universal expander correctness |
| Primitive conformance tests | Agreement with specified examples/properties | Full task satisfaction |
| Execution result | Evaluator completed or rejected under named limits | Acceptance by a task oracle |
| Public task tests | Agreement on disclosed inputs | Held-out generalization or proof |
| Held-out tests | Agreement on inputs withheld under documented custody | Universal correctness or uncontaminated training by itself |
| Exhaustive bounded enumeration | Every member of the precisely stated finite set checked | The larger input domain |
| Differential checks | Agreement between named implementation paths | Correctness when both share a defect |
| Formal proof/checker result | Named theorem under named assumptions accepted by a named checker | Unmodeled runtime/host properties |
| Native-backend evidence | Named generated artifact tested on a recorded target | Equivalence to every backend |
| Performance measurements | Observed distributions under a measurement protocol | Estimated speedups, safety, or correctness |
| Code review | Specific inspected findings and reasoning | Independent ground truth merely from another persona |

Each field retains `NOT_RUN`, `PASS`, `FAIL`, or `NOT_APPLICABLE`, plus scope,
identities, assumptions, and evidence location. Source-reported historic `PASS`
values are not current-run `PASS` values. “Verified” without a property and scope
is not an acceptable completion summary.

## Minimum implementation evidence

For a runtime change, cover the supported happy path, specified malformed inputs,
resource and type boundaries, expansion/capsule binding, and a task-negative case
that still typechecks. Compare against both contract-derived expectations and
the frozen reference where the spec requires it. Reference parity alone can
preserve a shared bug; contract-only tests can miss compatibility drift.

Invoke the CLI in a subprocess for exit/stdout/stderr checks; library-only tests
cannot establish the command interface. Test discovery must report a nonzero
number of cases. Do not bypass checks with optimized Python assertions or mark
skips as passes. A failed reference characterization is a real finding.

Record raw evidence in the episode's run directory (a future `runs/<run-id>/`,
created when a run exists), using [the run template](../../templates/RUN.md).
Record source revision and dirty-tree state, Python/tool versions, commands,
exits, result counts, logs, source/artifact hashes, and all missing checks.
Append new evidence after changes instead of overwriting earlier outcomes.

## Independence and benchmark custody

Expected answers must not be computed by the same generated AST used for actual
answers. Document three separate properties: independent authorship, different
implementation path, and hidden inputs. The public worked example has only the
second of these. A fresh reviewer can improve review but is not automatically an
independent task oracle.

The first coding task may use every public repository file. It is a public
reference-extraction/conformance task. Any final benchmark oracle must be held
outside the candidate's writable/readable environment and frozen before trials.
No such isolation or final oracle has been implemented in this repository.

Timing and LLM-quality claims require the
[benchmark protocol](../benchmarking/PROTOCOL.md), not just passing unit tests.
