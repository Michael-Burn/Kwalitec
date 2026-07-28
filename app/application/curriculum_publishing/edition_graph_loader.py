"""Load CKG editions from ORM for Founder inspection, snapshots, and revalidation."""

from __future__ import annotations

import json
from typing import Any

from app.application.curriculum_extraction.draft_graph_constructor import (
    DraftGraphBundle,
)
from app.application.curriculum_publishing.exceptions import EditionNotFoundError
from app.domain.curriculum_extraction.canonical_document import (
    DocumentKind,
    StructuralLocator,
)
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
from app.domain.curriculum_knowledge_graph.graph.curriculum_knowledge_graph import (
    CurriculumKnowledgeGraph,
)
from app.domain.curriculum_knowledge_graph.graph.edge import CkgEdge
from app.domain.curriculum_knowledge_graph.value_objects.relationship_type import (
    CkgRelationshipType,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
)
from app.models.curriculum_knowledge_graph import (
    CkgDefinition,
    CkgFormula,
    CkgGraphEdition,
    CkgLearningObjective,
    CkgNodeProvenance,
    CkgPracticeExercise,
    CkgReadingReference,
    CkgSection,
    CkgSubject,
    CkgSubsection,
    CkgSyllabusOutcome,
    CkgTopic,
    CkgWorkedExample,
)
from app.models.curriculum_knowledge_graph import (
    CkgEdge as CkgEdgeRow,
)


class EditionGraphLoader:
    """Read-side loader for persisted CKG editions."""

    def require_edition(self, edition_id: str) -> CkgGraphEdition:
        edition = CkgGraphEdition.query.filter_by(edition_id=edition_id).first()
        if edition is None:
            raise EditionNotFoundError(f"Edition not found: {edition_id}")
        return edition

    def subject_for_edition(self, edition_id: str) -> CkgSubject | None:
        return CkgSubject.query.filter_by(graph_edition_id=edition_id).first()

    def collect_stable_ids(self, edition_id: str) -> list[str]:
        """All stable ids belonging to the edition's live graph."""
        subject = self.subject_for_edition(edition_id)
        if subject is None:
            return []
        prefix = subject.code.upper()
        ids: list[str] = [subject.stable_id]
        for model in (
            CkgTopic,
            CkgSection,
            CkgSubsection,
            CkgLearningObjective,
            CkgDefinition,
            CkgFormula,
            CkgWorkedExample,
            CkgPracticeExercise,
            CkgReadingReference,
            CkgSyllabusOutcome,
        ):
            rows = model.query.filter(
                (model.stable_id == prefix) | (model.stable_id.like(f"{prefix}.%"))
            ).all()
            ids.extend(r.stable_id for r in rows)
        return sorted(set(ids))

    def structural_snapshot(self, edition_id: str) -> dict[str, Any]:
        """Serialize structural nodes/edges for history and comparison."""
        edition = self.require_edition(edition_id)
        subject = self.subject_for_edition(edition_id)
        if subject is None:
            return {
                "edition_id": edition_id,
                "subject_code": edition.subject_code,
                "edition_label": edition.edition_label,
                "nodes": [],
                "edges": [],
            }

        prefix = subject.code.upper()
        nodes: list[dict[str, Any]] = [
            {
                "stable_id": subject.stable_id,
                "kind": "subject",
                "title": subject.title,
                "code": subject.code,
                "metadata": {
                    "provider": subject.provider,
                    "edition_label": subject.edition_label,
                },
            }
        ]

        for row in CkgTopic.query.filter(
            CkgTopic.subject_stable_id == subject.stable_id
        ).all():
            nodes.append(
                {
                    "stable_id": row.stable_id,
                    "kind": "topic",
                    "title": row.title,
                    "code": row.code,
                    "parent_stable_id": row.subject_stable_id,
                    "metadata": {
                        "display_order": row.display_order,
                        "difficulty": row.difficulty,
                        "estimated_study_minutes": row.estimated_study_minutes,
                    },
                }
            )

        topic_ids = {n["stable_id"] for n in nodes if n["kind"] == "topic"}
        for row in CkgSection.query.filter(
            CkgSection.topic_stable_id.in_(topic_ids) if topic_ids else False
        ).all():
            nodes.append(
                {
                    "stable_id": row.stable_id,
                    "kind": "section",
                    "title": row.title,
                    "code": row.code,
                    "parent_stable_id": row.topic_stable_id,
                    "metadata": {
                        "display_order": row.display_order,
                        "difficulty": row.difficulty,
                        "estimated_study_minutes": row.estimated_study_minutes,
                    },
                }
            )

        section_ids = {n["stable_id"] for n in nodes if n["kind"] == "section"}
        for row in CkgSubsection.query.filter(
            CkgSubsection.section_stable_id.in_(section_ids) if section_ids else False
        ).all():
            nodes.append(
                {
                    "stable_id": row.stable_id,
                    "kind": "subsection",
                    "title": row.title,
                    "code": row.code,
                    "parent_stable_id": row.section_stable_id,
                    "metadata": {
                        "display_order": row.display_order,
                        "difficulty": row.difficulty,
                        "estimated_study_minutes": row.estimated_study_minutes,
                    },
                }
            )

        subsection_ids = {
            n["stable_id"] for n in nodes if n["kind"] == "subsection"
        }
        for row in CkgLearningObjective.query.filter(
            CkgLearningObjective.subsection_stable_id.in_(subsection_ids)
            if subsection_ids
            else False
        ).all():
            nodes.append(
                {
                    "stable_id": row.stable_id,
                    "kind": "learning_objective",
                    "title": row.statement,
                    "code": row.code,
                    "parent_stable_id": row.subsection_stable_id,
                    "metadata": {
                        "statement": row.statement,
                        "display_order": row.display_order,
                        "difficulty": row.difficulty,
                        "estimated_study_minutes": row.estimated_study_minutes,
                        "cognitive_level": row.cognitive_level,
                        "learning_type": row.learning_type,
                    },
                }
            )

        for model, kind, title_attr, extra in (
            (CkgDefinition, "definition", "title", ("body", "cmp_locator")),
            (CkgFormula, "formula", "title", ("notation", "latex")),
            (CkgWorkedExample, "worked_example", "title", ("summary",)),
            (CkgPracticeExercise, "practice_exercise", "title", ("difficulty",)),
            (
                CkgReadingReference,
                "reading_reference",
                "title",
                ("document_kind", "locator"),
            ),
            (
                CkgSyllabusOutcome,
                "syllabus_outcome",
                "outcome_code",
                ("statement_ref",),
            ),
        ):
            rows = model.query.filter(
                (model.stable_id == prefix) | (model.stable_id.like(f"{prefix}.%"))
            ).all()
            for row in rows:
                meta = {"owner_stable_id": row.owner_stable_id}
                for attr in extra:
                    meta[attr] = getattr(row, attr, None)
                title = getattr(row, title_attr, "") or ""
                nodes.append(
                    {
                        "stable_id": row.stable_id,
                        "kind": kind,
                        "title": title,
                        "code": "",
                        "parent_stable_id": row.owner_stable_id,
                        "metadata": meta,
                    }
                )

        edges = []
        for row in CkgEdgeRow.query.filter(
            (CkgEdgeRow.from_stable_id == prefix)
            | (CkgEdgeRow.from_stable_id.like(f"{prefix}.%"))
            | (CkgEdgeRow.to_stable_id == prefix)
            | (CkgEdgeRow.to_stable_id.like(f"{prefix}.%"))
        ).all():
            edges.append(
                {
                    "edge_id": row.edge_id,
                    "from_stable_id": row.from_stable_id,
                    "to_stable_id": row.to_stable_id,
                    "relationship_type": row.relationship_type,
                    "sequence_index": row.sequence_index,
                    "rationale": row.rationale,
                }
            )

        return {
            "edition_id": edition_id,
            "subject_code": edition.subject_code,
            "edition_label": edition.edition_label,
            "title": edition.title,
            "nodes": sorted(nodes, key=lambda n: n["stable_id"]),
            "edges": sorted(
                edges,
                key=lambda e: (
                    e["relationship_type"],
                    e["from_stable_id"],
                    e["to_stable_id"],
                ),
            ),
        }

    def load_draft_bundle(self, edition_id: str) -> DraftGraphBundle:
        """Rebuild a DraftGraphBundle from ORM for revalidation."""
        edition = self.require_edition(edition_id)
        subject_row = self.subject_for_edition(edition_id)
        if subject_row is None:
            raise EditionNotFoundError(f"No subject nodes for edition {edition_id}")

        subject = Subject.create(
            subject_row.stable_id,
            subject_row.title,
            code=subject_row.code,
            provider=subject_row.provider,
            edition_label=subject_row.edition_label,
            sequence_index=subject_row.sequence_index,
        )
        graph = CurriculumKnowledgeGraph(subject=subject)
        prefix = subject_row.code.upper()

        for row in CkgTopic.query.filter_by(
            subject_stable_id=subject_row.stable_id
        ).all():
            graph.add_node(
                Topic.create(
                    row.stable_id,
                    row.subject_stable_id,
                    row.title,
                    code=row.code,
                    display_order=row.display_order,
                    difficulty=row.difficulty,
                    estimated_study_minutes=row.estimated_study_minutes,
                )
            )

        for row in CkgSection.query.join(
            CkgTopic, CkgSection.topic_stable_id == CkgTopic.stable_id
        ).filter(CkgTopic.subject_stable_id == subject_row.stable_id).all():
            graph.add_node(
                Section.create(
                    row.stable_id,
                    row.topic_stable_id,
                    row.title,
                    code=row.code,
                    display_order=row.display_order,
                    difficulty=row.difficulty,
                    estimated_study_minutes=row.estimated_study_minutes,
                )
            )

        for row in CkgSubsection.query.join(
            CkgSection, CkgSubsection.section_stable_id == CkgSection.stable_id
        ).join(
            CkgTopic, CkgSection.topic_stable_id == CkgTopic.stable_id
        ).filter(CkgTopic.subject_stable_id == subject_row.stable_id).all():
            graph.add_node(
                Subsection.create(
                    row.stable_id,
                    row.section_stable_id,
                    row.title,
                    code=row.code,
                    display_order=row.display_order,
                    difficulty=row.difficulty,
                    estimated_study_minutes=row.estimated_study_minutes,
                )
            )

        for row in CkgLearningObjective.query.join(
            CkgSubsection,
            CkgLearningObjective.subsection_stable_id == CkgSubsection.stable_id,
        ).join(
            CkgSection, CkgSubsection.section_stable_id == CkgSection.stable_id
        ).join(
            CkgTopic, CkgSection.topic_stable_id == CkgTopic.stable_id
        ).filter(CkgTopic.subject_stable_id == subject_row.stable_id).all():
            graph.add_node(
                LearningObjective.create(
                    row.stable_id,
                    row.subsection_stable_id,
                    row.statement,
                    code=row.code,
                    cognitive_level=row.cognitive_level,
                    learning_type=row.learning_type,
                    display_order=row.display_order,
                    difficulty=row.difficulty,
                    estimated_study_minutes=row.estimated_study_minutes,
                )
            )

        for row in CkgDefinition.query.filter(
            CkgDefinition.stable_id.like(f"{prefix}.%")
        ).all():
            graph.add_node(
                Definition.create(
                    row.stable_id,
                    row.owner_stable_id,
                    row.title,
                    body=row.body,
                    cmp_locator=row.cmp_locator,
                )
            )
        for row in CkgFormula.query.filter(
            CkgFormula.stable_id.like(f"{prefix}.%")
        ).all():
            graph.add_node(
                Formula.create(
                    row.stable_id,
                    row.owner_stable_id,
                    row.title,
                    notation=row.notation,
                    latex=row.latex,
                )
            )
        for row in CkgWorkedExample.query.filter(
            CkgWorkedExample.stable_id.like(f"{prefix}.%")
        ).all():
            graph.add_node(
                WorkedExample.create(
                    row.stable_id,
                    row.owner_stable_id,
                    row.title,
                    summary=row.summary,
                )
            )
        for row in CkgPracticeExercise.query.filter(
            CkgPracticeExercise.stable_id.like(f"{prefix}.%")
        ).all():
            graph.add_node(
                PracticeExercise.create(
                    row.stable_id,
                    row.owner_stable_id,
                    row.title,
                    difficulty=row.difficulty,
                )
            )
        for row in CkgReadingReference.query.filter(
            (CkgReadingReference.stable_id == prefix)
            | (CkgReadingReference.stable_id.like(f"{prefix}.%"))
        ).all():
            graph.add_node(
                ReadingReference.create(
                    row.stable_id,
                    row.owner_stable_id,
                    row.title,
                    document_kind=row.document_kind,
                    locator=row.locator,
                )
            )
        for row in CkgSyllabusOutcome.query.filter(
            (CkgSyllabusOutcome.stable_id == prefix)
            | (CkgSyllabusOutcome.stable_id.like(f"{prefix}.%"))
        ).all():
            graph.add_node(
                SyllabusOutcome.create(
                    row.stable_id,
                    row.owner_stable_id,
                    row.outcome_code,
                    statement_ref=row.statement_ref,
                )
            )

        for row in CkgEdgeRow.query.filter(
            (CkgEdgeRow.from_stable_id == prefix)
            | (CkgEdgeRow.from_stable_id.like(f"{prefix}.%"))
        ).all():
            graph.add_edge(
                CkgEdge.create(
                    row.from_stable_id,
                    row.to_stable_id,
                    CkgRelationshipType(row.relationship_type),
                    edge_id=row.edge_id,
                    sequence_index=row.sequence_index,
                    rationale=row.rationale,
                )
            )

        provenance: dict[str, ExtractionProvenance] = {}
        for row in CkgNodeProvenance.query.filter_by(edition_id=edition_id).all():
            try:
                kind = DocumentKind(row.document_kind)
            except ValueError:
                kind = DocumentKind.CMP
            try:
                method = ExtractionMethod(row.extraction_method)
            except ValueError:
                method = ExtractionMethod.HEURISTIC
            provenance[row.stable_id] = ExtractionProvenance.create(
                row.stable_id,
                StructuralLocator.create(
                    row.source_document_id,
                    page_number=row.page_number,
                    structural_path=row.structural_path,
                    section_heading=row.section_heading,
                    paragraph_or_table_ref=row.paragraph_or_table_ref,
                ),
                document_kind=kind,
                confidence=row.confidence,
                extraction_method=method,
                notes=row.notes,
            )

        return DraftGraphBundle(
            graph=graph,
            provenance=provenance,
            explicit_requires_numbers=[],
            diagnostics=[f"reloaded_from_orm:{edition.edition_id}"],
        )

    @staticmethod
    def snapshot_from_json(payload: str) -> dict[str, Any]:
        return json.loads(payload)


def node_kind_for_stable_id(stable_id: str) -> str:
    """Best-effort kind from stable id suffix / depth."""
    sid = StableCurriculumId.of(stable_id)
    return sid.kind.value
