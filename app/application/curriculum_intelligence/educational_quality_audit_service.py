"""Educational quality audit metrics for CIP outputs (EQ-001)."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from app.domain.curriculum_intelligence.content_role import ContentRole
from app.domain.curriculum_intelligence.curriculum_entity import (
    CurriculumEntityKind,
    CurriculumKnowledgeEntity,
    CurriculumMap,
)
from app.domain.curriculum_intelligence.structural_document import (
    StructuralDocument,
    StructuralNode,
)


@dataclass(frozen=True)
class StructuralAudit:
    """Structural metrics for one mapped curriculum document."""

    label: str
    chapters: int
    sections: int
    topics: int
    objectives: int
    max_hierarchy_depth: int
    avg_topics_per_section: float
    avg_objectives_per_topic: float
    duplicate_titles: int
    empty_nodes: int
    orphan_nodes: int
    invalid_parent_refs: int
    entity_counts: dict[str, int]
    front_matter_contamination: float
    mean_confidence: float
    sample_titles: tuple[tuple[str, str, int | None], ...]
    sample_objectives: tuple[str, ...]


@dataclass(frozen=True)
class NoiseReport:
    role_counts: dict[str, int]
    examples: tuple[tuple[str, str, int | None], ...]


@dataclass(frozen=True)
class QualityIndicators:
    front_matter_contamination: float
    hierarchy_accuracy_proxy: float
    topic_coherence_proxy: float
    duplicate_rate: float
    objective_density: float
    mean_topic_title_length: float
    section_balance: float
    parser_confidence: float


class EducationalQualityAuditService:
    """Produce measurable educational-quality indicators from CIP maps."""

    def audit_map(
        self, curriculum_map: CurriculumMap, *, label: str
    ) -> StructuralAudit:
        by_id = {e.entity_id: e for e in curriculum_map.entities}
        modules = [
            e for e in curriculum_map.entities if e.kind is CurriculumEntityKind.MODULE
        ]
        topics = [
            e
            for e in curriculum_map.entities
            if e.kind
            in {CurriculumEntityKind.TOPIC, CurriculumEntityKind.SUBTOPIC}
        ]
        objectives = [
            e
            for e in curriculum_map.entities
            if e.kind is CurriculumEntityKind.LEARNING_OBJECTIVE
        ]
        depths = [self._depth(e, by_id) for e in curriculum_map.entities]
        title_counts = Counter(
            e.title.strip().lower()
            for e in curriculum_map.entities
            if e.kind
            in {
                CurriculumEntityKind.MODULE,
                CurriculumEntityKind.TOPIC,
                CurriculumEntityKind.SUBTOPIC,
                CurriculumEntityKind.LEARNING_OBJECTIVE,
            }
            and e.title.strip()
        )
        dupes = sum(1 for _t, c in title_counts.items() if c > 1)
        empty = sum(1 for e in curriculum_map.entities if not (e.title or "").strip())
        orphans = sum(
            1
            for e in curriculum_map.entities
            if e.parent_id
            and e.parent_id not in by_id
            and e.kind is not CurriculumEntityKind.SUBJECT
        )
        contaminated = sum(
            1
            for e in curriculum_map.entities
            if self._role(e)
            in {
                ContentRole.FRONT_MATTER.value,
                ContentRole.NAVIGATION.value,
                ContentRole.TABLE_OF_CONTENTS.value,
                ContentRole.QUALIFICATION_INFORMATION.value,
                ContentRole.COPYRIGHT.value,
                ContentRole.PUBLISHER_METADATA.value,
            }
        )
        total_hier = max(len(modules) + len(topics) + len(objectives), 1)
        confidences = [e.confidence for e in curriculum_map.entities]
        samples = tuple(
            (
                e.kind.value,
                e.title[:100],
                e.source_pages[0] if e.source_pages else None,
            )
            for e in curriculum_map.entities[:40]
        )
        return StructuralAudit(
            label=label,
            chapters=len(modules),
            sections=len(modules),
            topics=len(topics),
            objectives=len(objectives),
            max_hierarchy_depth=max(depths) if depths else 0,
            avg_topics_per_section=round(len(topics) / len(modules), 2)
            if modules
            else 0.0,
            avg_objectives_per_topic=round(len(objectives) / len(topics), 2)
            if topics
            else 0.0,
            duplicate_titles=dupes,
            empty_nodes=empty,
            orphan_nodes=orphans,
            invalid_parent_refs=orphans,
            entity_counts=dict(Counter(e.kind.value for e in curriculum_map.entities)),
            front_matter_contamination=round(contaminated / total_hier, 4),
            mean_confidence=round(sum(confidences) / len(confidences), 4)
            if confidences
            else 0.0,
            sample_titles=samples,
            sample_objectives=tuple(o.title[:160] for o in objectives[:50]),
        )

    def noise_report(self, structural: StructuralDocument) -> NoiseReport:
        counts: Counter[str] = Counter()
        examples: list[tuple[str, str, int | None]] = []

        def walk(node: StructuralNode) -> None:
            role = node.attribute("content_role") or "unspecified"
            counts[role] += 1
            if role != ContentRole.EDUCATIONAL.value and len(examples) < 40:
                examples.append((role, node.title[:100], node.source_page))
            for child in node.children:
                walk(child)

        walk(structural.root)
        return NoiseReport(role_counts=dict(counts), examples=tuple(examples))

    def quality_indicators(self, audit: StructuralAudit) -> QualityIndicators:
        expected_chapters = 5  # CS1 syllabus topics
        hierarchy_proxy = 1.0 - min(
            abs(audit.chapters - expected_chapters) / max(expected_chapters, 1), 1.0
        )
        # Prefer dozens–low hundreds of topics, not thousands.
        if audit.topics == 0:
            coherence = 0.0
        elif 10 <= audit.topics <= 250:
            coherence = 0.9
        elif audit.topics < 10:
            coherence = 0.4
        else:
            coherence = max(0.0, 1.0 - (audit.topics - 250) / 5000)
        hier = max(audit.topics + audit.sections + audit.objectives, 1)
        dup_rate = audit.duplicate_titles / hier
        obj_density = (
            audit.objectives / audit.topics if audit.topics else 0.0
        )
        title_lens = [
            len(t[1]) for t in audit.sample_titles if t[0] in {"topic", "subtopic"}
        ]
        mean_len = sum(title_lens) / len(title_lens) if title_lens else 0.0
        balance = (
            1.0 / (1.0 + abs(audit.avg_topics_per_section - 4.0) / 10.0)
            if audit.sections
            else 0.0
        )
        return QualityIndicators(
            front_matter_contamination=audit.front_matter_contamination,
            hierarchy_accuracy_proxy=round(hierarchy_proxy, 4),
            topic_coherence_proxy=round(coherence, 4),
            duplicate_rate=round(dup_rate, 4),
            objective_density=round(obj_density, 4),
            mean_topic_title_length=round(mean_len, 2),
            section_balance=round(balance, 4),
            parser_confidence=audit.mean_confidence,
        )

    @staticmethod
    def _depth(
        entity: CurriculumKnowledgeEntity,
        by_id: dict[str, CurriculumKnowledgeEntity],
    ) -> int:
        d = 0
        cur = entity
        seen: set[str] = set()
        while cur.parent_id and cur.parent_id in by_id and cur.parent_id not in seen:
            seen.add(cur.parent_id)
            d += 1
            cur = by_id[cur.parent_id]
            if d > 30:
                break
        return d

    @staticmethod
    def _role(entity: CurriculumKnowledgeEntity) -> str | None:
        for k, v in entity.attributes:
            if k == "content_role":
                return v
        return None
