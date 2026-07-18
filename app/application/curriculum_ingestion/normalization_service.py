"""NormalizationService — canonicalise extracted curriculum structures."""

from __future__ import annotations

from app.application.curriculum_ingestion.exceptions import NormalizationError
from app.application.curriculum_ingestion.policies.normalization_policy import (
    NormalizationPolicy,
)
from app.domain.curriculum_ingestion.extraction_result import ExtractionResult
from app.domain.curriculum_ingestion.normalization_result import (
    NormalizationResult,
    NormalizedObjective,
    NormalizedSection,
    NormalizedTopic,
)


class NormalizationService:
    """Normalise extracted structures into canonical identities and order.

    Deterministic. No teaching. No activity / session generation.
    """

    def normalize(
        self,
        extraction: ExtractionResult,
        *,
        result_id: str,
    ) -> NormalizationResult:
        """Produce a NormalizationResult from ``extraction``."""
        if extraction is None:
            raise NormalizationError("Extraction result is required")

        sections = self._normalize_sections(extraction)
        # Map original extracted ids → canonical ids
        extracted_to_canonical_section: dict[str, str] = {}
        for extracted, normalized in zip(
            extraction.sections, sections, strict=False
        ):
            extracted_to_canonical_section[extracted.section_id] = (
                normalized.section_id
            )
            for source in normalized.source_ids:
                extracted_to_canonical_section[source] = normalized.section_id

        if not sections:
            default = NormalizedSection.create(
                NormalizationPolicy.DEFAULT_SECTION_ID,
                NormalizationPolicy.DEFAULT_SECTION_TITLE,
                NormalizationPolicy.DEFAULT_SECTION_NUMBER,
                0,
            )
            sections = [default]

        section_ids = {s.section_id for s in sections}
        topics = self._normalize_topics(
            extraction,
            extracted_to_canonical_section,
            default_section_id=next(iter(section_ids)),
        )
        topic_id_map = {
            extracted.topic_id: normalized.topic_id
            for extracted, normalized in zip(
                extraction.topics, topics, strict=False
            )
        }
        # Also map by source
        for extracted, normalized in zip(
            extraction.topics, topics, strict=False
        ):
            topic_id_map[extracted.topic_id] = normalized.topic_id
            if extracted.source_entry_id:
                topic_id_map[extracted.source_entry_id] = normalized.topic_id

        objectives = self._normalize_objectives(extraction, topic_id_map, topics)
        edges = self._normalize_prerequisites(extraction, topic_id_map, topics)
        metadata = self._normalize_metadata(extraction)

        return NormalizationResult.create(
            result_id,
            extraction.result_id,
            sections=sections,
            topics=topics,
            objectives=objectives,
            prerequisite_edges=edges,
            metadata=metadata,
        )

    def _normalize_sections(
        self, extraction: ExtractionResult
    ) -> list[NormalizedSection]:
        sections: list[NormalizedSection] = []
        seen: set[str] = set()
        for index, section in enumerate(extraction.sections):
            sid = NormalizationPolicy.canonical_id(
                section.section_id,
                prefix="section",
                fallback_title=section.title,
            )
            # Deduplicate by canonical id — keep first
            if sid in seen:
                continue
            seen.add(sid)
            parent = None
            if section.parent_section_id:
                parent = NormalizationPolicy.canonical_id(
                    section.parent_section_id,
                    prefix="section",
                    fallback_title=section.parent_section_id,
                )
            number = NormalizationPolicy.canonical_number(
                section.number, order_index=index
            )
            sections.append(
                NormalizedSection.create(
                    sid,
                    NormalizationPolicy.collapse_whitespace(section.title),
                    number,
                    len(sections),
                    parent_section_id=parent,
                    source_ids=[section.section_id]
                    + (
                        [section.source_entry_id]
                        if section.source_entry_id
                        else []
                    ),
                )
            )
        return sections

    def _normalize_topics(
        self,
        extraction: ExtractionResult,
        section_map: dict[str, str],
        *,
        default_section_id: str,
    ) -> list[NormalizedTopic]:
        topics: list[NormalizedTopic] = []
        seen: set[str] = set()
        order_by_section: dict[str, int] = {}
        for topic in extraction.topics:
            tid = NormalizationPolicy.canonical_id(
                topic.topic_id, prefix="topic", fallback_title=topic.title
            )
            if tid in seen:
                continue
            seen.add(tid)
            section_id = default_section_id
            if topic.section_ref:
                section_id = section_map.get(
                    topic.section_ref,
                    NormalizationPolicy.canonical_id(
                        topic.section_ref,
                        prefix="section",
                        fallback_title=topic.section_ref,
                    ),
                )
                # If still unknown, keep canonicalised ref (validation catches)
            local_index = order_by_section.get(section_id, 0)
            order_by_section[section_id] = local_index + 1
            parent_number = None
            number = NormalizationPolicy.canonical_number(
                topic.number,
                order_index=local_index,
                parent_number=parent_number,
            )
            prereqs = tuple(
                NormalizationPolicy.canonical_id(
                    p, prefix="topic", fallback_title=p
                )
                for p in topic.prerequisite_refs
            )
            topics.append(
                NormalizedTopic.create(
                    tid,
                    NormalizationPolicy.collapse_whitespace(topic.title),
                    section_id,
                    number,
                    len(topics),
                    prerequisite_ids=prereqs,
                    source_ids=[topic.topic_id]
                    + ([topic.source_entry_id] if topic.source_entry_id else []),
                )
            )
        return topics

    def _normalize_objectives(
        self,
        extraction: ExtractionResult,
        topic_map: dict[str, str],
        topics: list[NormalizedTopic],
    ) -> list[NormalizedObjective]:
        objectives: list[NormalizedObjective] = []
        seen: set[str] = set()
        order_by_topic: dict[str, int] = {}
        fallback_topic = topics[0].topic_id if topics else None
        for objective in extraction.objectives:
            oid = NormalizationPolicy.canonical_id(
                objective.objective_id,
                prefix="objective",
                fallback_title=objective.text[:40],
            )
            if oid in seen:
                continue
            seen.add(oid)
            topic_id = fallback_topic
            if objective.topic_ref:
                topic_id = topic_map.get(
                    objective.topic_ref,
                    NormalizationPolicy.canonical_id(
                        objective.topic_ref,
                        prefix="topic",
                        fallback_title=objective.topic_ref,
                    ),
                )
            if topic_id is None:
                continue
            local_index = order_by_topic.get(topic_id, 0)
            order_by_topic[topic_id] = local_index + 1
            number = NormalizationPolicy.canonical_number(
                objective.number, order_index=local_index
            )
            objectives.append(
                NormalizedObjective.create(
                    oid,
                    NormalizationPolicy.collapse_whitespace(objective.text),
                    topic_id,
                    number,
                    len(objectives),
                    source_ids=[objective.objective_id]
                    + (
                        [objective.source_entry_id]
                        if objective.source_entry_id
                        else []
                    ),
                )
            )
        return objectives

    def _normalize_prerequisites(
        self,
        extraction: ExtractionResult,
        topic_map: dict[str, str],
        topics: list[NormalizedTopic],
    ) -> list[tuple[str, str]]:
        edges: list[tuple[str, str]] = []
        seen: set[tuple[str, str]] = set()
        for source, target in extraction.prerequisite_refs:
            src = topic_map.get(
                source,
                NormalizationPolicy.canonical_id(
                    source, prefix="topic", fallback_title=source
                ),
            )
            tgt = topic_map.get(
                target,
                NormalizationPolicy.canonical_id(
                    target, prefix="topic", fallback_title=target
                ),
            )
            edge = (src, tgt)
            if edge not in seen:
                seen.add(edge)
                edges.append(edge)
        for topic in topics:
            for prereq in topic.prerequisite_ids:
                edge = (topic.topic_id, prereq)
                if edge not in seen:
                    seen.add(edge)
                    edges.append(edge)
        return edges

    def _normalize_metadata(
        self, extraction: ExtractionResult
    ) -> list[tuple[str, str]]:
        seen: dict[str, str] = {}
        for key, value in extraction.metadata:
            canon_key = NormalizationPolicy.collapse_whitespace(key).lower()
            if canon_key and canon_key not in seen:
                seen[canon_key] = NormalizationPolicy.collapse_whitespace(value)
        return list(seen.items())
