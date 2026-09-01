"""KWP-010 — Educational Intervention Effectiveness Engine tests.

Deterministic prior-recommendation vs subsequent-evidence evaluation,
student feedback (no verdict labels), Sitting Report Progress composition,
and founder intervention metrics. No runtime authority redesign.
"""

from __future__ import annotations

from pathlib import Path

from app.application.intervention_effectiveness import (
    EffectivenessEvidenceInput,
    EffectivenessVerdict,
    InterventionEffectivenessEngine,
    InterventionKind,
    PriorIntervention,
    prior_from_sitting,
)
from app.application.learning_difficulty.dto import LoadRecommendation
from app.application.learning_strategy.dto import StrategyAction
from app.presentation.product_language import APPROVED_TERMS
from app.presentation.session.sitting_report import build_sitting_report
from app.services.intervention_effectiveness_metrics import (
    InterventionEffectivenessMetrics,
)

SESSION_BODY = Path("app/templates/session/partials/session_body.html")
FOUNDER_ALPHA = Path(
    "app/founder/dashboard/templates/founder_dashboard/alpha_observability.html"
)

_FORBIDDEN_FRAGMENTS = (
    "recommendation effective",
    "recommendation partially effective",
    "recommendation ineffective",
    "insufficient evidence",
    "digital twin",
    "evidence authority",
    "cognitive load",
    "overloaded",
    "load points",
)


def _prior(
    *,
    kind: InterventionKind | None = None,
    strategy: StrategyAction | str = "",
    load: LoadRecommendation | str = "",
    correct: int = 0,
    incorrect: int = 2,
    attempted: int = 2,
    duration: int | None = 70,
) -> PriorIntervention:
    return prior_from_sitting(
        strategy_action=strategy,
        load_recommendation=load,
        topic_title="Annuities",
        practice_correct=correct,
        practice_incorrect=incorrect,
        practice_attempted=attempted,
        session_duration_minutes=duration,
    )


class TestConsolidationEffectiveness:
    def test_consolidation_helped(self):
        report = InterventionEffectivenessEngine().evaluate(
            EffectivenessEvidenceInput(
                prior=_prior(
                    strategy=StrategyAction.CONSOLIDATE_UNDERSTANDING,
                    incorrect=2,
                    correct=0,
                ),
                topic_title="Annuities",
                practice_correct=2,
                practice_incorrect=0,
                practice_attempted=2,
                finish_verdict="yes",
                progress_advanced=True,
            )
        )
        assert report.verdict is EffectivenessVerdict.EFFECTIVE
        assert report.intervention_kind is InterventionKind.CONSOLIDATION
        assert "strengthened" in report.feedback.lower()
        for fragment in _FORBIDDEN_FRAGMENTS:
            assert fragment not in report.feedback.lower()

    def test_consolidation_ineffective(self):
        report = InterventionEffectivenessEngine().evaluate(
            EffectivenessEvidenceInput(
                prior=_prior(
                    strategy=StrategyAction.CONSOLIDATE_UNDERSTANDING,
                    incorrect=2,
                    correct=0,
                ),
                topic_title="Annuities",
                practice_correct=0,
                practice_incorrect=3,
                practice_attempted=3,
                weak_topic=True,
            )
        )
        assert report.verdict is EffectivenessVerdict.INEFFECTIVE


class TestReinforcementEffectiveness:
    def test_reinforcement_reduced_mistakes(self):
        report = InterventionEffectivenessEngine().evaluate(
            EffectivenessEvidenceInput(
                prior=_prior(
                    strategy=StrategyAction.IMMEDIATE_REINFORCEMENT,
                    incorrect=3,
                    correct=0,
                    attempted=3,
                ),
                topic_title="Annuities",
                practice_correct=2,
                practice_incorrect=1,
                practice_attempted=3,
            )
        )
        assert report.verdict in {
            EffectivenessVerdict.EFFECTIVE,
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
        }
        assert "reinforcement" in report.feedback.lower() or "strengthened" in (
            report.feedback.lower()
        )


class TestReduceSessionLength:
    def test_shorter_sessions_helped(self):
        report = InterventionEffectivenessEngine().evaluate(
            EffectivenessEvidenceInput(
                prior=_prior(
                    load=LoadRecommendation.REDUCE_SESSION_LENGTH,
                    incorrect=2,
                    correct=1,
                    duration=80,
                ),
                topic_title="Cash flows",
                practice_correct=2,
                practice_incorrect=1,
                practice_attempted=3,
                session_duration_minutes=40,
                finish_verdict="yes",
            )
        )
        assert report.intervention_kind is InterventionKind.REDUCE_SESSION_LENGTH
        assert report.verdict in {
            EffectivenessVerdict.EFFECTIVE,
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
        }
        assert "shorter" in report.feedback.lower()


class TestSpacingEffectiveness:
    def test_increase_spacing_held(self):
        report = InterventionEffectivenessEngine().evaluate(
            EffectivenessEvidenceInput(
                prior=_prior(
                    load=LoadRecommendation.INCREASE_SPACING,
                    incorrect=0,
                    correct=2,
                ),
                topic_title="Present value",
                practice_correct=2,
                practice_incorrect=0,
                practice_attempted=2,
                days_since_topic_practice=5,
                finish_verdict="yes",
            )
        )
        assert report.verdict is EffectivenessVerdict.EFFECTIVE
        assert report.intervention_kind is InterventionKind.INCREASE_SPACING

    def test_increase_spacing_failed_retention(self):
        report = InterventionEffectivenessEngine().evaluate(
            EffectivenessEvidenceInput(
                prior=_prior(
                    strategy=StrategyAction.SCHEDULED_REVISION,
                    incorrect=0,
                    correct=2,
                ),
                topic_title="Present value",
                practice_correct=0,
                practice_incorrect=2,
                practice_attempted=2,
                retention_risk=True,
                days_since_topic_practice=10,
            )
        )
        assert report.verdict is EffectivenessVerdict.INEFFECTIVE


class TestChallengeEffectiveness:
    def test_challenge_success(self):
        report = InterventionEffectivenessEngine().evaluate(
            EffectivenessEvidenceInput(
                prior=_prior(
                    strategy=StrategyAction.INCREASE_CHALLENGE,
                    incorrect=0,
                    correct=3,
                ),
                topic_title="Force of interest",
                practice_correct=3,
                practice_incorrect=0,
                practice_attempted=3,
                progress_advanced=True,
                finish_verdict="yes",
            )
        )
        assert report.verdict is EffectivenessVerdict.EFFECTIVE
        assert "challenge" in report.feedback.lower() or "tougher" in (
            report.feedback.lower()
        )

    def test_challenge_too_hard(self):
        report = InterventionEffectivenessEngine().evaluate(
            EffectivenessEvidenceInput(
                prior=_prior(
                    load=LoadRecommendation.INCREASE_CHALLENGE,
                    incorrect=0,
                    correct=2,
                ),
                topic_title="Force of interest",
                practice_correct=0,
                practice_incorrect=3,
                practice_attempted=3,
                weak_topic=True,
            )
        )
        assert report.verdict is EffectivenessVerdict.INEFFECTIVE


class TestInsufficientEvidence:
    def test_no_prior_recommendation(self):
        report = InterventionEffectivenessEngine().evaluate(
            EffectivenessEvidenceInput(
                topic_title="Intro",
                practice_correct=1,
                practice_incorrect=0,
                practice_attempted=1,
            )
        )
        assert report.verdict is EffectivenessVerdict.INSUFFICIENT_EVIDENCE
        assert report.feedback == ""
        assert not report.has_student_feedback

    def test_no_subsequent_practice(self):
        report = InterventionEffectivenessEngine().evaluate(
            EffectivenessEvidenceInput(
                prior=_prior(strategy=StrategyAction.IMMEDIATE_REINFORCEMENT),
                topic_title="Annuities",
            )
        )
        assert report.verdict is EffectivenessVerdict.INSUFFICIENT_EVIDENCE


class TestDeterminismAndPair:
    def test_determinism(self):
        evidence = EffectivenessEvidenceInput(
            prior=_prior(strategy=StrategyAction.CONSOLIDATE_UNDERSTANDING),
            topic_title="Annuities",
            practice_correct=2,
            practice_incorrect=0,
            practice_attempted=2,
            finish_verdict="yes",
        )
        a = InterventionEffectivenessEngine().evaluate(evidence)
        b = InterventionEffectivenessEngine().evaluate(evidence)
        assert a.to_opaque() == b.to_opaque()

    def test_evaluate_pair(self):
        report = InterventionEffectivenessEngine().evaluate_pair(
            {
                "topic_title": "Annuities",
                "practice_correct": 0,
                "practice_incorrect": 2,
                "practice_attempted": 2,
            },
            {
                "topic_title": "Annuities",
                "practice_correct": 2,
                "practice_incorrect": 0,
                "practice_attempted": 2,
                "finish_review": {"verdict": "yes"},
                "progress_advanced": True,
            },
            strategy_action=StrategyAction.IMMEDIATE_REINFORCEMENT,
        )
        assert report.verdict in {
            EffectivenessVerdict.EFFECTIVE,
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
        }


class TestSittingReportComposition:
    def test_progress_feedback_when_prior_present(self):
        report = build_sitting_report(
            topic_title="Annuities",
            opaque_summary={
                "topic_title": "Annuities",
                "practice_correct": 2,
                "practice_incorrect": 0,
                "practice_attempted": 2,
                "finish_review": {"verdict": "yes"},
                "prior_intervention": {
                    "strategy_action": "immediate_reinforcement",
                    "baseline_correct": 0,
                    "baseline_incorrect": 2,
                    "baseline_attempted": 2,
                    "topic_title": "Annuities",
                },
            },
        )
        assert report.strategy_title
        assert report.effectiveness_feedback
        assert "strengthened" in report.effectiveness_feedback.lower() or (
            "reinforcement" in report.effectiveness_feedback.lower()
        )
        blob = (
            report.effectiveness_feedback
            + " "
            + report.effectiveness_explanation
        ).lower()
        for fragment in _FORBIDDEN_FRAGMENTS:
            assert fragment not in blob

    def test_no_feedback_without_prior(self):
        report = build_sitting_report(
            topic_title="Intro",
            opaque_summary={
                "topic_title": "Intro",
                "practice_correct": 1,
                "practice_attempted": 1,
            },
        )
        assert report.effectiveness_feedback == ""


class TestFounderMetrics:
    def test_aggregate_outcomes(self):
        packages = [
            {
                "topic_title": "Annuities",
                "practice_correct": 0,
                "practice_incorrect": 2,
                "practice_attempted": 2,
                "difficulty": "moderate",
                "reinforcement_session_count": 1,
            },
            {
                "topic_title": "Annuities",
                "practice_correct": 2,
                "practice_incorrect": 0,
                "practice_attempted": 2,
                "finish_review": {"verdict": "yes"},
                "progress_advanced": True,
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
                "topic_title": "Present value",
                "practice_correct": 2,
                "practice_incorrect": 1,
                "practice_attempted": 3,
                "days_since_topic_practice": 4,
            },
        ]
        snap = InterventionEffectivenessMetrics.from_packages(packages)
        assert snap.pairs_evaluated >= 2
        assert snap.verdict_counts
        assert snap.kind_counts
        opaque = snap.to_opaque()
        assert "most_effective" in opaque
        assert "challenge_success_rate" in opaque


class TestProductSurfaces:
    def test_template_effectiveness_marker(self):
        html = SESSION_BODY.read_text(encoding="utf-8")
        from app.presentation.session.dto.study_session import StudySessionPage

        assert "effectiveness_feedback" in StudySessionPage.__dataclass_fields__
        assert "data-completion-what-happened" in html

    def test_founder_effectiveness_section(self):
        html = FOUNDER_ALPHA.read_text(encoding="utf-8")
        assert "Intervention Effectiveness" in html
        assert "most_effective" in html
        assert "challenge_success_rate" in html
        assert "recovery_after_consolidation_rate" in html

    def test_approved_term(self):
        assert "Intervention Effectiveness" in APPROVED_TERMS
