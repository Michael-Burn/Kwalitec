"""Progress tracking tests for orchestration."""

from __future__ import annotations

import pytest

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.orchestrator import OrchestrationProgress
from tests.domain.education.orchestrator.conftest import (
    make_started_orchestrator,
)


def test_progress_tracks_advancement() -> None:
    orch = make_started_orchestrator()
    assert orch.progress.completed_stages == 0
    orch.advance()
    assert orch.progress.completed_stages == 1
    assert orch.progress.ratio == pytest.approx(1 / 6)


def test_evidence_collection_points_counted() -> None:
    orch = make_started_orchestrator()
    assert orch.progress.total_evidence_collection_points >= 1
    while orch.progress.evidence_collection_points_reached < 1:
        orch.advance()
    assert orch.progress.evidence_collection_points_reached >= 1


def test_required_sequence_complete_flag() -> None:
    orch = make_started_orchestrator()
    assert not orch.progress.required_sequence_complete
    while not orch.progress.required_sequence_complete:
        orch.advance()
    assert orch.progress.required_sequence_complete


def test_progress_rejects_invalid_bounds() -> None:
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationProgress(
            current_index=0,
            completed_stages=2,
            total_stages=1,
            completed_required_stages=0,
            total_required_stages=1,
            evidence_collection_points_reached=0,
            total_evidence_collection_points=0,
        )


def test_progress_rejects_zero_total() -> None:
    with pytest.raises(EducationalInvariantViolation):
        OrchestrationProgress(
            current_index=0,
            completed_stages=0,
            total_stages=0,
            completed_required_stages=0,
            total_required_stages=0,
            evidence_collection_points_reached=0,
            total_evidence_collection_points=0,
        )


def test_evidence_points_complete_when_none() -> None:
    progress = OrchestrationProgress(
        current_index=0,
        completed_stages=0,
        total_stages=1,
        completed_required_stages=0,
        total_required_stages=1,
        evidence_collection_points_reached=0,
        total_evidence_collection_points=0,
    )
    assert progress.evidence_points_complete


def test_evidence_collection_stages_query() -> None:
    orch = make_started_orchestrator()
    points = orch.evidence_collection_stages()
    assert len(points) >= 1
    assert all(p.is_evidence_collection_point() for p in points)
