"""Injected educational ports for Mission Engine 2.0.

Mission Engine V2 depends on these Protocols only — never on concrete
Journey Engine, Session Runtime, or Curriculum Navigation implementations.
"""

from __future__ import annotations

from app.application.mission_engine_v2.ports.curriculum_navigation_port import (
    CurriculumNavigationPort,
)
from app.application.mission_engine_v2.ports.journey_engine_port import (
    JourneyEnginePort,
)
from app.application.mission_engine_v2.ports.session_runtime_port import (
    SessionRuntimePort,
)

__all__ = [
    "CurriculumNavigationPort",
    "JourneyEnginePort",
    "SessionRuntimePort",
]
