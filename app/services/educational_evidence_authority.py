"""Educational Evidence Authority (EIP-002).

Enforces the constitutional chain:

    Educational Activity
         ↓
    Educational Observation
         ↓
    Authorised Educational Evidence (V1.0 catalogue only)
         ↓
    Educational Inference
         ↓
    Twin-owned Estimated Knowledge / Estimated Mastery

Observing student behaviour does not automatically produce Educational Evidence.
Correct silence is preferred to artificial educational certainty.

Governing refs:
- Constitution Articles III, V, VIII
- EL-005, EL-006, EL-007
- EDUCATIONAL_EVIDENCE_MODEL.md
- EDUCATIONAL_STATE_AUTHORITY_MATRIX.md
- EDUCATIONAL_EVIDENCE_AUTHORITY.md
"""

from __future__ import annotations

from enum import Enum

from app.models.learning import StudyAttempt


class AuthorisedEvidenceSource(str, Enum):
    """V1.0 observations permitted to enter Educational Evidence for Twin updates.

    Sources listed here may lawfully inform Estimated Knowledge / Estimated Mastery
    when attributable outcomes exist. Quiz / mock / official exam engines are
    recognised by name for future wiring; they must not be invented here.
    """

    STRUCTURED_QUESTION_RESULTS = "structured_question_results"
    QUIZ_RESULTS = "quiz_results"
    MISSION_ASSESSMENT_RESULTS = "mission_assessment_results"
    MOCK_EXAMINATION_RESULTS = "mock_examination_results"
    OFFICIAL_EXAMINATION_RESULTS = "official_examination_results"


class ObservationKind(str, Enum):
    """Educational observations that must remain historical only (not Twin writers)."""

    TOPIC_MARKED_COMPLETED = "topic_marked_completed"
    MISSION_COMPLETED = "mission_completed"
    READING_COMPLETED = "reading_completed"
    TIME_SPENT_STUDYING = "time_spent_studying"
    CURRENT_LEARNING_CHANGE = "current_learning_change"
    STUDY_PLAN_COMPLETION = "study_plan_completion"
    STUDENT_CONFIDENCE = "student_confidence"
    REFLECTION = "reflection"
    RECOMMENDATION_ACCEPTANCE = "recommendation_acceptance"
    RECOMMENDATION_DISMISSAL = "recommendation_dismissal"


# Minimum accuracy-bearing attempts before Mastered-stage language is lawful.
MIN_AUTHORISED_OBSERVATIONS_FOR_HIGH_MASTERY = 2


class EducationalEvidenceAuthority:
    """Gate for what may update Twin-owned educational estimates."""

    AUTHORISED_V1_SOURCES: frozenset[AuthorisedEvidenceSource] = frozenset(
        AuthorisedEvidenceSource
    )

    FORBIDDEN_OBSERVATION_KINDS: frozenset[ObservationKind] = frozenset(ObservationKind)

    @staticmethod
    def is_authorised_source(source: AuthorisedEvidenceSource | str) -> bool:
        """Return True when *source* is in the V1.0 authorised evidence catalogue."""
        if isinstance(source, AuthorisedEvidenceSource):
            return source in EducationalEvidenceAuthority.AUTHORISED_V1_SOURCES
        try:
            return (
                AuthorisedEvidenceSource(source)
                in EducationalEvidenceAuthority.AUTHORISED_V1_SOURCES
            )
        except ValueError:
            return False

    @staticmethod
    def may_observation_update_twin(kind: ObservationKind | str) -> bool:
        """Unauthorised observations must never write Twin-owned estimates."""
        if isinstance(kind, ObservationKind):
            return kind not in EducationalEvidenceAuthority.FORBIDDEN_OBSERVATION_KINDS
        try:
            return (
                ObservationKind(kind)
                not in EducationalEvidenceAuthority.FORBIDDEN_OBSERVATION_KINDS
            )
        except ValueError:
            return False

    @staticmethod
    def study_attempt_has_structured_question_results(
        attempt: StudyAttempt,
    ) -> bool:
        """True when an attempt carries measurable structured question outcomes.

        Self-reported questions_attempted / questions_correct with a definable
        accuracy percentage are the interim V1.0 Structured Question Results
        pathway. Presence of duration, confidence, or notes alone is not enough.
        """
        return attempt.get_accuracy_percentage() is not None

    @staticmethod
    def collect_authorised_accuracies(
        attempts: list[StudyAttempt],
    ) -> list[float]:
        """Extract accuracies from attempts with authorised question results."""
        results: list[float] = []
        has_results = (
            EducationalEvidenceAuthority.study_attempt_has_structured_question_results
        )
        for attempt in attempts:
            if not has_results(attempt):
                continue
            accuracy = attempt.get_accuracy_percentage()
            if accuracy is not None:
                results.append(accuracy)
        return results

    @staticmethod
    def has_authorised_evidence_for_estimates(
        attempts: list[StudyAttempt],
    ) -> bool:
        """True when at least one V1.0 authorised evidence observation exists."""
        return bool(
            EducationalEvidenceAuthority.collect_authorised_accuracies(attempts)
        )

    @staticmethod
    def may_assign_high_mastery_stage(authorised_observation_count: int) -> bool:
        """High Mastered-stage language requires accumulation (EL-007 / Art. V §5)."""
        return (
            authorised_observation_count
            >= MIN_AUTHORISED_OBSERVATIONS_FOR_HIGH_MASTERY
        )
