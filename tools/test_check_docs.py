"""Regression tests for documentation tooling only; no Parallax runtime execution."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentationCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="parallax-doccheck-")
        self.root = Path(self.temporary.name) / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_checker(self) -> tuple[int, dict]:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools/check_docs.py"), "--root", str(self.root)],
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(completed.stderr, "", completed.stderr)
        return completed.returncode, json.loads(completed.stdout)

    def append(self, path: str, text: str) -> None:
        file = self.root / path
        file.write_text(file.read_text(encoding="utf-8") + text, encoding="utf-8")

    def rejects(self, fragment: str) -> None:
        code, report = self.run_checker()
        self.assertEqual(code, 1, report)
        self.assertEqual(report["status"], "FAIL", report)
        self.assertTrue(any(fragment in error for error in report["errors"]), report)
        self.assertEqual(report["runtime_execution_by_this_check"], "NOT_RUN")

    def test_clean_documentation(self) -> None:
        code, report = self.run_checker()
        self.assertEqual(code, 0, report)
        self.assertEqual(report["status"], "PASS")
        self.assertFalse(report["semantic_correctness_assessed"])

    def test_missing_local_link(self) -> None:
        self.append("README.md", "\n[missing](does-not-exist.md)\n")
        self.rejects("missing/outside-root link")

    def test_frozen_pack_drift(self) -> None:
        self.append("packs/intseq/PACK.md", "\nUnapproved semantic revision.\n")
        self.rejects("frozen v0.1 file changed")

    def test_changed_reference_fence(self) -> None:
        file = self.root / "runtime/REFERENCE.md"
        file.write_text(file.read_text().replace("MAX_WORK = 250_000", "MAX_WORK = 250_001"))
        self.rejects("frozen reference Python fence changed")

    def test_invalid_spec_state(self) -> None:
        file = self.root / "docs/specs/001-intseq-reference.md"
        file.write_text(file.read_text().replace("status: ready-for-dev", "status: almost-ready"))
        self.rejects("invalid/duplicate spec identity or status")

    def test_unclosed_fence(self) -> None:
        self.append("README.md", "\n```text\nunfinished\n")
        self.rejects("unclosed Markdown fence")

    def test_missing_source_map_entry(self) -> None:
        file = self.root / "docs/provenance/source-inventory.json"
        inventory = json.loads(file.read_text())
        inventory["sources"] = [row for row in inventory["sources"] if row["source_path"] != "README.md"]
        file.write_text(json.dumps(inventory))
        self.rejects("source-map coverage differs")


if __name__ == "__main__":
    unittest.main()
