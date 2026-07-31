"""V1S-003 — repository health, package lifecycle, engineering standards."""

from __future__ import annotations

import ast
from pathlib import Path

from app.application.mission_adapter import (
    V1S002_DISPOSITION as ADAPTER_DISPOSITION,
)
from app.application.mission_engine import (
    V1S002_DISPOSITION as ME_DISPOSITION,
)
from app.application.mission_engine_v2 import (
    V1S002_DISPOSITION as MEV2_DISPOSITION,
)
from app.services.package_lifecycle import (
    APPLICATION_PACKAGES,
    LIFECYCLE_ARCHIVED,
    LIFECYCLE_REMOVE,
    LIFECYCLE_VALUES,
    assert_registry_integrity,
    lifecycle_counts,
    packages_by_lifecycle,
)
from app.services.v1_readiness_dashboard import build_v1_readiness_snapshot

REPO_ROOT = Path(__file__).resolve().parents[1]
APP_APPLICATION = REPO_ROOT / "app" / "application"

ENGINEERING_DOCS = (
    "docs/engineering/REPOSITORY_STANDARDS.md",
    "docs/engineering/NAMING_STANDARDS.md",
    "docs/engineering/MODULE_STANDARDS.md",
    "docs/engineering/DEPENDENCY_RULES_APP.md",
    "docs/engineering/PACKAGE_LIFECYCLE_POLICY.md",
)


def test_package_lifecycle_registry_integrity():
    assert_registry_integrity()
    counts = lifecycle_counts()
    assert set(counts) == LIFECYCLE_VALUES
    assert sum(counts.values()) > 50
    assert counts[LIFECYCLE_ARCHIVED] >= 2
    assert counts[LIFECYCLE_REMOVE] >= 1


def test_every_application_package_is_registered():
    on_disk = {
        p.name
        for p in APP_APPLICATION.iterdir()
        if p.is_dir() and not p.name.startswith("_")
    }
    registered = {Path(entry.path).name for entry in APPLICATION_PACKAGES}
    missing = on_disk - registered
    extra = registered - on_disk
    assert missing == set(), f"Unregistered application packages: {missing}"
    assert extra == set(), f"Registry paths missing on disk: {extra}"


def test_archived_mission_packages_align_with_v1s002_markers():
    assert ME_DISPOSITION == "DEPRECATED"
    assert MEV2_DISPOSITION == "ARCHIVE"
    assert ADAPTER_DISPOSITION == "ARCHIVE"
    archived_paths = {e.path for e in packages_by_lifecycle(LIFECYCLE_ARCHIVED)}
    assert "app/application/mission_engine_v2" in archived_paths
    assert "app/application/mission_adapter" in archived_paths


def test_student_presentation_does_not_import_remove_packages():
    forbidden = (
        "app.application.mission_engine_v2",
        "app.application.mission_adapter",
        "app.application.learning_loop",
        "app.application.instructional_blueprint",
    )
    offenders: list[str] = []
    for path in (REPO_ROOT / "app" / "presentation").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(alias.name.startswith(f) for f in forbidden):
                        offenders.append(f"{path}:{alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(node.module.startswith(f) for f in forbidden):
                    offenders.append(f"{path}:{node.module}")
    assert offenders == []


def test_app_does_not_import_src_runtime_modules():
    offenders: list[str] = []
    for path in (REPO_ROOT / "app").rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "from src." not in text and "import src." not in text:
            continue
        tree = ast.parse(text, filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "src" or alias.name.startswith("src."):
                        offenders.append(f"{path}:{alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if node.module == "src" or node.module.startswith("src."):
                    offenders.append(f"{path}:{node.module}")
    assert offenders == []


def test_engineering_standards_documents_exist():
    for rel in ENGINEERING_DOCS:
        assert (REPO_ROOT / rel).is_file(), f"Missing standards doc: {rel}"


def test_v1_readiness_snapshot_includes_repository_health():
    snapshot = build_v1_readiness_snapshot()
    assert snapshot.programme in {"V1S-003", "V1S-004", "V1S-005"}
    assert snapshot.repository_health_summary
    assert len(snapshot.application_packages) == len(APPLICATION_PACKAGES)
    assert len(snapshot.engineering_quality) >= 4
    assert len(snapshot.code_debt) >= 5
    assert "ACTIVE" in snapshot.lifecycle_counts
    dim_names = {d.name for d in snapshot.dimensions}
    assert "Repository health" in dim_names
    assert "Engineering quality" in dim_names
    assert any("package_lifecycle.py" in p for p in snapshot.evidence_paths)
