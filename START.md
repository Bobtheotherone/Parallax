# Start: choose the kind of work

Read [AGENTS.md](AGENTS.md) once, then select **one** entry below. Do not recursively
load the repository. Links are routes, not automatic includes.

## Implement or review Parallax itself

The first programming task is [SPEC-001](docs/specs/001-intseq-reference.md).
Read it in full, including its explicit context list, then the
[development workflow](docs/development/WORKFLOW.md). Inspect the working tree
before editing. The spec's frontmatter is the authoritative lifecycle state.

A `ready-for-dev` spec is a contract to implement, not evidence of implementation.
Follow its acceptance criteria and record checks actually performed. No model API,
GPU toolchain, or BMAD installation is needed for SPEC-001.

Do **not** load the thesis, unrelated packs, or all role documents for this task.
The `roles/` files describe capsule/program-generation roles, not a mandatory team
or a software-development framework.

## Solve a task using a representation

Use [ROUTES.md](ROUTES.md), [task contracts](core/CONTRACT.md), and the
[task template](templates/TASK.md). Establish intent, unresolved semantic questions,
real tools/backends, required evidence, and a total budget before selecting a mode:
`DIRECT`, `CAPSULE`, or `DESIGN_ONLY`.

A supported capsule run follows [the synthesis protocol](core/PROTOCOL.md).
Freeze task and capsule; do not expose a held-out oracle through a convenience
context route. An implementation agent may read the public reference and tests;
a measured solution-generating agent receives only its declared task packet.
Those are different contexts with different read permissions.

## Research, extend, or maintain documentation

Select the matching row in [ROUTES.md](ROUTES.md). The
[authority map](docs/architecture/ARCHITECTURE.md) identifies which document to edit.
Record only the intent, route, selected spec/contract revision, unresolved issues,
and available tools needed for this episode—not another project essay.
