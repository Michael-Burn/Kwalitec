"""Pipeline execution coverage for Student Twin Initialization (BR-003)."""

from __future__ import annotations

from application.pipeline import PIPELINE_STAGES
from tests.education_os.application.student_initialization import (
    make_completed,
    make_service,
)


def test_executes_educational_pipeline_end_to_end() -> None:
    service = make_service()
    result = service.initialize(make_completed())

    stages = result.pipeline_result.stages_completed
    assert len(stages) == len(PIPELINE_STAGES)
    assert stages[0] == "analyse_evidence"
    assert stages[-1] == "enrich_recommendations"
    assert result.pipeline_result.mission is not None
    assert result.pipeline_result.study_plan is not None
    assert result.pipeline_result.recommendations is not None
    assert result.pipeline_result.student_experience is not None


def test_idempotent_replay_reruns_pipeline_without_duplicating_twin() -> None:
    service = make_service()
    first = service.initialize(make_completed())
    second = service.initialize(make_completed())

    assert first.idempotent_replay is False
    assert second.idempotent_replay is True
    assert second.twin_id == first.twin_id
    assert second.initial_evidence.primary_evidence_id == (
        first.initial_evidence.primary_evidence_id
    )
    assert len(second.pipeline_result.stages_completed) == len(
        first.pipeline_result.stages_completed
    )
