"""Seed the evidence catalogue from sealed onboarding declarations.

Produces observational ``EvidenceRecord`` values only. Never diagnoses,
recommends, or invents mastery scores.
"""

from __future__ import annotations

from datetime import datetime

from application.onboarding.results import StudentTwinInitializationRequest
from application.student_initialization.errors import OnboardingValidationError
from application.student_initialization.results import InitialEvidence
from domain.education.evidence import (
    ConfidenceMeasure,
    EvidenceContext,
    EvidenceContextId,
    EvidenceItem,
    EvidenceItemId,
    EvidenceItemKind,
    EvidenceRecord,
    EvidenceSource,
    EvidenceSourceId,
    EvidenceSourceKind,
    EvidenceStrength,
    EvidenceTimestamp,
)
from domain.education.foundation.enums import ConfidenceLevel, LearningDimension
from domain.education.foundation.errors import EducationalDomainError
from domain.education.foundation.ids import EvidenceId

_PROVENANCE_CHANNEL = "onboarding"
_SOURCE_LABEL = "Student onboarding declarations"


def evidence_id_for_onboarding(onboarding_id: str) -> str:
    """Stable evidence identity for idempotent seeding."""
    cleaned = (onboarding_id or "").strip()
    if not cleaned:
        raise OnboardingValidationError("onboarding_id is required")
    return f"evidence-onboarding-{cleaned}"


class EvidenceCatalogueSeeder:
    """Deterministically map onboarding declarations → ``InitialEvidence``."""

    @classmethod
    def seed(
        cls,
        declarations: StudentTwinInitializationRequest,
        *,
        occurred_at: datetime,
    ) -> InitialEvidence:
        """Build the initial evidence catalogue for one completed onboarding.

        Args:
            declarations: Closed Twin initialization cargo from onboarding.
            occurred_at: Timezone-aware timestamp for the evidence record.

        Returns:
            ``InitialEvidence`` containing one observational ``EvidenceRecord``.
        """
        cls._validate_declarations(declarations)
        if not isinstance(occurred_at, datetime) or occurred_at.tzinfo is None:
            raise OnboardingValidationError(
                "occurred_at must be a timezone-aware datetime"
            )

        onboarding_id = declarations.onboarding_id.strip()
        student_id = declarations.student_id.strip()
        evidence_id = evidence_id_for_onboarding(onboarding_id)
        items = cls._build_items(evidence_id, declarations)
        if not items:
            raise OnboardingValidationError(
                "onboarding declarations produced no observational items"
            )

        try:
            record = EvidenceRecord.record(
                evidence_id=EvidenceId(evidence_id),
                student_id=student_id,
                items=items,
                source=EvidenceSource(
                    source_id=EvidenceSourceId(f"source:{evidence_id}"),
                    kind=EvidenceSourceKind.REFLECTION_CAPTURE,
                    label=_SOURCE_LABEL,
                    channel=_PROVENANCE_CHANNEL,
                ),
                context=EvidenceContext(
                    context_id=EvidenceContextId(f"ctx:{evidence_id}"),
                    situation=(
                        "Student onboarding self-report; "
                        f"onboarding_id={onboarding_id}; "
                        f"exam_paper={declarations.exam_paper.strip()}"
                    ),
                    learning_dimension=LearningDimension.UNDERSTANDING,
                ),
                confidence=ConfidenceMeasure.of(ConfidenceLevel.MEDIUM),
                strength=EvidenceStrength.weak(),
                timestamp=EvidenceTimestamp(occurred_at=occurred_at),
            )
        except EducationalDomainError as exc:
            raise OnboardingValidationError(str(exc)) from exc

        return InitialEvidence(
            onboarding_id=onboarding_id,
            student_id=student_id,
            records=(record,),
        )

    @classmethod
    def _validate_declarations(
        cls, declarations: StudentTwinInitializationRequest
    ) -> None:
        if declarations is None or not isinstance(
            declarations, StudentTwinInitializationRequest
        ):
            raise OnboardingValidationError(
                "declarations must be a StudentTwinInitializationRequest"
            )
        if not (declarations.student_id or "").strip():
            raise OnboardingValidationError("student_id is required")
        if not (declarations.onboarding_id or "").strip():
            raise OnboardingValidationError("onboarding_id is required")
        if not (declarations.exam_paper or "").strip():
            raise OnboardingValidationError("exam_paper is required")
        if not declarations.declaration_confirmation:
            raise OnboardingValidationError(
                "declaration_confirmation must be true"
            )

    @classmethod
    def _build_items(
        cls,
        evidence_id: str,
        declarations: StudentTwinInitializationRequest,
    ) -> list[EvidenceItem]:
        observations = (
            f"pathway={declarations.pathway}",
            f"exam_paper={declarations.exam_paper}",
            f"intended_sitting_label={declarations.intended_sitting_label}",
            f"prior_study={declarations.prior_study}",
            f"core_reading={declarations.core_reading}",
            f"previous_attempts={declarations.previous_attempts}",
            f"sitting_intent={declarations.sitting_intent}",
            f"weekday_minutes={declarations.weekday_minutes}",
            f"weekend_minutes={declarations.weekend_minutes}",
            f"preferred_session_minutes={declarations.preferred_session_minutes}",
            f"confidence_band={declarations.confidence_band}",
            f"study_habit_preference={declarations.study_habit_preference}",
            f"typical_start_time={declarations.typical_start_time}",
            f"diagnostic_choice={declarations.diagnostic_choice}",
            f"contract_version={declarations.contract_version}",
        )
        if (declarations.confidence_notes or "").strip():
            observations = (
                *observations,
                f"confidence_notes={declarations.confidence_notes.strip()}",
            )

        items: list[EvidenceItem] = []
        for index, observation in enumerate(observations, start=1):
            text = (observation or "").strip()
            if not text:
                continue
            items.append(
                EvidenceItem(
                    item_id=EvidenceItemId(f"item:{evidence_id}:{index:02d}"),
                    kind=EvidenceItemKind.REFLECTION,
                    observation=text,
                )
            )
        return items
