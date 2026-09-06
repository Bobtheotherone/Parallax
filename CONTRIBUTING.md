# Contributing to Parallax

Parallax is a pre-production research prototype. Contributions should preserve its
central discipline: adapt representations without quietly changing the task,
trusted semantics, acceptance policy, or evidence standard.

This file is contributor guidance, not a new source of semantic authority. When it
conflicts with an owning document, treat that conflict as a defect and follow the
[source-of-truth map](docs/architecture/ARCHITECTURE.md#source-of-truth-map).

## Before changing anything

1. Read [START.md](START.md) and choose the smallest applicable route in
   [ROUTES.md](ROUTES.md). Do not load or edit unrelated research by default.
2. Inspect the actual branch and files before planning work. A roadmap entry or
   planned path is not evidence that an implementation exists.
3. Identify the authoritative home for the truth you intend to change. README is
   a summary; templates and examples do not override contracts or semantics.
4. For implementation work, use the selected file in `docs/specs/` as the bounded
   contract and follow the [development workflow](docs/development/WORKFLOW.md).

Do not weaken a task, checker, test, resource boundary, or acceptance oracle to
make an implementation pass. Preserve frozen identities and historical evidence.

## Choose the right kind of change

**Documentation or routing.** Edit the owning document and keep derived summaries
consistent. Run the documentation checker after changing live Markdown or links.
Historical migration claims belong in [provenance](docs/provenance/SOURCE-MAP.md),
not in a competing live specification.

**Implementation.** Work from an approved spec. Keep the change within its stated
file map, invariants, non-goals, acceptance criteria, and verification plan.
Record checks actually run and leave unavailable checks explicit.

**New primitive, backend, or semantic behavior.** This changes the trusted
implementation boundary. Follow [EVOLUTION.md](core/EVOLUTION.md): require an
explicitly reviewed change with semantics, reference behavior, tests, resource
policy, provenance, compatibility consequences, and an implementation spec as
appropriate. Generated capsules cannot authorize this class of change.

**Research or experiments.** Keep implementation truth separate from hypotheses.
Use the routed benchmark/evidence documents and report negative or inconclusive
results without promoting them into capability claims.

## Branches, commits, and pull requests

Use a branch and coherent commits. Do not force-push over someone else's work or
erase failed-run history. Preserve user changes that are outside the requested
scope.

A pull request should state:

- the problem and bounded scope;
- the owning spec/contract or documentation authority, when applicable;
- files and semantic boundaries intentionally not changed;
- verification actually performed, including failures and `NOT_RUN` checks;
- evidence locations or reproducible commands;
- unresolved risks, review needs, or owner decisions.

Review the exact revision being proposed. Self-review is useful, but it is not an
independent oracle and does not satisfy a policy that explicitly requires an
independent reviewer.

## Verification

For documentation and context changes, run:

```sh
python tools/check_docs.py
```

For implementation changes, also run the checks required by the selected spec and
follow [VERIFICATION.md](docs/development/VERIFICATION.md). Do not describe a hash,
typecheck, finite test suite, or source-reported historical result as stronger
evidence than it is; [EVIDENCE.md](core/EVIDENCE.md) defines the project's result
language.

When a required tool or oracle is unavailable, report that limitation rather than
inventing a pass.

## Licensing and imported material

No project license has been selected. Do not infer redistribution rights from the
repository's public visibility or from material used for research. Avoid adding
third-party code, text, datasets, or generated artifacts with unclear provenance
or incompatible terms. Licensing remains a repository-owner decision, as recorded
in [PROJECT.md](docs/PROJECT.md).
