"""Architecture purity and package export checks for Learning Episode."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[4]
    / "src"
    / "domain"
    / "education"
    / "learning_episode"
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
        "pydantic",
        "marshmallow",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "app.",
    "app.models",
    "app.services",
    "app.domain",
)


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


def test_package_directory_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    expected_files = {
        PACKAGE_ROOT / "__init__.py",
        PACKAGE_ROOT / "aggregates" / "learning_episode.py",
        PACKAGE_ROOT / "entities" / "episode_step.py",
        PACKAGE_ROOT / "entities" / "episode_goal.py",
        PACKAGE_ROOT / "entities" / "episode_reflection.py",
        PACKAGE_ROOT / "entities" / "episode_outcome.py",
        PACKAGE_ROOT / "value_objects" / "episode_sequence.py",
        PACKAGE_ROOT / "value_objects" / "episode_duration.py",
        PACKAGE_ROOT / "value_objects" / "episode_progress.py",
        PACKAGE_ROOT / "policies" / "episode_validation_policy.py",
        PACKAGE_ROOT / "policies" / "atomicity_policy.py",
        PACKAGE_ROOT / "policies" / "sequencing_policy.py",
        PACKAGE_ROOT / "specifications" / "episode_is_complete.py",
        PACKAGE_ROOT / "specifications" / "episode_is_atomic.py",
        PACKAGE_ROOT / "specifications" / "episode_can_transition.py",
        PACKAGE_ROOT / "events" / "episode_started.py",
        PACKAGE_ROOT / "events" / "episode_completed.py",
        PACKAGE_ROOT / "events" / "reflection_recorded.py",
        PACKAGE_ROOT / "enums.py",
    }
    for path in expected_files:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT)}"


@pytest.mark.parametrize(
    "path",
    _iter_python_files(),
    ids=lambda p: str(p.relative_to(PACKAGE_ROOT)),
)
def test_no_forbidden_infrastructure_imports(path: Path) -> None:
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
def test_no_persistence_or_serialization_imports(path: Path) -> None:
    imported = _imported_modules(path)
    forbidden_substrings = (
        "pickle",
        "sqlite",
        "psycopg",
        "pymongo",
        "dto",
        "repository",
        "serializer",
    )
    for name in imported:
        lowered = name.lower()
        for fragment in forbidden_substrings:
            assert fragment not in lowered.split("."), (
                f"{path.name} imports infrastructure-like module {name}"
            )


def test_imports_only_stdlib_foundation_or_self() -> None:
    allowed_stdlib = {
        "dataclasses",
        "typing",
        "collections.abc",
        "abc",
        "__future__",
        "enum",
        "re",
    }
    for path in _iter_python_files():
        for name in _imported_modules(path):
            if name.startswith("domain.education.foundation"):
                continue
            if name.startswith("domain.education.learning_episode"):
                continue
            assert name in allowed_stdlib, (
                f"{path.relative_to(PACKAGE_ROOT)} imports unexpected {name}"
            )


def test_public_exports() -> None:
    from domain.education import learning_episode as package

    required = [
        "LearningEpisode",
        "EpisodeGoal",
        "EpisodeGoalId",
        "EpisodeStep",
        "EpisodeReflection",
        "EpisodeOutcome",
        "EpisodeOutcomeId",
        "EpisodeStepId",
        "EpisodeStepKind",
        "EpisodeSequence",
        "EpisodeDuration",
        "EpisodeProgress",
        "EpisodeStatus",
        "EpisodeStepStatus",
        "EpisodeOutcomeKind",
        "DurationBand",
        "EpisodeValidationPolicy",
        "AtomicityPolicy",
        "SequencingPolicy",
        "EpisodeIsAtomicSpecification",
        "EpisodeCanCompleteSpecification",
        "EpisodeIsCompleteSpecification",
        "EpisodeSupportsReflectionSpecification",
        "EpisodeCanTransitionSpecification",
        "EpisodeStarted",
        "EpisodeCompleted",
        "ReflectionRecorded",
    ]
    for name in required:
        assert hasattr(package, name), f"missing export: {name}"
        assert name in package.__all__


@pytest.mark.parametrize(
    "module_path",
    [
        "domain.education.learning_episode.aggregates.learning_episode",
        "domain.education.learning_episode.entities.episode_goal",
        "domain.education.learning_episode.entities.episode_step",
        "domain.education.learning_episode.entities.episode_reflection",
        "domain.education.learning_episode.entities.episode_outcome",
        "domain.education.learning_episode.value_objects.episode_sequence",
        "domain.education.learning_episode.value_objects.episode_duration",
        "domain.education.learning_episode.value_objects.episode_progress",
        "domain.education.learning_episode.policies.atomicity_policy",
        "domain.education.learning_episode.policies.sequencing_policy",
        "domain.education.learning_episode.policies.episode_validation_policy",
        "domain.education.learning_episode.events.episode_started",
        "domain.education.learning_episode.events.episode_completed",
        "domain.education.learning_episode.events.reflection_recorded",
    ],
)
def test_architecture_source_traceability(module_path: str) -> None:
    module = __import__(module_path, fromlist=["*"])
    doc = module.__doc__ or ""
    assert "Architecture Source" in doc
    assert any(
        token in doc
        for token in (
            "LEARNING_EPISODE_ARCHITECTURE.md",
            "LEARNING_EPISODE_INVARIANTS.md",
            "LEARNING_EPISODE_LIFECYCLE.md",
            "LEARNING_EPISODE_TYPES.md",
            "LEARNING_EPISODE_SEQUENCE.md",
            "EDUCATIONAL_ATOMICITY.md",
        )
    )
    assert "Concept" in doc


def test_no_setter_methods_on_aggregate() -> None:
    from domain.education.learning_episode import LearningEpisode

    forbidden = {
        name
        for name in dir(LearningEpisode)
        if name.startswith("set_") or name.startswith("update_")
    }
    assert forbidden == set()


def test_no_infrastructure_import_statements() -> None:
    """Docstrings may name forbidden tech; import graphs must not use them."""
    for path in _iter_python_files():
        imported = _imported_modules(path)
        for name in imported:
            lowered = name.casefold()
            assert "flask" not in lowered
            assert "sqlalchemy" not in lowered
            assert "repository" not in lowered
            assert not lowered.endswith(".dto")
