"""MissionPromptBuilder — deterministic mission enrichment prompts.

Architecture Source
    AI-001 Educational Enrichment Layer
Concept
    Mission Prompt Builder
"""

from __future__ import annotations

from domain.mission_generation.mission_specification import MissionSpecification
from domain.student_experience.student_experience import StudentExperience
from infrastructure.ai.prompting.prompt_builder import PromptBuilder
from infrastructure.ai.providers.ai_provider import PromptDocument

PURPOSE = "mission_enrichment"


class MissionPromptBuilder(PromptBuilder):
    """Build deterministic prompts for MissionSpecification enrichment.

    Same mission and experience always yield the same PromptDocument.
    Educational fields are quoted for context; the model is forbidden from
    changing them.
    """

    def build(
        self,
        mission: MissionSpecification,
        experience: StudentExperience,
    ) -> PromptDocument:
        if not isinstance(mission, MissionSpecification):
            raise TypeError("mission must be a MissionSpecification")
        if not isinstance(experience, StudentExperience):
            raise TypeError("experience must be a StudentExperience")
        if mission.student_id != experience.student_id:
            raise ValueError(
                "mission and experience must share the same student_id"
            )
        if mission.mission_id != experience.mission_id:
            raise ValueError(
                "mission and experience must reference the same mission_id"
            )

        system = self.system_preamble(role="learner mission presentation")
        user = "\n".join(
            (
                "Enrich the following MissionSpecification for learner presentation.",
                "",
                f"mission_id: {mission.mission_id.value}",
                f"student_id: {mission.student_id}",
                f"objective_statement: {mission.objective.statement}",
                f"priority_band: {mission.priority.band.value}",
                f"priority_urgency: {mission.priority.urgency.value}",
                f"duration_minutes: {mission.duration.planned_minutes}",
                f"duration_band: {mission.duration.band.value}",
                self.format_lines(
                    "sequence_tasks",
                    tuple(
                        f"{task.sequence_index}. {task.label} "
                        f"({task.estimated_minutes}m, {task.strategy_type.value})"
                        for task in mission.sequence.tasks
                    ),
                ),
                f"educational_rationale: {mission.educational_rationale}",
                "",
                "StudentExperience context (presentation only):",
                f"experience_id: {experience.experience_id.value}",
                f"motivation_tone: {experience.motivation.tone.value}",
                f"motivation_message: {experience.motivation.message}",
                f"presentation_narrative: {experience.presentation_narrative}",
                f"streak_days: {experience.streak.current_days}",
                "",
                "Preserve objective, priority, duration, sequence, and "
                "educational rationale exactly. Enrich presentation only.",
            )
        )
        return PromptDocument(system=system, user=user, purpose=PURPOSE)
