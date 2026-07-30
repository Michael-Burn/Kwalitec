"""ObjectivePolicy — attach learning objectives / competencies (Generation 5)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.application.curriculum_intelligence.policies.base import EducationalPolicy
from app.domain.curriculum_intelligence.evidence import EvidenceGrade
from app.domain.curriculum_intelligence.generation import EducationalNode
from app.domain.curriculum_intelligence.policy import (
    EducationalDecision,
    ObjectiveKind,
    PolicyDescriptor,
)

_NUM = re.compile(r"^(\d+(?:\.\d+)*)\s+")
_VERB = re.compile(
    r"\b(describe|explain|calculate|derive|apply|analyse|analyze|evaluate|"
    r"compare|identify|understand|complete|use|determine|interpret|"
    r"construct|define|state|show|prove)\b",
    re.IGNORECASE,
)

_DESCRIPTOR = PolicyDescriptor(
    policy_id="objective_policy",
    name="ObjectivePolicy",
    purpose="Associate learning objectives, competencies, knowledge, exam expectations",
    version="1.0.0",
    deterministic=True,
    generation_index=5,
)


@dataclass(frozen=True)
class ObjectiveAttachment:
    """One educational association bound to a topic or objective node."""

    node_id: str
    kind: ObjectiveKind
    label: str
    syllabus_ref: str | None
    evidence_grade: EvidenceGrade
    confidence: float
    evidence_refs: tuple[str, ...]
    policy_id: str
    decision_id: str


@dataclass(frozen=True)
class ObjectivePlan:
    """Deterministic objective-intelligence plan."""

    decisions: tuple[EducationalDecision, ...]
    attachments: tuple[ObjectiveAttachment, ...]


class ObjectivePolicy(EducationalPolicy):
    """Attach educational associations to topics and learning objectives."""

    @property
    def descriptor(self) -> PolicyDescriptor:
        return _DESCRIPTOR

    def plan(
        self,
        nodes: tuple[EducationalNode, ...] | list[EducationalNode],
        *,
        decision_prefix: str = "obj",
    ) -> ObjectivePlan:
        """Produce attachments for active topics and learning objectives."""
        active = [n for n in nodes if n.active]
        by_id = {n.node_id: n for n in active}
        decisions: list[EducationalDecision] = []
        attachments: list[ObjectiveAttachment] = []
        seq = 0

        objectives = [
            n for n in active if n.kind in {"learning_objective", "objective"}
        ]
        topics = [n for n in active if n.kind in {"topic", "subtopic", "concept"}]

        for obj in sorted(objectives, key=lambda n: n.node_id):
            syllabus_ref = _syllabus_ref(obj)
            grade = (
                EvidenceGrade.A
                if syllabus_ref
                else (obj.evidence_grade or EvidenceGrade.C)
            )
            evidence_refs = _evidence_refs(obj)
            verb = _competency_verb(obj.title)
            knowledge = _strip_number(obj.title)

            bindings: list[tuple[ObjectiveKind, str, float]] = [
                (ObjectiveKind.LEARNING_OBJECTIVE, obj.title.strip(), 0.95),
                (
                    ObjectiveKind.KNOWLEDGE_STATEMENT,
                    knowledge or obj.title.strip(),
                    0.9,
                ),
            ]
            if verb:
                bindings.append(
                    (
                        ObjectiveKind.COMPETENCY,
                        f"{verb.title()} — {knowledge or obj.title.strip()}",
                        0.86,
                    )
                )
            exam = _exam_expectation(obj, by_id)
            if exam:
                bindings.append((ObjectiveKind.EXAM_EXPECTATION, exam, 0.8))

            for kind, label, confidence in bindings:
                seq += 1
                decision_id = f"{decision_prefix}-{seq}"
                decision = EducationalDecision(
                    decision_id=decision_id,
                    action=f"attach:{kind.value}",
                    subject_node_ids=(obj.node_id,),
                    reason=f"Associate {kind.value} from syllabus/CMP evidence",
                    evidence_refs=evidence_refs,
                    confidence=confidence,
                    policy_id=self.policy_id,
                    evidence_grade=grade,
                    syllabus_ref=syllabus_ref,
                    detail=label[:200],
                )
                decisions.append(decision)
                attachments.append(
                    ObjectiveAttachment(
                        node_id=obj.node_id,
                        kind=kind,
                        label=label[:300],
                        syllabus_ref=syllabus_ref,
                        evidence_grade=grade,
                        confidence=confidence,
                        evidence_refs=evidence_refs,
                        policy_id=self.policy_id,
                        decision_id=decision_id,
                    )
                )

        # Topics without child objectives still receive knowledge statements.
        obj_parents = {
            o.parent_node_id for o in objectives if o.parent_node_id is not None
        }
        for topic in sorted(topics, key=lambda n: n.node_id):
            if topic.node_id in obj_parents:
                continue
            seq += 1
            syllabus_ref = _syllabus_ref(topic)
            grade = EvidenceGrade.A if syllabus_ref else EvidenceGrade.B
            decision_id = f"{decision_prefix}-{seq}"
            label = _strip_number(topic.title) or topic.title
            decision = EducationalDecision(
                decision_id=decision_id,
                action=f"attach:{ObjectiveKind.KNOWLEDGE_STATEMENT.value}",
                subject_node_ids=(topic.node_id,),
                reason="Topic lacks child LO; attach knowledge statement for coverage",
                evidence_refs=_evidence_refs(topic),
                confidence=0.75,
                policy_id=self.policy_id,
                evidence_grade=grade,
                syllabus_ref=syllabus_ref,
                detail=label[:200],
            )
            decisions.append(decision)
            attachments.append(
                ObjectiveAttachment(
                    node_id=topic.node_id,
                    kind=ObjectiveKind.KNOWLEDGE_STATEMENT,
                    label=label[:300],
                    syllabus_ref=syllabus_ref,
                    evidence_grade=grade,
                    confidence=0.75,
                    evidence_refs=_evidence_refs(topic),
                    policy_id=self.policy_id,
                    decision_id=decision_id,
                )
            )

        return ObjectivePlan(
            decisions=tuple(decisions), attachments=tuple(attachments)
        )


def _evidence_refs(node: EducationalNode) -> tuple[str, ...]:
    refs: list[str] = []
    if node.provenance_id:
        refs.append(node.provenance_id)
    refs.extend(node.lineage.syllabus_refs)
    return tuple(refs)


def _syllabus_ref(node: EducationalNode) -> str | None:
    if node.lineage.syllabus_refs:
        return node.lineage.syllabus_refs[0]
    match = _NUM.match(node.title.strip())
    return match.group(1) if match else None


def _strip_number(title: str) -> str:
    return _NUM.sub("", title).strip(" -–—:\t")


def _competency_verb(title: str) -> str | None:
    match = _VERB.search(title)
    return match.group(1).lower() if match else None


def _exam_expectation(
    node: EducationalNode, by_id: dict[str, EducationalNode]
) -> str | None:
    """Derive exam expectation from chapter weight attributes when present."""
    current: EducationalNode | None = node
    seen: set[str] = set()
    while current is not None and current.node_id not in seen:
        seen.add(current.node_id)
        for key, value in current.attributes:
            if key in {"weight", "exam_weight", "chapter_weight"} and value:
                return f"Weighted examination topic ({value})"
            if key == "hierarchy_kind" and value == "chapter":
                weight = _weight_from_title(current.title)
                if weight:
                    return f"Chapter examination weight {weight}"
        parent_id = current.parent_node_id
        current = by_id.get(parent_id) if parent_id else None
    weight = _weight_from_title(node.title)
    return f"Syllabus objective ({weight})" if weight else "Syllabus learning objective"


def _weight_from_title(title: str) -> str | None:
    match = re.search(r"\[(\d+%?)\]", title)
    return match.group(1) if match else None
