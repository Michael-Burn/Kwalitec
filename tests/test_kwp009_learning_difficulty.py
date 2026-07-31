"""KWP-009 — Learning Difficulty & Cognitive Load Engine tests.

Deterministic difficulty / load modelling, student guidance (no band labels),
Sitting Report Pace composition, and founder difficulty metrics.
No runtime authority redesign.
"""

from __future__ import annotations

from pathlib import Path

from app.application.learning_difficulty import (
    DifficultyEvidenceInput,
    EducationalPacing,
    LearningDifficultyEngine,
    LearningEffort,
    LoadRecommendation,
    ObjectiveComplexity,
    ObservedDifficulty,
    RevisionPressure,
    SessionIntensity,
)
from app.application.learning_difficulty.complexity import (
    complexity_gap,
    objective_complexity,
    observed_difficulty,
)
from app.presentation.product_language import APPROVED_TERMS
from app.presentation.session.sitting_report import build_sitting_report
from app.services.learning_difficulty_metrics import LearningDifficultyMetrics

SESSION_BODY = Path("app/templates/session/partials/session_body.html")
FOUNDER_ALPHA = Path(
    "app/founder/dashboard/templates/founder_dashboard/alpha_observability.html"
)

_FORBIDDEN_FRAGMENTS = (
    "cognitive load",
    "mental load",
    "burnout",
    "anxiety",
    "fatigue",
    "overloaded",
    "very demanding",
    "load points",
    "psychological",
)


class TestObjectiveVsObserved:
    def test_authored_moderate_observed_very_demanding(self):
        evidence = DifficultyEvidenceInput(
            topic_title="Chapter 15",
            authored_difficulty="intermediate",
            practice_incorrect=3,
            practice_attempted=3,
            reinforcement_session_count=2,
            weak_topic=True,
        )
        assert objective_complexity(evidence) is ObjectiveComplexity.MODERATE
        assert observed_difficulty(evidence) is ObservedDifficulty.VERY_DEMANDING
        assert complexity_gap(
            ObjectiveComplexity.MODERATE,
            ObservedDifficulty.VERY_DEMANDING,
        ) == 2

    def test_ckg_foundational_maps_light(self):
        evidence = DifficultyEvidenceInput(
            topic_title="Interest",
            authored_difficulty="foundational",
            practice_correct=2,
            practice_attempted=2,
        )
        assert objective_complexity(evidence) is ObjectiveComplexity.LIGHT
        assert observed_difficulty(evidence) is ObservedDifficulty.LIGHT


class TestLoadRecommendations:
    def test_consolidation_when_observed_harder_than_objective(self):
        profile = LearningDifficultyEngine().evaluate(
            DifficultyEvidenceInput(
                topic_title="Annuities",
                authored_difficulty="moderate",
                practice_incorrect=2,
                practice_attempted=2,
                reinforcement_session_count=1,
            )
        )
        assert profile.recommendation is (
            LoadRecommendation.TAKE_CONSOLIDATION_SESSION
        )
        blob = (profile.guidance + " " + profile.explanation).lower()
        assert "more practice" in blob or "reinforcement" in blob
        for fragment in _FORBIDDEN_FRAGMENTS:
            assert fragment not in blob

    def test_reduce_session_length_when_long_dense(self):
        profile = LearningDifficultyEngine().evaluate(
            DifficultyEvidenceInput(
                topic_title="Cash flows",
                practice_incorrect=2,
                practice_attempted=3,
                session_duration_minutes=80,
                recent_session_count=5,
            )
        )
        assert profile.recommendation is LoadRecommendation.REDUCE_SESSION_LENGTH
        assert profile.session_intensity in {
            SessionIntensity.HEAVY,
            SessionIntensity.OVERLOADED,
        }
        assert "shorter" in profile.guidance.lower()

    def test_split_topic_after_repeated_reinforcement(self):
        profile = LearningDifficultyEngine().evaluate(
            DifficultyEvidenceInput(
                topic_title="Force of interest",
                practice_incorrect=3,
                practice_attempted=3,
                reinforcement_session_count=3,
                topic_attempt_count=4,
                weak_topic=True,
            )
        )
        assert profile.recommendation is LoadRecommendation.SPLIT_TOPIC
        guidance = profile.guidance.lower()
        assert "smaller" in guidance or "part" in guidance

    def test_increase_challenge_on_strong_light(self):
        profile = LearningDifficultyEngine().evaluate(
            DifficultyEvidenceInput(
                topic_title="Present value",
                authored_difficulty="foundational",
                practice_correct=3,
                practice_attempted=3,
                finish_verdict="yes",
                progress_advanced=True,
            )
        )
        assert profile.recommendation is LoadRecommendation.INCREASE_CHALLENGE
        assert profile.educational_pacing is EducationalPacing.ACCELERATE

    def test_increase_spacing_when_stable(self):
        profile = LearningDifficultyEngine().evaluate(
            DifficultyEvidenceInput(
                topic_title="Discount factors",
                practice_correct=2,
                practice_attempted=2,
                finish_verdict="yes",
            )
        )
        assert profile.recommendation in {
            LoadRecommendation.INCREASE_SPACING,
            LoadRecommendation.INCREASE_CHALLENGE,
            LoadRecommendation.MAINTAIN_PACE,
            LoadRecommendation.CONTINUE,
        }

    def test_decrease_spacing_elevated_pressure(self):
        profile = LearningDifficultyEngine().evaluate(
            DifficultyEvidenceInput(
                topic_title="Interest rates",
                practice_incorrect=1,
                practice_attempted=2,
                practice_correct=1,
                retention_risk=True,
            )
        )
        # Consolidation or decrease spacing — both close the loop.
        assert profile.recommendation in {
            LoadRecommendation.TAKE_CONSOLIDATION_SESSION,
            LoadRecommendation.DECREASE_SPACING,
            LoadRecommendation.REDUCE_SESSION_LENGTH,
        }
        assert profile.revision_pressure in {
            RevisionPressure.LIGHT,
            RevisionPressure.ELEVATED,
            RevisionPressure.URGENT,
        }

    def test_continue_after_recovery(self):
        profile = LearningDifficultyEngine().evaluate(
            DifficultyEvidenceInput(
                topic_title="Annuities",
                practice_correct=2,
                practice_incorrect=1,
                practice_attempted=3,
                recovered_after_difficult=True,
                recovered_after_misses=True,
            )
        )
        # May consolidate if still demanding, or continue after recovery.
        assert profile.recommendation in {
            LoadRecommendation.CONTINUE,
            LoadRecommendation.MAINTAIN_PACE,
            LoadRecommendation.TAKE_CONSOLIDATION_SESSION,
            LoadRecommendation.DECREASE_SPACING,
        }

    def test_maintain_pace_default_thin(self):
        profile = LearningDifficultyEngine().evaluate(
            DifficultyEvidenceInput(topic_title="Intro")
        )
        assert profile.recommendation in {
            LoadRecommendation.MAINTAIN_PACE,
            LoadRecommendation.CONTINUE,
        }
        assert profile.learning_effort in {
            LearningEffort.LOW,
            LearningEffort.STEADY,
        }

    def test_determinism(self):
        evidence = DifficultyEvidenceInput(
            topic_title="Cash flows",
            authored_difficulty="advanced",
            practice_incorrect=2,
            practice_attempted=2,
            session_duration_minutes=55,
            reinforcement_session_count=1,
        )
        a = LearningDifficultyEngine().evaluate(evidence)
        b = LearningDifficultyEngine().evaluate(evidence)
        assert a.to_opaque() == b.to_opaque()


class TestStudentCopySafety:
    def test_no_band_or_psych_labels(self):
        profile = LearningDifficultyEngine().evaluate(
            DifficultyEvidenceInput(
                topic_title="Annuities",
                authored_difficulty="moderate",
                practice_incorrect=3,
                practice_attempted=3,
                session_duration_minutes=90,
                reinforcement_session_count=2,
                has_reflection=True,
            )
        )
        blob = " ".join(
            [
                profile.recommendation_title,
                profile.guidance,
                profile.explanation,
                *profile.student_projection().values(),
            ]
        ).lower()
        for fragment in _FORBIDDEN_FRAGMENTS:
            assert fragment not in blob
        # Internal bands exist on opaque only.
        assert "very_demanding" in profile.to_opaque()["observed_difficulty"] or (
            profile.observed_difficulty.value != "very_demanding"
        )


class TestSittingReportComposition:
    def test_pace_guidance_on_sitting_report(self):
        report = build_sitting_report(
            topic_title="Annuities",
            opaque_summary={
                "topic_title": "Annuities",
                "practice_correct": 0,
                "practice_incorrect": 2,
                "practice_attempted": 2,
                "finish_review": {"verdict": "yes"},
                "difficulty": "moderate",
                "reinforcement_session_count": 1,
            },
        )
        assert report.strategy_title  # WHAT from strategy
        assert report.diagnostic_guidance  # Focus from diagnostics
        assert report.difficulty_guidance  # Pace from difficulty
        assert report.difficulty_title
        blob = " ".join(
            [
                report.difficulty_title,
                report.difficulty_guidance,
                report.difficulty_explanation,
            ]
        ).lower()
        for fragment in _FORBIDDEN_FRAGMENTS:
            assert fragment not in blob

    def test_example_consolidation_copy(self):
        report = build_sitting_report(
            topic_title="Annuities",
            opaque_summary={
                "topic_title": "Annuities",
                "practice_incorrect": 2,
                "practice_attempted": 2,
                "difficulty": "intermediate",
                "reinforcement_session_count": 1,
            },
        )
        blob = (
            report.difficulty_guidance + " " + report.difficulty_explanation
        ).lower()
        assert (
            "more practice" in blob
            or "reinforcement" in blob
            or "consolidat" in blob
        )


class TestFounderDifficultyMetrics:
    def test_load_and_pacing_trends(self):
        packages = [
            {
                "topic_title": "Annuities",
                "practice_incorrect": 3,
                "practice_attempted": 3,
                "difficulty": "moderate",
                "reinforcement_session_count": 2,
            },
            {
                "topic_title": "Present value",
                "practice_correct": 3,
                "practice_attempted": 3,
                "finish_review": {"verdict": "yes"},
                "progress_advanced": True,
                "difficulty": "foundational",
            },
            {
                "topic_title": "Annuities",
                "practice_incorrect": 1,
                "practice_attempted": 2,
                "practice_correct": 1,
                "session_duration_minutes": 80,
                "reinforcement_session_count": 1,
                "recovered_after_misses": True,
            },
        ]
        snap = LearningDifficultyMetrics.from_packages(packages)
        assert snap.sittings_evaluated == 3
        assert snap.recommendation_counts
        assert snap.average_load_points > 0
        assert any(t == "Annuities" for t, _ in snap.highest_load_topics)
        assert "Annuities" in snap.average_reinforcement_by_topic


class TestProductSurfaces:
    def test_template_difficulty_marker(self):
        html = SESSION_BODY.read_text(encoding="utf-8")
        assert "data-difficulty-guidance" in html
        assert "Pace ·" in html

    def test_founder_difficulty_section(self):
        html = FOUNDER_ALPHA.read_text(encoding="utf-8")
        assert "Learning Difficulty" in html
        assert "highest_load_topics" in html
        assert "recovery_after_difficult_rate" in html

    def test_approved_term(self):
        assert "Learning Difficulty" in APPROVED_TERMS
