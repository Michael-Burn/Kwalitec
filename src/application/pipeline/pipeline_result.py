"""PipelineResult — output of the Educational Pipeline Orchestrator.

Architecture Source
    APP-002 Educational Pipeline Orchestrator

Contains every Educational OS artefact produced by the ordered pipeline.
Enhanced mission / recommendation views are presentation wrappers; when AI
enrichment is unavailable they hold deterministic passthrough content.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from domain.explainability import EducationalExplanation
from domain.mission_generation import MissionSpecification
from domain.progress_evaluation import ProgressReport
from domain.recommendation import RecommendationSpecification
from domain.student_experience import StudentExperience
from domain.study_planning import StudyPlan


@runtime_checkable
class EnhancedMissionView(Protocol):
    """Presentation enrichment around a MissionSpecification.

    Satisfied by infrastructure ``EnhancedMission`` and by the deterministic
    passthrough produced when AI enrichment is unavailable.
    """

    @property
    def specification(self) -> MissionSpecification: ...

    @property
    def improved_wording(self) -> str: ...

    @property
    def examples(self) -> tuple[str, ...]: ...

    @property
    def analogies(self) -> tuple[str, ...]: ...

    @property
    def adapted_tone(self) -> str: ...

    @property
    def worked_examples(self) -> tuple[str, ...]: ...

    @property
    def revision_tips(self) -> tuple[str, ...]: ...

    @property
    def provider_name(self) -> str: ...


@runtime_checkable
class EnhancedRecommendationsView(Protocol):
    """Presentation enrichment around a RecommendationSpecification.

    Milestone alias: EnhancedRecommendations. Satisfied by infrastructure
    ``EnhancedRecommendation`` and by deterministic passthroughs.
    """

    @property
    def specification(self) -> RecommendationSpecification: ...

    @property
    def improved_wording(self) -> str: ...

    @property
    def examples(self) -> tuple[str, ...]: ...

    @property
    def analogies(self) -> tuple[str, ...]: ...

    @property
    def adapted_tone(self) -> str: ...

    @property
    def worked_examples(self) -> tuple[str, ...]: ...

    @property
    def revision_tips(self) -> tuple[str, ...]: ...

    @property
    def provider_name(self) -> str: ...


@dataclass(frozen=True, slots=True)
class DeterministicEnhancedMission:
    """AI-free enrichment wrapper preserving Educational OS mission decisions."""

    specification: MissionSpecification
    improved_wording: str
    examples: tuple[str, ...]
    analogies: tuple[str, ...]
    adapted_tone: str
    worked_examples: tuple[str, ...]
    revision_tips: tuple[str, ...]
    provider_name: str = "none"


@dataclass(frozen=True, slots=True)
class DeterministicEnhancedRecommendations:
    """AI-free enrichment wrapper preserving recommendation decisions."""

    specification: RecommendationSpecification
    improved_wording: str
    examples: tuple[str, ...]
    analogies: tuple[str, ...]
    adapted_tone: str
    worked_examples: tuple[str, ...]
    revision_tips: tuple[str, ...]
    provider_name: str = "none"


def deterministic_enhanced_mission(
    mission: MissionSpecification,
) -> DeterministicEnhancedMission:
    """Build presentation enrichment from the mission alone (no AI)."""
    return DeterministicEnhancedMission(
        specification=mission,
        improved_wording=mission.objective.statement,
        examples=(),
        analogies=(),
        adapted_tone="clear and steady",
        worked_examples=(),
        revision_tips=(),
        provider_name="none",
    )


def deterministic_enhanced_recommendations(
    recommendations: RecommendationSpecification,
) -> DeterministicEnhancedRecommendations:
    """Build presentation enrichment from recommendations alone (no AI)."""
    return DeterministicEnhancedRecommendations(
        specification=recommendations,
        improved_wording=recommendations.educational_rationale,
        examples=(),
        analogies=(),
        adapted_tone="clear and steady",
        worked_examples=(),
        revision_tips=(),
        provider_name="none",
    )


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """Complete Educational Pipeline cargo after a successful run.

    Attributes:
        mission: Generated MissionSpecification.
        study_plan: Built StudyPlan.
        progress_report: Evaluated ProgressReport.
        recommendations: RecommendationSpecification aggregate (ordered set).
        explanation: EducationalExplanation of the decisions.
        student_experience: Learner-facing StudentExperience.
        enhanced_mission: Mission presentation enrichment (AI or deterministic).
        enhanced_recommendations: Recommendation presentation enrichment.
        stages_completed: Ordered stage names executed for this run.
    """

    mission: MissionSpecification
    study_plan: StudyPlan
    progress_report: ProgressReport
    recommendations: RecommendationSpecification
    explanation: EducationalExplanation
    student_experience: StudentExperience
    enhanced_mission: EnhancedMissionView
    enhanced_recommendations: EnhancedRecommendationsView
    stages_completed: tuple[str, ...]

    @property
    def recommendation_specifications(self) -> tuple[RecommendationSpecification, ...]:
        """RecommendationSpecification set produced by this run (length 1)."""
        return (self.recommendations,)
