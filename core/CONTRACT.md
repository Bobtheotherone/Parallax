# Task contracts

A task contract determines success before representation search. It is not a
language specification and must not be inferred from whichever program compiles.

Record the requirement source, input domain, output relation, observable effects,
error cases, numerical policy, target, performance objective, prohibited behavior,
acceptance method, and unresolved assumptions. Name who may approve a revision.
Use [the template](../templates/TASK.md).

## Two different questions

`CheckCapsule(program)` asks whether a program is meaningful and permitted in its
capsule. `CheckTask(artifact, contract)` asks whether it implements the requested
behavior. Neither operation substitutes for the other.

A behavioral contract can be a mathematical relation, a trusted executable
reference, a formal specification, or a combination. Examples alone typically
leave multiple meanings possible. A reference can also be wrong; record its origin
and review status, not just its existence.

## Freeze and independence

Freeze the contract and acceptance policy before choosing a representation.
During development, expose public examples and counterexamples. Keep final
held-out tests outside the generator's context and outside the capsule builder's
read permissions where the evaluation environment supports that separation.

If the same LLM proposes task, program, and tests, the result is internally
consistent evidence, not independent validation. Multiple personas of the same
model do not establish independent ground truth.

A task clarification is allowed, but creates a new contract version and invalidates
comparisons that assumed the old one. Do not hide changes to tolerances, input
bounds, or unsupported cases inside a language revision.

## Stage-zero stop condition

If uncertainty can change the correct output or make execution unsafe, request
clarification or return `DESIGN_ONLY` with the unresolved obligation. Otherwise
state a provisional assumption explicitly and do not overstate its authority.
