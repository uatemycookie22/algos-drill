"""Makes the repo root importable and tracks drill timing/attempts."""
import os
import sys
import json
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

# ---------------------------------------------------------------------------
# Drill tracker
# ---------------------------------------------------------------------------
# Stored in .drill_progress.json:
# {
#   "binary_search": {
#     "started_at": 1720000000.0,   # unix timestamp of first non-TODO run
#     "attempts": 3,                # total pytest runs that included this function
#     "first_pass_at": 1720000120.0 # unix timestamp when all tests for it passed
#     "elapsed_seconds": 120.0      # time from start to first full pass
#   }
# }

PROGRESS_FILE = Path(__file__).parent / ".drill_progress.json"
SOLUTION_FILE = Path(__file__).parent / "drills" / "solution.py"
TODO_MARKER = "raise _TODO"

# Map test node ids to function names: "TestBinarySearch" → "binary_search"
# Derived from test class names by stripping "Test" and converting to snake_case
import re

def _class_to_func(class_name: str) -> str:
    name = class_name.removeprefix("Test")
    # CamelCase → snake_case
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def _load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text())
        except Exception:
            return {}
    return {}


def _save_progress(data: dict):
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def _is_todo(func_name: str) -> bool:
    """Return True if the function in solution.py body is just raise _TODO."""
    try:
        import ast
        src = SOLUTION_FILE.read_text()
        tree = ast.parse(src)
        lines = src.splitlines()

        def visit(node):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name == func_name:
                    body = node.body
                    # skip docstring
                    stmts = body
                    if (isinstance(body[0], ast.Expr)
                            and isinstance(body[0].value, ast.Constant)
                            and isinstance(body[0].value.value, str)):
                        stmts = body[1:]
                    if not stmts:
                        return True
                    # check if only statement is raise _TODO
                    if len(stmts) == 1 and isinstance(stmts[0], ast.Raise):
                        raise_src = lines[stmts[0].lineno - 1].strip()
                        return "raise _TODO" in raise_src
                    return False
            for child in ast.iter_child_nodes(node):
                result = visit(child)
                if result is not None:
                    return result
            return None

        result = visit(tree)
        return result if result is not None else False
    except Exception:
        return False


def _active_functions() -> set[str]:
    """Return set of function names that are NOT raise _TODO."""
    try:
        import ast
        src = SOLUTION_FILE.read_text()
        tree = ast.parse(src)
        active = set()

        def visit(node):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not _is_todo(node.name):
                    active.add(node.name)
            for child in ast.iter_child_nodes(node):
                visit(child)

        visit(tree)
        return active
    except Exception:
        return set()


# ---------------------------------------------------------------------------
# pytest hooks
# ---------------------------------------------------------------------------

_session_start: float = 0.0
_session_results: dict[str, list[bool]] = {}  # func_name → [passed, passed, ...]


def pytest_sessionstart(session):
    global _session_start
    _session_start = time.time()


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    # Extract class name from node id: drills/test_searching.py::TestBinarySearch::test_found_middle
    parts = report.nodeid.split("::")
    if len(parts) < 2:
        return
    class_name = parts[1] if len(parts) >= 3 else ""
    if not class_name.startswith("Test"):
        return
    func_name = _class_to_func(class_name)
    passed = report.outcome == "passed"
    _session_results.setdefault(func_name, []).append(passed)


def pytest_sessionfinish(session, exitstatus):
    if not _session_results:
        return

    now = time.time()
    progress = _load_progress()
    active = _active_functions()
    changed = False

    for func_name, results in _session_results.items():
        if _is_todo(func_name):
            continue  # still blank, don't track yet

        entry = progress.setdefault(func_name, {})

        # Record first attempt timestamp
        if "started_at" not in entry:
            entry["started_at"] = now
            entry["attempts"] = 0
            changed = True

        # Count this run as an attempt
        entry["attempts"] = entry.get("attempts", 0) + 1
        changed = True

        # Record first full pass
        all_passed = all(results)
        if all_passed and "first_pass_at" not in entry:
            entry["first_pass_at"] = now
            entry["elapsed_seconds"] = round(now - entry["started_at"], 1)
            changed = True

    if changed:
        _save_progress(progress)
        _print_summary(progress)


def _fmt_time(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.0f}s"
    m, s = divmod(int(seconds), 60)
    if m < 60:
        return f"{m}m{s:02d}s"
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m"


def _print_summary(progress: dict):
    # Only print for functions that have activity this session
    active_this_session = set(_session_results.keys())
    relevant = {k: v for k, v in progress.items() if k in active_this_session and not _is_todo(k)}
    if not relevant:
        return

    print("\n\033[1m── drill progress ──────────────────────────────────\033[0m")
    for func, entry in sorted(relevant.items()):
        attempts = entry.get("attempts", 1)
        elapsed = entry.get("elapsed_seconds")
        passed = "first_pass_at" in entry

        status = "\033[32m✓\033[0m" if passed else "\033[33m…\033[0m"
        time_str = f"  {_fmt_time(elapsed)}" if elapsed else ""
        attempt_str = f"  {attempts} attempt{'s' if attempts != 1 else ''}"
        print(f"  {status}  {func:<35}{attempt_str}{time_str}")
    print("\033[1m────────────────────────────────────────────────────\033[0m")
