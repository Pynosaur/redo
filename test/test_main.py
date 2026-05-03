#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2026-05-03

import unittest
import sys
from pathlib import Path
from unittest.mock import patch
from io import StringIO

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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


if __name__ == "__main__":
    unittest.main()
