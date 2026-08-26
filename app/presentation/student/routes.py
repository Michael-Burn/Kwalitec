"""HTTP routes for the Student Experience UI.

Thin Flask layer: auth → views → templates.
Educational authority stays in Student Experience application services.
"""

from __future__ import annotations

import logging

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.application.educational_runtime_engine import (
    EducationalPrerequisiteMissing,
)
from app.application.student_experience.exceptions import (
    PortUnavailable,
    StudentExperienceError,
)
from app.application.student_experience.recommendation_commitment import (
    RecommendationCommitmentService,
)
from app.domain.student_experience.experience_workspace import ExperienceSurface
from app.presentation.student import student_bp
from app.presentation.student.factory import get_experience_composition
from app.presentation.student.forms import (
    BeginRevisionForm,
    CompleteRuntimeMissionForm,
    DeferCommitmentForm,
    ExplainMissionTutorForm,
    ReflectionAckForm,
    StartSessionForm,
)
from app.presentation.student.views import load_page, start_todays_session

logger = logging.getLogger(__name__)


def _baseline_gate_redirect():
    """If an active plan lacks a complete Baseline, send the student there."""
    from app.application.student_baseline import StudentBaselineService
    from app.services.study_plan_service import StudyPlanService

    plan = StudyPlanService.get_user_active_plan(current_user.id)
    if plan is None:
        return None
    parts = (plan.exam_name or "").split(" ", 1)
    if len(parts) != 2:
        return None
    subject_key = StudentBaselineService.subject_key(parts[0], parts[1])
    complete = StudentBaselineService.get_complete(current_user.id, subject_key)
    if complete is not None:
        return None
    return redirect(
        url_for("student_baseline.for_plan", study_plan_id=plan.id)
    )


def _current_tip_payload() -> dict:
    """Read today's tip projection for commitment recording (pass-through)."""
    from app.presentation.student.factory import get_experience_service

    try:
        dash = get_experience_service().get_dashboard(
            str(current_user.id),
            surface="home",
            include_all_surfaces=False,
        )
        home = getattr(dash, "home", None)
        if home is None:
            return {}
        tip: dict = {
            "title": home.recommendation_title or "",
            "topic_title": home.recommendation_title or "",
            "summary": home.recommendation_summary or "",
            "category": "Study",
            "priority": "Medium",
            "reason": "",
            "why_recommended": "",
            "expected_benefit": "",
            "review_point": "",
            "suggested_next_action": "",
            "generated_at": home.recommendation_title or "",
        }
        expl = home.explanation
        if expl is not None:
            tip["reason"] = expl.timeliness_line or expl.why_recommended or ""
            tip["why_recommended"] = expl.why_recommended or ""
            tip["expected_benefit"] = expl.expected_benefit or ""
            tip["review_point"] = expl.review_point or ""
            tip["suggested_next_action"] = expl.suggested_next_action or ""
        commitment = getattr(home, "commitment", None)
        key = getattr(commitment, "recommendation_key", "") or ""
        if "|" in key:
            tip["generated_at"] = key.split("|", 1)[1]
        return tip
    except Exception:  # noqa: BLE001 — fail-open for preference path
        logger.warning("commitment_tip_payload_failed", exc_info=True)
        return {}


@student_bp.get("/")
@login_required
def home():
    """Student Home — what should I study next? (DX-005A Daily Mission)."""
    from app.presentation.student.services.student_home_service import (
        StudentHomeService,
    )
    from app.services.alpha_onboarding_service import AlphaOnboardingService
    from app.services.presentation_telemetry_service import (
        EVENT_DASHBOARD_OPENED,
        PresentationTelemetryService,
    )

    # B8 (PX-003): Student Home is the canonical post-login landing surface
    # under SOLE_RUNTIME — mirror the same first-time onboarding gate
    # `dashboard.index` already applies, so onboarding is guaranteed exactly
    # once regardless of which home a student's flag configuration resolves
    # to (see app/presentation/consolidation.py).
    if AlphaOnboardingService.should_show(current_user):
        return redirect(url_for("alpha.onboarding"))

    # SB-001A: active Study Plan without Baseline redirects to Baseline.
    baseline_gate = _baseline_gate_redirect()
    if baseline_gate is not None:
        return baseline_gate

    page = load_page(ExperienceSurface.HOME)
    PresentationTelemetryService.record(
        EVENT_DASHBOARD_OPENED,
        user_id=current_user.id,
        path="/student/",
        context={"surface": "home", "workspace": "adaptive-study"},
    )
    from app.services.presentation_telemetry_service import (
        EVENT_WORKSPACE_OPENED,
    )

    PresentationTelemetryService.record(
        EVENT_WORKSPACE_OPENED,
        user_id=current_user.id,
        path="/student/",
        context={"surface": "adaptive-study-workspace"},
    )
    form = StartSessionForm()
    complete_form = CompleteRuntimeMissionForm()
    if page.home:
        form.mission_id.data = page.home.mission_id
        form.session_id.data = page.home.session_id
        complete_form.mission_id.data = page.home.mission_id
        if page.home.commitment:
            form.recommendation_key.data = (
                page.home.commitment.recommendation_key or ""
            )
    # RR-001.1 / JR-07: syllabus-complete revision acknowledgement remains
    # reachable as the L0 Primary (Continue) under DX-005A.
    from app.services.learning_lifecycle_service import LearningLifecycleService

    lifecycle = LearningLifecycleService.resolve(current_user.id)
    home = StudentHomeService().build_home(
        page,
        show_revision_acknowledgement=lifecycle.show_completion_acknowledgement,
        revision_ack_title=getattr(lifecycle, "acknowledgement_title", "") or "",
        revision_ack_body=getattr(lifecycle, "acknowledgement_body", "") or "",
    )
    return render_template(
        "student/home.html",
        title=home.page_title,
        page=page,
        home=home,
        form=form,
        complete_form=complete_form,
    )


@student_bp.get("/tutor")
@login_required
def tutor():
    """UX-001 — Student Tutor surface (explainability, not new reasoning)."""
    from app.presentation.student.services.student_tutor_presentation_service import (
        StudentTutorPresentationService,
    )
    from app.services.presentation_telemetry_service import (
        EVENT_TUTOR_OPENED,
        PresentationTelemetryService,
    )

    page = load_page(ExperienceSurface.HOME)
    PresentationTelemetryService.record(
        EVENT_TUTOR_OPENED,
        user_id=current_user.id,
        path="/student/tutor",
        context={"surface": "tutor"},
    )
    tutor_page = StudentTutorPresentationService().build(page)
    return render_template(
        "student/tutor.html",
        title=tutor_page.page_title,
        page=page,
        tutor=tutor_page,
    )


@student_bp.post("/tutor/explain-mission")
@login_required
def tutor_explain_mission():
    """TUTOR-001 — evidence-backed explanation of today's mission.

    Explains Adaptive Mission / Twin decisions. Does not invent educational
    reasoning. Soft-fails when no Twin is available for the learner.
    """
    form = ExplainMissionTutorForm()
    if not form.validate_on_submit():
        flash("Please try explaining today's mission again.", "warning")
        return redirect(url_for("student.tutor"))

    from app.application.intelligent_tutor.intelligent_tutor_service import (
        IntelligentTutorService,
    )
    from app.application.student_digital_twin.student_digital_twin_service import (
        StudentDigitalTwinService,
    )
    from app.presentation.student.services.student_tutor_presentation_service import (
        StudentTutorPresentationService,
        TutorCitation,
    )

    page = load_page(ExperienceSurface.HOME)
    twins = StudentDigitalTwinService().list_twins_for_student(str(current_user.id))
    if not twins:
        tutor_page = StudentTutorPresentationService().build(
            page,
            error_message=(
                "Tutor guidance will appear once Learning Insights are available "
                "from your practice."
            ),
        )
        return render_template(
            "student/tutor.html",
            title=tutor_page.page_title,
            page=page,
            tutor=tutor_page,
        ), 200

    try:
        response = IntelligentTutorService().explain_mission(
            twins[0].twin_id,
            persist=True,
            enrich_evidence=True,
        )
    except ValueError as exc:
        logger.warning("tutor_explain_mission_failed: %s", exc)
        tutor_page = StudentTutorPresentationService().build(
            page,
            error_message=(
                "The Tutor could not explain today's mission just now. "
                "Please try again shortly."
            ),
        )
        return render_template(
            "student/tutor.html",
            title=tutor_page.page_title,
            page=page,
            tutor=tutor_page,
        ), 200

    citations: list[TutorCitation] = []
    explanation = response.explanation
    for point in getattr(explanation, "evidence_points", ()) or ():
        text = str(point).strip()
        if text:
            citations.append(TutorCitation(label=text[:160]))
    source = ""
    for attr in ("curriculum_source", "source_label", "authority_label"):
        raw = getattr(explanation, attr, None)
        if isinstance(raw, str) and raw.strip():
            source = raw.strip()
            break

    tutor_page = StudentTutorPresentationService().build(
        page,
        explanation_summary=getattr(explanation, "summary", "") or "",
        suggested_next_action=response.suggested_next_action or "",
        citations=tuple(citations[:8]),
        certified_source=source,
    )
    from app.services.presentation_telemetry_service import (
        EVENT_TUTOR_QUESTION,
        PresentationTelemetryService,
    )

    PresentationTelemetryService.record(
        EVENT_TUTOR_QUESTION,
        user_id=current_user.id,
        path="/student/tutor",
        context={"surface": "tutor", "action": "explain_mission"},
    )
    return render_template(
        "student/tutor.html",
        title=tutor_page.page_title,
        page=page,
        tutor=tutor_page,
    )


@student_bp.get("/knowledge-graph")
@login_required
def knowledge_graph():
    """UX-001 — first student-facing Knowledge Map (certified hierarchy)."""
    from app.presentation.student.services import (
        student_knowledge_graph_presentation_service as kg_svc,
    )

    page = load_page(ExperienceSurface.HOME)
    subject_code = ""
    examination_label = ""
    current_topic_id = ""
    completed: tuple[str, ...] = ()
    if page.home:
        examination_label = (page.home.examination_label or "").strip()
        edu = page.home.educational
        if edu and getattr(edu, "active", False):
            subject_code = (edu.subject_code or "").strip()
            examination_label = examination_label or (
                edu.examination_label or ""
            ).strip()
            current_topic_id = (edu.today_topic_code or "").strip()
    if page.journey:
        examination_label = examination_label or (
            page.journey.examination_label or ""
        ).strip()
        if page.journey.current:
            current_topic_id = current_topic_id or (
                page.journey.current.topic_id or ""
            ).strip()
        completed = tuple(
            (t.topic_id or "").strip()
            for t in (page.journey.completed or ())
            if (t.topic_id or "").strip()
        )

    graph = kg_svc.StudentKnowledgeGraphPresentationService().build(
        subject_code=subject_code,
        examination_label=examination_label,
        current_topic_id=current_topic_id,
        completed_topic_ids=completed,
    )
    from app.services.presentation_telemetry_service import (
        EVENT_KNOWLEDGE_MAP_OPENED,
        PresentationTelemetryService,
    )

    PresentationTelemetryService.record(
        EVENT_KNOWLEDGE_MAP_OPENED,
        user_id=current_user.id,
        path="/student/knowledge-graph",
        context={"surface": "knowledge_map", "subject": subject_code or ""},
    )
    return render_template(
        "student/knowledge_graph.html",
        title=graph.page_title,
        page=page,
        graph=graph,
    )


@student_bp.get("/journey")
@login_required
def journey():
    """Journey — topic progress toward exam readiness."""
    from app.services.presentation_telemetry_service import (
        EVENT_JOURNEY_OPENED,
        PresentationTelemetryService,
    )

    page = load_page(ExperienceSurface.JOURNEY)
    PresentationTelemetryService.record(
        EVENT_JOURNEY_OPENED,
        user_id=current_user.id,
        path="/student/journey",
        context={"surface": "journey"},
    )
    return render_template(
        "student/journey.html",
        title=page.shell.page_title,
        page=page,
    )


@student_bp.get("/revision")
@login_required
def revision():
    """Revision — highest-value revision from Adaptive Decision."""
    page = load_page(ExperienceSurface.REVISION)
    form = BeginRevisionForm()
    if page.revision and page.revision.primary:
        form.option_id.data = page.revision.primary.option_id
    return render_template(
        "student/revision.html",
        title=page.shell.page_title,
        page=page,
        form=form,
    )


@student_bp.get("/history")
@login_required
def history():
    """History — educational progress, not activity logs."""
    page = load_page(ExperienceSurface.HISTORY)
    return render_template(
        "student/history.html",
        title=page.shell.page_title,
        page=page,
    )


@student_bp.get("/decision-journal")
@login_required
def decision_journal():
    """ILE-002 — Decision Journal timeline (educational memory)."""
    from app.application.decision_journal import (
        DecisionJournalApplicationService,
    )
    from app.application.educational_feedback_loop import (
        EducationalFeedbackLoopApplicationService,
    )
    from app.presentation.student.forms import EducationalReflectionForm
    from app.presentation.student.view_models import (
        decision_journal_page_vm,
    )

    timeline = DecisionJournalApplicationService.timeline(
        int(current_user.id)
    )
    page = decision_journal_page_vm(timeline)
    reflection_forms: dict[str, EducationalReflectionForm] = {}
    reflection_intros: dict[str, str] = {}
    for entry in timeline.entries:
        if not entry.can_reflect:
            continue
        invite = EducationalFeedbackLoopApplicationService.reflection_invite(
            int(current_user.id),
            entry.decision_id,
        )
        if not invite.available:
            continue
        form = EducationalReflectionForm(prefix=entry.decision_id)
        form.entry_id.data = entry.decision_id
        reflection_forms[entry.decision_id] = form
        reflection_intros[entry.decision_id] = invite.intro_line
    return render_template(
        "student/decision_journal.html",
        title=page.shell.page_title,
        page=page,
        journal=timeline,
        reflection_forms=reflection_forms,
        reflection_intros=reflection_intros,
    )


@student_bp.post("/decision-journal/<entry_id>/reflect")
@login_required
def decision_journal_reflect(entry_id: str):
    """ILE-005 — optional educational reflection on a journal recommendation."""
    from app.application.educational_feedback_loop import (
        EducationalFeedbackLoopApplicationService,
    )
    from app.presentation.student.forms import EducationalReflectionForm
    from app.services.educational_feedback_loop_service import (
        EducationalFeedbackLoopError,
    )

    form = EducationalReflectionForm(prefix=entry_id)
    if not form.validate_on_submit():
        flash(
            "We couldn't save that reflection. Please try again from the journal.",
            "warning",
        )
        return redirect(url_for("student.decision_journal"))

    form_entry = (form.entry_id.data or entry_id or "").strip()
    if form_entry != entry_id:
        flash(
            "That reflection did not match the journal entry.",
            "warning",
        )
        return redirect(url_for("student.decision_journal"))

    try:
        EducationalFeedbackLoopApplicationService.capture_reflection(
            int(current_user.id),
            entry_id,
            helped=form.helped.data or "",
            timing=form.timing.data or "",
            understood_why=form.understood_why.data or "",
            same_decision=form.same_decision.data or "",
            free_text=form.free_text.data or "",
        )
        flash(
            "Reflection saved. Thank you. This helps us improve how we "
            "guide your study.",
            "success",
        )
    except EducationalFeedbackLoopError:
        flash(
            "That journal entry can't accept reflection right now.",
            "warning",
        )
    except Exception:  # noqa: BLE001 — fail open to journal
        logger.exception(
            "decision_journal_reflect_failed entry_id=%s", entry_id
        )
        flash(
            "We couldn't save that reflection just now. Please try again shortly.",
            "warning",
        )
    return redirect(url_for("student.decision_journal"))


@student_bp.get("/educational-timeline")
@login_required
def educational_timeline():
    """ILE-003 — Educational Timeline (reflective narrative over journal)."""
    from app.application.educational_timeline import (
        EducationalTimelineApplicationService,
    )
    from app.presentation.student.view_models import (
        educational_timeline_page_vm,
    )

    timeline = EducationalTimelineApplicationService.timeline(
        int(current_user.id)
    )
    page = educational_timeline_page_vm(timeline)
    return render_template(
        "student/educational_timeline.html",
        title=page.shell.page_title,
        page=page,
        timeline=timeline,
    )


@student_bp.get("/learning-journey")
@login_required
def learning_journey():
    """KWP-011 / KWP-012 — My Learning Journey + Readiness Forecast."""
    from app.application.educational_memory import get_educational_memory_service
    from app.application.readiness_forecast import get_readiness_forecast_engine
    from app.domain.student_experience.experience_workspace import (
        ExperienceSurface,
    )
    from app.presentation.session.factory import get_session_experience_composition
    from app.presentation.student.view_models import (
        StudentPageViewModel,
        learning_journey_vm,
        shell_vm,
    )
    from app.services.presentation_telemetry_service import (
        EVENT_FORECAST_VIEWED,
        EVENT_LEARNING_JOURNEY_OPENED,
        PresentationTelemetryService,
    )

    composition = get_session_experience_composition()
    store = getattr(composition, "store", None) if composition else None
    student_key = str(current_user.id)
    narrative = get_educational_memory_service().journey_for_student(
        store=store,
        student_id=student_key,
    )
    days_to_exam = None
    readiness_ratio = None
    try:
        # Prefer countdown / readiness already projected on Home when available.
        page_probe = load_page(ExperienceSurface.HOME)
        if page_probe and page_probe.home and page_probe.home.countdown:
            days_to_exam = page_probe.home.countdown.days
        if page_probe and page_probe.home and page_probe.home.readiness:
            raw = page_probe.home.readiness.readiness_percent_label or ""
            digits = "".join(ch for ch in raw if ch.isdigit() or ch == ".")
            if digits:
                readiness_ratio = float(digits)
                if readiness_ratio > 1.0:
                    readiness_ratio = readiness_ratio / 100.0
    except Exception:  # noqa: BLE001
        days_to_exam = None
        readiness_ratio = None

    forecast = get_readiness_forecast_engine().forecast_from_store(
        store,
        student_id=student_key,
        days_to_exam=days_to_exam,
        current_readiness_ratio=readiness_ratio,
    )
    journey = learning_journey_vm(narrative, forecast=forecast)
    # V1S-007 DF-015: shell_vm is keyword-only (active_surface / page_title).
    page = StudentPageViewModel(
        shell=shell_vm(
            active_surface=ExperienceSurface.HISTORY.value,
            page_title="My Learning Journey",
            page_description="Your learning story and readiness outlook.",
        ),
        history=None,
    )
    PresentationTelemetryService.record(
        EVENT_LEARNING_JOURNEY_OPENED,
        user_id=current_user.id,
        path="/student/learning-journey",
        context={"surface": "learning-journey"},
    )
    if getattr(journey, "has_forecast", False) or getattr(
        journey, "forecast_guidance", ""
    ):
        PresentationTelemetryService.record(
            EVENT_FORECAST_VIEWED,
            user_id=current_user.id,
            path="/student/learning-journey",
            context={"surface": "readiness-forecast"},
        )
    return render_template(
        "student/learning_journey.html",
        title="My Learning Journey",
        page=page,
        journey=journey,
    )


@student_bp.get("/profile")
@login_required
def profile():
    """Profile — examination, preferences, goals, settings."""
    page = load_page(ExperienceSurface.PROFILE)
    return render_template(
        "student/profile.html",
        title=page.shell.page_title,
        page=page,
    )


@student_bp.post("/mission/complete")
@login_required
def complete_runtime_mission():
    """PR-001B — complete today's Runtime C mission from Home.

    SR-002: retained only for rollback (SR_SESSION_PRIMARY OFF) or emergency
    pilot (SR_PILOT_MARK_COMPLETE ON). Never the default product Primary when
    session spine is enabled. Does not start Guided Session.
    """
    from app.application.config.v2_flags import resolve_v2_feature_flags

    flags = resolve_v2_feature_flags()
    if flags.SR_SESSION_PRIMARY and not flags.SR_PILOT_MARK_COMPLETE:
        flash(
            "Today's learning starts with a Session. "
            "Use Start Today's Session from Home.",
            "info",
        )
        return redirect(url_for("student.home"))
    if flags.SR_EVIDENCE_GATE:
        flash(
            "Completing today's focus requires a Session with accepted practice. "
            "Start or resume Today's Session from Home.",
            "info",
        )
        return redirect(url_for("student.home"))

    form = CompleteRuntimeMissionForm()
    if not form.validate_on_submit():
        flash(
            "We couldn't mark that mission complete. Please try again from Home.",
            "warning",
        )
        return redirect(url_for("student.home"))

    mission_id = (form.mission_id.data or "").strip()
    if not mission_id:
        flash(
            "Today's mission was not available to complete. "
            "Refresh Home and try again.",
            "warning",
        )
        return redirect(url_for("student.home"))

    from app.application.educational_experience import (
        EducationalExperienceService,
    )
    from app.application.educational_runtime_engine.exceptions import (
        IllegalRuntimeState,
        MissionAlreadyCompleted,
        MissionInstanceNotFound,
    )

    try:
        snap = EducationalExperienceService().complete_mission(
            user_id=current_user.id,
            mission_instance_id=mission_id,
        )
    except MissionAlreadyCompleted:
        flash(
            "That mission is already complete. Your progress is saved. "
            "return tomorrow for the next topic, or open Journey to review.",
            "info",
        )
        return redirect(url_for("student.home"))
    except MissionInstanceNotFound:
        flash(
            "We could not find that mission. Refresh Home and try again.",
            "warning",
        )
        return redirect(url_for("student.home"))
    except IllegalRuntimeState as exc:
        logger.warning("runtime_c_mission_complete_illegal: %s", exc)
        flash(
            "That mission cannot be completed right now. "
            "Refresh Home, or open Journey to see your place in the syllabus.",
            "warning",
        )
        return redirect(url_for("student.home"))
    except Exception:  # noqa: BLE001 — fail closed with recovery copy
        logger.exception("runtime_c_mission_complete_failed")
        flash(
            "We could not save mission completion just now. Please try again shortly.",
            "warning",
        )
        return redirect(url_for("student.home"))

    topic = ""
    if snap is not None and snap.mission is not None:
        topic = snap.mission.topic_title or snap.mission.title
    # ILE-004 — mirror completion into Decision Journal (fail-open).
    try:
        from app.services.daily_mission_intelligence_service import (
            DailyMissionIntelligenceService,
        )

        tip = _current_tip_payload()
        title = tip.get("title") or topic or "Today's Mission"
        brief = DailyMissionIntelligenceService.compose_from_home_fields(
            title=title,
            summary=tip.get("summary") or "",
            why_recommended=tip.get("why_recommended")
            or tip.get("reason")
            or "",
            expected_benefit=tip.get("expected_benefit") or "",
            supporting_evidence=(
                (tip.get("supporting_evidence"),)
                if tip.get("supporting_evidence")
                else ()
            ),
            uncertainty=tip.get("uncertainty") or "",
            mission_id=mission_id,
        )
        entry = DailyMissionIntelligenceService.record_completion(
            current_user.id,
            brief,
            tip=tip if tip.get("title") else None,
            outcome_summary=(
                f"Mission completed: {topic}" if topic else "Mission completed"
            ),
        )
        # ILE-005 — educational review of the completed recommendation (fail-open).
        if entry is not None:
            try:
                from app.services.educational_feedback_loop_service import (
                    EducationalFeedbackLoopService,
                )

                EducationalFeedbackLoopService.review_after_outcome(
                    int(current_user.id),
                    entry.entry_id,
                )
            except Exception:  # noqa: BLE001 — feedback loop must not block
                logger.exception("feedback_loop_after_mission_failed")
    except Exception:  # noqa: BLE001 — journal mirror must not block completion
        logger.exception("daily_mission_complete_journal_mirror_failed")

    if topic:
        flash(
            f"Mission complete: {topic}. Your journey progress is updated.",
            "success",
        )
    else:
        flash("Mission complete. Your journey progress is updated.", "success")
    return redirect(url_for("student.home"))


@student_bp.post("/session/start")
@login_required
def start_session():
    """Primary Home CTA — start Today's Session via Experience.

    EP-008.3 Pattern A: also records conscious commitment (preference only).
    """
    form = StartSessionForm()
    if not form.validate_on_submit():
        flash(
            "We couldn't start today's session. Please try again.",
            "warning",
        )
        return redirect(url_for("student.home"))
    mission_id = (form.mission_id.data or "").strip() or None
    session_id = (form.session_id.data or "").strip() or None
    tip = _current_tip_payload()
    try:
        from app.application.student_runtime.exceptions import (
            MissionNotAcceptable,
            SessionSpineUnavailable,
            StudentRuntimeError,
        )

        # Record commitment before / with start (Pattern A).
        if (form.record_commitment.data or "1") != "0" and tip.get("title"):
            RecommendationCommitmentService.confirm_commitment(
                current_user.id,
                tip,
                session_id=session_id,
            )
        handle = start_todays_session(
            mission_id=mission_id, session_id=session_id
        )
        RecommendationCommitmentService.mark_session_started(
            current_user.id,
            tip=tip,
            session_id=handle.session_id or session_id,
        )
    except EducationalPrerequisiteMissing as exc:
        logger.warning(
            "Start session educational readiness: %s missing=%s",
            exc,
            getattr(exc, "missing_prerequisite", None),
        )
        flash(
            "Your curriculum is not ready for study yet. Return to Home "
            "when your subjects are available.",
            "warning",
        )
        return redirect(url_for("student.home"))
    except PortUnavailable:
        flash(
            "Today's Session is temporarily unavailable. Please try again shortly.",
            "warning",
        )
        return redirect(url_for("student.home"))
    except (
        StudentExperienceError,
        MissionNotAcceptable,
        SessionSpineUnavailable,
        StudentRuntimeError,
    ) as exc:
        logger.warning("Start session failed: %s", exc)
        msg = str(exc).lower()
        if "certified cmp" in msg or "guidance" in msg:
            flash(
                "This topic does not yet have certified CMP guidance. "
                "No session was started. Continue with your CMP for "
                "unpublished material. Your progress is saved.",
                "warning",
            )
        else:
            flash(
                "We couldn't start Today's Session. Please try again from Home.",
                "warning",
            )
        return redirect(url_for("student.home"))

    from app.services.presentation_telemetry_service import (
        EVENT_MISSION_STARTED,
        PresentationTelemetryService,
    )

    PresentationTelemetryService.record(
        EVENT_MISSION_STARTED,
        user_id=current_user.id,
        resource_type="session",
        resource_id=handle.session_id or session_id,
        path="/student/session/start",
        context={"mission_id": mission_id or ""},
    )

    topic = handle.topic_title or "your topic"
    # UX-001: Home decides; Session Overview briefs. Begin Session starts practice.
    target_session_id = handle.session_id or session_id
    if target_session_id:
        flash(
            f"Session ready. {topic}. Review today's objective, then begin.",
            "success",
        )
        return redirect(
            url_for("session.overview", session_id=target_session_id)
        )
    flash(
        f"Session started. {topic}. Continue from Home when you're ready.",
        "success",
    )
    return redirect(url_for("student.home"))


@student_bp.post("/commitment/defer")
@login_required
def defer_commitment():
    """Honest deferral — catalogue reason; no ranking change.

    SR-002a: when Session Primary is ON and a Runtime C mission is present,
    also mark the mission Deferred (ILE-004) without starting a session.
    """
    form = DeferCommitmentForm()
    if not form.validate_on_submit():
        flash("We couldn't save that just now. Please try again.", "warning")
        return redirect(url_for("student.home"))
    tip = _current_tip_payload()
    RecommendationCommitmentService.defer_commitment(
        current_user.id,
        tip,
        reason_code=form.reason_code.data or "not_today",
        reason_note=form.reason_note.data or "",
    )
    try:
        from app.application.config.v2_flags import resolve_v2_feature_flags
        from app.application.educational_experience import (
            EducationalExperienceService,
        )
        from app.application.student_runtime import StudentRuntimeCoordinator

        flags = resolve_v2_feature_flags()
        if flags.SR_SESSION_PRIMARY:
            experience = EducationalExperienceService().load_for_user(
                int(current_user.id)
            )
            if (
                experience is not None
                and experience.mission is not None
                and experience.mission.mission_instance_id
            ):
                StudentRuntimeCoordinator(flags=flags).defer_mission(
                    user_id=int(current_user.id),
                    mission_instance_id=experience.mission.mission_instance_id,
                    reason_code=form.reason_code.data or "not_today",
                )
    except Exception:  # noqa: BLE001 — deferral preference must not hard-fail
        logger.exception("runtime_c_mission_defer_failed")
    flash(
        "Your study plan continues: we'll meet you when you're ready.",
        "info",
    )
    return redirect(url_for("student.home"))


@student_bp.post("/commitment/reflection/ack")
@login_required
def acknowledge_reflection():
    """Advance C3 → C4 after viewing completion reflection."""
    form = ReflectionAckForm()
    if not form.validate_on_submit():
        return redirect(url_for("student.home"))
    RecommendationCommitmentService.acknowledge_reflection(
        current_user.id,
        recommendation_key=(form.recommendation_key.data or "").strip(),
    )
    return redirect(url_for("student.home"))


@student_bp.post("/revision/acknowledge")
@login_required
def acknowledge_revision():
    """CQ-002 / CR1: syllabus-complete ack on the sole-runtime student surface.

    Mirrors ``dashboard.acknowledge_revision`` so Home does not depend on the
    legacy dashboard POST when ``SOLE_RUNTIME=1``.
    """
    from app.services.learning_lifecycle_service import LearningLifecycleService

    LearningLifecycleService.acknowledge_revision(current_user.id)
    return redirect(url_for("student.home"))


@student_bp.post("/revision/begin")
@login_required
def begin_revision():
    """Primary Revision CTA — begin revision via session start."""
    form = BeginRevisionForm()
    if not form.validate_on_submit():
        flash("We couldn't begin revision. Please try again.", "warning")
        return redirect(url_for("student.revision"))
    mission_id = (form.mission_id.data or "").strip() or None
    session_id = (form.session_id.data or "").strip() or None
    try:
        handle = start_todays_session(
            mission_id=mission_id, session_id=session_id
        )
    except Exception as exc:
        from app.application.educational_runtime_engine import (
            EducationalPrerequisiteMissing,
        )

        if isinstance(exc, EducationalPrerequisiteMissing):
            logger.warning("Begin revision educational readiness: %s", exc)
            flash(
                "Your curriculum is not ready for revision yet. Return here "
                "when your subjects are available.",
                "warning",
            )
            return redirect(url_for("student.revision"))
        if isinstance(exc, PortUnavailable):
            flash(
                "Revision is temporarily unavailable. Please try again shortly.",
                "warning",
            )
            return redirect(url_for("student.revision"))
        if isinstance(exc, StudentExperienceError):
            logger.warning("Begin revision failed: %s", exc)
            flash(
                "We couldn't begin revision. Please try again from this page.",
                "warning",
            )
            return redirect(url_for("student.revision"))
        raise

    composition = get_experience_composition()
    if composition is not None:
        composition.emit_revision_started(
            str(handle.student_id),
            option_id=(form.option_id.data or "").strip() or None,
        )
    topic = handle.topic_title or "selected topic"
    # UX-001: land on Overview briefing; Begin Session starts practice.
    target_session_id = handle.session_id or session_id
    if target_session_id:
        flash(
            f"Revision ready. {topic}. Review today's objective, then begin.",
            "success",
        )
        return redirect(
            url_for("session.overview", session_id=target_session_id)
        )
    flash(f"Revision started. {topic}. Continue when you're ready.", "success")
    return redirect(url_for("student.home"))
