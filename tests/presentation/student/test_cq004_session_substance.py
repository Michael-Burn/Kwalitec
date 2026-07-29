"""CQ-004 — Session Substance presentation and adapter contracts."""

from __future__ import annotations

from flask import render_template

from app.application.session_experience.activity_service import _build_activity
from app.application.session_experience.dto.activity_snapshot import ActivitySnapshot
from app.application.session_experience.dto.completion_snapshot import (
    CompletionSnapshot,
    ReturnHomeActionSnapshot,
)
from app.application.student_experience.dto.commitment_reflection_snapshot import (
    CommitmentReflectionSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.student_experience.dto.recommendation_commitment_snapshot import (
    RecommendationCommitmentSnapshot,
)
from app.application.student_experience.recommendation_commitment import (
    CONTINUITY_REFLECTION,
    WHAT_WAS_LEARNED_HUMBLE,
)
from app.domain.session_experience.activity_projection import ActivityPhase
from app.infrastructure.engines.opaque_bridges import ActivityOpaqueBridge
from app.infrastructure.session.activity_adapter import SessionActivityAdapter
from app.infrastructure.session.defaults import default_activity
from app.infrastructure.session.runtime_adapter import SessionRuntimeAdapter
from app.infrastructure.session.store import SessionDocumentStore
from app.presentation.session.messages import FLASH_SUCCESS
from app.presentation.session.view_models import activity_vm, completion_vm
from app.presentation.student.view_models import home_vm
from tests.presentation.student.helpers import render_student_home


def test_default_activity_is_topic_threaded():
    activity = default_activity(
        "stu-1", session_id="sess-1", index=1, total=3, topic_title="Cash flows"
    )
    assert "Cash flows" in activity["question"]
    assert activity["topic_title"] == "Cash flows"
    assert "Focused practice on Cash flows" == activity["context"]
    assert "Practice item" not in activity["question"]
    assert "Question 1" not in activity["question"]


def test_final_default_activity_cta_continues_to_reflection():
    activity = default_activity(
        "stu-1", session_id="sess-1", index=3, total=3, topic_title="Cash flows"
    )
    assert activity["next_action_label"] == "Continue to Reflection"


def test_activity_bridge_avoids_generic_practice_item_and_twin_copy():
    bridge = ActivityOpaqueBridge(activity_count=3)
    current = bridge.get_current_activity_opaque(
        "stu-1", session_id="sess-1", topic_title="Leases"
    )
    assert "Leases" in current["question"]
    assert "Practice item" not in current["question"]
    submitted = bridge.submit_response_opaque(
        "stu-1",
        session_id="sess-1",
        activity_id=current["activity_id"],
        response="an answer",
        topic_title="Leases",
    )
    assert isinstance(submitted["explanation"], str)
    assert "Twin" not in submitted["explanation"]
    assert "Leases" in submitted["explanation"]


def test_build_activity_coerces_explanation_dict():
    domain = _build_activity(
        "sess-1",
        {
            "activity_id": "act-1",
            "question": "Explain leases",
            "explanation": {"summary": "Compare to the worked example."},
            "activity_index": 1,
            "activities_total": 2,
            "phase": "explained",
        },
        phase=ActivityPhase.EXPLAINED,
    )
    assert domain.explanation == "Compare to the worked example."
    assert "{" not in domain.explanation


def test_activity_adapter_threads_overview_topic():
    store = SessionDocumentStore()
    runtime = SessionRuntimeAdapter(store=store)
    runtime.put_overview(
        "stu-1",
        session_id="sess-cash",
        document={
            "objective": "Strengthen Cash flows",
            "topics": ("Cash flows",),
            "mission_id": "m1",
        },
    )
    activity = SessionActivityAdapter(store=store, activity_count=3)
    current = activity.get_current_activity("stu-1", session_id="sess-cash")
    assert current is not None
    assert current["topic_title"] == "Cash flows"
    assert "Cash flows" in current["question"]


def test_activity_vm_final_cta_label():
    vm = activity_vm(
        ActivitySnapshot(
            activity_id="act-3",
            session_id="sess-1",
            question="Final question",
            activity_index=3,
            activities_total=3,
            next_action_label="Continue",
            is_final_activity=True,
            has_explanation=True,
            explanation="Takeaway",
        )
    )
    assert vm.next_action_label == "Continue to Reflection"
    assert vm.is_final is True


def test_completion_vm_headline_uses_topic():
    vm = completion_vm(
        CompletionSnapshot(
            session_id="sess-1",
            student_id="stu-1",
            topics_completed=("Cash flows",),
            activities_completed=3,
            can_return_home=True,
            return_home=ReturnHomeActionSnapshot(),
        )
    )
    assert "Cash flows" in vm.headline
    assert vm.headline.startswith("You completed today's Session")
    assert vm.learning_insights


def test_activities_complete_flash_exists():
    msg = FLASH_SUCCESS["activities_complete"]
    assert msg.endswith(".")
    assert "reflection" in msg.lower()


def test_overview_intro_echoes_topic(app, ctx):
    from app.presentation.session.dto.study_session import (
        LearningTask,
        SessionPersistentContext,
        StudySessionPage,
    )

    study = StudySessionPage(
        page_title="Session",
        surface="overview",
        context=SessionPersistentContext(
            subject="Cash flows",
            chapter="Cash flows",
            objective="Strengthen Cash flows",
            activity_label="Begin practice",
            session_progress="Session step 1 of 4",
            elapsed_label="About 25 minutes",
        ),
        task=LearningTask(
            activity="Begin practice",
            expected_outcome="Strengthen Cash flows",
            estimated_duration="About 25 minutes",
            next_milestone="3 learning activities",
            instruction="Start the session to open the first learning activity.",
        ),
        primary_label="Start Session",
        primary_kind="begin_form",
        primary_enabled=True,
        blocking_issue="",
        exit_href="/student/",
        exit_label="Exit",
        content_title="Current objective",
        content_body="Strengthen Cash flows",
        content_support="",
        answer_prompt="Your answer",
        show_answer_input=False,
        feedback_outcome="",
        feedback_explanation="",
        disclosures=(),
        technical_lines=("Session ID · sess-1",),
        session_id="sess-1",
        activity_id="",
        mission_id="m1",
    )
    with app.test_request_context("/session/sess-1/overview"):
        html = render_template(
            "session/overview.html",
            page=None,
            study=study,
            form=None,
            quick_check_embed=None,
        )
    assert "Cash flows" in html
    assert "Strengthen Cash flows" in html
    assert "Time remaining" not in html
    assert "Readiness estimate" not in html


def test_completion_card_uses_headline(app, ctx):
    from app.presentation.session.dto.study_session import (
        LearningTask,
        SessionPersistentContext,
        StudySessionPage,
    )

    study = StudySessionPage(
        page_title="Session",
        surface="summary",
        context=SessionPersistentContext(
            subject="Cash flows",
            chapter="Cash flows",
            objective="Complete the current practice step",
            activity_label="Session complete",
            session_progress="Session step 4 of 4",
            elapsed_label="25 minutes studied",
        ),
        task=LearningTask(
            activity="Complete session",
            expected_outcome="Close practice and return to Home",
            estimated_duration="25 minutes studied",
            next_milestone="Home",
            instruction="Practice on Cash flows is finished.",
        ),
        primary_label="Return Home",
        primary_kind="complete_form",
        primary_enabled=True,
        blocking_issue="",
        exit_href="/student/",
        exit_label="Exit",
        content_title="Session complete",
        content_body="Session practice on Cash flows is complete.",
        content_support="",
        answer_prompt="Your answer",
        show_answer_input=False,
        feedback_outcome="",
        feedback_explanation="",
        disclosures=(),
        technical_lines=("Session ID · sess-1",),
        session_id="sess-1",
        activity_id="",
    )
    with app.test_request_context("/session/sess-1/summary"):
        html = render_template(
            "session/summary.html",
            page=None,
            study=study,
            form=None,
        )
    assert "Cash flows" in html
    assert "Session practice" in html
    assert "Return Home" in html or "complete_form" in study.primary_kind
    assert "Readiness estimate" not in html


def test_home_commitment_reflection_not_on_home(app, ctx):
    reflection = CommitmentReflectionSnapshot(
        what_you_did="Completed: Cash flows",
        what_changed="Reassess after tonight.",
        why_it_mattered="Exam readiness.",
        what_was_learned=WHAT_WAS_LEARNED_HUMBLE,
        what_happens_next="Return Home for the next Mission.",
    )
    commitment = RecommendationCommitmentSnapshot(
        state="completed",
        title="Cash flows",
        continuity_line=CONTINUITY_REFLECTION,
        reflection=reflection,
    )
    page_home = home_vm(
        HomeSnapshot(
            student_id="1",
            greeting="Welcome back",
            has_recommendation=True,
            recommendation_title="Cash flows",
            can_start_session=False,
            commitment=commitment,
        ),
        unified_journey=False,
    )
    html = render_student_home(app, page_home)
    assert 'data-reflection-compact="true"' not in html
    assert "More about this session" not in html
    assert 'data-reflection-field="what_you_did"' not in html
    assert 'data-reflection-field="what_happens_next"' not in html
    assert 'data-reflection-field="what_was_learned"' not in html
