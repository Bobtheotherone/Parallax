# Security and trust boundary

Parallax is a **pre-production research prototype**. It provides design rules and
an embedded reference interpreter; it is not a hardened sandbox, production
capability system, or isolated model-execution service.

Security depends on keeping generated representations useful without allowing them
to become authority.

## Trust model

| Layer | Trust / authority |
|---|---|
| User/model/retrieved text, capsules, programs, examples, task inputs | Treat as data that may be malformed, adversarial, misleading, or resource-expensive |
| Parser, schema/type checker, macro expander, interpreter/backend | Trusted implementation that must validate data before giving it operational meaning |
| Host/integration layer | Owns process lifetime, filesystem/network/tool/model access, credentials, resource limits, pack/backend selection, and oracle custody |
| Task acceptance mechanism | Owns the external judgment of task success; it must not be silently replaced by candidate computation |

The current embedded `intseq` reference implements only the middle data-checking and
interpretation slice. [runtime/HOST.md](runtime/HOST.md) describes host obligations
that are **not** implemented by this repository.

## Security invariants

1. **Data cannot grant capability.** A capsule/program field, retrieved code fence,
   prompt, or model statement cannot authorize network access, file access, process
   creation, native code, model calls, secrets, or final-oracle access.
2. **Unknown structure fails closed.** Unsupported operations, fields, versions,
   types, scopes, or identity bindings are rejected rather than guessed or executed.
3. **Semantic authority is pinned.** Generated content may select or compose admitted
   operations; introducing a trusted primitive/backend requires explicit
   implementation and versioned evolution.
4. **Acceptance stays external.** Candidate code cannot redefine the task oracle or
   convert successful execution into an acceptance claim.
5. **Resource checks are scoped claims.** AST depth/node, integer, vector, work, or
   document-size limits reduce some denial-of-service surface; they are not process
   isolation, memory safety, or a hard wall-clock guarantee.
6. **Evidence does not self-authenticate.** Hashes bind content under a recipe but
   do not prove authorship, correctness, safety, or freshness.

## Main attack surfaces

**Capability confusion.** The highest-risk design error is treating generated text
as permission. Keep capability grants in host configuration and pass only explicit,
least-privilege handles into trusted implementations.

**Arbitrary code execution.** Do not generalize the reviewed
[runtime/REFERENCE.md](runtime/REFERENCE.md) extraction procedure into automatic
execution of arbitrary Markdown or retrieved code. A data-only AST is valuable
precisely because it avoids this path.

**Parser and evaluator resource exhaustion.** Validate size before expensive
parsing, bound recursion/expansion/work, reject oversized integers and collections,
and test limits near the actual boundary. For hostile workloads, enforce CPU,
memory, process, and wall-time limits outside the interpreter as well.

**Backend/native bridges.** A native/GPU/compiler adapter crosses into a much larger
trusted surface: ABI/layout, aliasing, device resources, numerical behavior,
compiler flags, and generated code all become relevant. Do not expose such a
backend until those boundaries are implemented and tested.

**Oracle or secret leakage.** Held-out acceptance inputs, credentials, private data,
and privileged diagnostics must remain outside candidate-readable/writable state
when secrecy is part of the evaluation or security model. Avoid logging secrets
into run artifacts or prompts.

**Semantic substitution.** A malicious or buggy artifact may be perfectly
well-formed while computing the wrong thing. Type/admission checks are not a task
oracle; maintain a separately specified acceptance path.

**Identity confusion.** Pin semantic pack/runtime/backend identities separately from
capsule/program identities. Reject mismatched bindings. Do not interpret an old
version identifier using silently changed semantics.

## Host requirements for hostile workloads

A production-grade host would need controls outside this repository, including
process isolation, filesystem/network policy, CPU/memory/wall-time enforcement,
credential scoping, safe temporary storage, controlled native/device access,
final-oracle custody, log redaction, and auditable capability assignment.

Those controls must exist in code or infrastructure. Markdown instructions,
allowlist prose, and a model's promise not to use a capability are not substitutes.

## Current non-guarantees

The repository does not currently provide:

- an operating-system sandbox or hostile-code containment;
- a production orchestration host or capability broker;
- an isolated held-out oracle;
- a native/GPU backend;
- formal verification of the parser, expander, interpreter, or host;
- a released security-support matrix or remediation SLA.

The reference CLI can read caller-selected local paths. Its bounded interpreter does
not execute generated Python, but the Python implementation and operating
environment remain trusted.

## Security review of a change

When a change crosses a trust boundary, answer the engineering questions that
matter: what new data is accepted, what authority it can reach, where validation
occurs, what resource can be exhausted, what secrets become observable, and how a
failure is contained. Prefer concrete enforcement and adversarial tests over policy
text.

## Reporting a vulnerability

Do not publish credentials, private benchmark material, or a weaponized exploit in
a public issue. If GitHub private vulnerability reporting is enabled, use it.
Otherwise use a private contact channel provided by the repository owner; if none is
available, open only a minimal public request for a private reporting path.

For a useful report, include the affected revision, expected trust boundary,
minimal reproduction, observed behavior, and realistic impact. Distinguish a
demonstrated implementation flaw from a proposed hardening improvement.
