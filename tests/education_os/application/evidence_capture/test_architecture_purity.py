"""Architecture purity for Learning Evidence Capture (V3-006)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4] / "src" / "application" / "evidence_capture"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
        "celery",
        "redis",
        "boto3",
        "openai",
        "anthropic",
        "pydantic",
        "marshmallow",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "infrastructure.",
    "web.",
    "app.",
    "openai.",
    "anthropic.",
    "domain.",
)

FORBIDDEN_METHOD_NAMES = frozenset(
    {
        "diagnose",
        "calculate_mastery",
        "prioritise",
        "prioritize",
        "choose_strategy",
        "select_strategy",
        "interpret_evidence",
        "create_hypothesis",
        "generate_mission",
        "generate_recommendations",
        "rewrite_mission",
        "change_recommendation",
        "mutate_recommendation",
        "orchestrate",
        "persist",
        "save",
        "commit",
    }
)

EXPECTED_FILES = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "learning_session_outcome.py",
    PACKAGE_ROOT / "evidence_capture_service.py",
    PACKAGE_ROOT / "captured_evidence.py",
    PACKAGE_ROOT / "evidence_mapper.py",
}

ALLOWED_PRESENTATION_IMPORTS = frozenset(
    {
        "presentation.study_session.session_view_model",
        "presentation.reflection.reflection_view_model",
    }
)

ALLOWED_SESSION_RUNTIME_IMPORT = "application.session_runtime.session_state"


def _iter_python_files() -> list[Path]:
    return sorted(PACKAGE_ROOT.rglob("*.py"))


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def _defined_methods(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    }


def test_package_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    for path in EXPECTED_FILES:
        assert path.is_file(), f"missing {path.name}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_forbidden_imports(path: Path) -> None:
    imported = _imported_modules(path)
    for name in imported:
        assert name not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
        assert not any(
            name == prefix.rstrip(".") or name.startswith(prefix)
            for prefix in FORBIDDEN_PREFIXES
        ), f"{path.name} imports forbidden module {name}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_persistence_or_ai_code(path: Path) -> None:
    source = path.read_text(encoding="utf-8").lower()
    for fragment in (
        "create_engine",
        "sessionmaker",
        "sqlite3.connect",
        "psycopg",
        "openai",
        "anthropic",
        ".commit(",
        "session.add",
        "datetime.now",
        "time.time",
    ):
        assert fragment not in source, f"{path.name} contains {fragment}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_educational_intelligence_methods(path: Path) -> None:
    methods = _defined_methods(path)
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in methods, f"{path.name} defines {forbidden}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_modules_use_future_annotations(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    if not source.strip():
        return
    assert "from __future__ import annotations" in source


def test_only_allowed_presentation_and_runtime_imports() -> None:
    """Capture may read view models / SessionState; not engines or UI kits."""
    for path in _iter_python_files():
        for name in _imported_modules(path):
            if name == "presentation" or name.startswith("presentation."):
                assert name in ALLOWED_PRESENTATION_IMPORTS, (
                    f"{path.name} imports {name}; only "
                    f"{sorted(ALLOWED_PRESENTATION_IMPORTS)} are allowed"
                )
            if name.startswith("application.session_runtime"):
                assert name == ALLOWED_SESSION_RUNTIME_IMPORT, (
                    f"{path.name} imports {name}; only "
                    f"{ALLOWED_SESSION_RUNTIME_IMPORT} is allowed"
                )


def test_no_engine_or_pipeline_authority() -> None:
    sources = [
        path.read_text(encoding="utf-8") for path in _iter_python_files()
    ]
    for source in sources:
        assert "MissionGenerator" not in source
        assert "StudyPlanner" not in source
        assert "ProgressEvaluator" not in source
        assert "RecommendationGenerator" not in source
        assert "EducationalPipeline" not in source
        assert "ExperienceGenerator" not in source
        assert "SessionRuntime(" not in source


def test_public_exports() -> None:
    from application.evidence_capture import (
        CapturedEvidence,
        CompletionStatus,
        EvidenceCaptureService,
        EvidenceMapper,
        LearningSessionOutcome,
    )

    assert EvidenceCaptureService is not None
    assert EvidenceMapper is not None
    assert LearningSessionOutcome is not None
    assert CapturedEvidence is not None
    assert CompletionStatus is not None
