"""Executable boundary checks: subprocess status, diagnostics, image bytes, atomic output."""
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from parallax_raytracer.image import write_png


class CLITests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, "-m", "parallax_raytracer", *args],
                              capture_output=True, text=True, timeout=30)

    def test_help_and_invalid_arguments(self):
        help_result = self.run_cli("--help")
        self.assertEqual(help_result.returncode, 0)
        self.assertIn("--max-depth", help_result.stdout)
        self.assertEqual(help_result.stderr, "")
        for arguments in (("--width", "0"), ("--samples", "no"), ("--samples", "0"),
                          ("--max-depth", "-1"), ("--exposure", "nan"), ("--output", "bad.jpg")):
            result = self.run_cli(*arguments)
            self.assertEqual(result.returncode, 2, result)
            self.assertIn("error:", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_cli_creates_requested_png_and_repeats_exactly(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "new" / "showcase.png"
            args = ("--output", str(path), "--width", "31", "--height", "19", "--samples", "3",
                    "--max-depth", "4", "--seed", "42", "--quiet")
            result = self.run_cli(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            data = path.read_bytes()
            self.assertGreater(len(data), 100)
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack(">II", data[16:24]), (31, 19))
            result = self.run_cli(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(path.read_bytes(), data)

    def test_image_failure_preserves_destination_and_removes_temporary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "keep.png"
            path.write_bytes(b"original")
            with patch("PIL.Image.Image.save", side_effect=OSError("synthetic encoder failure")):
                with self.assertRaises(OSError):
                    write_png(path, 1, 1, b"\x00\x00\x00")
            self.assertEqual(path.read_bytes(), b"original")
            self.assertEqual(list(Path(directory).iterdir()), [path])
            with self.assertRaises(ValueError):
                write_png(path, 2, 2, b"abc")


if __name__ == "__main__":
    unittest.main()
