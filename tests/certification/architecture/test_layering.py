"""Architecture certification — layering and dependency rules."""

from __future__ import annotations

from tests.certification.helpers import (
    AUTOMATION_ROOT,
    FOUNDER_ROOT,
    imports_matching,
    package_imports,
)

# Packages that must never depend on Flask / presentation.
_CORE_PACKAGES = (
    "knowledge_engine",
    "capability_archive",
    "internal_alpha",
    "operational_state",
    "recommendations",
    "briefing",
    "internal_alpha_workflow",
)

# Founder dependency direction (allowed →, prohibited ←).
_FORBIDDEN: dict[str, tuple[str, ...]] = {
    "knowledge_engine": (
        "app.founder.capability_archive",
        "app.founder.internal_alpha",
        "app.founder.operational_state",
        "app.founder.recommendations",
        "app.founder.briefing",
        "app.founder.dashboard",
        "app.founder.internal_alpha_workflow",
        "app.automation",
        "flask",
    ),
    "capability_archive": (
        "app.founder.knowledge_engine",
        "app.founder.internal_alpha",
        "app.founder.operational_state",
        "app.founder.recommendations",
        "app.founder.briefing",
        "app.founder.dashboard",
        "app.founder.internal_alpha_workflow",
        "app.automation",
        "flask",
    ),
    "internal_alpha": (
        "app.founder.knowledge_engine",
        "app.founder.capability_archive",
        "app.founder.operational_state",
        "app.founder.recommendations",
        "app.founder.briefing",
        "app.founder.dashboard",
        "app.founder.internal_alpha_workflow",
        "app.automation",
        "flask",
    ),
    "operational_state": (
        "app.founder.recommendations",
        "app.founder.briefing",
        "app.founder.dashboard",
        "app.founder.internal_alpha_workflow",
        "app.founder.internal_alpha",
        "app.automation",
        "flask",
    ),
    "recommendations": (
        "app.founder.knowledge_engine",
        "app.founder.capability_archive",
        "app.founder.internal_alpha",
        "app.founder.briefing",
        "app.founder.dashboard",
        "app.founder.internal_alpha_workflow",
        "app.automation",
        "flask",
    ),
    "briefing": (
        "app.founder.knowledge_engine",
        "app.founder.capability_archive",
        "app.founder.internal_alpha",
        "app.founder.dashboard",
        "app.founder.internal_alpha_workflow",
        "app.automation",
        "flask",
    ),
    "internal_alpha_workflow": (
        "app.founder.dashboard",
        "app.automation",
        "flask",
    ),
    "dashboard": (
        "app.founder.knowledge_engine.repository",
        "app.founder.capability_archive.repository",
        "app.automation",
    ),
}


class TestFounderLayering:
    def test_core_packages_do_not_import_flask(self) -> None:
        violations: list[str] = []
        for name in _CORE_PACKAGES:
            imports = package_imports(FOUNDER_ROOT / name)
            flask_hits = imports_matching(imports, "flask")
            if flask_hits:
                violations.append(f"{name}: {sorted(flask_hits)}")
        assert not violations, f"Flask leaked into core packages: {violations}"

    def test_forbidden_cross_package_imports(self) -> None:
        violations: list[str] = []
        for package, forbidden_prefixes in _FORBIDDEN.items():
            imports = package_imports(FOUNDER_ROOT / package)
            for prefix in forbidden_prefixes:
                hits = imports_matching(imports, prefix)
                if hits:
                    violations.append(f"{package} → {prefix}: {sorted(hits)}")
        assert not violations, (
            "Dependency rule violations:\n" + "\n".join(violations)
        )

    def test_operational_state_live_bridges_avoid_repository_imports(
        self,
    ) -> None:
        """FSI-001 bridges use query services — not repository scanners."""

        imports = package_imports(FOUNDER_ROOT / "operational_state")
        ke_repo = imports_matching(
            imports, "app.founder.knowledge_engine.repository"
        )
        ca_repo = imports_matching(
            imports, "app.founder.capability_archive.repository"
        )
        assert not ke_repo, ke_repo
        assert not ca_repo, ca_repo

    def test_automation_framework_is_flask_free(self) -> None:
        imports = package_imports(AUTOMATION_ROOT)
        assert not imports_matching(imports, "flask")

    def test_automation_does_not_import_dashboard(self) -> None:
        imports = package_imports(AUTOMATION_ROOT)
        assert not imports_matching(imports, "app.founder.dashboard")
