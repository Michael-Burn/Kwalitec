"""V1S-006 — live dogfood week evidence registry & Founder trends."""

from __future__ import annotations

from pathlib import Path

from app.services.dogfood_validation import (
    DOGFOOD_PROGRESS,
    LEARNING_FRICTION_REGISTER,
    VALIDATION_ISSUES,
    assert_dogfood_registry_integrity,
    dogfood_completion_trend,
    dogfood_confidence_trend,
    dogfood_friction_trend,
    dogfood_metrics_summary,
    dogfood_motivation_trend,
    dogfood_study_consistency,
    open_friction_issues,
    resolved_friction_records,
)
from app.services.v1_readiness_dashboard import build_v1_readiness_snapshot

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_dogfood_registry_integrity_v1s006():
    assert_dogfood_registry_integrity()


def test_day1_live_sitting_recorded():
    live = [e for e in DOGFOOD_PROGRESS if e.evidence_kind == "live_sitting"]
    assert len(live) >= 1
    day1 = live[0]
    assert day1.study_date == "2026-07-31"
    assert day1.subject == "CS1"
    assert day1.completion_status == "blocked"
    assert day1.confidence_before == 4
    assert day1.confidence_after == 2
    assert day1.motivation_before == 4
    assert day1.motivation_after == 2
    assert day1.workaround_reasons
    assert any("DF-013" in n for n in day1.learning_friction_notes)


def test_new_live_week_issues_status():
    """V1S-006 discoveries; V1S-007/008 resolve educational P0/P1 defects."""
    by_id = {i.issue_id: i for i in VALIDATION_ISSUES}
    for issue_id in ("DF-013", "DF-014", "DF-015", "DF-016"):
        assert issue_id in by_id
    assert by_id["DF-013"].status == "RESOLVED"
    assert by_id["DF-013"].priority == "P0"
    assert by_id["DF-014"].status == "RESOLVED"
    assert by_id["DF-014"].priority == "P0"
    assert by_id["DF-015"].status == "RESOLVED"
    assert by_id["DF-016"].status == "RESOLVED"
    open_ids = {i.issue_id for i in open_friction_issues()}
    assert "DF-013" not in open_ids
    assert "DF-016" not in open_ids
    assert "DF-014" not in open_ids
    assert "DF-015" not in open_ids


def test_no_duplicate_friction_or_issue_ids():
    issue_ids = [i.issue_id for i in VALIDATION_ISSUES]
    assert len(issue_ids) == len(set(issue_ids))
    friction_ids = [r.issue_id for r in LEARNING_FRICTION_REGISTER]
    assert len(friction_ids) == len(set(friction_ids))


def test_v1s005_resolved_p0_remain_resolved():
    by_id = {i.issue_id: i for i in VALIDATION_ISSUES}
    for issue_id in ("DF-001", "DF-002", "DF-003"):
        assert by_id[issue_id].status == "RESOLVED"


def test_trend_helpers_and_metrics():
    assert len(dogfood_confidence_trend()) == len(DOGFOOD_PROGRESS)
    assert len(dogfood_motivation_trend()) == len(DOGFOOD_PROGRESS)
    assert len(dogfood_completion_trend()) == len(DOGFOOD_PROGRESS)
    consistency = dogfood_study_consistency()
    assert any("NOT MET" in line for line in consistency)
    friction = dogfood_friction_trend()
    assert any("P0 open: 0" in line for line in friction)
    metrics = dogfood_metrics_summary()
    assert metrics["live_sittings"] >= 1
    assert metrics["live_days"] >= 1
    assert metrics["blocked_live_sittings"] >= 1


def test_v1_readiness_snapshot_v1s006():
    snapshot = build_v1_readiness_snapshot()
    assert snapshot.programme in {"V1S-006", "V1S-007", "V1S-008"}
    assert "HOLD" in snapshot.overall_status
    assert snapshot.dogfood_motivation_trend
    assert snapshot.dogfood_completion_trend
    assert snapshot.dogfood_study_consistency
    assert snapshot.dogfood_friction_trend
    open_p0 = [i for i in snapshot.learning_friction_open if i.priority == "P0"]
    assert open_p0 == []
    assert resolved_friction_records() == LEARNING_FRICTION_REGISTER


def test_v1s006_report_exists():
    assert (REPO_ROOT / "V1S006_DOGFOOD_WEEK_REPORT.md").is_file()


def test_v1_readiness_template_has_v1s006_trends():
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
        "Confidence Trend",
        "Motivation Trend",
        "Completion Trend",
        "Study Consistency",
        "Learning Friction Trend",
    ):
        assert label in text, f"Missing template section: {label}"
