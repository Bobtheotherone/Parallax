# Evidence: answer engineering questions, do not manufacture confidence

Evidence is useful when it changes what a competent engineer should believe or do.
Parallax records evidence by **claim and scope**, not as one confidence score and
not as a requirement to produce a large verification dossier.

The governing rule is simple: never claim a tool ran, a benchmark was measured, a
test passed, or a property was proved unless that event actually occurred on the
identified artifact.

## Match the instrument to the claim

| Claim or uncertainty | High-value evidence | Common overclaim |
|---|---|---|
| Artifact is syntactically admissible | Parser/schema/allowlist result | "Correct" |
| Types/scope/capsule binding are valid | Type/admission/expansion check | "Implements the task" |
| Candidate behavior matches examples/properties | Targeted tests, property checks, differential cases | "Proved for all inputs" |
| Algorithm handles a suspected boundary | Minimal counterexample or discriminating test | Large redundant suite as a substitute for diagnosis |
| Implementation preserves an interface | Compatibility/differential checks against a pinned reference plus contract-derived cases | Reference parity means the reference is correct |
| Concurrency/state behavior is safe | Stress/model/property checks targeted at races, ownership, ordering, retries, or idempotency | A unit suite proves absence of races |
| Numerical behavior is acceptable | Error analysis plus adversarial/representative measurements under a stated relation | Mathematical equality implies floating-point equivalence |
| Performance is good | Profiler/benchmark on the actual target with a controlled protocol | Operation count or estimated speedup is measurement |
| Security boundary holds | Threat-model-specific negative tests, isolation/capability checks, review, or proof where appropriate | Data-only syntax is a sandbox |
| Universal property is proved | Named theorem checked under named assumptions by a named proof system | Finite tests are proof |

A tool should answer a question. If two plausible hypotheses predict the same tool
output, choose a more discriminating experiment.

## Counterexamples are first-class evidence

A small failure that isolates a semantic distinction can be more valuable than
thousands of passing cases. Preserve counterexamples that reveal:

- ordering or state-transition mistakes;
- boundary/overflow/aliasing behavior;
- mismatch between semantic scope and implementation schedule;
- incorrect ownership, lifetime, retry, or concurrency assumptions;
- compatibility drift;
- resource failures mistaken for functional failures.

Use the debugging loop:

```text
observe -> localize -> form competing hypotheses
        -> choose discriminating experiment -> repair root cause -> re-evaluate
```

Do not respond to every failure by adding a test, changing the representation, or
broadening the runtime. First identify which boundary is actually broken.

## Independence has multiple dimensions

Report these separately when they matter:

- **implementation diversity** — expected and actual results come from different
  implementation paths;
- **authorship/review independence** — the specification/oracle was independently
  authored or reviewed;
- **input hold-out** — final cases were inaccessible to the candidate-generation
  loop;
- **semantic independence** — the oracle does not simply re-execute the candidate's
  own lowered graph.

A second persona or model call can improve review quality but does not automatically
create independent ground truth. The bundled intseq direct-loop oracle has a
different implementation path from the AST interpreter, while sharing project
authorship and public inputs.

## Minimal evidence record

For a consequential claim, retain only what is needed to reconstruct it:

```text
claim/property
artifact + semantic dependency identity
question the check answers
command/tool or review method
scope/input set
result (PASS | FAIL | NOT_RUN | NOT_APPLICABLE)
relevant environment/assumptions
raw output or durable evidence location when useful
```

`NOT_RUN` is preferable to an invented pass. A hash binds bytes; it is not a
signature, proof, benchmark result, or statement of semantic correctness.

Do not demand raw logs for every trivial local edit. Preserve them when exact tool
behavior, reproducibility, benchmark integrity, failure diagnosis, or external
review depends on them.

## Acceptance

The task's acceptance policy is fixed outside the candidate representation. Hard
functional, safety, compatibility, effect, or required-evidence failures are not
compensated by lower latency or a weighted score.

Reserve final held-out evaluation for the end when claiming hold-out performance.
Repeatedly exposing its failures to the repair loop turns it into development data.
An accepted result is always **accepted under a stated policy and evidence scope**,
not universally certified correct.
