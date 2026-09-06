# Imported example evidence — not rerun

**Origin:** the source archive author's report, preserved below. The bootstrap
checked archive and source identities, but did not run these commands or
independently validate the report. This is not Parallax benchmark evidence.

The archive author reports executing these commands against the extracted
reference source and reading the capsule/program from the original Markdown.
The `identities` object describes **original archive files**, not a manifest of
the migrated repository. In particular, the reference Markdown wrapper changed;
the extracted Python fence did not. See the [source map](../../docs/provenance/SOURCE-MAP.md).
No historical hash below is asserted to identify a changed current document.

The exhaustive set contains every vector of length 0..4 over integers -3..3:
`1 + 7 + 49 + 343 + 2401 = 2801`. The random set uses seed `20260905`, lengths
0..64, and elements in [-1000000,1000000]. These do not exhaust the task's full
input domain. Additional checks cover the seven primitives, structural
rejections, resource errors, and lexical macro substitution.

A deliberately well-typed wrong program returns 7 instead of 5 on `[-1,0]`.
That result is a passing **negative test of the methodology**: the type checker
admits the program, and the separate task reference detects its wrong answer.

The direct-loop oracle and the AST interpreter are different implementation paths,
but share project authorship. All tests are public. No independent authorship,
hidden benchmark, formal proof, GPU execution, native code generation, performance
win, or improvement in LLM generation quality is claimed.

The timestamp is the execution container's UTC clock. Project document dates
identify the design revision. These are source-reported local evidence, not an externally signed attestation.
The UTC date is retained from that report; September 6 UTC can fall on September 5
in America/Anchorage. No new timestamp or successful run is inferred from it.

## Commands, identities, and captured output

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

## Reproduction

Use the reproduction instructions in [runtime/REFERENCE.md](../../runtime/REFERENCE.md). Run both commands in the JSON
record from the repository root. Expect exit status zero and the displayed
results; the Python version and timing metadata can differ across environments.
A changed runtime/pack requires new evidence, not reuse of this report by name.
