# Development workflow

**Consumer:** an agent implementing or reviewing Parallax. This is not the
[capsule synthesis protocol](../../core/PROTOCOL.md), which governs task-solving
attempts using a runtime. There is no BMAD installation or mandatory persona stack.

## One bounded episode

**Request → context.** Read START and the selected route. Inspect actual files and
working-tree changes; do not treat planned paths as existing code. Identify the
base commit, requested spec, allowed changes, and available tools before editing.
Existing user work is not a disposable baseline.

**Context → spec.** Use the smallest coherent implementation contract. A
`ready-for-dev` spec needs fixed intent, invariants/non-goals, relevant I/O and
edge cases, a file map, tasks, observable acceptance criteria, and runnable-in-
principle verification. Resolve discoverable answers from the repository first.
State reversible implementation choices; stop on an unresolved semantic or
permission conflict. Do not create a PRD or ADR for a local mechanical choice.

**Spec → implementation.** Set `in-progress` and append the baseline commit and
assumptions to the spec history. Implement only this slice. Add tests whose
expected behavior comes from the contract, not just the implementation. An
apparent reference/spec conflict is a finding to retain and resolve, not a silent
“cleanup.” New primitives and task changes need their own approval.

**Implementation → verification.** Run the selected checks. Record commands,
working directory, environment, exits, stdout/stderr or durable artifact paths,
input/source identities, and unrun checks under the
[verification guide](VERIFICATION.md). Keep task acceptance separate from type,
expansion, and execution evidence. Re-run affected checks after repairs.

**Verification → review → evidence.** Move to `in-review` when the candidate and
its evidence are available. Review the diff against each acceptance criterion,
semantic boundaries, and regression risks. For each finding, record fix, reasoned
rejection, explicit deferral, or decision needed. No minimum finding quota.
Record who reviewed and whether review was independent, same-model, or self-review.
Self-review alone does not satisfy a policy requiring an independent reviewer.

Mark `done` only when every required acceptance check passes, review is resolved,
and the evidence is linked. When required review/tools/oracle are missing, retain
`in-review` or `blocked` with the reason; do not invent a pass. A single-agent
implementation can finish its episode with a reviewable artifact rather than a
false completion claim.

## Lifecycle: one source of machine state

Each implementation spec's YAML frontmatter owns its state. Indexes and roadmap
links do not duplicate it. No separate sprint database is needed for one task.

| State | Meaning / permitted next move |
|---|---|
| `draft` | Intent or implementation contract incomplete; refine before coding |
| `ready-for-dev` | Readiness gate met; implementation may begin |
| `in-progress` | Coding/checking underway; continue or move to review |
| `in-review` | Candidate submitted with evidence; fix findings or complete |
| `done` | Acceptance and review policy met; subsequent changes are new work |
| `blocked` | Cannot safely proceed; record cause, preserved work, and required resolution |

A blocked spec can resume only after an explicit resolution is appended; choose
`ready-for-dev`, `in-progress`, or `in-review` to match the preserved work. Do not
delete the spec or failed history to retry. A failed check is evidence, not a
reason to erase its attempt. Discovery of a defect in a completed task creates
linked follow-up work instead of rewriting the old evidence as if it had passed.

## Changes, commits, and context maintenance

Use a branch and coherent commits. Do not force-push or overwrite concurrent user
changes. The PR summary should identify scope, spec, evidence, unresolved risks,
and the exact reviewed revision. A lack of push permission does not justify
claiming publication; retain a local patch/bundle and report the blocker.

After development starts, append revision/review history with date, actor, change,
reason, and impacted checks. Update the current spec body when legitimately
revised, but keep the prior contract recoverable in Git. For a measured trial,
freeze the starting contract: an output-changing revision terminates that trial
and begins a new version, rather than improving its score retrospectively.

Change each truth in its authoritative home. Keep README a summary and research
behind routes. Run `python tools/check_docs.py` after context edits. A useful
lesson becomes a targeted rule/spec correction only when it prevents a concrete
recurrence; do not dump the episode transcript into AGENTS.
