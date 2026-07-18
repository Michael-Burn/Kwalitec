"""Generate activity plans, session skeletons, and learning sequences.

Transforms compiled blueprints into structural activity flows.
Never generates educational content.
"""

from __future__ import annotations

from app.application.instructional_blueprint.dto.blueprint_plan import (
    ActivityPlanSlot,
    BlueprintPlan,
    LearningSequenceEntry,
    SessionSkeleton,
)
from app.application.instructional_blueprint.dto.compiled_blueprint import (
    CompiledBlueprint,
)
from app.application.instructional_blueprint.exceptions import (
    SequenceGenerationError,
)


class SequenceGenerator:
    """Produce activity plans and session skeletons from compiled blueprints."""

    def generate(
        self,
        compiled: CompiledBlueprint,
        *,
        objective_ids: list[str] | tuple[str, ...] | None = None,
    ) -> BlueprintPlan:
        """Generate a BlueprintPlan from a CompiledBlueprint.

        Args:
            compiled: Compiled instructional structure.
            objective_ids: Optional objective identities to attach structurally
                (round-robin across slots; never invents content).

        Returns:
            Immutable BlueprintPlan with activity slots, session skeleton,
            learning sequence, and effort estimates.

        Raises:
            SequenceGenerationError: When the compiled blueprint has no steps.
        """
        if not compiled.steps:
            raise SequenceGenerationError(
                "Cannot generate sequence from compiled blueprint with zero steps"
            )

        objectives = tuple(
            oid.strip()
            for oid in (objective_ids or ())
            if isinstance(oid, str) and oid.strip()
        )

        slots: list[ActivityPlanSlot] = []
        sequence: list[LearningSequenceEntry] = []
        phase_labels: list[str] = []

        for index, step in enumerate(compiled.steps):
            objective_id = (
                objectives[index % len(objectives)] if objectives else None
            )
            role = step.role or "core"
            slots.append(
                ActivityPlanSlot(
                    activity_kind=step.activity_kind,
                    sequence_index=index,
                    role=role,
                    effort_weight=step.effort_weight,
                    objective_id=objective_id,
                    metadata=step.metadata,
                )
            )
            sequence.append(
                LearningSequenceEntry(
                    sequence_index=index,
                    activity_kind=step.activity_kind,
                    role=role,
                    step_id=step.step_id,
                )
            )
            phase_labels.append(f"{index}:{step.activity_kind}:{role}")

        skeleton = SessionSkeleton(
            slot_count=len(slots),
            phase_labels=tuple(phase_labels),
            estimated_effort_units=compiled.estimated_effort_units,
            metadata=(
                f"blueprint={compiled.blueprint_id}",
                f"type={compiled.blueprint_type.value}",
                "no_content",
            ),
        )

        rationale = (
            f"blueprint={compiled.blueprint_id}",
            f"type={compiled.blueprint_type.value}",
            f"slots={len(slots)}",
            f"objectives={len(objectives)}",
            f"effort={compiled.estimated_effort_band.value}",
            "activity_plan",
            "session_skeleton",
            "learning_sequence",
            "no_content_generation",
            "no_questions",
            "no_explanations",
            "no_pdfs",
            "no_ai",
        )

        return BlueprintPlan(
            blueprint_id=compiled.blueprint_id,
            blueprint_type=compiled.blueprint_type,
            activity_slots=tuple(slots),
            session_skeleton=skeleton,
            learning_sequence=tuple(sequence),
            estimated_effort_band=compiled.estimated_effort_band,
            estimated_effort_units=compiled.estimated_effort_units,
            rationale_tags=rationale,
            objective_ids=objectives,
        )

    def session_skeleton(self, compiled: CompiledBlueprint) -> SessionSkeleton:
        """Return only the session skeleton for a compiled blueprint."""
        return self.generate(compiled).session_skeleton

    def learning_sequence(
        self, compiled: CompiledBlueprint
    ) -> tuple[LearningSequenceEntry, ...]:
        """Return only the learning sequence for a compiled blueprint."""
        return self.generate(compiled).learning_sequence
