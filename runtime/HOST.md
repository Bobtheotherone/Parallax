# Host boundary and reference capabilities

**Authority:** intended host/runtime boundary. No orchestration host is implemented.
“Reference” below means the embedded source in [REFERENCE.md](REFERENCE.md), not
an installed service. Capability descriptions are source-level descriptions;
new execution evidence must be recorded separately.

## Available in the provided reference

Read a bounded Markdown artifact containing one JSON block; reject invalid schema;
validate intseq operation signatures and pure macros; check a program and capsule
identity; expand to a primitive IR; evaluate bounded integer-sequence expressions;
run the bundled public tests; emit structured results.

No native compiler, GPU runtime, LLM API, theorem prover, benchmark harness,
optimizer, hole enumerator, repository publisher, or operating-system sandbox is
included. These capabilities cannot be conjured by documenting their names.

## Agent integration contract

A repository-enabled agent may use its existing file and shell tools to extract
and run the reviewed reference. Tool availability and permissions come from that
agent's host. The Markdown workflow does not grant execution rights or enforce
budgets, final-test secrecy, filesystem access rules, or network isolation.

The expression interpreter does not execute arbitrary generated Python: it
interprets an allowlisted data tree. The reference CLI itself is ordinary trusted
Python, with local file access to caller-specified paths. It is not a secure
container for untrusted Python or a proof that all implementation bugs are absent.

Do not automatically execute code fences from arbitrary retrieved documents.
Review and pin the particular reference source, pack, and extraction boundary.
For hostile workloads or native adapters, use external process isolation,
resource controls, capability restrictions, and an independently maintained
harness. These are integration requirements, not implemented features here.

## Generated artifact versus trusted implementation

A generated capsule or program is data. The parser, checker, expander, interpreter,
Python runtime, and operating environment form the implementation base whose
behavior is relied on. The test oracle is a separate source of task expectations.
Tests increase confidence but do not turn this base into formally verified code.

The reference permits larger mathematical inputs than the worked task contract.
A real host must enforce each task's domain and acceptance oracle separately.
It must also record cost and provenance; the CLI does not perform full experiment
accounting just by returning a capsule hash.
