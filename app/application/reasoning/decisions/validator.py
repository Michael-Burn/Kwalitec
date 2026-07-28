"""Validate EducationalDecisionSet before Twin application.

Rejects invalid updates explicitly. Never silently repairs malformed decisions.
"""

from __future__ import annotations

from collections.abc import Collection

from app.application.reasoning.decisions.versions import SUPPORTED_DECISION_VERSIONS
from app.domain.reasoning.decisions.category import (
    KNOWN_DECISION_CATEGORIES,
    DecisionCategory,
)
from app.domain.reasoning.decisions.decision import EducationalDecision
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin

REQUIRED_PROVENANCE_KEYS = frozenset(
    {
        "evidence_bundle_id",
        "educational_observation_ids",
        "reasoning_request_id",
        "decision_id",
        "decision_version",
        "assessment_session_id",
        "correlation_id",
    }
)

REQUIRED_TRACEABILITY_KEYS = frozenset(
    {
        "evidence_bundle_id",
        "educational_observation_ids",
        "reasoning_request_id",
        "decision_id",
        "decision_version",
        "assessment_session_id",
        "correlation_id",
        "twin_id",
    }
)


class DecisionValidator:
    """Fail-closed validation for Twin-bound educational decisions."""

    def __init__(
        self,
        *,
        supported_versions: Collection[str] | None = None,
    ) -> None:
        self._supported_versions = (
            frozenset(supported_versions)
            if supported_versions is not None
            else SUPPORTED_DECISION_VERSIONS
        )

    def validate(
        self,
        decision_set: EducationalDecisionSet,
        *,
        twin: StudentDigitalTwin,
    ) -> EducationalDecisionSet:
        """Validate and return the same set, or raise explicitly."""
        if decision_set is None:
            from app.domain.reasoning.decisions.errors import InvalidDecisionSchema

            raise InvalidDecisionSchema("decision_set is null")

        if decision_set.decision_version not in self._supported_versions:
            from app.domain.reasoning.decisions.errors import (
                UnsupportedDecisionVersion,
            )

            raise UnsupportedDecisionVersion(
                f"unsupported decision version: {decision_set.decision_version!r}"
            )

        if decision_set.context.twin_id != twin.twin_id:
            from app.domain.reasoning.decisions.errors import TwinUpdateRejected

            raise TwinUpdateRejected(
                f"decision twin_id {decision_set.context.twin_id!r} "
                f"does not match Twin {twin.twin_id!r}"
            )

        applied = _applied_decision_ids(twin)
        seen_in_set: set[str] = set()
        for decision in decision_set.decisions:
            self._validate_decision(decision, twin=twin, applied=applied)
            if decision.decision_id in seen_in_set:
                from app.domain.reasoning.decisions.errors import DuplicateDecision

                raise DuplicateDecision(
                    f"duplicate decision: {decision.decision_id!r}"
                )
            seen_in_set.add(decision.decision_id)

        return decision_set

    def _validate_decision(
        self,
        decision: EducationalDecision,
        *,
        twin: StudentDigitalTwin,
        applied: frozenset[str],
    ) -> None:
        if decision.category.value not in KNOWN_DECISION_CATEGORIES:
            from app.domain.reasoning.decisions.errors import UnknownDecisionCategory

            raise UnknownDecisionCategory(
                f"unknown decision category: {decision.category!r}"
            )

        if decision.decision_version not in self._supported_versions:
            from app.domain.reasoning.decisions.errors import (
                UnsupportedDecisionVersion,
            )

            raise UnsupportedDecisionVersion(
                f"unsupported decision version: {decision.decision_version!r}"
            )

        if decision.decision_id in applied:
            from app.domain.reasoning.decisions.errors import DuplicateDecision

            raise DuplicateDecision(
                f"decision already applied to Twin: {decision.decision_id!r}"
            )

        if decision.twin_id != twin.twin_id:
            from app.domain.reasoning.decisions.errors import TwinUpdateRejected

            raise TwinUpdateRejected(
                f"decision twin_id mismatch: {decision.twin_id!r}"
            )

        self._validate_provenance(decision)
        self._validate_traceability(decision)
        self._validate_curriculum_refs(decision)

    def _validate_provenance(self, decision: EducationalDecision) -> None:
        from app.domain.reasoning.decisions.errors import BrokenDecisionProvenance

        provenance = dict(decision.provenance or {})
        missing = [k for k in REQUIRED_PROVENANCE_KEYS if k not in provenance]
        if missing:
            raise BrokenDecisionProvenance(
                f"missing provenance keys {missing} on {decision.decision_id!r}"
            )

        if not (decision.reference.evidence_bundle_id or "").strip():
            raise BrokenDecisionProvenance("missing evidence_bundle_id")
        if not decision.reference.educational_observation_ids:
            raise BrokenDecisionProvenance("missing educational_observation_ids")
        if not (decision.reference.reasoning_request_id or "").strip():
            raise BrokenDecisionProvenance("missing reasoning_request_id")
        if not (decision.reference.assessment_session_id or "").strip():
            raise BrokenDecisionProvenance("missing assessment_session_id")
        if not (decision.reference.correlation_id or "").strip():
            raise BrokenDecisionProvenance("missing correlation_id")
        if not (decision.decision_id or "").strip():
            raise BrokenDecisionProvenance("missing decision_id")
        if not (decision.decision_version or "").strip():
            raise BrokenDecisionProvenance("missing decision_version")

        obs_ids = provenance.get("educational_observation_ids")
        if not isinstance(obs_ids, list | tuple) or not obs_ids:
            raise BrokenDecisionProvenance(
                "provenance educational_observation_ids must be non-empty"
            )

    def _validate_traceability(self, decision: EducationalDecision) -> None:
        from app.domain.reasoning.decisions.errors import MissingDecisionTraceability

        trace = dict(decision.traceability or {})
        missing = [k for k in REQUIRED_TRACEABILITY_KEYS if k not in trace]
        if missing:
            raise MissingDecisionTraceability(
                f"missing traceability keys {missing} on {decision.decision_id!r}"
            )

    def _validate_curriculum_refs(self, decision: EducationalDecision) -> None:
        lo = (decision.reference.learning_objective_reference or "").strip()
        if not lo:
            from app.domain.reasoning.decisions.errors import (
                InvalidLearningObjectiveReference,
            )

            raise InvalidLearningObjectiveReference(
                f"missing learning objective on {decision.decision_id!r}"
            )

        if decision.category is DecisionCategory.MASTERY_BELIEF_UPDATE:
            concept = (decision.reference.concept_reference or "").strip()
            if not concept:
                from app.domain.reasoning.decisions.errors import (
                    UnknownConceptReference,
                )

                raise UnknownConceptReference(
                    f"unknown concept for mastery decision {decision.decision_id!r}"
                )
            if (decision.subject_ref or "").strip() != concept:
                from app.domain.reasoning.decisions.errors import InvalidDecisionSchema

                raise InvalidDecisionSchema(
                    "mastery subject_ref must equal concept_reference"
                )


def _applied_decision_ids(twin: StudentDigitalTwin) -> frozenset[str]:
    """Reconstruct previously applied decision ids from Twin reasoning history."""
    ids: set[str] = set()
    for record in twin.reasoning_history:
        for step in record.steps:
            if step.code != "educational_decision_set":
                continue
            raw = step.outputs.get("decision_ids")
            if isinstance(raw, list | tuple):
                ids.update(str(item) for item in raw if item)
            single = step.outputs.get("decision_id")
            if single:
                ids.add(str(single))
    return frozenset(ids)
