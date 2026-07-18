"""Validation of Learning Journey state transitions, ordering, and consistency.

Pure domain rules. Deterministic. No persistence or Flask.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.learning_journey.entities.journey_reflection import ReflectionPosture
from app.domain.learning_journey.entities.learning_journey import LearningJourney
from app.domain.learning_journey.entities.learning_session import LearningSession
from app.domain.learning_journey.value_objects.journey_state import (
    JourneyState,
    JourneyTransitionEvent,
    next_journey_state,
)
from app.domain.learning_journey.value_objects.session_state import (
    SessionState,
    SessionTransitionEvent,
    next_session_state,
)


@dataclass(frozen=True)
class ValidationIssue:
    """One validation finding.

    Attributes:
        code: Stable machine-readable issue code.
        message: Human-readable explanation.
        severity: ``error`` blocks; ``warning`` is advisory.
    """

    code: str
    message: str
    severity: str = "error"

    @property
    def is_error(self) -> bool:
        """True when the issue blocks a transition or consistency claim."""
        return self.severity == "error"


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of a validation check."""

    issues: tuple[ValidationIssue, ...] = ()

    @property
    def is_valid(self) -> bool:
        """True when no error-severity issues are present."""
        return not any(i.is_error for i in self.issues)

    @classmethod
    def ok(cls) -> ValidationResult:
        """Empty successful result."""
        return cls(issues=())

    @classmethod
    def failed(cls, *issues: ValidationIssue) -> ValidationResult:
        """Result containing one or more issues."""
        return cls(issues=tuple(issues))


class JourneyValidationService:
    """Validate journey/session transitions, ordering, and aggregate consistency."""

    @staticmethod
    def validate_journey_transition(
        current: JourneyState,
        event: JourneyTransitionEvent,
        *,
        meets_completion_criteria: bool | None = None,
        pending_reflection: bool = False,
    ) -> ValidationResult:
        """Validate a JourneyState transition for ``event``.

        Args:
            current: Current journey state.
            event: Transition event.
            meets_completion_criteria: Required True for COMPLETION_CRITERIA_MET.
            pending_reflection: When True, CONFIRM_TOPIC_COMPLETE is blocked.
        """
        issues: list[ValidationIssue] = []
        nxt = next_journey_state(current, event)
        if nxt is None:
            issues.append(
                ValidationIssue(
                    code="invalid_journey_transition",
                    message=(
                        f"Transition {current.value} + {event.value} is not lawful"
                    ),
                )
            )
            return ValidationResult.failed(*issues)

        if event == JourneyTransitionEvent.COMPLETION_CRITERIA_MET:
            if meets_completion_criteria is False:
                issues.append(
                    ValidationIssue(
                        code="completion_criteria_not_met",
                        message="Cannot move to READY_FOR_COMPLETION without criteria",
                    )
                )
            elif meets_completion_criteria is None:
                issues.append(
                    ValidationIssue(
                        code="completion_criteria_unknown",
                        message=(
                            "Completion criteria must be evaluated "
                            "before transition"
                        ),
                        severity="warning",
                    )
                )

        if event == JourneyTransitionEvent.CONFIRM_TOPIC_COMPLETE:
            if pending_reflection:
                issues.append(
                    ValidationIssue(
                        code="reflection_pending",
                        message=(
                            "Cannot confirm Topic Complete while a "
                            "reflection is pending"
                        ),
                    )
                )
            # Session-complete alone never completes a journey — already enforced
            # by requiring READY_FOR_COMPLETION as the only lawful from-state.

        return (
            ValidationResult.ok()
            if not any(i.is_error for i in issues)
            else ValidationResult.failed(*issues)
        )

    @staticmethod
    def validate_session_transition(
        current: SessionState,
        event: SessionTransitionEvent,
        *,
        parent_journey_state: JourneyState | None = None,
    ) -> ValidationResult:
        """Validate a SessionState transition for ``event``.

        Args:
            current: Current session state.
            event: Transition event.
            parent_journey_state: When provided, enforces journey coupling rules.
        """
        issues: list[ValidationIssue] = []
        nxt = next_session_state(current, event)
        if nxt is None:
            issues.append(
                ValidationIssue(
                    code="invalid_session_transition",
                    message=(
                        f"Transition {current.value} + {event.value} is not lawful"
                    ),
                )
            )
            return ValidationResult.failed(*issues)

        if parent_journey_state is not None:
            if event == SessionTransitionEvent.START_SESSION:
                if parent_journey_state not in {
                    JourneyState.NOT_STARTED,
                    JourneyState.ACTIVE,
                    JourneyState.RESUMED,
                }:
                    issues.append(
                        ValidationIssue(
                            code="journey_not_startable",
                            message=(
                                "Session may only start when journey is "
                                "NOT_STARTED, ACTIVE, or RESUMED"
                            ),
                        )
                    )
            if event == SessionTransitionEvent.FINISH_SESSION:
                if parent_journey_state == JourneyState.PAUSED:
                    issues.append(
                        ValidationIssue(
                            code="journey_paused",
                            message=(
                                "Cannot finish a session while parent journey is PAUSED"
                            ),
                        )
                    )

        return (
            ValidationResult.ok()
            if not any(i.is_error for i in issues)
            else ValidationResult.failed(*issues)
        )

    @staticmethod
    def validate_session_ordering(journey: LearningJourney) -> ValidationResult:
        """Ensure session sequence indexes are unique and non-negative."""
        issues: list[ValidationIssue] = []
        seen: set[int] = set()
        for session in journey.sessions:
            if session.sequence_index < 0:
                issues.append(
                    ValidationIssue(
                        code="negative_sequence_index",
                        message=f"Session {session.session_id} has negative sequence",
                    )
                )
            if session.sequence_index in seen:
                issues.append(
                    ValidationIssue(
                        code="duplicate_sequence_index",
                        message=(
                            f"Duplicate session sequence_index "
                            f"{session.sequence_index}"
                        ),
                    )
                )
            seen.add(session.sequence_index)
            if session.journey_id != journey.journey_id:
                issues.append(
                    ValidationIssue(
                        code="session_journey_mismatch",
                        message=f"Session {session.session_id} journey_id mismatch",
                    )
                )
        return (
            ValidationResult.ok()
            if not issues
            else ValidationResult.failed(*issues)
        )

    @staticmethod
    def validate_objective_ordering(journey: LearningJourney) -> ValidationResult:
        """Ensure objective sequence indexes are unique and topic-aligned."""
        issues: list[ValidationIssue] = []
        seen: set[int] = set()
        for objective in journey.objectives:
            if objective.topic_id != journey.topic_id:
                issues.append(
                    ValidationIssue(
                        code="objective_topic_mismatch",
                        message=(
                            f"Objective {objective.objective_id} topic_id mismatch"
                        ),
                    )
                )
            if objective.sequence_index in seen:
                issues.append(
                    ValidationIssue(
                        code="duplicate_objective_sequence",
                        message=(
                            f"Duplicate objective sequence_index "
                            f"{objective.sequence_index}"
                        ),
                    )
                )
            seen.add(objective.sequence_index)
        return (
            ValidationResult.ok()
            if not issues
            else ValidationResult.failed(*issues)
        )

    @staticmethod
    def validate_consistency(journey: LearningJourney) -> ValidationResult:
        """Validate aggregate relationships and educational consistency rules."""
        issues: list[ValidationIssue] = []

        ordering = JourneyValidationService.validate_session_ordering(journey)
        issues.extend(ordering.issues)
        obj_ordering = JourneyValidationService.validate_objective_ordering(journey)
        issues.extend(obj_ordering.issues)

        session_ids = {s.session_id for s in journey.sessions}
        for evidence in journey.evidence:
            if evidence.journey_id != journey.journey_id:
                issues.append(
                    ValidationIssue(
                        code="evidence_journey_mismatch",
                        message=(
                            f"Evidence {evidence.journey_evidence_id} "
                            "journey_id mismatch"
                        ),
                    )
                )
            if (
                evidence.session_id is not None
                and evidence.session_id not in session_ids
            ):
                issues.append(
                    ValidationIssue(
                        code="evidence_session_unknown",
                        message=(
                            f"Evidence {evidence.journey_evidence_id} references "
                            "unknown session"
                        ),
                    )
                )

        for reflection in journey.reflections:
            if reflection.journey_id != journey.journey_id:
                issues.append(
                    ValidationIssue(
                        code="reflection_journey_mismatch",
                        message=(
                            f"Reflection {reflection.reflection_id} "
                            "journey_id mismatch"
                        ),
                    )
                )
            if reflection.session_id not in session_ids:
                issues.append(
                    ValidationIssue(
                        code="reflection_session_unknown",
                        message=(
                            f"Reflection {reflection.reflection_id} references "
                            "unknown session"
                        ),
                    )
                )

        for recommendation in journey.recommendations:
            if recommendation.journey_id != journey.journey_id:
                issues.append(
                    ValidationIssue(
                        code="recommendation_journey_mismatch",
                        message=(
                            f"Recommendation {recommendation.recommendation_id} "
                            "journey_id mismatch"
                        ),
                    )
                )

        # Session complete ≠ journey complete.
        if journey.state == JourneyState.COMPLETED:
            completed_sessions = [
                s for s in journey.sessions if s.state == SessionState.COMPLETED
            ]
            if len(completed_sessions) == 1 and len(journey.sessions) == 1:
                # Single session alone is insufficient unless criteria flag says so —
                # warn when progress does not meet criteria.
                if not journey.progress.meets_completion_criteria:
                    issues.append(
                        ValidationIssue(
                            code="completed_without_criteria",
                            message=(
                                "Journey COMPLETED without meets_completion_criteria"
                            ),
                        )
                    )

        # Pending reflections on completed sessions.
        for session in journey.sessions:
            if session.state == SessionState.COMPLETED:
                pending = JourneyValidationService._session_reflection_pending(
                    journey, session
                )
                if pending and journey.state == JourneyState.READY_FOR_COMPLETION:
                    issues.append(
                        ValidationIssue(
                            code="pending_reflection_before_completion",
                            message=(
                                f"Session {session.session_id} reflection still pending"
                            ),
                            severity="warning",
                        )
                    )

        if not issues:
            return ValidationResult.ok()
        if any(i.is_error for i in issues):
            return ValidationResult.failed(*issues)
        return ValidationResult(issues=tuple(issues))

    @staticmethod
    def _session_reflection_pending(
        journey: LearningJourney,
        session: LearningSession,
    ) -> bool:
        if (
            session.reflection is not None
            and session.reflection.posture == ReflectionPosture.PENDING
        ):
            return True
        for reflection in journey.reflections:
            if (
                reflection.session_id == session.session_id
                and reflection.posture == ReflectionPosture.PENDING
            ):
                return True
            if (
                reflection.session_id == session.session_id
                and reflection.posture == ReflectionPosture.CAPTURED
            ):
                return False
        # Completed with no reflection artefact at all ⇒ pending owed.
        if session.reflection is None:
            return True
        return session.reflection.posture != ReflectionPosture.CAPTURED
