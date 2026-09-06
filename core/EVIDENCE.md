# Evidence profiles, not a single confidence label

Use orthogonal fields; evidence is not a simple ladder. A reference interpreter
can give strong semantic clarity without proving its implementation. A numerical
benchmark can be extensive without proving memory safety.

Record separately: document parsing, capsule checks, type checks, expansion
checks, execution, public tests, held-out tests, bounded exhaustive tests,
property/differential tests, formal proofs, backend validation, and performance
measurements. Each field is `NOT_RUN`, `PASS`, `FAIL`, or `NOT_APPLICABLE`, with
scope, tool/source identity, artifact identity, assumptions, and evidence location.

## Language for results

Say “typechecked by intseq reference version X,” not “verified correct.” Say
“agreed with oracle O on these 2,801 bounded inputs,” not “proved for all inputs.”
Say “a proof checker accepted theorem X under assumptions A” only when that
actually happened. Say “estimated” rather than “measured” for model-based costs.

Raw stdout, a reproducible command, exit status, input/output artifacts, runtime
identity, and environment version should accompany execution claims. A hash binds
content but is neither a signature nor evidence that the content is correct.

## Independence

Preserve an oracle outside the generated representation. Prefer different
implementations and, for consequential work, separately reviewed specifications.
Do not derive both expected and actual answers by executing the same macro graph.
Independent authorship, implementation diversity, and hidden inputs are different
properties; report them separately.

The bundled example has a hand-written direct-loop oracle and a separate AST
interpreter. Both were authored in this project, and all tests are public. It has
implementation diversity but does not claim independent authorship or a hidden
benchmark. The test run measures runtime behavior, not LLM synthesis quality.

## Acceptance

The requirement owner chooses a task-appropriate evidence policy before search.
Functional failures, prohibited effects, or missing required evidence are hard
gates. Do not compensate for them with lower latency or a high weighted score.
Reserve final held-out evaluation for the end; repeatedly querying it turns it
into development feedback and invalidates that hold-out claim.
