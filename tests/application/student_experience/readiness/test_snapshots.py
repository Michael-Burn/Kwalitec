"""Snapshot tests for Exam Readiness Experience (XP-003)."""

from __future__ import annotations

from application.student_experience.readiness import (
    ExamReadinessService,
    ReadinessSnapshotId,
)
from tests.application.student_experience.readiness.conftest import (
    STUDENT_ID,
    FakeReadinessExportProvider,
    make_full_inputs,
)


def test_build_snapshot_projects_compact_fields(
    service: ExamReadinessService,
) -> None:
    view = service.build_readiness(make_full_inputs(), readiness_id="readiness-snap")
    snapshot = service.build_snapshot(
        view,
        snapshot_id=ReadinessSnapshotId("rsnap-001"),
        home_focus_headline="Today's focus is Probability.",
        journey_trajectory_message="You're building a steady study rhythm.",
    )
    assert snapshot.snapshot_id.value == "rsnap-001"
    assert snapshot.student_id == STUDENT_ID
    assert snapshot.readiness_available is True
    assert snapshot.readiness_percent == view.readiness.readiness_percent
    assert snapshot.readiness_category is view.readiness.readiness_category
    assert snapshot.strength_count == len(view.strengths.items)
    assert snapshot.risk_count == len(view.risks.items)
    assert snapshot.action_count == len(view.action_plan.items)
    assert snapshot.milestone_count == len(view.upcoming_milestones.milestones)
    assert snapshot.home_focus_headline == "Today's focus is Probability."
    assert "steady study rhythm" in (snapshot.journey_trajectory_message or "")


def test_deterministic_snapshot_id(service: ExamReadinessService) -> None:
    view = service.build_readiness(make_full_inputs(), readiness_id="readiness-det")
    snapshot = service.build_snapshot(view)
    assert snapshot.snapshot_id.value.startswith("rsnap:readiness-det:")


def test_export_readiness_uses_provider() -> None:
    service = ExamReadinessService(
        readiness_export_provider=FakeReadinessExportProvider()
    )
    view = service.build_readiness(make_full_inputs(), readiness_id="readiness-exp")
    assert service.export_readiness(view) == "export:readiness-exp"


def test_export_without_provider_returns_none(service: ExamReadinessService) -> None:
    view = service.build_readiness(make_full_inputs())
    assert service.export_readiness(view) is None
