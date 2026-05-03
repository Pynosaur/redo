#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2026-05-03

import sys
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    __package__ = "app"

from app import __version__
from app.core.runner import run
from app.utils.doc_reader import read_app_doc


def print_help():
    doc = read_app_doc('redo')

    desc = doc.get('description', 'Repeat a command with timing summary')
    usage = doc.get('usage', ["redo 'command' -t N [-i S] [-s] [-q]"])
    options = doc.get('options', [])
    examples = doc.get('examples', [])

    print(f"redo - {desc}")
    print("\nUSAGE:")
    for u in usage:
        print(f"    {u}")

    if options:
        print("\nOPTIONS:")
        for opt in options:
            print(f"    {opt}")

    if examples:
        print("\nEXAMPLES:")
        for ex in examples:
            print(f"    {ex}")


def print_version():
    doc = read_app_doc('redo')
    print(doc.get('version', __version__))


def main():
    args = sys.argv[1:]

    if not args:
        print_help()
        return 0

    if args[0] in ("-h", "--help", "help"):
        print_help()
        return 0

    if args[0] in ("-v", "--version"):
        print_version()
        return 0

    # Parse freely-ordered flags and the quoted command
    command = None
    times = 1
    interval = 0.0
    stop_on_fail = False
    quiet = False

    i = 0
    while i < len(args):
        a = args[i]

        if a == "-t":
            i += 1
            if i >= len(args):
                _die("-t requires a number")
            try:
                times = int(args[i])
            except ValueError:
                _die(f"invalid count: {args[i]}")
            if times < 1:
                _die("count must be at least 1")

        elif a == "-i":
            i += 1
            if i >= len(args):
                _die("-i requires a number (seconds)")
            try:
                interval = float(args[i])
            except ValueError:
                _die(f"invalid interval: {args[i]}")
            if interval < 0:
                _die("interval must be non-negative")

        elif a == "-s":
            stop_on_fail = True

        elif a == "-q":
            quiet = True

        elif a.startswith("-"):
            _die(f"unknown option: {a}")

        else:
            if command is not None:
                _die("only one command allowed (use quotes around it)")
            command = a

        i += 1

    if command is None:
        _die("no command specified")

    return run(command, times, interval, stop_on_fail, quiet)


def _die(msg):
    print(f"redo: {msg}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
