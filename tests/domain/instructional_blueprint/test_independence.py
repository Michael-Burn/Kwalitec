"""Domain independence and package boundary tests."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

DOMAIN_ROOT = (
    Path(__file__).resolve().parents[3] / "app" / "domain" / "instructional_blueprint"
)

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
    "app.curriculum",
    "app.domain.curriculum",
    "app.domain.learning_journey",
    "app.domain.learning_activity",
)


def _iter_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.append(node.module)
    return found


def test_domain_has_no_forbidden_imports():
    offenders: list[str] = []
    for path in DOMAIN_ROOT.rglob("*.py"):
        for module in _iter_imports(path):
            if module in FORBIDDEN_ROOT_MODULES or any(
                module == prefix or module.startswith(prefix + ".")
                for prefix in FORBIDDEN_PREFIXES
            ):
                offenders.append(f"{path}: {module}")
            if module.startswith("flask") or module.startswith("sqlalchemy"):
                offenders.append(f"{path}: {module}")
    assert offenders == []


def test_domain_source_mentions_no_student_state_apis():
    # Soft structural check: domain files should not reference student_id.
    for path in DOMAIN_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "student_id" not in text
        assert "mastery_score" not in text


def test_required_domain_files_exist():
    required = {
        "blueprint.py",
        "blueprint_step.py",
        "blueprint_rule.py",
        "blueprint_profile.py",
        "blueprint_type.py",
        "__init__.py",
    }
    present = {path.name for path in DOMAIN_ROOT.glob("*.py")}
    assert required <= present


@pytest.mark.parametrize(
    "name",
    [
        "BlueprintProfile",
        "BlueprintRule",
        "BlueprintRuleKind",
        "BlueprintStep",
        "BlueprintType",
        "EffortBand",
        "InstructionalBlueprint",
        "effort_at_least",
        "effort_rank",
        "effort_units_for",
        "resolve_effort_band",
    ],
)
def test_domain_lazy_export_names(name):
    import app.domain.instructional_blueprint as pkg

    assert hasattr(pkg, name)
    assert getattr(pkg, name) is not None


def test_unknown_domain_export_raises():
    import app.domain.instructional_blueprint as pkg

    with pytest.raises(AttributeError):
        getattr(pkg, "NotARealExport")
