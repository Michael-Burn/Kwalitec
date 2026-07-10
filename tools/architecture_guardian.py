#!/usr/bin/env python3
"""Architecture Guardian — static audit of Kwalitec layering invariants.

Read-only analysis. Complements unit/integration tests; does not replace them.

Usage:
    python tools/architecture_guardian.py
    python tools/architecture_guardian.py --json
    python tools/architecture_guardian.py --root /path/to/kwalitec

Checks (aligned with ARCHITECTURE.md and ADR-001..004):

* Thin routes / route size
* Business logic inside routes
* Direct model access from templates (heuristic)
* Duplicate curriculum traversal
* Service layer violations (Flask request/session)
* Circular imports (import graph)
* Duplicate helper functions (basic)
* Large files
* Missing docstrings (optional warning)
* Missing type hints (optional warning)
* Blueprint separation
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Iterator

# ---------------------------------------------------------------------------
# Thresholds
# ---------------------------------------------------------------------------

ROUTE_WARN_LINES = 40
ROUTE_FAIL_LINES = 80
FILE_WARN_LINES = 500
FILE_FAIL_LINES = 900
DOCSTRING_COVERAGE_WARN = 0.70
TYPEHINT_COVERAGE_WARN = 0.60

EXPECTED_BLUEPRINTS = (
    "auth",
    "dashboard",
    "mission",
    "study_plan",
    "analytics",
    "settings",
)

# Modules allowed to own curriculum ordering / V1-V2 branching.
CANONICAL_TRAVERSAL_OWNERS = frozenset(
    {
        "app/services/curriculum_service.py",
        "app/models/curriculum.py",
    }
)

# Patterns that suggest syllabus-order traversal outside CurriculumService.
TRAVERSAL_PATTERNS = (
    re.compile(r"Topic\.query\.filter_by\([^)]*curriculum_id"),
    re.compile(r"Topic\.query\.filter\([^)]*curriculum_id"),
    re.compile(r"\.order_by\(\s*Topic\.order"),
    re.compile(r"parent_topic_id\s*==\s*None"),
    re.compile(r"parent_topic_id\s+is\s+None"),
    re.compile(r"get_all_topics_ordered\s*\("),
    re.compile(r"def\s+_?(?:walk|traverse|order)_?topics?\b", re.I),
    re.compile(r"def\s+_?(?:get_)?topics?_ordered\b", re.I),
)

# Business-logic smells inside route modules (ORM / domain math — not service calls).
ROUTE_LOGIC_PATTERNS = (
    re.compile(r"\b\w+\.query\."),
    re.compile(r"\bdb\.session\."),
    re.compile(r"\bmastery_score\s*[+\-*/=]"),
    re.compile(r"\bweighted_score\b"),
    re.compile(r"\bpass_risk\s*[+\-*/=]"),
    re.compile(r"\bspaced_repetition\b"),
    re.compile(r"\bimport_curricula\s*\("),
)

SERVICE_FLASK_GLOBALS = frozenset({"request", "session", "g", "current_app"})

TEMPLATE_MODEL_PATTERNS = (
    re.compile(r"\{\{[^}]*\.query\."),
    re.compile(r"\{%[^%]*\.query\."),
    re.compile(r"\{\{[^}]*db\.session"),
    re.compile(r"from\s+app\.models"),
    re.compile(r"import\s+app\.models"),
)

# ---------------------------------------------------------------------------
# Report model
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """A single audit finding."""

    severity: str  # pass | warning | fail
    check: str
    message: str
    location: str = ""


@dataclass
class CheckResult:
    """Aggregated result for one named check."""

    name: str
    status: str  # PASS | WARNING | FAIL
    findings: list[Finding] = field(default_factory=list)
    summary: str = ""


@dataclass
class AuditReport:
    """Full architecture audit report."""

    checks: list[CheckResult] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    def add(self, result: CheckResult) -> None:
        self.checks.append(result)

    @property
    def overall_score(self) -> int:
        """Score 0–100 from check statuses."""
        if not self.checks:
            return 0
        weights = {"PASS": 100, "WARNING": 70, "FAIL": 0}
        total = sum(weights.get(c.status, 0) for c in self.checks)
        return round(total / len(self.checks))


# ---------------------------------------------------------------------------
# Filesystem helpers
# ---------------------------------------------------------------------------


def project_root_from(start: Path | None = None) -> Path:
    """Resolve repository root (directory containing ``app/``)."""
    if start is not None:
        candidate = start.resolve()
        if (candidate / "app").is_dir():
            return candidate
        raise SystemExit(f"No app/ package under {candidate}")

    here = Path(__file__).resolve().parent
    for parent in [here, *here.parents]:
        if (parent / "app").is_dir() and (parent / "ARCHITECTURE.md").exists():
            return parent
    # Fallback: parent of tools/
    return here.parent


def iter_python_files(root: Path, *relative: str) -> Iterator[Path]:
    """Yield ``.py`` files under ``root / relative`` (skip __pycache__)."""
    base = root.joinpath(*relative) if relative else root
    if not base.exists():
        return
    for path in sorted(base.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        yield path


def iter_template_files(root: Path) -> Iterator[Path]:
    """Yield Jinja templates under ``app/templates``."""
    base = root / "app" / "templates"
    if not base.exists():
        return
    for path in sorted(base.rglob("*")):
        if path.suffix in {".html", ".jinja", ".j2"} and path.is_file():
            yield path


def rel(root: Path, path: Path) -> str:
    """Path relative to project root as posix string."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path) -> str:
    """Read file as UTF-8, ignoring undecodable bytes."""
    return path.read_text(encoding="utf-8", errors="replace")


def line_count(path: Path) -> int:
    """Count lines in a text file."""
    return len(read_text(path).splitlines())


def parse_ast(path: Path) -> ast.AST | None:
    """Parse a Python file; return None on syntax errors."""
    try:
        return ast.parse(read_text(path), filename=str(path))
    except SyntaxError:
        return None


# ---------------------------------------------------------------------------
# AST utilities
# ---------------------------------------------------------------------------


def is_route_decorator(node: ast.AST) -> bool:
    """True if decorator looks like a Flask route registration."""
    # @bp.route / @bp.get / @bp.post / @login_required wrapping those
    target = node
    while isinstance(target, ast.Call):
        target = target.func
    if isinstance(target, ast.Attribute):
        return target.attr in {"route", "get", "post", "put", "patch", "delete"}
    if isinstance(target, ast.Name):
        return target.id in {"route", "login_required"}
    return False


def function_has_route_decorator(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if any decorator is a Flask route (possibly under login_required)."""
    for dec in fn.decorator_list:
        if is_route_decorator(dec):
            # login_required alone is not enough — need an actual route
            if isinstance(dec, ast.Name) and dec.id == "login_required":
                continue
            if (
                isinstance(dec, ast.Call)
                and isinstance(dec.func, ast.Name)
                and dec.func.id == "login_required"
            ):
                continue
            return True
        # @bp.route(...) form already handled; also Attribute without Call
        if isinstance(dec, ast.Attribute) and dec.attr in {
            "route",
            "get",
            "post",
            "put",
            "patch",
            "delete",
        }:
            return True
    # Common pattern: @bp.get + @login_required — check any route-like attr
    for dec in fn.decorator_list:
        cur: ast.AST = dec
        while isinstance(cur, ast.Call):
            cur = cur.func
        if isinstance(cur, ast.Attribute) and cur.attr in {
            "route",
            "get",
            "post",
            "put",
            "patch",
            "delete",
        }:
            return True
    return False


def function_span_lines(fn: ast.AST) -> int:
    """Inclusive line span of a function node."""
    end = getattr(fn, "end_lineno", None) or fn.lineno
    return max(1, end - fn.lineno + 1)


def iter_functions(tree: ast.AST) -> Iterator[ast.FunctionDef | ast.AsyncFunctionDef]:
    """Yield top-level and nested function defs."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node


def public_functions(tree: ast.AST) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    """Module-level and class methods that are not private (``_`` prefix)."""
    results: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    for node in tree.body if isinstance(tree, ast.Module) else []:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                results.append(node)
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if item.name.startswith("_") and item.name != "__init__":
                        continue
                    results.append(item)
    return results


def has_docstring(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """True if function has a docstring."""
    return ast.get_docstring(fn) is not None


def typed_params_ratio(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[int, int]:
    """Return (annotated_count, total_annotatable) excluding ``self``/``cls``."""
    args = list(fn.args.args) + list(fn.args.kwonlyargs)
    if fn.args.vararg:
        args.append(fn.args.vararg)  # type: ignore[arg-type]
    if fn.args.kwarg:
        args.append(fn.args.kwarg)  # type: ignore[arg-type]

    total = 0
    annotated = 0
    for arg in args:
        if arg.arg in {"self", "cls"}:
            continue
        total += 1
        if arg.annotation is not None:
            annotated += 1
    # Return annotation counts as one more slot when present
    if total > 0 or fn.returns is not None:
        total += 1
        if fn.returns is not None:
            annotated += 1
    return annotated, total


def imported_names_from_flask(tree: ast.AST) -> set[str]:
    """Names imported from ``flask`` (direct)."""
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module == "flask":
            for alias in node.names:
                names.add(alias.asname or alias.name)
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "flask":
                    names.add(alias.asname or "flask")
    return names


def module_imports(tree: ast.AST) -> set[str]:
    """Absolute ``app.*`` module names imported by this file."""
    mods: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("app"):
            # ImportFrom app.services.x import Y → depend on app.services.x
            mods.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("app"):
                    mods.add(alias.name)
    return mods


def path_to_module(root: Path, path: Path) -> str:
    """Convert ``app/foo/bar.py`` → ``app.foo.bar``."""
    rel_path = path.resolve().relative_to(root.resolve())
    parts = list(rel_path.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def normalize_helper_signature(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    """Fingerprint for duplicate-helper detection; skip tiny stubs."""
    if function_span_lines(fn) < 4:
        return None
    # Body dump without docstring
    body = list(fn.body)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    if not body:
        return None
    try:
        dump = ast.dump(ast.Module(body=body, type_ignores=[]), annotate_fields=False)
    except TypeError:
        dump = ast.dump(ast.Module(body=body, type_ignores=[]))
    # Collapse numeric literals / string constants lightly
    dump = re.sub(r"Constant\([^)]*\)", "Constant(_)", dump)
    return dump


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------


def check_thin_routes(root: Path) -> CheckResult:
    """Flag oversized Flask route handlers."""
    findings: list[Finding] = []
    for path in iter_python_files(root, "app"):
        if path.name != "routes.py":
            continue
        tree = parse_ast(path)
        if tree is None:
            continue
        for fn in iter_functions(tree):
            if not function_has_route_decorator(fn):
                continue
            span = function_span_lines(fn)
            loc = f"{rel(root, path)}:{fn.lineno}"
            if span >= ROUTE_FAIL_LINES:
                findings.append(
                    Finding(
                        "fail",
                        "Thin Routes",
                        f"Route `{fn.name}` is {span} lines (limit {ROUTE_FAIL_LINES})",
                        loc,
                    )
                )
            elif span >= ROUTE_WARN_LINES:
                findings.append(
                    Finding(
                        "warning",
                        "Thin Routes",
                        f"Route `{fn.name}` is {span} lines (warn at {ROUTE_WARN_LINES})",
                        loc,
                    )
                )

    status = _status_from_findings(findings)
    summary = (
        "All route handlers are within size limits."
        if status == "PASS"
        else f"{len(findings)} route size issue(s)."
    )
    return CheckResult("Thin Routes", status, findings, summary)


def check_business_logic_in_routes(root: Path) -> CheckResult:
    """Detect ORM / domain-math smells inside blueprint routes."""
    findings: list[Finding] = []
    for path in iter_python_files(root, "app"):
        if path.name != "routes.py":
            continue
        text = read_text(path)
        lines = text.splitlines()
        # Skip import lines for .query false positives on unused imports? Keep them —
        # imports of models are fine; .query. usage is the smell.
        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("import ") or stripped.startswith("from "):
                continue
            # Service orchestration is the intended route shape — skip those lines.
            if "Service." in stripped or "catalogue." in stripped:
                continue
            for pattern in ROUTE_LOGIC_PATTERNS:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            "warning",
                            "Business Logic in Routes",
                            f"Possible domain logic in route: `{stripped[:100]}`",
                            f"{rel(root, path)}:{i}",
                        )
                    )
                    break

    # Cap noise: collapse to unique locations already; if many, keep all but status WARNING
    # Escalate to FAIL when many distinct files have query usage
    files_with_query = {
        f.location.split(":")[0]
        for f in findings
        if ".query." in f.message or "db.session" in f.message
    }
    status = "PASS"
    if findings:
        status = "FAIL" if len(files_with_query) >= 3 else "WARNING"
    summary = (
        "No ORM/domain-math smells detected in routes."
        if status == "PASS"
        else f"{len(findings)} possible business-logic smell(s) across {len(files_with_query)} route file(s)."
    )
    return CheckResult("Business Logic in Routes", status, findings, summary)


def check_template_model_access(root: Path) -> CheckResult:
    """Heuristic: templates should not call ORM query APIs."""
    findings: list[Finding] = []
    for path in iter_template_files(root):
        text = read_text(path)
        for i, line in enumerate(text.splitlines(), start=1):
            for pattern in TEMPLATE_MODEL_PATTERNS:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            "fail",
                            "Template Model Access",
                            f"Possible direct model/DB access in template: `{line.strip()[:100]}`",
                            f"{rel(root, path)}:{i}",
                        )
                    )
                    break
    status = _status_from_findings(findings)
    summary = (
        "No direct model access detected in templates."
        if status == "PASS"
        else f"{len(findings)} template model-access issue(s)."
    )
    return CheckResult("Template Model Access", status, findings, summary)


def check_canonical_traversal(root: Path) -> CheckResult:
    """Flag duplicate syllabus-order traversal outside CurriculumService."""
    findings: list[Finding] = []
    for path in iter_python_files(root, "app"):
        r = rel(root, path)
        if r in CANONICAL_TRAVERSAL_OWNERS:
            continue
        if r.startswith("app/curriculum/"):
            # Engine package owns in-memory ordering; DB product path is CurriculumService
            continue
        text = read_text(path)
        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            for pattern in TRAVERSAL_PATTERNS:
                if pattern.search(line):
                    # Allow calling CurriculumService.get_all_topics_ordered
                    if "CurriculumService" in line and "get_all_topics_ordered" in line:
                        continue
                    if "CurriculumService" in line and "get_ordered_topics" in line:
                        continue
                    # Calling curriculum.get_all_topics_ordered on ORM model is OK only
                    # inside curriculum_service (already skipped). Elsewhere it's a smell
                    # unless it's clearly delegated.
                    severity = "fail" if "def " in line or "Topic.query" in line else "warning"
                    findings.append(
                        Finding(
                            severity,
                            "Canonical Traversal",
                            f"Possible non-canonical topic traversal: `{stripped[:100]}`",
                            f"{r}:{i}",
                        )
                    )
                    break

    status = _status_from_findings(findings)
    summary = (
        "Topic ordering appears to go through CurriculumService."
        if status == "PASS"
        else f"{len(findings)} possible duplicate traversal signal(s)."
    )
    return CheckResult("Canonical Traversal", status, findings, summary)


def check_service_layer(root: Path) -> CheckResult:
    """Services must not depend on Flask request/session globals."""
    findings: list[Finding] = []
    for path in iter_python_files(root, "app", "services"):
        tree = parse_ast(path)
        if tree is None:
            continue
        flask_names = imported_names_from_flask(tree)
        bad = flask_names & SERVICE_FLASK_GLOBALS
        if bad:
            findings.append(
                Finding(
                    "fail",
                    "Service Layer",
                    f"Service imports Flask globals: {', '.join(sorted(bad))}",
                    rel(root, path),
                )
            )
        # Also scan for attribute access flask.request if imported as flask
        text = read_text(path)
        for i, line in enumerate(text.splitlines(), start=1):
            if re.search(r"\bflask\.(request|session|g)\b", line):
                findings.append(
                    Finding(
                        "fail",
                        "Service Layer",
                        f"Service uses Flask global: `{line.strip()[:100]}`",
                        f"{rel(root, path)}:{i}",
                    )
                )
            if re.search(r"\bfrom flask import[^\n]*\b(request|session)\b", line):
                # Already covered via AST; skip duplicate if present
                pass

    status = _status_from_findings(findings)
    summary = (
        "Services do not import Flask request/session globals."
        if status == "PASS"
        else f"{len(findings)} service-layer violation(s)."
    )
    return CheckResult("Service Layer", status, findings, summary)


def check_circular_imports(root: Path) -> CheckResult:
    """Detect cycles in the ``app.*`` import graph (static)."""
    graph: dict[str, set[str]] = defaultdict(set)
    modules: dict[str, Path] = {}

    for path in iter_python_files(root, "app"):
        mod = path_to_module(root, path)
        modules[mod] = path
        tree = parse_ast(path)
        if tree is None:
            continue
        for dep in module_imports(tree):
            # Normalize: if dep is a package, keep as-is; edges to known modules only
            graph[mod].add(dep)

    # Only keep edges to modules we know (or their parents that exist)
    known = set(modules)
    # Also allow package roots that have __init__
    for mod in list(known):
        parts = mod.split(".")
        for i in range(1, len(parts)):
            known.add(".".join(parts[:i]))

    filtered: dict[str, set[str]] = defaultdict(set)
    for src, deps in graph.items():
        for dep in deps:
            if dep in known and dep != src:
                filtered[src].add(dep)
            else:
                # Try parent packages of dep that are known
                parts = dep.split(".")
                for i in range(len(parts), 0, -1):
                    parent = ".".join(parts[:i])
                    if parent in known and parent != src:
                        filtered[src].add(parent)
                        break

    cycles = _find_cycles(filtered)
    findings: list[Finding] = []
    for cycle in cycles[:20]:
        findings.append(
            Finding(
                "fail",
                "Circular Imports",
                "Cycle: " + " → ".join(cycle),
            )
        )

    status = _status_from_findings(findings)
    summary = (
        "No circular imports detected in the app package graph."
        if status == "PASS"
        else f"{len(cycles)} import cycle(s) detected."
    )
    return CheckResult("Circular Imports", status, findings, summary)


def _find_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    """Tarjan-ish simple cycle enumeration (bounded)."""
    cycles: list[list[str]] = []
    seen_cycle_keys: set[tuple[str, ...]] = set()

    def dfs(node: str, stack: list[str], in_stack: set[str], visiting: set[str]) -> None:
        stack.append(node)
        in_stack.add(node)
        visiting.add(node)
        for nbr in sorted(graph.get(node, ())):
            if nbr in in_stack:
                idx = stack.index(nbr)
                cycle = stack[idx:] + [nbr]
                key = tuple(sorted(cycle[:-1]))
                if key not in seen_cycle_keys and len(cycle) > 2:
                    seen_cycle_keys.add(key)
                    cycles.append(cycle)
            elif nbr not in visiting and len(stack) < 12:
                dfs(nbr, stack, in_stack, visiting)
        stack.pop()
        in_stack.discard(node)

    for start in sorted(graph):
        dfs(start, [], set(), set())
        if len(cycles) >= 20:
            break
    return cycles


def check_duplicate_helpers(root: Path) -> CheckResult:
    """Basic detection of identical helper function bodies."""
    fingerprints: dict[str, list[tuple[str, str, int]]] = defaultdict(list)

    scan_dirs = [
        ("app", "services"),
        ("app", "utils"),
        ("app", "auth"),
        ("app", "dashboard"),
        ("app", "mission"),
        ("app", "study_plan"),
        ("app", "analytics"),
        ("app", "settings"),
    ]
    for parts in scan_dirs:
        base = root.joinpath(*parts)
        if not base.exists():
            continue
        for path in iter_python_files(root, *parts):
            tree = parse_ast(path)
            if tree is None:
                continue
            for fn in iter_functions(tree):
                if not fn.name.startswith("_") and "Service" in (fn.name):
                    continue
                # Focus on helpers (private) and small shared utils
                if not (fn.name.startswith("_") or "util" in rel(root, path)):
                    continue
                fp = normalize_helper_signature(fn)
                if fp is None:
                    continue
                fingerprints[fp].append((rel(root, path), fn.name, fn.lineno))

    findings: list[Finding] = []
    for _fp, locs in fingerprints.items():
        if len(locs) < 2:
            continue
        # Same name preferred signal
        names = {n for _, n, _ in locs}
        desc = ", ".join(f"{p}:{n}" for p, n, _ in locs[:5])
        severity = "warning" if len(names) == 1 or len(locs) == 2 else "fail"
        findings.append(
            Finding(
                severity,
                "Duplicate Helpers",
                f"Similar helper bodies ({len(locs)} copies): {desc}",
            )
        )

    status = _status_from_findings(findings)
    summary = (
        "No duplicate helper bodies detected."
        if status == "PASS"
        else f"{len(findings)} duplicate-helper cluster(s)."
    )
    return CheckResult("Duplicate Helpers", status, findings, summary)


def check_large_files(root: Path) -> CheckResult:
    """Flag oversized Python modules under app/."""
    findings: list[Finding] = []
    for path in iter_python_files(root, "app"):
        n = line_count(path)
        r = rel(root, path)
        if n >= FILE_FAIL_LINES:
            findings.append(
                Finding(
                    "fail",
                    "Large Files",
                    f"{r} has {n} lines (limit {FILE_FAIL_LINES})",
                    r,
                )
            )
        elif n >= FILE_WARN_LINES:
            findings.append(
                Finding(
                    "warning",
                    "Large Files",
                    f"{r} has {n} lines (warn at {FILE_WARN_LINES})",
                    r,
                )
            )
    status = _status_from_findings(findings)
    summary = (
        "No oversized modules under app/."
        if status == "PASS"
        else f"{len(findings)} large-file finding(s)."
    )
    return CheckResult("Large Files", status, findings, summary)


def check_missing_docstrings(root: Path) -> CheckResult:
    """Optional warning: public functions/methods without docstrings."""
    missing = 0
    total = 0
    samples: list[Finding] = []
    for path in iter_python_files(root, "app"):
        tree = parse_ast(path)
        if tree is None:
            continue
        for fn in public_functions(tree):
            total += 1
            if not has_docstring(fn):
                missing += 1
                if len(samples) < 15:
                    samples.append(
                        Finding(
                            "warning",
                            "Missing Docstrings",
                            f"`{fn.name}` has no docstring",
                            f"{rel(root, path)}:{fn.lineno}",
                        )
                    )

    coverage = (total - missing) / total if total else 1.0
    findings = list(samples)
    if coverage < DOCSTRING_COVERAGE_WARN:
        findings.insert(
            0,
            Finding(
                "warning",
                "Missing Docstrings",
                f"Docstring coverage {coverage:.0%} "
                f"({total - missing}/{total}); warn below {DOCSTRING_COVERAGE_WARN:.0%}",
            ),
        )
        status = "WARNING"
    else:
        status = "PASS"
        findings = [
            Finding(
                "pass",
                "Missing Docstrings",
                f"Docstring coverage {coverage:.0%} ({total - missing}/{total})",
            )
        ]
    return CheckResult(
        "Missing Docstrings",
        status,
        findings,
        f"Coverage {coverage:.0%} across {total} public callables.",
    )


def check_missing_type_hints(root: Path) -> CheckResult:
    """Optional warning: public callables with sparse annotations."""
    annotated = 0
    total = 0
    samples: list[Finding] = []
    for path in iter_python_files(root, "app"):
        tree = parse_ast(path)
        if tree is None:
            continue
        for fn in public_functions(tree):
            a, t = typed_params_ratio(fn)
            if t == 0:
                continue
            total += t
            annotated += a
            if a < t and len(samples) < 15:
                samples.append(
                    Finding(
                        "warning",
                        "Missing Type Hints",
                        f"`{fn.name}` annotations {a}/{t}",
                        f"{rel(root, path)}:{fn.lineno}",
                    )
                )

    coverage = annotated / total if total else 1.0
    findings = list(samples)
    if coverage < TYPEHINT_COVERAGE_WARN:
        findings.insert(
            0,
            Finding(
                "warning",
                "Missing Type Hints",
                f"Type-hint coverage {coverage:.0%} "
                f"({annotated}/{total}); warn below {TYPEHINT_COVERAGE_WARN:.0%}",
            ),
        )
        status = "WARNING"
    else:
        status = "PASS"
        findings = [
            Finding(
                "pass",
                "Missing Type Hints",
                f"Type-hint coverage {coverage:.0%} ({annotated}/{total})",
            )
        ]
    return CheckResult(
        "Missing Type Hints",
        status,
        findings,
        f"Coverage {coverage:.0%} across {total} annotatable slots.",
    )


def check_blueprint_separation(root: Path) -> CheckResult:
    """Verify expected feature blueprints exist and are registered."""
    findings: list[Finding] = []
    init_path = root / "app" / "__init__.py"
    init_text = read_text(init_path) if init_path.exists() else ""

    for name in EXPECTED_BLUEPRINTS:
        bp_dir = root / "app" / name
        routes = bp_dir / "routes.py"
        if not bp_dir.is_dir():
            findings.append(
                Finding(
                    "fail",
                    "Blueprint Separation",
                    f"Missing blueprint package app/{name}/",
                )
            )
            continue
        if not routes.exists():
            findings.append(
                Finding(
                    "fail",
                    "Blueprint Separation",
                    f"Missing routes module app/{name}/routes.py",
                )
            )
        # Registration signal
        if f"{name}_bp" not in init_text and f"register_blueprint" in init_text:
            # soft check — name_bp convention
            if not re.search(rf"register_blueprint\(\s*{name}_bp", init_text):
                findings.append(
                    Finding(
                        "warning",
                        "Blueprint Separation",
                        f"Blueprint `{name}_bp` not clearly registered in app/__init__.py",
                    )
                )

    # Ensure create_app remains the factory
    if "def create_app" not in init_text:
        findings.append(
            Finding(
                "fail",
                "Blueprint Separation",
                "create_app() not found in app/__init__.py",
            )
        )

    status = _status_from_findings(findings)
    summary = (
        "Expected blueprints are present and registered."
        if status == "PASS"
        else f"{len(findings)} blueprint separation issue(s)."
    )
    return CheckResult("Blueprint Separation", status, findings, summary)


# ---------------------------------------------------------------------------
# Aggregation / reporting
# ---------------------------------------------------------------------------


def _status_from_findings(findings: Iterable[Finding]) -> str:
    """Derive PASS/WARNING/FAIL from finding severities."""
    sevs = {f.severity for f in findings}
    if "fail" in sevs:
        return "FAIL"
    if "warning" in sevs:
        return "WARNING"
    return "PASS"


def build_recommendations(report: AuditReport) -> list[str]:
    """Human-readable follow-ups from failed/warned checks."""
    recs: list[str] = []
    by_name = {c.name: c for c in report.checks}

    thin = by_name.get("Thin Routes")
    if thin and thin.status != "PASS":
        recs.append(
            "Extract wizard/step helpers from large route handlers into services "
            "so routes stay authenticate → validate → call service → render."
        )

    biz = by_name.get("Business Logic in Routes")
    if biz and biz.status != "PASS":
        recs.append(
            "Move SQLAlchemy queries and domain math out of blueprint routes into "
            "app/services/ (ADR-001)."
        )

    trav = by_name.get("Canonical Traversal")
    if trav and trav.status != "PASS":
        recs.append(
            "Route all syllabus-order walks through CurriculumService.get_all_topics_ordered "
            "(ADR-004); do not reimplement V1/V2 ordering."
        )

    svc = by_name.get("Service Layer")
    if svc and svc.status != "PASS":
        recs.append(
            "Remove flask.request / session / g imports from services; pass explicit arguments."
        )

    circ = by_name.get("Circular Imports")
    if circ and circ.status != "PASS":
        recs.append(
            "Break import cycles with local imports inside functions or by extracting shared types."
        )

    large = by_name.get("Large Files")
    if large and large.status != "PASS":
        recs.append(
            "Split oversized modules by responsibility (e.g. wizard helpers vs plan CRUD)."
        )

    docs = by_name.get("Missing Docstrings")
    if docs and docs.status != "PASS":
        recs.append(
            "Add concise docstrings to public service methods (purpose, Args, Returns)."
        )

    hints = by_name.get("Missing Type Hints")
    if hints and hints.status != "PASS":
        recs.append(
            "Annotate public service APIs with built-in generics (list[str], dict[str, Any])."
        )

    dup = by_name.get("Duplicate Helpers")
    if dup and dup.status != "PASS":
        recs.append(
            "Consolidate duplicated private helpers into a single shared utility or service method."
        )

    tmpl = by_name.get("Template Model Access")
    if tmpl and tmpl.status != "PASS":
        recs.append(
            "Keep ORM access in services; pass plain data into Jinja templates."
        )

    if not recs:
        recs.append(
            "Architecture checks are clean. Keep new features behind services and "
            "CurriculumService traversal helpers."
        )
    return recs


def run_audit(root: Path) -> AuditReport:
    """Execute all architecture checks."""
    report = AuditReport()
    report.add(check_thin_routes(root))
    report.add(check_business_logic_in_routes(root))
    report.add(check_template_model_access(root))
    report.add(check_canonical_traversal(root))
    report.add(check_service_layer(root))
    report.add(check_circular_imports(root))
    report.add(check_duplicate_helpers(root))
    report.add(check_large_files(root))
    report.add(check_missing_docstrings(root))
    report.add(check_missing_type_hints(root))
    report.add(check_blueprint_separation(root))
    report.recommendations = build_recommendations(report)
    return report


def format_report(report: AuditReport) -> str:
    """Render the human-readable Architecture Audit report."""
    lines: list[str] = []
    lines.append("Architecture Audit")
    lines.append("=" * 60)
    lines.append("")

    for check in report.checks:
        lines.append(f"{check.status:8} {check.name}")
        if check.summary:
            lines.append(f"         {check.summary}")
        # Show non-pass findings (cap for readability)
        interesting = [f for f in check.findings if f.severity in {"fail", "warning"}]
        for finding in interesting[:12]:
            loc = f" @ {finding.location}" if finding.location else ""
            lines.append(f"         - [{finding.severity.upper()}] {finding.message}{loc}")
        if len(interesting) > 12:
            lines.append(f"         - … {len(interesting) - 12} more")
        lines.append("")

    lines.append("-" * 60)
    lines.append(f"Overall Score: {report.overall_score}/100")
    lines.append("")
    lines.append("Recommendations")
    lines.append("-" * 60)
    for i, rec in enumerate(report.recommendations, start=1):
        lines.append(f"{i}. {rec}")
    lines.append("")
    return "\n".join(lines)


def report_to_dict(report: AuditReport) -> dict[str, Any]:
    """JSON-serialisable representation."""
    return {
        "overall_score": report.overall_score,
        "checks": [
            {
                "name": c.name,
                "status": c.status,
                "summary": c.summary,
                "findings": [
                    {
                        "severity": f.severity,
                        "message": f.message,
                        "location": f.location,
                    }
                    for f in c.findings
                ],
            }
            for c in report.checks
        ],
        "recommendations": report.recommendations,
    }


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Kwalitec Architecture Guardian — read-only layering audit."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Project root (directory containing app/). Default: auto-detect.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of the text report.",
    )
    args = parser.parse_args(argv)

    root = project_root_from(args.root)
    report = run_audit(root)

    if args.json:
        print(json.dumps(report_to_dict(report), indent=2))
    else:
        print(format_report(report))

    # Exit non-zero only on FAIL (warnings still succeed for CI soft-gate use)
    if any(c.status == "FAIL" for c in report.checks):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
