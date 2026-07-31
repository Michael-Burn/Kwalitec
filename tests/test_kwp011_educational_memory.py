"""KWP-011 — Educational Memory & Learning Timeline tests.

Persistence of EI outputs, frozen Sitting Report history, timeline /
patterns / milestones, student journey narrative, and founder metrics.
No runtime authority redesign.
"""

from __future__ import annotations

from pathlib import Path

from app.application.educational_memory import (
    EducationalMemoryService,
    get_educational_memory_service,
)
from app.application.educational_memory.dto import (
    TimelineEventKind,
)
from app.application.educational_memory.milestones import detect_learning_milestones
from app.application.educational_memory.narrative import (
    build_learning_journey_narrative,
)
from app.application.educational_memory.patterns import detect_longitudinal_patterns
from app.application.educational_memory.snapshot import (
    capture_intelligence_snapshot,
    resolve_prior_from_packages,
    snapshot_from_package,
)
from app.application.educational_memory.timeline import build_learning_timeline
from app.application.learning_strategy.dto import StrategyAction
from app.infrastructure.session.store import SessionDocumentStore
from app.presentation.product_language import APPROVED_TERMS
from app.presentation.session.sitting_report import build_sitting_report
from app.services.educational_memory_metrics import EducationalMemoryMetrics

FOUNDER_ALPHA = Path(
    "app/founder/dashboard/templates/founder_dashboard/alpha_observability.html"
)
JOURNEY_TMPL = Path("app/templates/student/learning_journey.html")
HISTORY_TMPL = Path("app/templates/student/history.html")

_FORBIDDEN = (
    "digital twin",
    "evidence authority",
    "cognitive load",
    "overloaded",
    "load points",
    "recommendation effective",
    "badge",
    "leaderboard",
    "points earned",
)


def _package(
    *,
    session_id: str,
    student_id: str = "learner-1",
    topic: str = "Discount Factors",
    created_at: str = "2026-01-01T10:00:00+00:00",
    correct: int = 1,
    incorrect: int = 2,
    finish: str = "partially",
    progress: bool = False,
    reflection: bool = False,
    retention_risk: bool = False,
) -> dict:
    observations = []
    for _ in range(correct):
        observations.append({"type_id": "EV-RT-07", "payload": {}})
    for _ in range(incorrect):
        observations.append({"type_id": "EV-RT-08", "payload": {}})
    if reflection:
        observations.append({"type_id": "EV-RT-10", "payload": {}})
    return {
        "package_id": f"pkg-{session_id}",
        "student_id": student_id,
        "session_id": session_id,
        "topic_id": "topic-df",
        "topic_title": topic,
        "learning_objectives": ["Apply discount factors"],
        "observations": observations,
        "created_at": created_at,
        "finish_review_verdict": finish,
        "finish_review": {"verdict": finish},
        "progress_advanced": progress,
        "retention_risk": retention_risk,
        "validation": {"disposition": "accepted"},
    }


class TestIntelligenceSnapshot:
    def test_capture_persists_student_sitting_report(self):
        snap = capture_intelligence_snapshot(_package(session_id="s1"))
        assert snap.has_student_report
        assert snap.student_sitting_report.get("strategy_title")
        assert snap.outgoing_intervention.get("strategy_action")
        opaque = snap.to_opaque()
        restored = snapshot_from_package({"intelligence_snapshot": opaque})
        assert restored is not None
        assert (
            restored.student_sitting_report["strategy_title"]
            == snap.student_sitting_report["strategy_title"]
        )

    def test_prior_chain_from_previous_same_topic(self):
        first = _package(session_id="s1", created_at="2026-01-01T10:00:00+00:00")
        service = EducationalMemoryService()
        updated_first, snap1 = service.capture_for_package(first)
        assert snap1.outgoing_intervention

        second = _package(
            session_id="s2",
            created_at="2026-01-08T10:00:00+00:00",
            correct=2,
            incorrect=0,
            finish="yes",
        )
        prior = resolve_prior_from_packages(
            [updated_first],
            student_id="learner-1",
            topic_title="Discount Factors",
            exclude_session_id="s2",
        )
        assert prior is not None
        assert prior.has_recommendation
        _updated_second, snap2 = service.capture_for_package(
            second, prior_packages=[updated_first]
        )
        assert snap2.prior_intervention.get("strategy_action")


class TestStorePersistence:
    def test_persist_on_store_is_idempotent(self):
        store = SessionDocumentStore()
        pkg = _package(session_id="s1")
        store.save("lsr.evidence_package", "s1", pkg)
        service = get_educational_memory_service()
        first = service.persist_on_store(store=store, session_id="s1")
        second = service.persist_on_store(store=store, session_id="s1")
        assert first is not None and second is not None
        assert (
            first.student_sitting_report["strategy_title"]
            == second.student_sitting_report["strategy_title"]
        )
        loaded = store.get("lsr.evidence_package", "s1")
        assert isinstance(loaded.get("intelligence_snapshot"), dict)


class TestFrozenSittingReport:
    def test_frozen_snapshot_preferred_over_live_engines(self):
        report = build_sitting_report(
            topic_title="Discount Factors",
            opaque_summary={
                "topic_title": "Discount Factors",
                "practice_correct": 0,
                "practice_incorrect": 2,
                "practice_attempted": 2,
                "intelligence_snapshot": {
                    "student_sitting_report": {
                        "strategy_title": "Frozen Historical Strategy",
                        "strategy_body": "As advised that day.",
                        "strategy_explanation": "Why it was recommended then.",
                        "diagnostic_guidance": "Frozen diagnostic focus.",
                        "difficulty_guidance": "Frozen pace guidance.",
                        "effectiveness_feedback": "Frozen progress feedback.",
                    }
                },
            },
            metadata={"intelligence_captured": "true"},
        )
        assert report.strategy_title == "Frozen Historical Strategy"
        assert report.diagnostic_guidance == "Frozen diagnostic focus."
        assert report.difficulty_guidance == "Frozen pace guidance."
        assert report.effectiveness_feedback == "Frozen progress feedback."
        blob = " ".join(
            [
                report.strategy_title,
                report.strategy_body,
                report.diagnostic_guidance,
                report.difficulty_guidance,
                report.effectiveness_feedback,
            ]
        ).lower()
        for term in _FORBIDDEN:
            assert term not in blob


class TestLearningTimeline:
    def test_timeline_from_evidence_not_fabricated(self):
        packages = [
            _package(
                session_id="s1",
                created_at="2026-01-01T10:00:00+00:00",
                correct=0,
                incorrect=2,
            ),
            _package(
                session_id="s2",
                created_at="2026-02-01T10:00:00+00:00",
                correct=2,
                incorrect=0,
                finish="yes",
                progress=True,
            ),
        ]
        # Capture snapshots so strategy actions exist.
        service = EducationalMemoryService()
        packages = [service.capture_for_package(p)[0] for p in packages]
        timeline = build_learning_timeline(packages, student_id="learner-1")
        kinds = {e.kind for e in timeline}
        assert TimelineEventKind.STARTED_TOPIC in kinds
        assert TimelineEventKind.SITTING_RECORDED in kinds
        # Improvement requires accuracy delta — second sitting stronger.
        assert TimelineEventKind.UNDERSTANDING_IMPROVED in kinds
        assert TimelineEventKind.ADVANCED in kinds
        for entry in timeline:
            assert entry.body
            assert "fabricat" not in entry.body.lower()


class TestLongitudinalPatternsAndMilestones:
    def test_patterns_and_milestones_from_sequence(self):
        service = EducationalMemoryService()
        packages = []
        # Early weak sittings needing reinforcement.
        for i in range(3):
            pkg = _package(
                session_id=f"early-{i}",
                created_at=f"2026-01-0{i + 1}T10:00:00+00:00",
                correct=0,
                incorrect=2,
                finish="partially",
            )
            packages.append(service.capture_for_package(pkg)[0])
        # Later strong recovery / advance sittings.
        for i in range(3):
            pkg = _package(
                session_id=f"late-{i}",
                created_at=f"2026-03-0{i + 1}T10:00:00+00:00",
                correct=3,
                incorrect=0,
                finish="yes",
                progress=True,
            )
            # Seed recovery prior on first late sitting.
            if i == 0:
                pkg = {
                    **pkg,
                    "prior_intervention": {
                        "kind": "recovery",
                        "strategy_action": StrategyAction.RECOVER_PRIOR_KNOWLEDGE.value,
                        "baseline_correct": 0,
                        "baseline_incorrect": 2,
                        "baseline_attempted": 2,
                    },
                    "retention_risk": True,
                }
            packages.append(service.capture_for_package(pkg)[0])

        patterns = detect_longitudinal_patterns(
            packages, student_id="learner-1"
        )
        milestones = detect_learning_milestones(
            packages, student_id="learner-1"
        )
        assert patterns or milestones
        pattern_kinds = {p.kind for p in patterns}
        milestone_kinds = {m.kind for m in milestones}
        # At least one educational growth signal.
        assert pattern_kinds or milestone_kinds
        for m in milestones:
            assert "badge" not in m.narrative.lower()
            assert "points" not in m.narrative.lower()
            assert "leaderboard" not in m.narrative.lower()


class TestLearningJourneyNarrative:
    def test_story_not_raw_analytics(self):
        service = EducationalMemoryService()
        packages = [
            service.capture_for_package(
                _package(
                    session_id="s1",
                    created_at="2026-01-01T10:00:00+00:00",
                    correct=0,
                    incorrect=2,
                )
            )[0],
            service.capture_for_package(
                _package(
                    session_id="s2",
                    created_at="2026-04-01T10:00:00+00:00",
                    correct=2,
                    incorrect=0,
                    finish="yes",
                    progress=True,
                )
            )[0],
        ]
        narrative = build_learning_journey_narrative(
            packages, student_id="learner-1"
        )
        assert narrative.has_memory
        assert narrative.story_paragraphs
        blob = " ".join(narrative.story_paragraphs).lower()
        assert "discount factors" in blob or "understanding" in blob
        for term in ("load points", "verdict", "digital twin"):
            assert term not in blob
        assert narrative.sitting_archives
        assert narrative.sitting_archives[0]["session_id"]


class TestFounderMemoryMetrics:
    def test_metrics_from_packages(self):
        service = EducationalMemoryService()
        packages = [
            service.capture_for_package(
                _package(session_id="s1", created_at="2026-01-01T10:00:00+00:00")
            )[0],
            service.capture_for_package(
                _package(
                    session_id="s2",
                    created_at="2026-02-01T10:00:00+00:00",
                    correct=2,
                    incorrect=0,
                    finish="yes",
                    progress=True,
                )
            )[0],
        ]
        metrics = EducationalMemoryMetrics.from_packages(packages)
        assert metrics.sittings_total == 2
        assert metrics.sittings_with_memory == 2
        assert metrics.snapshot_coverage == 1.0
        assert metrics.recommendation_persistence_rate == 1.0
        assert metrics.timeline_entry_count > 0
        assert metrics.learners_with_journey == 1


class TestProductSurfaces:
    def test_approved_terms(self):
        assert "Educational Memory" in APPROVED_TERMS
        assert "My Learning Journey" in APPROVED_TERMS
        assert "Learning Timeline" in APPROVED_TERMS

    def test_founder_template_markers(self):
        text = FOUNDER_ALPHA.read_text(encoding="utf-8")
        assert "Educational Memory" in text
        assert "Snapshot coverage" in text
        assert "Timeline completeness" in text

    def test_journey_template_markers(self):
        text = JOURNEY_TMPL.read_text(encoding="utf-8")
        assert "My Learning Journey" in text
        assert "data-educational-memory" in text
        assert "Educational milestones" in text
        assert "points or badges" in text

    def test_history_bridge_to_journey(self):
        text = HISTORY_TMPL.read_text(encoding="utf-8")
        assert "learning_journey" in text
        assert "My Learning Journey" in text
