#!/usr/bin/env python3
"""Check Parallax documentation integrity without executing reference software.

Python 3.11+, standard library only. This is documentation tooling, not a runtime
or a semantic verifier. It checks live Markdown routes, source-archive provenance,
selected executable/canonical semantic identities, packet bindings, and simple spec
metadata. External URLs are not network-checked. Malformed Markdown test fixtures
and run logs are not live docs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from zipfile import BadZipFile, ZipFile

LIVE_DIRS = ("core", "docs", "examples", "packs", "research", "roles", "runtime", "templates")
STATES = {"draft", "ready-for-dev", "in-progress", "in-review", "done", "blocked"}
READY_SECTIONS = (
    "Intent", "Required context", "Invariants", "Non-goals",
    "Interfaces and observable behavior", "File map", "Implementation tasks",
    "Acceptance criteria", "Verification plan", "Readiness and history",
)
INTSEQ_SIGNATURES = {
    "seq.add": "VecInt, Int -> VecInt",
    "seq.mul": "VecInt, Int -> VecInt",
    "seq.filter_ge": "VecInt, Int -> VecInt",
    "seq.sum": "VecInt -> Int",
    "seq.count": "VecInt -> Int",
    "int.add": "Int, Int -> Int",
    "int.mul": "Int, Int -> Int",
}
LINK = re.compile(r"(?<!!)\[[^\]\n]+\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)")
IMAGE = re.compile(r"!\[[^\]\n]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unfenced(text: str) -> str:
    """Drop fenced code, which contains illustrative paths rather than routes."""
    output: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            value = marker.group(1)
            if fence is None:
                fence = value
            elif value[0] == fence[0] and len(value) >= len(fence):
                fence = None
            continue
        if fence is None:
            output.append(line)
    if fence is not None:
        raise ValueError("unclosed Markdown fence")
    return "\n".join(output)


def heading_ids(text: str) -> set[str]:
    counts: dict[str, int] = {}
    result: set[str] = set()
    for line in unfenced(text).splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)(?:\s+#+)?$", line)
        if not match:
            continue
        heading = re.sub(r"<[^>]*>", "", match.group(1)).lower()
        slug = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
        index = counts.get(slug, 0)
        counts[slug] = index + 1
        result.add(f"{slug}-{index}" if index else slug)
    return result


def one_fence(text: str, language: str) -> str:
    blocks = re.findall(r"^```" + re.escape(language) + r"[ \t]*\n(.*?)^```[ \t]*$",
                        text, re.MULTILINE | re.DOTALL)
    if len(blocks) != 1:
        raise ValueError(f"expected one {language} fence, found {len(blocks)}")
    return blocks[0]


def canonical_identity(obj: object) -> str:
    data = json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("utf-8")
    return sha256(data)


def check(root: Path) -> dict[str, object]:
    errors: list[str] = []
    paths = set(root.glob("*.md"))
    for directory in LIVE_DIRS:
        paths.update((root / directory).rglob("*.md"))
    text_by_path = {p: p.read_text(encoding="utf-8") for p in sorted(paths)}

    links = 0
    for source, text in text_by_path.items():
        label = source.relative_to(root).as_posix()
        try:
            prose = unfenced(text)
        except ValueError as exc:
            errors.append(f"{label}: {exc}")
            continue
        for expression in (LINK, IMAGE):
            for match in expression.finditer(prose):
                target = urlsplit(match.group(1).strip("<>"))
                if target.scheme or target.netloc:
                    continue
                links += 1
                path = (source.parent / unquote(target.path)).resolve() if target.path else source
                if not path.is_relative_to(root) or not path.exists():
                    errors.append(f"{label}: missing/outside-root link {match.group(1)}")
                elif target.fragment and path.suffix == ".md":
                    target_text = text_by_path.get(path) or path.read_text(encoding="utf-8")
                    if unquote(target.fragment) not in heading_ids(target_text):
                        errors.append(f"{label}: missing heading {match.group(1)}")

    inventory_path = root / "docs/provenance/source-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    archive = root / inventory["archive"]["path"]
    if sha256(archive.read_bytes()) != inventory["archive"]["sha256"]:
        errors.append("original archive SHA-256 mismatch")
    rows = inventory["sources"]
    originals = {row["source_path"]: row for row in rows}
    if len(originals) != len(rows):
        errors.append("duplicate input source-map entries")
    prefix = inventory["archive"]["source_prefix"]
    manifest_count = 0
    with ZipFile(archive) as source_zip:
        archived = {name[len(prefix):] for name in source_zip.namelist()
                    if name.startswith(prefix) and name.endswith(".md")}
        if archived != set(originals) or len(archived) != inventory["markdown_count"]:
            errors.append("source-map coverage differs from archive Markdown corpus")
        for name, row in originals.items():
            data = source_zip.read(prefix + name)
            if len(data) != row["bytes"] or sha256(data) != row["sha256"]:
                errors.append(f"original source identity mismatch: {name}")
            if not row["disposition"] or not row["targets"]:
                errors.append(f"missing migration disposition/target: {name}")
            for target in row["targets"]:
                destination = (root / target).resolve()
                if not destination.is_relative_to(root) or not destination.exists():
                    errors.append(f"missing migration target: {name} -> {target}")
        manifest = source_zip.read(prefix + "MANIFEST.md").decode("utf-8")
        entries = re.findall(r"^\| \[([^\]]+)\]\([^)]*\) \| (\d+) \| `([a-f0-9]{64})` \|$",
                             manifest, re.MULTILINE)
        manifest_count = len(entries)
        if manifest_count != len(archived) - 1:
            errors.append("original manifest entry count mismatch")
        for name, size, identity in entries:
            data = source_zip.read(prefix + name)
            if len(data) != int(size) or sha256(data) != identity:
                errors.append(f"original manifest mismatch: {name}")

    # Compatibility is pinned at executable/machine-readable boundaries, not by
    # requiring explanatory Markdown wrappers to remain byte-identical forever.
    reference_text = (root / "runtime/REFERENCE.md").read_text(encoding="utf-8")
    code = one_fence(reference_text, "python")
    reference_identity = sha256(code.encode("utf-8"))
    if reference_identity != inventory["reference_python_fence_sha256"]:
        errors.append("frozen reference Python fence changed")

    objects: dict[str, object] = {}
    for name, identity in inventory["canonical_json"].items():
        obj = json.loads(one_fence((root / name).read_text(encoding="utf-8"), "json"))
        objects[name] = obj
        if canonical_identity(obj) != identity:
            errors.append(f"canonical JSON identity changed: {name}")

    capsule = objects["examples/intseq/CAPSULE.md"]
    program = objects["examples/intseq/PROGRAM.md"]
    capsule_identity = inventory["canonical_json"]["examples/intseq/CAPSULE.md"]
    if capsule.get("protocol") != "arl-capsule/0.1" or capsule.get("pack") != "intseq/0.1":
        errors.append("canonical example capsule protocol/pack changed")
    if program.get("protocol") != "arl-program/0.1":
        errors.append("canonical example program protocol changed")
    if program.get("capsule_sha256") != capsule_identity:
        errors.append("example program capsule binding mismatch")

    # The live semantic-pack prose may improve, but its stable operation surface and
    # signatures must stay synchronized with the preserved v0.1 executable model.
    pack_text = (root / "packs/intseq/PACK.md").read_text(encoding="utf-8")
    table_rows = dict(re.findall(r"^\| `([^`]+)` \| `([^`]+)` \|", pack_text, re.MULTILINE))
    if table_rows != INTSEQ_SIGNATURES:
        errors.append("intseq operation table changed or is incomplete")

    format_text = (root / "packs/intseq/CAPSULE.md").read_text(encoding="utf-8")
    for marker in ("intseq/0.1", "arl-capsule/0.1", "arl-program/0.1"):
        if marker not in format_text:
            errors.append(f"intseq format document missing stable identifier: {marker}")

    # Packets bind executable meaning, not recursively fragile whole-Markdown bytes.
    packet_path = root / "examples/intseq/PACKET.md"
    packet = packet_path.read_text(encoding="utf-8")
    packet_capsule = json.loads(one_fence(packet, "json"))
    if canonical_identity(packet_capsule) != capsule_identity:
        errors.append("programmer packet embedded capsule identity mismatch")

    task = json.loads(one_fence((root / "examples/intseq/TASK.md").read_text(encoding="utf-8"), "json"))
    expected_bindings = {
        "task_id": task.get("task_id"),
        "contract_version": task.get("contract_version"),
        "pack": "intseq/0.1",
        "capsule_protocol": "arl-capsule/0.1",
        "program_protocol": "arl-program/0.1",
        "capsule_canonical_json_sha256": capsule_identity,
        "reference_python_fence_sha256": inventory["reference_python_fence_sha256"],
    }
    packet_bindings = dict(re.findall(r"^- `([^`]+)`: `([^`]+)`$", packet, re.MULTILINE))
    if packet_bindings != expected_bindings:
        errors.append("programmer packet semantic bindings changed, stale, or incomplete")

    ready: list[str] = []
    spec_ids: set[str] = set()
    for spec in sorted((root / "docs/specs").glob("*.md")):
        text = spec.read_text(encoding="utf-8")
        front = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        if not front:
            errors.append(f"{spec.name}: missing spec frontmatter")
            continue
        # Check only the documented simple scalar fields, not general YAML.
        fields = dict(re.findall(r"^([a-z_]+):[ \t]*(.*)$", front.group(1), re.MULTILINE))
        status, identity = fields.get("status"), fields.get("id")
        if status not in STATES or not identity or identity in spec_ids or not fields.get("spec_version"):
            errors.append(f"{spec.name}: invalid/duplicate spec identity or status")
        if identity:
            spec_ids.add(identity)
        if status == "ready-for-dev":
            ready.append(spec.relative_to(root).as_posix())
            for heading in READY_SECTIONS:
                section = re.search(r"^## " + re.escape(heading) + r"\n(.*?)(?=^## |\Z)",
                                    text, re.MULTILINE | re.DOTALL)
                if not section or not section.group(1).strip():
                    errors.append(f"{spec.name}: missing ready section {heading}")
            if not re.search(r"^\| AC\d+ \|", text, re.MULTILINE):
                errors.append(f"{spec.name}: no acceptance identifiers")

    return {
        "check_kind": "documentation-integrity",
        "status": "FAIL" if errors else "PASS",
        "markdown_files": len(paths),
        "local_links_checked": links,
        "source_markdown_files": len(originals),
        "original_manifest_entries": manifest_count,
        "canonical_json_identities": len(objects),
        "intseq_operation_signatures": len(table_rows),
        "packet_semantic_bindings": len(packet_bindings),
        "ready_specs": ready,
        "runtime_execution_by_this_check": "NOT_RUN",
        "semantic_correctness_assessed": False,
        "external_urls_checked": False,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        result = check(args.root.resolve())
    except (OSError, ValueError, KeyError, TypeError, BadZipFile) as exc:
        result = {
            "check_kind": "documentation-integrity",
            "status": "FAIL",
            "errors": [str(exc)],
            "runtime_execution_by_this_check": "NOT_RUN",
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
