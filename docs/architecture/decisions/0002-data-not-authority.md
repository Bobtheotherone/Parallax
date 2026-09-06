---
id: ADR-0002
status: accepted
date: 2026-09-05
---
# Generated artifacts are data, not authority

## Context and forces

An LLM may emit plausible source code, capability requests, or undocumented
operations inside a capsule. Treating that text as trusted implementation would
let the generator change the checker or escape the comparison's semantic boundary.
A useful capsule still needs enough expressive structure to compose algorithms.

## Alternatives

Executing generated Python/compiler fragments is flexible but adds executable
trust on each attempt. Allowing declarative permission requests to take effect
silently confuses requested capabilities with granted authority. Data-only
compositions require a smaller surface but keep the trust change explicit.

## Decision

The ordinary capsule/program path accepts bounded structured data interpreted by
an existing implementation. Capsules may select primitives and define typed macros;
they cannot grant permissions, load native code, redefine a primitive, or choose a
new acceptance oracle. The external host owns tool access, approved implementations,
isolation, budget enforcement, and oracle custody.

## Consequences and follow-up

Unsupported fields/operations are rejected rather than executed or guessed. A new
primitive/backend is a reviewed project change, not a capsule revision. Pure AST
interpretation does not itself make Python or the operating environment secure.
Host isolation remains unimplemented and must be specified before exposing hostile
workloads or native adapters. The first extraction task must preserve the existing
boundary without pretending to implement that host.

Source basis: [host boundary](../../../runtime/HOST.md),
[capsule admission](../../../core/CAPSULE.md), and
[extension classes](../../../core/EVOLUTION.md).
