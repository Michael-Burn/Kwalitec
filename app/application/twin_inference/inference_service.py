"""Belief generation services for Twin Inference Engine (EI-006).

Infers and rebuilds explainable beliefs from Learning Evidence without
mutating evidence history, curriculum content, or generating recommendations.
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime

from app.application.twin_inference.dto import (
    BeliefView,
    KnowledgeStateView,
    RebuildBeliefsResult,
)
from app.application.twin_inference.exceptions import (
    InstanceNotFoundError,
    NodeNotFoundError,
)
from app.domain.curriculum_knowledge_graph.value_objects.relationship_type import (
    CkgRelationshipType,
)
from app.domain.learning_evidence.evidence_event import EvidenceEvent
from app.domain.twin_inference.engine import TwinInferenceEngine
from app.domain.twin_inference.knowledge_state import aggregate_knowledge_state
from app.domain.twin_inference.version import INFERENCE_VERSION
from app.extensions import db
from app.models.curriculum_knowledge_graph import CkgEdge
from app.models.learning_evidence import LeeEvidenceEvent
from app.models.student_curriculum_binding import (
    SciCurriculumNodeState,
    SciStudentCurriculumInstance,
)
from app.models.twin_inference import TieNodeBelief


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class BeliefInferenceService:
    """Infer, rebuild, and project Twin beliefs for an SCI."""

    def __init__(self, engine: TwinInferenceEngine | None = None) -> None:
        self._engine = engine or TwinInferenceEngine()

    def infer_node_belief(
        self,
        instance_id: str,
        node_stable_id: str,
        *,
        as_of: datetime | None = None,
        persist: bool = True,
        project_to_node_state: bool = True,
    ) -> BeliefView:
        """Infer belief for one curriculum node from its evidence history.

        Args:
            instance_id: Student Curriculum Instance id.
            node_stable_id: Curriculum node within the instance.
            as_of: Inference clock (defaults to now); inject for determinism.
            persist: When True, upsert ``tie_node_beliefs``.
            project_to_node_state: When True, write mastery/confidence onto
                ``SciCurriculumNodeState`` (educational state slots only).

        Returns:
            BeliefView with belief + explanation.

        Raises:
            InstanceNotFoundError: SCI missing.
            NodeNotFoundError: Node not in SCI.
        """
        instance = self._require_instance(instance_id)
        node_state = SciCurriculumNodeState.query.filter_by(
            instance_id=instance_id,
            node_stable_id=node_stable_id,
        ).first()
        if node_state is None:
            raise NodeNotFoundError(
                f"Node {node_stable_id} not in instance {instance_id}"
            )

        when = as_of if as_of is not None else _utc_now()
        when = when.replace(tzinfo=None) if when.tzinfo else when
        evidence = self._load_node_evidence(instance_id, node_stable_id)
        prereq_map = self._prerequisite_mastery(instance_id, node_stable_id)

        existing = TieNodeBelief.query.filter_by(
            instance_id=instance_id,
            node_stable_id=node_stable_id,
        ).first()
        belief_id = existing.belief_id if existing else f"tie-{uuid.uuid4().hex[:16]}"

        result = self._engine.infer_node_belief(
            belief_id=belief_id,
            instance_id=instance_id,
            node_stable_id=node_stable_id,
            evidence=evidence,
            as_of=when,
            prerequisite_mastery=prereq_map,
        )
        view = BeliefView.from_result(result)

        if persist:
            self._upsert_belief(existing, view, now=when)
            if project_to_node_state:
                node_state.mastery = view.belief.mastery_level
                node_state.confidence = view.belief.confidence_score
                node_state.updated_at = when
            db.session.commit()

        # Silence unused binding warning when persist is False.
        _ = instance
        return view

    def rebuild_beliefs(
        self,
        instance_id: str,
        *,
        as_of: datetime | None = None,
        project_to_node_state: bool = True,
    ) -> RebuildBeliefsResult:
        """Full recalculation of beliefs for every node in the SCI.

        Deletes and replaces prior belief rows for the instance. Evidence
        events are never modified.
        """
        instance = self._require_instance(instance_id)
        when = as_of if as_of is not None else _utc_now()
        when = when.replace(tzinfo=None) if when.tzinfo else when

        node_states = (
            SciCurriculumNodeState.query.filter_by(instance_id=instance_id)
            .order_by(SciCurriculumNodeState.node_stable_id.asc())
            .all()
        )

        # Clear prior derived beliefs (recalculation).
        TieNodeBelief.query.filter_by(instance_id=instance_id).delete()
        db.session.flush()

        # Infer leaves/all nodes in stable order. Two-pass for prerequisites:
        # first pass without prereq caps, second pass with projected mastery.
        first_pass: dict[str, BeliefView] = {}
        all_evidence = self._load_instance_evidence(instance_id)
        by_node: dict[str, list[EvidenceEvent]] = {}
        for event in all_evidence:
            by_node.setdefault(event.node_stable_id, []).append(event)

        for node in node_states:
            evidence = tuple(by_node.get(node.node_stable_id, ()))
            belief_id = f"tie-{uuid.uuid4().hex[:16]}"
            result = self._engine.infer_node_belief(
                belief_id=belief_id,
                instance_id=instance_id,
                node_stable_id=node.node_stable_id,
                evidence=evidence,
                as_of=when,
                prerequisite_mastery={},
            )
            first_pass[node.node_stable_id] = BeliefView.from_result(result)

        mastery_lookup = {
            nid: v.belief.mastery_level for nid, v in first_pass.items()
        }
        views: list[BeliefView] = []
        for node in node_states:
            evidence = tuple(by_node.get(node.node_stable_id, ()))
            prereq_ids = self._prerequisite_ids(node.node_stable_id)
            prereq_map = {
                pid: mastery_lookup.get(pid, 0.0) for pid in prereq_ids
            }
            # Preserve stable belief_id from first pass for explainability continuity.
            prior = first_pass[node.node_stable_id]
            result = self._engine.infer_node_belief(
                belief_id=prior.belief.belief_id,
                instance_id=instance_id,
                node_stable_id=node.node_stable_id,
                evidence=evidence,
                as_of=when,
                prerequisite_mastery=prereq_map,
            )
            view = BeliefView.from_result(result)
            self._upsert_belief(None, view, now=when)
            if project_to_node_state:
                node.mastery = view.belief.mastery_level
                node.confidence = view.belief.confidence_score
                node.updated_at = when
            views.append(view)

        db.session.commit()
        _ = instance
        return RebuildBeliefsResult(
            instance_id=instance_id,
            belief_count=len(views),
            inference_version=self._engine.inference_version,
            beliefs=tuple(views),
        )

    def infer_subject_knowledge_state(
        self,
        instance_id: str,
        *,
        as_of: datetime | None = None,
        rebuild_if_empty: bool = True,
    ) -> KnowledgeStateView:
        """Subject-level knowledge state from persisted (or rebuilt) beliefs."""
        instance = self._require_instance(instance_id)
        when = as_of if as_of is not None else _utc_now()
        when = when.replace(tzinfo=None) if when.tzinfo else when

        rows = (
            TieNodeBelief.query.filter_by(instance_id=instance_id)
            .order_by(TieNodeBelief.node_stable_id.asc())
            .all()
        )
        if not rows and rebuild_if_empty:
            rebuilt = self.rebuild_beliefs(instance_id, as_of=when)
            return KnowledgeStateView(
                state=aggregate_knowledge_state(
                    instance_id=instance_id,
                    subject_code=instance.subject_code,
                    beliefs=[v.belief for v in rebuilt.beliefs],
                    inferred_at=when,
                    inference_version=self._engine.inference_version,
                ),
                node_summaries=rebuilt.beliefs,
            )

        views = tuple(self._row_to_view(row) for row in rows)
        state = aggregate_knowledge_state(
            instance_id=instance_id,
            subject_code=instance.subject_code,
            beliefs=[v.belief for v in views],
            inferred_at=when,
            inference_version=self._engine.inference_version,
        )
        return KnowledgeStateView(state=state, node_summaries=views)

    @staticmethod
    def _require_instance(instance_id: str) -> SciStudentCurriculumInstance:
        instance = SciStudentCurriculumInstance.query.filter_by(
            instance_id=instance_id
        ).first()
        if instance is None:
            raise InstanceNotFoundError(f"Instance not found: {instance_id}")
        return instance

    def _load_node_evidence(
        self, instance_id: str, node_stable_id: str
    ) -> tuple[EvidenceEvent, ...]:
        rows = (
            LeeEvidenceEvent.query.filter_by(
                instance_id=instance_id,
                node_stable_id=node_stable_id,
            )
            .order_by(
                LeeEvidenceEvent.occurred_at.asc(),
                LeeEvidenceEvent.id.asc(),
            )
            .all()
        )
        return tuple(self._to_event(row) for row in rows)

    def _load_instance_evidence(
        self, instance_id: str
    ) -> tuple[EvidenceEvent, ...]:
        rows = (
            LeeEvidenceEvent.query.filter_by(instance_id=instance_id)
            .order_by(
                LeeEvidenceEvent.occurred_at.asc(),
                LeeEvidenceEvent.id.asc(),
            )
            .all()
        )
        return tuple(self._to_event(row) for row in rows)

    @staticmethod
    def _to_event(row: LeeEvidenceEvent) -> EvidenceEvent:
        try:
            metadata = json.loads(row.metadata_json or "{}")
        except json.JSONDecodeError:
            metadata = {}
        if not isinstance(metadata, dict):
            metadata = {}
        return EvidenceEvent(
            evidence_id=row.evidence_id,
            instance_id=row.instance_id,
            node_stable_id=row.node_stable_id,
            evidence_type=row.evidence_type,
            occurred_at=row.occurred_at,
            source=row.source,
            recorded_at=row.recorded_at,
            metadata=metadata,
            corrects_evidence_id=row.corrects_evidence_id,
        )

    def _prerequisite_ids(self, node_stable_id: str) -> tuple[str, ...]:
        rows = (
            CkgEdge.query.filter_by(
                from_stable_id=node_stable_id,
                relationship_type=CkgRelationshipType.REQUIRES.value,
            )
            .order_by(CkgEdge.to_stable_id.asc())
            .all()
        )
        return tuple(r.to_stable_id for r in rows)

    def _prerequisite_mastery(
        self, instance_id: str, node_stable_id: str
    ) -> dict[str, float]:
        prereq_ids = self._prerequisite_ids(node_stable_id)
        if not prereq_ids:
            return {}
        # Prefer persisted beliefs; fall back to SCI node-state mastery.
        out: dict[str, float] = {}
        for pid in prereq_ids:
            belief = TieNodeBelief.query.filter_by(
                instance_id=instance_id, node_stable_id=pid
            ).first()
            if belief is not None:
                out[pid] = float(belief.mastery_level)
                continue
            state = SciCurriculumNodeState.query.filter_by(
                instance_id=instance_id, node_stable_id=pid
            ).first()
            out[pid] = float(state.mastery) if state is not None else 0.0
        return out

    def _upsert_belief(
        self,
        existing: TieNodeBelief | None,
        view: BeliefView,
        *,
        now: datetime,
    ) -> TieNodeBelief:
        payload_evidence = json.dumps(
            list(view.belief.supporting_evidence_ids), sort_keys=True
        )
        payload_explanation = json.dumps(
            view.explanation.to_dict(), sort_keys=True
        )
        if existing is None:
            # May already exist by belief_id after rebuild delete+insert path.
            existing = TieNodeBelief.query.filter_by(
                belief_id=view.belief.belief_id
            ).first()
        if existing is None:
            existing = TieNodeBelief.query.filter_by(
                instance_id=view.belief.instance_id,
                node_stable_id=view.belief.node_stable_id,
            ).first()
        if existing is None:
            row = TieNodeBelief(
                belief_id=view.belief.belief_id,
                instance_id=view.belief.instance_id,
                node_stable_id=view.belief.node_stable_id,
                mastery_level=view.belief.mastery_level,
                confidence_score=view.belief.confidence_score,
                learning_state=view.belief.learning_state,
                supporting_evidence_json=payload_evidence,
                rationale_summary=view.belief.rationale_summary,
                explanation_json=payload_explanation,
                inference_timestamp=view.belief.inference_timestamp,
                inference_version=view.belief.inference_version,
                created_at=now,
                updated_at=now,
            )
            db.session.add(row)
            return row

        existing.mastery_level = view.belief.mastery_level
        existing.confidence_score = view.belief.confidence_score
        existing.learning_state = view.belief.learning_state
        existing.supporting_evidence_json = payload_evidence
        existing.rationale_summary = view.belief.rationale_summary
        existing.explanation_json = payload_explanation
        existing.inference_timestamp = view.belief.inference_timestamp
        existing.inference_version = view.belief.inference_version
        existing.updated_at = now
        return existing

    @staticmethod
    def _row_to_view(row: TieNodeBelief) -> BeliefView:
        from app.domain.twin_inference.belief import TwinBelief
        from app.domain.twin_inference.explanation import (
            BeliefExplanation,
            ConfidenceCalculation,
            RuleContributionRecord,
        )

        try:
            evidence = json.loads(row.supporting_evidence_json or "[]")
        except json.JSONDecodeError:
            evidence = []
        if not isinstance(evidence, list):
            evidence = []
        try:
            expl = json.loads(row.explanation_json or "{}")
        except json.JSONDecodeError:
            expl = {}
        if not isinstance(expl, dict):
            expl = {}

        belief = TwinBelief(
            belief_id=row.belief_id,
            instance_id=row.instance_id,
            node_stable_id=row.node_stable_id,
            mastery_level=float(row.mastery_level),
            confidence_score=float(row.confidence_score),
            learning_state=row.learning_state,
            supporting_evidence_ids=tuple(str(x) for x in evidence),
            inference_timestamp=row.inference_timestamp,
            inference_version=row.inference_version,
            rationale_summary=row.rationale_summary,
        )

        conf_raw = expl.get("confidence_calculation") or {}
        mast_raw = expl.get("mastery_calculation")
        rules_raw = expl.get("contributing_rules") or []
        explanation = BeliefExplanation(
            belief_id=row.belief_id,
            supporting_evidence_ids=tuple(
                str(x) for x in (expl.get("supporting_evidence_ids") or evidence)
            ),
            contributing_rules=tuple(
                RuleContributionRecord(
                    rule_id=str(r.get("rule_id", "")),
                    mastery_delta=float(r.get("mastery_delta", 0)),
                    confidence_delta=float(r.get("confidence_delta", 0)),
                    weight=float(r.get("weight", 1)),
                    evidence_ids=tuple(str(x) for x in (r.get("evidence_ids") or [])),
                    detail=str(r.get("detail") or ""),
                )
                for r in rules_raw
                if isinstance(r, dict)
            ),
            confidence_calculation=ConfidenceCalculation(
                raw_sum=float(conf_raw.get("raw_sum", 0)),
                clamped=float(conf_raw.get("clamped", row.confidence_score)),
                formula=str(
                    conf_raw.get("formula")
                    or "clamp(sum(weighted confidence deltas), 0, 1)"
                ),
                components=tuple(str(x) for x in (conf_raw.get("components") or [])),
            ),
            mastery_calculation=(
                ConfidenceCalculation(
                    raw_sum=float(mast_raw.get("raw_sum", 0)),
                    clamped=float(mast_raw.get("clamped", row.mastery_level)),
                    formula=str(
                        mast_raw.get("formula")
                        or "clamp(sum(weighted mastery deltas), 0, 1)"
                    ),
                    components=tuple(
                        str(x) for x in (mast_raw.get("components") or [])
                    ),
                )
                if isinstance(mast_raw, dict)
                else None
            ),
            inference_rationale=str(
                expl.get("inference_rationale") or row.rationale_summary
            ),
            inference_version=str(
                expl.get("inference_version") or row.inference_version
            ),
            learning_state_reason=str(expl.get("learning_state_reason") or ""),
        )
        return BeliefView(belief=belief, explanation=explanation)


# Avoid unused import lint for INFERENCE_VERSION re-export convenience.
__all__ = ["BeliefInferenceService", "INFERENCE_VERSION"]
