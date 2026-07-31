"""V1S-004 — founder dogfood validation registry and readiness sections.

Superseded in part by V1S-005 taxonomy; kept for continuity of prior evidence.
"""

from __future__ import annotations

from pathlib import Path

from app.services.dogfood_validation import (
    CLASS_WORKS_WELL,
    DOGFOOD_PROGRESS,
    EDUCATIONAL_IMPROVEMENTS,
    FINDING_CLASSES,
    PRODUCT_RATINGS,
    SURFACE_AUDIT,
    VALIDATION_ISSUES,
    assert_dogfood_registry_integrity,
    outstanding_issues,
    resolved_issues,
    validation_issue_counts,
)
from app.services.v1_readiness_dashboard import build_v1_readiness_snapshot

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_dogfood_registry_integrity():
    assert_dogfood_registry_integrity()
    assert len(DOGFOOD_PROGRESS) >= 1
    assert len(VALIDATION_ISSUES) >= 8
    assert len(EDUCATIONAL_IMPROVEMENTS) >= 4
    assert len(PRODUCT_RATINGS) == 8
    assert len(SURFACE_AUDIT) == 6


def test_finding_classes_include_remediation_taxonomy():
    required = {
        "WORKS WELL",
        "BUG",
        "LEARNING FRICTION",
        "UX IMPROVEMENT",
        "TECHNICAL DEBT",
        "DEFERRED",
    }
    assert required == set(FINDING_CLASSES)
    used = {i.finding_class for i in VALIDATION_ISSUES}
    assert "BUG" in used
    assert "LEARNING FRICTION" in used


def test_outstanding_excludes_works_well():
    for issue in outstanding_issues():
        assert issue.finding_class != CLASS_WORKS_WELL
        assert issue.status in {"OPEN", "DEFERRED"}


def test_resolved_includes_works_well_baselines():
    resolved = resolved_issues()
    assert any(i.finding_class == CLASS_WORKS_WELL for i in resolved)
    assert all(i.status == "RESOLVED" for i in resolved)


def test_educational_improvements_cover_four_questions():
    questions = {e.question for e in EDUCATIONAL_IMPROVEMENTS}
    assert "What am I learning today?" in questions
    assert "Why am I learning it?" in questions
    assert "How do I know I succeeded?" in questions
    assert "What should I do next?" in questions


def test_product_ratings_cover_required_areas():
    areas = {r.area for r in PRODUCT_RATINGS}
    required = {
        "Loading states",
        "Empty states",
        "Navigation",
        "Typography",
        "Spacing",
        "Motion",
        "Terminology",
        "Daily workflow",
    }
    assert areas == required
    assert all(1 <= r.score <= 5 for r in PRODUCT_RATINGS)


def test_v1_readiness_snapshot_includes_dogfood_sections():
    snapshot = build_v1_readiness_snapshot()
    assert snapshot.programme in {"V1S-005", "V1S-006"}
    assert snapshot.dogfood_progress_summary
    assert len(snapshot.dogfood_progress) >= 1
    assert len(snapshot.resolved_issues) >= 1
    assert len(snapshot.educational_improvements) >= 4
    assert len(snapshot.product_ratings) == 8
    assert len(snapshot.surface_audit) == 6
    assert "Dogfood validation" in {d.name for d in snapshot.dimensions}
    counts = snapshot.validation_issue_counts
    assert counts == validation_issue_counts()
    assert sum(counts.values()) == len(VALIDATION_ISSUES)


def test_dogfood_report_exists():
    assert (REPO_ROOT / "V1S004_DOGFOOD_REPORT.md").is_file()


def test_v1_readiness_template_has_dogfood_sections():
    path = (
        REPO_ROOT
        / "app"
        / "founder"
        / "dashboard"
        / "templates"
        / "founder_dashboard"
        / "v1_readiness.html"
    )
    text = path.read_text(encoding="utf-8")
    for label in (
        "Dogfood Progress",
        "Validation Issues",
        "Educational Improvements",
        "Resolved Issues",
        "Outstanding Issues",
        "Learning Friction",
    ):
        assert label in text, f"Missing template section: {label}"
