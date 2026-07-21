"""Architecture purity tests for BR-004 persistence adapters."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[5]
    / "src"
    / "infrastructure"
    / "persistence"
)

BR004_ADAPTER_FILES = (
    PACKAGE_ROOT / "user_repository.py",
    PACKAGE_ROOT / "onboarding_repository.py",
    PACKAGE_ROOT / "checkpoint_repository.py",
    PACKAGE_ROOT / "twin_repository.py",
    PACKAGE_ROOT / "evidence_repository.py",
    PACKAGE_ROOT / "sqlalchemy_uow.py",
)

BR004_MAPPER_FILES = (
    PACKAGE_ROOT / "mappers" / "user_mapper.py",
    PACKAGE_ROOT / "mappers" / "onboarding_mapper.py",
    PACKAGE_ROOT / "mappers" / "checkpoint_mapper.py",
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
    }
)


def _defined_methods(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
    }


def test_br004_adapter_files_exist() -> None:
    for path in BR004_ADAPTER_FILES:
        assert path.is_file(), f"missing {path.name}"


def test_br004_mapper_files_exist() -> None:
    for path in BR004_MAPPER_FILES:
        assert path.is_file(), f"missing {path.name}"


@pytest.mark.parametrize(
    "path",
    BR004_ADAPTER_FILES,
    ids=lambda p: p.name,
)
def test_adapters_define_no_educational_intelligence(path: Path) -> None:
    methods = _defined_methods(path)
    for forbidden in FORBIDDEN_METHOD_NAMES:
        assert forbidden not in methods, f"{path.name} defines {forbidden}"


@pytest.mark.parametrize(
    "path",
    BR004_ADAPTER_FILES + BR004_MAPPER_FILES,
    ids=lambda p: p.name,
)
def test_modules_use_future_annotations(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    assert "from __future__ import annotations" in source


def test_product_uow_does_not_import_flask() -> None:
    source = (PACKAGE_ROOT / "sqlalchemy_uow.py").read_text(encoding="utf-8").lower()
    assert "flask" not in source
