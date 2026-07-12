"""Tests for Educational Intelligence feature flags (Capability 3.3.1).

Covers safe defaults, immutability of the central configuration, and
framework independence (no Flask / routes / environment loading).
"""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from app.application.config import (
    ENABLE_EDUCATIONAL_ORCHESTRATOR,
    ENABLE_EI_EXPLAINABILITY,
    ENABLE_EI_MISSIONS,
    ENABLE_EI_PROGRESS,
    ENABLE_EI_RECOMMENDATIONS,
    FEATURE_FLAGS,
    EducationalIntelligenceFeatureFlags,
)

CONFIG_ROOT = Path(__file__).resolve().parents[2] / "app" / "application" / "config"

FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "wtforms",
        "dotenv",
    }
)

FORBIDDEN_PREFIXES = (
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
    "app.models",
    "app.services",
)

FLAG_NAMES = (
    "ENABLE_EDUCATIONAL_ORCHESTRATOR",
    "ENABLE_EI_RECOMMENDATIONS",
    "ENABLE_EI_MISSIONS",
    "ENABLE_EI_EXPLAINABILITY",
    "ENABLE_EI_PROGRESS",
)


# ═══════════════════════════════════════════════════════════════════════════════
# Default values
# ═══════════════════════════════════════════════════════════════════════════════


class TestDefaultValues:
    def test_all_flags_default_to_false(self) -> None:
        flags = EducationalIntelligenceFeatureFlags()
        for name in FLAG_NAMES:
            assert getattr(flags, name) is False

    def test_feature_flags_singleton_is_all_false(self) -> None:
        assert FEATURE_FLAGS.ENABLE_EDUCATIONAL_ORCHESTRATOR is False
        assert FEATURE_FLAGS.ENABLE_EI_RECOMMENDATIONS is False
        assert FEATURE_FLAGS.ENABLE_EI_MISSIONS is False
        assert FEATURE_FLAGS.ENABLE_EI_EXPLAINABILITY is False
        assert FEATURE_FLAGS.ENABLE_EI_PROGRESS is False

    def test_module_aliases_match_feature_flags(self) -> None:
        assert (
            ENABLE_EDUCATIONAL_ORCHESTRATOR
            is FEATURE_FLAGS.ENABLE_EDUCATIONAL_ORCHESTRATOR
        )
        assert ENABLE_EI_RECOMMENDATIONS is FEATURE_FLAGS.ENABLE_EI_RECOMMENDATIONS
        assert ENABLE_EI_MISSIONS is FEATURE_FLAGS.ENABLE_EI_MISSIONS
        assert ENABLE_EI_EXPLAINABILITY is FEATURE_FLAGS.ENABLE_EI_EXPLAINABILITY
        assert ENABLE_EI_PROGRESS is FEATURE_FLAGS.ENABLE_EI_PROGRESS

    def test_module_aliases_are_false(self) -> None:
        assert ENABLE_EDUCATIONAL_ORCHESTRATOR is False
        assert ENABLE_EI_RECOMMENDATIONS is False
        assert ENABLE_EI_MISSIONS is False
        assert ENABLE_EI_EXPLAINABILITY is False
        assert ENABLE_EI_PROGRESS is False


# ═══════════════════════════════════════════════════════════════════════════════
# Immutability
# ═══════════════════════════════════════════════════════════════════════════════


class TestImmutability:
    def test_feature_flags_instance_is_frozen(self) -> None:
        with pytest.raises(FrozenInstanceError):
            FEATURE_FLAGS.ENABLE_EDUCATIONAL_ORCHESTRATOR = True  # type: ignore[misc]

    def test_each_flag_assignment_raises(self) -> None:
        for name in FLAG_NAMES:
            with pytest.raises(FrozenInstanceError):
                setattr(FEATURE_FLAGS, name, True)

    def test_fresh_instance_is_also_frozen(self) -> None:
        flags = EducationalIntelligenceFeatureFlags(ENABLE_EI_MISSIONS=True)
        with pytest.raises(FrozenInstanceError):
            flags.ENABLE_EI_MISSIONS = False  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════════════════════════
# Framework independence
# ═══════════════════════════════════════════════════════════════════════════════


class TestFrameworkIndependence:
    def test_config_package_has_no_flask_route_or_service_imports(self) -> None:
        violations: list[str] = []
        for path in sorted(CONFIG_ROOT.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        if root in FORBIDDEN_ROOT_MODULES or alias.name.startswith(
                            FORBIDDEN_PREFIXES
                        ):
                            violations.append(f"{path.name}: import {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", 1)[0]
                    if root in FORBIDDEN_ROOT_MODULES or node.module.startswith(
                        FORBIDDEN_PREFIXES
                    ):
                        violations.append(f"{path.name}: from {node.module}")
        assert violations == []

    def test_feature_flags_source_has_no_environment_loading(self) -> None:
        src = (CONFIG_ROOT / "feature_flags.py").read_text(encoding="utf-8")
        assert "os.environ" not in src
        assert "getenv" not in src
        assert "dotenv" not in src
        assert "load_dotenv" not in src

    def test_feature_flags_source_has_no_flask_request_or_routes(self) -> None:
        src = (CONFIG_ROOT / "feature_flags.py").read_text(encoding="utf-8")
        assert "flask.request" not in src
        assert "flask.session" not in src
        assert "Blueprint" not in src
        assert "bp.route" not in src
        assert "sqlalchemy" not in src.lower()
