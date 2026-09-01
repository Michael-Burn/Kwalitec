"""KWP-007 — Learning Strategy Engine tests.

Deterministic educational strategy recommendations, confidence calibration
(internal only), spacing, momentum, Sitting Report projection, and founder
strategy metrics. No runtime authority redesign.
"""

from __future__ import annotations

from pathlib import Path

from app.application.learning_session.dto.candidate_observation import (
    RuntimeEvidenceType,
)
from app.application.learning_strategy import (
    ConfidenceCalibration,
    LearningStrategyEngine,
    MomentumPosture,
    SpacingDecision,
    StrategyAction,
    StrategyEvidenceInput,
)
from app.application.learning_strategy.calibration import (
    calibrate,
    guidance_for,
)
from app.presentation.product_language import APPROVED_TERMS
from app.presentation.session.sitting_report import build_sitting_report
from app.services.learning_strategy_metrics import LearningStrategyMetrics

SESSION_BODY = Path("app/templates/session/partials/session_body.html")
FOUNDER_ALPHA = Path(
    "app/founder/dashboard/templates/founder_dashboard/alpha_observability.html"
)


class TestStrategyDecisionRules:
    def test_repeated_incorrect_immediate_reinforcement(self):
        advice = LearningStrategyEngine().evaluate(
            StrategyEvidenceInput(
                topic_title="Discount factors",
                learning_objectives=("Apply discount factors",),
                practice_incorrect=2,
                practice_attempted=2,
                finish_verdict="yes",
            )
        )
        assert advice.action is StrategyAction.IMMEDIATE_REINFORCEMENT
        assert advice.spacing is SpacingDecision.IMMEDIATE
        assert "reinforcement" in advice.explanation.lower()
        assert "discount" in advice.explanation.lower()

    def test_correct_low_confidence_practice_for_certainty(self):
        advice = LearningStrategyEngine().evaluate(
            StrategyEvidenceInput(
                topic_title="Present value",
                practice_correct=2,
                practice_attempted=2,
                reported_confidence=0.15,
                finish_verdict="yes",
            )
        )
        assert advice.action is StrategyAction.PRACTICE_FOR_CERTAINTY
        assert advice.calibration is ConfidenceCalibration.UNDER_CONFIDENT
        # Never expose calibration labels to students.
        blob = " ".join(
            [
                advice.recommendation_title,
                advice.recommendation_body,
                advice.explanation,
                advice.confidence_guidance,
            ]
        ).lower()
        assert "under-confident" not in blob
        assert "underconfident" not in blob
        assert "certainty" in blob or "sure" in blob

    def test_incorrect_high_confidence_consolidate(self):
        advice = LearningStrategyEngine().evaluate(
            StrategyEvidenceInput(
                topic_title="Annuities",
                practice_incorrect=1,
                practice_attempted=1,
                reported_confidence=0.9,
                finish_verdict="yes",
            )
        )
        assert advice.action is StrategyAction.CONSOLIDATE_UNDERSTANDING
        assert advice.calibration is ConfidenceCalibration.OVER_CONFIDENT
        blob = (
            advice.explanation + advice.confidence_guidance
        ).lower()
        assert "over-confident" not in blob
        assert "overconfident" not in blob

    def test_strong_accepted_advance(self):
        advice = LearningStrategyEngine().evaluate(
            StrategyEvidenceInput(
                topic_title="Present value",
                practice_correct=3,
                practice_attempted=3,
                finish_verdict="yes",
                progress_advanced=True,
                mission_completed=True,
                next_topic_title="Discount factors",
            )
        )
        assert advice.action is StrategyAction.ADVANCE_TOPIC
        assert "Discount factors" in advice.recommendation_body
        assert advice.spacing in {
            SpacingDecision.NO_REVIEW,
            SpacingDecision.THIS_WEEK,
        }

    def test_long_gap_schedules_revision(self):
        advice = LearningStrategyEngine().evaluate(
            StrategyEvidenceInput(
                topic_title="Interest rates",
                days_since_topic_practice=21,
                finish_verdict="yes",
            )
        )
        assert advice.action is StrategyAction.SCHEDULED_REVISION
        assert advice.spacing in {
            SpacingDecision.THIS_WEEK,
            SpacingDecision.LATER,
        }

    def test_abandoned_triggers_recovery(self):
        advice = LearningStrategyEngine().evaluate(
            StrategyEvidenceInput(
                topic_title="Cash flows",
                abandoned=True,
            )
        )
        assert advice.action is StrategyAction.RECOVER_PRIOR_KNOWLEDGE
        assert advice.momentum is MomentumPosture.RECOVERY

    def test_repeated_partial_slows_progression(self):
        advice = LearningStrategyEngine().evaluate(
            StrategyEvidenceInput(
                topic_title="Force of interest",
                consecutive_partial_finishes=2,
                practice_incorrect=1,
                practice_correct=1,
                finish_verdict="partially",
            )
        )
        assert advice.action is StrategyAction.SLOW_PROGRESSION

    def test_sustained_strong_increases_challenge(self):
        advice = LearningStrategyEngine().evaluate(
            StrategyEvidenceInput(
                topic_title="Present value",
                practice_correct=2,
                practice_attempted=2,
                progress_advanced=True,
                consecutive_strong_sittings=2,
                reported_confidence=0.7,
                finish_verdict="yes",
            )
        )
        assert advice.action is StrategyAction.INCREASE_CHALLENGE


class TestConfidenceCalibration:
    def test_guidance_never_exposes_labels(self):
        for cal in ConfidenceCalibration:
            text = guidance_for(cal, topic="Annuities").lower()
            assert "over-confident" not in text
            assert "under-confident" not in text
            assert "overconfident" not in text
            assert "underconfident" not in text
            # Internal enum names must never appear as student claims.
            assert "healthy" not in text

    def test_calibrate_unknown_without_confidence(self):
        evidence = StrategyEvidenceInput(
            practice_correct=2,
            practice_attempted=2,
        )
        assert calibrate(evidence) is ConfidenceCalibration.UNKNOWN


class TestSittingReportStrategyProjection:
    def test_incorrect_sitting_surfaces_strategy_why(self):
        report = build_sitting_report(
            topic_title="Discount factors",
            opaque_summary={
                "learning_objectives": ("Apply discount factors",),
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_INCORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_INCORRECT.value},
                    {"type_id": RuntimeEvidenceType.FINISH_REVIEW_YES.value},
                ],
                "finish_review": {"verdict": "yes"},
                "substance": "package",
            },
        )
        assert report.strategy_title
        assert "Reinforce" in report.strategy_title or "Consolidate" in (
            report.strategy_title
        ) or "Repeat" in report.strategy_title
        assert report.strategy_explanation
        assert "discount" in report.strategy_explanation.lower()
        forbidden = (
            "twin",
            "evidence authority",
            "educational+",
            "over-confident",
            "under-confident",
            "fsm",
        )
        blob = " ".join(
            [
                report.strategy_title,
                report.strategy_body,
                report.strategy_explanation,
                report.strategy_confidence_guidance,
                *report.learning_insights,
            ]
        ).lower()
        assert not any(term in blob for term in forbidden)

    def test_strong_sitting_advances_with_explanation(self):
        report = build_sitting_report(
            topic_title="Present value",
            opaque_summary={
                "learning_objectives": ("Discount cash flows to today",),
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.FINISH_REVIEW_YES.value},
                ],
                "progress_advanced": True,
                "mission_completed": True,
                "finish_review": {"verdict": "yes"},
            },
            metadata={
                "progress_advanced": "true",
                "mission_completed": "true",
            },
            next_recommendation="Discount factors",
        )
        assert report.strategy_title == "Advance Topic"
        assert "Discount factors" in report.strategy_body
        assert report.strategy_explanation


class TestFounderStrategyMetrics:
    def test_distribution_from_packages(self):
        packages = [
            {
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_INCORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_INCORRECT.value},
                ],
                "finish_review": {"verdict": "yes"},
                "topic_title": "A",
            },
            {
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                ],
                "finish_review": {"verdict": "yes"},
                "progress_advanced": True,
                "mission_completed": True,
                "topic_title": "B",
            },
        ]
        snap = LearningStrategyMetrics.from_packages(packages)
        assert snap.sittings_evaluated == 2
        assert snap.reinforcement_rate > 0
        assert snap.advance_rate > 0
        opaque = snap.to_opaque()
        assert "strategy_counts" in opaque


class TestProductSurfaceMarkers:
    def test_session_template_has_strategy_block(self):
        text = SESSION_BODY.read_text(encoding="utf-8")
        # Strategy DTO fields remain; Session redesign completion uses honest
        # what-changed copy rather than a strategy chrome block.
        from app.presentation.session.dto.study_session import StudySessionPage

        assert "strategy_title" in StudySessionPage.__dataclass_fields__
        assert "data-completion-what-changed" in text

    def test_founder_template_has_strategy_section(self):
        text = FOUNDER_ALPHA.read_text(encoding="utf-8")
        assert "Learning Strategy" in text
        assert "recovery_rate" in text

    def test_approved_term(self):
        assert "Learning Strategy" in APPROVED_TERMS


class TestDeterminism:
    def test_same_inputs_same_advice(self):
        engine = LearningStrategyEngine()
        evidence = StrategyEvidenceInput(
            topic_title="Annuities",
            practice_correct=1,
            practice_incorrect=1,
            finish_verdict="yes",
            reported_confidence=0.5,
        )
        a = engine.evaluate(evidence)
        b = engine.evaluate(evidence)
        assert a.action == b.action
        assert a.rule_id == b.rule_id
        assert a.explanation == b.explanation
        assert a.spacing == b.spacing
