"""Validate TutorExplanation before presentation / persistence.

Rejects invalid explanations explicitly. Never silently repairs or invents
missing educational provenance.
"""

from __future__ import annotations

from collections.abc import Collection

from app.application.intelligent_tutor.explainability.versions import (
    SUPPORTED_DECISION_VERSIONS_FOR_EXPLANATION,
    SUPPORTED_EXPLANATION_VERSIONS,
    SUPPORTED_PLANNING_VERSIONS_FOR_EXPLANATION,
)
from app.domain.intelligent_tutor.explainability.explanation import TutorExplanation
from app.domain.intelligent_tutor.explainability.section import (
    KNOWN_EXPLANATION_SECTION_KINDS,
    ConceptExplanation,
    ExplanationSection,
    LearningObjectiveExplanation,
)

REQUIRED_PROVENANCE_KEYS = frozenset(
    {
        "decision_id",
        "decision_version",
        "twin_version",
        "evidence_bundle_id",
        "educational_observation_ids",
        "reasoning_request_id",
        "assessment_session_id",
        "correlation_id",
        "explanation_version",
    }
)


class ExplanationValidator:
    """Fail-closed validation for Tutor explainability."""

    def __init__(
        self,
        *,
        supported_explanation_versions: Collection[str] | None = None,
        supported_decision_versions: Collection[str] | None = None,
        supported_planning_versions: Collection[str] | None = None,
        existing_request_ids: Collection[str] | None = None,
        expected_twin_version: int | None = None,
        expected_planning_version: str | None = None,
    ) -> None:
        self._supported_explanation_versions = (
            frozenset(supported_explanation_versions)
            if supported_explanation_versions is not None
            else SUPPORTED_EXPLANATION_VERSIONS
        )
        self._supported_decision_versions = (
            frozenset(supported_decision_versions)
            if supported_decision_versions is not None
            else SUPPORTED_DECISION_VERSIONS_FOR_EXPLANATION
        )
        self._supported_planning_versions = (
            frozenset(supported_planning_versions)
            if supported_planning_versions is not None
            else SUPPORTED_PLANNING_VERSIONS_FOR_EXPLANATION
        )
        self._existing_request_ids = frozenset(existing_request_ids or ())
        self._expected_twin_version = expected_twin_version
        self._expected_planning_version = expected_planning_version

    def validate(self, explanation: TutorExplanation) -> TutorExplanation:
        """Validate and return the same explanation, or raise explicitly."""
        if explanation is None:
            from app.domain.intelligent_tutor.explainability.errors import (
                InvalidExplanationSchema,
            )

            raise InvalidExplanationSchema("tutor explanation is null")

        if explanation.explanation_version not in self._supported_explanation_versions:
            from app.domain.intelligent_tutor.explainability.errors import (
                UnsupportedExplanationContract,
            )

            raise UnsupportedExplanationContract(
                f"unsupported explanation version: "
                f"{explanation.explanation_version!r}"
            )

        ctx = explanation.context
        if ctx.decision_version not in self._supported_decision_versions:
            from app.domain.intelligent_tutor.explainability.errors import (
                InvalidDecisionVersion,
            )

            raise InvalidDecisionVersion(
                f"invalid decision version for explanation: {ctx.decision_version!r}"
            )

        if ctx.twin_version < 1 or explanation.twin_version < 1:
            from app.domain.intelligent_tutor.explainability.errors import (
                UnknownTwinVersion,
            )

            raise UnknownTwinVersion(
                f"unknown twin version: {explanation.twin_version!r}"
            )

        if (
            self._expected_twin_version is not None
            and explanation.twin_version != self._expected_twin_version
        ):
            from app.domain.intelligent_tutor.explainability.errors import (
                TwinVersionMismatch,
            )

            raise TwinVersionMismatch(
                f"twin version mismatch: explanation={explanation.twin_version!r} "
                f"expected={self._expected_twin_version!r}"
            )

        if ctx.twin_version != explanation.twin_version:
            from app.domain.intelligent_tutor.explainability.errors import (
                TwinVersionMismatch,
            )

            raise TwinVersionMismatch(
                f"twin version mismatch between context ({ctx.twin_version}) "
                f"and explanation ({explanation.twin_version})"
            )

        planning_version = (ctx.planning_version or "").strip()
        if planning_version:
            if planning_version not in self._supported_planning_versions:
                from app.domain.intelligent_tutor.explainability.errors import (
                    MissionVersionMismatch,
                )

                raise MissionVersionMismatch(
                    f"unsupported mission planning version: {planning_version!r}"
                )
            if (
                self._expected_planning_version is not None
                and planning_version != self._expected_planning_version
            ):
                from app.domain.intelligent_tutor.explainability.errors import (
                    MissionVersionMismatch,
                )

                raise MissionVersionMismatch(
                    f"mission version mismatch: plan={planning_version!r} "
                    f"expected={self._expected_planning_version!r}"
                )

        request_id = ctx.explanation_request_id
        if request_id in self._existing_request_ids:
            from app.domain.intelligent_tutor.explainability.errors import (
                DuplicateExplanationRequest,
            )

            raise DuplicateExplanationRequest(
                f"duplicate explanation request: {request_id!r}"
            )

        if explanation.available and not explanation.sections:
            from app.domain.intelligent_tutor.explainability.errors import (
                IncompleteProvenance,
            )

            raise IncompleteProvenance(
                "available explanation must include at least one section"
            )

        seen: set[str] = set()
        for section in explanation.sections:
            self._validate_section(section, twin_id=explanation.twin_id)
            if section.section_id in seen:
                from app.domain.intelligent_tutor.explainability.errors import (
                    InvalidExplanationSchema,
                )

                raise InvalidExplanationSchema(
                    f"duplicate section: {section.section_id!r}"
                )
            seen.add(section.section_id)

        return explanation

    def _validate_section(
        self, section: ExplanationSection, *, twin_id: str
    ) -> None:
        if section.kind.value not in KNOWN_EXPLANATION_SECTION_KINDS:
            from app.domain.intelligent_tutor.explainability.errors import (
                UnknownExplanationSchema,
            )

            raise UnknownExplanationSchema(
                f"unknown explanation section kind: {section.kind!r}"
            )

        if section.reference.twin_id != twin_id:
            from app.domain.intelligent_tutor.explainability.errors import (
                ExplanationRejected,
            )

            raise ExplanationRejected(
                f"section twin_id mismatch on {section.section_id!r}"
            )

        decision_version = section.reference.decision_version
        if decision_version not in self._supported_decision_versions:
            from app.domain.intelligent_tutor.explainability.errors import (
                InvalidDecisionVersion,
            )

            raise InvalidDecisionVersion(
                f"invalid decision version: {decision_version!r}"
            )

        self._validate_provenance(section)
        self._validate_typed_references(section)

    def _validate_provenance(self, section: ExplanationSection) -> None:
        from app.domain.intelligent_tutor.explainability.errors import (
            IncompleteProvenance,
            MissingProvenance,
        )

        provenance = dict(section.provenance or {})
        missing = [k for k in REQUIRED_PROVENANCE_KEYS if k not in provenance]
        if missing:
            raise IncompleteProvenance(
                f"missing provenance keys {missing} on {section.section_id!r}"
            )

        ref = section.reference
        if not (ref.decision_id or "").strip():
            raise MissingProvenance("missing decision_id")
        if not (ref.decision_version or "").strip():
            raise MissingProvenance("missing decision_version")
        if not (ref.evidence_bundle_id or "").strip():
            raise MissingProvenance("missing evidence_bundle_id")
        if not ref.educational_observation_ids:
            raise MissingProvenance("missing educational_observation_ids")
        if not (ref.reasoning_request_id or "").strip():
            raise MissingProvenance("missing reasoning_request_id")
        if not (ref.assessment_session_id or "").strip():
            raise MissingProvenance("missing assessment_session_id")
        if not (ref.correlation_id or "").strip():
            raise MissingProvenance("missing correlation_id")
        if not (ref.explanation_version or "").strip():
            raise MissingProvenance("missing explanation_version")
        if ref.twin_version < 1:
            raise MissingProvenance("invalid twin_version")

        obs_ids = provenance.get("educational_observation_ids")
        if not isinstance(obs_ids, list | tuple) or not obs_ids:
            raise IncompleteProvenance(
                "provenance educational_observation_ids must be non-empty"
            )

    def _validate_typed_references(self, section: ExplanationSection) -> None:
        if isinstance(section, ConceptExplanation):
            primary = (section.primary_concept_id or "").strip()
            if not primary and not section.concept_ids:
                from app.domain.intelligent_tutor.explainability.errors import (
                    BrokenConceptReference,
                )

                raise BrokenConceptReference(
                    f"broken concept reference on {section.section_id!r}"
                )
        if isinstance(section, LearningObjectiveExplanation):
            lo = (section.primary_learning_objective_id or "").strip()
            if not lo and not section.learning_objective_ids:
                from app.domain.intelligent_tutor.explainability.errors import (
                    BrokenLearningObjectiveReference,
                )

                raise BrokenLearningObjectiveReference(
                    f"missing learning objective on {section.section_id!r}"
                )
