"""DTO package for Student Digital Twin application projections."""

from __future__ import annotations

from app.application.student_twin.dto.comparison_snapshot import ComparisonSnapshot
from app.application.student_twin.dto.evidence_summary import EvidenceSummary
from app.application.student_twin.dto.learner_snapshot import LearnerSnapshot
from app.application.student_twin.dto.mastery_summary import (
    MasterySummary,
    TopicMasteryDTO,
)
from app.application.student_twin.dto.readiness_summary import ReadinessSummary
from app.application.student_twin.dto.recommendation_snapshot import (
    RecommendationExplanation,
    RecommendationItemDTO,
    RecommendationSnapshot,
)
from app.application.student_twin.dto.twin_snapshot import TwinSnapshotDTO

__all__ = [
    "ComparisonSnapshot",
    "EvidenceSummary",
    "LearnerSnapshot",
    "MasterySummary",
    "ReadinessSummary",
    "RecommendationExplanation",
    "RecommendationItemDTO",
    "RecommendationSnapshot",
    "TopicMasteryDTO",
    "TwinSnapshotDTO",
]
