"""Navigation mapping for continuous Student Experience journey (PX-002).

Maps FocusActionKind / IntegratedNextAction to journey surfaces and
adapter action keys. Routing concern helpers only — no educational logic.
"""

from __future__ import annotations

from application.student_experience.home.enums import FocusActionKind
from application.student_experience.home.models.primary_focus import PrimaryFocus
from application.student_experience.integration.enums import JourneySurface
from application.student_experience.integration.models import IntegratedNextAction

_ACTION_DESTINATION: dict[FocusActionKind, JourneySurface] = {
    FocusActionKind.START_MISSION: JourneySurface.WORKSPACE,
    FocusActionKind.RESUME_MISSION: JourneySurface.WORKSPACE,
    FocusActionKind.RESUME_SESSION: JourneySurface.WORKSPACE,
    FocusActionKind.CONTINUE_MISSION: JourneySurface.WORKSPACE,
    FocusActionKind.REVIEW_REFLECTION: JourneySurface.REFLECTION,
    FocusActionKind.PREPARE_CHECKPOINT: JourneySurface.WORKSPACE,
    FocusActionKind.VIEW_SCHEDULE: JourneySurface.HOME,
    FocusActionKind.NONE: JourneySurface.HOME,
}

_ACTION_KEY: dict[FocusActionKind, str] = {
    FocusActionKind.START_MISSION: "continue_mission",
    FocusActionKind.RESUME_MISSION: "resume_session",
    FocusActionKind.RESUME_SESSION: "resume_session",
    FocusActionKind.CONTINUE_MISSION: "continue_mission",
    FocusActionKind.REVIEW_REFLECTION: "open_reflection",
    FocusActionKind.PREPARE_CHECKPOINT: "prepare_checkpoint",
    FocusActionKind.VIEW_SCHEDULE: "view_progress",
    FocusActionKind.NONE: "return_home",
}


def destination_for_action(action_kind: FocusActionKind) -> JourneySurface:
    """Resolve which journey surface continues the student's state."""
    return _ACTION_DESTINATION.get(action_kind, JourneySurface.HOME)


def action_key_for_focus(action_kind: FocusActionKind) -> str:
    """Resolve an adapter navigation action key for a focus kind."""
    return _ACTION_KEY.get(action_kind, "return_home")


def next_action_from_focus(focus: PrimaryFocus) -> IntegratedNextAction:
    """Project PrimaryFocus into an IntegratedNextAction."""
    return IntegratedNextAction(
        action_kind=focus.action_kind,
        label=focus.action_label,
        reason=focus.reason,
        destination=destination_for_action(focus.action_kind),
        mission_id=focus.mission_id,
        preserves_context=True,
        has_action=focus.has_focus,
    )
