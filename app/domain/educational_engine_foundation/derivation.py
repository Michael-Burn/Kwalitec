"""Deterministic derivation rules for curriculum-published educational artefacts.

PI-001B keeps published curriculum as the single source of truth and derives
student-learning structures from that published package without UI coupling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.domain.curriculum.entities.prerequisite import Prerequisite
from app.domain.curriculum.entities.topic import Topic
from app.domain.curriculum.graph.curriculum_graph import CurriculumGraph
from app.domain.curriculum.graph.graph_builder import GraphBuilder
from app.domain.educational_quality.rules import (
    build_mission_completion_definition,
    build_mission_educational_rationale,
)
from app.domain.educational_runtime_engine.student_facing_identity import (
    student_mission_title,
    student_syllabus_code,
)


@dataclass(frozen=True)
class CurriculumSectionNode:
    section_id: str
    code: str
    title: str
    number: str
    display_order: int
    topic_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class CurriculumTopicNode:
    topic_id: str
    code: str
    title: str
    section_id: str
    number: str
    display_order: int
    estimated_minutes: int
    difficulty: str
    learning_objective_ids: tuple[str, ...] = field(default_factory=tuple)
    prerequisite_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class CurriculumObjectiveNode:
    objective_id: str
    code: str
    text: str
    topic_id: str
    number: str
    display_order: int
    estimated_minutes: int
    learning_type: str
    cognitive_level: str


@dataclass(frozen=True)
class StudyPlanTopicTemplate:
    topic_id: str
    topic_code: str
    topic_title: str
    section_id: str
    recommended_minutes: int
    prerequisite_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class MissionTemplate:
    template_id: str
    topic_id: str
    topic_code: str
    mission_kind: str
    title: str
    task_descriptions: tuple[str, ...] = field(default_factory=tuple)
    objective_ids: tuple[str, ...] = field(default_factory=tuple)
    estimated_duration_minutes: int = 0
    completion_definition: str = ""
    educational_rationale: str = ""
    prerequisite_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class JourneyTopicNode:
    topic_id: str
    topic_code: str
    title: str
    objective_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class JourneySectionNode:
    section_id: str
    code: str
    title: str
    topics: tuple[JourneyTopicNode, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ProgressTopicNode:
    topic_id: str
    topic_code: str
    objective_ids: tuple[str, ...] = field(default_factory=tuple)
    prerequisite_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ProgressModel:
    curriculum_identity: str
    section_ids: tuple[str, ...]
    topic_ids: tuple[str, ...]
    objective_ids: tuple[str, ...]
    topics: tuple[ProgressTopicNode, ...]


@dataclass(frozen=True)
class EducationalArtefactBundle:
    curriculum_identity: str
    subject_code: str
    version_label: str
    sections: tuple[CurriculumSectionNode, ...]
    topics: tuple[CurriculumTopicNode, ...]
    objectives: tuple[CurriculumObjectiveNode, ...]
    graph: CurriculumGraph
    study_plan_template: tuple[StudyPlanTopicTemplate, ...]
    mission_templates: tuple[MissionTemplate, ...]
    journey: tuple[JourneySectionNode, ...]
    progress_model: ProgressModel
    prerequisite_edges: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)


class EducationalDerivationError(ValueError):
    """Raised when a published package cannot derive lawful artefacts."""


class EducationalArtefactDeriver:
    """Pure derivation service over a published curriculum package dict."""

    def derive(self, package: dict[str, Any]) -> EducationalArtefactBundle:
        structure = package.get("structure") or {}
        subject_code = _text(package.get("subject_code"), "subject_code")
        version_label = _text(package.get("version_label"), "version_label")
        identity = f"{subject_code}:{version_label}"

        raw_sections = tuple(structure.get("sections") or ())
        raw_topics = tuple(structure.get("topics") or ())
        raw_objectives = tuple(structure.get("objectives") or ())
        raw_edges = tuple(structure.get("prerequisite_edges") or ())
        raw_metadata = tuple(structure.get("metadata") or ())

        if not raw_sections or not raw_topics or not raw_objectives:
            raise EducationalDerivationError(
                "published curriculum must include sections, topics, and objectives"
            )

        objectives = _derive_objectives(raw_objectives)
        objective_by_topic: dict[str, list[CurriculumObjectiveNode]] = {}
        for objective in objectives:
            objective_by_topic.setdefault(objective.topic_id, []).append(objective)

        topics = _derive_topics(raw_topics, objective_by_topic)
        topic_ids = {topic.topic_id for topic in topics}
        for objective in objectives:
            if objective.topic_id not in topic_ids:
                raise EducationalDerivationError(
                    "objective "
                    f"{objective.objective_id} references unknown topic "
                    f"{objective.topic_id}"
                )

        sections = _derive_sections(raw_sections, topics)
        section_ids = {section.section_id for section in sections}
        for topic in topics:
            if topic.section_id not in section_ids:
                raise EducationalDerivationError(
                    "topic "
                    f"{topic.topic_id} references unknown section "
                    f"{topic.section_id}"
                )

        prerequisite_edges = _normalize_edges(raw_edges, topic_ids)
        graph = _derive_graph(topics, prerequisite_edges)
        ordered_topic_ids = _derive_topic_order(topics, prerequisite_edges)
        topic_by_id = {topic.topic_id: topic for topic in topics}
        ordered_topics = tuple(topic_by_id[topic_id] for topic_id in ordered_topic_ids)

        study_plan_template = tuple(
            StudyPlanTopicTemplate(
                topic_id=topic.topic_id,
                topic_code=topic.code,
                topic_title=topic.title,
                section_id=topic.section_id,
                recommended_minutes=topic.estimated_minutes,
                prerequisite_ids=topic.prerequisite_ids,
            )
            for topic in ordered_topics
        )
        mission_templates = tuple(
            _mission_template_for_topic(
                topic,
                objective_by_topic.get(topic.topic_id, []),
            )
            for topic in ordered_topics
        )
        journey = tuple(
            JourneySectionNode(
                section_id=section.section_id,
                code=section.code,
                title=section.title,
                topics=tuple(
                    JourneyTopicNode(
                        topic_id=topic.topic_id,
                        topic_code=topic.code,
                        title=topic.title,
                        objective_ids=topic.learning_objective_ids,
                    )
                    for topic in ordered_topics
                    if topic.section_id == section.section_id
                ),
            )
            for section in sections
        )
        progress_model = ProgressModel(
            curriculum_identity=identity,
            section_ids=tuple(section.section_id for section in sections),
            topic_ids=tuple(topic.topic_id for topic in ordered_topics),
            objective_ids=tuple(objective.objective_id for objective in objectives),
            topics=tuple(
                ProgressTopicNode(
                    topic_id=topic.topic_id,
                    topic_code=topic.code,
                    objective_ids=topic.learning_objective_ids,
                    prerequisite_ids=topic.prerequisite_ids,
                )
                for topic in ordered_topics
            ),
        )

        return EducationalArtefactBundle(
            curriculum_identity=identity,
            subject_code=subject_code,
            version_label=version_label,
            sections=sections,
            topics=ordered_topics,
            objectives=objectives,
            graph=graph,
            study_plan_template=study_plan_template,
            mission_templates=mission_templates,
            journey=journey,
            progress_model=progress_model,
            prerequisite_edges=prerequisite_edges,
            metadata=tuple(
                (str(k).strip(), str(v).strip())
                for k, v in raw_metadata
                if str(k).strip() and str(v).strip()
            ),
        )


def _derive_sections(
    raw_sections: tuple[Any, ...],
    topics: tuple[CurriculumTopicNode, ...],
) -> tuple[CurriculumSectionNode, ...]:
    topic_ids_by_section: dict[str, list[str]] = {}
    for topic in topics:
        topic_ids_by_section.setdefault(topic.section_id, []).append(topic.topic_id)
    sections = []
    for index, raw in enumerate(raw_sections, start=1):
        section_id = _text(raw.get("section_id"), "section_id")
        sections.append(
            CurriculumSectionNode(
                section_id=section_id,
                code=str(raw.get("code") or raw.get("number") or section_id).strip(),
                title=_text(raw.get("title"), "section title"),
                number=str(raw.get("number") or index).strip(),
                display_order=_int(raw.get("order_index"), default=index),
                topic_ids=tuple(topic_ids_by_section.get(section_id, ())),
            )
        )
    return tuple(
        sorted(
            sections,
            key=lambda s: (s.display_order, s.number, s.section_id),
        )
    )


def _derive_topics(
    raw_topics: tuple[Any, ...],
    objective_by_topic: dict[str, list[CurriculumObjectiveNode]],
) -> tuple[CurriculumTopicNode, ...]:
    topics = []
    for index, raw in enumerate(raw_topics, start=1):
        topic_id = _text(raw.get("topic_id"), "topic_id")
        topic_objectives = tuple(
            objective.objective_id
            for objective in sorted(
                objective_by_topic.get(topic_id, []),
                key=lambda objective: (
                    objective.display_order,
                    objective.number,
                    objective.objective_id,
                ),
            )
        )
        prereqs = tuple(
            _text(prereq, f"prerequisite for {topic_id}")
            for prereq in tuple(raw.get("prerequisite_ids") or ())
        )
        topics.append(
            CurriculumTopicNode(
                topic_id=topic_id,
                code=student_syllabus_code(
                    code=str(raw.get("code") or "").strip(),
                    title=str(raw.get("title") or "").strip(),
                    number=str(raw.get("number") or index).strip(),
                )
                or str(raw.get("number") or index).strip(),
                title=_text(raw.get("title"), "topic title"),
                section_id=_text(raw.get("section_ref"), "topic section_ref"),
                number=str(raw.get("number") or index).strip(),
                display_order=_int(raw.get("order_index"), default=index),
                estimated_minutes=_int(
                    raw.get("estimated_minutes"),
                    default=max(30, len(topic_objectives) * 25),
                ),
                difficulty=(
                    str(raw.get("difficulty") or "foundational").strip()
                    or "foundational"
                ),
                learning_objective_ids=topic_objectives,
                prerequisite_ids=prereqs,
            )
        )
    return tuple(topics)


def _derive_objectives(
    raw_objectives: tuple[Any, ...],
) -> tuple[CurriculumObjectiveNode, ...]:
    objectives = []
    for index, raw in enumerate(raw_objectives, start=1):
        objective_id = _text(raw.get("objective_id"), "objective_id")
        objectives.append(
            CurriculumObjectiveNode(
                objective_id=objective_id,
                code=student_syllabus_code(
                    code=str(raw.get("code") or "").strip(),
                    title=str(raw.get("text") or "").strip(),
                    number=str(raw.get("number") or index).strip(),
                )
                or str(raw.get("number") or index).strip(),
                text=_text(raw.get("text"), "objective text"),
                topic_id=_text(raw.get("topic_ref"), "objective topic_ref"),
                number=str(raw.get("number") or index).strip(),
                display_order=_int(raw.get("order_index"), default=index),
                # Missing estimates → 0 (unknown). Do not invent a sitting
                # duration; a former default of 20 made every LO look identical.
                estimated_minutes=_int(raw.get("estimated_minutes"), default=0),
                learning_type=(
                    str(raw.get("learning_type") or "concept").strip()
                    or "concept"
                ),
                cognitive_level=(
                    str(raw.get("cognitive_level") or "understand").strip()
                    or "understand"
                ),
            )
        )
    return tuple(
        sorted(
            objectives,
            key=lambda objective: (
                objective.topic_id,
                objective.display_order,
                objective.number,
                objective.objective_id,
            ),
        )
    )


def _normalize_edges(
    raw_edges: tuple[Any, ...],
    topic_ids: set[str],
) -> tuple[tuple[str, str], ...]:
    edges: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for index, edge in enumerate(raw_edges, start=1):
        if not isinstance(edge, list | tuple) or len(edge) != 2:
            raise EducationalDerivationError(
                f"prerequisite edge #{index} must be a pair of topic ids"
            )
        source = _text(edge[0], "prerequisite source")
        target = _text(edge[1], "prerequisite target")
        if source not in topic_ids or target not in topic_ids:
            raise EducationalDerivationError(
                f"prerequisite edge {source}->{target} references unknown topic"
            )
        if source == target:
            raise EducationalDerivationError(
                f"prerequisite edge {source}->{target} cannot self-reference"
            )
        pair = (source, target)
        if pair in seen:
            continue
        seen.add(pair)
        edges.append(pair)
    return tuple(edges)


def _derive_graph(
    topics: tuple[CurriculumTopicNode, ...],
    prerequisite_edges: tuple[tuple[str, str], ...],
) -> CurriculumGraph:
    domain_topics = [
        Topic.create(
            topic.topic_id,
            topic.title,
            difficulty=topic.difficulty,
            estimated_effort_minutes=topic.estimated_minutes,
            learning_objective_refs=list(topic.learning_objective_ids),
            sequence_index=max(0, topic.display_order - 1),
            metadata={
                "topic_code": topic.code,
                "topic_number": topic.number,
                "section_id": topic.section_id,
            },
        )
        for topic in topics
    ]
    prereqs = [
        Prerequisite.create(
            f"{source}->{target}",
            source,
            target,
            rationale="published_curriculum_prerequisite",
        )
        for source, target in prerequisite_edges
    ]
    return GraphBuilder().build_from_topics(domain_topics, prerequisites=prereqs)


def _derive_topic_order(
    topics: tuple[CurriculumTopicNode, ...],
    prerequisite_edges: tuple[tuple[str, str], ...],
) -> tuple[str, ...]:
    base_order = [topic.topic_id for topic in topics]
    base_rank = {topic_id: index for index, topic_id in enumerate(base_order)}
    incoming: dict[str, int] = {topic_id: 0 for topic_id in base_order}
    dependents: dict[str, list[str]] = {topic_id: [] for topic_id in base_order}
    for source, target in prerequisite_edges:
        incoming[source] += 1
        dependents[target].append(source)

    ready = [topic_id for topic_id in base_order if incoming[topic_id] == 0]
    ordered: list[str] = []
    while ready:
        ready.sort(key=lambda topic_id: base_rank[topic_id])
        current = ready.pop(0)
        ordered.append(current)
        for dependent in dependents[current]:
            incoming[dependent] -= 1
            if incoming[dependent] == 0:
                ready.append(dependent)

    if len(ordered) != len(base_order):
        raise EducationalDerivationError(
            "graph topic ordering did not cover all topics"
        )
    return tuple(ordered)


def _mission_template_for_topic(
    topic: CurriculumTopicNode,
    objectives: list[CurriculumObjectiveNode],
) -> MissionTemplate:
    human_code = student_syllabus_code(
        code=topic.code,
        title=topic.title,
        number=topic.number,
    ) or topic.number or topic.code
    task_descriptions = [student_mission_title(code=human_code, title=topic.title)]
    if objectives:
        lead = objectives[0]
        lead_code = student_syllabus_code(
            code=lead.code, title=lead.text, number=lead.number
        ) or lead.number
        task_descriptions.append(
            f"Work through objective {lead_code}: {lead.text}"
            if lead_code
            else f"Work through: {lead.text}"
        )
    if len(objectives) > 1:
        task_descriptions.append(
            f"Consolidate {len(objectives)} learning objectives for {human_code}"
        )
    objective_codes = tuple(
        student_syllabus_code(code=o.code, title=o.text, number=o.number)
        or o.number
        or o.text
        for o in objectives
    )
    duration = topic.estimated_minutes
    if duration <= 0:
        duration = max(30, sum(max(0, o.estimated_minutes) for o in objectives) or 30)
    return MissionTemplate(
        template_id=f"{topic.topic_id}:learn",
        topic_id=topic.topic_id,
        topic_code=human_code,
        mission_kind="learn_topic",
        title=student_mission_title(code=human_code, title=topic.title),
        task_descriptions=tuple(task_descriptions),
        objective_ids=tuple(objective.objective_id for objective in objectives),
        estimated_duration_minutes=duration,
        completion_definition=build_mission_completion_definition(
            topic_code=human_code
        ),
        educational_rationale=build_mission_educational_rationale(
            topic_code=human_code,
            topic_title=topic.title,
            objective_codes=objective_codes,
            prerequisite_ids=topic.prerequisite_ids,
        ),
        prerequisite_ids=topic.prerequisite_ids,
    )


def _text(value: Any, field_name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise EducationalDerivationError(f"{field_name} is required")
    return text


def _int(value: Any, *, default: int) -> int:
    if value in (None, ""):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
