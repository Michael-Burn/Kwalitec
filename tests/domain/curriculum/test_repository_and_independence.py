"""Repository contract and framework-independence tests (V2-004)."""

from __future__ import annotations

import ast
from abc import ABC
from pathlib import Path

import pytest

from app.domain.curriculum import (
    Curriculum,
    CurriculumGraph,
    CurriculumId,
    CurriculumNavigationService,
    CurriculumRepository,
    DependencyType,
    GraphBuilder,
    GraphNode,
    GraphValidationResult,
    PrerequisiteService,
    RevisionPathService,
    TopicDifficulty,
    TopicId,
    TopicStatus,
)
from tests.domain.curriculum.helpers import linear_curriculum, make_curriculum

DOMAIN_ROOT = Path(__file__).resolve().parents[3] / "app" / "domain" / "curriculum"
FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "sqlalchemy",
        "wtforms",
    }
)
FORBIDDEN_PREFIXES = (
    "app.services",
    "app.models",
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
    "app.study_plan",
    "app.application",
    "app.domain.learning_journey",
)


# ---------------------------------------------------------------------------
# Lazy package exports
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "name",
    [
        "Curriculum",
        "CurriculumGraph",
        "CurriculumId",
        "CurriculumNavigationService",
        "CurriculumRepository",
        "CurriculumVersion",
        "Dependency",
        "DependencyType",
        "GraphBuilder",
        "GraphEdge",
        "GraphNode",
        "GraphValidationResult",
        "GraphValidator",
        "LearningPath",
        "Module",
        "Prerequisite",
        "PrerequisiteEvaluation",
        "PrerequisiteService",
        "RevisionLink",
        "RevisionPathService",
        "Subject",
        "Topic",
        "TopicDifficulty",
        "TopicId",
        "TopicStatus",
    ],
)
def test_package_exports_resolve(name: str) -> None:
    import app.domain.curriculum as pkg

    assert getattr(pkg, name) is not None


def test_package_dir_includes_exports() -> None:
    import app.domain.curriculum as pkg

    names = dir(pkg)
    assert "CurriculumGraph" in names
    assert "Topic" in names


def test_package_unknown_attr() -> None:
    import app.domain.curriculum as pkg

    with pytest.raises(AttributeError):
        _ = pkg.DoesNotExist  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Repository contract
# ---------------------------------------------------------------------------


def test_repository_is_abstract() -> None:
    assert issubclass(CurriculumRepository, ABC)
    with pytest.raises(TypeError):
        CurriculumRepository()  # type: ignore[abstract]


def test_in_memory_repository_contract() -> None:
    class InMemoryCurriculumRepository(CurriculumRepository):
        def __init__(self) -> None:
            self._store: dict[str, Curriculum] = {}

        def get_by_id(self, curriculum_id: str | CurriculumId) -> Curriculum | None:
            return self._store.get(CurriculumId.of(curriculum_id).value)

        def list_all(self) -> list[Curriculum]:
            return list(self._store.values())

        def save(self, curriculum: Curriculum) -> None:
            self._store[curriculum.curriculum_id.value] = curriculum

        def delete(self, curriculum_id: str | CurriculumId) -> bool:
            key = CurriculumId.of(curriculum_id).value
            if key not in self._store:
                return False
            del self._store[key]
            return True

    repo = InMemoryCurriculumRepository()
    curr = linear_curriculum()
    assert repo.get_by_id(curr.curriculum_id) is None
    repo.save(curr)
    assert repo.get_by_id("demo-curr") is curr
    assert len(repo.list_all()) == 1
    assert repo.delete("demo-curr") is True
    assert repo.delete("demo-curr") is False


def test_repository_methods_documented() -> None:
    methods = {
        "get_by_id",
        "list_all",
        "save",
        "delete",
    }
    for name in methods:
        assert hasattr(CurriculumRepository, name)
        assert callable(getattr(CurriculumRepository, name))


# ---------------------------------------------------------------------------
# Framework independence (AST scan)
# ---------------------------------------------------------------------------


def _iter_domain_py_files() -> list[Path]:
    return sorted(DOMAIN_ROOT.rglob("*.py"))


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.append(node.module)
    return modules


def test_domain_root_exists() -> None:
    assert DOMAIN_ROOT.is_dir()
    assert (DOMAIN_ROOT / "graph" / "curriculum_graph.py").is_file()


def test_no_forbidden_imports_in_curriculum_domain() -> None:
    violations: list[str] = []
    for path in _iter_domain_py_files():
        for mod in _imported_modules(path):
            root = mod.split(".", 1)[0]
            if root in FORBIDDEN_ROOT_MODULES or mod in FORBIDDEN_ROOT_MODULES:
                violations.append(f"{path.name}: {mod}")
            for prefix in FORBIDDEN_PREFIXES:
                if mod == prefix or mod.startswith(prefix + "."):
                    violations.append(f"{path.name}: {mod}")
    assert violations == []


def test_curriculum_domain_does_not_import_learning_journey() -> None:
    for path in _iter_domain_py_files():
        for mod in _imported_modules(path):
            assert "learning_journey" not in mod, path


def test_entities_are_importable_without_flask() -> None:
    # Smoke: constructing domain objects needs no app context.
    curr = make_curriculum("x")
    assert curr.curriculum_id.value == "x"
    g = CurriculumGraph()
    g.add_topic(GraphNode.create("t", "T"))
    assert g.topic_count() == 1


def test_graph_builder_and_services_compose() -> None:
    curr = linear_curriculum()
    graph = GraphBuilder().build_from_curriculum(curr)
    nav = CurriculumNavigationService(curr, graph)
    prereq = PrerequisiteService(graph)
    rev = RevisionPathService(graph)
    assert nav.next_topic("a") is not None
    assert prereq.eligible_topics(set())
    assert rev.revision_clusters()


def test_value_object_enums_exhaustive() -> None:
    assert set(DependencyType) == {
        DependencyType.REQUIRES,
        DependencyType.RECOMMENDS,
        DependencyType.RELATED,
        DependencyType.OPTIONAL,
        DependencyType.REVISION,
    }
    assert set(TopicDifficulty) == {
        TopicDifficulty.FOUNDATIONAL,
        TopicDifficulty.INTERMEDIATE,
        TopicDifficulty.ADVANCED,
        TopicDifficulty.CAPSTONE,
    }
    assert set(TopicStatus) == {
        TopicStatus.LOCKED,
        TopicStatus.AVAILABLE,
        TopicStatus.ACTIVE,
        TopicStatus.COMPLETED,
        TopicStatus.ARCHIVED,
    }


def test_validation_result_is_valid_property() -> None:
    ok = GraphValidationResult()
    assert ok.is_valid
    bad = GraphValidationResult(issues=("cycle",), has_cycles=True)
    assert not bad.is_valid


def test_topic_id_str() -> None:
    assert str(TopicId("abc")) == "abc"
    assert str(CurriculumId("cs1")) == "cs1"


def test_curriculum_version_on_empty() -> None:
    curr = make_curriculum("paper-x", version_label="2025.1")
    assert curr.version.version_label == "2025.1"
    assert curr.version.schema_version == 1
