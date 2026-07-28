"""RelationshipBuilder — deterministic RelationshipProjection construction.

Projects only approved relationship types from Twin decisions.
Never invents missing relationships or stores independent mastery.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.application.learning_graph.projections.versions import (
    PROJECTION_PROVENANCE_PREFIX,
    PROJECTION_VERSION,
)
from app.domain.learning_graph.projections.context import ProjectionContext
from app.domain.learning_graph.projections.reference import ProjectionReference
from app.domain.learning_graph.projections.relationship import RelationshipProjection
from app.domain.learning_graph.projections.relationship_type import (
    ProjectionRelationshipType,
)
from app.domain.reasoning.decisions.category import DecisionCategory
from app.domain.reasoning.decisions.decision import EducationalDecision


class RelationshipBuilder:
    """Build immutable relationship projections without inventing facts."""

    def __init__(
        self,
        *,
        context: ProjectionContext,
        created_at: datetime | None = None,
    ) -> None:
        self._context = context
        self._created_at = created_at or datetime.now(UTC).replace(tzinfo=None)
        self._seen_ids: set[str] = set()

    @property
    def context(self) -> ProjectionContext:
        return self._context

    @property
    def seen_ids(self) -> frozenset[str]:
        return frozenset(self._seen_ids)

    def build_from_decision(
        self,
        decision: EducationalDecision,
    ) -> tuple[RelationshipProjection, ...]:
        """Derive zero or more relationships from one Twin decision.

        Soft / non-relationship decisions yield an empty tuple (caller may emit
        GraphProjectionSkipped). Never invents prerequisites or dependencies.
        """
        category = decision.category
        if category is DecisionCategory.MASTERY_BELIEF_UPDATE:
            return self._from_mastery(decision)
        if category is DecisionCategory.CONFIDENCE_BELIEF_UPDATE:
            return self._from_confidence(decision)
        if category is DecisionCategory.UNCERTAINTY_PRESERVED:
            return ()
        if category is DecisionCategory.PROVENANCE_RECORDED:
            return ()
        return ()

    def build_explicit(
        self,
        *,
        relationship_type: ProjectionRelationshipType | str,
        from_ref: str,
        to_ref: str,
        decision: EducationalDecision,
        payload: dict[str, Any] | None = None,
    ) -> RelationshipProjection:
        """Build one explicit relationship; reject duplicate ids in this builder."""
        from app.domain.learning_graph.projections.relationship_type import (
            parse_projection_relationship_type,
        )

        rel_type = parse_projection_relationship_type(relationship_type)
        projection_id = self._projection_id(
            relationship_type=rel_type,
            from_ref=from_ref,
            to_ref=to_ref,
            decision_id=decision.decision_id,
        )
        if projection_id in self._seen_ids:
            from app.domain.learning_graph.projections.errors import DuplicateProjection

            raise DuplicateProjection(f"duplicate projection: {projection_id!r}")
        self._seen_ids.add(projection_id)

        context = self._context
        reference = ProjectionReference(
            decision_id=decision.decision_id,
            decision_version=decision.decision_version,
            twin_version=context.twin_version,
            evidence_bundle_id=decision.reference.evidence_bundle_id,
            educational_observation_ids=(
                decision.reference.educational_observation_ids
            ),
            reasoning_request_id=decision.reference.reasoning_request_id,
            assessment_session_id=decision.reference.assessment_session_id,
            correlation_id=decision.reference.correlation_id,
            projection_version=PROJECTION_VERSION,
            twin_id=context.twin_id,
            graph_id=context.graph_id,
            learning_objective_reference=(
                decision.reference.learning_objective_reference
            ),
            concept_reference=decision.reference.concept_reference,
            projection_id=projection_id,
        )
        provenance = {
            "prefix": PROJECTION_PROVENANCE_PREFIX,
            "decision_id": decision.decision_id,
            "decision_version": decision.decision_version,
            "twin_version": context.twin_version,
            "evidence_bundle_id": decision.reference.evidence_bundle_id,
            "educational_observation_ids": list(
                decision.reference.educational_observation_ids
            ),
            "reasoning_request_id": decision.reference.reasoning_request_id,
            "assessment_session_id": decision.reference.assessment_session_id,
            "correlation_id": decision.reference.correlation_id,
            "projection_version": PROJECTION_VERSION,
            "twin_id": context.twin_id,
            "graph_id": context.graph_id,
            "relationship_type": rel_type.value,
        }
        return RelationshipProjection(
            projection_id=projection_id,
            relationship_type=rel_type,
            from_ref=from_ref,
            to_ref=to_ref,
            twin_id=context.twin_id,
            graph_id=context.graph_id,
            reference=reference,
            projection_version=PROJECTION_VERSION,
            created_at=self._created_at,
            decision_id=decision.decision_id,
            twin_decision_ref=decision.decision_id,
            provenance=provenance,
            payload=payload or {},
        )

    def _from_mastery(
        self, decision: EducationalDecision
    ) -> tuple[RelationshipProjection, ...]:
        student_id = self._context.student_id
        concept = (decision.reference.concept_reference or "").strip()
        lo = (decision.reference.learning_objective_reference or "").strip()
        if not concept:
            return ()

        built: list[RelationshipProjection] = []
        # Student ↔ Concept — references Twin decision; no mastery SoT.
        built.append(
            self.build_explicit(
                relationship_type=ProjectionRelationshipType.STUDENT_CONCEPT,
                from_ref=student_id,
                to_ref=concept,
                decision=decision,
                payload={
                    "twin_decision_ref": decision.decision_id,
                    "mastery_link_ref": str(
                        (decision.payload or {}).get("mastery_id") or ""
                    ),
                },
            )
        )
        if lo:
            built.append(
                self.build_explicit(
                    relationship_type=(
                        ProjectionRelationshipType.LEARNING_OBJECTIVE_CONCEPT
                    ),
                    from_ref=lo,
                    to_ref=concept,
                    decision=decision,
                )
            )
            built.append(
                self.build_explicit(
                    relationship_type=(
                        ProjectionRelationshipType.STUDENT_LEARNING_OBJECTIVE
                    ),
                    from_ref=student_id,
                    to_ref=lo,
                    decision=decision,
                )
            )

        # Explicit payload relationships only — never inferred.
        built.extend(self._explicit_structure_from_payload(decision))
        built.extend(self._misconceptions_from_payload(decision))
        return tuple(built)

    def _from_confidence(
        self, decision: EducationalDecision
    ) -> tuple[RelationshipProjection, ...]:
        lo = (decision.reference.learning_objective_reference or "").strip()
        if not lo:
            return ()
        return (
            self.build_explicit(
                relationship_type=(
                    ProjectionRelationshipType.STUDENT_LEARNING_OBJECTIVE
                ),
                from_ref=self._context.student_id,
                to_ref=lo,
                decision=decision,
                payload={"twin_decision_ref": decision.decision_id},
            ),
        )

    def _explicit_structure_from_payload(
        self, decision: EducationalDecision
    ) -> list[RelationshipProjection]:
        payload = dict(decision.payload or {})
        built: list[RelationshipProjection] = []
        concept = (decision.reference.concept_reference or "").strip()

        for related in _string_list(payload.get("related_concepts")):
            if not concept or related == concept:
                continue
            built.append(
                self.build_explicit(
                    relationship_type=ProjectionRelationshipType.CONCEPT_CONCEPT,
                    from_ref=concept,
                    to_ref=related,
                    decision=decision,
                )
            )

        for prereq in _string_list(payload.get("prerequisites")):
            if not concept or prereq == concept:
                continue
            built.append(
                self.build_explicit(
                    relationship_type=ProjectionRelationshipType.PREREQUISITE,
                    from_ref=concept,
                    to_ref=prereq,
                    decision=decision,
                )
            )

        for dep in _string_list(payload.get("dependencies")):
            if not concept or dep == concept:
                continue
            built.append(
                self.build_explicit(
                    relationship_type=ProjectionRelationshipType.DEPENDENCY,
                    from_ref=concept,
                    to_ref=dep,
                    decision=decision,
                )
            )
        return built

    def _misconceptions_from_payload(
        self, decision: EducationalDecision
    ) -> list[RelationshipProjection]:
        payload = dict(decision.payload or {})
        tags = _string_list(payload.get("misconception_tags"))
        if not tags:
            # Also accept provenance-carried misconception indicators.
            tags = _string_list(
                (decision.provenance or {}).get("misconception_tags")
            )
        built: list[RelationshipProjection] = []
        for tag in tags:
            built.append(
                self.build_explicit(
                    relationship_type=(
                        ProjectionRelationshipType.STUDENT_MISCONCEPTION
                    ),
                    from_ref=self._context.student_id,
                    to_ref=tag,
                    decision=decision,
                )
            )
        return built

    def _projection_id(
        self,
        *,
        relationship_type: ProjectionRelationshipType,
        from_ref: str,
        to_ref: str,
        decision_id: str,
    ) -> str:
        return (
            f"gp:{self._context.twin_id}:{decision_id}:"
            f"{relationship_type.value}:{from_ref}:{to_ref}"
        )


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, list | tuple):
        out: list[str] = []
        for item in value:
            text = str(item or "").strip()
            if text and text not in out:
                out.append(text)
        return out
    return []
