"""Stateless recommendation selection rules for Learning Journeys.

Produces explainable next-step advice. Never claims mastery, never
auto-completes topics, and never invents unsupported competence.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.learning_journey.policies.progression_policy import (
    ProgressionPolicy,
)
from app.domain.learning_journey.entities.journey_progress import (
    EvidenceConfidencePosture,
)
from app.domain.learning_journey.entities.journey_recommendation import (
    RecommendationCertainty,
    RecommendationKind,
)
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.value_objects.journey_state import JourneyState
from app.domain.learning_journey.value_objects.session_state import SessionState


@dataclass(frozen=True)
class RecommendationDecision:
    """Policy decision for the next educational recommendation."""

    kind: RecommendationKind | None
    reason: str
    confidence_explanation: str
    certainty: RecommendationCertainty
    rationale_tags: tuple[str, ...]
    session_id: str | None = None
    objective_id: str | None = None


class RecommendationPolicy:
    """Educational recommendation rules (stateless, deterministic)."""

    @staticmethod
    def decide(journey: LearningJourney) -> RecommendationDecision:
        """Select the next recommendation kind for ``journey``.

        Priority (deterministic):
        1. Terminal / deferred / abandoned → none
        2. READY_FOR_COMPLETION → confirm topic complete
        3. Pending reflection → capture reflection
        4. Active/paused session → continue current session
        5. Paused journey → pause advice (already paused)
        6. Thin/low prior evidence with addressed work → revise/review
        7. Next unaddressed objective → begin next objective
        8. Otherwise attempt practice / continue structure
        """
        if journey.state in {
            JourneyState.COMPLETED,
            JourneyState.ABANDONED,
            JourneyState.ARCHIVED,
        }:
            return RecommendationDecision(
                kind=None,
                reason="Journey is terminal; no further educational advice",
                confidence_explanation=(
                    "No recommendation is issued for terminal journeys"
                ),
                certainty=RecommendationCertainty.CONDITIONAL,
                rationale_tags=("terminal_journey",),
            )

        if journey.state == JourneyState.DEFERRED:
            return RecommendationDecision(
                kind=None,
                reason="Journey is deferred; reactivate before advising work",
                confidence_explanation=(
                    "Advice is withheld while the journey is deferred"
                ),
                certainty=RecommendationCertainty.CONDITIONAL,
                rationale_tags=("deferred_journey",),
            )

        if journey.state == JourneyState.READY_FOR_COMPLETION:
            return RecommendationDecision(
                kind=RecommendationKind.CONFIRM_TOPIC_COMPLETE,
                reason=(
                    "Educational completion criteria are met; "
                    "confirm Topic Complete when appropriate"
                ),
                confidence_explanation=(
                    "Provisional: criteria are structural, not mastery claims"
                ),
                certainty=RecommendationCertainty.PROVISIONAL,
                rationale_tags=("ready_for_completion", "no_mastery_claim"),
            )

        pending = ProgressionPolicy.pending_reflection_sessions(journey)
        if pending:
            session = pending[0]
            return RecommendationDecision(
                kind=RecommendationKind.CAPTURE_REFLECTION,
                reason=(
                    f"Session {session.session_id} is completed and still "
                    "owes a captured reflection"
                ),
                confidence_explanation=(
                    "Suggested: reflection closes the session educationally"
                ),
                certainty=RecommendationCertainty.SUGGESTED,
                rationale_tags=("pending_reflection", "session_complete_not_topic"),
                session_id=session.session_id,
                objective_id=session.objective_id,
            )

        for session in journey.ordered_sessions():
            if session.state in {SessionState.ACTIVE, SessionState.PAUSED}:
                return RecommendationDecision(
                    kind=RecommendationKind.CONTINUE_CURRENT_SESSION,
                    reason=(
                        f"Session {session.session_id} is "
                        f"{session.state.value} and should continue"
                    ),
                    confidence_explanation=(
                        "Suggested: continue in-progress educational work"
                    ),
                    certainty=RecommendationCertainty.SUGGESTED,
                    rationale_tags=("active_session",),
                    session_id=session.session_id,
                    objective_id=session.objective_id,
                )

        if journey.state == JourneyState.PAUSED:
            return RecommendationDecision(
                kind=RecommendationKind.PAUSE_JOURNEY,
                reason="Journey is paused; resume before starting new work",
                confidence_explanation=(
                    "Conditional: pause is an explicit learner posture"
                ),
                certainty=RecommendationCertainty.CONDITIONAL,
                rationale_tags=("journey_paused",),
            )

        # Evidence honesty: thin/low evidence after prior completed work suggests
        # revise/review — never claims mastery deficiency.
        confidence = journey.progress.evidence_confidence
        completed_count = sum(
            1 for s in journey.sessions if s.state == SessionState.COMPLETED
        )
        if completed_count >= 1 and confidence in {
            EvidenceConfidencePosture.THIN,
            EvidenceConfidencePosture.LOW,
            EvidenceConfidencePosture.UNKNOWN,
        }:
            if confidence == EvidenceConfidencePosture.UNKNOWN and completed_count == 0:
                pass
            elif journey.evidence:
                return RecommendationDecision(
                    kind=RecommendationKind.REVISE_EARLIER_EVIDENCE,
                    reason=(
                        "Accumulated evidence confidence is limited; "
                        "revise earlier evidence before advancing claims"
                    ),
                    confidence_explanation=(
                        "Provisional: thin evidence must not imply mastery"
                    ),
                    certainty=RecommendationCertainty.PROVISIONAL,
                    rationale_tags=(
                        "thin_evidence",
                        "no_mastery_claim",
                        "revise_before_advance",
                    ),
                )
            elif completed_count >= 1:
                return RecommendationDecision(
                    kind=RecommendationKind.REVIEW_PREVIOUS_CONCEPT,
                    reason=(
                        "Prior session work exists with little attributed "
                        "evidence; review previous concepts"
                    ),
                    confidence_explanation=(
                        "Suggested: review without claiming understanding gaps"
                    ),
                    certainty=RecommendationCertainty.SUGGESTED,
                    rationale_tags=("review_previous", "no_mastery_claim"),
                )

        next_objective = ProgressionPolicy.next_unaddressed_objective(journey)
        if next_objective is not None:
            return RecommendationDecision(
                kind=RecommendationKind.BEGIN_NEXT_OBJECTIVE,
                reason=(
                    f"Objective {next_objective.objective_id} "
                    f"({next_objective.title}) is next unaddressed"
                ),
                confidence_explanation=(
                    "Suggested: begin the next ordered educational objective"
                ),
                certainty=RecommendationCertainty.SUGGESTED,
                rationale_tags=("next_objective", next_objective.kind.value),
                objective_id=next_objective.objective_id,
            )

        not_started = [
            s
            for s in journey.ordered_sessions()
            if s.state == SessionState.NOT_STARTED
        ]
        if not_started:
            session = not_started[0]
            return RecommendationDecision(
                kind=RecommendationKind.ATTEMPT_PRACTICE,
                reason=(
                    f"Session {session.session_id} is planned and ready to start"
                ),
                confidence_explanation=(
                    "Suggested: attempt planned practice without mastery claims"
                ),
                certainty=RecommendationCertainty.SUGGESTED,
                rationale_tags=("planned_session",),
                session_id=session.session_id,
                objective_id=session.objective_id,
            )

        return RecommendationDecision(
            kind=RecommendationKind.ATTEMPT_PRACTICE,
            reason="No active session; plan further practice within the journey",
            confidence_explanation=(
                "Provisional: further practice is advisory, not Topic Complete"
            ),
            certainty=RecommendationCertainty.PROVISIONAL,
            rationale_tags=("plan_further_work", "no_mastery_claim"),
        )
