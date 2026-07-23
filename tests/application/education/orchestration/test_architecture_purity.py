"""Architecture purity for Educational Orchestration (EDU-003.6)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "application"
    / "education"
    / "orchestration"
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
        "numpy",
        "scipy",
        "sklearn",
        "random",
        "uuid",
        "logging",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "infrastructure.",
    "web.",
    "app.",
    "presentation.",
    "openai.",
    "anthropic.",
)

# Educational reasoning must stay in domain engines — not here.
FORBIDDEN_METHOD_NAMES = frozenset(
    {
        "estimate_mastery_score",
        "calculate_mastery",
        "compute_mastery",
        "score_mastery",
        "rank_recommendations",
        "prioritise_recommendations",
        "prioritize_recommendations",
        "select_recommendation",
        "diagnose",
        "choose_strategy",
        "generate_mission",
        "invoke_ai",
        "call_llm",
    }
)

ALLOWED_DOMAIN_PREFIXES = (
    "domain.education.student_state",
    "domain.education.educational_evidence",
    "domain.education.knowledge_graph",
    "domain.education.mastery_estimation",
    "domain.education.recommendation_engine",
    "domain.education.foundation",
)

EXPECTED_LAYOUT = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "educational_orchestrator.py",
    PACKAGE_ROOT / "result_composer.py",
    PACKAGE_ROOT / "stages.py",
    PACKAGE_ROOT / "dto" / "__init__.py",
    PACKAGE_ROOT / "dto" / "educational_decision.py",
    PACKAGE_ROOT / "dto" / "educational_evaluation.py",
    PACKAGE_ROOT / "dto" / "evaluation_summary.py",
    PACKAGE_ROOT / "dto" / "evaluation_snapshot.py",
    PACKAGE_ROOT / "dto" / "interaction_requests.py",
    PACKAGE_ROOT / "ports" / "__init__.py",
    PACKAGE_ROOT / "ports" / "student_state_provider.py",
    PACKAGE_ROOT / "ports" / "evidence_provider.py",
    PACKAGE_ROOT / "ports" / "knowledge_graph_provider.py",
    PACKAGE_ROOT / "ports" / "assessment_publisher.py",
    PACKAGE_ROOT / "ports" / "recommendation_publisher.py",
}


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
    for path in EXPECTED_LAYOUT:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT.parent)}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_forbidden_imports(path: Path) -> None:
    for module in _imported_modules(path):
        root = module.split(".", 1)[0]
        assert root not in FORBIDDEN_MODULES and module not in FORBIDDEN_MODULES, (
            f"{path.name} imports forbidden module {module}"
        )
        for prefix in FORBIDDEN_PREFIXES:
            assert not module.startswith(prefix), (
                f"{path.name} imports forbidden prefix {module}"
            )


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_domain_imports_are_education_os_only(path: Path) -> None:
    for module in _imported_modules(path):
        if not module.startswith("domain."):
            continue
        if module.startswith("domain.education."):
            allowed = any(
                module == prefix or module.startswith(prefix + ".")
                for prefix in ALLOWED_DOMAIN_PREFIXES
            )
            assert allowed, (
                f"{path.name} imports disallowed domain module {module}"
            )
            continue
        pytest.fail(f"{path.name} imports non-education domain module {module}")


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_forbidden_reasoning_methods(path: Path) -> None:
    methods = _defined_methods(path)
    forbidden = methods & FORBIDDEN_METHOD_NAMES
    assert forbidden == set(), f"{path.name} defines forbidden methods {forbidden}"


def test_ports_are_abstract_only() -> None:
    ports_root = PACKAGE_ROOT / "ports"
    for path in ports_root.glob("*.py"):
        if path.name == "__init__.py":
            continue
        source = path.read_text(encoding="utf-8")
        assert "ABC" in source
        assert "abstractmethod" in source
        assert "from sqlalchemy" not in source
        assert "import sqlalchemy" not in source
        assert "Session(" not in source


def test_orchestrator_exports() -> None:
    from application.education.orchestration import (
        EducationalDecision,
        EducationalEvaluation,
        EducationalOrchestrator,
        EvaluationSnapshot,
        EvaluationSummary,
        EvidenceProvider,
        KnowledgeGraphProvider,
        StudentStateProvider,
    )

    assert EducationalOrchestrator is not None
    assert EducationalEvaluation is not None
    assert EducationalDecision is not None
    assert EvaluationSummary is not None
    assert EvaluationSnapshot is not None
    assert StudentStateProvider is not None
    assert EvidenceProvider is not None
    assert KnowledgeGraphProvider is not None


def test_no_datetime_now_or_uuid4() -> None:
    for path in _iter_python_files():
        source = path.read_text(encoding="utf-8")
        assert "datetime.now" not in source
        assert "uuid4" not in source
        assert "time.time" not in source
