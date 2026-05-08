#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2026-05-03

import re
import unittest
import sys
from pathlib import Path
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import __version__

REPO_ROOT = Path(__file__).resolve().parent.parent

from app.core.runner import run, _fmt


class TestFmt(unittest.TestCase):
    def test_milliseconds(self):
        self.assertEqual(_fmt(0.045), "45ms")

    def test_seconds(self):
        self.assertEqual(_fmt(5.123), "5.123s")

    def test_minutes(self):
        self.assertEqual(_fmt(125.5), "2m5.5s")


class TestRun(unittest.TestCase):
    def test_success(self):
        rc = run("true", 3, 0, False, False)
        self.assertEqual(rc, 0)

    def test_failure(self):
        rc = run("false", 3, 0, False, False)
        self.assertEqual(rc, 1)

    def test_stop_on_fail(self):
        # Should stop after first failure
        rc = run("false", 5, 0, True, False)
        self.assertEqual(rc, 1)

    def test_quiet_no_stdout(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            run("true", 3, 0, False, True)
            self.assertEqual(mock_out.getvalue(), "")

    def test_single_run(self):
        rc = run("echo hello", 1, 0, False, True)
        self.assertEqual(rc, 0)


class TestMainHelp(unittest.TestCase):
    def test_help_flag(self):
        from app.main import main
        with patch('sys.argv', ['redo', '-h']):
            rc = main()
            self.assertEqual(rc, 0)

    def test_no_args(self):
        from app.main import main
        with patch('sys.argv', ['redo']):
            rc = main()
            self.assertEqual(rc, 0)


class TestVersionConsistency(unittest.TestCase):
    """All version references must match. CI catches drift."""

    def _read_program_version(self):
        text = (REPO_ROOT / ".program").read_text()
        for line in text.splitlines():
            if line.startswith("version:"):
                return line.split(":", 1)[1].strip()
        self.fail(".program has no version field")

    def _read_doc_version(self):
        doc_file = REPO_ROOT / "doc" / "redo.yaml"
        text = doc_file.read_text()
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.upper().startswith("VERSION:"):
                val = stripped.split(":", 1)[1].strip()
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                return val
        self.fail("doc/redo.yaml has no VERSION field")

    def _read_readme_version(self):
        readme = REPO_ROOT / "README.md"
        if not readme.exists():
            return None
        text = readme.read_text()
        match = re.search(r'^Version:\s*(.+)$', text, re.MULTILINE)
        return match.group(1).strip() if match else None

    def test_all_versions_match(self):
        program_v = self._read_program_version()
        doc_v = self._read_doc_version()
        readme_v = self._read_readme_version()
        init_v = __version__

        self.assertEqual(
            init_v, program_v,
            f"__init__.py ({init_v}) != .program ({program_v})",
        )
        self.assertEqual(
            init_v, doc_v,
            f"__init__.py ({init_v}) != doc yaml ({doc_v})",
        )
        if readme_v is not None:
            self.assertEqual(
                init_v, readme_v,
                f"__init__.py ({init_v}) != README.md ({readme_v})",
            )


if __name__ == "__main__":
    unittest.main()
