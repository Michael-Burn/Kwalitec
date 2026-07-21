"""Architecture purity for Flask onboarding adapter package layout (BR-002)."""

from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[5] / "src" / "adapters" / "flask" / "onboarding"
)

EXPECTED_FILES = {
    PACKAGE_ROOT / "__init__.py",
    PACKAGE_ROOT / "controller.py",
    PACKAGE_ROOT / "routes.py",
    PACKAGE_ROOT / "dependency_provider.py",
    PACKAGE_ROOT / "factory.py",
}


def test_package_layout() -> None:
    assert PACKAGE_ROOT.is_dir()
    for path in EXPECTED_FILES:
        assert path.is_file(), f"missing {path.name}"


def test_controller_has_no_flask_import() -> None:
    source = (PACKAGE_ROOT / "controller.py").read_text(encoding="utf-8")
    assert "import flask" not in source
    assert "from flask" not in source


def test_routes_do_not_contain_recommendation_logic() -> None:
    source = (PACKAGE_ROOT / "routes.py").read_text(encoding="utf-8").lower()
    for fragment in ("generate_mission", "calculate_mastery", "openai", "anthropic"):
        assert fragment not in source
