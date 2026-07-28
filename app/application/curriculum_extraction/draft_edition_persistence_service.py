"""Draft Edition Persistence — write validated draft CKG to ckg_* tables."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import or_

from app.application.curriculum_extraction.draft_graph_constructor import (
    DraftGraphBundle,
)
from app.application.curriculum_extraction.exceptions import PersistenceError
from app.domain.curriculum_extraction.publication_state import (
    PublicationState,
    ValidationStatus,
)
from app.domain.curriculum_extraction.validation import ValidationReport
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
from app.domain.curriculum_knowledge_graph.graph.curriculum_knowledge_graph import (
    CurriculumKnowledgeGraph,
)
from app.domain.curriculum_knowledge_graph.value_objects.relationship_type import (
    CkgRelationshipType,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableIdDepth,
)
from app.extensions import db
from app.models.curriculum_knowledge_graph import (
    CkgDefinition,
    CkgEdge,
    CkgFormula,
    CkgGraphEdition,
    CkgLearningObjective,
    CkgLoLink,
    CkgNodeProvenance,
    CkgPracticeExercise,
    CkgReadingReference,
    CkgSection,
    CkgSubject,
    CkgSubsection,
    CkgSyllabusOutcome,
    CkgTopic,
    CkgValidationReport,
    CkgWorkedExample,
)


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class DraftEditionPersistenceService:
    """Persist a validated draft edition. Refuses non-draft publication states."""

    STAGE_ID = "draft_persist"

    def persist(
        self,
        *,
        bundle: DraftGraphBundle,
        validation: ValidationReport,
        job_id: str,
        source_cmp_ref: str,
        source_syllabus_ref: str,
    ) -> str:
        """Replace-or-create draft edition for subject+edition. Returns edition_id.

        Raises:
            PersistenceError: when validation failed or state is not draft.
        """
        if not validation.passed:
            raise PersistenceError(
                "Cannot persist draft edition while validation has blockers"
            )

        graph = bundle.graph
        subject = graph.subject
        edition_id = self._edition_id_for(subject, job_id)

        existing = CkgGraphEdition.query.filter_by(
            subject_code=subject.code,
            edition_label=subject.edition_label,
        ).first()
        if existing is not None:
            if existing.publication_state != PublicationState.DRAFT.value:
                raise PersistenceError(
                    "Refusing to overwrite non-draft edition "
                    f"{existing.edition_id} "
                    f"(state={existing.publication_state})"
                )
            self._delete_edition_graph(existing.edition_id, subject.code)
            edition = existing
            edition.edition_id = edition_id
            edition.title = subject.title
            edition.provider = subject.provider
            edition.publication_state = PublicationState.DRAFT.value
            edition.validation_status = ValidationStatus.PASSED.value
            edition.source_cmp_ref = source_cmp_ref
            edition.source_syllabus_ref = source_syllabus_ref
            edition.updated_at = _utc_now()
        else:
            edition = CkgGraphEdition(
                edition_id=edition_id,
                subject_code=subject.code,
                edition_label=subject.edition_label,
                provider=subject.provider,
                title=subject.title,
                publication_state=PublicationState.DRAFT.value,
                validation_status=ValidationStatus.PASSED.value,
                source_cmp_ref=source_cmp_ref,
                source_syllabus_ref=source_syllabus_ref,
            )
            db.session.add(edition)

        if edition.publication_state != PublicationState.DRAFT.value:
            raise PersistenceError("publication_state must be draft")

        self._write_nodes(graph, edition_id)
        self._write_edges(graph)
        self._write_lo_links(graph)
        self._write_provenance(edition_id, bundle)
        self._write_validation_report(edition_id, validation)
        db.session.commit()
        return edition_id

    def _edition_id_for(self, subject: Subject, job_id: str) -> str:
        safe_job = "".join(c for c in job_id if c.isalnum() or c in "-_")[:24]
        return f"ckg-{subject.code.lower()}-{subject.edition_label}-{safe_job}"

    def _delete_edition_graph(self, edition_id: str, subject_code: str) -> None:
        """Remove prior draft nodes/edges/provenance for replace-on-reextract."""
        prefix = subject_code.upper()
        subjects = CkgSubject.query.filter_by(graph_edition_id=edition_id).all()
        subject_ids = [s.stable_id for s in subjects] or [prefix]

        CkgNodeProvenance.query.filter_by(edition_id=edition_id).delete()
        CkgValidationReport.query.filter_by(edition_id=edition_id).delete()

        # Delete educational objects whose stable_id belongs to this subject.
        for model in (
            CkgDefinition,
            CkgFormula,
            CkgWorkedExample,
            CkgPracticeExercise,
            CkgReadingReference,
            CkgSyllabusOutcome,
        ):
            model.query.filter(
                or_(
                    model.stable_id == prefix,
                    model.stable_id.like(f"{prefix}.%"),
                )
            ).delete(synchronize_session=False)

        lo_rows = CkgLearningObjective.query.filter(
            CkgLearningObjective.stable_id.like(f"{prefix}.%")
        ).all()
        lo_ids = [r.stable_id for r in lo_rows]
        if lo_ids:
            CkgLoLink.query.filter(
                CkgLoLink.lo_stable_id.in_(lo_ids)
            ).delete(synchronize_session=False)

        CkgEdge.query.filter(
            or_(
                CkgEdge.from_stable_id == prefix,
                CkgEdge.from_stable_id.like(f"{prefix}.%"),
                CkgEdge.to_stable_id == prefix,
                CkgEdge.to_stable_id.like(f"{prefix}.%"),
            )
        ).delete(synchronize_session=False)

        CkgLearningObjective.query.filter(
            CkgLearningObjective.stable_id.like(f"{prefix}.%")
        ).delete(synchronize_session=False)
        CkgSubsection.query.filter(
            CkgSubsection.stable_id.like(f"{prefix}.%")
        ).delete(synchronize_session=False)
        CkgSection.query.filter(
            CkgSection.stable_id.like(f"{prefix}.%")
        ).delete(synchronize_session=False)
        CkgTopic.query.filter(
            CkgTopic.stable_id.like(f"{prefix}.%")
        ).delete(synchronize_session=False)
        CkgSubject.query.filter(
            CkgSubject.stable_id.in_(subject_ids)
        ).delete(synchronize_session=False)
        db.session.flush()

    def _write_nodes(
        self, graph: CurriculumKnowledgeGraph, edition_id: str
    ) -> None:
        for node in graph.nodes():
            if isinstance(node, Subject):
                db.session.add(
                    CkgSubject(
                        stable_id=node.stable_id.value,
                        graph_edition_id=edition_id,
                        code=node.code,
                        title=node.title,
                        provider=node.provider,
                        edition_label=node.edition_label,
                        sequence_index=node.sequence_index,
                    )
                )
            elif isinstance(node, Topic):
                db.session.add(
                    CkgTopic(
                        stable_id=node.stable_id.value,
                        subject_stable_id=node.subject_id.value,
                        code=node.code,
                        title=node.title,
                        display_order=node.display_order,
                        difficulty=node.difficulty.value,
                        estimated_study_minutes=node.estimated_study_minutes,
                    )
                )
            elif isinstance(node, Section):
                db.session.add(
                    CkgSection(
                        stable_id=node.stable_id.value,
                        topic_stable_id=node.topic_id.value,
                        code=node.code,
                        title=node.title,
                        display_order=node.display_order,
                        difficulty=node.difficulty.value,
                        estimated_study_minutes=node.estimated_study_minutes,
                    )
                )
            elif isinstance(node, Subsection):
                db.session.add(
                    CkgSubsection(
                        stable_id=node.stable_id.value,
                        section_stable_id=node.section_id.value,
                        code=node.code,
                        title=node.title,
                        display_order=node.display_order,
                        difficulty=node.difficulty.value,
                        estimated_study_minutes=node.estimated_study_minutes,
                    )
                )
            elif isinstance(node, LearningObjective):
                db.session.add(
                    CkgLearningObjective(
                        stable_id=node.stable_id.value,
                        subsection_stable_id=node.subsection_id.value,
                        code=node.code,
                        statement=node.statement,
                        cognitive_level=node.cognitive_level.value,
                        learning_type=node.learning_type.value,
                        display_order=node.display_order,
                        difficulty=node.difficulty.value,
                        estimated_study_minutes=node.estimated_study_minutes,
                    )
                )
            elif isinstance(node, Definition):
                db.session.add(
                    CkgDefinition(
                        stable_id=node.stable_id.value,
                        owner_stable_id=node.owner_id.value,
                        title=node.title,
                        body=node.body,
                        cmp_locator=node.cmp_locator,
                    )
                )
            elif isinstance(node, Formula):
                db.session.add(
                    CkgFormula(
                        stable_id=node.stable_id.value,
                        owner_stable_id=node.owner_id.value,
                        title=node.title,
                        notation=node.notation,
                        latex=node.latex,
                    )
                )
            elif isinstance(node, WorkedExample):
                db.session.add(
                    CkgWorkedExample(
                        stable_id=node.stable_id.value,
                        owner_stable_id=node.owner_id.value,
                        title=node.title,
                        summary=node.summary,
                    )
                )
            elif isinstance(node, PracticeExercise):
                db.session.add(
                    CkgPracticeExercise(
                        stable_id=node.stable_id.value,
                        owner_stable_id=node.owner_id.value,
                        title=node.title,
                        difficulty=node.difficulty.value,
                    )
                )
            elif isinstance(node, ReadingReference):
                db.session.add(
                    CkgReadingReference(
                        stable_id=node.stable_id.value,
                        owner_stable_id=node.owner_id.value,
                        title=node.title,
                        document_kind=node.document_kind,
                        locator=node.locator,
                    )
                )
            elif isinstance(node, SyllabusOutcome):
                db.session.add(
                    CkgSyllabusOutcome(
                        stable_id=node.stable_id.value,
                        owner_stable_id=node.owner_id.value,
                        outcome_code=node.outcome_code,
                        statement_ref=node.statement_ref,
                    )
                )

    def _write_edges(self, graph: CurriculumKnowledgeGraph) -> None:
        for edge in graph.edges():
            db.session.add(
                CkgEdge(
                    edge_id=edge.edge_id,
                    from_stable_id=edge.from_stable_id.value,
                    to_stable_id=edge.to_stable_id.value,
                    relationship_type=edge.relationship_type.value,
                    sequence_index=edge.sequence_index,
                    rationale=edge.rationale,
                )
            )

    def _write_lo_links(self, graph: CurriculumKnowledgeGraph) -> None:
        seq = 0
        for edge in graph.edges(relationship_type=CkgRelationshipType.REFERENCES):
            lo = edge.from_stable_id
            target = edge.to_stable_id
            if lo.depth is not StableIdDepth.LEARNING_OBJECTIVE:
                continue
            seq += 1
            db.session.add(
                CkgLoLink(
                    link_id=f"lolink-{uuid4().hex[:12]}",
                    lo_stable_id=lo.value,
                    target_kind=target.kind.value,
                    target_stable_id=target.value,
                    relationship_type=CkgRelationshipType.REFERENCES.value,
                    sequence_index=seq,
                )
            )

    def _write_provenance(
        self, edition_id: str, bundle: DraftGraphBundle
    ) -> None:
        for sid, prov in bundle.provenance.items():
            db.session.add(
                CkgNodeProvenance(
                    edition_id=edition_id,
                    stable_id=sid,
                    source_document_id=prov.locator.document_id,
                    document_kind=prov.document_kind.value,
                    page_number=prov.locator.page_number,
                    structural_path=prov.locator.structural_path,
                    section_heading=prov.locator.section_heading,
                    paragraph_or_table_ref=prov.locator.paragraph_or_table_ref,
                    confidence=prov.confidence.score,
                    extraction_method=prov.extraction_method.value,
                    notes=prov.notes,
                )
            )

    def _write_validation_report(
        self, edition_id: str, validation: ValidationReport
    ) -> None:
        payload: dict[str, Any] = validation.to_dict()
        db.session.add(
            CkgValidationReport(
                report_id=f"val-{uuid4().hex[:12]}",
                edition_id=edition_id,
                passed=validation.passed,
                issue_count=validation.issue_count,
                report_json=json.dumps(payload, sort_keys=True),
            )
        )
