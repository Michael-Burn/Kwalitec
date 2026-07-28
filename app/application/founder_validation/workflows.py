"""Version 1 student journey workflow catalogue for FV-001.

Defines the ordered surfaces the founder must exercise during dogfooding.
No educational reasoning — identifiers and touchpoint labels only.
"""

from __future__ import annotations

from app.application.founder_validation.dto import WorkflowStep

VERSION_1_STUDENT_JOURNEY: tuple[WorkflowStep, ...] = (
    WorkflowStep(
        step_id="registration",
        name="Registration / account access",
        surface="auth",
        ei_touchpoint="None (access gate)",
        journal_required=False,
    ),
    WorkflowStep(
        step_id="study_plan",
        name="Study Plan",
        surface="study_plan",
        ei_touchpoint="LP-001 onboard after create (when published CKG)",
    ),
    WorkflowStep(
        step_id="sci_creation",
        name="SCI creation",
        surface="learner_lifecycle",
        ei_touchpoint="EI-004 Student Curriculum Instance",
    ),
    WorkflowStep(
        step_id="curriculum_binding",
        name="Curriculum binding",
        surface="learner_lifecycle",
        ei_touchpoint="EI-004 node state initialisation",
    ),
    WorkflowStep(
        step_id="dashboard",
        name="Dashboard / Student Home",
        surface="dashboard",
        ei_touchpoint="RI-001 Experience Models (Preferred Authority)",
    ),
    WorkflowStep(
        step_id="daily_mission",
        name="Daily Mission",
        surface="mission",
        ei_touchpoint="RI-001 / EX-001 mission framing",
    ),
    WorkflowStep(
        step_id="study_session",
        name="Study Session",
        surface="session",
        ei_touchpoint="RI-001 session briefing + LP-001 evidence",
    ),
    WorkflowStep(
        step_id="learning_evidence",
        name="Learning Evidence",
        surface="learner_lifecycle",
        ei_touchpoint="EI-005 via LP-001 process_evidence",
    ),
    WorkflowStep(
        step_id="twin_refresh",
        name="Twin refresh",
        surface="learner_lifecycle",
        ei_touchpoint="EI-006 belief rebuild after evidence",
    ),
    WorkflowStep(
        step_id="educational_decisions",
        name="Educational Decisions",
        surface="learner_lifecycle",
        ei_touchpoint="EI-007 decision regeneration",
    ),
    WorkflowStep(
        step_id="experience_models",
        name="Experience Models",
        surface="educational_experience",
        ei_touchpoint="EX-001 experience transformation",
    ),
    WorkflowStep(
        step_id="revision_planner",
        name="Revision Planner",
        surface="revision",
        ei_touchpoint="RI-001 revision entries",
    ),
    WorkflowStep(
        step_id="coach",
        name="Coach",
        surface="tutor / coach",
        ei_touchpoint="RI-001 coach context",
    ),
    WorkflowStep(
        step_id="progress_tracking",
        name="Progress tracking",
        surface="progress / analytics",
        ei_touchpoint="SCI + Twin state (read paths)",
    ),
)


def workflow_catalogue() -> list[dict[str, object]]:
    """Return the Version 1 journey as serialisable dicts."""
    return [step.to_dict() for step in VERSION_1_STUDENT_JOURNEY]


def workflow_ids() -> tuple[str, ...]:
    """Ordered workflow step identifiers for issue/journal tagging."""
    return tuple(step.step_id for step in VERSION_1_STUDENT_JOURNEY)
