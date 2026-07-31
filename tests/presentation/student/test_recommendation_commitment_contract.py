"""EP-008.3A — Recommendation Commitment contract tests (CF-A0*)."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace

from flask import render_template

from app.application.student_experience.dto.commitment_reflection_snapshot import (
    CommitmentReflectionSnapshot,
)
from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.history_snapshot import HistorySnapshot
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.application.student_experience.dto.recommendation_commitment_snapshot import (
    RecommendationCommitmentSnapshot,
)
from app.application.student_experience.dto.recommendation_narrative_entry_snapshot import (  # noqa: E501
    RecommendationNarrativeEntrySnapshot,
)
from app.application.student_experience.recommendation_commitment import (
    CONTINUITY_COMMIT,
    CONTINUITY_DEFER,
    CONTINUITY_REFLECTION,
    FORBIDDEN_SHAME_SUBSTRINGS,
    WHAT_WAS_LEARNED_HUMBLE,
    RecommendationCommitmentService,
)
from app.application.student_experience.recommendation_trust import (
    TRUST_STATE_COMPLETE,
    TRUST_STATE_REFUSAL,
)
from app.presentation.student.view_models import history_vm, home_vm


def _schema_complete_explanation(**overrides) -> ExplanationSnapshot:
    data = dict(
        summary="Focus on cash flow statements next.",
        why_recommended=(
            "Your recent practice shows soft recall on cash flow statements."
        ),
        evidence_points=(
            "Two recent practice attempts scored below your topic average.",
            "Cash flow is on the near-term revision list.",
        ),
        expected_benefit="Strengthen exam readiness on cash flow analysis.",
        confidence_label="Suggested",
        suggested_next_action="Start a 25-minute cash flow practice session.",
        review_point="Reassess after tonight's practice set.",
        confidence_basis="Based on recent practice outcomes.",
        is_complete=True,
        plan_coherence="aligned",
        plan_coherence_label="Supports today's mission",
        honest_refusal=False,
        timeliness_line="High educational return before the exam window.",
        completion_loop_line="Reassess after tonight's practice set.",
    )
    data.update(overrides)
    return ExplanationSnapshot(**data)


def _commitment_home(**overrides) -> HomeSnapshot:
    commitment = RecommendationCommitmentSnapshot(
        state="offered",
        recommendation_key="Cash flow statements|2026-07-26",
        title="Cash flow statements",
        continuity_line=CONTINUITY_COMMIT,
        show_commit_affordance=True,
        show_defer_affordance=True,
    )
    kwargs = dict(
        student_id="stu-1",
        greeting="Welcome back",
        examination_label="ACCA AA",
        exam_countdown_days=30,
        exam_readiness=0.62,
        exam_readiness_label="Exam Readiness",
        recommendation_title="Cash flow statements",
        recommendation_summary="Focus on cash flow statements next.",
        estimated_study_minutes=25,
        explanation=_schema_complete_explanation(),
        start_session=StartSessionActionSnapshot(
            label="Start Session",
            enabled=True,
            can_start=True,
            mission_id="m-1",
        ),
        has_recommendation=True,
        can_start_session=True,
        trust_state=TRUST_STATE_COMPLETE,
        commitment=commitment,
    )
    kwargs.update(overrides)
    return HomeSnapshot(**kwargs)


def _render_home(app, page_home, *, form=None, defer_form=None, reflection_form=None):
    from app.presentation.student.services.student_home_service import (
        StudentHomeService,
    )
    from app.presentation.student.view_models import (
        StudentPageViewModel,
        StudentShellViewModel,
    )

    page = StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="home",
            active_label="Home",
            navigation=(),
            page_title="Home",
        ),
        home=page_home,
    )
    if form is None:
        form = SimpleNamespace(
            hidden_tag=lambda: "",
            mission_id=lambda: '<input type="hidden" name="mission_id">',
            session_id=lambda: '<input type="hidden" name="session_id">',
            recommendation_key=lambda: "",
            record_commitment=lambda: "",
        )
    with app.test_request_context("/student/"):
        home = StudentHomeService().build_home(page)
        return render_template(
            "student/home.html",
            page=page,
            home=home,
            form=form,
            defer_form=defer_form,
            reflection_form=reflection_form,
        )


def test_cf_a01_schema_complete_exposes_commitment_confirm(app, ctx):
    """CF-A01 / SOP-001: Home is a command centre — no commitment chrome wall.

    Commitment confirm remains an application preference path; Home keeps a
    single Mission Primary (DX-005A / SOP-001).
    """
    page_home = home_vm(_commitment_home(), unified_journey=False)
    html = _render_home(app, page_home)
    assert 'data-commitment="confirm"' not in html
    assert "ds-os-home" in html
    assert html.count('data-student-cta="primary"') <= 1


def test_cf_a02_refusal_hides_commitment_and_defer(app, ctx):
    """CF-A02: refusal fixture → no commitment / defer controls on Home."""
    explanation = _schema_complete_explanation(
        honest_refusal=True,
        why_recommended="Not enough personal study evidence yet.",
        confidence_label="Cannot yet be estimated",
        plan_coherence="deferred",
        plan_coherence_label="No recommendation yet",
        timeliness_line="",
    )
    commitment = RecommendationCommitmentSnapshot(
        state="refusal",
        title="No recommendation yet",
        show_commit_affordance=False,
        show_defer_affordance=False,
    )
    snap = _commitment_home(
        recommendation_title="No recommendation yet",
        explanation=explanation,
        trust_state=TRUST_STATE_REFUSAL,
        commitment=commitment,
    )
    page_home = home_vm(snap, unified_journey=False)
    html = _render_home(app, page_home)
    assert 'data-commitment="confirm"' not in html
    assert 'data-commitment="defer-open"' not in html
    assert "ds-os-home" in html


def test_cf_a03_defer_persists_student_safe_label(ctx, user):
    """CF-A03: defer POST with catalogue code persists deferred state + label."""
    tip = {
        "title": "Cash flow statements",
        "category": "Revision",
        "priority": "High",
        "reason": "Why",
        "expected_benefit": "Benefit",
        "generated_at": datetime(2026, 7, 26, 10, 0, 0),
    }
    snap = RecommendationCommitmentService.defer_commitment(
        user.id, tip, reason_code="need_prerequisite"
    )
    assert snap.state == "deferred"
    assert snap.deferred_reason_label == "Need a prerequisite first"
    assert snap.deferred_reason_code == "need_prerequisite"
    assert "need_prerequisite" not in (snap.deferred_reason_label or "")


def test_cf_a04_forbidden_shame_strings_absent(app, ctx):
    """CF-A04: forbidden shame/streak strings absent from defer/reflection."""
    reflection = CommitmentReflectionSnapshot(
        what_you_did="Completed: Cash flow",
        what_changed="Reassess after tonight.",
        why_it_mattered="Strengthen readiness.",
        what_was_learned=WHAT_WAS_LEARNED_HUMBLE,
        what_happens_next="Return Home for the next Mission.",
    )
    commitment = RecommendationCommitmentSnapshot(
        state="completed",
        title="Cash flow statements",
        continuity_line=CONTINUITY_REFLECTION,
        reflection=reflection,
        show_commit_affordance=False,
        show_defer_affordance=False,
    )
    page_home = home_vm(_commitment_home(commitment=commitment), unified_journey=False)
    defer_form = SimpleNamespace(
        hidden_tag=lambda: "",
        recommendation_key=lambda: "",
        reason_code=SimpleNamespace(
            choices=[
                ("not_enough_time", "Not enough time"),
                ("not_today", "Not today"),
            ],
            data="not_today",
        ),
        reason_note=lambda **kwargs: '<input name="reason_note">',
    )
    offered = home_vm(_commitment_home(), unified_journey=False)
    html_offered = _render_home(app, offered, defer_form=defer_form)
    html_reflection = _render_home(app, page_home)
    combined = (html_offered + html_reflection).lower()
    # Scope to Home article — shell footer may contain class names like beta-badge.
    start = combined.find('class="ds-page')
    if start < 0:
        start = combined.find("ds-os-home")
    scoped = combined[start:] if start >= 0 else combined
    end = scoped.find("</article>")
    if end >= 0:
        scoped = scoped[: end + len("</article>")]
    for phrase in FORBIDDEN_SHAME_SUBSTRINGS:
        assert phrase.lower() not in scoped


def test_cf_a05_single_primary_start_session_cta(app, ctx):
    """CF-A05: DR-050 — single primary Start Session CTA."""
    page_home = home_vm(_commitment_home(), unified_journey=False)
    defer_form = SimpleNamespace(
        hidden_tag=lambda: "",
        recommendation_key=lambda: "",
        reason_code=SimpleNamespace(
            choices=[("not_today", "Not today")],
            data="not_today",
        ),
        reason_note=lambda **kwargs: "",
    )
    html = _render_home(app, page_home, defer_form=defer_form)
    assert html.count('data-student-cta="primary"') == 1


def test_cf_a06_reflection_binds_authored_humble_frames(app, ctx):
    """CF-A06 / SOP-001: reflection chrome is not hosted on Home."""
    reflection = CommitmentReflectionSnapshot(
        what_you_did="Completed: Cash flow statements",
        what_changed="Reassess after tonight's practice set.",
        why_it_mattered="Strengthen exam readiness on cash flow analysis.",
        what_was_learned=WHAT_WAS_LEARNED_HUMBLE,
        what_happens_next="Return Home for the next Mission.",
    )
    commitment = RecommendationCommitmentSnapshot(
        state="completed",
        title="Cash flow statements",
        continuity_line=CONTINUITY_REFLECTION,
        reflection=reflection,
    )
    page_home = home_vm(_commitment_home(commitment=commitment), unified_journey=False)
    reflection_form = SimpleNamespace(
        hidden_tag=lambda: "",
        recommendation_key=lambda: "",
    )
    html = _render_home(app, page_home, reflection_form=reflection_form)
    assert 'data-reflection-field="what_you_did"' not in html
    assert "twin" not in html.lower()
    assert "llm" not in html.lower()
    assert "pipeline" not in html.lower()
    assert "ds-os-home" in html


def test_cf_a07_history_narrative_completed_and_deferred(app, ctx):
    """CF-A07: History narrative includes completed + deferred; cap respected."""
    entries = tuple(
        RecommendationNarrativeEntrySnapshot(
            kind=kind,
            title=f"Title {i}",
            occurred_at="2026-07-26",
            summary_line=f"{kind.title()} · Title {i} · detail",
            reason_label="Not today" if kind == "deferred" else "",
        )
        for i, kind in enumerate(["completed", "deferred"] + ["completed"] * 8)
    )
    assert len(entries) == 10
    snap = HistorySnapshot(
        student_id="1",
        recommendation_narrative=entries,
        recommendation_narrative_header=("Choices you've made inside one study plan."),
    )
    page = history_vm(snap)
    assert len(page.recommendation_narrative) == 10
    kinds = {e.kind for e in page.recommendation_narrative}
    assert "completed" in kinds
    assert "deferred" in kinds
    page_ns = SimpleNamespace(
        history=page,
        shell=SimpleNamespace(
            active_surface="history",
            navigation=(),
            page_title="History",
            page_description="What have I accomplished?",
        ),
    )
    with app.test_request_context("/student/history"):
        html = render_template("student/history.html", page=page_ns)
    assert 'data-commitment="history"' in html
    assert "Recent study choices" in html
    assert "Deferred" in html or "deferred" in html.lower()


def test_cf_a08_continuity_on_commit_defer_reflection(app, ctx):
    """CF-A08 / SOP-001: continuity copy is not a Home chrome requirement."""
    html_commit = _render_home(app, home_vm(_commitment_home(), unified_journey=False))
    assert 'data-commitment="continuity"' not in html_commit
    assert "ds-os-home" in html_commit

    deferred = RecommendationCommitmentSnapshot(
        state="deferred",
        title="Cash flow statements",
        deferred_reason_label="Not today",
        continuity_line=CONTINUITY_DEFER,
    )
    html_defer = _render_home(
        app,
        home_vm(_commitment_home(commitment=deferred), unified_journey=False),
    )
    assert "ds-os-home" in html_defer

    reflection = CommitmentReflectionSnapshot(
        what_you_did="Done",
        what_changed="Changed",
        why_it_mattered="Mattered",
        what_was_learned=WHAT_WAS_LEARNED_HUMBLE,
        what_happens_next="Next",
    )
    completed = RecommendationCommitmentSnapshot(
        state="completed",
        title="Cash flow",
        continuity_line=CONTINUITY_REFLECTION,
        reflection=reflection,
    )
    html_ref = _render_home(
        app,
        home_vm(_commitment_home(commitment=completed), unified_journey=False),
    )
    assert "ds-os-home" in html_ref


def test_cf_a11_trust_bindings_still_present(app, ctx):
    """CF-A11 / SOP-001: MES trust wall is not reintroduced on Home."""
    html = _render_home(app, home_vm(_commitment_home(), unified_journey=False))
    assert 'data-mes-field="why_recommended"' not in html
    assert "ds-os-home" in html
    assert html.count("ds-btn--primary") <= 1


def test_cf_a12_terminology_guard_commitment_chrome(app, ctx):
    """CF-A12: no pipeline/warrant/Twin leakage in commitment chrome."""
    html = _render_home(app, home_vm(_commitment_home(), unified_journey=False)).lower()
    for term in (
        "pipeline",
        "warrant",
        "digital twin",
        "learning twin",
        "adaptive engine",
    ):
        assert term not in html
