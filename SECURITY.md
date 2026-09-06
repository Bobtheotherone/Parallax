# Security and trust boundary

Parallax is a **pre-production research prototype**, not a hardened execution
sandbox or production security boundary. The current maturity baseline is in
[PROJECT.md](docs/PROJECT.md), and the intended execution/permission boundary is
owned by [HOST.md](runtime/HOST.md).

This file explains how to interpret and report security-relevant behavior. It does
not expand the runtime's authority or claim that unimplemented controls exist.

## Supported versions

There is currently no released production version or security-support matrix. The
repository contains routed documentation, an embedded intseq reference, tooling,
and implementation specifications. Security claims should therefore name the
exact commit, file, tool, or future runtime version they apply to.

No response-time or remediation SLA is promised at this prototype stage.

## What is security-relevant

Please treat the following as security-relevant findings when they affect actual
repository code or a future implementation:

- arbitrary code execution where an artifact is specified to remain data-only;
- bypass of an operation allowlist, type/scope check, capsule binding, or documented
  resource/admission boundary;
- unintended filesystem, network, process, model, oracle, or host capability gained
  from generated or retrieved content;
- unsafe automatic execution of arbitrary retrieved code fences;
- a documented security boundary that the implementation claims to enforce but can
  be bypassed;
- exposure of held-out acceptance material through a component that is supposed to
  keep it outside candidate context or write permissions.

A useful report identifies the affected revision, expected boundary, minimal
reproduction, observed result, and realistic impact. Separate implementation facts
from hypothetical downstream deployments.

## Known non-guarantees

The following are deliberate current limitations, not by themselves vulnerabilities:

- the repository does not provide an operating-system sandbox;
- bounded AST/resource checks are not hard wall-clock, memory-isolation, or hostile
  code containment guarantees;
- the embedded/reference CLI may read caller-authorized local paths;
- no LLM orchestration host, isolated final oracle, native/GPU backend, or production
  capability system is implemented;
- a capsule/program hash binds content under the documented recipe but does not
  authenticate authorship or prove correctness;
- typechecking, expansion, execution, and finite tests do not establish task
  correctness or universal security properties.

See the [architecture trust boundary](docs/architecture/ARCHITECTURE.md#trust-boundary-and-resource-policy),
[agent constraints](AGENTS.md), and [evidence rules](core/EVIDENCE.md) for the
corresponding authoritative statements.

## Reporting a sensitive finding

Do not publish secrets, credentials, private benchmark material, or a weaponized
proof of concept in a public issue.

If GitHub offers private vulnerability reporting for this repository, prefer that
channel. Otherwise, use a private contact method made available by the repository
owner. If no private channel is available, open only a minimal public issue asking
for a private reporting path and omit exploit details until one is established.

Non-sensitive security-design questions can be discussed publicly, but distinguish
a proposed hardening improvement from a demonstrated vulnerability.

## Integration responsibility

Generated capsules and programs are data. The parser/checker/expander, interpreter
or backend, Python/runtime environment, and external host remain trusted
implementation. A host processing hostile workloads must separately provide the
process isolation, filesystem/network policy, resource controls, capability
restrictions, oracle custody, and evidence retention required by its threat model.

Do not infer those controls from Markdown instructions or from the absence of an
operation in a generated artifact.
