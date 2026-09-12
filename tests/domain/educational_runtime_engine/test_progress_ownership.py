"""Study Progress ownership: verified coverage vs prior-knowledge claims."""

from __future__ import annotations

import pytest

from app.domain.educational_runtime_engine.events import (
    EducationalEventRecord,
    EducationalEventType,
)
from app.domain.educational_runtime_engine.progress import (
    ProgressModelSpec,
    ProgressTopicSpec,
    derive_progress,
)


def _model() -> ProgressModelSpec:
    return ProgressModelSpec(
        curriculum_identity="LAW1:2027.1",
        topic_ids=("t1", "t2", "t3"),
        topics=(
            ProgressTopicSpec(topic_id="t1", topic_code="1.1"),
            ProgressTopicSpec(
                topic_id="t2",
                topic_code="1.2",
                prerequisite_ids=("t1",),
            ),
            ProgressTopicSpec(
                topic_id="t3",
                topic_code="2.1",
                prerequisite_ids=("t2",),
            ),
        ),
    )


def _event(
    event_id: str,
    event_type: EducationalEventType,
    topic_id: str,
    *,
    payload: dict | None = None,
) -> EducationalEventRecord:
    return EducationalEventRecord(
        event_id=event_id,
        event_type=event_type,
        user_id=1,
        curriculum_identity="LAW1:2027.1",
        topic_id=topic_id,
        payload=payload or {},
    )


def test_prior_knowledge_claim_is_not_verified_coverage():
    """Self-declared claims are a distinct category from TOPIC_COMPLETED."""
    events = (
        _event(
            "c1",
            EducationalEventType.PRIOR_KNOWLEDGE_CLAIM,
            "t1",
            payload={
                "source": "baseline_self_declared",
                "warrant": "thin_self_declared",
            },
        ),
    )
    progress = derive_progress(_model(), events)
    assert progress.prior_knowledge_claimed_topic_ids == ("t1",)
    assert progress.verified_completed_topic_ids == ()
    assert progress.progressed_topic_ids == ("t1",)
    # Back-compat alias: progressed-past, not verified coverage.
    assert progress.completed_topic_ids == ("t1",)
    assert progress.verified_coverage_ratio == 0.0
    assert progress.coverage_ratio == pytest.approx(1 / 3)
    assert progress.current_topic_id == "t2"


def test_legacy_baseline_topic_completed_reclassified_as_claim():
    """Historical baseline TOPIC_COMPLETED rows reclassify as claims on read."""
    events = (
        _event(
            "legacy1",
            EducationalEventType.TOPIC_COMPLETED,
            "t1",
            payload={
                "source": "baseline_self_declared",
                "warrant": "thin_self_declared",
            },
        ),
    )
    progress = derive_progress(_model(), events)
    assert progress.prior_knowledge_claimed_topic_ids == ("t1",)
    assert progress.verified_completed_topic_ids == ()
    assert progress.progressed_topic_ids == ("t1",)
    assert progress.current_topic_id == "t2"


def test_mission_topic_completed_is_verified_coverage():
    events = (
        _event(
            "m1",
            EducationalEventType.TOPIC_COMPLETED,
            "t1",
            payload={"source": "mission_completion"},
        ),
    )
    progress = derive_progress(_model(), events)
    assert progress.verified_completed_topic_ids == ("t1",)
    assert progress.prior_knowledge_claimed_topic_ids == ()
    assert progress.progressed_topic_ids == ("t1",)
    assert progress.verified_coverage_ratio == pytest.approx(1 / 3)
    assert progress.current_topic_id == "t2"


def test_claim_then_verified_keeps_categories_distinct():
    events = (
        _event(
            "c1",
            EducationalEventType.PRIOR_KNOWLEDGE_CLAIM,
            "t1",
            payload={"source": "baseline_self_declared"},
        ),
        _event(
            "m1",
            EducationalEventType.TOPIC_COMPLETED,
            "t2",
            payload={"source": "mission_completion"},
        ),
    )
    progress = derive_progress(_model(), events)
    assert progress.prior_knowledge_claimed_topic_ids == ("t1",)
    assert progress.verified_completed_topic_ids == ("t2",)
    assert progress.progressed_topic_ids == ("t1", "t2")
    assert progress.current_topic_id == "t3"
