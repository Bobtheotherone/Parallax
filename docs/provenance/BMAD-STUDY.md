# BMAD methodological study — historical influence

This document records what the 2026-09-05 bootstrap studied in BMAD and which ideas influenced Parallax. It is provenance, not an instruction to run BMAD or reproduce its workflow structure.

## Source pin and method

Repository: `bmad-code-org/BMAD-METHOD`  
Default branch studied: `main`  
Pinned commit: **`beb368e5fc9b95bcec5e1de5bc7870dc15bece72`**  
Source: [pinned GitHub tree](https://github.com/bmad-code-org/BMAD-METHOD/tree/beb368e5fc9b95bcec5e1de5bc7870dc15bece72)

The bootstrap enumerated the recursive Git tree, then read the canonical English methodology across repository instructions, `docs/`, and `skills/`, including Markdown templates, step files, review prompts, schemas, and relevant TOML persona/customization definitions. The study covered project context, requirements/specification, architecture, implementation, autonomous single-unit work, review/verification, lifecycle state, retrospectives, existing-codebase work, routing, and documentation style.

Translated READMEs (`README_CN.md`, `README_KR.md`, `README_VN.md`) were recognized as translations rather than separate methodological authorities. Release history, governance material, fixtures/example outputs, and derived web-bundle distribution artifacts were not treated as independent definitions of the current method.

No BMAD repository write, installation, workflow execution, or runtime dependency was introduced. The bootstrap environment could not perform the network clone shown below, so the study used GitHub reads against the pinned commit instead. The commands remain a reproducible way for a later reader to enumerate the Markdown corpus:

```sh
git clone https://github.com/bmad-code-org/BMAD-METHOD.git bmad-study
git -C bmad-study checkout --detach beb368e5fc9b95bcec5e1de5bc7870dc15bece72
git -C bmad-study ls-tree -r --name-only HEAD -- '*.md'
```

This was a methodology reading, not an audit of BMAD's implementation and not evidence that its process improves engineering outcomes.

## Ideas that survived into Parallax

The useful lessons were mechanisms, not ceremony.

| Studied idea | Engineering value retained in Parallax | Representative source |
|---|---|---|
| Route ambient context instead of loading everything | Reduces irrelevant context while preserving task-critical semantics; `START.md`/`ROUTES.md` provide task-directed entry | [project-context skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/skills/bmad-project-context/SKILL.md) |
| Separate intent from bounded implementation contract | Lets an implementer reason from observable behavior/invariants instead of a project essay | [spec skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/skills/bmad-spec/SKILL.md) |
| Record architecture only for consequential cross-cutting choices | Preserves dependency/trust/compatibility reasoning without an ADR for every local choice | [architecture skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/skills/bmad-architecture/SKILL.md) |
| Treat existing code/files as evidence | Prevents greenfield plans that invent nonexistent components or erase compatibility constraints | [existing-codebase guidance](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/existing-codebases/getting-deeper.md) |
| Review behavior and intent, not only style | Directs attention to contract failures, state/dataflow, regressions, and concrete consequences | [code-review skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/skills/bmad-code-review/SKILL.md) |
| Keep testing, human review, and aggregate learning conceptually distinct | Prevents a test pass, walkthrough, or retrospective from masquerading as the same kind of evidence | [test guide](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/build/test-completed-work.md) |
| Scope an autonomous worker to one bounded unit | Supports high agency without turning one coding episode into an unsupervised backlog scheduler | [autonomous-loop guide](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/build/autonomous-development-loops.md) |

These ideas aligned with constraints already present in the adaptive-representations source: stable task meaning, routed context, bounded episodes, explicit evidence, and separation of task acceptance from internal checking.

## What Parallax deliberately did not import

The bootstrap did **not** install or copy BMAD's workflow implementation. It did not add an `_bmad` tree, persona cast, custom skill loader, sprint database, or broad persistent-facts layer. BMAD is not a runtime or development dependency of Parallax.

Several methodological choices were also rejected or narrowed:

- no mandatory role-playing/persona stack for repository development;
- no minimum review-finding quota;
- no requirement to create PRDs, ADRs, or status artifacts for reversible local choices;
- no automatic rollback that can erase user work or failed evidence;
- no assumption that another model persona supplies independent ground truth;
- no generated test suite accepted as an external task oracle merely because it is separate text;
- no worker authority to advance unrelated roadmap items after finishing its requested unit.

Later Parallax guidance may compress process further when a step does not change an engineering decision. That is compatible with this historical study: the point was to retain useful distinctions, not the shape of BMAD's ceremony.

## Lasting interpretation

The strongest BMAD-derived idea for Parallax is that **context and process are interfaces to cognition**. They should expose the decisions that improve implementation quality and remove the ones that merely consume attention.

Parallax therefore uses routing, bounded specs, architecture decisions, and evidence distinctions as tools when they reduce search space or protect correctness. None is valuable because a methodology says it must exist. This study records the source of those influences; the current Parallax documents own their present behavior.
