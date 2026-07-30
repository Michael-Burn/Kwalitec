"""Generation 5 — Objective Intelligence Agent.

Associates learning objectives, competencies, knowledge statements, and
exam expectations via ObjectivePolicy with evidence grades.
"""

from __future__ import annotations

from dataclasses import replace

from app.application.curriculum_intelligence.agents.base import (
    CurriculumIntelligenceAgent,
    record_educational_decisions,
    utc_now_iso,
)
from app.application.curriculum_intelligence.generation_hash import (
    compute_generation_hash,
    stable_id,
)
from app.application.curriculum_intelligence.generation_quality import (
    compute_quality_snapshot,
)
from app.application.curriculum_intelligence.mock_generation_runners import (
    GenerationRunContext,
)
from app.application.curriculum_intelligence.policies.objective_policy import (
    ObjectivePolicy,
)
from app.domain.curriculum_intelligence.agent import (
    STANDARD_QUALITY_METRICS,
    AgentDescriptor,
)
from app.domain.curriculum_intelligence.confidence import (
    ConfidenceRecord,
    confidence_band_from_score,
)
from app.domain.curriculum_intelligence.evidence import (
    EvidenceGrade,
    evidence_grade_weight,
)
from app.domain.curriculum_intelligence.generation import (
    CurriculumGenerationSnapshot,
    EducationalNode,
    Generation,
    LineageOperation,
    LineageOperationKind,
    SnapshotStatus,
    purpose_for_index,
)

_AGENT_VERSION = "1.0.0"
_DESCRIPTOR = AgentDescriptor(
    agent_id="objective_intelligence_agent",
    name="ObjectiveIntelligenceAgent",
    purpose="objective_intelligence",
    consumes=("curriculum_generation_snapshot",),
    produces=("curriculum_generation_snapshot", "objective_attachments"),
    dependencies=("concept_formation_agent", "objective_policy"),
    version=_AGENT_VERSION,
    deterministic=True,
    supports_rollback=True,
    quality_metrics_produced=STANDARD_QUALITY_METRICS,
)


class ObjectiveIntelligenceAgent(CurriculumIntelligenceAgent):
    """Generation 5 — attach educational associations to concepts/objectives."""

    generation_index = 5

    def __init__(self, *, policy: ObjectivePolicy | None = None) -> None:
        self._policy = policy or ObjectivePolicy()

    @property
    def descriptor(self) -> AgentDescriptor:
        return _DESCRIPTOR

    def execute(self, context: GenerationRunContext) -> CurriculumGenerationSnapshot:
        if context.prior_snapshot is None:
            raise ValueError(
                "ObjectiveIntelligenceAgent requires a prior Gen 4 snapshot."
            )
        prior = context.prior_snapshot
        created_at = context.fixed_created_at_iso or utc_now_iso()
        generation_id = stable_id(
            "gen",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
            "g5",
        )
        snapshot_id = stable_id(
            "snap",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
            "g5",
        )

        plan = self._policy.plan(
            prior.nodes, decision_prefix=f"obj-{generation_id[-8:]}"
        )
        by_node: dict[str, list] = {}
        for attachment in plan.attachments:
            by_node.setdefault(attachment.node_id, []).append(attachment)

        nodes: list[EducationalNode] = []
        for node in prior.nodes:
            if not node.active:
                nodes.append(node)
                continue
            attachments = by_node.get(node.node_id, [])
            if not attachments:
                grade = node.evidence_grade or (
                    EvidenceGrade.A if node.lineage.syllabus_refs else EvidenceGrade.B
                )
                nodes.append(
                    replace(
                        node,
                        evidence_grade=grade,
                        policy_id=node.policy_id or self._policy.policy_id,
                    )
                )
                continue

            attrs = list(node.attributes)
            best_grade = node.evidence_grade or EvidenceGrade.D
            best_conf = node.confidence.score
            syllabus_refs = list(node.lineage.syllabus_refs)
            evidence_refs: list[str] = []
            for att in attachments:
                attrs.append((f"obj:{att.kind.value}", att.label[:240]))
                attrs.append((f"obj_grade:{att.kind.value}", att.evidence_grade.value))
                attrs.append((f"obj_decision:{att.kind.value}", att.decision_id))
                if att.syllabus_ref and att.syllabus_ref not in syllabus_refs:
                    syllabus_refs.append(att.syllabus_ref)
                evidence_refs.extend(att.evidence_refs)
                if evidence_grade_weight(att.evidence_grade) >= evidence_grade_weight(
                    best_grade
                ):
                    best_grade = att.evidence_grade
                best_conf = max(best_conf, att.confidence)

            attrs.append(("policy_id", self._policy.policy_id))
            attrs.append(("objective_attachment_count", str(len(attachments))))

            op = LineageOperation(
                operation_id=stable_id("op", node.node_id, generation_id, "obj"),
                kind=LineageOperationKind.ROLE_CHANGED,
                generation_id=generation_id,
                generation_index=5,
                reason_code="objective:attached",
                reason_label=(
                    f"Attached {len(attachments)} educational associations "
                    f"via {self._policy.policy_id}"
                ),
                related_node_ids=(),
                evidence_refs=tuple(dict.fromkeys(evidence_refs)),
                confidence=best_conf,
                created_at_iso=created_at,
            )
            lineage = replace(
                node.lineage.with_appended(op),
                syllabus_refs=tuple(syllabus_refs),
            )
            conf = ConfidenceRecord(
                confidence_id=f"conf-{node.node_id}-g5",
                subject_kind="educational_node",
                subject_id=node.node_id,
                score=best_conf,
                band=confidence_band_from_score(best_conf),
                reason="objective_intelligence",
                factors=(),
                needs_review=best_conf < 0.6,
                review_threshold=0.6,
                provenance_id=node.provenance_id,
            )
            nodes.append(
                replace(
                    node,
                    confidence=conf,
                    lineage=lineage,
                    attributes=tuple(attrs),
                    evidence_grade=best_grade,
                    policy_id=self._policy.policy_id,
                )
            )

        node_tuple = tuple(nodes)
        metrics = compute_quality_snapshot(
            node_tuple, rejected_count=len(prior.rejected_nodes)
        )
        # Objective density should not decrease coverage; boost via attributes count.
        calibration_id = (
            context.calibration_profile.profile_id
            if context.calibration_profile
            else prior.generation.calibration_profile_id
        )
        generation_hash = compute_generation_hash(
            source_document_ids=context.source_document_ids,
            parent_snapshot_hash=prior.generation_hash,
            calibration_profile_id=calibration_id,
            agent_id=self.descriptor.agent_id,
            agent_version=self.descriptor.version,
            generation_index=5,
            nodes=node_tuple,
        )
        generation = Generation(
            generation_id=generation_id,
            chain_id=context.chain_id,
            generation_index=5,
            purpose=purpose_for_index(5),
            parent_generation_ids=(prior.generation_id,),
            source_document_ids=context.source_document_ids,
            workspace_id=context.workspace_id,
            created_at_iso=created_at,
            calibration_profile_id=calibration_id,
        )
        record_educational_decisions(
            context,
            plan.decisions,
            generation_index=5,
            generation_id=generation_id,
            agent_id=self.descriptor.agent_id,
            created_at_iso=created_at,
            snapshot_id=snapshot_id,
        )
        return CurriculumGenerationSnapshot(
            snapshot_id=snapshot_id,
            generation=generation,
            nodes=node_tuple,
            rejected_nodes=prior.rejected_nodes,
            metrics=metrics,
            provenance_bundle_id=f"bundle-{snapshot_id}",
            created_at_iso=created_at,
            status=SnapshotStatus.ACCEPTED,
            generation_hash=generation_hash,
            agent_id=self.descriptor.agent_id,
            agent_version=self.descriptor.version,
        )
