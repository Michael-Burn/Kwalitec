"""V1S-005 — dogfood remediation registry, friction board, package readiness."""

from __future__ import annotations

from pathlib import Path

from app.services.dogfood_validation import (
    CLASS_BUG,
    CLASS_DEFERRED,
    CLASS_LEARNING_FRICTION,
    CLASS_TECHNICAL_DEBT,
    CLASS_UX_IMPROVEMENT,
    CLASS_WORKS_WELL,
    DOGFOOD_PROGRESS,
    EDUCATIONAL_IMPROVEMENTS,
    FINDING_CLASSES,
    LEARNING_FRICTION_REGISTER,
    PRODUCT_RATINGS,
    SURFACE_AUDIT,
    VALIDATION_ISSUES,
    assert_dogfood_registry_integrity,
    assess_dogfood_package_readiness,
    dogfood_confidence_trend,
    dogfood_metrics_summary,
    open_educational_improvements,
    open_friction_issues,
    outstanding_issues,
    resolved_friction_records,
    resolved_issues,
    validation_issue_counts,
)
from app.services.v1_readiness_dashboard import build_v1_readiness_snapshot

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_dogfood_registry_integrity():
    assert_dogfood_registry_integrity()
    assert len(DOGFOOD_PROGRESS) >= 3
    assert len(VALIDATION_ISSUES) >= 12
    assert len(EDUCATIONAL_IMPROVEMENTS) >= 4
    assert len(PRODUCT_RATINGS) == 8
    assert len(SURFACE_AUDIT) == 6
    assert len(LEARNING_FRICTION_REGISTER) >= 8


def test_finding_classes_cover_v1s005_taxonomy():
    required = {
        CLASS_BUG,
        CLASS_LEARNING_FRICTION,
        CLASS_UX_IMPROVEMENT,
        CLASS_TECHNICAL_DEBT,
        CLASS_DEFERRED,
        CLASS_WORKS_WELL,
    }
    assert required == set(FINDING_CLASSES)
    used = {i.finding_class for i in VALIDATION_ISSUES}
    assert CLASS_BUG in used
    assert CLASS_LEARNING_FRICTION in used
    assert CLASS_UX_IMPROVEMENT in used


def test_p0_issues_resolved():
    by_id = {i.issue_id: i for i in VALIDATION_ISSUES}
    for issue_id in ("DF-001", "DF-002", "DF-003"):
        assert by_id[issue_id].status == "RESOLVED"
        assert by_id[issue_id].priority == "P0"


def test_p1_issues_resolved():
    by_id = {i.issue_id: i for i in VALIDATION_ISSUES}
    for issue_id in (
        "DF-004",
        "DF-005",
        "DF-006",
        "DF-007",
        "DF-008",
        "DF-009",
    ):
        assert by_id[issue_id].status == "RESOLVED"


def test_outstanding_excludes_works_well():
    for issue in outstanding_issues():
        assert issue.finding_class != CLASS_WORKS_WELL
        assert issue.status in {"OPEN", "DEFERRED"}


def test_resolved_friction_records_match_register():
    records = resolved_friction_records()
    assert records == LEARNING_FRICTION_REGISTER
    assert all(r.before and r.after and r.student_benefit for r in records)


def test_open_friction_may_include_v1s006_p0():
    """V1S-005–008 closed educational P0 friction; none remain open."""
    by_id = {i.issue_id: i for i in VALIDATION_ISSUES}
    for issue_id in ("DF-001", "DF-002", "DF-003", "DF-013", "DF-014", "DF-016"):
        assert by_id[issue_id].status == "RESOLVED"
    open_p0 = [i for i in open_friction_issues() if i.priority == "P0"]
    assert open_p0 == []


def test_educational_improvements_resolved():
    assert not open_educational_improvements()
    questions = {e.question for e in EDUCATIONAL_IMPROVEMENTS}
    assert "What am I learning today?" in questions
    assert "Why am I learning it?" in questions
    assert "How do I know I succeeded?" in questions
    assert "What should I do next?" in questions


def test_confidence_trend_and_metrics():
    trend = dogfood_confidence_trend()
    assert len(trend) == len(DOGFOOD_PROGRESS)
    metrics = dogfood_metrics_summary()
    assert metrics["sittings"] == len(DOGFOOD_PROGRESS)
    assert metrics["avg_confidence"] >= 1


def test_package_readiness_helper_returns_structured_result(ctx):
    result = assess_dogfood_package_readiness("CS1")
    assert result.subject_code == "CS1"
    assert isinstance(result.ready, bool)
    assert result.reason


def test_v1_readiness_snapshot_includes_friction_board():
    snapshot = build_v1_readiness_snapshot()
    assert snapshot.programme in {"V1S-005", "V1S-006", "V1S-007", "V1S-008"}
    assert snapshot.dogfood_progress_summary
    assert len(snapshot.learning_friction_resolved) >= 8
    assert snapshot.package_readiness.subject_code == "CS1"
    assert snapshot.dogfood_confidence_trend
    assert snapshot.dogfood_metrics["sittings"] >= 3
    assert "Learning friction" in {d.name for d in snapshot.dimensions}
    counts = snapshot.validation_issue_counts
    assert counts == validation_issue_counts()
    assert sum(counts.values()) == len(VALIDATION_ISSUES)
    assert resolved_issues()


def test_v1s005_report_exists():
    assert (REPO_ROOT / "V1S005_IMPLEMENTATION_REPORT.md").is_file()


def test_v1_readiness_template_has_friction_sections():
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
        "Learning Friction",
        "Resolved Friction",
        "Open Friction",
        "Confidence Trend",
        "Dogfood Progress",
        "Validation Issues",
    ):
        assert label in text, f"Missing template section: {label}"


def test_home_template_has_remediation_markers():
    home = (
        REPO_ROOT / "app" / "templates" / "student" / "home.html"
    ).read_text(encoding="utf-8")
    session_body = (
        REPO_ROOT / "app" / "templates" / "session" / "partials" / "session_body.html"
    ).read_text(encoding="utf-8")
    # UX-001: episode / quiet / stages live on Session Overview; Home is decision-only.
    assert "015-tomorrow-preview" not in home
    assert 'data-ux="session-briefing"' in session_body
    assert "Session stages" in session_body
    assert "015-learning-episode" not in home


def test_syllabus_nav_label():
    from app.domain.student_experience.experience_workspace import (
        SURFACE_LABELS,
        ExperienceSurface,
    )

    assert SURFACE_LABELS[ExperienceSurface.JOURNEY] == "Syllabus"
