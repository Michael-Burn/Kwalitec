"""Provenance of a Learning Event.

Identifies which subsystem or channel produced the event so Twin updates and
recommendations remain attributable (see Evidence Source in the ubiquitous
language and Learning Evidence Model).
"""

from __future__ import annotations

from enum import Enum


class EventSource(str, Enum):
    """Where Learning Event evidence originated.

    New producers are added as members without changing domain architecture.
    Future Integrations remain a reserved provenance for sensors not yet
    productised.
    """

    MANUAL = "manual"
    STUDY_PLANNER = "study_planner"
    MISSION_ENGINE = "mission_engine"
    QUIZ_ENGINE = "quiz_engine"
    MOCK_EXAM = "mock_exam"
    AI_TUTOR = "ai_tutor"
    REVISION_ENGINE = "revision_engine"
    FUTURE_INTEGRATIONS = "future_integrations"
