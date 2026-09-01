"""Session redesign: stage density, practice feedback, completion milestones."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.application.educational_packages.loader import find_package_by_id
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.educational_flow import EducationalStage
from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.session.content_sections import ContentSection
from app.presentation.session.dto.study_session import (
    LearningTask,
    SessionPersistentContext,
    StudySessionPage,
)
from app.presentation.session.services.study_session_service import (
    StudySessionService,
    _content_stage_key,
    _practice_feedback_parts,
    _stage_position_label,
)
from app.presentation.session.view_models import (
    ActivityViewModel,
    SessionPageViewModel,
    SessionShellViewModel,
)

ROOT = Path(__file__).resolve().parents[3]
PACKAGES = ROOT / "app/curriculum/data/educational_packages/cs1"
BODY = ROOT / "app/templates/session/partials/session_body.html"


def _load_package(name: str) -> dict:
    return json.loads((PACKAGES / name).read_text(encoding="utf-8"))


def _base_page(**overrides) -> StudySessionPage:
    ctx = SessionPersistentContext(
        subject="CS1",
        chapter="Probability",
        objective="Apply Bayes",
        activity_label="Practice",
        session_progress="",
    )
    task = LearningTask(
        activity="Practice",
        expected_outcome="",
        estimated_duration="",
        next_milestone="",
        instruction="",
    )
    base = StudySessionPage(
        page_title="Session",
        surface="activity",
        context=ctx,
        task=task,
        primary_label="Continue",
        primary_kind="advance_form",
        primary_enabled=True,
        blocking_issue="",
        exit_href="/student/",
        exit_label="Exit",
        content_title="Reading",
        content_body="",
        content_support="",
        answer_prompt="Your answer",
        show_answer_input=False,
        feedback_outcome="",
        feedback_explanation="",
        disclosures=(),
        technical_lines=(),
        session_id="sess-1",
        activity_id="act-1",
    )
    return replace(base, **overrides) if overrides else base


def _render(
    app,
    study: StudySessionPage,
    *,
    answer_form=None,
    advance_form=None,
    form=None,
):
    with app.test_request_context():
        return app.jinja_env.get_template(
            "session/partials/session_body.html"
        ).render(
            study=study,
            answer_form=answer_form,
            advance_form=advance_form,
            form=form,
            px_microcopy=None,
            csrf_token=lambda: "test",
        )


# --- Stage density / structure with representative package content ---


def test_read_stage_uses_prose_measure_and_position_cue(app):
    pkg = _load_package("5.1.1-bayes-theorem-cs1015.json")
    reading = pkg.get("reading_guidance") or {}
    body = reading.get("lead_line") or "Bayes reading guidance"
    study = _base_page(
        content_stage="read",
        stage_position_label="Read",
        content_title="Reading",
        content_sections=(
            ContentSection(label="Focus", paragraphs=(str(body)[:400],), bullets=()),
        ),
        content_intro_line="Read the Bayes setup carefully.",
    )
    html = _render(app, study)
    assert 'data-content-stage="read"' in html
    assert 'data-session-position="read"' in html
    assert "ds-session-prose" in html
    assert "ds-session-reading-progress" not in html
    assert "ds-stage-indicator" not in html
    assert "ds-session-timer" not in html


def test_worked_example_stage_gives_math_plane_for_bayes_package(app):
    pkg = _load_package("5.1.1-bayes-theorem-cs1015.json")
    we = pkg["worked_example"]
    calc = we["steps"][0]["calculation"]
    study = _base_page(
        content_stage="worked_example",
        stage_position_label="Worked example",
        content_title="Worked example",
        content_sections=(
            ContentSection(
                label="Step 1",
                paragraphs=(we["problem_statement"], calc),
                bullets=(),
            ),
        ),
    )
    html = _render(app, study)
    assert 'data-content-stage="worked_example"' in html
    assert "ds-session-math-plane" in html
    assert "ds-session-derivation-step" in html


def test_worked_example_linear_combinations_derivation_structure(app):
    pkg = _load_package("2.2.4-linear-combinations-cs1005.json")
    we = pkg["worked_example"]
    step2 = we["steps"][1]["calculation"]
    study = _base_page(
        content_stage="worked_example",
        stage_position_label="Worked example",
        content_sections=(
            ContentSection(label="Covariance", paragraphs=(step2,), bullets=()),
        ),
    )
    html = _render(app, study)
    assert "ds-session-stage-density--worked_example" in html
    assert "ds-session-math-plane" in html


def test_practice_stage_mle_numeric_is_maximally_focused(app):
    pkg = _load_package("3.1.2-maximum-likelihood-cs1010.json")
    cp = next(k for k in pkg["knowledge_checks"] if k["response_type"] == "numeric")
    study = _base_page(
        content_stage="practice",
        stage_position_label="Practice",
        content_title="Practice",
        content_intro_line=cp["prompt"],
        response_type="numeric",
        show_answer_input=True,
        primary_kind="answer_form",
        primary_label="Submit answer",
    )
    # Minimal WTForms stub
    class _Field:
        name = "response"
        id = "response"

        def __call__(self, **kwargs):
            return ""

    answer_form = SimpleNamespace(
        hidden_tag=lambda: "",
        session_id=lambda: "",
        activity_id=lambda: "",
        response=_Field(),
        choice=SimpleNamespace(name="choice"),
    )
    html = _render(app, study, answer_form=answer_form)
    assert 'data-content-stage="practice"' in html
    assert "ds-session-practice__prompt" in html
    assert "ds-session-timer" not in html
    assert "ds-stage-indicator" not in html


def test_css_declares_session_measure_and_learning_state_tokens():
    css = (ROOT / "app/static/css/session/session_study.css").read_text(
        encoding="utf-8"
    )
    assert ".ds-session-prose" in css
    assert ".ds-session-math-plane" in css
    assert ".ds-session-learning-state--developing" in css
    assert ".ds-session-learning-state--mastered" in css
    assert ".ds-session-more-guidance" in css
    assert ".ds-session-answer__input--short" in css
    assert ".ds-session-position__count" in css
    assert "body:has(.ds-session-page)" in css


def test_template_drops_numeric_progress_and_streak_chrome():
    text = BODY.read_text(encoding="utf-8")
    assert "ds-session-reading-progress" not in text
    assert "ds-stage-indicator" not in text
    assert "ds-session-timer" not in text
    assert "data-session-position" in text
    assert "data-practice-feedback" in text
    assert "data-completion-what-happened" in text


# --- Practice feedback structure (MCQ / numeric / short) ---


@pytest.mark.parametrize(
    ("response_type", "scored", "expected_means"),
    [
        ("mcq", False, "Incorrect"),
        ("numeric", True, "Correct"),
        (
            "short_structured",
            False,
            "Insufficient evidence to judge this answer confidently",
        ),
    ],
)
def test_practice_feedback_parts_by_response_type(
    response_type: str, scored: bool, expected_means: str
):
    parts = _practice_feedback_parts(
        outcome="Correct" if scored else "Incorrect",
        explanation="General explanation of the method.",
        common_mistake="",
        submitted_response="42" if response_type != "mcq" else "b",
        response_type=response_type,
        scored_correct=scored,
        practice_choices=(("a", "First"), ("b", "Second")),
    )
    assert expected_means in parts["what_it_means"]
    assert "You answered:" in parts["what_happened"]
    assert parts["what_to_understand"] == "General explanation of the method."


def test_practice_feedback_prefers_choice_aware_common_mistake():
    parts = _practice_feedback_parts(
        outcome="Incorrect",
        explanation="General explanation.",
        common_mistake="That choice drops Var(B) from the MSE.",
        submitted_response="c",
        response_type="mcq",
        scored_correct=False,
        practice_choices=(("c", "Only bias squared"),),
    )
    assert parts["what_to_understand"].startswith("That choice drops")
    assert "Only bias squared" in parts["what_happened"]


def test_practice_feedback_renders_three_parts_in_template(app):
    study = _base_page(
        content_stage="practice",
        stage_position_label="Practice",
        feedback_what_happened="You answered: 0.24",
        feedback_what_it_means="Correct",
        feedback_what_to_understand="Posterior updates with the likelihood.",
        feedback_locked=True,
        submitted_response="0.24",
        response_type="numeric",
        show_answer_input=False,
    )
    html = _render(app, study)
    assert 'data-feedback-what-happened="true"' in html
    assert 'data-feedback-what-it-means="true"' in html
    assert 'data-feedback-what-to-understand="true"' in html
    assert 'data-response-locked="true"' in html
    assert "ds-session-answer--locked" in html


# --- Completion + milestones ---


def test_completion_screen_shows_honest_three_parts(app):
    study = _base_page(
        surface="complete",
        content_stage="complete",
        stage_position_label="Complete",
        primary_kind="complete_form",
        primary_label="Return Home",
        completion_what_happened="Session completed on Bayes' theorem.",
        completion_what_we_know="Estimated knowledge for Bayes' theorem is developing.",
        learning_state_key="developing",
        learning_state_label="Estimated knowledge for Bayes' theorem is developing.",
        what_changed_label="Your practice on this topic was recorded.",
        session_milestone_label="",
        topic_display="Bayes' theorem",
    )
    html = _render(app, study)
    assert 'data-completion-what-happened="true"' in html
    assert 'data-completion-what-we-know="true"' in html
    assert 'data-completion-what-changed="true"' in html
    assert 'data-learning-state="developing"' in html
    assert "data-session-milestone" not in html


def test_completion_screen_shows_milestone_when_earned(app):
    study = _base_page(
        surface="complete",
        content_stage="complete",
        stage_position_label="Complete",
        primary_kind="complete_form",
        primary_label="Return Home",
        completion_what_happened="Session completed on Bayes' theorem.",
        completion_what_we_know=(
            "Not yet enough evidence to estimate knowledge for Bayes' theorem."
        ),
        learning_state_key="not_yet_enough_evidence",
        what_changed_label="Your practice on this topic was recorded.",
        session_milestone_label="7-day study streak reached",
        topic_display="Bayes' theorem",
    )
    html = _render(app, study)
    assert 'data-session-milestone="true"' in html
    assert "7-day study streak reached" in html


def test_enrich_completion_wires_milestone_when_detector_returns_one(monkeypatch):
    study = _base_page(
        surface="complete",
        content_stage="complete",
        topic_display="Topic A",
        completion_what_happened="Session completed on Topic A.",
        what_changed_label="Recorded.",
    )

    class _Honest:
        def consume_new_milestones(self, *, user_id, flash_messages=False):
            assert user_id == 9
            assert flash_messages is False
            return ("Estimated knowledge mastered for Topic A",)

    monkeypatch.setattr(
        "app.presentation.student.services.honest_progress_service.HonestProgressService",
        _Honest,
    )
    monkeypatch.setattr(
        "app.presentation.session.services.study_session_service._topic_learning_state",
        lambda **kwargs: ("mastered", "Estimated knowledge for Topic A is mastered."),
    )
    out = StudySessionService().enrich_completion(
        study, user_id=9, subject_code="CS1", topic_id="t1"
    )
    assert out.session_milestone_label == "Estimated knowledge mastered for Topic A"
    assert out.learning_state_key == "mastered"


def test_enrich_completion_omits_milestone_when_none_earned(monkeypatch):
    study = _base_page(
        surface="complete",
        content_stage="complete",
        topic_display="Topic A",
        completion_what_happened="Session completed on Topic A.",
        what_changed_label="Recorded.",
    )

    class _Honest:
        def consume_new_milestones(self, *, user_id, flash_messages=False):
            return ()

    monkeypatch.setattr(
        "app.presentation.student.services.honest_progress_service.HonestProgressService",
        _Honest,
    )
    monkeypatch.setattr(
        "app.presentation.session.services.study_session_service._topic_learning_state",
        lambda **kwargs: (
            "not_yet_enough_evidence",
            "Not yet enough evidence to estimate knowledge for Topic A.",
        ),
    )
    out = StudySessionService().enrich_completion(
        study, user_id=3, subject_code="CS1"
    )
    assert out.session_milestone_label == ""
    assert out.learning_state_key == "not_yet_enough_evidence"


def test_content_stage_keys_from_activity_vm():
    shell = SessionShellViewModel(
        session_id="s1",
        student_id="1",
        active_surface="activity",
        page_eyebrow="",
        page_title="Session",
        page_description="",
        steps=(),
        topic_title="Bayes",
    )
    for activity_type, expected in (
        ("read", "read"),
        ("worked_example", "worked_example"),
        ("practice", "practice"),
    ):
        page = SessionPageViewModel(
            shell=shell,
            activity=ActivityViewModel(
                activity_id="a1",
                activity_type=activity_type,
                stage_label=activity_type.replace("_", " ").title(),
            ),
        )
        assert _content_stage_key(SessionSurface.ACTIVITY, page) == expected
        assert _stage_position_label(expected)


def test_static_asset_version_bumped_for_session_css():
    version = (ROOT / "app/version.py").read_text(encoding="utf-8")
    assert 'APP_VERSION}-g11"' in version or "-g11" in version


def test_reflection_stage_consolidated_headings(app):
    """Reflection: chrome label only, then the reflection question (no heading stack)."""
    study = _base_page(
        surface="reflection",
        content_stage="reflection",
        stage_position_label="Reflection",
        content_title="",
        content_support="Focused practice on Today's topic strengthens recall",
        answer_prompt="What still feels unclear about Today's topic?",
        primary_kind="reflection_form",
        primary_label="Continue to Summary",
        show_answer_input=True,
        task=LearningTask(
            activity="Session reflection",
            expected_outcome="Reflect on Today's topic",
            estimated_duration="",
            next_milestone="Continue to Summary",
            instruction="",
        ),
    )

    class _Field:
        name = "reflection_note"
        id = "reflection_note"

        def __call__(self, **kwargs):
            return ""

    form = SimpleNamespace(
        hidden_tag=lambda: "",
        session_id=lambda: "",
        reflection_note=_Field(),
        confidence_rating=SimpleNamespace(
            name="confidence_rating",
            data=None,
            choices=(),
        ),
    )
    html = _render(app, study, form=form)
    assert 'data-session-position="reflection"' in html
    assert "ds-session-position__stage" in html
    assert "Reflection" in html
    assert "What still feels unclear about Today" in html
    assert "ds-session-reflection__invite" in html
    assert "Session reflection" not in html
    assert "A moment to reflect" not in html
    assert "ds-learning-task" not in html
    assert "Focused practice on Today's topic strengthens recall" not in html
    assert "ds-session-content__title" not in html or "visually-hidden" in html


def test_read_stage_no_redundant_learning_task_heading(app):
    study = _base_page(
        content_stage="read",
        stage_position_label="Read",
        content_title="Reading",
        content_intro_line="Read the Bayes setup carefully.",
    )
    html = _render(app, study)
    assert 'data-session-position="read"' in html
    assert "ds-learning-task" not in html


def test_reading_substance_drops_bridge_question() -> None:
    pack = find_package_by_id("CS1-EP001-PKG-2.6-T-STATISTIC")
    assert pack is not None
    substance = substance_from_package(
        pack, curriculum_identity="cs1-test", topic_id="t-statistic"
    )
    reading = next(
        a for a in substance.activities if a.activity_id == "act-read-1"
    )
    assert reading.stage is EducationalStage.READ
    assert reading.requires_response is False
    assert reading.answer_prompt == ""
    assert "extract from the cmp" not in reading.answer_prompt.lower()


def test_reading_render_has_no_bridge_answer_field(app):
    pkg = _load_package("2.6.5-t-statistic-cs1009.json")
    reading = pkg["reading_guidance"]
    study = _base_page(
        content_stage="read",
        stage_position_label="Read",
        content_title="Reading",
        stage_step_label="Step 1 of 4",
        content_intro_line=f"Mission: {pkg['mission']['display_title']}",
        content_sections=(
            ContentSection(
                label="Open the CMP",
                paragraphs=(),
                bullets=(f"Open your CMP at {reading['open_point']}",),
            ),
            ContentSection(
                label="Focus questions",
                paragraphs=(),
                bullets=tuple(reading["focus_questions"]),
            ),
        ),
        primary_kind="advance_form",
        primary_label="Continue",
        show_answer_input=False,
    )
    html = _render(app, study)
    assert "What did you extract from the CMP setup?" not in html
    assert "ds-session-answer__format-hint" not in html
    assert 'data-session-step-count="true"' in html
    assert "Step 1 of 4" in html
    assert "Focus questions" in html


def test_worked_example_substance_drops_bridge_question() -> None:
    pack = find_package_by_id("CS1-EP001-PKG-2.6-T-STATISTIC")
    assert pack is not None
    substance = substance_from_package(
        pack, curriculum_identity="cs1-test", topic_id="t-statistic"
    )
    example = next(
        a for a in substance.activities if a.activity_id == "act-example-1"
    )
    assert example.stage is EducationalStage.WORKED_EXAMPLE
    assert example.requires_response is False
    assert example.answer_prompt == ""
    assert "calculated quantity" not in example.answer_prompt.lower()


def test_worked_example_render_has_no_bridge_answer_field(app):
    pkg = _load_package("2.6.5-t-statistic-cs1009.json")
    we = pkg["worked_example"]
    study = _base_page(
        content_stage="worked_example",
        stage_position_label="Worked example",
        content_title="Worked example",
        stage_step_label="Step 2 of 4",
        content_sections=(
            ContentSection(
                label="Given values",
                paragraphs=(we["problem_statement"],),
                bullets=(),
            ),
        ),
        primary_kind="advance_form",
        primary_label="Continue to Practice",
        show_answer_input=False,
    )
    html = _render(app, study)
    assert "Which calculated quantity will you reuse in the checks?" not in html
    assert "Which pause-point note will you reuse in the checks?" not in html
    assert "ds-session-answer__format-hint" not in html
    assert 'data-session-step-count="true"' in html
    assert "Step 2 of 4" in html


def test_stage_step_count_renders_in_session_chrome(app):
    study = _base_page(
        content_stage="read",
        stage_position_label="Read",
        stage_step_label="Step 1 of 4",
    )
    html = _render(app, study)
    assert 'data-session-step-count="true"' in html
    assert "Step 1 of 4" in html
    assert "ds-session-position__count" in html


def test_more_guidance_panel_uses_step_and_outcome_spacing_classes(app):
    study = _base_page(
        content_stage="worked_example",
        stage_position_label="Worked example",
        content_title="Worked example",
        content_sections_more=(
            ContentSection(
                label="Worked solution — Step 1",
                paragraphs=("Set up the likelihood.",),
                bullets=(),
            ),
            ContentSection(
                label="Worked solution — Step 2",
                paragraphs=("Differentiate and solve.",),
                bullets=(),
            ),
            ContentSection(
                label="Final answer",
                paragraphs=(),
                bullets=("θ̂ = 0.24",),
            ),
            ContentSection(
                label="Common pitfall",
                paragraphs=(),
                bullets=("Forgetting the log step.",),
            ),
        ),
    )
    html = _render(app, study)
    assert 'data-ux="reading-more-guidance"' in html
    assert "ds-session-more-guidance" in html
    assert "ds-session-more-guidance__step" in html
    assert "ds-session-more-guidance__outcome" in html
    assert "ds-session-more-guidance__pitfall" in html
    assert "Worked solution — Step 1" in html
    assert "Final answer" in html


def test_short_answer_field_has_format_hint_and_compact_size(app):
    study = _base_page(
        content_stage="practice",
        stage_position_label="Practice",
        stage_step_label="Step 3 of 4",
        content_intro_line="Closed-book. Name the pivot for a one-sample mean.",
        response_type="short_structured",
        answer_prompt="Closed-book. Name the pivot for a one-sample mean.",
        show_answer_input=True,
        primary_kind="answer_form",
        primary_label="Submit answer",
    )

    class _Field:
        name = "response"
        id = "response"

        def __call__(self, **kwargs):
            attrs = " ".join(
                f'{key.replace("_", "-")}="{value}"'
                for key, value in kwargs.items()
            )
            return f"<textarea {attrs}></textarea>"

    answer_form = SimpleNamespace(
        hidden_tag=lambda: "",
        session_id=lambda: "",
        activity_id=lambda: "",
        response=_Field(),
        choice=SimpleNamespace(name="choice"),
    )
    html = _render(app, study, answer_form=answer_form)
    assert 'id="session-answer-format-hint"' in html
    assert "ds-session-answer__format-hint" in html
    assert "ds-session-answer__input--short" in html
    assert 'rows="2"' in html or "rows=&#34;2&#34;" in html
    assert (
        'placeholder="e.g. a value, symbol, or brief phrase"' in html
        or "placeholder=&#34;e.g. a value, symbol, or brief phrase&#34;" in html
    )
    assert "not a full explanation" in html
