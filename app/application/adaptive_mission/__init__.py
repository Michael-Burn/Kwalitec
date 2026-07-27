"""Adaptive Mission Engine application package (AME-001).

Consumes Student Digital Twin, Educational Reasoning decisions, Learning Graph
structure, and Curriculum Retrieval evidence. Never performs educational
reasoning itself. No LLM.
"""

from __future__ import annotations

from app.application.adaptive_mission.adaptive_mission_service import (
    AdaptiveMissionService,
)

__all__ = ["AdaptiveMissionService"]
