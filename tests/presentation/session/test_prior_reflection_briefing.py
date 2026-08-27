"""Tier A prior-reflection Session Overview briefing block."""

from __future__ import annotations

from flask import render_template

from app.domain.session_experience.session_workspace import SessionSurface
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.session.composition import SessionExperienceComposition
from app.infrastructure.session.store import SessionDocumentStore
from app.presentation.session.dto.study_session import StudySessionPage
from app.presentation.session.services.study_session_service import (
    StudySessionService,
)
from app.presentation.session.view_models import (
    OverviewViewModel,
    SessionPageViewModel,
    SessionShellViewModel,
)


def _overview_page(
    *,
    session_id: str = "sess-current",
    student_id: str = "stu-1",
    topic_title: str = "Place GLM responses in the exponential family",
) -> SessionPageViewModel:
    return SessionPageViewModel(
        shell=SessionShellViewModel(
            session_id=session_id,
            student_id=student_id,
            active_surface=SessionSurface.OVERVIEW.value,
            topic_title=topic_title,
        ),
        overview=OverviewViewModel(
            objective=f"Strengthen {topic_title}",
            learning_goal=topic_title,
            why_studying="This topic closes a coverage gap before the exam.",
            topics=(topic_title,),
            learning_objectives=(f"Strengthen understanding of {topic_title}",),
            begin_label="Begin Session",
            begin_enabled=True,
            session_id=session_id,
            subject_code="CS1",
        ),
        primary_cta_label="Begin Session",
        primary_cta_enabled=True,
    )


def _wire_composition(app, store: SessionDocumentStore) -> None:
    composition = SessionExperienceComposition(
        store=store,
        seed_demo_learners=False,
    )
    app.config["SESSION_EXPERIENCE_COMPOSITION"] = composition
    # Drop request-cached composition so factory picks up app.config.
    from flask import g

    g.pop("session_experience_composition", None)


def test_prior_reflection_excerpt_on_overview_when_past_note_exists(app, ctx) -> None:
    store = SessionDocumentStore()
    past = "I got stuck on the link function choice last sitting."
    adapter = LearningSessionPersistenceAdapter(store=store)
    store.save(
        "lsr.handle",
        "sess-past",
        {
            "session_id": "sess-past",
            "student_id": "stu-1",
            "topic_id": "topic-glm",
            "mission_instance_id": "m-past",
            "reflection_note": past,
            "status": "completed",
        },
    )
    store.save(
        "lsr.handle",
        "sess-current",
        {
            "session_id": "sess-current",
            "student_id": "stu-1",
            "topic_id": "topic-glm",
            "mission_instance_id": "m-now",
            "reflection_note": "",
            "status": "open",
        },
    )
    _wire_composition(app, store)

    with app.test_request_context("/session/sess-current/"):
        study = StudySessionService().build_page(_overview_page())
        assert study.prior_reflection_excerpt == past
        assert adapter.find_prior_reflection_note(
            student_id="stu-1",
            topic_id="topic-glm",
            exclude_session_id="sess-current",
        ) == past

        from app.presentation.session.forms import BeginSessionForm

        form = BeginSessionForm()
        form.session_id.data = "sess-current"
        html = render_template(
            "session/partials/session_body.html",
            study=study,
            form=form,
            answer_form=None,
            advance_form=None,
        )
    assert 'data-briefing="prior-reflection"' in html
    assert "Last time" in html
    assert f'You wrote: "{past}"' in html


def test_prior_reflection_absent_when_no_qualifying_past(app, ctx) -> None:
    store = SessionDocumentStore()
    store.save(
        "lsr.handle",
        "sess-current",
        {
            "session_id": "sess-current",
            "student_id": "stu-1",
            "topic_id": "topic-glm",
            "mission_instance_id": "m-now",
            "reflection_note": "",
            "status": "open",
        },
    )
    _wire_composition(app, store)

    with app.test_request_context("/session/sess-current/"):
        study = StudySessionService().build_page(_overview_page())
        assert study.prior_reflection_excerpt == ""

        from app.presentation.session.forms import BeginSessionForm

        form = BeginSessionForm()
        form.session_id.data = "sess-current"
        html = render_template(
            "session/partials/session_body.html",
            study=study,
            form=form,
            answer_form=None,
            advance_form=None,
        )
    assert 'data-briefing="prior-reflection"' not in html


def test_prior_reflection_truncates_long_notes(app, ctx) -> None:
    store = SessionDocumentStore()
    long_note = "A" * 150
    store.save(
        "lsr.handle",
        "sess-past",
        {
            "session_id": "sess-past",
            "student_id": "stu-1",
            "topic_id": "topic-glm",
            "reflection_note": long_note,
            "status": "completed",
        },
    )
    store.save(
        "lsr.handle",
        "sess-current",
        {
            "session_id": "sess-current",
            "student_id": "stu-1",
            "topic_id": "topic-glm",
            "status": "open",
        },
    )
    _wire_composition(app, store)

    with app.test_request_context("/session/sess-current/"):
        study = StudySessionService().build_page(_overview_page())
    assert len(study.prior_reflection_excerpt) == 118  # 117 + ellipsis
    assert study.prior_reflection_excerpt.endswith("…")
    assert study.prior_reflection_excerpt.startswith("A" * 117)


def test_study_session_page_defaults_prior_reflection_empty() -> None:
    """Frozen DTO default keeps Overview unchanged when field omitted."""
    from app.presentation.session.dto.study_session import (
        LearningTask,
        SessionPersistentContext,
    )

    page = StudySessionPage(
        page_title="Session",
        surface="overview",
        context=SessionPersistentContext(
            subject="CS1",
            chapter="",
            objective="",
            activity_label="",
            session_progress="",
        ),
        task=LearningTask(
            activity="",
            expected_outcome="",
            estimated_duration="",
            next_milestone="",
            instruction="",
        ),
        primary_label="Begin",
        primary_kind="begin_form",
        primary_enabled=True,
        blocking_issue="",
        exit_href="/",
        exit_label="Exit",
        content_title="",
        content_body="",
        content_support="",
        answer_prompt="",
        show_answer_input=False,
        feedback_outcome="",
        feedback_explanation="",
        disclosures=(),
        technical_lines=(),
        session_id="s1",
        activity_id="",
    )
    assert page.prior_reflection_excerpt == ""
