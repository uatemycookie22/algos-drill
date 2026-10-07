#!/usr/bin/env python3
"""Archive current solution and reset functions back to raise _TODO.

Usage:
    python3 reset.py                     # archive + reset ALL implemented functions
    python3 reset.py binary_search bfs   # archive + reset specific functions only
"""
import ast
import sys
import shutil
from datetime import date
from pathlib import Path

SOLUTION = Path("drills/solution.py")
SOLUTIONS_DIR = Path("solutions")

TODO = "raise _TODO"


def archive():
    SOLUTIONS_DIR.mkdir(exist_ok=True)
    dest = SOLUTIONS_DIR / f"{date.today()}.py"
    if dest.exists():
        suffix = 2
        while (candidate := SOLUTIONS_DIR / f"{date.today()}-{suffix}.py").exists():
            suffix += 1
        dest = candidate
    shutil.copy(SOLUTION, dest)
    print(f"archived → {dest}")


def get_ranges(source: str) -> list[tuple[str, int, int, int]]:
    """Return [(name, def_lineno, body_start, body_end)] for all defs."""
    tree = ast.parse(source)
    results = []

    def visit(node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            start = body[0].lineno
            # skip docstring
            if (isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                start = body[1].lineno if len(body) > 1 else node.end_lineno
            results.append((node.name, node.lineno, start, node.end_lineno))
        for child in ast.iter_child_nodes(node):
            visit(child)

    visit(tree)
    return results


def is_already_todo(lines: list[str], start: int, end: int) -> bool:
    body = [l.strip() for l in lines[start - 1:end] if l.strip()]
    return body == [TODO]


def reset_functions(names: list[str] | None):
    # Re-parse each time so line numbers stay accurate after each replacement
    changed = 0
    skipped = 0

    while True:
        source = SOLUTION.read_text()
        lines = source.splitlines(keepends=True)
        ranges = get_ranges(source)

        # Filter to targets
        if names:
            targets = [r for r in ranges if r[0] in names]
        else:
            targets = ranges

        # Find the first function that still needs resetting (top-down)
        to_reset = None
        for name, def_line, start, end in targets:
            if not is_already_todo(lines, start, end):
                to_reset = (name, start, end)
                break

        if to_reset is None:
            break

        name, start, end = to_reset
        first_body_line = lines[start - 1]
        indent = len(first_body_line) - len(first_body_line.lstrip())
        todo_line = " " * indent + TODO + "\n"

        lines[start - 1:end] = [todo_line]
        SOLUTION.write_text("".join(lines))
        print(f"  reset: {name}")
        changed += 1

    # Report skipped
    source = SOLUTION.read_text()
    for name, _, start, end in get_ranges(source):
        if names and name not in names:
            continue
        if is_already_todo(source.splitlines(keepends=True), start, end):
            pass  # already done or was already blank

    if names:
        already_blank = [n for n in names if n not in [r[0] for r in get_ranges(source)]]
        for n in already_blank:
            print(f"  warning: '{n}' not found")

    print(f"\n{changed} function(s) reset.")


def clear_progress(names: list[str] | None):
    progress_file = Path(".drill_progress.json")
    if not progress_file.exists():
        return
    if names is None:
        progress_file.unlink()
        print("cleared progress tracking")
    else:
        data = json.loads(progress_file.read_text())
        for n in names:
            data.pop(n, None)
        progress_file.write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    import json
    args = sys.argv[1:]
    archive()
    reset_functions(args if args else None)
    clear_progress(args if args else None)
