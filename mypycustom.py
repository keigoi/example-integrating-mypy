"""Copied from https://github.com/python/mypy/blob/2d70ac0/mypy/main.py"""

from __future__ import annotations

import mypy.main

import os
import sys
import time
from typing import TextIO
from typing_extensions import Final

from mypy import util
from mypy.fscache import FileSystemCache

from typing import TextIO

orig_stat: Final = os.stat
MEM_PROFILE: Final = False  # If True, dump memory profile

def main(
    args: list[str] | None = None
) -> mypy.build.BuildResult | None:
    stdout: TextIO = sys.stdout
    stderr: TextIO = sys.stderr
    
    util.check_python_version("mypy")
    t0 = time.time()
    # To log stat() calls: os.stat = stat_proxy
    sys.setrecursionlimit(2**14)
    if args is None:
        args = sys.argv[1:]

    fscache = FileSystemCache()
    sources, options = mypy.main.process_options(args, stdout=stdout, stderr=stderr, fscache=fscache)

    # AST を保存
    options.preserve_asts = True

    formatter = util.FancyFormatter(stdout, stderr, options.hide_error_codes)

    if options.install_types and (stdout is not sys.stdout or stderr is not sys.stderr):
        # Since --install-types performs user input, we want regular stdout and stderr.
        mypy.main.fail("error: --install-types not supported in this mode of running mypy", stderr, options)

    if options.non_interactive and not options.install_types:
        mypy.main.fail("error: --non-interactive is only supported with --install-types", stderr, options)

    if options.install_types and not options.incremental:
        mypy.main.fail(
            "error: --install-types not supported with incremental mode disabled", stderr, options
        )

    if options.install_types and options.python_executable is None:
        mypy.main.fail(
            "error: --install-types not supported without python executable or site packages",
            stderr,
            options,
        )

    if options.install_types and not sources:
        mypy.main.install_types(formatter, options, non_interactive=options.non_interactive)
        return None

    res, messages, blockers = mypy.main.run_build(sources, options, fscache, t0, stdout, stderr)

    code = 0
    n_errors, n_notes, n_files = util.count_stats(messages)
    if messages and n_notes < len(messages):
        code = 2 if blockers else 1
    if options.error_summary:
        if n_errors:
            summary = formatter.format_error(
                n_errors, n_files, len(sources), blockers=blockers, use_color=options.color_output
            )
            stdout.write(summary + "\n")
        # Only notes should also output success
        elif not messages or n_notes == len(messages):
            stdout.write(formatter.format_success(len(sources), options.color_output) + "\n")
        stdout.flush()

    if options.install_types and not options.non_interactive:
        result = mypy.main.install_types(formatter, options, after_run=True, non_interactive=False)
        if result:
            print()
            print("note: Run mypy again for up-to-date results with installed types")
            code = 2

    if code:
        return None
    else:
        return res
