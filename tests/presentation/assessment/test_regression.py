"""Regression: Assessment Delivery must not touch Twin / Reasoning / Mission."""

from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN_IMPORT_FRAGMENTS = (
    "student_digital_twin",
    "educational_reasoning",
    "StudentReasoningService",
    "mission_engine",
    "intelligent_tutor",
)


def _python_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.py") if p.is_file()]


def test_presentation_assessment_import_purity() -> None:
    root = Path(__file__).resolve().parents[3] / "app/presentation/assessment"
    for path in _python_files(root):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for frag in FORBIDDEN_IMPORT_FRAGMENTS:
                        assert frag not in alias.name, f"{path}: {alias.name}"
            elif isinstance(node, ast.ImportFrom) and node.module:
                for frag in FORBIDDEN_IMPORT_FRAGMENTS:
                    assert frag not in node.module, f"{path}: {node.module}"


def test_delivery_service_stops_before_reasoning() -> None:
    path = (
        Path(__file__).resolve().parents[3]
        / "src/application/assessment/delivery/delivery_service.py"
    )
    text = path.read_text(encoding="utf-8")
    assert "mark_reasoned" not in text
    assert "StudentReasoningService" not in text
    assert "EvidencePackagingService" in text
    assert "export_for_ap001" not in text or "Does not invoke" in text
    # Packaging exposes evidence only; delivery must not call Reasoning.
    assert "StudentDigitalTwin" not in text
    assert "mission_engine" not in text
