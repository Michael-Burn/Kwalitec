"""Session Overview briefing must not mad-lib generic decision titles.

Fallback missions (e.g. \"Continue with CS1\" with no authored package) must
omit Learning objectives / Concept focus / Checkpoint / Reflection rather
than treating the placeholder title as a syllabus concept.
"""

from __future__ import annotations

from flask import render_template

from app.application.educational_authoring.writing import is_generic_session_topic_title
from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.session.services.study_session_service import StudySessionService
from app.presentation.session.view_models import (
    OverviewViewModel,
    SessionPageViewModel,
    SessionShellViewModel,
)


def _overview_page(
    *,
    topic_title: str,
    objectives: tuple[str, ...] = (),
) -> SessionPageViewModel:
    return SessionPageViewModel(
        shell=SessionShellViewModel(
            session_id="sess-generic",
            student_id="stu-1",
            active_surface=SessionSurface.OVERVIEW.value,
            topic_title=topic_title,
        ),
        overview=OverviewViewModel(
            objective=f"Strengthen {topic_title}",
            learning_goal=topic_title,
            why_studying=(
                "Continuing with CS1 keeps momentum on your current study path."
            ),
            topics=(topic_title,),
            learning_objectives=objectives
            or (f"Strengthen understanding of {topic_title}",),
            begin_label="Begin Session",
            begin_enabled=True,
            session_id="sess-generic",
        ),
        primary_cta_label="Begin Session",
        primary_cta_enabled=True,
    )


def test_is_generic_session_topic_title_detects_continue_with_paper() -> None:
    assert is_generic_session_topic_title("Continue with CS1")
    assert is_generic_session_topic_title("Today's topic")
    assert is_generic_session_topic_title("Study CM2")
    assert not is_generic_session_topic_title(
        "Place GLM responses in the exponential family"
    )
    assert not is_generic_session_topic_title(
        "2.6.5 Understand and use generalised linear models"
    )


def test_overview_briefing_omits_mad_libs_for_continue_with_cs1() -> None:
    page = _overview_page(topic_title="Continue with CS1")
    briefing = StudySessionService._overview_briefing(
        page, flow_label="Read → Worked example → Practice → Reflection"
    )
    assert briefing["learning_objectives"] == ()
    assert briefing["concept_focus"] == ()
    assert briefing["checkpoint_preview"] == ""
    assert briefing["reflection_preview"] == ""
    # Catalogue why from overview is kept; narrative mad-lib is not invented.
    assert "momentum" in str(briefing["why_today"]).lower()
    assert "Continue with CS1" not in str(briefing["checkpoint_preview"])
    assert briefing["session_stages"] == (
        "Read",
        "Worked example",
        "Practice",
        "Reflection",
    )


def test_overview_briefing_keeps_real_topic_fields() -> None:
    topic = "Place GLM responses in the exponential family"
    page = _overview_page(
        topic_title=topic,
        objectives=("Recognise exponential-family membership for named responses.",),
    )
    briefing = StudySessionService._overview_briefing(page, flow_label="")
    assert briefing["learning_objectives"]
    assert any("exponential" in o.lower() for o in briefing["learning_objectives"])
    assert briefing["concept_focus"]
    assert topic in briefing["concept_focus"] or any(
        "exponential" in c.lower() for c in briefing["concept_focus"]
    )
    assert "Checkpoint:" in briefing["checkpoint_preview"]
    assert topic in briefing["checkpoint_preview"]
    assert "Reflect briefly:" in briefing["reflection_preview"]
    assert topic in briefing["reflection_preview"]


def test_build_page_session_details_omit_generic_mad_libs(app, ctx) -> None:
    page = _overview_page(topic_title="Continue with CS1")
    study = StudySessionService().build_page(page)
    assert study.learning_objectives == ()
    assert study.concept_focus == ()
    assert study.checkpoint_preview == ""
    assert study.reflection_preview == ""

    with app.test_request_context("/session/sess-generic/"):
        from app.presentation.session.forms import BeginSessionForm

        form = BeginSessionForm()
        form.session_id.data = "sess-generic"
        html = render_template(
            "session/partials/session_body.html",
            study=study,
            form=form,
            answer_form=None,
            advance_form=None,
        )
    assert 'data-briefing="concept-focus"' not in html
    assert 'data-briefing="checkpoint"' not in html
    assert 'data-briefing="reflection"' not in html
    assert 'data-briefing="learning-objectives"' not in html
    assert "Checkpoint: can you explain Continue with CS1" not in html
    # Why-today catalogue line may still render.
    assert 'data-briefing="why-today"' in html
