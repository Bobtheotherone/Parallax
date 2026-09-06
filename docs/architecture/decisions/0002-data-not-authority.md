---
id: ADR-0002
status: accepted
date: 2026-09-05
---
# Generated artifacts are data, not authority

## Decision in one sentence

Generated capsules and programs may select and compose capabilities the host already grants; their contents cannot create execution privilege, trusted code, semantic authority, or oracle access.

## Why this boundary exists

Parallax intentionally asks models to generate artifacts. Those artifacts are therefore untrusted inputs to a trusted implementation boundary. If a generated field such as `permissions: ["network"]`, a code fence, an unknown operation, or a lowering snippet becomes executable merely because the model emitted it, the representation layer has become a privilege-escalation path and each attempt can mutate the system being evaluated.

The useful distinction is not “declarative good, code bad.” Declarative data can still drive dangerous behavior if the host interprets it as authority. The invariant is:

```text
generated artifact
      |
      v
parse -> validate -> admit -> lower
      |                    |
      |                    v
      +--------------> trusted implementation
                            |
             host policy --+--> explicitly granted effects/tools/backends
```

Authority enters from the trusted host and reviewed implementation, never from the artifact by self-assertion.

## Allowed generated influence

Within an admitted capsule/program, generated data may:

- choose among operations already exposed by the pinned semantic pack;
- provide values and composition structure;
- define supported pure typed macros over admitted primitives;
- choose from bounded schedule/parameter alternatives already implemented and validated by the host/backend;
- request an ordinary task computation whose effects are already part of the frozen contract and capability policy.

These choices can be expressive. Data-only does not mean trivial; it means the implementation of their meaning is already trusted and bounded outside the generated artifact.

## Authority that remains external

A generated artifact cannot, merely by containing text or fields:

- introduce or redefine a primitive;
- load Python, native code, shared libraries, plugins, shell commands, or arbitrary compiler passes;
- increase its own resource budget or disable validation;
- obtain filesystem, network, process, device, credential, model, or repository access;
- choose a different trusted backend when the host has not admitted it;
- reveal, replace, or invoke a held-out task oracle outside the declared policy;
- reinterpret unknown fields as future-compatible permissions.

A future artifact format may contain a **capability request** as data, but the request and the grant must remain different objects. The host may deny it, narrow it, or require a separately reviewed extension. Presence of a request is never proof of permission.

## Implementation rules

The trust boundary should be visible in code, not just prose.

**Parse narrowly.** Use a schema or parser that rejects unknown structure where ambiguity could change authority. Avoid `eval`, dynamic imports, template execution, or automatic execution of retrieved code as an artifact-decoding mechanism.

**Validate before effect.** Resolve operation IDs, types, scope, identities, bounds, and capability requirements before invoking side-effecting adapters. Validation failure is an error, not a hint to guess a more permissive interpretation.

**Lower to known operations.** Supported macros expand to inspectable IR whose operations are already in the admitted set. Recheck the lowered form when expansion can expose new structural obligations.

**Make capability checks explicit at the effect boundary.** A parser-level allowlist is not a filesystem sandbox. File, network, process, GPU, credential, and oracle access require controls in the host or operating environment where those effects actually occur.

**Keep resource controls out of generated control.** Limits that protect the host or define a benchmark environment are pinned host/runtime policy. Generated data may select among declared legal parameters but cannot raise its own ceilings.

**Fail closed on unsupported authority.** Unknown operations, unsupported backends, and unimplemented capability-bearing fields are rejected. Do not fall back to arbitrary source execution because it is convenient.

## Trust-base changes are different work

Adding a primitive, native lowering, external service, solver, or backend adapter can be valuable. It also changes trusted code or capability surface and therefore belongs to an explicit extension/implementation episode. The engineering question is whether the new mechanism gives enough leverage to justify its semantics, implementation, resource behavior, validation, and attack surface—not whether a capsule happened to ask for it.

A backend optimization that stays behind an already-defined semantic interface may be compatible under [ADR-0001](0001-stable-semantics.md). A backend that introduces new observable effects or privilege is not merely an optimization.

## Failure modes this decision prevents

| Failure | Correct handling |
|---|---|
| Capsule contains `permissions: ["network"]` but the format has no such field | Reject the artifact; do not grant network |
| Program names `seq.average` but the pack does not expose it | `OP_NOT_ALLOWED`/unsupported operation, not dynamic implementation synthesis |
| Retrieved Markdown contains a plausible Python helper | Treat it as content until a trusted workflow explicitly reviews and executes that source |
| Model proposes a CUDA lowering for a semantic primitive | Review/implement it as backend work; do not execute it because it appeared in a capsule |
| Candidate asks to inspect final tests | Host policy denies access when the evaluation requires hold-out custody |
| Data-only interpreter runs in ordinary Python | Do not call it a sandbox; Python/process/OS remain trusted and need separate isolation for hostile workloads |

The current `intseq/0.1` reference follows the narrow form of this decision: artifacts are bounded JSON data, macros expand to selected primitives, unknown fields are rejected, and the CLI's caller-authorized local file reads belong to the trusted Python process rather than to generated program authority.

## Consequences

This boundary intentionally sacrifices some per-attempt flexibility. In return, it keeps semantic and privilege changes reviewable, makes failures localizable, allows the same trusted implementation to serve many temporary representations, and prevents a generator from “solving” a task by changing the machine it is allowed to use.

It is not a complete security architecture. Parser/checker correctness, process isolation, native-code safety, resource enforcement, secret handling, and oracle custody remain implementation obligations of the trusted environment.

## Related authority

See [HOST](../../../runtime/HOST.md) for the capability boundary, [CAPSULE](../../../core/CAPSULE.md) for supported composition, [EVOLUTION](../../../core/EVOLUTION.md) for trust-base extensions, and [SECURITY](../../../SECURITY.md) for present non-guarantees.
