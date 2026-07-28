"""Decision generation services for Educational Reasoning Engine (EI-007).

Evaluates and rebuilds explainable educational decisions from published
curriculum, SCI state, Twin beliefs, and evidence references. Does not
mutate curriculum, evidence, or beliefs, and never generates mission text
or student UI copy.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime

from app.application.educational_reasoning_engine.dto import (
    DecisionView,
    EvaluateDecisionsResult,
)
from app.application.educational_reasoning_engine.exceptions import (
    InstanceNotFoundError,
)
from app.application.twin_inference.inference_service import BeliefInferenceService
from app.domain.curriculum_knowledge_graph.value_objects.relationship_type import (
    CkgRelationshipType,
)
from app.domain.educational_reasoning_engine.context import (
    NodeReasoningState,
    ReasoningContext,
)
from app.domain.educational_reasoning_engine.engine import EducationalReasoningEngine
from app.domain.educational_reasoning_engine.version import REASONING_VERSION
from app.domain.twin_inference.learning_state import LearningState
from app.extensions import db
from app.models.curriculum_knowledge_graph import (
    CkgEdge,
    CkgLearningObjective,
    CkgSection,
    CkgSubsection,
    CkgTopic,
)
from app.models.educational_reasoning_engine import EreEducationalDecision
from app.models.student_curriculum_binding import (
    SciCurriculumNodeState,
    SciStudentCurriculumInstance,
)
from app.models.twin_inference import TieNodeBelief


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class DecisionReasoningService:
    """Evaluate, rebuild, and persist educational decisions for an SCI."""

    def __init__(
        self,
        engine: EducationalReasoningEngine | None = None,
        belief_service: BeliefInferenceService | None = None,
    ) -> None:
        self._engine = engine or EducationalReasoningEngine()
        self._belief_service = belief_service or BeliefInferenceService()

    def evaluate_instance(
        self,
        instance_id: str,
        *,
        as_of: datetime | None = None,
        persist: bool = True,
        ensure_beliefs: bool = True,
    ) -> EvaluateDecisionsResult:
        """Generate ordered educational decisions for a Student Curriculum Instance.

        Args:
            instance_id: Student Curriculum Instance id.
            as_of: Reasoning clock (defaults to now); inject for determinism.
            persist: When True, replace ``ere_educational_decisions`` for SCI.
            ensure_beliefs: When True and beliefs are missing, rebuild Twin
                beliefs first (read-only for evidence/curriculum).

        Returns:
            EvaluateDecisionsResult with ranked DecisionViews.

        Raises:
            InstanceNotFoundError: SCI missing.
        """
        instance = self._require_instance(instance_id)
        when = as_of if as_of is not None else _utc_now()
        when = when.replace(tzinfo=None) if when.tzinfo else when

        if ensure_beliefs:
            belief_count = TieNodeBelief.query.filter_by(
                instance_id=instance_id
            ).count()
            if belief_count == 0:
                self._belief_service.rebuild_beliefs(
                    instance_id, as_of=when, project_to_node_state=True
                )

        context = self._build_context(instance, when)
        result = self._engine.evaluate(context)
        views = tuple(DecisionView.from_item(i) for i in result.items)

        if persist:
            self._replace_decisions(instance_id, views, now=when)

        return EvaluateDecisionsResult(
            instance_id=instance_id,
            decision_count=len(views),
            reasoning_version=self._engine.reasoning_version,
            decisions=views,
        )

    def rebuild_decisions(
        self,
        instance_id: str,
        *,
        as_of: datetime | None = None,
        ensure_beliefs: bool = True,
    ) -> EvaluateDecisionsResult:
        """Full recalculation of educational decisions for an SCI.

        Deletes and replaces prior decision rows. Beliefs, evidence, and
        curriculum content are never modified by this method (belief rebuild
        may run separately when ``ensure_beliefs`` finds an empty store).
        """
        return self.evaluate_instance(
            instance_id,
            as_of=as_of,
            persist=True,
            ensure_beliefs=ensure_beliefs,
        )

    @staticmethod
    def _require_instance(instance_id: str) -> SciStudentCurriculumInstance:
        instance = SciStudentCurriculumInstance.query.filter_by(
            instance_id=instance_id
        ).first()
        if instance is None:
            raise InstanceNotFoundError(f"Instance not found: {instance_id}")
        return instance

    def _build_context(
        self,
        instance: SciStudentCurriculumInstance,
        as_of: datetime,
    ) -> ReasoningContext:
        instance_id = instance.instance_id
        node_states = (
            SciCurriculumNodeState.query.filter_by(instance_id=instance_id)
            .order_by(SciCurriculumNodeState.node_stable_id.asc())
            .all()
        )
        beliefs = {
            row.node_stable_id: row
            for row in TieNodeBelief.query.filter_by(instance_id=instance_id).all()
        }
        prereq_map = self._load_prerequisite_map(
            [n.node_stable_id for n in node_states]
        )
        lo_ids = [
            n.node_stable_id
            for n in node_states
            if n.node_kind == "learning_objective"
        ]
        syllabus_index = self._load_syllabus_index(lo_ids)
        difficulty_map = self._load_difficulty_map(
            [n.node_stable_id for n in node_states]
        )

        nodes: list[NodeReasoningState] = []
        for state in node_states:
            belief = beliefs.get(state.node_stable_id)
            evidence_ids: tuple[str, ...] = ()
            if belief is not None:
                try:
                    raw = json.loads(belief.supporting_evidence_json or "[]")
                except json.JSONDecodeError:
                    raw = []
                if isinstance(raw, list):
                    evidence_ids = tuple(str(x) for x in raw if str(x).strip())
            nodes.append(
                NodeReasoningState(
                    node_stable_id=state.node_stable_id,
                    node_kind=state.node_kind,
                    completion_status=state.completion_status,
                    revision_status=state.revision_status,
                    mastery=(
                        float(belief.mastery_level)
                        if belief is not None
                        else float(state.mastery)
                    ),
                    confidence=(
                        float(belief.confidence_score)
                        if belief is not None
                        else float(state.confidence)
                    ),
                    learning_state=(
                        belief.learning_state
                        if belief is not None
                        else LearningState.UNKNOWN.value
                    ),
                    belief_id=belief.belief_id if belief is not None else None,
                    supporting_evidence_ids=evidence_ids,
                    prerequisite_ids=prereq_map.get(state.node_stable_id, ()),
                    syllabus_index=syllabus_index.get(state.node_stable_id, 0),
                    difficulty=difficulty_map.get(state.node_stable_id, "foundational"),
                    last_interaction_at=state.last_interaction_at,
                    attempts=int(state.attempts or 0),
                    total_study_time_minutes=int(state.total_study_time_minutes or 0),
                )
            )

        return ReasoningContext(
            instance_id=instance_id,
            as_of=as_of,
            nodes=tuple(nodes),
            metadata={"edition_id": instance.edition_id},
        )

    @staticmethod
    def _load_prerequisite_map(
        node_ids: list[str],
    ) -> dict[str, tuple[str, ...]]:
        if not node_ids:
            return {}
        rows = (
            CkgEdge.query.filter(
                CkgEdge.from_stable_id.in_(node_ids),
                CkgEdge.relationship_type == CkgRelationshipType.REQUIRES.value,
            )
            .order_by(CkgEdge.from_stable_id.asc(), CkgEdge.to_stable_id.asc())
            .all()
        )
        out: dict[str, list[str]] = {nid: [] for nid in node_ids}
        for row in rows:
            out.setdefault(row.from_stable_id, []).append(row.to_stable_id)
        return {k: tuple(v) for k, v in out.items()}

    @staticmethod
    def _load_syllabus_index(lo_ids: list[str]) -> dict[str, int]:
        """Composite syllabus order from topic/section/subsection/LO display_order."""
        if not lo_ids:
            return {}
        los = CkgLearningObjective.query.filter(
            CkgLearningObjective.stable_id.in_(lo_ids)
        ).all()
        if not los:
            return {nid: idx for idx, nid in enumerate(sorted(lo_ids))}

        subsection_ids = {lo.subsection_stable_id for lo in los}
        subsections = {
            s.stable_id: s
            for s in CkgSubsection.query.filter(
                CkgSubsection.stable_id.in_(subsection_ids)
            ).all()
        }
        section_ids = {s.section_stable_id for s in subsections.values()}
        sections = {
            s.stable_id: s
            for s in CkgSection.query.filter(
                CkgSection.stable_id.in_(section_ids)
            ).all()
        }
        topic_ids = {s.topic_stable_id for s in sections.values()}
        topics = {
            t.stable_id: t
            for t in CkgTopic.query.filter(CkgTopic.stable_id.in_(topic_ids)).all()
        }

        keyed: list[tuple[tuple[int, int, int, int, str], str]] = []
        for lo in los:
            sub = subsections.get(lo.subsection_stable_id)
            sec = sections.get(sub.section_stable_id) if sub else None
            topic = topics.get(sec.topic_stable_id) if sec else None
            key = (
                topic.display_order if topic else 0,
                sec.display_order if sec else 0,
                sub.display_order if sub else 0,
                lo.display_order,
                lo.stable_id,
            )
            keyed.append((key, lo.stable_id))
        keyed.sort()
        return {nid: idx for idx, (_, nid) in enumerate(keyed)}

    @staticmethod
    def _load_difficulty_map(node_ids: list[str]) -> dict[str, str]:
        if not node_ids:
            return {}
        out: dict[str, str] = {}
        for lo in CkgLearningObjective.query.filter(
            CkgLearningObjective.stable_id.in_(node_ids)
        ).all():
            out[lo.stable_id] = lo.difficulty or "foundational"
        for topic in CkgTopic.query.filter(CkgTopic.stable_id.in_(node_ids)).all():
            out[topic.stable_id] = topic.difficulty or "foundational"
        for section in CkgSection.query.filter(
            CkgSection.stable_id.in_(node_ids)
        ).all():
            out[section.stable_id] = section.difficulty or "foundational"
        for sub in CkgSubsection.query.filter(
            CkgSubsection.stable_id.in_(node_ids)
        ).all():
            out[sub.stable_id] = sub.difficulty or "foundational"
        return out

    def _replace_decisions(
        self,
        instance_id: str,
        views: tuple[DecisionView, ...],
        *,
        now: datetime,
    ) -> None:
        EreEducationalDecision.query.filter_by(instance_id=instance_id).delete()
        db.session.flush()
        for view in views:
            db.session.add(self._to_row(view, now=now))
        db.session.commit()

    @staticmethod
    def _to_row(view: DecisionView, *, now: datetime) -> EreEducationalDecision:
        d = view.decision
        return EreEducationalDecision(
            decision_id=d.decision_id,
            instance_id=d.instance_id,
            decision_type=d.decision_type,
            curriculum_target=d.curriculum_target,
            priority=d.priority,
            rank_position=d.rank_position,
            rationale_summary=d.rationale_summary,
            prerequisite_chain_json=json.dumps(
                list(d.prerequisite_chain), sort_keys=True
            ),
            estimated_effort_minutes=d.estimated_effort_minutes,
            expected_educational_outcome=d.expected_educational_outcome,
            supporting_beliefs_json=json.dumps(
                list(d.supporting_belief_ids), sort_keys=True
            ),
            supporting_curriculum_json=json.dumps(
                list(d.supporting_curriculum_refs), sort_keys=True
            ),
            supporting_evidence_json=json.dumps(
                list(d.supporting_evidence_ids), sort_keys=True
            ),
            applied_rules_json=json.dumps(list(d.applied_rule_ids), sort_keys=True),
            explanation_json=json.dumps(view.explanation.to_dict(), sort_keys=True),
            reasoned_at=d.reasoned_at,
            reasoning_version=d.reasoning_version,
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def _row_to_view(row: EreEducationalDecision) -> DecisionView:
        from app.domain.educational_reasoning_engine.decision import EducationalDecision
        from app.domain.educational_reasoning_engine.explanation import (
            DecisionExplanation,
            PriorityCalculation,
            RuleProposalRecord,
        )

        def _load_list(raw: str) -> tuple[str, ...]:
            try:
                data = json.loads(raw or "[]")
            except json.JSONDecodeError:
                data = []
            if not isinstance(data, list):
                return ()
            return tuple(str(x) for x in data if str(x).strip())

        try:
            expl = json.loads(row.explanation_json or "{}")
        except json.JSONDecodeError:
            expl = {}
        if not isinstance(expl, dict):
            expl = {}

        decision = EducationalDecision(
            decision_id=row.decision_id,
            instance_id=row.instance_id,
            decision_type=row.decision_type,
            curriculum_target=row.curriculum_target,
            priority=float(row.priority),
            rank_position=int(row.rank_position),
            rationale_summary=row.rationale_summary,
            prerequisite_chain=_load_list(row.prerequisite_chain_json),
            estimated_effort_minutes=int(row.estimated_effort_minutes),
            expected_educational_outcome=row.expected_educational_outcome,
            supporting_belief_ids=_load_list(row.supporting_beliefs_json),
            supporting_curriculum_refs=_load_list(row.supporting_curriculum_json),
            supporting_evidence_ids=_load_list(row.supporting_evidence_json),
            applied_rule_ids=_load_list(row.applied_rules_json),
            reasoned_at=row.reasoned_at,
            reasoning_version=row.reasoning_version,
        )

        pri_raw = expl.get("priority_calculation") or {}
        rules_raw = expl.get("rule_proposals") or []
        explanation = DecisionExplanation(
            decision_id=row.decision_id,
            contributing_beliefs=tuple(
                str(x) for x in (expl.get("contributing_beliefs") or [])
            ),
            curriculum_dependencies=tuple(
                str(x) for x in (expl.get("curriculum_dependencies") or [])
            ),
            educational_rules_applied=tuple(
                str(x)
                for x in (
                    expl.get("educational_rules_applied")
                    or list(decision.applied_rule_ids)
                )
            ),
            evidence_references=tuple(
                str(x) for x in (expl.get("evidence_references") or [])
            ),
            priority_calculation=PriorityCalculation(
                raw_sum=float(pri_raw.get("raw_sum", row.priority)),
                clamped=float(pri_raw.get("clamped", row.priority)),
                formula=str(
                    pri_raw.get("formula")
                    or "clamp(sum(rule priority_deltas), 0, 1)"
                ),
                components=tuple(str(x) for x in (pri_raw.get("components") or [])),
            ),
            rule_proposals=tuple(
                RuleProposalRecord(
                    rule_id=str(r.get("rule_id", "")),
                    priority_delta=float(r.get("priority_delta", 0)),
                    detail=str(r.get("detail") or ""),
                    supporting_belief_ids=tuple(
                        str(x) for x in (r.get("supporting_belief_ids") or [])
                    ),
                    supporting_curriculum_refs=tuple(
                        str(x) for x in (r.get("supporting_curriculum_refs") or [])
                    ),
                    supporting_evidence_ids=tuple(
                        str(x) for x in (r.get("supporting_evidence_ids") or [])
                    ),
                )
                for r in rules_raw
                if isinstance(r, dict)
            ),
            rationale_summary=str(
                expl.get("rationale_summary") or row.rationale_summary
            ),
            reasoning_version=str(
                expl.get("reasoning_version") or row.reasoning_version
            ),
        )
        return DecisionView(decision=decision, explanation=explanation)


__all__ = ["DecisionReasoningService", "REASONING_VERSION"]
