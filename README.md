# Parallax

**Task-adaptive representations over stable, checkable semantics.**

Parallax investigates whether an LLM can solve engineering tasks more reliably or
at lower total cost by adapting the programming interface to the task—without
changing the task, trusted semantics, checker, backend, or acceptance oracle.
The research term is **adaptive representation synthesis**. A direct solution
remains preferable when adaptation does not justify its cost.

## Current state

**Pre-production research-prototype bootstrap.** This repository contains semantic
contracts, context routes, an embedded Python `intseq` reference, worked artifacts,
a proposed benchmark protocol, and one implementation-ready development task.
The archive includes a source-author public test report; it has **not been
independently reproduced during this bootstrap**.

There is no packaged Parallax runtime, LLM orchestration host, native/GPU backend,
or completed LLM benchmark. Documentation readiness is not system validation.
The [project intent](docs/PROJECT.md) owns scope and the maturity baseline.

## Start here

**Coding agent:** read [START.md](START.md), then implement
[SPEC-001: package and characterize the intseq reference](docs/specs/001-intseq-reference.md).
Its status is `ready-for-dev`; its implementation checks have not run.

**Human:** read [project intent](docs/PROJECT.md) and the
[architecture](docs/architecture/ARCHITECTURE.md). The
[roadmap](docs/ROADMAP.md) sequences exit gates, not shipped features.

**Researcher:** use the [benchmark protocol](docs/benchmarking/PROTOCOL.md)
before the [thesis](research/THESIS.md) and [related work](research/RELATED-WORK.md).
The worked example is public development material, not a hidden benchmark.

[ROUTES.md](ROUTES.md) maps every activity to its minimum context.
The preserved source, migration dispositions, and pinned BMAD methodological
reference are in [provenance](docs/provenance/SOURCE-MAP.md).
BMAD is not installed and is not a dependency.

## Checks and boundaries

`python tools/check_docs.py` checks documentation links, provenance, frozen
identities, and spec state structure. It does **not** execute Parallax semantics.
Reference reproduction is a separate, explicit route in
[runtime/REFERENCE.md](runtime/REFERENCE.md).

`AGENTS.md` is operating guidance, not a sandbox. Runtime permissions and held-out
oracle secrecy require an external host. Legacy `arl-capsule/0.1` and
`arl-program/0.1` wire identifiers are deliberately preserved.
No project license has been selected in this bootstrap.
