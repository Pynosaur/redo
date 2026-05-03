#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: @spacemany2k38
# 2026-05-03

"""Core runner: execute a command repeatedly with timing and summary."""

import subprocess
import signal
import sys
import time


def run(command, times, interval, stop_on_fail, quiet, listen=False):
    """Execute *command* up to *times* times (0 = infinite).

    Returns exit code 0 if all runs succeeded, 1 otherwise.
    """
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    infinite = times == 0
    results = []       # list of (index, ok, elapsed, returncode)
    total_start = time.monotonic()
    i = 0

    while True:
        i += 1
        if not infinite and i > times:
            break

        t0 = time.monotonic()
        try:
            proc = subprocess.run(
                command,
                shell=True,
            )
            rc = proc.returncode
        except Exception as e:
            label = f"[{i}]" if infinite else f"[{i}/{times}]"
            _eprint(f"{label} error: {e}")
            rc = 1

        elapsed = time.monotonic() - t0
        ok = rc == 0
        results.append((i, ok, elapsed, rc))

        if not quiet:
            label = f"[{i}]" if infinite else f"[{i}/{times}]"
            mark = "\033[32m✓\033[0m" if ok else "\033[31m✗\033[0m"
            rc_info = "" if ok else f" (exit {rc})"
            print(f"{label} {mark} {elapsed:.3f}s{rc_info}")

        if stop_on_fail and not ok:
            if not quiet:
                _eprint(f"Stopped: command failed on run {i}")
            break

        # In listen mode, wait for Enter or q
        if listen:
            at_limit = not infinite and i >= times
            if not at_limit:
                try:
                    line = input()
                except EOFError:
                    break
                if line.strip().lower() == "q":
                    break
        else:
            # Sleep between runs (not after the last one)
            at_end = not infinite and i >= times
            if interval > 0 and not at_end:
                time.sleep(interval)

    total_elapsed = time.monotonic() - total_start
    _print_summary(results, times, total_elapsed)

    failed = sum(1 for _, ok, _, _ in results if not ok)
    return 1 if failed else 0


def _print_summary(results, total_requested, total_elapsed):
    """Print a one-line summary to stderr."""
    passed = sum(1 for _, ok, _, _ in results if ok)
    failed = len(results) - passed
    ran = len(results)
    times_list = [e for _, _, e, _ in results]
    avg = sum(times_list) / len(times_list) if times_list else 0

    parts = []
    if failed:
        if total_requested == 0:
            parts.append(f"\033[32m{passed}\033[0m/\033[31m{ran}\033[0m executed")
        else:
            parts.append(f"\033[32m{passed}\033[0m/\033[31m{ran}\033[0m executed")
    else:
        parts.append(f"\033[32m{ran}\033[0m executed")

    parts.append(f"total {_fmt(total_elapsed)}")
    parts.append(f"avg {_fmt(avg)}")

    if len(times_list) > 1:
        parts.append(f"min {_fmt(min(times_list))}")
        parts.append(f"max {_fmt(max(times_list))}")

    sys.stderr.write(f"\n{'  │  '.join(parts)}\n")


def _fmt(seconds):
    """Format seconds to a human-readable string."""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    if seconds < 60:
        return f"{seconds:.3f}s"
    m, s = divmod(seconds, 60)
    return f"{int(m)}m{s:.1f}s"


def _eprint(msg):
    sys.stderr.write(msg + "\n")
