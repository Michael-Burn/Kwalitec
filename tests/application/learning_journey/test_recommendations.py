"""Tests for recommendation builder and recommendation policy."""

from __future__ import annotations

from app.application.learning_journey.dto.recommendation_result import (
    RecommendationResult,
)
from app.application.learning_journey.policies.recommendation_policy import (
    RecommendationPolicy,
)
from app.application.learning_journey.recommendation_builder import (
    RecommendationBuilder,
)
from app.domain.evidence.evidence_category import EvidenceConfidenceLevel
from app.domain.learning_journey.entities.journey_progress import (
    EvidenceConfidencePosture,
    JourneyProgress,
)
from app.domain.learning_journey.entities.journey_recommendation import (
    RecommendationCertainty,
    RecommendationKind,
)
from app.domain.learning_journey.entities.journey_reflection import (
    JourneyReflection,
)
from app.domain.learning_journey.value_objects.completion_status import CompletionStatus
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState
from tests.application.learning_journey.helpers import (
    NOW,
    make_captured_reflection,
    make_evidence,
    make_journey,
    make_objective,
    make_session,
)


class TestRecommendationPolicy:
    def test_terminal_yields_none(self) -> None:
        decision = RecommendationPolicy.decide(
            make_journey(state=JourneyState.COMPLETED)
        )
        assert decision.kind is None
        assert "terminal" in decision.rationale_tags[0]

    def test_abandoned_yields_none(self) -> None:
        decision = RecommendationPolicy.decide(
            make_journey(state=JourneyState.ABANDONED)
        )
        assert decision.kind is None

    def test_deferred_yields_none(self) -> None:
        decision = RecommendationPolicy.decide(
            make_journey(state=JourneyState.DEFERRED)
        )
        assert decision.kind is None

    def test_ready_for_completion(self) -> None:
        journey = make_journey(state=JourneyState.READY_FOR_COMPLETION)
        decision = RecommendationPolicy.decide(journey)
        assert decision.kind == RecommendationKind.CONFIRM_TOPIC_COMPLETE
        assert "no_mastery_claim" in decision.rationale_tags

    def test_pending_reflection(self) -> None:
        pending = JourneyReflection.create_pending("r1", "sess-1", "journey-1")
        journey = make_journey(
            state=JourneyState.ACTIVE,
            sessions=[
                make_session(
                    "sess-1",
                    state=SessionState.COMPLETED,
                    reflection=pending,
                )
            ],
            reflections=[pending],
        )
        decision = RecommendationPolicy.decide(journey)
        assert decision.kind == RecommendationKind.CAPTURE_REFLECTION
        assert decision.session_id == "sess-1"

    def test_continue_active_session(self) -> None:
        journey = make_journey(
            state=JourneyState.ACTIVE,
            sessions=[make_session(state=SessionState.ACTIVE)],
        )
        decision = RecommendationPolicy.decide(journey)
        assert decision.kind == RecommendationKind.CONTINUE_CURRENT_SESSION

    def test_continue_paused_session(self) -> None:
        journey = make_journey(
            state=JourneyState.ACTIVE,
            sessions=[make_session(state=SessionState.PAUSED)],
        )
        decision = RecommendationPolicy.decide(journey)
        assert decision.kind == RecommendationKind.CONTINUE_CURRENT_SESSION

    def test_paused_journey(self) -> None:
        journey = make_journey(state=JourneyState.PAUSED)
        decision = RecommendationPolicy.decide(journey)
        assert decision.kind == RecommendationKind.PAUSE_JOURNEY

    def test_begin_next_objective(self) -> None:
        journey = make_journey(
            state=JourneyState.ACTIVE,
            objectives=[
                make_objective("obj-1", sequence_index=0),
                make_objective("obj-2", sequence_index=1),
            ],
            sessions=[
                make_session(
                    "sess-1",
                    state=SessionState.COMPLETED,
                    objective_id="obj-1",
                    reflection=make_captured_reflection("r1", "sess-1"),
                )
            ],
            reflections=[make_captured_reflection("r1", "sess-1")],
            evidence=[make_evidence(objective_id="obj-1")],
        )
        # Attach progress with medium confidence so revise path is skipped
        journey = journey.with_progress(
            JourneyProgress.create(
                objectives_total=2,
                objectives_addressed=1,
                sessions_completed=1,
                sessions_planned=1,
                evidence_count=1,
                reflections_captured=1,
                evidence_confidence=EvidenceConfidencePosture.MEDIUM,
                completion_status=CompletionStatus.IN_PROGRESS,
            )
        )
        decision = RecommendationPolicy.decide(journey)
        assert decision.kind == RecommendationKind.BEGIN_NEXT_OBJECTIVE
        assert decision.objective_id == "obj-2"

    def test_revise_thin_evidence(self) -> None:
        journey = make_journey(
            state=JourneyState.ACTIVE,
            objectives=[make_objective()],
            sessions=[
                make_session(
                    "sess-1",
                    state=SessionState.COMPLETED,
                    objective_id="obj-1",
                    reflection=make_captured_reflection("r1", "sess-1"),
                )
            ],
            reflections=[make_captured_reflection("r1", "sess-1")],
            evidence=[
                make_evidence(confidence=EvidenceConfidenceLevel.LOW),
            ],
        )
        journey = journey.with_progress(
            JourneyProgress.create(
                objectives_total=1,
                objectives_addressed=1,
                sessions_completed=1,
                sessions_planned=1,
                evidence_count=1,
                reflections_captured=1,
                evidence_confidence=EvidenceConfidencePosture.THIN,
                completion_status=CompletionStatus.IN_PROGRESS,
            )
        )
        decision = RecommendationPolicy.decide(journey)
        assert decision.kind == RecommendationKind.REVISE_EARLIER_EVIDENCE
        assert "no_mastery_claim" in decision.rationale_tags

    def test_review_when_no_evidence(self) -> None:
        journey = make_journey(
            state=JourneyState.ACTIVE,
            objectives=[make_objective()],
            sessions=[
                make_session(
                    "sess-1",
                    state=SessionState.COMPLETED,
                    objective_id="obj-1",
                    reflection=make_captured_reflection("r1", "sess-1"),
                )
            ],
            reflections=[make_captured_reflection("r1", "sess-1")],
        )
        journey = journey.with_progress(
            JourneyProgress.create(
                objectives_total=1,
                objectives_addressed=1,
                sessions_completed=1,
                sessions_planned=1,
                evidence_count=0,
                reflections_captured=1,
                evidence_confidence=EvidenceConfidencePosture.UNKNOWN,
                completion_status=CompletionStatus.IN_PROGRESS,
            )
        )
        decision = RecommendationPolicy.decide(journey)
        assert decision.kind == RecommendationKind.REVIEW_PREVIOUS_CONCEPT

    def test_attempt_practice_for_planned(self) -> None:
        journey = make_journey(
            state=JourneyState.ACTIVE,
            sessions=[make_session(state=SessionState.NOT_STARTED)],
        )
        decision = RecommendationPolicy.decide(journey)
        assert decision.kind == RecommendationKind.ATTEMPT_PRACTICE

    def test_never_claims_certainty(self) -> None:
        for state in (
            JourneyState.ACTIVE,
            JourneyState.READY_FOR_COMPLETION,
            JourneyState.PAUSED,
        ):
            decision = RecommendationPolicy.decide(make_journey(state=state))
            assert decision.certainty != "certain"
            assert decision.certainty in {
                RecommendationCertainty.SUGGESTED,
                RecommendationCertainty.PROVISIONAL,
                RecommendationCertainty.CONDITIONAL,
            }


class TestRecommendationBuilder:
    def test_build_creates_artefact(self) -> None:
        builder = RecommendationBuilder(
            clock=lambda: NOW,
            id_factory=lambda: "rec-fixed",
        )
        journey = make_journey(
            state=JourneyState.ACTIVE,
            sessions=[make_session(state=SessionState.ACTIVE)],
        )
        result = builder.build(journey)
        assert isinstance(result, RecommendationResult)
        assert result.recommendation is not None
        assert result.recommendation.recommendation_id == "rec-fixed"
        assert result.kind == RecommendationKind.CONTINUE_CURRENT_SESSION

    def test_build_terminal_no_artefact(self) -> None:
        builder = RecommendationBuilder()
        result = builder.build(make_journey(state=JourneyState.COMPLETED))
        assert result.recommendation is None
        assert result.kind is None

    def test_build_and_attach(self) -> None:
        builder = RecommendationBuilder(
            clock=lambda: NOW,
            id_factory=lambda: "rec-1",
        )
        journey = make_journey(
            state=JourneyState.ACTIVE,
            objectives=[make_objective()],
        )
        updated, result = builder.build_and_attach(journey)
        assert len(updated.recommendations) == 1
        assert result.recommendation is not None

    def test_does_not_mutate_original(self) -> None:
        builder = RecommendationBuilder(id_factory=lambda: "rec-1")
        journey = make_journey(state=JourneyState.ACTIVE)
        before = len(journey.recommendations)
        builder.build(journey)
        assert len(journey.recommendations) == before
