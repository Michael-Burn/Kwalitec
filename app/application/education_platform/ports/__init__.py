"""Port contracts for the Educational Composition Layer (interface-only)."""

from __future__ import annotations

from app.application.education_platform.ports.activity_port import ActivityPort
from app.application.education_platform.ports.blueprint_port import BlueprintPort
from app.application.education_platform.ports.curriculum_port import CurriculumPort
from app.application.education_platform.ports.journey_port import JourneyPort
from app.application.education_platform.ports.mission_port import MissionPort
from app.application.education_platform.ports.session_port import SessionPort

__all__ = [
    "ActivityPort",
    "BlueprintPort",
    "CurriculumPort",
    "JourneyPort",
    "MissionPort",
    "SessionPort",
]
