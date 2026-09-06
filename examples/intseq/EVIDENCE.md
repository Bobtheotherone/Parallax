# Imported intseq reference evidence — historical record

This file records a **source-author run from the preserved archive**. It has not
been rerun by the documentation bootstrap or by this golden rewrite, and it is not
evidence that a current extracted package passes.

Use it for two things:

1. to understand which mechanisms the original reference exercised;
2. to know the exact historical outputs and identities that must not be rewritten
   as though they came from a new run.

The archive/source relationship is documented in
[the source map](../../docs/provenance/SOURCE-MAP.md). The extracted Python fence
remains identified by
`4025a0043e958785196e35d6530ec4570dcedd36cf621b555249a1809649dc91`.

## What the reported run establishes

According to the archived report, the source author ran the public reference
self-test and the example CLI successfully under Python `3.13.5`.

| Mechanism exercised | Reported scope |
|---|---:|
| bounded exhaustive task differential | 2,801 inputs: every vector of length 0..4 over `-3..3` |
| seeded randomized task differential | 1,000 inputs, seed `20260905`, lengths 0..64, values in ±1,000,000 |
| primitive differential checks | 700 |
| rejection checks | 17 |
| macro lexical-scope check | 1 |
| example CLI | value `16` |
| typed-but-wrong negative case | candidate `7`, direct-loop oracle `5` on `[-1,0]` |

The direct-loop oracle and AST interpreter are different implementation paths but
share project authorship. All these cases are public. This is useful compatibility
and regression evidence; it is not independent authorship, a hidden benchmark, or
a universal proof.

The wrong-program case is especially informative: the checker and evaluator are
supposed to accept the represented computation while the task oracle rejects the
algorithm. Treating that as a successful negative test protects the architecture's
separation between representation preservation and task satisfaction.

## What the report does not establish

No held-out evaluation, formal proof, native compilation, GPU execution,
performance comparison, LLM synthesis comparison, security isolation, or current
package conformance was run. A hash identifies bytes under a recipe; it does not
prove their correctness or authorship.

The UTC timestamp below is historical. `2026-09-06` UTC can still be
`2026-09-05` in America/Anchorage. Do not replace it with the time of a later
documentation or reproduction run.

The whole-file Markdown hashes in the record identify **original archive files**.
Some live wrappers have since changed. Preserve those values as provenance rather
than updating them to make the old report look current.

## Immutable archived report

```json
{
  "run_kind": "public reference-implementation validation; no LLM experiment",
  "runtime_clock_utc": "2026-09-06T00:19:17.326439+00:00",
  "python": "3.13.5",
  "commands": [
    {
      "command": "python reference.py --selftest",
      "exit_status": 0
    },
    {
      "command": "python reference.py --capsule examples/intseq/CAPSULE.md --program examples/intseq/PROGRAM.md --input '[-2,-1,0,2]'",
      "exit_status": 0
    }
  ],
  "identities": {
    "capsule_canonical_json_sha256": "2a340d75023574cd3b55590dfe5583700984ded258b1257f316dd7b6490e2ee9",
    "program_canonical_json_sha256": "db2dad5bd80762eb3fa6eeba57410027755dfdcc57d22ff212236b99613b1517",
    "extracted_runtime_source_sha256": "4025a0043e958785196e35d6530ec4570dcedd36cf621b555249a1809649dc91",
    "runtime_markdown_sha256": "6c3254e60778efb66092f2e6ffc1e00362b71a16208c60a50ec9fa117f95d1b3",
    "pack_markdown_sha256": "1d3de58d8bbdb9334f2fee2d40135aada79e26b35decc9cbe146e0c099ff717b",
    "capsule_schema_markdown_sha256": "f38fcb922a05528d1dc8db48127a6bb5eef4a5555420bf2f35f5886ef5a30029",
    "contract_markdown_sha256": "f08bce72ad70d544409917c41af5b07dcb9a15c84731b733f32b40464a9b4f50",
    "capsule_markdown_sha256": "33bd94fe2226635f81af35fe5b897f618d036d0d2341aac0e8694a6aaca812d8",
    "program_markdown_sha256": "4563c0af751770e7e0c31d16318cd143ed50ea682f1eab7fa93f397967b405e5"
  },
  "evidence": {
    "capsule_types_and_expansion": "PASS on recorded example and documented checks",
    "example_cli_execution": "PASS; result 16",
    "bounded_exhaustive_public_task_tests": "PASS; 2801 inputs",
    "randomized_public_task_tests": "PASS; 1000 inputs",
    "primitive_differential_checks": "PASS; 700 checks",
    "rejection_checks": "PASS; 17 checks",
    "macro_scope_check": "PASS; 1 check",
    "held_out_tests": "NOT_RUN",
    "formal_proof": "NOT_RUN",
    "native_compilation": "NOT_RUN",
    "GPU_execution": "NOT_RUN",
    "performance_comparison": "NOT_RUN",
    "LLM_synthesis_comparison": "NOT_RUN"
  },
  "example_cli_stdout": {
    "capsule_sha256": "2a340d75023574cd3b55590dfe5583700984ded258b1257f316dd7b6490e2ee9",
    "expanded_ir": [
      "seq.sum",
      [
        "seq.add",
        [
          "seq.mul",
          [
            "seq.filter_ge",
            "x",
            0
          ],
          3
        ],
        5
      ]
    ],
    "program_sha256": "db2dad5bd80762eb3fa6eeba57410027755dfdcc57d22ff212236b99613b1517",
    "status": "EVALUATED",
    "task_correctness": "NOT_CHECKED",
    "value": 16
  },
  "selftest_stdout": {
    "capsule_sha256": "2a340d75023574cd3b55590dfe5583700984ded258b1257f316dd7b6490e2ee9",
    "counts": {
      "exhaustive_task_inputs": 2801,
      "macro_scope_checks": 1,
      "primitive_differential_checks": 700,
      "random_task_inputs": 1000,
      "rejection_checks": 17
    },
    "program_sha256": "db2dad5bd80762eb3fa6eeba57410027755dfdcc57d22ff212236b99613b1517",
    "python": "3.13.5",
    "status": "PASS",
    "typed_but_wrong_counterexample": {
      "candidate": 7,
      "input": [
        -1,
        0
      ],
      "oracle": 5
    }
  }
}
```

## How to obtain new evidence

Use the reviewed reproduction path in
[runtime/REFERENCE.md](../../runtime/REFERENCE.md) or the implementation commands in
[SPEC-001](../../docs/specs/001-intseq-reference.md). Verify the pinned Python-fence
hash before executing the extracted reference.

A new run should create a new evidence record with its own commit, environment,
commands, exits, and outputs. Do not edit the JSON above to represent a rerun.
