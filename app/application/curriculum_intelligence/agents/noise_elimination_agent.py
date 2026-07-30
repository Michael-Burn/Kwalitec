"""Generation 2 — Noise Elimination Agent.

Lifts EQ-001 ContentClassificationService. Does not delete nodes.
Rejected nodes become inactive with reason, confidence, and evidence.
"""

from __future__ import annotations

from dataclasses import replace

from app.application.curriculum_intelligence.agents.base import (
    CurriculumIntelligenceAgent,
    utc_now_iso,
)
from app.application.curriculum_intelligence.content_classification_service import (
    ContentClassificationService,
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
from app.domain.curriculum_intelligence.agent import (
    STANDARD_QUALITY_METRICS,
    AgentDescriptor,
)
from app.domain.curriculum_intelligence.content_role import (
    NON_CURRICULUM_ROLES,
    ContentRole,
    is_curriculum_role,
)
from app.domain.curriculum_intelligence.generation import (
    CurriculumGenerationSnapshot,
    EducationalNode,
    Generation,
    LineageOperation,
    LineageOperationKind,
    RejectedNode,
    SnapshotStatus,
    purpose_for_index,
)

_AGENT_VERSION = "1.0.0"
_DESCRIPTOR = AgentDescriptor(
    agent_id="noise_elimination_agent",
    name="NoiseEliminationAgent",
    purpose="noise_elimination",
    consumes=("curriculum_generation_snapshot",),
    produces=("curriculum_generation_snapshot", "rejected_node"),
    dependencies=("raw_graph_agent",),
    version=_AGENT_VERSION,
    deterministic=True,
    supports_rollback=True,
    quality_metrics_produced=STANDARD_QUALITY_METRICS,
)

_REASON_LABELS: dict[str, str] = {
    ContentRole.FRONT_MATTER.value: "Front matter — non-curriculum",
    ContentRole.NAVIGATION.value: "Navigation / page chrome",
    ContentRole.COPYRIGHT.value: "Copyright / legal notice",
    ContentRole.PUBLISHER_METADATA.value: "Publisher metadata",
    ContentRole.TABLE_OF_CONTENTS.value: "Table of contents",
    ContentRole.QUALIFICATION_INFORMATION.value: "Qualification information",
    ContentRole.ASSESSMENT_LOGISTICS.value: "Assessment logistics",
    ContentRole.APPENDIX.value: "Appendix material",
    ContentRole.INDEX.value: "Index material",
    ContentRole.REFERENCES.value: "References / bibliography",
    ContentRole.BLANK_ARTEFACT.value: "Blank / empty artefact",
}


class NoiseEliminationAgent(CurriculumIntelligenceAgent):
    """Generation 2 — soft-reject non-curriculum roles (EQ-001 classifier)."""

    generation_index = 2

    def __init__(
        self, classifier: ContentClassificationService | None = None
    ) -> None:
        self._classifier = classifier or ContentClassificationService()

    @property
    def descriptor(self) -> AgentDescriptor:
        return _DESCRIPTOR

    def execute(self, context: GenerationRunContext) -> CurriculumGenerationSnapshot:
        if context.prior_snapshot is None:
            raise ValueError("NoiseEliminationAgent requires a prior Gen 1 snapshot.")
        prior = context.prior_snapshot
        created_at = context.fixed_created_at_iso or utc_now_iso()
        generation_id = stable_id(
            "gen",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
            "g2",
        )
        snapshot_id = stable_id(
            "snap",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
            "g2",
        )

        nodes: list[EducationalNode] = []
        rejected: list[RejectedNode] = list(prior.rejected_nodes)

        for node in prior.nodes:
            if not node.active:
                nodes.append(node)
                continue

            role = self._resolve_role(node)
            if is_curriculum_role(role):
                nodes.append(node)
                continue

            reason_code = f"noise:{role.value}"
            reason_label = _REASON_LABELS.get(
                role.value, f"Non-curriculum role: {role.value}"
            )
            evidence_refs = (
                (node.provenance_id,)
                if node.provenance_id
                else tuple(
                    f"title:{node.title[:80]}" for _ in range(1) if node.title
                )
            )
            conf = float(node.confidence.score)
            op = LineageOperation(
                operation_id=stable_id("op", node.node_id, generation_id, "reject"),
                kind=LineageOperationKind.REJECTED,
                generation_id=generation_id,
                generation_index=2,
                reason_code=reason_code,
                reason_label=reason_label,
                evidence_refs=evidence_refs,
                confidence=conf,
                created_at_iso=created_at,
            )
            lineage = node.lineage.with_appended(op)
            inactive = replace(node, active=False, lineage=lineage, role=role.value)
            nodes.append(inactive)
            rejected.append(
                RejectedNode(
                    node=inactive,
                    rejected_at_generation=generation_id,
                    reason_code=reason_code,
                    reason_label=reason_label,
                    confidence=conf,
                    evidence_refs=evidence_refs,
                )
            )

        metrics = compute_quality_snapshot(nodes, rejected_count=len(rejected))
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
            generation_index=2,
            nodes=tuple(nodes),
        )
        generation = Generation(
            generation_id=generation_id,
            chain_id=context.chain_id,
            generation_index=2,
            purpose=purpose_for_index(2),
            parent_generation_ids=(prior.generation_id,),
            source_document_ids=context.source_document_ids,
            workspace_id=context.workspace_id,
            created_at_iso=created_at,
            calibration_profile_id=calibration_id,
        )
        return CurriculumGenerationSnapshot(
            snapshot_id=snapshot_id,
            generation=generation,
            nodes=tuple(nodes),
            rejected_nodes=tuple(rejected),
            metrics=metrics,
            provenance_bundle_id=f"bundle-{snapshot_id}",
            created_at_iso=created_at,
            status=SnapshotStatus.ACCEPTED,
            generation_hash=generation_hash,
            agent_id=self.descriptor.agent_id,
            agent_version=self.descriptor.version,
        )

    def _resolve_role(self, node: EducationalNode) -> ContentRole:
        if node.role:
            try:
                existing = ContentRole(node.role)
                if (
                    existing in NON_CURRICULUM_ROLES
                    or existing is ContentRole.EDUCATIONAL
                ):
                    return existing
                if existing is ContentRole.LEARNING_OBJECTIVE:
                    return existing
            except ValueError:
                pass
        return self._classifier.classify_line(node.title or node.body)
