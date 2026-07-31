"""KWP-008 — Learning Diagnostics Engine tests.

Deterministic cause diagnosis, student guidance (no category labels),
Sitting Report WHAT+WHY composition, and founder diagnostic metrics.
No runtime authority redesign.
"""

from __future__ import annotations

from pathlib import Path

from app.application.learning_diagnostics import (
    DiagnosticCategory,
    DiagnosticEvidenceInput,
    LearningDiagnosticsEngine,
)
from app.application.learning_strategy import StrategyAction
from app.presentation.product_language import APPROVED_TERMS
from app.presentation.session.sitting_report import build_sitting_report
from app.services.learning_diagnostics_metrics import LearningDiagnosticsMetrics

SESSION_BODY = Path("app/templates/session/partials/session_body.html")
FOUNDER_ALPHA = Path(
    "app/founder/dashboard/templates/founder_dashboard/alpha_observability.html"
)

_LABEL_FRAGMENTS = (
    "prerequisite weakness",
    "conceptual misunderstanding",
    "formula recall weakness",
    "confidence mismatch",
    "retention decay",
    "inconsistent practice",
    "exam technique",
    "calculation accuracy",
    "reading interpretation",
)


class TestDiagnosticDecisionRules:
    def test_prerequisite_weakness_guidance_never_labels(self):
        report = LearningDiagnosticsEngine().evaluate(
            DiagnosticEvidenceInput(
                topic_title="Annuities",
                practice_incorrect=2,
                practice_attempted=2,
                weak_topic=True,
                prerequisite_title="Discount factors",
            )
        )
        assert report.category is DiagnosticCategory.PREREQUISITE_WEAKNESS
        assert "Discount factors" in report.guidance
        assert "Annuities" in report.guidance
        blob = (report.guidance + " " + report.explanation).lower()
        for fragment in _LABEL_FRAGMENTS:
            assert fragment not in blob

    def test_prerequisite_transfer_when_strong_prior(self):
        report = LearningDiagnosticsEngine().evaluate(
            DiagnosticEvidenceInput(
                topic_title="Annuities",
                practice_incorrect=1,
                practice_attempted=1,
                prerequisite_title="Discount factors",
                strong_prerequisite=True,
            )
        )
        assert report.category is DiagnosticCategory.PREREQUISITE_WEAKNESS
        assert "link" in report.explanation.lower() or "Discount" in report.explanation

    def test_confidence_mismatch_under_knowledge_stronger(self):
        report = LearningDiagnosticsEngine().evaluate(
            DiagnosticEvidenceInput(
                topic_title="Present value",
                practice_correct=2,
                practice_attempted=2,
                reported_confidence=0.15,
                finish_verdict="yes",
            )
        )
        assert report.category is DiagnosticCategory.CONFIDENCE_MISMATCH
        assert report.primary.mismatch_polarity == "under"
        blob = (report.guidance + report.explanation).lower()
        assert "under-confident" not in blob
        assert "stronger" in blob or "certainty" in blob

    def test_conceptual_overconfident_errors(self):
        report = LearningDiagnosticsEngine().evaluate(
            DiagnosticEvidenceInput(
                topic_title="Annuities",
                practice_incorrect=1,
                practice_attempted=1,
                reported_confidence=0.9,
                finish_verdict="yes",
            )
        )
        # Confidence mismatch and conceptual may both fire; primary is first
        # matching priority (retention → prereq → confidence → conceptual).
        assert report.category in {
            DiagnosticCategory.CONFIDENCE_MISMATCH,
            DiagnosticCategory.CONCEPTUAL_MISUNDERSTANDING,
        }
        cats = {f.category for f in report.findings}
        assert DiagnosticCategory.CONCEPTUAL_MISUNDERSTANDING in cats
        assert DiagnosticCategory.CONFIDENCE_MISMATCH in cats

    def test_retention_decay_long_gap(self):
        report = LearningDiagnosticsEngine().evaluate(
            DiagnosticEvidenceInput(
                topic_title="Interest rates",
                days_since_topic_practice=21,
                practice_incorrect=1,
                practice_attempted=1,
                weak_topic=True,
            )
        )
        assert report.category is DiagnosticCategory.RETENTION_DECAY
        assert "21" in report.explanation or "fade" in report.explanation.lower()

    def test_improving_understanding_after_misses(self):
        report = LearningDiagnosticsEngine().evaluate(
            DiagnosticEvidenceInput(
                topic_title="Cash flows",
                practice_correct=2,
                practice_incorrect=1,
                practice_attempted=3,
                recovered_after_misses=True,
                finish_verdict="yes",
            )
        )
        cats = {f.category for f in report.findings}
        assert DiagnosticCategory.IMPROVING_UNDERSTANDING in cats
        improving = next(
            f
            for f in report.findings
            if f.category is DiagnosticCategory.IMPROVING_UNDERSTANDING
        )
        assert (
            "improving" in improving.explanation.lower()
            or "right direction" in improving.explanation.lower()
        )

    def test_formula_recall_from_hints(self):
        report = LearningDiagnosticsEngine().evaluate(
            DiagnosticEvidenceInput(
                topic_title="Discount factors",
                practice_incorrect=1,
                practice_attempted=1,
                numeric_incorrect=1,
                practice_hints=("Recall v = 1 / (1 + i).",),
            )
        )
        cats = {f.category for f in report.findings}
        assert DiagnosticCategory.FORMULA_RECALL_WEAKNESS in cats
        assert "formula" in report.guidance.lower() or any(
            "formula" in f.guidance.lower() for f in report.findings
        )

    def test_calculation_accuracy_numeric_mix(self):
        report = LearningDiagnosticsEngine().evaluate(
            DiagnosticEvidenceInput(
                topic_title="Present value",
                practice_incorrect=1,
                practice_correct=1,
                practice_attempted=2,
                numeric_incorrect=1,
                numeric_correct=1,
            )
        )
        cats = {f.category for f in report.findings}
        assert DiagnosticCategory.CALCULATION_ACCURACY in cats

    def test_reading_skipped_weak_practice(self):
        report = LearningDiagnosticsEngine().evaluate(
            DiagnosticEvidenceInput(
                topic_title="Force of interest",
                practice_incorrect=2,
                practice_attempted=2,
                reading_skipped=True,
            )
        )
        cats = {f.category for f in report.findings}
        assert DiagnosticCategory.READING_INTERPRETATION in cats

    def test_exam_technique_partial_mixed(self):
        report = LearningDiagnosticsEngine().evaluate(
            DiagnosticEvidenceInput(
                topic_title="Annuities",
                practice_incorrect=1,
                practice_correct=1,
                finish_verdict="partially",
                consecutive_partial_finishes=2,
            )
        )
        cats = {f.category for f in report.findings}
        assert DiagnosticCategory.EXAM_TECHNIQUE in cats

    def test_strong_performance(self):
        report = LearningDiagnosticsEngine().evaluate(
            DiagnosticEvidenceInput(
                topic_title="Present value",
                practice_correct=3,
                practice_attempted=3,
                finish_verdict="yes",
                progress_advanced=True,
                next_topic_title="Discount factors",
            )
        )
        assert report.category is DiagnosticCategory.STRONG_PERFORMANCE

    def test_determinism(self):
        evidence = DiagnosticEvidenceInput(
            topic_title="Cash flows",
            practice_incorrect=2,
            practice_attempted=2,
            retention_risk=True,
            weak_topic=True,
        )
        a = LearningDiagnosticsEngine().evaluate(evidence)
        b = LearningDiagnosticsEngine().evaluate(evidence)
        assert a.to_opaque() == b.to_opaque()


class TestSittingReportComposition:
    def test_what_and_why_with_diagnostic_focus(self):
        report = build_sitting_report(
            topic_title="Annuities",
            opaque_summary={
                "topic_title": "Annuities",
                "practice_correct": 0,
                "practice_incorrect": 2,
                "practice_attempted": 2,
                "finish_review": {"verdict": "yes"},
                "learning_objectives": ("Apply annuity factors",),
            },
            twin_signals={
                "prerequisite_title": "Discount factors",
                "weak_topic": True,
            },
        )
        assert report.strategy_title  # WHAT from strategy
        assert report.strategy_explanation  # WHY composed
        assert "Discount factors" in report.diagnostic_guidance
        blob = " ".join(
            [
                report.strategy_title,
                report.strategy_body,
                report.strategy_explanation,
                report.diagnostic_guidance,
            ]
        ).lower()
        for fragment in _LABEL_FRAGMENTS:
            assert fragment not in blob

    def test_strategy_action_still_present(self):
        report = build_sitting_report(
            topic_title="Present value",
            opaque_summary={
                "practice_correct": 0,
                "practice_incorrect": 2,
                "practice_attempted": 2,
                "finish_review": {"verdict": "yes"},
            },
        )
        # Strategy WHAT remains Immediate Reinforcement / Consolidate path.
        from app.application.learning_strategy import LearningStrategyEngine
        from app.application.learning_strategy.dto import StrategyEvidenceInput

        advice = LearningStrategyEngine().evaluate(
            StrategyEvidenceInput(
                topic_title="Present value",
                practice_incorrect=2,
                practice_attempted=2,
                finish_verdict="yes",
            )
        )
        assert advice.action is StrategyAction.IMMEDIATE_REINFORCEMENT
        assert report.strategy_title == advice.recommendation_title


class TestFounderDiagnosticsMetrics:
    def test_category_distribution(self):
        packages = [
            {
                "topic_title": "A",
                "practice_incorrect": 2,
                "practice_attempted": 2,
                "retention_risk": True,
                "weak_topic": True,
            },
            {
                "topic_title": "B",
                "practice_correct": 2,
                "practice_attempted": 2,
                "reported_confidence": 0.1,
                "finish_review": {"verdict": "yes"},
            },
            {
                "topic_title": "C",
                "practice_correct": 3,
                "practice_attempted": 3,
                "finish_review": {"verdict": "yes"},
                "progress_advanced": True,
            },
        ]
        snap = LearningDiagnosticsMetrics.from_packages(packages)
        assert snap.sittings_evaluated == 3
        assert snap.retention_decay_rate > 0
        assert snap.confidence_mismatch_rate > 0
        assert snap.strong_performance_rate > 0
        assert snap.category_counts


class TestProductSurfaces:
    def test_template_diagnostic_marker(self):
        html = SESSION_BODY.read_text(encoding="utf-8")
        assert "data-diagnostic-guidance" in html
        assert "data-strategy-why" in html

    def test_founder_diagnostics_section(self):
        html = FOUNDER_ALPHA.read_text(encoding="utf-8")
        assert "Learning Diagnostics" in html
        assert "confidence_mismatch_rate" in html

    def test_approved_term(self):
        assert "Learning Diagnostics" in APPROVED_TERMS
