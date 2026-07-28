"""HTTP routes for Adaptive Assessment Quick Check (ILE-001B).

Thin Flask layer: auth → experience service → templates.
No Twin updates, Reasoning, Mission planning, or Assessment Engine logic.
"""

from __future__ import annotations

import logging

from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.application.adaptive_assessment.localisation import resolve_copy
from app.application.adaptive_assessment.quick_check_experience import (
    QuickCheckExperienceError,
    QuickCheckPhase,
)
from app.presentation.adaptive_assessment import adaptive_assessment_bp
from app.presentation.adaptive_assessment.forms import (
    BeginQuickCheckForm,
    DeferQuickCheckForm,
    HintQuickCheckForm,
    PauseQuickCheckForm,
    ReflectQuickCheckForm,
    RespondQuickCheckForm,
    ResumeQuickCheckForm,
    ReturnToMissionForm,
    StartQuickCheckForm,
    WhyThisForm,
)
from app.presentation.adaptive_assessment.views import (
    apply_mission_return,
    page_for,
    remember_return,
    resolve_return_url,
    service,
    student_id,
)

logger = logging.getLogger(__name__)


def _phase_redirect(snapshot) -> str:
    phase = snapshot.phase
    eid = snapshot.experience_id
    mapping = {
        QuickCheckPhase.INTRODUCTION: "adaptive_assessment.introduction",
        QuickCheckPhase.QUESTION: "adaptive_assessment.question",
        QuickCheckPhase.REFLECTION: "adaptive_assessment.reflection",
        QuickCheckPhase.COMPLETION: "adaptive_assessment.completion",
        QuickCheckPhase.PAUSED: "adaptive_assessment.paused",
    }
    endpoint = mapping.get(phase)
    if endpoint and eid:
        return url_for(endpoint, experience_id=eid)
    return url_for("student.home")


def _load_or_404(experience_id: str):
    try:
        return service().snapshot(experience_id, student_id=student_id())
    except QuickCheckExperienceError as exc:
        msg = str(exc).lower()
        if "not owned" in msg:
            abort(403)
        abort(404)


@adaptive_assessment_bp.post("/quick-check/start")
@login_required
def start():
    """Mission entry Continue → introduction."""
    form = StartQuickCheckForm()
    if not form.validate_on_submit():
        flash(resolve_copy("empty.adaptive_assessment_unavailable"), "warning")
        return redirect(url_for("student.home"))
    remember_return(
        return_endpoint=form.return_endpoint.data or "",
        return_session_id=form.return_session_id.data or "",
    )
    try:
        snapshot = service().start(
            student_id=student_id(),
            mission_ref=form.mission_ref.data or "",
            subject_code=form.subject_code.data or "",
        )
    except QuickCheckExperienceError:
        logger.warning("Quick Check start failed", exc_info=True)
        flash(resolve_copy("empty.adaptive_assessment_unavailable"), "warning")
        return redirect(
            resolve_return_url(
                return_endpoint=form.return_endpoint.data or "",
                return_session_id=form.return_session_id.data or "",
                mission_ref=form.mission_ref.data or "",
            )
        )
    return redirect(_phase_redirect(snapshot))


@adaptive_assessment_bp.post("/quick-check/why")
@login_required
def why_this():
    """Emit AssessmentExplained and stay on / return to Mission card context."""
    form = WhyThisForm()
    if form.validate_on_submit():
        service().explain(
            student_id=student_id(),
            subject_code=form.subject_code.data or "",
            surface="why_this",
        )
    # Prefer staying on introduction when an experience exists.
    eid = (form.experience_id.data or "").strip()
    if eid:
        try:
            snapshot = service().snapshot(eid, student_id=student_id())
            return redirect(_phase_redirect(snapshot))
        except QuickCheckExperienceError:
            pass
    referrer = request.referrer
    if referrer and referrer.startswith(request.host_url):
        return redirect(referrer)
    return redirect(url_for("student.home"))


@adaptive_assessment_bp.post("/quick-check/defer")
@login_required
def defer():
    """Not now — dismiss and return to Mission."""
    form = DeferQuickCheckForm()
    if not form.validate_on_submit():
        return redirect(url_for("student.home"))
    remember_return(
        return_endpoint=form.return_endpoint.data or "",
        return_session_id=form.return_session_id.data or "",
    )
    eid = (form.experience_id.data or "").strip()
    try:
        if eid:
            ack = service().defer(eid, student_id=student_id())
        else:
            ack = service().defer_from_invitation(
                student_id=student_id(),
                mission_ref=form.mission_ref.data or "",
                subject_code=form.subject_code.data or "",
            )
    except QuickCheckExperienceError:
        ack = service().defer_from_invitation(
            student_id=student_id(),
            mission_ref=form.mission_ref.data or "",
            subject_code=form.subject_code.data or "",
        )
    apply_mission_return(ack)
    flash(ack.acknowledgement, "success")
    return redirect(
        resolve_return_url(
            return_endpoint=form.return_endpoint.data or "",
            return_session_id=form.return_session_id.data or "",
            mission_ref=form.mission_ref.data or "",
        )
    )


@adaptive_assessment_bp.get("/quick-check/<experience_id>/introduction")
@login_required
def introduction(experience_id: str):
    snapshot = _load_or_404(experience_id)
    if snapshot.phase != QuickCheckPhase.INTRODUCTION:
        return redirect(_phase_redirect(snapshot))
    page = page_for(snapshot)
    begin_form = BeginQuickCheckForm()
    begin_form.experience_id.data = experience_id
    begin_form.submit.label.text = resolve_copy("quick_check.intro.begin")
    defer_form = DeferQuickCheckForm()
    defer_form.experience_id.data = experience_id
    defer_form.mission_ref.data = snapshot.mission_ref
    defer_form.subject_code.data = snapshot.subject_code
    defer_form.return_endpoint.data = page.return_endpoint
    defer_form.return_session_id.data = page.return_session_id
    defer_form.submit.label.text = resolve_copy("action.defer")
    why_form = WhyThisForm()
    why_form.experience_id.data = experience_id
    why_form.subject_code.data = snapshot.subject_code
    why_form.submit.label.text = resolve_copy("quick_check.invitation.why_this")
    return render_template(
        "adaptive_assessment/introduction.html",
        title=page.page_title,
        page=page,
        begin_form=begin_form,
        defer_form=defer_form,
        why_form=why_form,
    )


@adaptive_assessment_bp.post("/quick-check/<experience_id>/begin")
@login_required
def begin(experience_id: str):
    form = BeginQuickCheckForm()
    if not form.validate_on_submit():
        return redirect(
            url_for(
                "adaptive_assessment.introduction",
                experience_id=experience_id,
            )
        )
    try:
        snapshot = service().begin_questions(
            experience_id, student_id=student_id()
        )
    except QuickCheckExperienceError as exc:
        if "not owned" in str(exc).lower():
            abort(403)
        abort(404)
    return redirect(_phase_redirect(snapshot))


@adaptive_assessment_bp.get("/quick-check/<experience_id>/question")
@login_required
def question(experience_id: str):
    snapshot = _load_or_404(experience_id)
    if snapshot.phase == QuickCheckPhase.PAUSED:
        return redirect(
            url_for("adaptive_assessment.paused", experience_id=experience_id)
        )
    if snapshot.phase != QuickCheckPhase.QUESTION or snapshot.question is None:
        return redirect(_phase_redirect(snapshot))
    page = page_for(snapshot)
    q = snapshot.question
    respond_form = RespondQuickCheckForm()
    respond_form.experience_id.data = experience_id
    respond_form.item_id.data = q.item_id
    respond_form.submit.label.text = q.next_label
    if q.response_kind == "choice" and q.choices:
        respond_form.choice.choices = [(c, c) for c in q.choices]
    hint_form = HintQuickCheckForm()
    hint_form.experience_id.data = experience_id
    hint_form.submit.label.text = q.hint_request_label
    pause_form = PauseQuickCheckForm()
    pause_form.experience_id.data = experience_id
    pause_form.submit.label.text = q.pause_label
    return render_template(
        "adaptive_assessment/question.html",
        title=page.page_title,
        page=page,
        respond_form=respond_form,
        hint_form=hint_form,
        pause_form=pause_form,
    )


@adaptive_assessment_bp.post("/quick-check/<experience_id>/respond")
@login_required
def respond(experience_id: str):
    form = RespondQuickCheckForm()
    snapshot = _load_or_404(experience_id)
    if snapshot.question and snapshot.question.response_kind == "choice":
        form.choice.choices = [
            (c, c) for c in snapshot.question.choices
        ]
    if not form.validate_on_submit():
        return redirect(
            url_for("adaptive_assessment.question", experience_id=experience_id)
        )
    response = (form.free_text.data or form.choice.data or "").strip()
    try:
        next_snap = service().submit_response(
            experience_id,
            student_id=student_id(),
            item_id=form.item_id.data or "",
            response=response,
        )
    except QuickCheckExperienceError as exc:
        if "not owned" in str(exc).lower():
            abort(403)
        flash(resolve_copy("empty.adaptive_assessment_unavailable"), "warning")
        return redirect(
            url_for("adaptive_assessment.question", experience_id=experience_id)
        )
    return redirect(_phase_redirect(next_snap))


@adaptive_assessment_bp.post("/quick-check/<experience_id>/hint")
@login_required
def hint(experience_id: str):
    form = HintQuickCheckForm()
    if not form.validate_on_submit():
        return redirect(
            url_for("adaptive_assessment.question", experience_id=experience_id)
        )
    try:
        service().show_hint(experience_id, student_id=student_id())
    except QuickCheckExperienceError as exc:
        if "not owned" in str(exc).lower():
            abort(403)
    return redirect(
        url_for("adaptive_assessment.question", experience_id=experience_id)
    )


@adaptive_assessment_bp.get("/quick-check/<experience_id>/reflection")
@login_required
def reflection(experience_id: str):
    snapshot = _load_or_404(experience_id)
    if snapshot.phase != QuickCheckPhase.REFLECTION:
        return redirect(_phase_redirect(snapshot))
    page = page_for(snapshot)
    reflect_form = ReflectQuickCheckForm()
    reflect_form.experience_id.data = experience_id
    reflect_form.submit.label.text = resolve_copy(
        "quick_check.reflection.continue"
    )
    pause_form = PauseQuickCheckForm()
    pause_form.experience_id.data = experience_id
    pause_form.submit.label.text = resolve_copy("action.pause")
    return render_template(
        "adaptive_assessment/reflection.html",
        title=page.page_title,
        page=page,
        reflect_form=reflect_form,
        pause_form=pause_form,
    )


@adaptive_assessment_bp.post("/quick-check/<experience_id>/reflect")
@login_required
def reflect(experience_id: str):
    form = ReflectQuickCheckForm()
    if not form.validate_on_submit():
        return redirect(
            url_for(
                "adaptive_assessment.reflection", experience_id=experience_id
            )
        )
    try:
        snapshot = service().submit_reflection(
            experience_id,
            student_id=student_id(),
            reflection=form.reflection.data or "",
        )
    except QuickCheckExperienceError as exc:
        if "not owned" in str(exc).lower():
            abort(403)
        abort(404)
    return redirect(_phase_redirect(snapshot))


@adaptive_assessment_bp.get("/quick-check/<experience_id>/completion")
@login_required
def completion(experience_id: str):
    snapshot = _load_or_404(experience_id)
    if snapshot.phase != QuickCheckPhase.COMPLETION:
        return redirect(_phase_redirect(snapshot))
    page = page_for(snapshot)
    return_form = ReturnToMissionForm()
    return_form.experience_id.data = experience_id
    return_form.return_endpoint.data = page.return_endpoint
    return_form.return_session_id.data = page.return_session_id
    return_form.submit.label.text = resolve_copy(
        "quick_check.completion.return"
    )
    return render_template(
        "adaptive_assessment/completion.html",
        title=page.page_title,
        page=page,
        return_form=return_form,
    )


@adaptive_assessment_bp.post("/quick-check/<experience_id>/return")
@login_required
def return_to_mission(experience_id: str):
    form = ReturnToMissionForm()
    if not form.validate_on_submit():
        return redirect(
            url_for(
                "adaptive_assessment.completion", experience_id=experience_id
            )
        )
    try:
        ack = service().complete_return(
            experience_id, student_id=student_id()
        )
        snapshot = service().snapshot(
            experience_id, student_id=student_id()
        )
    except QuickCheckExperienceError as exc:
        if "not owned" in str(exc).lower():
            abort(403)
        abort(404)
    apply_mission_return(ack)
    flash(ack.acknowledgement, "success")
    return redirect(
        resolve_return_url(
            return_endpoint=form.return_endpoint.data or "",
            return_session_id=form.return_session_id.data or "",
            mission_ref=snapshot.mission_ref,
        )
    )


@adaptive_assessment_bp.post("/quick-check/<experience_id>/pause")
@login_required
def pause(experience_id: str):
    form = PauseQuickCheckForm()
    if not form.validate_on_submit():
        return redirect(_phase_redirect(_load_or_404(experience_id)))
    try:
        snapshot = service().pause(experience_id, student_id=student_id())
    except QuickCheckExperienceError as exc:
        if "not owned" in str(exc).lower():
            abort(403)
        abort(404)
    return redirect(_phase_redirect(snapshot))


@adaptive_assessment_bp.get("/quick-check/<experience_id>/paused")
@login_required
def paused(experience_id: str):
    snapshot = _load_or_404(experience_id)
    if snapshot.phase != QuickCheckPhase.PAUSED:
        return redirect(_phase_redirect(snapshot))
    page = page_for(snapshot)
    resume_form = ResumeQuickCheckForm()
    resume_form.experience_id.data = experience_id
    resume_form.submit.label.text = resolve_copy("quick_check.action.resume")
    defer_form = DeferQuickCheckForm()
    defer_form.experience_id.data = experience_id
    defer_form.mission_ref.data = snapshot.mission_ref
    defer_form.subject_code.data = snapshot.subject_code
    defer_form.return_endpoint.data = page.return_endpoint
    defer_form.return_session_id.data = page.return_session_id
    defer_form.submit.label.text = resolve_copy("action.defer")
    return render_template(
        "adaptive_assessment/paused.html",
        title=page.page_title,
        page=page,
        resume_form=resume_form,
        defer_form=defer_form,
    )


@adaptive_assessment_bp.post("/quick-check/<experience_id>/resume")
@login_required
def resume(experience_id: str):
    form = ResumeQuickCheckForm()
    if not form.validate_on_submit():
        return redirect(
            url_for("adaptive_assessment.paused", experience_id=experience_id)
        )
    try:
        snapshot = service().resume(experience_id, student_id=student_id())
    except QuickCheckExperienceError as exc:
        if "not owned" in str(exc).lower():
            abort(403)
        abort(404)
    return redirect(_phase_redirect(snapshot))
