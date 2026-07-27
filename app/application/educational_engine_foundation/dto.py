"""Immutable snapshots for PI-001B derived educational artefacts."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class GraphSnapshot:
    topic_ids: tuple[str, ...] = field(default_factory=tuple)
    prerequisite_edges: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    topological_order: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class StudyPlanTemplateSnapshot:
    curriculum_identity: str
    subject_code: str
    version_label: str
    topic_templates: tuple[dict, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class MissionTemplateSnapshot:
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
class JourneySnapshot:
    curriculum_identity: str
    sections: tuple[dict, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ProgressModelSnapshot:
    curriculum_identity: str
    topic_ids: tuple[str, ...] = field(default_factory=tuple)
    objective_ids: tuple[str, ...] = field(default_factory=tuple)
    topics: tuple[dict, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class EducationalArtefactSnapshot:
    curriculum_identity: str
    subject_code: str
    version_label: str
    sections: tuple[dict, ...] = field(default_factory=tuple)
    topics: tuple[dict, ...] = field(default_factory=tuple)
    objectives: tuple[dict, ...] = field(default_factory=tuple)
    graph: GraphSnapshot = field(default_factory=GraphSnapshot)
    study_plan_template: StudyPlanTemplateSnapshot | None = None
    mission_templates: tuple[MissionTemplateSnapshot, ...] = field(
        default_factory=tuple
    )
    journey: JourneySnapshot | None = None
    progress_model: ProgressModelSnapshot | None = None
    metadata: tuple[tuple[str, str], ...] = field(default_factory=tuple)
