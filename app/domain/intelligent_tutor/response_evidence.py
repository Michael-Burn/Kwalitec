"""Response evidence — structured assembly before response generation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.intelligent_tutor.tutor_context import TutorContext
from app.domain.intelligent_tutor.tutor_question import TutorQuestionKind


class EvidenceCategory(StrEnum):
    CURRICULUM = "curriculum"
    STUDENT = "student"
    LEARNING_GRAPH = "learning_graph"
    REASONING = "reasoning"
    OBSERVATION = "observation"
    MISSION = "mission"
    ASSESSMENT = "assessment"


@dataclass(frozen=True)
class EvidenceItemRef:
    """One structured evidence reference included in a Tutor response."""

    evidence_id: str
    category: EvidenceCategory
    summary: str
    source_id: str = ""
    concept_id: str = ""

    def __post_init__(self) -> None:
        if not (self.evidence_id or "").strip():
            raise ValueError("evidence_id is required")
        if not (self.summary or "").strip():
            raise ValueError("evidence summary is required")
        category = (
            self.category
            if isinstance(self.category, EvidenceCategory)
            else EvidenceCategory(str(self.category))
        )
        object.__setattr__(self, "category", category)


@dataclass(frozen=True)
class AssembledEvidence:
    """Structured evidence package prepared before response generation."""

    assembly_id: str
    twin_id: str
    items: tuple[EvidenceItemRef, ...]
    primary_concept_id: str = ""
    curriculum_count: int = 0
    student_count: int = 0
    graph_count: int = 0
    reasoning_count: int = 0
    observation_count: int = 0

    def __post_init__(self) -> None:
        if not (self.assembly_id or "").strip():
            raise ValueError("assembly_id is required")
        object.__setattr__(self, "items", tuple(self.items or ()))

    @property
    def evidence_ids(self) -> tuple[str, ...]:
        return tuple(item.evidence_id for item in self.items)

    def by_category(self, category: EvidenceCategory) -> tuple[EvidenceItemRef, ...]:
        return tuple(i for i in self.items if i.category == category)


def assemble_evidence(
    context: TutorContext,
    *,
    assembly_id: str,
    question_kind: TutorQuestionKind | str = TutorQuestionKind.GENERAL,
) -> AssembledEvidence:
    """Structure TutorContext into categorised evidence before generation.

    Pure function — does not call Twin, Reasoning, Graph, or Retrieval.
    """
    kind = (
        question_kind
        if isinstance(question_kind, TutorQuestionKind)
        else TutorQuestionKind(str(question_kind))
    )
    items: list[EvidenceItemRef] = []
    n = 0

    def _add(
        category: EvidenceCategory,
        summary: str,
        *,
        source_id: str = "",
        concept_id: str = "",
    ) -> None:
        nonlocal n
        if not (summary or "").strip():
            return
        n += 1
        items.append(
            EvidenceItemRef(
                evidence_id=f"{assembly_id}-ev-{n}",
                category=category,
                summary=summary.strip(),
                source_id=source_id,
                concept_id=concept_id or context.primary_concept_id,
            )
        )

    for excerpt, eid in zip(
        context.curriculum_excerpts,
        context.curriculum_evidence_ids
        or tuple(f"curr-{i}" for i in range(len(context.curriculum_excerpts))),
        strict=False,
    ):
        _add(EvidenceCategory.CURRICULUM, excerpt, source_id=eid)

    for note in context.mastery_notes:
        _add(EvidenceCategory.STUDENT, note, source_id="mastery")
    for note in context.confidence_notes:
        _add(EvidenceCategory.STUDENT, note, source_id="confidence")
    if context.learning_state_summary:
        _add(
            EvidenceCategory.STUDENT,
            context.learning_state_summary,
            source_id="learning_state",
        )

    for gap in context.knowledge_gap_summaries:
        _add(EvidenceCategory.REASONING, f"Knowledge gap: {gap}", source_id="gap")
    for rec in context.recommendation_summaries:
        _add(
            EvidenceCategory.REASONING,
            f"Recommendation: {rec}",
            source_id="recommendation",
        )
    if context.reasoning_run_id:
        _add(
            EvidenceCategory.REASONING,
            f"Latest educational reasoning run {context.reasoning_run_id}",
            source_id=context.reasoning_run_id,
        )

    if context.recovery_path:
        path = " → ".join(context.recovery_path)
        _add(
            EvidenceCategory.LEARNING_GRAPH,
            f"Recovery path: {path}",
            source_id="recovery_path",
        )
    for prereq in context.prerequisite_ids:
        _add(
            EvidenceCategory.LEARNING_GRAPH,
            f"Prerequisite: {prereq}",
            source_id=prereq,
            concept_id=prereq,
        )
    for related in context.related_concept_ids:
        _add(
            EvidenceCategory.LEARNING_GRAPH,
            f"Related concept: {related}",
            source_id=related,
            concept_id=related,
        )

    if context.active_mission_id:
        mission_bits = [
            f"Active mission {context.active_mission_id}",
        ]
        if context.active_mission_goal:
            mission_bits.append(f"goal: {context.active_mission_goal}")
        if context.active_mission_reason:
            mission_bits.append(f"reason: {context.active_mission_reason}")
        _add(
            EvidenceCategory.MISSION,
            "; ".join(mission_bits),
            source_id=context.active_mission_id,
        )

    for fb in context.assessment_feedback_summaries:
        _add(EvidenceCategory.ASSESSMENT, fb, source_id="assessment_feedback")

    # Prefer categories aligned to question focus (still keep all evidence).
    _ = kind  # classification already shaped context assembly upstream

    curriculum_count = sum(
        1 for i in items if i.category == EvidenceCategory.CURRICULUM
    )
    student_count = sum(1 for i in items if i.category == EvidenceCategory.STUDENT)
    graph_count = sum(
        1 for i in items if i.category == EvidenceCategory.LEARNING_GRAPH
    )
    reasoning_count = sum(
        1 for i in items if i.category == EvidenceCategory.REASONING
    )
    observation_count = sum(
        1 for i in items if i.category == EvidenceCategory.OBSERVATION
    )

    return AssembledEvidence(
        assembly_id=assembly_id,
        twin_id=context.twin_id,
        items=tuple(items),
        primary_concept_id=context.primary_concept_id,
        curriculum_count=curriculum_count,
        student_count=student_count,
        graph_count=graph_count,
        reasoning_count=reasoning_count,
        observation_count=observation_count,
    )
