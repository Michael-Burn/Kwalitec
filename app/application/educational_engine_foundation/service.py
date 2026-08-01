"""Application service for PI-001B Educational Engine Foundation."""

from __future__ import annotations

from app.application.curriculum_studio_foundation.authority import (
    PublishedCurriculumAuthority,
)
from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
    GraphSnapshot,
    JourneySnapshot,
    MissionTemplateSnapshot,
    ProgressModelSnapshot,
    StudyPlanTemplateSnapshot,
)
from app.domain.educational_engine_foundation import EducationalArtefactDeriver


class EducationalEngineFoundationService:
    """Derive student-learning artefacts from published curriculum packages."""

    SERVICE_ID = "educational_engine_foundation"
    SERVICE_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        authority: PublishedCurriculumAuthority | None = None,
        deriver: EducationalArtefactDeriver | None = None,
    ) -> None:
        self._authority = authority or PublishedCurriculumAuthority()
        self._deriver = deriver or EducationalArtefactDeriver()

    def derive_active(self, subject_code: str) -> EducationalArtefactSnapshot | None:
        package = self._authority.get_active(subject_code)
        if package is None:
            return None
        return self.derive_from_package(package.package)

    def derive_version(
        self, subject_code: str, version_label: str
    ) -> EducationalArtefactSnapshot | None:
        package = self._authority.get_by_version_label(subject_code, version_label)
        if package is None:
            return None
        return self.derive_from_package(package.package)

    def derive_from_package(self, package: dict) -> EducationalArtefactSnapshot:
        bundle = self._deriver.derive(package)
        subject = bundle.subject_code
        mission_templates = tuple(
            self._overlay_mission_template(template, subject_code=subject)
            for template in bundle.mission_templates
        )
        return EducationalArtefactSnapshot(
            curriculum_identity=bundle.curriculum_identity,
            subject_code=bundle.subject_code,
            version_label=bundle.version_label,
            sections=tuple(
                {
                    "section_id": section.section_id,
                    "code": section.code,
                    "title": section.title,
                    "number": section.number,
                    "display_order": section.display_order,
                    "topic_ids": section.topic_ids,
                }
                for section in bundle.sections
            ),
            topics=tuple(
                {
                    "topic_id": topic.topic_id,
                    "code": topic.code,
                    "title": topic.title,
                    "section_id": topic.section_id,
                    "number": topic.number,
                    "display_order": topic.display_order,
                    "estimated_minutes": topic.estimated_minutes,
                    "difficulty": topic.difficulty,
                    "learning_objective_ids": topic.learning_objective_ids,
                    "prerequisite_ids": topic.prerequisite_ids,
                }
                for topic in bundle.topics
            ),
            objectives=tuple(
                {
                    "objective_id": objective.objective_id,
                    "code": objective.code,
                    "text": objective.text,
                    "topic_id": objective.topic_id,
                    "number": objective.number,
                    "display_order": objective.display_order,
                    "estimated_minutes": objective.estimated_minutes,
                    "learning_type": objective.learning_type,
                    "cognitive_level": objective.cognitive_level,
                }
                for objective in bundle.objectives
            ),
            graph=GraphSnapshot(
                topic_ids=tuple(node.topic_id.value for node in bundle.graph.nodes()),
                prerequisite_edges=tuple(
                    (
                        edge.source_id.value,
                        edge.target_id.value,
                    )
                    for edge in bundle.graph.edges()
                ),
                topological_order=tuple(
                    topic_id.value for topic_id in bundle.graph.topological_ordering()
                ),
            ),
            study_plan_template=StudyPlanTemplateSnapshot(
                curriculum_identity=bundle.curriculum_identity,
                subject_code=bundle.subject_code,
                version_label=bundle.version_label,
                topic_templates=tuple(
                    {
                        "topic_id": topic.topic_id,
                        "topic_code": topic.topic_code,
                        "topic_title": topic.topic_title,
                        "section_id": topic.section_id,
                        "recommended_minutes": topic.recommended_minutes,
                        "prerequisite_ids": topic.prerequisite_ids,
                    }
                    for topic in bundle.study_plan_template
                ),
            ),
            mission_templates=mission_templates,
            journey=JourneySnapshot(
                curriculum_identity=bundle.curriculum_identity,
                sections=tuple(
                    {
                        "section_id": section.section_id,
                        "code": section.code,
                        "title": section.title,
                        "topics": tuple(
                            {
                                "topic_id": topic.topic_id,
                                "topic_code": topic.topic_code,
                                "title": topic.title,
                                "objective_ids": topic.objective_ids,
                            }
                            for topic in section.topics
                        ),
                    }
                    for section in bundle.journey
                ),
            ),
            progress_model=ProgressModelSnapshot(
                curriculum_identity=bundle.progress_model.curriculum_identity,
                topic_ids=bundle.progress_model.topic_ids,
                objective_ids=bundle.progress_model.objective_ids,
                topics=tuple(
                    {
                        "topic_id": topic.topic_id,
                        "topic_code": topic.topic_code,
                        "objective_ids": topic.objective_ids,
                        "prerequisite_ids": topic.prerequisite_ids,
                    }
                    for topic in bundle.progress_model.topics
                ),
            ),
            metadata=bundle.metadata,
        )

    @staticmethod
    def _overlay_mission_template(
        template, *, subject_code: str
    ) -> MissionTemplateSnapshot:
        """Apply certified package fields without changing selection."""
        from app.application.educational_packages.loader import (
            find_educational_package,
        )

        pack = find_educational_package(
            topic_id=template.topic_id,
            topic_code=template.topic_code,
            topic_title=template.title,
            subject_id=subject_code,
        )
        title = template.title
        tasks = template.task_descriptions
        rationale = template.educational_rationale
        duration = template.estimated_duration_minutes
        if pack is not None:
            title = pack.display_title or title
            if pack.task_descriptions:
                tasks = pack.task_descriptions
            rationale = pack.educational_rationale or rationale
            duration = pack.estimated_duration_minutes or duration
        return MissionTemplateSnapshot(
            template_id=template.template_id,
            topic_id=template.topic_id,
            topic_code=template.topic_code,
            mission_kind=template.mission_kind,
            title=title,
            task_descriptions=tasks,
            objective_ids=template.objective_ids,
            estimated_duration_minutes=duration,
            completion_definition=template.completion_definition,
            educational_rationale=rationale,
            prerequisite_ids=template.prerequisite_ids,
        )
