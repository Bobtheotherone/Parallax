# Extension, revision, and retirement

The representation can be short-lived; the ability to reconstruct its meaning
must survive as long as its artifacts matter.

## Extension classes

**Selection/restriction:** expose fewer existing operations or tighten a domain.
Check that the task remains supported; this is not automatic.

**Compositional macro:** define a typed expression over supported primitives.
Use hygienic substitution and bounded expansion. Validate the expansion. v0.1
supports this class but prohibits recursive or cross-macro calls in macro bodies.

**New primitive/backend:** add meaning or implementation not already available.
This changes the trusted implementation boundary. Require a separate branch or
review stage, formal semantics, reference behavior, tests, implementation,
resource policy, provenance, and any required proof/checker integration. A regular
programming episode cannot admit this class by merely editing a capsule.

## Conservative changes

New spelling must not redefine existing operations. Version existing meanings
immutably. A representation extension may preserve old meanings yet change search
behavior, context cost, or resource consumption; evaluate those separately.

Cached capsules are reusable only after checking the task/input domain, pack hash,
runtime/backend hash, environment, and evidence policy. Model/decoder versions and
tutorial variants also matter for empirical success estimates. Do not reuse an
old success rate as a guarantee for a changed model or environment.

## Retirement

Archive contract, original capsule, canonical IR, program, dependency identities,
checker/runtime sources or durable references, tests, tool results, and native
artifact where one exists. Preserve debug/source correspondence when lowering.
The surface need not stay in active use; its semantics cannot simply be discarded
if later audit, debugging, or reproducibility is required.

For larger systems, make component interfaces explicit about data, effects,
errors, ownership, and concurrency. Matching function names or JSON schemas does
not establish semantic compatibility between independently generated languages.
