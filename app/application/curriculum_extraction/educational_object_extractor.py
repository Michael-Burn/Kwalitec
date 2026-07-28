"""Educational Object Extraction — materialise CKG entities from segments."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.curriculum_extraction.models import (
    CurriculumSegmentTree,
    ParsedObjectCue,
    SegmentNode,
)
from app.domain.curriculum_extraction.canonical_document import DocumentKind
from app.domain.curriculum_extraction.provenance import (
    ExtractionMethod,
    ExtractionProvenance,
)
from app.domain.curriculum_knowledge_graph.entities.definition import Definition
from app.domain.curriculum_knowledge_graph.entities.formula import Formula
from app.domain.curriculum_knowledge_graph.entities.learning_objective import (
    LearningObjective,
)
from app.domain.curriculum_knowledge_graph.entities.practice_exercise import (
    PracticeExercise,
)
from app.domain.curriculum_knowledge_graph.entities.reading_reference import (
    ReadingReference,
)
from app.domain.curriculum_knowledge_graph.entities.section import Section
from app.domain.curriculum_knowledge_graph.entities.subject import Subject
from app.domain.curriculum_knowledge_graph.entities.subsection import Subsection
from app.domain.curriculum_knowledge_graph.entities.syllabus_outcome import (
    SyllabusOutcome,
)
from app.domain.curriculum_knowledge_graph.entities.topic import Topic
from app.domain.curriculum_knowledge_graph.entities.worked_example import (
    WorkedExample,
)
from app.domain.curriculum_knowledge_graph.value_objects.node_kind import (
    CkgNodeKind,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
    StableIdDepth,
)

NodePayload = (
    Subject
    | Topic
    | Section
    | Subsection
    | LearningObjective
    | Definition
    | Formula
    | WorkedExample
    | PracticeExercise
    | ReadingReference
    | SyllabusOutcome
)


@dataclass
class ExtractedCatalogue:
    """All CKG nodes + provenance before relationship wiring."""

    subject: Subject
    nodes: list[NodePayload] = field(default_factory=list)
    provenance: dict[str, ExtractionProvenance] = field(default_factory=dict)
    number_to_stable_id: dict[str, str] = field(default_factory=dict)
    lo_ids: list[str] = field(default_factory=list)
    object_ids_by_owner: dict[str, list[str]] = field(default_factory=dict)
    diagnostics: list[str] = field(default_factory=list)


class EducationalObjectExtractor:
    """Assign stable ids and create CKG entity instances."""

    STAGE_ID = "educational_object_extraction"

    def extract(self, tree: CurriculumSegmentTree) -> ExtractedCatalogue:
        """Populate structural nodes and educational objects."""
        subject = Subject.create(
            tree.subject_code,
            tree.subject_title,
            provider=tree.provider,
            edition_label=tree.edition_label,
        )
        catalogue = ExtractedCatalogue(subject=subject)
        subject_id = subject.stable_id.value
        catalogue.nodes.append(subject)
        if tree.subject_locator is not None:
            catalogue.provenance[subject_id] = ExtractionProvenance.create(
                subject_id,
                tree.subject_locator,
                document_kind=DocumentKind.SYLLABUS,
                confidence=99,
                extraction_method=ExtractionMethod.STRUCTURED_FIELD,
            )

        for topic_idx, topic_seg in enumerate(tree.topics, start=1):
            self._add_topic(catalogue, topic_seg, topic_idx, tree)

        self._attach_educational_objects(catalogue, tree)
        self._ensure_subject_reading_and_outcome(catalogue, tree)
        return catalogue

    def _add_topic(
        self,
        catalogue: ExtractedCatalogue,
        segment: SegmentNode,
        topic_n: int,
        tree: CurriculumSegmentTree,
    ) -> None:
        topic_id = StableCurriculumId.topic(tree.subject_code, topic_n)
        topic = Topic.create(
            topic_id,
            catalogue.subject.stable_id,
            segment.title,
            code=segment.number,
            display_order=topic_n,
            difficulty=segment.difficulty,
            estimated_study_minutes=segment.estimated_study_minutes,
        )
        catalogue.nodes.append(topic)
        catalogue.number_to_stable_id[segment.number] = topic_id.value
        self._prov(catalogue, topic_id.value, segment)

        for section_idx, section_seg in enumerate(segment.children, start=1):
            if section_seg.kind != "section":
                continue
            self._add_section(
                catalogue, section_seg, topic_n, section_idx, tree
            )

    def _add_section(
        self,
        catalogue: ExtractedCatalogue,
        segment: SegmentNode,
        topic_n: int,
        section_n: int,
        tree: CurriculumSegmentTree,
    ) -> None:
        # CKG section ids use (topic_n, section_n, ordinal); ordinal mirrors
        # section_n for syllabus-aligned numbering.
        section_id = StableCurriculumId.section(
            tree.subject_code, topic_n, section_n, section_n
        )
        topic_id = StableCurriculumId.topic(tree.subject_code, topic_n)
        section = Section.create(
            section_id,
            topic_id,
            segment.title,
            code=segment.number,
            display_order=section_n,
            difficulty=segment.difficulty,
            estimated_study_minutes=segment.estimated_study_minutes,
        )
        catalogue.nodes.append(section)
        catalogue.number_to_stable_id[segment.number] = section_id.value
        self._prov(catalogue, section_id.value, segment)

        for ss_idx, ss_seg in enumerate(segment.children, start=1):
            if ss_seg.kind != "subsection":
                continue
            self._add_subsection(
                catalogue, ss_seg, topic_n, section_n, ss_idx, tree
            )

    def _add_subsection(
        self,
        catalogue: ExtractedCatalogue,
        segment: SegmentNode,
        topic_n: int,
        section_n: int,
        subsection_n: int,
        tree: CurriculumSegmentTree,
    ) -> None:
        subsection_id = StableCurriculumId.subsection(
            tree.subject_code, topic_n, section_n, section_n, subsection_n
        )
        section_id = StableCurriculumId.section(
            tree.subject_code, topic_n, section_n, section_n
        )
        subsection = Subsection.create(
            subsection_id,
            section_id,
            segment.title,
            code=segment.number,
            display_order=subsection_n,
            difficulty=segment.difficulty,
            estimated_study_minutes=segment.estimated_study_minutes,
        )
        catalogue.nodes.append(subsection)
        catalogue.number_to_stable_id[segment.number] = subsection_id.value
        self._prov(catalogue, subsection_id.value, segment)

        for lo_idx, lo_seg in enumerate(segment.children, start=1):
            if lo_seg.kind != "learning_objective":
                continue
            lo_id = StableCurriculumId.learning_objective(
                tree.subject_code,
                topic_n,
                section_n,
                section_n,
                subsection_n,
                lo_idx,
            )
            lo = LearningObjective.create(
                lo_id,
                subsection_id,
                lo_seg.title,
                code=lo_seg.number,
                display_order=lo_idx,
                difficulty=lo_seg.difficulty,
                estimated_study_minutes=lo_seg.estimated_study_minutes,
                cognitive_level=lo_seg.cognitive_level,
                learning_type=lo_seg.learning_type,
            )
            catalogue.nodes.append(lo)
            catalogue.lo_ids.append(lo_id.value)
            catalogue.number_to_stable_id[lo_seg.number] = lo_id.value
            self._prov(catalogue, lo_id.value, lo_seg)

            # Syllabus outcome aligned to each LO.
            so_id = StableCurriculumId.educational_object(
                lo_id, CkgNodeKind.SYLLABUS_OUTCOME, 1
            )
            outcome = SyllabusOutcome.create(
                so_id,
                lo_id,
                lo_seg.number,
                statement_ref=lo_seg.title,
            )
            catalogue.nodes.append(outcome)
            catalogue.object_ids_by_owner.setdefault(lo_id.value, []).append(
                so_id.value
            )
            catalogue.provenance[so_id.value] = ExtractionProvenance.create(
                so_id.value,
                lo_seg.locator,
                document_kind=lo_seg.document_kind,
                confidence=lo_seg.confidence,
                extraction_method=lo_seg.extraction_method,
                notes="syllabus_outcome_from_lo",
            )

    def _attach_educational_objects(
        self,
        catalogue: ExtractedCatalogue,
        tree: CurriculumSegmentTree,
    ) -> None:
        counters: dict[tuple[str, str], int] = {}
        for cue in tree.object_cues:
            if cue.object_kind in {"study_time", "difficulty"}:
                continue
            owner_id = self._resolve_owner(catalogue, cue)
            if owner_id is None:
                catalogue.diagnostics.append(
                    f"Unhosted object cue skipped: {cue.object_kind} "
                    f"{cue.title[:60]}"
                )
                continue
            key = (owner_id, cue.object_kind)
            counters[key] = counters.get(key, 0) + 1
            n = counters[key]
            node = self._build_object(cue, owner_id, n)
            if node is None:
                continue
            catalogue.nodes.append(node)
            sid = node.stable_id.value
            catalogue.object_ids_by_owner.setdefault(owner_id, []).append(sid)
            catalogue.provenance[sid] = ExtractionProvenance.create(
                sid,
                cue.locator,
                document_kind=cue.document_kind,
                confidence=cue.confidence,
                extraction_method=cue.extraction_method,
            )

    def _resolve_owner(
        self, catalogue: ExtractedCatalogue, cue: ParsedObjectCue
    ) -> str | None:
        host = dict(cue.attributes).get("host_number")
        if host and host in catalogue.number_to_stable_id:
            candidate = catalogue.number_to_stable_id[host]
            # Educational objects attach to subsection or LO (RR also subject).
            parsed = StableCurriculumId.of(candidate)
            if cue.object_kind == "reading_reference":
                if parsed.depth in {
                    StableIdDepth.SUBJECT,
                    StableIdDepth.SUBSECTION,
                    StableIdDepth.LEARNING_OBJECTIVE,
                }:
                    return candidate
                return self._nearest_subsection(catalogue, host)
            if parsed.depth in {
                StableIdDepth.SUBSECTION,
                StableIdDepth.LEARNING_OBJECTIVE,
            }:
                return candidate
            return self._nearest_subsection(catalogue, host)
        # Fallback: first subsection in catalogue.
        for node in catalogue.nodes:
            if isinstance(node, Subsection):
                return node.stable_id.value
        return None

    def _nearest_subsection(
        self, catalogue: ExtractedCatalogue, number: str
    ) -> str | None:
        parts = number.split(".")
        for length in range(len(parts), 0, -1):
            key = ".".join(parts[:length])
            sid = catalogue.number_to_stable_id.get(key)
            if sid is None:
                continue
            depth = StableCurriculumId.of(sid).depth
            if depth is StableIdDepth.SUBSECTION:
                return sid
            if depth is StableIdDepth.LEARNING_OBJECTIVE:
                parent = StableCurriculumId.of(sid).parent_id()
                return parent.value if parent else None
            if depth is StableIdDepth.SECTION:
                # First child subsection of this section.
                for node in catalogue.nodes:
                    if (
                        isinstance(node, Subsection)
                        and node.section_id.value == sid
                    ):
                        return node.stable_id.value
        for node in catalogue.nodes:
            if isinstance(node, Subsection):
                return node.stable_id.value
        return None

    def _build_object(
        self, cue: ParsedObjectCue, owner_id: str, n: int
    ) -> NodePayload | None:
        kind_map = {
            "definition": CkgNodeKind.DEFINITION,
            "formula": CkgNodeKind.FORMULA,
            "worked_example": CkgNodeKind.WORKED_EXAMPLE,
            "practice_exercise": CkgNodeKind.PRACTICE_EXERCISE,
            "reading_reference": CkgNodeKind.READING_REFERENCE,
        }
        kind = kind_map.get(cue.object_kind)
        if kind is None:
            return None
        sid = StableCurriculumId.educational_object(owner_id, kind, n)
        if cue.object_kind == "definition":
            return Definition.create(
                sid,
                owner_id,
                cue.title,
                body=cue.body,
                cmp_locator=cue.locator.structural_path,
            )
        if cue.object_kind == "formula":
            return Formula.create(sid, owner_id, cue.title, notation=cue.body)
        if cue.object_kind == "worked_example":
            return WorkedExample.create(
                sid, owner_id, cue.title, summary=cue.body
            )
        if cue.object_kind == "practice_exercise":
            return PracticeExercise.create(sid, owner_id, cue.title)
        if cue.object_kind == "reading_reference":
            return ReadingReference.create(
                sid,
                owner_id,
                cue.title,
                document_kind="cmp",
                locator=cue.locator.structural_path or cue.body[:120],
            )
        return None

    def _ensure_subject_reading_and_outcome(
        self,
        catalogue: ExtractedCatalogue,
        tree: CurriculumSegmentTree,
    ) -> None:
        """Guarantee at least one subject-level RR when CMP present."""
        has_rr = any(isinstance(n, ReadingReference) for n in catalogue.nodes)
        if has_rr:
            return
        locator = tree.subject_locator
        if locator is None:
            return
        rr_id = StableCurriculumId.educational_object(
            catalogue.subject.stable_id,
            CkgNodeKind.READING_REFERENCE,
            1,
        )
        rr = ReadingReference.create(
            rr_id,
            catalogue.subject.stable_id,
            f"{tree.subject_code} CMP",
            document_kind="cmp",
            locator=locator.structural_path or tree.subject_code,
        )
        catalogue.nodes.append(rr)
        catalogue.provenance[rr_id.value] = ExtractionProvenance.create(
            rr_id.value,
            locator,
            document_kind=DocumentKind.CMP,
            confidence=90,
            extraction_method=ExtractionMethod.HEURISTIC,
            notes="default_subject_reading_reference",
        )

    def _prov(
        self,
        catalogue: ExtractedCatalogue,
        stable_id: str,
        segment: SegmentNode,
    ) -> None:
        catalogue.provenance[stable_id] = ExtractionProvenance.create(
            stable_id,
            segment.locator,
            document_kind=segment.document_kind,
            confidence=segment.confidence,
            extraction_method=segment.extraction_method,
        )
