"""Graph Validation — detect structural and educational integrity issues."""

from __future__ import annotations

from app.application.curriculum_extraction.draft_graph_constructor import (
    DraftGraphBundle,
)
from app.domain.curriculum_extraction.validation import (
    ValidationReport,
    ValidationReportBuilder,
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
from app.domain.curriculum_knowledge_graph.entities.subsection import Subsection
from app.domain.curriculum_knowledge_graph.entities.syllabus_outcome import (
    SyllabusOutcome,
)
from app.domain.curriculum_knowledge_graph.entities.topic import Topic
from app.domain.curriculum_knowledge_graph.entities.worked_example import (
    WorkedExample,
)
from app.domain.curriculum_knowledge_graph.value_objects.relationship_type import (
    HARD_PREREQUISITE_TYPES,
    CkgRelationshipType,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
    StableIdDepth,
)


class GraphValidationService:
    """Validate a draft CKG candidate before persistence."""

    STAGE_ID = "validation"

    def validate(self, bundle: DraftGraphBundle) -> ValidationReport:
        """Return a validation report. Blockers prevent draft persist."""
        builder = ValidationReportBuilder()
        graph = bundle.graph
        node_ids = {n.stable_id.value for n in graph.nodes()}

        self._check_duplicates(graph, builder)
        self._check_hierarchy_and_orphans(graph, node_ids, builder)
        self._check_incomplete_objects(graph, builder)
        self._check_relationships(graph, node_ids, builder)
        self._check_requires_acyclicity(graph, builder)
        self._check_missing_prerequisites(bundle, builder)
        self._check_provenance_and_confidence(bundle, node_ids, builder)

        for message in bundle.diagnostics:
            builder.diagnostic(message)
        return builder.build()

    def _check_duplicates(self, graph, builder: ValidationReportBuilder) -> None:
        # Graph aggregate already rejects duplicates at add time; scan snapshot.
        seen: set[str] = set()
        for node in graph.nodes():
            key = node.stable_id.value
            if key in seen:
                builder.blocker(
                    "duplicate_stable_id",
                    f"Duplicate stable_id {key}",
                    stable_id=key,
                )
            seen.add(key)

    def _check_hierarchy_and_orphans(
        self, graph, node_ids: set[str], builder: ValidationReportBuilder
    ) -> None:
        subject_id = graph.subject.stable_id.value
        for node in graph.nodes():
            sid = node.stable_id.value
            if isinstance(node, Topic):
                self._owner_ok(
                    sid, node.subject_id.value, subject_id, node_ids, builder
                )
            elif isinstance(node, Section):
                self._owner_ok(
                    sid, node.topic_id.value, node.topic_id.value, node_ids, builder
                )
            elif isinstance(node, Subsection):
                self._owner_ok(
                    sid,
                    node.section_id.value,
                    node.section_id.value,
                    node_ids,
                    builder,
                )
            elif isinstance(node, LearningObjective):
                self._owner_ok(
                    sid,
                    node.subsection_id.value,
                    node.subsection_id.value,
                    node_ids,
                    builder,
                )
            elif isinstance(
                node,
                Definition
                | Formula
                | WorkedExample
                | PracticeExercise
                | ReadingReference
                | SyllabusOutcome,
            ):
                owner = node.owner_id.value
                if owner not in node_ids:
                    builder.blocker(
                        "orphan_node",
                        f"Owner {owner} missing for {sid}",
                        stable_id=sid,
                    )
                parent = StableCurriculumId.of(sid).parent_id()
                if parent is not None and parent.value != owner:
                    builder.blocker(
                        "broken_hierarchy",
                        f"stable_id parent {parent.value} != owner {owner}",
                        stable_id=sid,
                    )

            # Containment reachability from subject (except subject itself).
            if sid != subject_id:
                reachable = set(graph.traverse_containment(subject_id))
                if sid not in reachable:
                    # May still be connected via role edges only — check owner chain.
                    if not self._owner_chain_present(node, node_ids):
                        builder.blocker(
                            "orphan_node",
                            f"Node {sid} not reachable via containment",
                            stable_id=sid,
                        )

    def _owner_ok(
        self,
        sid: str,
        declared_owner: str,
        expected_in_graph: str,
        node_ids: set[str],
        builder: ValidationReportBuilder,
    ) -> None:
        if expected_in_graph not in node_ids:
            builder.blocker(
                "orphan_node",
                f"Parent {expected_in_graph} missing for {sid}",
                stable_id=sid,
            )
            return
        parent = StableCurriculumId.of(sid).parent_id()
        if parent is not None and parent.value != declared_owner:
            builder.blocker(
                "broken_hierarchy",
                f"stable_id parent {parent.value} != owner {declared_owner}",
                stable_id=sid,
            )

    def _owner_chain_present(self, node, node_ids: set[str]) -> bool:
        if isinstance(node, Topic):
            return node.subject_id.value in node_ids
        if isinstance(node, Section):
            return node.topic_id.value in node_ids
        if isinstance(node, Subsection):
            return node.section_id.value in node_ids
        if isinstance(node, LearningObjective):
            return node.subsection_id.value in node_ids
        if hasattr(node, "owner_id"):
            return node.owner_id.value in node_ids
        return True

    def _check_incomplete_objects(
        self, graph, builder: ValidationReportBuilder
    ) -> None:
        for node in graph.nodes():
            sid = node.stable_id.value
            if isinstance(node, LearningObjective) and not node.statement.strip():
                builder.blocker(
                    "incomplete_object",
                    "Learning objective missing statement",
                    stable_id=sid,
                )
            if (
                isinstance(node, Topic | Section | Subsection)
                and not node.title.strip()
            ):
                builder.blocker(
                    "incomplete_object",
                    f"{type(node).__name__} missing title",
                    stable_id=sid,
                )
            if isinstance(node, Definition) and not node.title.strip():
                builder.blocker(
                    "incomplete_object",
                    "Definition missing title",
                    stable_id=sid,
                )
            if isinstance(node, Formula) and not node.title.strip():
                builder.blocker(
                    "incomplete_object",
                    "Formula missing title",
                    stable_id=sid,
                )
            if isinstance(node, WorkedExample) and not node.title.strip():
                builder.blocker(
                    "incomplete_object",
                    "Worked example missing title",
                    stable_id=sid,
                )
            if isinstance(node, PracticeExercise) and not node.title.strip():
                builder.blocker(
                    "incomplete_object",
                    "Practice exercise missing title",
                    stable_id=sid,
                )
            if isinstance(node, ReadingReference) and not node.title.strip():
                builder.blocker(
                    "incomplete_object",
                    "Reading reference missing title",
                    stable_id=sid,
                )
            if isinstance(node, SyllabusOutcome) and not node.outcome_code.strip():
                builder.blocker(
                    "incomplete_object",
                    "Syllabus outcome missing outcome_code",
                    stable_id=sid,
                )

    def _check_relationships(
        self, graph, node_ids: set[str], builder: ValidationReportBuilder
    ) -> None:
        for edge in graph.edges():
            if edge.from_stable_id.value not in node_ids:
                builder.blocker(
                    "invalid_relationship",
                    f"Edge source missing: {edge.from_stable_id.value}",
                    stable_id=edge.from_stable_id.value,
                )
            if edge.to_stable_id.value not in node_ids:
                builder.blocker(
                    "invalid_reference",
                    f"Edge target missing: {edge.to_stable_id.value}",
                    stable_id=edge.to_stable_id.value,
                )
            if edge.from_stable_id.value == edge.to_stable_id.value:
                builder.blocker(
                    "invalid_relationship",
                    "Self-loop relationship",
                    stable_id=edge.from_stable_id.value,
                )
            if edge.relationship_type is CkgRelationshipType.REQUIRES:
                if (
                    edge.from_stable_id.depth is not StableIdDepth.LEARNING_OBJECTIVE
                    or edge.to_stable_id.depth is not StableIdDepth.LEARNING_OBJECTIVE
                ):
                    builder.blocker(
                        "invalid_relationship",
                        "requires edges must connect learning objectives",
                        stable_id=edge.from_stable_id.value,
                    )

    def _check_requires_acyclicity(
        self, graph, builder: ValidationReportBuilder
    ) -> None:
        try:
            graph.topological_learning_objectives()
        except ValueError:
            builder.blocker(
                "invalid_relationship",
                "requires graph contains a cycle",
            )

    def _check_missing_prerequisites(
        self, bundle: DraftGraphBundle, builder: ValidationReportBuilder
    ) -> None:
        if not bundle.explicit_requires_numbers:
            return
        requires = [
            e
            for e in bundle.graph.edges()
            if e.relationship_type in HARD_PREREQUISITE_TYPES
        ]
        if not requires:
            from_num, to_num = bundle.explicit_requires_numbers[0]
            builder.blocker(
                "missing_prerequisite",
                f"Explicit prerequisite {from_num}→{to_num} not materialised",
            )
        else:
            for from_num, to_num in bundle.explicit_requires_numbers:
                builder.diagnostic(
                    f"Prerequisite cue recorded: {from_num}→{to_num}"
                )

    def _check_provenance_and_confidence(
        self,
        bundle: DraftGraphBundle,
        node_ids: set[str],
        builder: ValidationReportBuilder,
    ) -> None:
        for sid in node_ids:
            prov = bundle.provenance.get(sid)
            if prov is None:
                builder.blocker(
                    "incomplete_object",
                    f"Missing provenance for {sid}",
                    stable_id=sid,
                )
                continue
            if prov.confidence.requires_manual_confirmation():
                builder.warning(
                    "low_confidence",
                    f"Confidence {prov.confidence.score}% requires manual "
                    "confirmation",
                    stable_id=sid,
                )
