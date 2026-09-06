# BMAD methodological study

**Consumer:** maintainer reviewing why the context/development system is shaped
this way. This is provenance, not another agent instruction layer.

## Source pin and scope

Repository: `bmad-code-org/BMAD-METHOD`. Default branch studied: `main`.
Commit: **`beb368e5fc9b95bcec5e1de5bc7870dc15bece72`**.
[Commit source](https://github.com/bmad-code-org/BMAD-METHOD/tree/beb368e5fc9b95bcec5e1de5bc7870dc15bece72).
The default-branch head was read through GitHub and rechecked at the same SHA.
No BMAD repository write, installation, workflow execution, or runtime dependency
was introduced.

The recursive Git tree was enumerated first. Canonical English methodology was
read from repository instructions, `docs/`, and `skills/`, including actual
Markdown templates, step files, reviewer prompts, schemas, and relevant TOML
persona/customization definitions—not only marketing documentation. The study
covered project context, planning/requirements/architecture/specs, implementation,
autonomous single-unit workers, review/verification, status transitions,
retrospectives, existing-codebase work, routing, and documentation style. Related
analysis/UX/elicitation/research skills were read to understand artifact boundaries,
not to import them into Parallax.

Translated READMEs (`README_CN.md`, `README_KR.md`, `README_VN.md`) were identified
as translations rather than separate authorities. Release history, governance,
test fixtures/example outputs, and derived web-bundle distribution material were
not treated as independent definitions of the current development methodology.
The canonical English source, not a translated/packaged duplicate, governs the
lessons below. This was a methodology reading, not an audit or execution of BMAD's
installer and implementation scripts, and not evidence of its efficacy.

The corpus enumeration is reproducible independently:

```sh
git clone https://github.com/bmad-code-org/BMAD-METHOD.git bmad-study
git -C bmad-study checkout --detach beb368e5fc9b95bcec5e1de5bc7870dc15bece72
git -C bmad-study ls-tree -r --name-only HEAD -- '*.md'
```

Those commands describe a reproduction route; network clone was unavailable in
the bootstrap container, so this study used GitHub reads instead.

## What Parallax adopts

| Lesson | Studied canonical sources | Parallax application |
|---|---|---|
| Ambient context must earn its cost; route local facts | [AGENTS](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/AGENTS.md), [project-context skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/skills/bmad-project-context/SKILL.md), [context maintenance](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/existing-codebases/set-and-maintain-project-context.md) | Compact AGENTS; START and activity routes; research is optional |
| Intent and execution are distinct contracts | [spec skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/skills/bmad-spec/SKILL.md), [requirements/spec guide](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/plan/define-requirements-and-a-specification.md), build spec templates | PROJECT defines what/why; one bounded spec defines observable behavior and exclusions |
| Architecture records non-obvious cross-unit decisions | [architecture skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/skills/bmad-architecture/SKILL.md), its spine templates, [architecture guide](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/plan/design-ux-and-architecture.md) | One authority map and three meaningful ADRs; no decision record for every file |
| Lifecycle state belongs in a durable implementation record | [build skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/skills/bmad-build/SKILL.md), [autonomous loop guide](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/build/autonomous-development-loops.md), actual build/build-auto templates and step files | Spec frontmatter owns state; append revision/evidence history; blocked is legitimate |
| Review must test intent and changed behavior, not just style | [code-review skill](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/skills/bmad-code-review/SKILL.md), its review prompts, [review guide](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/build/review-a-change.md) | Acceptance mapping, concrete findings and dispositions; missing evidence stays missing |
| Verification, human understanding, and aggregate learning are different | [test guide](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/build/test-completed-work.md), [walkthrough](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/build/walk-through-a-change.md), [retrospective](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/skills/bmad-retrospective/SKILL.md) | Distinct test evidence, review, and targeted lessons; no transcript in AGENTS |
| A worker episode is not a backlog scheduler | [build-auto source](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/skills/bmad-build-auto/SKILL.md), [autonomous guide](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/build/autonomous-development-loops.md) | Start one spec; do not autonomously execute the roadmap |
| Existing files are evidence; planning must not invent a greenfield state | [existing-codebase guide](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/existing-codebases/getting-deeper.md), [planning paths](https://github.com/bmad-code-org/BMAD-METHOD/blob/beb368e5fc9b95bcec5e1de5bc7870dc15bece72/docs/plan/choose-a-planning-path.md) | Inspect actual tree, separate embedded source from planned package, preserve user edits |

## What Parallax deliberately does not import

No `_bmad` directory, workflow installation, persona cast, custom skill loader,
sprint database, broad persistent-facts layer, or BMAD-specific file-writer rule
is needed for this repository. Spec status is enough machine state for one task.
No automatic rollback may erase user work or failed-run history. A blocked spec
is resumed through a recorded resolution, not deletion of the record.

Some review prompts request a minimum finding count. Parallax does not: findings
need evidence; zero findings is possible. Multiple personas or fresh model sessions
are not an independent task oracle. Generated tests from existing code cannot
replace separately specified expected behavior. These departures preserve the
source archive's stronger evidence and authority boundaries.

The result is a small Parallax-specific system informed by BMAD's distinctions,
not a copy of its workflow implementation or a claim that its methods have already
been validated here.
