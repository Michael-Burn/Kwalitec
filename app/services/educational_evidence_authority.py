"""Educational Evidence Authority (EIP-002 + EV-001A / EV-001B).

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

Also validates Student Runtime sitting Evidence Packages (EV-001B) under the
EV-001A Educational Evidence Contract. LearningSessionRuntime may emit
candidates; this Authority alone Accepts or Rejects them.

Observing student behaviour does not automatically produce Educational Evidence.
Correct silence is preferred to artificial educational certainty.

Governing refs:
- Constitution Articles III, V, VIII
- EL-005, EL-006, EL-007
- EDUCATIONAL_EVIDENCE_MODEL.md
- EDUCATIONAL_STATE_AUTHORITY_MATRIX.md
- EDUCATIONAL_EVIDENCE_AUTHORITY.md
- EV001A_EDUCATIONAL_EVIDENCE_CONTRACT.md
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING

from app.models.learning import StudyAttempt

if TYPE_CHECKING:
    from app.application.learning_session.dto.evidence_package import (
        SessionEvidencePackage,
    )


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

    # ------------------------------------------------------------------
    # EV-001A / EV-001B — Session Evidence Package validation
    # ------------------------------------------------------------------

    @staticmethod
    def validate_session_evidence_package(
        package: SessionEvidencePackage,
    ):
        """Validate a sitting Evidence Package under EV-001A.

        Returns one of Accepted / Accepted with Restrictions / Rejected.
        Does not mutate Twin. Does not invent Educational+ grades.

        Grade ceilings and non-authoritative package rules are binding.
        """
        from app.application.learning_session.dto.candidate_observation import (
            TYPE_CEILING_GRADE,
            RuntimeEvidenceType,
        )
        from app.application.learning_session.dto.evidence_package import (
            EvidenceDisposition,
            EvidenceLifecycleState,
            EvidenceValidationResult,
        )

        now = datetime.now(tz=UTC)
        type_ids = package.observation_type_ids()
        finish = (package.finish_review_verdict or "").strip().lower() or None

        if not package.student_id or not package.session_id:
            return EvidenceValidationResult(
                disposition=EvidenceDisposition.REJECTED,
                lifecycle_state=EvidenceLifecycleState.REJECTED,
                may_complete_session=False,
                may_complete_mission=False,
                may_advance_progress=False,
                may_update_twin=False,
                reason="package_missing_attribution",
                student_explanation=(
                    "We could not verify this study sitting. "
                    "Please return to your session and try again."
                ),
                highest_grade="informational",
                validated_at=now,
            )

        grades = [
            TYPE_CEILING_GRADE.get(obs.type_id, "informational")
            for obs in package.observations
        ]
        highest = _highest_grade(grades)

        practice_types = {
            RuntimeEvidenceType.PRACTICE_ATTEMPTED.value,
            RuntimeEvidenceType.PRACTICE_CORRECT.value,
            RuntimeEvidenceType.PRACTICE_INCORRECT.value,
            RuntimeEvidenceType.PRACTICE_PARTIAL_UNSCORED.value,
            RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS.value,
        }
        educational_practice = {
            RuntimeEvidenceType.PRACTICE_CORRECT.value,
            RuntimeEvidenceType.PRACTICE_INCORRECT.value,
            RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS.value,
        }
        reading_types = {
            RuntimeEvidenceType.READING_STARTED.value,
            RuntimeEvidenceType.READING_COMPLETED.value,
        }
        reflection_types = {
            RuntimeEvidenceType.REFLECTION_SUBMITTED.value,
            RuntimeEvidenceType.REFLECTION_SKIPPED.value,
        }
        duration_types = {RuntimeEvidenceType.SESSION_DURATION.value}
        checklist_types = {RuntimeEvidenceType.CHECKLIST_TICKS.value}

        has_practice = bool(type_ids & practice_types)
        has_educational = bool(type_ids & educational_practice)
        has_reading = bool(type_ids & reading_types)
        has_reflection = bool(type_ids & reflection_types)
        has_duration = bool(type_ids & duration_types)
        has_checklist = bool(type_ids & checklist_types)

        # Explicit Partial / No — honest session close; no mission/progress/Twin.
        if finish in {"partially", "no"}:
            return EvidenceValidationResult(
                disposition=EvidenceDisposition.ACCEPTED_WITH_RESTRICTIONS,
                lifecycle_state=EvidenceLifecycleState.ACCEPTED,
                may_complete_session=True,
                may_complete_mission=False,
                may_advance_progress=False,
                may_update_twin=False,
                reason=(
                    "explicit_partial_finish_review"
                    if finish == "partially"
                    else "explicit_no_finish_review"
                ),
                student_explanation=(
                    "Thanks for the honest finish review. Today's session is "
                    "closed. This mission stays open so you can continue when "
                    "you are ready — no progress was claimed."
                ),
                restrictions=(
                    "mission_completion_blocked",
                    "progress_advancement_blocked",
                    "twin_update_forbidden",
                    "mastery_claims_forbidden",
                ),
                highest_grade=highest if grades else "behavioural",
                validated_at=now,
            )

        # Non-authoritative packages (EV-001A C8).
        if has_practice is False:
            if has_reading and not has_reflection:
                return _rejected_non_authoritative(
                    reason="reading_only_package",
                    explanation=(
                        "Reading alone is not enough to complete this mission. "
                        "Continue with practice when you are ready."
                    ),
                    highest=highest,
                    now=now,
                )
            if has_reflection and not has_reading:
                return _rejected_non_authoritative(
                    reason="reflection_only_package",
                    explanation=(
                        "Reflection alone does not complete this mission. "
                        "Return to practice when you are ready."
                    ),
                    highest=highest,
                    now=now,
                )
            if has_duration and not has_reading and not has_reflection:
                return _rejected_non_authoritative(
                    reason="duration_only_package",
                    explanation=(
                        "Time spent studying is not enough to complete this "
                        "mission. Practice is still needed."
                    ),
                    highest=highest,
                    now=now,
                )
            if has_checklist and not has_reading and not has_reflection:
                return _rejected_non_authoritative(
                    reason="checklist_only_package",
                    explanation=(
                        "Checklist ticks alone cannot complete this mission. "
                        "Work through today's practice first."
                    ),
                    highest=highest,
                    now=now,
                )
            # Finish Review Yes alone / empty / objectives-only.
            return _rejected_non_authoritative(
                reason="insufficient_educational_evidence",
                explanation=(
                    "We could not accept educational evidence for this sitting. "
                    "Finish Review confirms honesty, but practice evidence is "
                    "still required before this mission can complete."
                ),
                highest=highest,
                now=now,
            )

        # Practice package — Accepted (Educational+) or Accepted with Restrictions.
        # Twin may update only for Educational+ (SDT-004 / P5). Behavioural
        # practice participation advances mission/progress but not Twin.
        if has_educational:
            return EvidenceValidationResult(
                disposition=EvidenceDisposition.ACCEPTED,
                lifecycle_state=EvidenceLifecycleState.ACCEPTED,
                may_complete_session=True,
                may_complete_mission=True,
                may_advance_progress=True,
                may_update_twin=True,
                reason="educational_practice_accepted",
                student_explanation=(
                    "Your practice evidence was accepted. Today's mission is "
                    "complete and coverage may advance."
                ),
                restrictions=(),
                highest_grade="educational",
                validated_at=now,
            )

        return EvidenceValidationResult(
            disposition=EvidenceDisposition.ACCEPTED_WITH_RESTRICTIONS,
            lifecycle_state=EvidenceLifecycleState.ACCEPTED,
            may_complete_session=True,
            may_complete_mission=True,
            may_advance_progress=True,
            may_update_twin=False,
            reason="practice_participation_accepted",
            student_explanation=(
                "Your practice participation was accepted for today's mission. "
                "Coverage may advance. Mastery estimates stay unchanged."
            ),
            restrictions=(
                "twin_update_forbidden",
                "mastery_claims_forbidden",
                "educational_grade_not_reached",
            ),
            highest_grade=highest if grades else "behavioural",
            validated_at=now,
        )


_GRADE_RANK = {
    "informational": 0,
    "behavioural": 1,
    "educational": 2,
    "mastery": 3,
    "constitutional": 4,
}


def _highest_grade(grades: list[str]) -> str:
    if not grades:
        return "informational"
    return max(grades, key=lambda g: _GRADE_RANK.get(g, 0))


def _rejected_non_authoritative(
    *,
    reason: str,
    explanation: str,
    highest: str,
    now: datetime,
):
    from app.application.learning_session.dto.evidence_package import (
        EvidenceDisposition,
        EvidenceLifecycleState,
        EvidenceValidationResult,
    )

    return EvidenceValidationResult(
        disposition=EvidenceDisposition.REJECTED,
        lifecycle_state=EvidenceLifecycleState.REJECTED,
        may_complete_session=False,
        may_complete_mission=False,
        may_advance_progress=False,
        may_update_twin=False,
        reason=reason,
        student_explanation=explanation,
        restrictions=(
            "mission_completion_blocked",
            "progress_advancement_blocked",
            "twin_update_forbidden",
            "understanding_claims_forbidden",
        ),
        highest_grade=highest,
        validated_at=now,
    )
