"""Student Experience Integration — PX-002.

Transforms separate Student Experience modules into one continuous
learning journey.

Responsibilities
    Orchestrate Home, Workspace, Reflection, Journey, Readiness, and Coach
    into a single refresh / navigation flow.
    Resolve state-aware primary CTAs.
    Surface readiness changes and empty / success states.

Non-responsibilities
    Educational reasoning, new domain capabilities, Education OS changes,
    persistence, UI rendering, or LLM calls.
"""

from __future__ import annotations

from application.student_experience.integration.enums import (
    CascadeStep,
    IntegrationTrigger,
    JourneySurface,
)
from application.student_experience.integration.errors import (
    IntegrationExperienceError,
    IntegrationInvariantViolation,
)
from application.student_experience.integration.experience_integration_service import (
    ExperienceIntegrationService,
)
from application.student_experience.integration.ids import ExperienceBundleId
from application.student_experience.integration.integration_composer import (
    aligned_module_inputs,
    compose_experience,
    compose_readiness_change,
    compose_surface_states,
)
from application.student_experience.integration.integration_inputs import (
    IntegrationInputs,
)
from application.student_experience.integration.models import (
    ExperienceJourneyViewModel,
    ExperienceSnapshotBundle,
    IntegratedNextAction,
    ReadinessChangeNotice,
    SurfaceState,
)
from application.student_experience.integration.navigation import (
    action_key_for_focus,
    destination_for_action,
    next_action_from_focus,
)
from application.student_experience.integration.ports import (
    ExperienceIntegrationPublisher,
)

__all__ = [
    # Service
    "ExperienceIntegrationService",
    # Inputs
    "IntegrationInputs",
    # Identity
    "ExperienceBundleId",
    # View models
    "ExperienceJourneyViewModel",
    "ExperienceSnapshotBundle",
    "IntegratedNextAction",
    "ReadinessChangeNotice",
    "SurfaceState",
    # Helpers
    "aligned_module_inputs",
    "compose_experience",
    "compose_readiness_change",
    "compose_surface_states",
    "action_key_for_focus",
    "destination_for_action",
    "next_action_from_focus",
    # Enums
    "CascadeStep",
    "IntegrationTrigger",
    "JourneySurface",
    # Errors
    "IntegrationExperienceError",
    "IntegrationInvariantViolation",
    # Ports
    "ExperienceIntegrationPublisher",
]
