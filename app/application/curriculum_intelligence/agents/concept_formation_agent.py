"""Generation 4 — Concept Formation Agent.

Formerly Topic Consolidation. Discovers coherent learning units via
ConceptFormationPolicy (merge / split / retain) with full lineage.
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
from app.application.curriculum_intelligence.policies.concept_formation_policy import (
    ConceptFormationPolicy,
)
from app.domain.curriculum_intelligence.agent import (
    STANDARD_QUALITY_METRICS,
    AgentDescriptor,
)
from app.domain.curriculum_intelligence.confidence import (
    ConfidenceRecord,
    confidence_band_from_score,
)
from app.domain.curriculum_intelligence.content_role import ContentRole
from app.domain.curriculum_intelligence.evidence import EvidenceGrade
from app.domain.curriculum_intelligence.generation import (
    CurriculumGenerationSnapshot,
    EducationalNode,
    Generation,
    LineageOperation,
    LineageOperationKind,
    LineageRecord,
    RejectedNode,
    SnapshotStatus,
    purpose_for_index,
)
from app.domain.curriculum_intelligence.provenance import (
    ProvenanceChainStage,
    ProvenanceRecord,
    ProvenanceSubjectKind,
    SupportingEvidence,
)

_AGENT_VERSION = "1.0.0"
_DESCRIPTOR = AgentDescriptor(
    agent_id="concept_formation_agent",
    name="ConceptFormationAgent",
    purpose="concept_formation",
    consumes=("curriculum_generation_snapshot",),
    produces=("curriculum_generation_snapshot", "concepts"),
    dependencies=("hierarchy_construction_agent", "concept_formation_policy"),
    version=_AGENT_VERSION,
    deterministic=True,
    supports_rollback=True,
    quality_metrics_produced=STANDARD_QUALITY_METRICS,
)


class ConceptFormationAgent(CurriculumIntelligenceAgent):
    """Generation 4 — form coherent learning concepts from hierarchy topics."""

    generation_index = 4

    def __init__(self, *, policy: ConceptFormationPolicy | None = None) -> None:
        self._policy = policy or ConceptFormationPolicy()

    @property
    def descriptor(self) -> AgentDescriptor:
        return _DESCRIPTOR

    def execute(self, context: GenerationRunContext) -> CurriculumGenerationSnapshot:
        if context.prior_snapshot is None:
            raise ValueError("ConceptFormationAgent requires a prior Gen 3 snapshot.")
        prior = context.prior_snapshot
        created_at = context.fixed_created_at_iso or utc_now_iso()
        generation_id = stable_id(
            "gen",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
            "g4",
        )
        snapshot_id = stable_id(
            "snap",
            prior.generation_hash or prior.snapshot_id,
            self.descriptor.version,
            "g4",
        )

        plan = self._policy.plan(
            prior.nodes, decision_prefix=f"cf-{generation_id[-8:]}"
        )
        merge_map = {survivor: absorbed for survivor, absorbed in plan.merges}
        absorbed_to_survivor = {
            abs_id: survivor
            for survivor, absorbed in plan.merges
            for abs_id in absorbed
        }
        split_map = {source: titles for source, titles in plan.splits}

        nodes: list[EducationalNode] = []
        rejected: list[RejectedNode] = list(prior.rejected_nodes)
        decision_by_subject: dict[str, object] = {}
        for decision in plan.decisions:
            for nid in decision.subject_node_ids:
                decision_by_subject.setdefault(nid, decision)

        # Children of absorbed topics reassign to the merge survivor.
        reparent_map: dict[str, str] = {}
        for survivor, absorbed in plan.merges:
            for abs_id in absorbed:
                reparent_map[abs_id] = survivor

        for node in prior.nodes:
            if not node.active:
                nodes.append(node)
                continue

            if node.node_id in absorbed_to_survivor:
                survivor_id = absorbed_to_survivor[node.node_id]
                decision = decision_by_subject.get(survivor_id)
                op = LineageOperation(
                    operation_id=stable_id(
                        "op", node.node_id, generation_id, "merged"
                    ),
                    kind=LineageOperationKind.MERGED,
                    generation_id=generation_id,
                    generation_index=4,
                    reason_code="concept:merged_into",
                    reason_label=(
                        decision.reason
                        if decision is not None
                        else "Merged into coherent learning unit"
                    ),
                    related_node_ids=(survivor_id,),
                    evidence_refs=(
                        decision.evidence_refs if decision is not None else ()
                    ),
                    confidence=(
                        decision.confidence if decision is not None else 0.9
                    ),
                    created_at_iso=created_at,
                )
                lineage = node.lineage.with_appended(op)
                inactive = replace(
                    node,
                    active=False,
                    lineage=lineage,
                    evidence_grade=(
                        decision.evidence_grade
                        if decision is not None
                        else node.evidence_grade or EvidenceGrade.A
                    ),
                    policy_id=self._policy.policy_id,
                )
                nodes.append(inactive)
                rejected.append(
                    RejectedNode(
                        node=inactive,
                        rejected_at_generation=generation_id,
                        reason_code=op.reason_code,
                        reason_label=op.reason_label,
                        confidence=op.confidence or 0.9,
                        evidence_refs=op.evidence_refs,
                    )
                )
                continue

            if node.node_id in split_map:
                decision = decision_by_subject.get(node.node_id)
                titles = split_map[node.node_id]
                child_ids: list[str] = []
                for index, title in enumerate(titles):
                    child_id = stable_id(
                        "node", generation_id, "split", node.node_id, title, str(index)
                    )
                    child_ids.append(child_id)
                    child = _new_concept_node(
                        node_id=child_id,
                        title=title,
                        parent_node_id=node.parent_node_id,
                        generation_id=generation_id,
                        created_at=created_at,
                        source=node,
                        local_index=index,
                        evidence_grade=(
                            decision.evidence_grade
                            if decision is not None
                            else EvidenceGrade.A
                        ),
                        policy_id=self._policy.policy_id,
                        reason="Split from compound topic into coherent unit",
                    )
                    nodes.append(child)
                op = LineageOperation(
                    operation_id=stable_id(
                        "op", node.node_id, generation_id, "split"
                    ),
                    kind=LineageOperationKind.SPLIT,
                    generation_id=generation_id,
                    generation_index=4,
                    reason_code="concept:split",
                    reason_label=(
                        decision.reason
                        if decision is not None
                        else "Split compound topic"
                    ),
                    related_node_ids=tuple(child_ids),
                    evidence_refs=(
                        decision.evidence_refs if decision is not None else ()
                    ),
                    confidence=(
                        decision.confidence if decision is not None else 0.88
                    ),
                    created_at_iso=created_at,
                )
                inactive = replace(
                    node,
                    active=False,
                    lineage=node.lineage.with_appended(op),
                    evidence_grade=(
                        decision.evidence_grade
                        if decision is not None
                        else node.evidence_grade or EvidenceGrade.A
                    ),
                    policy_id=self._policy.policy_id,
                )
                nodes.append(inactive)
                rejected.append(
                    RejectedNode(
                        node=inactive,
                        rejected_at_generation=generation_id,
                        reason_code=op.reason_code,
                        reason_label=op.reason_label,
                        confidence=op.confidence or 0.88,
                        evidence_refs=op.evidence_refs,
                    )
                )
                continue

            # Reassign children whose parent was absorbed into a survivor.
            new_parent = node.parent_node_id
            reassigned = False
            if node.parent_node_id and node.parent_node_id in reparent_map:
                new_parent = reparent_map[node.parent_node_id]
                reassigned = True

            # Retain / survivor of merge / non-topic passthrough.
            if node.node_id in merge_map:
                decision = decision_by_subject.get(node.node_id)
                absorbed = merge_map[node.node_id]
                op = LineageOperation(
                    operation_id=stable_id(
                        "op", node.node_id, generation_id, "merge_survivor"
                    ),
                    kind=LineageOperationKind.MERGED,
                    generation_id=generation_id,
                    generation_index=4,
                    reason_code="concept:merged_from",
                    reason_label=(
                        decision.reason
                        if decision is not None
                        else "Absorbed sibling fragments into coherent unit"
                    ),
                    related_node_ids=absorbed,
                    evidence_refs=(
                        decision.evidence_refs if decision is not None else ()
                    ),
                    confidence=(
                        decision.confidence if decision is not None else 0.9
                    ),
                    created_at_iso=created_at,
                )
                attrs = list(node.attributes)
                attrs.append(("concept_action", "merge"))
                attrs.append(("policy_id", self._policy.policy_id))
                if decision is not None:
                    attrs.append(("decision_id", decision.decision_id))
                    attrs.append(("decision_reason", decision.reason[:200]))
                nodes.append(
                    replace(
                        node,
                        kind="concept" if node.kind == "topic" else node.kind,
                        lineage=node.lineage.with_appended(op),
                        attributes=tuple(attrs),
                        evidence_grade=(
                            decision.evidence_grade
                            if decision is not None
                            else node.evidence_grade or EvidenceGrade.A
                        ),
                        policy_id=self._policy.policy_id,
                    )
                )
                continue

            if node.kind in {"topic", "subtopic"}:
                decision = decision_by_subject.get(node.node_id)
                attrs = list(node.attributes)
                attrs.append(("concept_action", "retain"))
                attrs.append(("policy_id", self._policy.policy_id))
                if decision is not None:
                    attrs.append(("decision_id", decision.decision_id))
                    attrs.append(("decision_reason", decision.reason[:200]))
                    conf_score = decision.confidence
                else:
                    conf_score = node.confidence.score
                conf = ConfidenceRecord(
                    confidence_id=f"conf-{node.node_id}-g4",
                    subject_kind="educational_node",
                    subject_id=node.node_id,
                    score=conf_score,
                    band=confidence_band_from_score(conf_score),
                    reason="concept_formation_retain",
                    factors=(),
                    needs_review=conf_score < 0.6,
                    review_threshold=0.6,
                    provenance_id=node.provenance_id,
                )
                lineage = node.lineage
                parent_id = new_parent
                if reassigned:
                    op = LineageOperation(
                        operation_id=stable_id(
                            "op", node.node_id, generation_id, "reparent"
                        ),
                        kind=LineageOperationKind.REPARENTED,
                        generation_id=generation_id,
                        generation_index=4,
                        reason_code="concept:reassigned",
                        reason_label=(
                            "Reassigned under merge survivor for educational coherence"
                        ),
                        related_node_ids=(new_parent,) if new_parent else (),
                        evidence_refs=_node_evidence(node),
                        confidence=conf_score,
                        created_at_iso=created_at,
                    )
                    lineage = lineage.with_appended(op)
                    attrs.append(("reassigned_from", node.parent_node_id or ""))
                nodes.append(
                    replace(
                        node,
                        kind="concept" if node.kind == "topic" else node.kind,
                        parent_node_id=parent_id,
                        confidence=conf,
                        lineage=lineage,
                        attributes=tuple(attrs),
                        evidence_grade=(
                            decision.evidence_grade
                            if decision is not None
                            else node.evidence_grade or EvidenceGrade.A
                        ),
                        policy_id=self._policy.policy_id,
                    )
                )
                continue

            # Non-topic hierarchy nodes: carry forward with evidence grade.
            grade = node.evidence_grade or (
                EvidenceGrade.A if node.lineage.syllabus_refs else EvidenceGrade.B
            )
            lineage = node.lineage
            parent_id = new_parent
            attrs = list(node.attributes)
            if reassigned:
                op = LineageOperation(
                    operation_id=stable_id(
                        "op", node.node_id, generation_id, "reparent"
                    ),
                    kind=LineageOperationKind.REPARENTED,
                    generation_id=generation_id,
                    generation_index=4,
                    reason_code="concept:reassigned",
                    reason_label=(
                        "Reassigned under merge survivor for educational coherence"
                    ),
                    related_node_ids=(new_parent,) if new_parent else (),
                    evidence_refs=_node_evidence(node),
                    confidence=node.confidence.score,
                    created_at_iso=created_at,
                )
                lineage = lineage.with_appended(op)
                attrs.append(("reassigned_from", node.parent_node_id or ""))
                attrs.append(("policy_id", self._policy.policy_id))
            nodes.append(
                replace(
                    node,
                    parent_node_id=parent_id,
                    lineage=lineage,
                    attributes=tuple(attrs) if reassigned else node.attributes,
                    evidence_grade=grade,
                    policy_id=node.policy_id or self._policy.policy_id,
                )
            )

        node_tuple = tuple(nodes)
        metrics = compute_quality_snapshot(
            node_tuple, rejected_count=len(rejected)
        )
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
            generation_index=4,
            nodes=node_tuple,
        )
        generation = Generation(
            generation_id=generation_id,
            chain_id=context.chain_id,
            generation_index=4,
            purpose=purpose_for_index(4),
            parent_generation_ids=(prior.generation_id,),
            source_document_ids=context.source_document_ids,
            workspace_id=context.workspace_id,
            created_at_iso=created_at,
            calibration_profile_id=calibration_id,
        )
        record_educational_decisions(
            context,
            plan.decisions,
            generation_index=4,
            generation_id=generation_id,
            agent_id=self.descriptor.agent_id,
            created_at_iso=created_at,
            snapshot_id=snapshot_id,
        )
        return CurriculumGenerationSnapshot(
            snapshot_id=snapshot_id,
            generation=generation,
            nodes=node_tuple,
            rejected_nodes=tuple(rejected),
            metrics=metrics,
            provenance_bundle_id=f"bundle-{snapshot_id}",
            created_at_iso=created_at,
            status=SnapshotStatus.ACCEPTED,
            generation_hash=generation_hash,
            agent_id=self.descriptor.agent_id,
            agent_version=self.descriptor.version,
        )


def _node_evidence(node: EducationalNode) -> tuple[str, ...]:
    refs: list[str] = []
    if node.provenance_id:
        refs.append(node.provenance_id)
    refs.extend(node.lineage.syllabus_refs)
    return tuple(refs)


def _new_concept_node(
    *,
    node_id: str,
    title: str,
    parent_node_id: str | None,
    generation_id: str,
    created_at: str,
    source: EducationalNode,
    local_index: int,
    evidence_grade: EvidenceGrade,
    policy_id: str,
    reason: str,
) -> EducationalNode:
    prov = ProvenanceRecord(
        provenance_id=f"prov-{node_id}",
        subject_kind=ProvenanceSubjectKind.EDUCATIONAL_NODE,
        subject_id=node_id,
        source_document_id=(
            source.provenance.source_document_id if source.provenance else 0
        ),
        source_version_label="concept_formation",
        source_pages=source.provenance.source_pages if source.provenance else (),
        source_paragraphs=(0,),
        source_block_ids=(f"cf-{node_id}",),
        parser_version="ei-concept/1.0",
        mapper_version="ei-concept/1.0",
        graph_builder_version="ei-concept/1.0",
        pipeline_job_id="",
        extraction_id="",
        parse_id="",
        map_id="",
        graph_id="",
        chain_stage=ProvenanceChainStage.CURRICULUM_MAPPING,
        evidence=(
            SupportingEvidence(
                page_number=None,
                paragraph_index=0,
                block_id=f"cf-{node_id}",
                excerpt=title[:200],
            ),
        ),
        created_at_iso=created_at,
    )
    score = 0.88
    conf = ConfidenceRecord(
        confidence_id=f"conf-{node_id}",
        subject_kind="educational_node",
        subject_id=node_id,
        score=score,
        band=confidence_band_from_score(score),
        reason="concept_formation_split",
        factors=(),
        needs_review=False,
        review_threshold=0.6,
        provenance_id=prov.provenance_id,
    )
    op = LineageOperation(
        operation_id=stable_id("op", node_id, "created"),
        kind=LineageOperationKind.CREATED,
        generation_id=generation_id,
        generation_index=4,
        reason_code="concept:split_created",
        reason_label=reason,
        related_node_ids=(source.node_id,),
        evidence_refs=(prov.provenance_id,),
        confidence=score,
        created_at_iso=created_at,
    )
    syllabus_refs = source.lineage.syllabus_refs
    match_num = title.split()[0] if title[:1].isdigit() else None
    if match_num and match_num[0].isdigit():
        syllabus_refs = (match_num,) + tuple(
            r for r in syllabus_refs if r != match_num
        )
    lineage = LineageRecord(
        created_generation=generation_id,
        created_generation_index=4,
        last_modified_generation=generation_id,
        last_modified_generation_index=4,
        operations=(op,),
        related_node_ids=(source.node_id,),
        syllabus_refs=syllabus_refs,
        parent_history=(parent_node_id,),
    )
    return EducationalNode(
        node_id=node_id,
        generation_local_id=f"g4-split-{local_index}",
        title=title,
        kind="concept",
        role=ContentRole.EDUCATIONAL.value,
        parent_node_id=parent_node_id,
        confidence=conf,
        lineage=lineage,
        active=True,
        provenance_id=prov.provenance_id,
        provenance=prov,
        body=source.body,
        attributes=(
            ("concept_action", "split"),
            ("policy_id", policy_id),
            ("split_from", source.node_id),
        ),
        evidence_grade=evidence_grade,
        policy_id=policy_id,
    )
