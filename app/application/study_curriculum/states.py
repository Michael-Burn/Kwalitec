"""Four honest learning states for Study's Curriculum view.

These are a read-side join of Study Progress coverage and Twin Estimated
Knowledge. They are not a new educational authority and do not write Twin
state, Study Progress, or ADR-027 decisions.

Thresholds are the existing project constants, not new numbers:
``POLICY_V1_MIN_EVIDENCE`` (evidence-reliability floor) and
``EK_MASTERED_THRESHOLD`` (mastery bar used by ``is_ek_mastered``).
"""

from __future__ import annotations

from enum import StrEnum

from app.application.adaptive_decision.types import POLICY_V1_MIN_EVIDENCE
from app.application.learner_progress.milestones import EK_MASTERED_THRESHOLD

EVIDENCE_RELIABILITY_FLOOR = POLICY_V1_MIN_EVIDENCE
MASTERY_THRESHOLD = EK_MASTERED_THRESHOLD


class TopicLearningState(StrEnum):
    """One honest learning state per syllabus topic."""

    NOT_STARTED = "not_started"
    NOT_YET_ASSESSED = "not_yet_assessed"
    DEVELOPING = "developing"
    MASTERED = "mastered"
