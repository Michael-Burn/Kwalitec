"""ILE-001C — Contextual intent and educational framing tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.application.adaptive_assessment import (
    EvidenceBand,
    QuickCheckExperienceService,
    QuickCheckExperienceStore,
    QuickCheckPhase,
    SessionTypeId,
    build_context_card,
    build_educational_summary,
    build_recommendation_frame,
    build_reflection_frame,
    default_intent_context,
    resolve_adaptive_assessment_flags,
    resolve_copy,
    validate_registered_adaptive_assessment_resources,
)
from app.application.adaptive_assessment.feature_flags import (
    AdaptiveAssessmentFeatureFlags,
)
from app.application.adaptive_assessment.session_registry import get_session_type
from app.application.adaptive_assessment.telemetry import (
    InMemoryTelemetrySink,
    ProductTelemetryRecorder,
    TelemetryEventName,
)

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "adaptive_assessment"
)
TEMPLATES = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "templates"
    / "adaptive_assessment"
)

ENABLED_FRAMING = AdaptiveAssessmentFeatureFlags(
    ENABLE_ADAPTIVE_ASSESSMENT=True,
    ENABLE_QUICK_CHECK=True,
    ENABLE_CONTEXTUAL_FRAMING=True,
)

ENABLED_QC_ONLY = AdaptiveAssessmentFeatureFlags(
    ENABLE_ADAPTIVE_ASSESSMENT=True,
    ENABLE_QUICK_CHECK=True,
    ENABLE_CONTEXTUAL_FRAMING=False,
)

FORBIDDEN_IMPORT_FRAGMENTS = (
    "student_digital_twin",
    "educational_reasoning",
    "StudentReasoningService",
    "mission_engine",
    "mission_engine_v2",
    "assessment_pipeline",
    "intelligent_tutor",
    "learning_graph",
    "StudentDigitalTwin",
)

BANNED_SUMMARY = (
    "pass",
    "fail",
    "mastery",
    "score",
    "exam",
    "algorithm",
    "model decided",
    "twin",
)


def _service(flags=ENABLED_FRAMING, **kwargs) -> QuickCheckExperienceService:
    sink = InMemoryTelemetrySink()
    recorder = ProductTelemetryRecorder(sink=sink)
    store = QuickCheckExperienceStore()
    svc = QuickCheckExperienceService(
        store=store,
        telemetry=recorder,
        flags=flags,
        **kwargs,
    )
    svc._test_sink = sink  # type: ignore[attr-defined]
    return svc


def test_contextual_framing_flag_defaults_off():
    flags = resolve_adaptive_assessment_flags(environ={})
    assert flags.ENABLE_CONTEXTUAL_FRAMING is False
    assert flags.is_contextual_framing_enabled() is False


def test_contextual_framing_requires_master_switch():
    flags = AdaptiveAssessmentFeatureFlags(
        ENABLE_ADAPTIVE_ASSESSMENT=False,
        ENABLE_CONTEXTUAL_FRAMING=True,
    )
    assert flags.is_contextual_framing_enabled() is False


def test_context_card_arc_from_copy_registry():
    ctx = default_intent_context(focus_label="Compound Distributions")
    duration = get_session_type(SessionTypeId.QUICK_CHECK).expected_duration_label
    card = build_context_card(ctx, duration_label=duration)
    assert card.observation
    assert "Compound Distributions" in card.observation
    assert card.meaning
    assert card.purpose
    assert card.benefit
    assert card.invitation
    assert card.accessibility.keyboard_navigable is True
    blob = " ".join(
        [card.observation, card.meaning, card.purpose, card.benefit]
    ).lower()
    for banned in BANNED_SUMMARY:
        assert banned not in blob


def test_educational_summary_avoids_performance_language():
    ctx = default_intent_context(focus_label="Discounting")
    summary = build_educational_summary(ctx)
    blob = " ".join(
        [summary.learned, summary.evidence, summary.meaning, summary.next_step]
    ).lower()
    for banned in BANNED_SUMMARY:
        assert banned not in blob
    assert "Discounting" in summary.learned


def test_recommendation_framing_layers():
    ctx = default_intent_context(
        focus_label="Compound Distributions",
        evidence_band=EvidenceBand.RELIABLE,
    )
    rec = build_recommendation_frame(ctx)
    assert rec.recommendation
    assert rec.reason
    assert rec.supporting_evidence
    assert rec.confidence_level == resolve_copy("framing.confidence.reliable")
    assert rec.expected_outcome
    assert rec.why_label
    assert "algorithm" not in rec.why_body.lower()
    assert rec.suppress_primary is False


def test_uncertainty_when_insufficient_evidence():
    ctx = default_intent_context(evidence_band=EvidenceBand.INSUFFICIENT)
    rec = build_recommendation_frame(ctx)
    assert rec.suppress_primary is True
    assert rec.show_uncertainty is True
    assert "enough evidence" in rec.uncertainty.lower()
    assert rec.confidence_level == resolve_copy(
        "framing.confidence.insufficient"
    )


def test_observation_only_uncertainty_language():
    ctx = default_intent_context(evidence_band=EvidenceBand.OBSERVATION_ONLY)
    rec = build_recommendation_frame(ctx)
    assert rec.suppress_primary is True
    assert "observe" in rec.uncertainty.lower() or "gathering" in (
        rec.reason.lower() + rec.uncertainty.lower()
    )


def test_reflection_frame_preserves_student_choice():
    frame = build_reflection_frame(default_intent_context())
    assert frame.observation
    assert frame.meaning
    assert frame.suggested_action
    assert frame.student_choice_prompt
    assert "guidance" in frame.student_choice_prompt.lower()
    assert frame.accept_choice_label
    assert frame.defer_choice_label
    assert frame.own_choice_label


def test_framing_off_preserves_ile001b_introduction():
    svc = _service(flags=ENABLED_QC_ONLY)
    snap = svc.start(student_id="1", mission_ref="m1")
    assert snap.framing_enabled is False
    assert snap.context_card is None
    assert snap.introduction is not None
    assert snap.phase == QuickCheckPhase.INTRODUCTION


def test_framing_on_builds_context_card_and_emits_context_viewed():
    svc = _service()
    snap = svc.start(student_id="2", mission_ref="m2", subject_code="CS1")
    assert snap.framing_enabled is True
    assert snap.context_card is not None
    assert snap.introduction is not None
    svc.mark_context_viewed(snap.experience_id, student_id="2")
    svc.mark_context_viewed(snap.experience_id, student_id="2")
    viewed = [
        e
        for e in svc._test_sink.events  # type: ignore[attr-defined]
        if e.event_name == TelemetryEventName.CONTEXT_VIEWED.value
    ]
    assert len(viewed) == 1


def test_full_framed_journey_with_recommendation_choice():
    svc = _service()
    snap = svc.start(student_id="3", mission_ref="m3")
    eid = snap.experience_id
    snap = svc.begin_questions(eid, student_id="3")
    while snap.phase == QuickCheckPhase.QUESTION:
        snap = svc.submit_response(
            eid,
            student_id="3",
            item_id=snap.question.item_id,
            response="ok",
        )
    assert snap.phase == QuickCheckPhase.REFLECTION
    assert snap.reflection_frame is not None
    assert snap.recommendation is not None
    snap = svc.submit_reflection(
        eid,
        student_id="3",
        reflection="clearer on the core idea",
        recommendation_choice="accept",
    )
    assert snap.phase == QuickCheckPhase.COMPLETION
    assert snap.educational_summary is not None
    assert snap.recommendation is not None
    names = [e.event_name for e in svc._test_sink.events]  # type: ignore
    assert TelemetryEventName.REFLECTION_COMPLETED.value in names
    assert TelemetryEventName.RECOMMENDATION_ACCEPTED.value in names
    assert TelemetryEventName.QUICK_CHECK_COMPLETED.value in names
    for event in svc._test_sink.events:  # type: ignore
        for key in event.payload:
            assert key.lower() not in {
                "answer",
                "score",
                "learner_state",
                "reflection",
            }


def test_recommendation_defer_telemetry():
    svc = _service()
    snap = svc.start(student_id="4", mission_ref="m4")
    eid = snap.experience_id
    svc.begin_questions(eid, student_id="4")
    snap = svc.snapshot(eid, student_id="4")
    while snap.phase == QuickCheckPhase.QUESTION:
        snap = svc.submit_response(
            eid,
            student_id="4",
            item_id=snap.question.item_id,
            response="x",
        )
    svc.submit_reflection(
        eid, student_id="4", reflection="", recommendation_choice="defer"
    )
    names = {e.event_name for e in svc._test_sink.events}  # type: ignore
    assert TelemetryEventName.RECOMMENDATION_DEFERRED.value in names


def test_expand_explanation_telemetry():
    svc = _service()
    svc.expand_explanation(
        student_id="1",
        subject_code="CS1",
        surface="why_recommendation",
    )
    names = [e.event_name for e in svc._test_sink.events]  # type: ignore
    assert TelemetryEventName.WHY_RECOMMENDATION_OPENED.value in names
    svc.expand_explanation(
        student_id="1", subject_code="CS1", surface="context_why"
    )
    names = [e.event_name for e in svc._test_sink.events]  # type: ignore
    assert TelemetryEventName.EXPLANATION_EXPANDED.value in names


def test_framing_copy_passes_terminology():
    validate_registered_adaptive_assessment_resources()
    for key in (
        "framing.context.observation",
        "framing.summary.learned",
        "framing.recommendation.why_body",
        "framing.uncertainty.insufficient",
    ):
        assert resolve_copy(key)


def test_templates_include_framing_structure():
    intro = (TEMPLATES / "introduction.html").read_text(encoding="utf-8")
    assert "context_card" in intro
    assert "observation_label" in intro
    completion = (TEMPLATES / "completion.html").read_text(encoding="utf-8")
    assert "educational_summary" in completion
    assert "recommendation_frame" in completion
    reflection = (TEMPLATES / "reflection.html").read_text(encoding="utf-8")
    assert "reflection_frame" in reflection
    assert "student_choice" in reflection or "choice_label" in reflection
    rec = (
        TEMPLATES / "components" / "recommendation_frame.html"
    ).read_text(encoding="utf-8")
    assert "why_label" in rec
    assert "confidence_level" in rec


def test_ui_no_scores_in_framed_templates():
    for name in ("introduction.html", "completion.html", "reflection.html"):
        text = (TEMPLATES / name).read_text(encoding="utf-8").lower()
        assert "score" not in text
        assert "pass/fail" not in text
        assert "incorrect!" not in text


def test_architecture_purity_framing_module():
    path = PACKAGE_ROOT / "educational_framing.py"
    text = path.read_text(encoding="utf-8")
    for fragment in FORBIDDEN_IMPORT_FRAGMENTS:
        assert fragment not in text
    assert "flask.request" not in text


def test_blueprint_framing_routes(app):
    rules = {rule.endpoint for rule in app.url_map.iter_rules()}
    assert "adaptive_assessment.expand_explanation" in rules
    assert "adaptive_assessment.recommendation_choice" in rules


def test_mission_card_why_body_when_framing_on():
    svc = _service()
    card = svc.mission_card(subject_code="CS1")
    assert card.framing_enabled is True
    assert card.why_body
    assert "grade" in card.why_body.lower() or "evidence" in card.why_body.lower()


@pytest.mark.parametrize(
    "band",
    [
        EvidenceBand.INSUFFICIENT,
        EvidenceBand.EMERGING,
        EvidenceBand.RELIABLE,
        EvidenceBand.HIGH,
    ],
)
def test_recommendation_bands_deterministic(band: EvidenceBand):
    a = build_recommendation_frame(
        default_intent_context(focus_label="X", evidence_band=band)
    )
    b = build_recommendation_frame(
        default_intent_context(focus_label="X", evidence_band=band)
    )
    assert a.recommendation == b.recommendation
    assert a.confidence_level == b.confidence_level
