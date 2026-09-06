# Host architecture: authority, execution, and feedback

The host is the trusted integration layer around Parallax. It decides what a model
may read, write, call, and execute; pins semantic/runtime dependencies; isolates
attempts; enforces budgets; and keeps task acceptance outside generated authority.
A capsule or program is data. Describing a capability never grants it.

**Current state:** no orchestration host is implemented in this repository. The
only executable semantic reference is the embedded intseq source in [REFERENCE](REFERENCE.md).
The interfaces below define the engineering boundary a future host should satisfy;
they are not claims of deployed controls.

## Core dataflow

```text
frozen task + acceptance policy
        |
        v
host snapshot ----> context/capability view ----> generator
     |                                         capsule/program data
     |                                                |
     +----> admission/check/expand ----> execution ----+
     |                                  |
     +----> independent acceptance <----+
     |
     +----> diagnostic + evidence + cost -> next bounded decision
```

The host should make these stages separately observable. `ADMITTED`, `EXECUTED`,
and `ACCEPTED` are different facts and should never collapse into one success bit.

## Episode snapshot

A serious run begins from an immutable snapshot containing only information that
can change the meaning or reproducibility of the episode:

- task contract/version and acceptance-policy identity;
- semantic pack, capsule when applicable, checker/runtime/backend identities;
- model/decoder configuration and the context actually exposed;
- target environment and relevant tool/capability grants;
- synthesis budget, execution resource policy, and acceptance budget;
- writable workspace identity and any external state intentionally visible.

Pin by content where drift would matter. Human-readable version names are useful
labels, not sufficient pins. Reversible local implementation choices need not be
promoted into global protocol metadata.

## Capability model

Treat every capability as an explicit host grant. Useful categories include:

| Capability | Host decision |
|---|---|
| Read | Which repository/artifact/data regions enter candidate context |
| Write | Which workspace paths or external resources may be mutated |
| Execute | Which interpreters, compilers, subprocesses, devices, or services may run |
| Network | Which destinations/protocols, if any, are reachable |
| Model/tool | Which model calls and engineering tools are available and budgeted |
| Backend | Which pinned semantic implementations may lower/execute admitted IR |
| Oracle | Which public diagnostics may be queried and which final acceptance data stay isolated |

Generated content may request one of these, but only the host can grant it. Unknown
operations, undeclared adapters, arbitrary code fences, and self-authored permission
fields remain inert or rejected.

For the bundled intseq reference, the host may authorize ordinary Python execution
of the reviewed reference/package and caller-selected local artifact paths. The
reference itself provides no OS sandbox, network policy, model API, native/GPU
runtime, theorem prover, package publisher, or hidden-oracle isolation.

## Context assembly as an engineering interface

Context should expose the structure needed to solve the task, not mirror the whole
repository by default. Assemble from the snapshot:

1. the task behavior and constraints that can change the correct solution;
2. selected semantic operations and their exact preconditions/effects;
3. architecture/API surfaces the candidate must integrate with;
4. relevant examples, diagnostics, and tool instructions;
5. no final oracle material whose secrecy is part of the evaluation claim.

Include transitive semantic dependencies when omitting them could change meaning.
Omit historical narration, unrelated packs, duplicate policy, and low-value logs.
Cache exact unchanged context by identity. Context reduction is invalid when it
removes a constraint the candidate needs to produce a correct result.

## Attempt isolation and concurrency

Parallel attempts should share immutable inputs, not mutable workspaces. Give each
candidate an isolated branch/worktree/process namespace or equivalent write scope.
Do not let one attempt observe another attempt's unreviewed code, diagnostics, or
private oracle results unless cross-attempt sharing is an explicit treatment.

The host owns selection and integration of parallel results. Generated artifacts
must not merge branches, overwrite another attempt, mutate the semantic pack, or
change acceptance state. If attempts share caches or accelerators, ensure cache
keys include every dependency that can affect meaning or measured performance.

For stateful tools/services, define ownership, lifetime, cancellation, and retry
semantics. A timeout or interrupted write must not become an ambiguous partial
success.

## Tool brokerage

A tool call should answer a concrete engineering question. The host should expose
high-leverage instruments—repository search, compiler/interpreter, debugger,
static analyzer, profiler, benchmark harness, reference implementation, property
or differential checker—when the task permits them.

Before a side-effecting call, bind its write scope and expected artifact. After a
call, retain enough result to support the next decision: exit/status, salient
stdout/stderr or artifact identity, measured values, and environment when relevant.
Do not require verbose transcripts when a structured result is sufficient.

Tool failures must remain typed failures (`UNAVAILABLE`, `TIMEOUT`, `REJECTED`,
`FAILED`, or a domain-specific diagnostic), not silently converted into model
claims about what would have happened.

## Execution and resource semantics

Keep three budgets conceptually separate:

- **search budget:** model calls, retrieval, repairs, synthesis, and engineering tools;
- **candidate resource policy:** limits on one admitted program/backend execution;
- **acceptance budget:** public/final tests, measurement, proof, or reviewer effort.

An execution resource rejection is not mathematical incorrectness. A budget-exhausted
search is not proof that no solution exists. Record which limit fired and the last
reproducible artifact/diagnostic.

Use process isolation, filesystem/network restrictions, device quotas, and hard
resource limits appropriate to the threat model when running hostile or native
workloads. AST size/work checks are useful admission controls but are not substitutes
for OS-level containment.

## Acceptance boundary

Task acceptance consumes the candidate result but derives expected behavior from
the frozen task/oracle, not from the candidate's capsule, lowered IR, or generated
tests. The host enforces task-domain bounds that may be narrower than a runtime's
mathematical domain.

Public feedback may return during development according to policy. Final held-out
material stays outside candidate read/write capabilities when a held-out claim is
made. Reusing final failures as repair feedback ends that hold-out episode.

## Diagnostics: return the smallest useful truth

Classify failures before deciding what to expose:

| Failure class | Example | Useful feedback |
|---|---|---|
| Artifact/schema | unknown field, malformed JSON | exact location/code |
| Identity | capsule/runtime mismatch | expected vs observed identity |
| Type/scope/admission | wrong arity, unbound name, disallowed op | local checker diagnostic |
| Algorithm/task | well-typed wrong result | public counterexample or violated invariant |
| Resource | node/work/memory/time/device limit | limit, observed usage when measurable |
| Backend/tool | unsupported target, compiler failure | actual capability/tool diagnostic |
| Infrastructure | unavailable service, interrupted workspace | retryability and preserved state |
| Acceptance-policy | required evidence missing | unmet acceptance obligation |

Prefer the highest-information diagnostic that does not leak protected oracle data.
Do not flood the generator with every log line when one counterexample localizes the
bug.

## Evidence and observability

Retain what is needed to reconstruct consequential claims: snapshot identities,
candidate identities, decisive diagnostics, actual tool/execution results, costs,
and acceptance outcome. Aggregate routine successful calls instead of creating an
audit bureaucracy.

Hashes bind bytes; they do not prove correctness or authorship. Model self-review
can improve a candidate; it is not an independent task oracle. Performance claims
require measurements on the actual target and methodology sufficient to interpret
them.

## Current reference boundary

[REFERENCE](REFERENCE.md) can parse one bounded JSON fence, validate `intseq/0.1`
capsules/programs, hygienically expand supported macros, evaluate primitive IR, and
run public self-tests. It intentionally does **not** implement context assembly,
model orchestration, task-domain enforcement, experiment scheduling, durable run
storage, capability isolation, or final task acceptance. A packaged extraction of
that reference should preserve this boundary rather than accidentally turning the
runtime into the host.
