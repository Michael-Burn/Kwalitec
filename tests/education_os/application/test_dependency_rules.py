"""Dependency direction tests: Application → Domain; never reverse or infra."""

from __future__ import annotations

import ast
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[3] / "src" / "application"
DOMAIN_ROOT = Path(__file__).resolve().parents[3] / "src" / "domain"
PORTS_ROOT = PACKAGE_ROOT / "ports"


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


def test_application_may_import_domain() -> None:
    found_domain = False
    for path in PACKAGE_ROOT.rglob("*.py"):
        for name in _imported_modules(path):
            if name.startswith("domain."):
                found_domain = True
    assert found_domain, "application layer should depend on domain"


def test_application_does_not_import_infrastructure_package() -> None:
    """Business application code must not import infrastructure.

    The composition root is the sole exception: it may construct and inject
    infrastructure adapters (ENG-004 / APP-001).
    """
    for path in PACKAGE_ROOT.rglob("*.py"):
        if "composition" in path.relative_to(PACKAGE_ROOT).parts:
            continue
        for name in _imported_modules(path):
            assert not name.startswith("infrastructure"), (
                f"{path.name} imports infrastructure ({name})"
            )
            assert not name.startswith("app."), f"{path.name} imports app ({name})"


def test_domain_does_not_import_application() -> None:
    for path in DOMAIN_ROOT.rglob("*.py"):
        for name in _imported_modules(path):
            assert not name.startswith("application"), (
                f"domain {path.relative_to(DOMAIN_ROOT)} imports application ({name})"
            )


def test_ports_contain_abstract_repositories_only() -> None:
    source = (PORTS_ROOT / "repositories.py").read_text(encoding="utf-8")
    assert "ABC" in source
    assert "abstractmethod" in source
    for name in (
        "DigitalTwinRepository",
        "LearningEpisodeRepository",
        "EvidenceRepository",
        "SubjectKnowledgeRepository",
        "TeachingPlanRepository",
        "DiagnosisRepository",
        "HypothesisRepository",
        "PriorityRepository",
        "TeachingIntentionRepository",
        "TeachingStrategyRepository",
        "DecisionRepository",
        "OrchestratorRepository",
    ):
        assert f"class {name}" in source
    assert "sqlite" not in source.lower()
    assert "sqlalchemy" not in source.lower()
    assert "flask" not in source.lower()


def test_ports_contain_infrastructure_interfaces() -> None:
    for module_name, class_name in (
        ("unit_of_work.py", "UnitOfWork"),
        ("clock.py", "Clock"),
        ("uuid_generator.py", "UUIDGenerator"),
        ("transaction_manager.py", "TransactionManager"),
    ):
        source = (PORTS_ROOT / module_name).read_text(encoding="utf-8")
        assert "ABC" in source
        assert "abstractmethod" in source
        assert f"class {class_name}" in source
        assert "sqlalchemy" not in source.lower()
        assert "flask" not in source.lower()
        assert "psycopg" not in source.lower()


def test_ports_have_no_concrete_persistence() -> None:
    for path in PORTS_ROOT.rglob("*.py"):
        source = path.read_text(encoding="utf-8").lower()
        for fragment in (
            "create_engine",
            "sessionmaker",
            "sqlite3",
            "psycopg",
            "postgresql",
            "flask",
            "sqlalchemy",
        ):
            assert fragment not in source, f"{path.name} contains {fragment}"
