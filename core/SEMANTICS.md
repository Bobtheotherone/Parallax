# Semantic boundaries

The permanent part should be a small set of stable interfaces and domain packs,
not an ambitious claim that one universal graph has solved all domain semantics.
A tensor pack, transaction pack, and protocol pack need distinct definitions of
observable behavior. A common graph container does not supply those definitions.

## Correct maps, not sets of unrelated syntax

For capsule C, let E_C map its programs to a stable domain IR. Let D map that IR
to a backend implementation. Let Phi_T describe task success. A program is useful
when Phi_T(D(E_C(p))) holds under the frozen environment and observation model.

Programs in two syntaxes are not literally subsets of each other. Compare their
lowered behaviors, or a stated relation between behaviors. Include errors, effects,
termination, resource constraints, and relevant numerical observations as needed.

## Two distinct obligations

1. **Representation preservation:** macro expansion and lowering preserve the
   capsule's specified behavior, under stated assumptions.
2. **Task satisfaction:** that behavior meets the externally fixed task contract.

Correct compilation of the wrong algorithm still fails the second obligation.
A well-typed program can compute the wrong answer. A passing finite test suite
does not automatically establish either universal property.

For a pure compositional macro, its mathematical meaning is defined to be its
expansion. This removes a separate informal macro interpretation, but does not
prove that the expander or primitive implementations are correct. The reference
has executable checks and tests, not a mechanized proof.

## Effects and targets

Outside intseq, types should record relevant dimensions, ownership, lifetimes,
resource capabilities, numerical formats, and communication/reduction scopes.
Restrictions prevent a bad behavior only if the checker or construction rule
actually enforces them and the backend preserves that property.

For example, a source-level absence of secret-dependent branches is not by itself
a target-level timing guarantee. Bounded loops are not by themselves a hardware
wall-clock bound. These require separately specified observation models and
backend evidence. Do not turn a syntactic restriction into an unsupported claim.

Approximate numerical lowerings require an explicit relation and composed error
budget; mathematical equality is not a license to reorder floating-point
operations. A backend optimization that cannot discharge its obligations is
excluded or labeled unverified, not silently accepted.

## Prototype boundary

intseq has exact mathematical integer results when evaluation succeeds. The host
may reject a computation that exceeds configured resource bounds. No claim is
made that all mathematically equivalent expressions consume identical resources
or fail at the same point.
