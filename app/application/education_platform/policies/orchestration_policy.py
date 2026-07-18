"""Stateless orchestration rules for the Educational Composition Layer.

Defines workflow → port step order only. No educational reasoning.
"""

from __future__ import annotations

from app.application.education_platform.exceptions import OrchestrationError

# Canonical Educational Core dependency chain (composition order).
DEPENDENCY_CHAIN: tuple[str, ...] = (
    "curriculum",
    "blueprint",
    "journey",
    "session",
    "activity",
    "mission",
)

# Named workflows exposed by EducationPlatform.
WORKFLOW_GENERATE_SUBJECT = "generate_subject"
WORKFLOW_GENERATE_JOURNEY = "generate_journey"
WORKFLOW_GENERATE_LEARNING_SESSIONS = "generate_learning_sessions"
WORKFLOW_GENERATE_LEARNING_ACTIVITIES = "generate_learning_activities"
WORKFLOW_GENERATE_DAILY_MISSIONS = "generate_daily_missions"
WORKFLOW_BUILD_PLATFORM_SNAPSHOT = "build_platform_snapshot"
WORKFLOW_VALIDATE_PLATFORM = "validate_platform"

ALL_WORKFLOWS: frozenset[str] = frozenset(
    {
        WORKFLOW_GENERATE_SUBJECT,
        WORKFLOW_GENERATE_JOURNEY,
        WORKFLOW_GENERATE_LEARNING_SESSIONS,
        WORKFLOW_GENERATE_LEARNING_ACTIVITIES,
        WORKFLOW_GENERATE_DAILY_MISSIONS,
        WORKFLOW_BUILD_PLATFORM_SNAPSHOT,
        WORKFLOW_VALIDATE_PLATFORM,
    }
)

# Port steps required before a workflow may run (prefix of DEPENDENCY_CHAIN
# plus special cases for snapshot / validate).
_WORKFLOW_STEPS: dict[str, tuple[str, ...]] = {
    WORKFLOW_GENERATE_SUBJECT: ("curriculum",),
    WORKFLOW_GENERATE_JOURNEY: ("curriculum", "blueprint", "journey"),
    WORKFLOW_GENERATE_LEARNING_SESSIONS: (
        "curriculum",
        "blueprint",
        "journey",
        "session",
    ),
    WORKFLOW_GENERATE_LEARNING_ACTIVITIES: (
        "curriculum",
        "blueprint",
        "journey",
        "session",
        "activity",
    ),
    WORKFLOW_GENERATE_DAILY_MISSIONS: (
        "curriculum",
        "blueprint",
        "journey",
        "session",
        "activity",
        "mission",
    ),
    WORKFLOW_BUILD_PLATFORM_SNAPSHOT: DEPENDENCY_CHAIN,
    WORKFLOW_VALIDATE_PLATFORM: (),
}


class OrchestrationPolicy:
    """Deterministic workflow step ordering (stateless)."""

    @staticmethod
    def known_workflows() -> frozenset[str]:
        """Return the set of supported workflow names."""
        return ALL_WORKFLOWS

    @staticmethod
    def is_known_workflow(workflow: str) -> bool:
        """True when ``workflow`` is a supported platform workflow."""
        return workflow in ALL_WORKFLOWS

    @staticmethod
    def steps_for(workflow: str) -> tuple[str, ...]:
        """Return ordered port names for ``workflow``.

        Raises:
            OrchestrationError: When the workflow name is unknown.
        """
        try:
            return _WORKFLOW_STEPS[workflow]
        except KeyError as exc:
            raise OrchestrationError(
                f"Unknown workflow: {workflow!r}"
            ) from exc

    @staticmethod
    def required_ports(workflow: str) -> frozenset[str]:
        """Return the set of ports required by ``workflow``."""
        return frozenset(OrchestrationPolicy.steps_for(workflow))

    @staticmethod
    def dependency_chain() -> tuple[str, ...]:
        """Return the canonical Educational Core composition order."""
        return DEPENDENCY_CHAIN

    @staticmethod
    def workflow_ready(
        workflow: str,
        *,
        registered: frozenset[str] | set[str],
    ) -> bool:
        """True when every required port for ``workflow`` is registered."""
        if not OrchestrationPolicy.is_known_workflow(workflow):
            return False
        required = OrchestrationPolicy.required_ports(workflow)
        return required.issubset(registered)
