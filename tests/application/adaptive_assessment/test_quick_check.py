"""ILE-001B — Quick Check learner experience tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.application.adaptive_assessment import (
    QuickCheckExperienceError,
    QuickCheckExperienceService,
    QuickCheckExperienceStore,
    QuickCheckPhase,
    SessionTypeId,
    build_calm_progress,
    build_quick_check_completion,
    build_quick_check_introduction,
    build_quick_check_mission_card,
    build_quick_check_mission_return,
    build_quick_check_question,
    get_already_selected_quick_check,
    resolve_adaptive_assessment_flags,
    resolve_copy,
    validate_registered_adaptive_assessment_resources,
)
from app.application.adaptive_assessment.feature_flags import (
    AdaptiveAssessmentFeatureFlags,
)
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
PRESENTATION_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "presentation"
    / "adaptive_assessment"
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

ENABLED_FLAGS = AdaptiveAssessmentFeatureFlags(
    ENABLE_ADAPTIVE_ASSESSMENT=True,
    ENABLE_QUICK_CHECK=True,
)


def _service(**kwargs) -> QuickCheckExperienceService:
    sink = InMemoryTelemetrySink()
    recorder = ProductTelemetryRecorder(sink=sink)
    store = QuickCheckExperienceStore()
    svc = QuickCheckExperienceService(
        store=store,
        telemetry=recorder,
        flags=ENABLED_FLAGS,
        **kwargs,
    )
    svc._test_sink = sink  # type: ignore[attr-defined]
    return svc


# ---------------------------------------------------------------------------
# Feature flags / availability
# ---------------------------------------------------------------------------


def test_quick_check_unavailable_when_flags_off():
    svc = QuickCheckExperienceService(
        flags=resolve_adaptive_assessment_flags(environ={})
    )
    assert svc.is_available() is False
    assert svc.mission_card().available is False
    with pytest.raises(QuickCheckExperienceError):
        svc.start(student_id="1", mission_ref="m1")


def test_quick_check_available_when_flags_on():
    svc = _service()
    assert svc.is_available() is True
    card = svc.mission_card()
    assert card.available is True
    assert card.title == "Quick Check"
    assert "strengthen" in card.invitation.lower()


# ---------------------------------------------------------------------------
# Presentation contracts
# ---------------------------------------------------------------------------


def test_quick_check_contracts_from_copy_registry():
    intro = build_quick_check_introduction()
    assert intro.title == resolve_copy("quick_check.intro.title")
    assert intro.begin_label == resolve_copy("quick_check.intro.begin")
    assert "grade" in intro.body.lower() or "evidence" in intro.body.lower()

    completion = build_quick_check_completion()
    assert completion.thank_you == "Thank you"
    assert completion.evidence_summary
    assert completion.uncertainty_summary
    assert completion.mission_benefit
    # Never graded / mastery language in completion contract fields
    blob = " ".join(
        [
            completion.thank_you,
            completion.evidence_summary,
            completion.uncertainty_summary,
            completion.mission_benefit,
        ]
    ).lower()
    for banned in ("grade", "pass", "fail", "mastery", "score", "exam", "test"):
        assert banned not in blob

    ret = build_quick_check_mission_return()
    assert ret.acknowledgement == "We've gathered useful evidence."

    card = build_quick_check_mission_card(available=True)
    assert card.continue_label == "Continue"
    assert card.why_this_label == "Why this?"
    assert card.accessibility.keyboard_navigable is True


def test_calm_progress_never_shows_question_numbering():
    progress = build_calm_progress(index=0, total=3)
    assert progress.show_numeric_position is False
    assert "question" not in progress.label.lower()
    assert " of " not in progress.label.lower()
    mid = build_calm_progress(index=1, total=3)
    late = build_calm_progress(index=2, total=3)
    assert mid.label
    assert late.label


def test_already_selected_learning_check_has_items():
    check = get_already_selected_quick_check()
    assert check.check_id
    assert len(check.items) >= 2
    q = build_quick_check_question(check.items[0], index=0, total=len(check.items))
    assert q.stem
    assert q.progress.show_numeric_position is False


# ---------------------------------------------------------------------------
# Experience flow
# ---------------------------------------------------------------------------


def test_full_quick_check_learner_journey():
    svc = _service()
    snap = svc.start(student_id="42", mission_ref="mission-7", subject_code="CS1")
    assert snap.phase == QuickCheckPhase.INTRODUCTION
    assert snap.introduction is not None
    eid = snap.experience_id

    snap = svc.begin_questions(eid, student_id="42")
    assert snap.phase == QuickCheckPhase.QUESTION
    assert snap.question is not None
    assert snap.question.progress.show_numeric_position is False

    # Hint
    snap = svc.show_hint(eid, student_id="42")
    assert snap.question is not None
    assert snap.question.hint_visible is True

    # Answer all items
    while snap.phase == QuickCheckPhase.QUESTION:
        item_id = snap.question.item_id
        snap = svc.submit_response(
            eid, student_id="42", item_id=item_id, response="ok"
        )

    assert snap.phase == QuickCheckPhase.REFLECTION
    snap = svc.submit_reflection(eid, student_id="42", reflection="clearer")
    assert snap.phase == QuickCheckPhase.COMPLETION
    assert snap.completion is not None
    assert snap.completion.thank_you == "Thank you"

    ack = svc.complete_return(eid, student_id="42")
    assert "evidence" in ack.acknowledgement.lower()

    sink = svc._test_sink  # type: ignore[attr-defined]
    names = [e.event_name for e in sink.events]
    assert TelemetryEventName.QUICK_CHECK_STARTED.value in names
    assert TelemetryEventName.QUICK_CHECK_COMPLETED.value in names
    for event in sink.events:
        for key in event.payload:
            assert key.lower() not in {
                "answer",
                "answers",
                "score",
                "learner_state",
            }


def test_pause_and_resume():
    svc = _service()
    snap = svc.start(student_id="7", mission_ref="m")
    eid = snap.experience_id
    svc.begin_questions(eid, student_id="7")
    paused = svc.pause(eid, student_id="7")
    assert paused.phase == QuickCheckPhase.PAUSED
    assert paused.paused is not None
    resumed = svc.resume(eid, student_id="7")
    assert resumed.phase == QuickCheckPhase.QUESTION


def test_defer_emits_dismissed_telemetry():
    svc = _service()
    snap = svc.start(student_id="9", mission_ref="m")
    svc.defer(snap.experience_id, student_id="9")
    sink = svc._test_sink  # type: ignore[attr-defined]
    names = {e.event_name for e in sink.events}
    assert TelemetryEventName.QUICK_CHECK_DISMISSED.value in names
    assert TelemetryEventName.ASSESSMENT_DEFERRED.value in names


def test_ownership_guard():
    svc = _service()
    snap = svc.start(student_id="owner", mission_ref="m")
    with pytest.raises(QuickCheckExperienceError):
        svc.snapshot(snap.experience_id, student_id="other")


def test_explain_telemetry():
    svc = _service()
    svc.explain(student_id="1", subject_code="CS1", surface="why_this")
    sink = svc._test_sink  # type: ignore[attr-defined]
    assert sink.events[-1].event_name == (
        TelemetryEventName.ASSESSMENT_EXPLAINED.value
    )


# ---------------------------------------------------------------------------
# Copy / terminology
# ---------------------------------------------------------------------------


def test_ile001b_copy_passes_terminology():
    validate_registered_adaptive_assessment_resources()
    required = {
        "quick_check.invitation.headline",
        "quick_check.invitation.cta",
        "quick_check.completion.thank_you",
        "quick_check.mission.evidence_ack",
        "quick_check.progress.making",
    }
    for key in required:
        assert resolve_copy(key)


# ---------------------------------------------------------------------------
# Accessibility
# ---------------------------------------------------------------------------


def test_accessibility_wiring_on_surfaces():
    card = build_quick_check_mission_card(available=True)
    assert card.accessibility.semantic_role == "region"
    assert card.accessibility.reduced_motion_compatible is True
    assert card.accessibility.colour_not_sole_encoding is True
    intro = build_quick_check_introduction()
    assert intro.accessibility.keyboard_navigable is True
    completion = build_quick_check_completion()
    assert completion.accessibility.focus_order_hint


# ---------------------------------------------------------------------------
# Mission integration helper
# ---------------------------------------------------------------------------


def test_mission_embed_respects_flags(app):
    from app.presentation.adaptive_assessment.mission_embed import (
        build_mission_quick_check_embed,
    )

    off = QuickCheckExperienceService(
        flags=resolve_adaptive_assessment_flags(environ={})
    )
    assert (
        build_mission_quick_check_embed(
            mission_ref="1", service=off, emit_viewed=False
        )
        is None
    )

    on = _service()
    with app.test_request_context("/"):
        embed = build_mission_quick_check_embed(
            mission_ref="42",
            return_endpoint="session.overview",
            return_session_id="sess-1",
            service=on,
            emit_viewed=True,
        )
    assert embed is not None
    assert embed.available is True
    assert embed.start_form.mission_ref.data == "42"
    assert embed.card.title == "Quick Check"


# ---------------------------------------------------------------------------
# Architecture purity
# ---------------------------------------------------------------------------


def test_architecture_purity_application_layer():
    for path in sorted(PACKAGE_ROOT.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        for fragment in FORBIDDEN_IMPORT_FRAGMENTS:
            assert fragment not in text, (
                f"{path.name} must not reference {fragment}"
            )
        assert "flask.request" not in text


def test_architecture_purity_no_assessment_engine_in_aa_app():
    for path in sorted(PACKAGE_ROOT.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        assert "application.assessment" not in text
        assert "domain.assessment" not in text
        assert "AssessmentDeliveryService" not in text


def test_presentation_templates_exist():
    templates = (
        Path(__file__).resolve().parents[3]
        / "app"
        / "templates"
        / "adaptive_assessment"
    )
    for name in (
        "base.html",
        "introduction.html",
        "question.html",
        "reflection.html",
        "completion.html",
        "paused.html",
    ):
        assert (templates / name).is_file()


def test_no_exam_chrome_in_question_template():
    path = (
        Path(__file__).resolve().parents[3]
        / "app"
        / "templates"
        / "adaptive_assessment"
        / "question.html"
    )
    text = path.read_text(encoding="utf-8").lower()
    assert "question 1 of" not in text
    assert "incorrect!" not in text
    assert "correct!" not in text
    assert "score" not in text
    assert "timer" not in text


# ---------------------------------------------------------------------------
# Regression
# ---------------------------------------------------------------------------


def test_regression_alembic_head_unchanged():
    from alembic.config import Config
    from alembic.script import ScriptDirectory

    config = Config("migrations/alembic.ini")
    config.set_main_option("script_location", "migrations")
    script = ScriptDirectory.from_config(config)
    assert script.get_current_head() == "202608240002"


def test_regression_session_type_still_registered():
    from app.application.adaptive_assessment import get_session_type

    quick = get_session_type(SessionTypeId.QUICK_CHECK)
    assert quick.mission_compatible is True


def test_blueprint_registered(app):
    assert "adaptive_assessment" in app.blueprints
    rules = {rule.endpoint for rule in app.url_map.iter_rules()}
    assert "adaptive_assessment.start" in rules
    assert "adaptive_assessment.question" in rules
    assert "adaptive_assessment.completion" in rules
