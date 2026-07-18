"""Composition root — assemble the Educational Composition Layer via DI.

Wires Curriculum → Blueprint → Journey → Session → Activity → Mission
using injected ports only. Never constructs concrete engines internally.
"""

from __future__ import annotations

from app.application.education_platform.dependency_registry import DependencyRegistry
from app.application.education_platform.exceptions import CompositionError
from app.application.education_platform.policies.orchestration_policy import (
    DEPENDENCY_CHAIN,
)
from app.application.education_platform.ports.activity_port import ActivityPort
from app.application.education_platform.ports.blueprint_port import BlueprintPort
from app.application.education_platform.ports.curriculum_port import CurriculumPort
from app.application.education_platform.ports.journey_port import JourneyPort
from app.application.education_platform.ports.mission_port import MissionPort
from app.application.education_platform.ports.session_port import SessionPort


class CompositionRoot:
    """Assemble an EducationPlatform from injected Educational Core ports.

    Dependency injection only — callers supply port implementations.
    """

    @staticmethod
    def build_registry(
        *,
        curriculum: CurriculumPort | None = None,
        blueprint: BlueprintPort | None = None,
        journey: JourneyPort | None = None,
        session: SessionPort | None = None,
        activity: ActivityPort | None = None,
        mission: MissionPort | None = None,
        require_complete: bool = False,
    ) -> DependencyRegistry:
        """Register provided ports into a fresh DependencyRegistry.

        Args:
            curriculum: Curriculum Graph / navigation port.
            blueprint: Instructional Blueprint Engine port.
            journey: Learning Journey Engine port.
            session: Learning Session Runtime port.
            activity: Learning Activity Engine port.
            mission: Mission Engine / Mission Adapter port.
            require_complete: When True, raise if any required port is absent.

        Returns:
            Populated DependencyRegistry (ports only — no concrete construction).

        Raises:
            CompositionError: When require_complete and ports are missing.
        """
        registry = DependencyRegistry()
        mapping: dict[str, object | None] = {
            "curriculum": curriculum,
            "blueprint": blueprint,
            "journey": journey,
            "session": session,
            "activity": activity,
            "mission": mission,
        }
        for name in DEPENDENCY_CHAIN:
            port = mapping[name]
            if port is not None:
                registry.register(name, port)
        if require_complete:
            missing = registry.missing_names()
            if missing:
                raise CompositionError(
                    f"Incomplete composition; missing ports: {missing}"
                )
        return registry

    @staticmethod
    def assemble(
        *,
        curriculum: CurriculumPort | None = None,
        blueprint: BlueprintPort | None = None,
        journey: JourneyPort | None = None,
        session: SessionPort | None = None,
        activity: ActivityPort | None = None,
        mission: MissionPort | None = None,
        require_complete: bool = False,
        clock=None,
    ):
        """Build an EducationPlatform from injected ports.

        Returns:
            EducationPlatform ready for workflow invocation.
        """
        # Local import avoids circular dependency with platform.py
        from app.application.education_platform.platform import EducationPlatform

        registry = CompositionRoot.build_registry(
            curriculum=curriculum,
            blueprint=blueprint,
            journey=journey,
            session=session,
            activity=activity,
            mission=mission,
            require_complete=require_complete,
        )
        return EducationPlatform.from_registry(registry, clock=clock)
