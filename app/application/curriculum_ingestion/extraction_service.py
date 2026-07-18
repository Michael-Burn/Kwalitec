"""ExtractionService — deterministic structure extraction from documents."""

from __future__ import annotations

from app.application.curriculum_ingestion.exceptions import ExtractionError
from app.application.curriculum_ingestion.policies.extraction_policy import (
    ExtractionPolicy,
)
from app.domain.curriculum_ingestion.curriculum_document import (
    CurriculumDocument,
    DocumentEntry,
    DocumentEntryType,
    DocumentKind,
)
from app.domain.curriculum_ingestion.extracted_objective import ExtractedObjective
from app.domain.curriculum_ingestion.extracted_section import ExtractedSection
from app.domain.curriculum_ingestion.extracted_topic import ExtractedTopic
from app.domain.curriculum_ingestion.extraction_result import ExtractionResult


class ExtractionService:
    """Extract sections, topics, objectives, and prerequisites.

    Deterministic. No AI. No teaching content generation.
    """

    def extract(
        self,
        documents: list[CurriculumDocument] | tuple[CurriculumDocument, ...],
        classified_kinds: list[tuple[str, DocumentKind]]
        | tuple[tuple[str, DocumentKind], ...],
        *,
        result_id: str,
    ) -> ExtractionResult:
        """Extract structures from classified documents."""
        docs = tuple(documents)
        if not docs:
            raise ExtractionError("No documents to extract")
        kind_map = {did: kind for did, kind in classified_kinds}
        sections: list[ExtractedSection] = []
        topics: list[ExtractedTopic] = []
        objectives: list[ExtractedObjective] = []
        prereqs: list[tuple[str, str]] = []
        metadata: list[tuple[str, str]] = []
        notes: list[str] = []

        for doc in docs:
            kind = kind_map.get(doc.document_id, DocumentKind.UNKNOWN)
            allowed = ExtractionPolicy.extractable_entry_types(kind)
            current_section: str | None = None
            current_topic: str | None = None
            for entry in doc.entries:
                if entry.entry_type not in allowed:
                    continue
                if entry.entry_type is DocumentEntryType.SECTION:
                    section = self._section_from_entry(entry, doc.document_id)
                    sections.append(section)
                    current_section = section.section_id
                elif entry.entry_type is DocumentEntryType.TOPIC:
                    topic = self._topic_from_entry(
                        entry,
                        doc.document_id,
                        default_section=current_section,
                    )
                    topics.append(topic)
                    current_topic = topic.topic_id
                    for pref in topic.prerequisite_refs:
                        prereqs.append((topic.topic_id, pref))
                elif entry.entry_type is DocumentEntryType.OBJECTIVE:
                    objective = self._objective_from_entry(
                        entry,
                        doc.document_id,
                        default_topic=current_topic,
                    )
                    objectives.append(objective)
                elif entry.entry_type is DocumentEntryType.PREREQUISITE:
                    topic_ref = (
                        entry.parent_ref
                        or entry.attribute("topic_ref")
                        or current_topic
                    )
                    if topic_ref:
                        prereqs.append((topic_ref, entry.text.strip()))
                elif entry.entry_type is DocumentEntryType.METADATA:
                    key = entry.attribute("key") or entry.number or entry.entry_id
                    metadata.append((key, entry.text))
                elif entry.entry_type in {
                    DocumentEntryType.FORMULA,
                    DocumentEntryType.NOTE,
                }:
                    notes.append(entry.text)

            for key, value in doc.metadata:
                metadata.append((key, value))

        return ExtractionResult.create(
            result_id,
            [d.document_id for d in docs],
            document_kinds=tuple(classified_kinds),
            sections=sections,
            topics=topics,
            objectives=objectives,
            prerequisite_refs=prereqs,
            metadata=metadata,
            notes=notes,
        )

    def _section_from_entry(
        self, entry: DocumentEntry, document_id: str
    ) -> ExtractedSection:
        return ExtractedSection.create(
            entry.entry_id,
            entry.text,
            number=entry.number,
            source_entry_id=entry.entry_id,
            parent_section_id=entry.parent_ref,
            metadata=(("document_id", document_id),),
        )

    def _topic_from_entry(
        self,
        entry: DocumentEntry,
        document_id: str,
        *,
        default_section: str | None,
    ) -> ExtractedTopic:
        prereq_attr = entry.attribute("prerequisites") or entry.attribute(
            "prerequisite"
        )
        prereqs: list[str] = []
        if prereq_attr:
            prereqs = [p.strip() for p in prereq_attr.split(",") if p.strip()]
        return ExtractedTopic.create(
            entry.entry_id,
            entry.text,
            section_ref=entry.parent_ref or default_section,
            number=entry.number,
            source_entry_id=entry.entry_id,
            prerequisite_refs=prereqs,
            metadata=(("document_id", document_id),),
        )

    def _objective_from_entry(
        self,
        entry: DocumentEntry,
        document_id: str,
        *,
        default_topic: str | None,
    ) -> ExtractedObjective:
        return ExtractedObjective.create(
            entry.entry_id,
            entry.text,
            topic_ref=entry.parent_ref
            or entry.attribute("topic_ref")
            or default_topic,
            number=entry.number,
            source_entry_id=entry.entry_id,
            metadata=(("document_id", document_id),),
        )
