"""ILE-001A — Adaptive Assessment product foundations tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.application.adaptive_assessment import (
    FORBIDDEN_STUDENT_TERMS,
    SESSION_TYPES,
    SessionTypeId,
    accessibility_for_session,
    assert_adaptive_assessment_copy_safe,
    build_mission_presentation_contract,
    build_product_contracts,
    build_session_presentation_contract,
    build_telemetry_event,
    format_message,
    get_copy,
    get_default_catalogue,
    get_session_type,
    iter_copy_entries,
    iter_session_types,
    reduced_motion_safe,
    resolve_adaptive_assessment_flags,
    resolve_copy,
    validate_product_resources,
    validate_registered_adaptive_assessment_resources,
)
from app.application.adaptive_assessment.localisation import format_pluralizable
from app.application.adaptive_assessment.telemetry import (
    FORBIDDEN_PAYLOAD_KEYS,
    InMemoryTelemetrySink,
    ProductTelemetryRecorder,
    TelemetryEventName,
)
from app.application.adaptive_assessment.terminology import TerminologyError

PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "adaptive_assessment"
)

# Educational / intelligence modules that Adaptive Assessment foundations
# must never import (architecture purity — ILE-001A).
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


# ---------------------------------------------------------------------------
# Feature flags
# ---------------------------------------------------------------------------


def test_feature_flags_default_all_off():
    flags = resolve_adaptive_assessment_flags(environ={})
    assert flags.ENABLE_ADAPTIVE_ASSESSMENT is False
    assert flags.ENABLE_QUICK_CHECK is False
    assert flags.ENABLE_DEEP_CHECK is False
    assert flags.ENABLE_RECOVERY_CHECK is False
    assert flags.ENABLE_CONFIDENCE_CHECK is False
    assert flags.ENABLE_READINESS_CHECK is False
    assert flags.ENABLE_CONTEXTUAL_FRAMING is False
    assert flags.enabled_subjects == frozenset()
    assert flags.enabled_cohorts == frozenset()
    assert flags.is_globally_enabled() is False
    assert flags.is_available("quick_check", subject_code="CS1") is False
    assert flags.is_contextual_framing_enabled() is False


def test_feature_flags_global_and_session_type():
    flags = resolve_adaptive_assessment_flags(
        environ={
            "KWALITEC_ADAPTIVE_ASSESSMENT": "1",
            "KWALITEC_QUICK_CHECK": "true",
        }
    )
    assert flags.is_globally_enabled() is True
    assert flags.is_session_type_enabled("quick_check") is True
    assert flags.is_session_type_enabled("deep_check") is False
    assert flags.is_available("quick_check") is True
    assert flags.is_available("deep_check") is False


def test_feature_flags_subject_allowlist():
    flags = resolve_adaptive_assessment_flags(
        environ={
            "KWALITEC_ADAPTIVE_ASSESSMENT": "1",
            "KWALITEC_QUICK_CHECK": "1",
            "KWALITEC_ADAPTIVE_ASSESSMENT_SUBJECTS": "CS1, CM2",
        }
    )
    assert flags.is_subject_enabled("CS1") is True
    assert flags.is_subject_enabled("CM2") is True
    assert flags.is_subject_enabled("SP1") is False
    assert flags.is_available("quick_check", subject_code="CS1") is True
    assert flags.is_available("quick_check", subject_code="SP1") is False


def test_feature_flags_cohort_allowlist():
    flags = resolve_adaptive_assessment_flags(
        environ={
            "KWALITEC_ADAPTIVE_ASSESSMENT": "yes",
            "KWALITEC_QUICK_CHECK": "on",
            "KWALITEC_ADAPTIVE_ASSESSMENT_COHORTS": "alpha,dogfood",
        }
    )
    assert flags.is_cohort_enabled("alpha") is True
    assert flags.is_cohort_enabled("prod") is False
    assert (
        flags.is_available(
            "quick_check", subject_code="CS1", cohort_id="alpha"
        )
        is True
    )
    assert (
        flags.is_available(
            "quick_check", subject_code="CS1", cohort_id="prod"
        )
        is False
    )


# ---------------------------------------------------------------------------
# Session registry
# ---------------------------------------------------------------------------


def test_session_registry_contains_required_types():
    required = {
        SessionTypeId.QUICK_CHECK,
        SessionTypeId.DEEP_CHECK,
        SessionTypeId.RECOVERY_CHECK,
        SessionTypeId.CONFIDENCE_CHECK,
        SessionTypeId.READINESS_CHECK,
    }
    assert required.issubset(set(SESSION_TYPES))
    sessions = iter_session_types()
    assert len(sessions) >= 5
    quick = get_session_type(SessionTypeId.QUICK_CHECK)
    assert quick.display_name == "Quick Check"
    assert quick.mission_compatible is True
    assert quick.tutor_compatible is True
    assert quick.icon_token
    assert quick.colour_token
    assert quick.expected_duration_minutes > 0
    assert quick.educational_intent
    assert quick.student_facing_copy_key


def test_session_registry_unknown_raises():
    with pytest.raises(KeyError):
        get_session_type("mock_exam")


# ---------------------------------------------------------------------------
# Copy registry
# ---------------------------------------------------------------------------


def test_copy_registry_required_keys():
    required = {
        "session.quick_check.name",
        "action.continue_learning",
        "action.strengthen_understanding",
        "action.build_confidence",
        "explain.why_am_i_seeing_this",
        "uncertainty.not_enough_evidence",
        "uncertainty.gather_more",
    }
    keys = {entry.key for entry in iter_copy_entries()}
    assert required.issubset(keys)
    assert get_copy("action.continue_learning").default == "Continue Learning"
    assert get_copy("session.quick_check.name").default == "Quick Check"


def test_copy_registry_unknown_raises():
    with pytest.raises(KeyError):
        get_copy("session.mock_exam.name")


# ---------------------------------------------------------------------------
# Terminology
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("term", list(FORBIDDEN_STUDENT_TERMS))
def test_terminology_rejects_forbidden_terms(term: str):
    with pytest.raises(TerminologyError):
        assert_adaptive_assessment_copy_safe(f"Please {term} now")


def test_terminology_allows_safe_copy():
    text = "Quick Check — helps keep today's plan accurate."
    assert assert_adaptive_assessment_copy_safe(text) == text


def test_terminology_validate_product_resources():
    violations = validate_product_resources(
        {
            "bad": "You will fail this exam",
            "good": "Continue Learning",
        }
    )
    assert len(violations) >= 2
    assert all(v.source == "bad" for v in violations)


def test_registered_resources_pass_terminology_guard():
    validate_registered_adaptive_assessment_resources()


# ---------------------------------------------------------------------------
# Localisation
# ---------------------------------------------------------------------------


def test_localisation_interpolation_and_plurals():
    assert format_message("Hello {name}", name="Ada") == "Hello Ada"
    assert format_message("Hello {name}") == "Hello {name}"
    catalogue = get_default_catalogue()
    assert catalogue.locale == "en"
    assert catalogue.has("duration.about_minutes")
    one = format_pluralizable("duration.about_minutes", count=1)
    other = format_pluralizable("duration.about_minutes", count=5)
    assert "1 minute" in one
    assert "5 minutes" in other
    assert resolve_copy("action.continue_learning") == "Continue Learning"
    assert "Quick Check" in resolve_copy(
        "a11y.session_region", session_name="Quick Check"
    )


# ---------------------------------------------------------------------------
# Accessibility
# ---------------------------------------------------------------------------


def test_accessibility_metadata_for_session():
    meta = accessibility_for_session(SessionTypeId.QUICK_CHECK)
    assert "Quick Check" in meta.accessible_label
    assert meta.keyboard_navigable is True
    assert meta.semantic_role == "region"
    assert meta.reduced_motion_compatible is True
    assert meta.colour_not_sole_encoding is True
    assert meta.screen_reader_description
    assert reduced_motion_safe(prefers_reduced_motion=True) is False
    assert reduced_motion_safe(prefers_reduced_motion=False) is True


# ---------------------------------------------------------------------------
# Telemetry
# ---------------------------------------------------------------------------


def test_telemetry_allowlisted_events_and_privacy():
    sink = InMemoryTelemetrySink()
    recorder = ProductTelemetryRecorder(sink=sink)
    event = build_telemetry_event(
        TelemetryEventName.QUICK_CHECK_STARTED,
        session_type_id="quick_check",
        subject_code="CS1",
        payload={"surface": "mission_step"},
    )
    recorder.record(event)
    assert len(sink.events) == 1
    assert sink.events[0].event_name == "QuickCheckStarted"

    with pytest.raises(ValueError):
        build_telemetry_event("UnknownEvent")

    for key in ("answer", "score", "twin_state", "learner_state"):
        assert key in FORBIDDEN_PAYLOAD_KEYS
        with pytest.raises(ValueError):
            build_telemetry_event(
                TelemetryEventName.QUICK_CHECK_COMPLETED,
                payload={key: "secret"},
            )


def test_telemetry_named_events_cover_milestone_set():
    names = {e.value for e in TelemetryEventName}
    assert {
        "AdaptiveAssessmentViewed",
        "QuickCheckStarted",
        "QuickCheckDismissed",
        "QuickCheckCompleted",
        "AssessmentDeferred",
        "AssessmentExplained",
    }.issubset(names)


# ---------------------------------------------------------------------------
# Product contracts
# ---------------------------------------------------------------------------


def test_product_contracts_are_immutable_presentation_only():
    contracts = build_product_contracts()
    assert len(contracts.sessions) == len(SESSION_TYPES)
    quick = build_session_presentation_contract(SessionTypeId.QUICK_CHECK)
    assert quick.display_name == "Quick Check"
    assert quick.entry_frame
    assert quick.accessibility.keyboard_navigable is True
    assert contracts.content.continue_learning == "Continue Learning"
    assert contracts.content.why_am_i_seeing_this == "Why am I seeing this?"
    assert contracts.content.not_enough_evidence == "Not enough evidence yet"
    assert (
        contracts.content.gather_more
        == "Let's gather a little more information"
    )
    mission = build_mission_presentation_contract(SessionTypeId.QUICK_CHECK)
    assert mission.mission_compatible is True
    assert mission.step_label == "Quick Check"
    # Frozen dataclasses
    with pytest.raises(Exception):
        quick.display_name = "Exam"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Architecture purity
# ---------------------------------------------------------------------------


def test_architecture_purity_no_educational_imports():
    for path in sorted(PACKAGE_ROOT.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        for fragment in FORBIDDEN_IMPORT_FRAGMENTS:
            assert fragment not in text, (
                f"{path.name} must not reference {fragment}"
            )


def test_architecture_purity_no_flask_request_coupling():
    for path in sorted(PACKAGE_ROOT.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        assert "flask.request" not in text
        assert "from flask" not in text


# ---------------------------------------------------------------------------
# Regression — no educational behaviour / schema impact
# ---------------------------------------------------------------------------


def test_regression_alembic_head_unchanged():
    from alembic.config import Config
    from alembic.script import ScriptDirectory

    config = Config("migrations/alembic.ini")
    config.set_main_option("script_location", "migrations")
    script = ScriptDirectory.from_config(config)
    assert script.get_current_head() == "202608300001"


def test_regression_flags_do_not_enable_learner_behaviour_by_default():
    """No learner-facing adaptive behaviour until ILE-001B+ enables flags."""
    flags = resolve_adaptive_assessment_flags(environ={})
    for session_id in (
        "quick_check",
        "deep_check",
        "recovery_check",
        "confidence_check",
        "readiness_check",
    ):
        assert flags.is_available(session_id) is False
