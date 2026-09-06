"""Architecture independence for the Study Curriculum assembler."""

from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN_IMPORT_FRAGMENTS = (
    "educational_packages",
    "educational_campaigns",
    "educational_authoring",
    "curriculum.data",
    "curriculum/data",
    "app.curriculum.data",
)

FORBIDDEN_SINGLE_TOPIC_ATTRS = frozenset(
    {
        "topic_knowledge",
        "topic_covered",
        "topics_with_estimated_knowledge",
    }
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _study_curriculum_app_paths() -> list[Path]:
    root = _repo_root() / "app" / "application" / "study_curriculum"
    return sorted(root.rglob("*.py"))


def _study_curriculum_infra_paths() -> list[Path]:
    root = _repo_root() / "app" / "infrastructure" / "adapters" / "study_curriculum"
    return sorted(root.rglob("*.py"))


def test_study_curriculum_modules_do_not_import_content_authoring_paths():
    offenders: list[str] = []
    for path in _study_curriculum_app_paths() + _study_curriculum_infra_paths():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            for mod in modules:
                lowered = mod.replace("\\", "/")
                for frag in FORBIDDEN_IMPORT_FRAGMENTS:
                    if frag in lowered:
                        offenders.append(f"{path.name}:{mod}")
    assert offenders == [], offenders


def test_assembler_does_not_call_single_topic_twin_or_coverage_methods():
    path = (
        _repo_root()
        / "app"
        / "application"
        / "study_curriculum"
        / "assembler.py"
    )
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    called: list[str] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Attribute)
            and node.attr in FORBIDDEN_SINGLE_TOPIC_ATTRS
        ):
            called.append(node.attr)
    assert called == []


def test_application_package_does_not_import_flask_or_models():
    offenders: list[str] = []
    forbidden = ("flask", "sqlalchemy", "app.models", "app.extensions")
    for path in _study_curriculum_app_paths():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            for mod in modules:
                if any(mod == f or mod.startswith(f + ".") for f in forbidden):
                    offenders.append(f"{path.name}:{mod}")
    assert offenders == [], offenders
