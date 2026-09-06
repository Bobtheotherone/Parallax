---
id: SPEC-NNN
status: draft
spec_version: 1
created: YYYY-MM-DD
depends_on: []
---
# One bounded implementation outcome

Use a spec when a coding agent needs a durable implementation contract. A strong
spec compresses the engineering problem: it fixes externally meaningful behavior,
exposes architecture and hard constraints, identifies the dangerous unknowns, and
leaves reversible local choices to the implementer. Delete guidance or sections
that do not affect this slice.

## Intent

State what becomes possible after this change, who/what consumes it, and the
observable outcome. Include why this slice is the right boundary rather than a
larger rewrite or a local patch.

## Required context

Link the smallest set of authoritative contracts, interfaces, code, and reference
artifacts needed to implement the change. Distinguish authority from examples or
research. Name any known contradiction that could change the implementation.

## Approach and tooling choice

Describe only consequential choices already fixed by the spec: language/runtime,
important dependencies, interoperability constraints, required target/backend, or
an algorithm/representation choice that downstream code must share.

For uncertain choices, state the engineering question and the cheapest experiment
that can discriminate alternatives. Prefer existing mature libraries and native
interfaces when they dominate bespoke machinery.

## Invariants

List properties that must survive any implementation choice: compatibility,
semantic meaning, ordering, numerical behavior, state transitions, ownership,
security/capability boundaries, persistence, determinism, or task-acceptance
separation. If an invariant may change, name the authority allowed to change it.

## Non-goals

Exclude adjacent work that is tempting but unnecessary for the outcome. Do not use
non-goals to evade behavior the task actually requires.

## Interfaces and observable behavior

Define the boundary precisely enough to implement and review:

- inputs/outputs, types/shapes/schema, versioning, and compatibility;
- errors, partial failure, retries/idempotence, and cancellation where relevant;
- effects, state ownership, lifetimes, concurrency/ordering, and transactional
  behavior where relevant;
- numerical policy, precision/tolerance, determinism, and special values where
  relevant;
- resource/performance envelope: asymptotics, expected scale, memory/allocation,
  I/O/serialization, latency/throughput, device boundaries, or other real limits;
- observability needed to localize failures without coupling callers to internals.

Use tables, state machines, pseudocode, or examples when they are more precise than
paragraphs. Include at least one realistic edge/counterexample for semantics that
are easy to misread.

## Engineering model

Describe the dependency/dataflow that should be true after the change. Identify the
owner of mutable state, the direction of dependencies, where validation occurs,
and which boundaries are trusted. For multi-module work, show the minimum component
map needed to prevent local implementations from fighting each other.

If performance matters, identify the likely bottleneck and the representation/data
movement choices that dominate it. If concurrency matters, state the synchronization
or ownership model rather than leaving races to implementation folklore.

## File map

Map existing and planned paths to responsibilities. Mark new paths as planned text,
not links. The map should expose dependency direction and where tests/fixtures/adapters
belong; it is not a quota of files to touch.

## Implementation tasks

Order a small number of milestones by dependency and information value. Attack the
highest-risk semantic or integration uncertainty early. Prefer vertical slices that
can be exercised through a real interface over a long sequence of scaffolding steps.

Do not prescribe low-level edits the implementer can safely derive. Do identify
migrations, compatibility shims, data transformations, or rollout sequencing when
partial states could break users.

## Acceptance criteria

Give stable `ACn` identifiers for externally meaningful conditions. An acceptance
criterion is a property, not a command. Map each property to the strongest practical
way to discriminate correct from plausible-but-wrong implementations.

A good set covers the happy path, realistic boundary/failure behavior, compatibility,
and any required performance/resource property without optimizing for test count.
Expected behavior must come from the contract/reference/oracle, not be regenerated
from the candidate under test.

## Verification plan

List the tools that answer remaining questions: focused tests, compiler/type checker,
static analysis, reference/differential checks, property/fuzz checks, debugger,
profiler, benchmark, sanitizer, integration environment, or proof checker as
appropriate. State exact commands only when they are stable and useful.

For each important check, record what failure would mean. Measure performance only
on the relevant target with enough methodology to separate noise from a real change.
Mark planned commands as unexecuted until they actually run.

## Readiness and history

A spec is ready when the contract is implementable without guessing a consequential
semantic, permission, compatibility, or irreversible architecture decision. Local,
reversible ambiguity is not a blocker: choose a sensible default during implementation
and keep moving.

Append only history that changes how a future implementer/reviewer interprets the
contract: baseline revision, approved contract change, material failed assumption,
acceptance evidence, and review disposition. Git already stores ordinary editing
history.
