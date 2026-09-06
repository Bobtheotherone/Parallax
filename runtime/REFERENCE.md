# Embedded intseq reference: executable compatibility model

This document contains the frozen source-archive implementation of `intseq/0.1`.
Its Python fence is a compatibility artifact, not a packaged runtime, task oracle,
or security boundary. The normative operation semantics and artifact formats remain
[PACK](../packs/intseq/PACK.md) and [CAPSULE](../packs/intseq/CAPSULE.md); when prose
and executable behavior appear to disagree, preserve the smallest reproducer and
resolve the conflict explicitly rather than silently redefining either side.

The Python fence is intentionally byte-stable. `ARL` wording and the
`arl-capsule/0.1` / `arl-program/0.1` identifiers are preserved compatibility
history. [SPEC-001](../docs/specs/001-intseq-reference.md) defines the extraction
work needed to turn this reference into ordinary package code.

## Compatibility surface worth understanding

| Area | Reference behavior that affects implementations |
|---|---|
| Documents | UTF-8 Markdown, at most 65,536 bytes, exactly one lowercase `json` fence; surrounding prose has no authority |
| JSON | Duplicate keys and `NaN`/`Infinity` are rejected; booleans/floats are not integers |
| Capsule | Exact v0.1 keys, one input `x:VecInt`, selected primitive allowlist, at most 16 macros, 1–8 parameters each |
| Macro body | Typed lexical expression over the macro's parameters and selected **primitives only**; no macro-to-macro body calls |
| Program | Exact v0.1 keys; canonical capsule SHA-256 must match before checking/expansion |
| Expansion | Hygienic lexical substitution; program-level macro calls may nest; expanded primitive IR is re-typechecked |
| Evaluation | Eager left-to-right argument evaluation; exact integers; sequence operations preserve order; `seq.sum` checks each left-to-right intermediate |
| Resource policy | depth 32, nodes 4,096, vector length 4,096, magnitude 256 bits, work 250,000; rejection point is observable compatibility behavior |
| CLI success | `EVALUATED` plus value/IR/hashes and `task_correctness: NOT_CHECKED` |
| CLI handled failure | exit 2, empty stdout, JSON `REJECTED` detail on stderr; argparse usage errors remain argparse errors |
| Self-test | Public same-project checks using Python `assert`; never run it with `-O`/`PYTHONOPTIMIZE` when characterizing compatibility |

Two details are easy to accidentally “improve” into incompatibility. First,
resource equivalence is not mathematical equivalence: evaluation order and
intermediate magnitude/work checks matter. Second, the checker is deliberately not
a task oracle: the bundled wrong-order program can typecheck and execute while the
separate direct-loop task oracle rejects its result.

## Engineering use

Use this source as an executable behavioral model when implementing or refactoring
the intseq runtime. Characterize observable boundaries instead of mechanically
copying internal structure. High-value comparisons include rejection **codes**,
canonical hashes, exact expanded IR, lexical macro scope, intermediate overflow,
near-limit resource cases, CLI exits/streams, and the typed-but-task-wrong example.

Do not infer properties it does not establish. The reference has no model host,
process sandbox, task-domain enforcement, final oracle custody, native/GPU backend,
formal proof, or performance guarantee. Its direct-loop self-test oracle has a
different implementation path from the AST evaluator but the same project
authorship and fully public inputs.

## Frozen reference source

```python
"""ARL intseq/0.1: data-only capsule validator, macro expander and interpreter.

This is a small research reference implementation, not a proof checker, native
compiler, general sandbox, LLM client, or task-correctness oracle.
Python 3.11+; standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import re
import sys
from typing import Any

MAX_BYTES = 65_536
MAX_DEPTH = 32
MAX_NODES = 4_096
MAX_VECTOR = 4_096
MAX_BITS = 256
MAX_WORK = 250_000
SIG = {
    "seq.add": (("VecInt", "Int"), "VecInt"),
    "seq.mul": (("VecInt", "Int"), "VecInt"),
    "seq.filter_ge": (("VecInt", "Int"), "VecInt"),
    "seq.sum": (("VecInt",), "Int"),
    "seq.count": (("VecInt",), "Int"),
    "int.add": (("Int", "Int"), "Int"),
    "int.mul": (("Int", "Int"), "Int"),
}
NAME = re.compile(r"[a-z][a-z0-9_]{0,31}\Z")

class Rejection(ValueError):
    def __init__(self, code: str, detail: str):
        self.code = code
        super().__init__(f"{code}: {detail}")

def require(ok: bool, code: str, detail: str) -> None:
    if not ok:
        raise Rejection(code, detail)

def fields(obj: Any, names: set[str], where: str) -> None:
    require(type(obj) is dict and set(obj) == names, "SCHEMA", where)

def checked_int(value: Any) -> int:
    require(type(value) is int, "TYPE", "expected an integer, not bool/float")
    require(value.bit_length() <= MAX_BITS, "RESOURCE_LIMIT", "integer bit budget")
    return value

def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("utf-8")

def digest(obj: Any) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()

def strict_json(text: str) -> Any:
    require(len(text.encode("utf-8")) <= MAX_BYTES, "RESOURCE_LIMIT", "JSON bytes")
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in items:
            require(key not in out, "SCHEMA", f"duplicate key {key}")
            out[key] = value
        return out
    def constant(value: str) -> Any:
        raise Rejection("SCHEMA", f"non-JSON constant {value}")
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except (json.JSONDecodeError, RecursionError, ValueError) as exc:
        if isinstance(exc, Rejection):
            raise
        raise Rejection("SCHEMA", "invalid or too deeply nested JSON") from exc

def read_document(path: str | Path) -> Any:
    p = Path(path)
    require(p.stat().st_size <= MAX_BYTES, "RESOURCE_LIMIT", "document bytes")
    text = p.read_text(encoding="utf-8")
    blocks = re.findall(r"^```json[ \t]*\n(.*?)^```[ \t]*$", text,
                        re.MULTILINE | re.DOTALL)
    require(len(blocks) == 1, "SCHEMA", "expected exactly one json fence")
    return strict_json(blocks[0])

def infer(expr: Any, env: dict[str, str], signatures: dict,
          depth: int = 0, budget: list[int] | None = None) -> str:
    if budget is None:
        budget = [0]
    budget[0] += 1
    require(depth <= MAX_DEPTH and budget[0] <= MAX_NODES,
            "RESOURCE_LIMIT", "expression depth/nodes")
    if type(expr) is int:
        checked_int(expr)
        return "Int"
    if type(expr) is str:
        require(expr in env, "TYPE", f"unbound variable {expr}")
        return env[expr]
    require(type(expr) is list and len(expr) >= 1 and type(expr[0]) is str,
            "SCHEMA", "expected an expression array")
    op = expr[0]
    require(op in signatures, "OP_NOT_ALLOWED", op)
    args, result = signatures[op]
    require(len(expr) - 1 == len(args), "TYPE", f"arity of {op}")
    for child, expected in zip(expr[1:], args):
        require(infer(child, env, signatures, depth + 1, budget) == expected,
                "TYPE", f"argument of {op} must be {expected}")
    return result

def validate_capsule(cap: Any) -> tuple[dict, dict[str, dict]]:
    fields(cap, {"protocol", "pack", "input", "output", "primitives", "macros"},
           "capsule keys")
    require(cap["protocol"] == "arl-capsule/0.1" and cap["pack"] == "intseq/0.1",
            "VERSION", "unsupported protocol/pack")
    require(cap["input"] == {"x": "VecInt"}, "TYPE", "one VecInt input x required")
    require(cap["output"] in ("Int", "VecInt"), "TYPE", "output type")
    ops = cap["primitives"]
    require(type(ops) is list and 1 <= len(ops) <= len(SIG)
            and all(type(op) is str and op in SIG for op in ops),
            "OP_NOT_ALLOWED", "primitive allowlist")
    require(len(set(ops)) == len(ops), "SCHEMA", "duplicate primitive")
    signatures = {op: SIG[op] for op in ops}
    macros = cap["macros"]
    require(type(macros) is list and len(macros) <= 16, "SCHEMA", "macro count")
    definitions: dict[str, dict] = {}
    for macro in macros:
        fields(macro, {"name", "params", "returns", "body"}, "macro keys")
        name = macro["name"]
        require(type(name) is str and NAME.fullmatch(name) is not None,
                "SCHEMA", "macro name")
        key = "macro." + name
        require(key not in definitions, "SCHEMA", "duplicate macro name")
        params = macro["params"]
        require(type(params) is list and 1 <= len(params) <= 8,
                "SCHEMA", "macro parameters")
        env: dict[str, str] = {}
        for pair in params:
            require(type(pair) is list and len(pair) == 2, "SCHEMA", "parameter pair")
            var, typ = pair
            require(type(var) is str and NAME.fullmatch(var) is not None
                    and var not in env, "SCHEMA", "parameter name")
            require(typ in ("Int", "VecInt"), "TYPE", "parameter type")
            env[var] = typ
        require(macro["returns"] in ("Int", "VecInt"), "TYPE", "macro result type")
        # Bodies may call allowlisted primitives only: no macro recursion or chaining.
        require(infer(macro["body"], env, signatures) == macro["returns"],
                "TYPE", "macro result mismatch")
        definitions[key] = macro
    # Delayed update keeps every body restricted to primitives.
    for key, macro in definitions.items():
        signatures[key] = (tuple(p[1] for p in macro["params"]), macro["returns"])
    return signatures, definitions

def expand(expr: Any, definitions: dict[str, dict]) -> Any:
    budget = [0]
    def walk(node: Any, env: dict[str, Any], depth: int) -> Any:
        budget[0] += 1
        require(depth <= MAX_DEPTH and budget[0] <= MAX_NODES,
                "RESOURCE_LIMIT", "macro expansion depth/nodes")
        if type(node) is str:
            # The actual argument is already in the caller's scope. Substitution
            # must not apply the callee's environment recursively to that argument.
            return walk(env[node], {}, depth + 1) if node in env else node
        if type(node) is int:
            return node
        op = node[0]
        args = [walk(arg, env, depth + 1) for arg in node[1:]]
        if op in definitions:
            macro = definitions[op]
            actuals = dict(zip((p[0] for p in macro["params"]), args))
            return walk(macro["body"], actuals, depth + 1)
        return [op, *args]
    return walk(expr, {}, 0)

def check_program(cap: Any, prog: Any) -> Any:
    signatures, definitions = validate_capsule(cap)
    fields(prog, {"protocol", "capsule_sha256", "expr"}, "program keys")
    require(prog["protocol"] == "arl-program/0.1", "VERSION", "program version")
    require(prog["capsule_sha256"] == digest(cap), "HASH_MISMATCH", "capsule changed")
    require(infer(prog["expr"], {"x": "VecInt"}, signatures) == cap["output"],
            "TYPE", "program result type")
    lowered = expand(prog["expr"], definitions)
    primitive_sigs = {op: SIG[op] for op in cap["primitives"]}
    require(infer(lowered, {"x": "VecInt"}, primitive_sigs) == cap["output"],
            "TYPE", "expanded result type")
    return lowered

def evaluate(cap: Any, prog: Any, x: Any) -> tuple[Any, Any]:
    lowered = check_program(cap, prog)
    require(type(x) is list and len(x) <= MAX_VECTOR,
            "RESOURCE_LIMIT", "input must be a bounded list")
    for value in x:
        checked_int(value)
    work = [0]
    def run(expr: Any) -> Any:
        work[0] += 1
        require(work[0] <= MAX_WORK, "RESOURCE_LIMIT", "work budget")
        if type(expr) is int:
            return expr
        if type(expr) is str:
            return x
        op = expr[0]
        args = [run(arg) for arg in expr[1:]]
        if op.startswith("seq."):
            v = args[0]
            work[0] += len(v)
            require(work[0] <= MAX_WORK, "RESOURCE_LIMIT", "element work budget")
            if op == "seq.add":
                return [checked_int(item + args[1]) for item in v]
            if op == "seq.mul":
                return [checked_int(item * args[1]) for item in v]
            if op == "seq.filter_ge":
                return [item for item in v if item >= args[1]]
            if op == "seq.count":
                return checked_int(len(v))
            total = 0
            for item in v:
                total = checked_int(total + item)
            return total
        if op == "int.add":
            return checked_int(args[0] + args[1])
        return checked_int(args[0] * args[1])
    return run(lowered), lowered

def sample_capsule() -> dict:
    return {
        "protocol": "arl-capsule/0.1", "pack": "intseq/0.1",
        "input": {"x": "VecInt"}, "output": "Int",
        "primitives": ["seq.filter_ge", "seq.mul", "seq.add", "seq.sum"],
        "macros": [{"name": "affine", "params": [["v", "VecInt"], ["a", "Int"], ["b", "Int"]],
                    "returns": "VecInt", "body": ["seq.add", ["seq.mul", "v", "a"], "b"]}],
    }

def program(cap: dict, expr: Any) -> dict:
    return {"protocol": "arl-program/0.1", "capsule_sha256": digest(cap), "expr": expr}

def oracle(x: list[int]) -> int:
    # Independent hand-written task oracle; does not inspect capsules or ASTs.
    result = 0
    for item in x:
        if item >= 0:
            result += 3 * item + 5
    return result

def selftest() -> dict:
    cap = sample_capsule()
    good = program(cap, ["seq.sum", ["macro.affine", ["seq.filter_ge", "x", 0], 3, 5]])
    counts = {"exhaustive_task_inputs": 0, "random_task_inputs": 0,
              "primitive_differential_checks": 0, "rejection_checks": 0,
              "macro_scope_checks": 0}
    for n in range(5):
        for values in itertools.product(range(-3, 4), repeat=n):
            x = list(values)
            assert evaluate(cap, good, x)[0] == oracle(x)
            counts["exhaustive_task_inputs"] += 1
    rng = random.Random(20260905)
    for _ in range(1000):
        x = [rng.randint(-10**6, 10**6) for _ in range(rng.randint(0, 64))]
        assert evaluate(cap, good, x)[0] == oracle(x)
        counts["random_task_inputs"] += 1
    full = {"protocol": "arl-capsule/0.1", "pack": "intseq/0.1",
            "input": {"x": "VecInt"}, "output": "Int", "primitives": list(SIG), "macros": []}
    for _ in range(100):
        x = [rng.randint(-100, 100) for _ in range(rng.randint(0, 20))]
        a, b = rng.randint(-10, 10), rng.randint(-10, 10)
        cases = [(["seq.add", "x", a], [v+a for v in x], "VecInt"),
                 (["seq.mul", "x", a], [v*a for v in x], "VecInt"),
                 (["seq.filter_ge", "x", a], [v for v in x if v >= a], "VecInt"),
                 (["seq.sum", "x"], sum(x), "Int"),
                 (["seq.count", "x"], len(x), "Int"),
                 (["int.add", a, b], a+b, "Int"),
                 (["int.mul", a, b], a*b, "Int")]
        for expr, expected, result_type in cases:
            c = {**full, "output": result_type}
            assert evaluate(c, program(c, expr), x)[0] == expected
            counts["primitive_differential_checks"] += 1
    def reject(thunk, code: str) -> None:
        try:
            thunk()
        except Rejection as exc:
            assert exc.code == code, (exc.code, code)
            counts["rejection_checks"] += 1
        else:
            raise AssertionError("expected rejection " + code)
    reject(lambda: evaluate(cap, {**good, "capsule_sha256": "0"*64}, []), "HASH_MISMATCH")
    reject(lambda: evaluate(cap, program(cap, ["seq.sum", 3]), []), "TYPE")
    reject(lambda: evaluate(cap, program(cap, ["seq.count", "x"]), []), "OP_NOT_ALLOWED")
    reject(lambda: evaluate(cap, program(cap, ["seq.sum", "x", 1]), []), "TYPE")
    reject(lambda: evaluate(cap, program(cap, ["seq.sum", "y"]), []), "TYPE")
    reject(lambda: evaluate(cap, program(cap, True), []), "SCHEMA")
    reject(lambda: evaluate(cap, good, [True]), "TYPE")
    reject(lambda: evaluate(cap, good, [1.5]), "TYPE")
    reject(lambda: evaluate(cap, good, [0]*(MAX_VECTOR+1)), "RESOURCE_LIMIT")
    reject(lambda: evaluate(cap, good, [1 << MAX_BITS]), "RESOURCE_LIMIT")
    reject(lambda: evaluate(cap, program(cap, ["seq.sum", ["seq.mul", "x", 2]]), [1 << 255]), "RESOURCE_LIMIT")
    reject(lambda: validate_capsule({**cap, "permissions": ["network"]}), "SCHEMA")
    bad_macro = {**cap["macros"][0], "body": ["macro.affine", "v", "a", "b"]}
    reject(lambda: validate_capsule({**cap, "macros": [bad_macro]}), "OP_NOT_ALLOWED")
    reject(lambda: validate_capsule({**cap, "primitives": cap["primitives"]*2}), "OP_NOT_ALLOWED")
    reject(lambda: strict_json('{"a":1,"a":2}'), "SCHEMA")
    reject(lambda: strict_json('{"a":NaN}'), "SCHEMA")
    nested: Any = "x"
    for _ in range(MAX_DEPTH + 1):
        nested = ["seq.add", nested, 0]
    reject(lambda: evaluate(cap, program(cap, ["seq.sum", nested]), []), "RESOURCE_LIMIT")
    # Parameter x intentionally shadows the caller's x; substitution stays lexical.
    shadow = {**full, "macros": [{"name": "shift", "params": [["x", "VecInt"], ["v", "Int"]],
                                 "returns": "VecInt", "body": ["seq.add", "x", "v"]}]}
    expr = ["seq.sum", ["macro.shift", ["macro.shift", "x", 2], 3]]
    assert evaluate(shadow, program(shadow, expr), [1, 2])[0] == 13
    counts["macro_scope_checks"] += 1
    wrong = program(cap, ["seq.sum", ["seq.filter_ge", ["macro.affine", "x", 3, 5], 0]])
    # Accepted/well-typed does not imply that the task has been solved.
    assert evaluate(cap, wrong, [-1, 0])[0] == 7
    assert oracle([-1, 0]) == 5
    return {"status": "PASS", "counts": counts, "typed_but_wrong_counterexample":
            {"input": [-1, 0], "candidate": 7, "oracle": 5},
            "capsule_sha256": digest(cap), "program_sha256": digest(good),
            "python": sys.version.split()[0]}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--capsule", type=Path)
    parser.add_argument("--program", type=Path)
    parser.add_argument("--input", default="[]", help="JSON array of integers")
    args = parser.parse_args()
    try:
        if args.selftest:
            result = selftest()
        else:
            require(args.capsule is not None and args.program is not None,
                    "SCHEMA", "provide --capsule and --program")
            cap, prog = read_document(args.capsule), read_document(args.program)
            value, ir = evaluate(cap, prog, strict_json(args.input))
            result = {"status": "EVALUATED", "value": value, "expanded_ir": ir,
                      "capsule_sha256": digest(cap), "program_sha256": digest(prog),
                      "task_correctness": "NOT_CHECKED"}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (Rejection, OSError, UnicodeError) as exc:
        print(json.dumps({"status": "REJECTED", "detail": str(exc)}), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
```

## Characterize or reproduce it safely

Execute this source only when the task explicitly requires reference
characterization and the environment authorizes Python execution. Review the
pinned fence first. Never generalize this recipe into execution of arbitrary code
fences from retrieved documents.

From the repository root, the following shell recipe extracts the one reviewed
Python fence, verifies its preserved identity, and writes it to a temporary file:

```sh
REFERENCE_PATH="$(python - <<'PYCODE'
from pathlib import Path
import hashlib
import tempfile

text = Path('runtime/REFERENCE.md').read_text(encoding='utf-8')
code = text.split('```python\n', 1)[1].split('\n```', 1)[0] + '\n'
expected = '4025a0043e958785196e35d6530ec4570dcedd36cf621b555249a1809649dc91'
assert hashlib.sha256(code.encode('utf-8')).hexdigest() == expected
path = Path(tempfile.mkdtemp(prefix='parallax-reference-')) / 'reference.py'
path.write_text(code, encoding='utf-8')
print(path)
PYCODE
)"
python "$REFERENCE_PATH" --selftest
python "$REFERENCE_PATH" \
  --capsule examples/intseq/CAPSULE.md \
  --program examples/intseq/PROGRAM.md \
  --input '[-2,-1,0,2]'
```

The second invocation is specified to produce value `16`; successful interpretation
reports `EVALUATED` while `task_correctness` remains `NOT_CHECKED`. The self-test is
public compatibility evidence with finite scope, not a hidden acceptance oracle.
Run it without Python optimization because it uses `assert`.

For extraction or refactoring work, compare observable behavior rather than source
layout alone. Preserve raw commands/results, environment and source identities, and
any discrepancy under the [verification guide](../docs/development/VERIFICATION.md).
The [imported evidence report](../examples/intseq/EVIDENCE.md) is historical; a new
implementation needs fresh evidence rather than inheriting its `PASS` values.
