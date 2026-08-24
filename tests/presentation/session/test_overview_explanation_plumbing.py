"""Pass (a) — Overview carries Adaptive ExplanationSnapshot (data only)."""

from __future__ import annotations

from app.application.session_experience.dto.overview_snapshot import OverviewSnapshot
from app.application.session_experience.facade import SessionFlowSnapshot
from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.domain.session_experience.session_workspace import (
    SessionSurface,
    SessionWorkspace,
)
from app.infrastructure.session.composition import SessionExperienceComposition
from app.presentation.session.services.study_session_service import (
    StudySessionService,
)
from app.presentation.session.view_models import overview_vm, page_from_flow


def test_composition_seeds_recommendation_explanation_opaque():
    composition = SessionExperienceComposition(seed_demo_learners=True)
    composition.seed_learner("stu-mes-a", demo=True)
    today = composition.mission.get_todays_session("stu-mes-a") or {}
    session_id = str(today.get("session_id") or "sess-1")
    overview = composition.runtime.get_session_overview(
        "stu-mes-a", session_id=session_id
    )
    assert overview is not None
    assert overview.get("why_studying")
    expl = overview.get("recommendation_explanation")
    assert isinstance(expl, dict)
    assert expl.get("evidence_points") or expl.get("why_recommended") or expl.get(
        "expected_benefit"
    )


def test_open_session_hydrates_explanation_on_overview_snapshot():
    composition = SessionExperienceComposition(seed_demo_learners=True)
    composition.seed_learner("stu-mes-b", demo=True)
    svc = composition.build_service()
    today = composition.mission.get_todays_session("stu-mes-b") or {}
    session_id = str(today.get("session_id") or "sess-1")

    snap = svc.open_session("stu-mes-b", session_id=session_id)
    assert isinstance(snap, OverviewSnapshot)
    assert snap.why_studying
    assert snap.explanation is not None
    assert isinstance(snap.explanation, ExplanationSnapshot)
    assert snap.explanation.evidence_points or snap.explanation.why_recommended

    # Resume / re-open: second open still carries explanation from opaque.
    again = svc.open_session("stu-mes-b", session_id=session_id)
    assert again.explanation is not None
    assert again.explanation.evidence_points == snap.explanation.evidence_points


def test_overview_vm_and_study_session_page_carry_explanation(app, ctx):
    composition = SessionExperienceComposition(seed_demo_learners=True)
    composition.seed_learner("stu-mes-c", demo=True)
    svc = composition.build_service()
    today = composition.mission.get_todays_session("stu-mes-c") or {}
    session_id = str(today.get("session_id") or "sess-1")
    snap = svc.open_session("stu-mes-c", session_id=session_id)

    vm = overview_vm(snap)
    assert vm.explanation is not None
    assert vm.explanation.has_content

    ws = SessionWorkspace.create("sw-mes", "stu-mes-c", session_id)
    page = page_from_flow(
        SessionFlowSnapshot(
            workspace=ws,
            surface=SessionSurface.OVERVIEW.value,
            overview=snap,
            next_surface="activity",
        )
    )
    study = StudySessionService().build_page(page)
    assert study.explanation is not None
    assert study.explanation.has_content
    assert study.why_today  # L1 string still present alongside MES

def test_overview_explanation_none_without_adaptive_recommendation():
    composition = SessionExperienceComposition(seed_demo_learners=False)
    # No demo seed → no adaptive recommendation on empty store.
    svc = composition.build_service()
    composition.runtime.put_overview(
        "stu-empty",
        session_id="sess-empty",
        document={
            "objective": "Practice",
            "topics": ("Topic",),
            "mission_id": "m1",
            "why_studying": "Manual why only.",
            "activity_count": 1,
            "session_id": "sess-empty",
        },
    )
    snap = svc.open_session("stu-empty", session_id="sess-empty")
    assert snap.why_studying == "Manual why only."
    assert snap.explanation is None
    assert overview_vm(snap).explanation is None
