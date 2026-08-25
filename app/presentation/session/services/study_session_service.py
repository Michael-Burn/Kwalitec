"""Study Session service — Persistent context / Learning Task / Practice.

Authority: DX-005C Focused Study Session + LXP-003 session product completion.
Presentation projection only. Does not alter session, mission, or
question engines.
"""

from __future__ import annotations

from flask import url_for

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.session.content_sections import (
    parse_session_content_body,
    strip_author_voice,
)
from app.presentation.session.dto.study_session import (
    LearningTask,
    SessionDisclosure,
    SessionPersistentContext,
    StudySessionPage,
)
from app.presentation.session.view_models import SessionPageViewModel

_PAGE_TITLE = "Session"


class StudySessionService:
    """Build the DX-005C Study Session page from existing session VMs."""

    def build_page(self, page: SessionPageViewModel) -> StudySessionPage:
        """Assemble persistent context, L0 task, L1 content, L2/L3."""
        surface = SessionSurface(page.shell.active_surface)
        product = bool(resolve_v2_feature_flags().SR_SESSION_COMPLETION_PRODUCT)
        substance = bool(resolve_v2_feature_flags().SR_SESSION_SUBSTANCE)
        context = self._context(page, surface)
        task = self._task(page, surface, product=product, substance=substance)
        primary_label, primary_kind, primary_enabled, blocking = self._primary(
            page, surface, product=product
        )
        content = self._content(page, surface, product=product, substance=substance)
        content_body = strip_author_voice(str(content["body"] or ""))
        content_support = strip_author_voice(str(content["support"] or ""))
        # Drop support when it merely repeats the body (legacy exit_line dump).
        if content_support and content_body and content_support in content_body:
            content_support = ""
        content_sections = parse_session_content_body(content_body)
        disclosures = self._disclosures(page, surface)
        # KWP-002: technical IDs stay off learner chrome (founder diagnostics only).
        technical: tuple[str, ...] = ()
        reading_progress = self._reading_progress_percent(page, surface)
        checklist = self._checklist(page)
        lifecycle = ""
        completion = page.completion
        meta = getattr(completion, "metadata", None) if completion is not None else None
        if meta:
            meta_map = dict(meta)
            lifecycle = meta_map.get("lifecycle_label", "")

        learning_objectives: tuple[str, ...] = ()
        if page.overview and page.overview.learning_objectives:
            learning_objectives = tuple(page.overview.learning_objectives)
        activity_type = ""
        stage_label = ""
        if page.activity:
            activity_type = page.activity.activity_type or ""
            stage_label = page.activity.stage_label or ""
        flow_label = ""
        if substance:
            flow_label = "Read → Worked example → Practice → Reflection"

        page_title = self._page_title(page, surface)
        journey_update = ""
        finish_outcome = ""
        insights: tuple[str, ...] = ()
        next_rec = ""
        headline = ""
        what_studied = ""
        performance_summary = ""
        progress_explanation = ""
        tomorrow_preview = ""
        assessment_mode_active = False
        assessment_summary = ""
        exercises_assigned: tuple[str, ...] = ()
        exercises_completed: tuple[str, ...] = ()
        strengthened: tuple[str, ...] = ()
        needs_reinforcement: tuple[str, ...] = ()
        syllabus_refs: tuple[str, ...] = ()
        sitting_report_ready = False
        strategy_title = ""
        strategy_body = ""
        strategy_explanation = ""
        strategy_spacing_guidance = ""
        strategy_momentum_guidance = ""
        strategy_confidence_guidance = ""
        diagnostic_guidance = ""
        diagnostic_explanation = ""
        difficulty_title = ""
        difficulty_guidance = ""
        difficulty_explanation = ""
        effectiveness_feedback = ""
        effectiveness_explanation = ""
        if completion is not None:
            journey_update = completion.journey_update_label or ""
            finish_outcome = completion.finish_outcome_label or ""
            insights = completion.learning_insights or ()
            next_rec = completion.next_recommendation or ""
            headline = completion.headline or ""
            what_studied = completion.what_studied or ""
            performance_summary = completion.performance_summary or ""
            progress_explanation = completion.progress_explanation or ""
            tomorrow_preview = completion.tomorrow_preview or ""
            assessment_mode_active = bool(completion.assessment_mode_active)
            assessment_summary = completion.assessment_summary or ""
            exercises_assigned = completion.exercises_assigned or ()
            exercises_completed = completion.exercises_completed or ()
            strengthened = completion.strengthened or ()
            needs_reinforcement = completion.needs_reinforcement or ()
            syllabus_refs = completion.syllabus_refs or ()
            sitting_report_ready = bool(completion.sitting_report_ready)
            strategy_title = completion.strategy_title or ""
            strategy_body = completion.strategy_body or ""
            strategy_explanation = completion.strategy_explanation or ""
            strategy_spacing_guidance = (
                completion.strategy_spacing_guidance or ""
            )
            strategy_momentum_guidance = (
                completion.strategy_momentum_guidance or ""
            )
            strategy_confidence_guidance = (
                completion.strategy_confidence_guidance or ""
            )
            diagnostic_guidance = completion.diagnostic_guidance or ""
            diagnostic_explanation = completion.diagnostic_explanation or ""
            difficulty_title = completion.difficulty_title or ""
            difficulty_guidance = completion.difficulty_guidance or ""
            difficulty_explanation = completion.difficulty_explanation or ""
            effectiveness_feedback = completion.effectiveness_feedback or ""
            effectiveness_explanation = (
                completion.effectiveness_explanation or ""
            )
            if completion.learning_objectives and not learning_objectives:
                learning_objectives = completion.learning_objectives

        why_today = ""
        concept_focus: tuple[str, ...] = ()
        session_stages: tuple[str, ...] = ()
        expected_outcome = ""
        checkpoint_preview = ""
        reflection_preview = ""
        explanation = None
        if surface is SessionSurface.OVERVIEW:
            briefing = self._overview_briefing(page, flow_label=flow_label)
            why_today = briefing["why_today"]
            concept_focus = briefing["concept_focus"]
            session_stages = briefing["session_stages"]
            expected_outcome = briefing["expected_outcome"]
            checkpoint_preview = briefing["checkpoint_preview"]
            reflection_preview = briefing["reflection_preview"]
            if briefing["learning_objectives"] and not learning_objectives:
                learning_objectives = briefing["learning_objectives"]
            if page.overview is not None:
                explanation = page.overview.explanation

        workflow_steps: tuple[str, ...] = ()
        workflow_step_index = 0
        page_eyebrow = (page.shell.page_eyebrow or "").strip()
        estimated_time_label = ""
        if page.shell.steps:
            workflow_steps = tuple(step.label for step in page.shell.steps)
            active = next((s for s in page.shell.steps if s.is_active), None)
            if active:
                workflow_step_index = max(0, active.step_number - 1)
            elif surface is SessionSurface.COMPLETE:
                workflow_step_index = max(0, len(workflow_steps) - 1)
        if surface is SessionSurface.OVERVIEW and page.overview:
            estimated_time_label = (
                page.overview.estimated_duration_label or ""
            ).strip()

        return StudySessionPage(
            page_title=page_title,
            surface=surface.value,
            context=context,
            task=task,
            primary_label=primary_label,
            primary_kind=primary_kind,
            primary_enabled=primary_enabled,
            blocking_issue=blocking,
            exit_href=url_for("student.home"),
            exit_label="Exit" if not product else "Pause & Exit",
            content_title=content["title"],
            content_body=content_body,
            content_support=content_support,
            content_sections=content_sections,
            answer_prompt=content["answer_prompt"],
            show_answer_input=content["show_answer_input"],
            feedback_outcome=content["feedback_outcome"],
            feedback_explanation=content["feedback_explanation"],
            model_answer=str(content.get("model_answer") or ""),
            common_mistake=str(content.get("common_mistake") or ""),
            feedback_next_action=str(content.get("feedback_next_action") or ""),
            disclosures=disclosures,
            technical_lines=technical,
            session_id=page.shell.session_id,
            activity_id=(page.activity.activity_id if page.activity else ""),
            mission_id=(page.overview.mission_id if page.overview else "") or "",
            reading_progress_percent=reading_progress,
            show_pause=product
            and surface
            in {
                SessionSurface.OVERVIEW,
                SessionSurface.ACTIVITY,
                SessionSurface.REFLECTION,
            }
            and surface is not SessionSurface.OVERVIEW,
            finish_review_required=product and surface is SessionSurface.SUMMARY,
            lifecycle_label=lifecycle,
            checklist=checklist,
            learning_objectives=learning_objectives,
            activity_type=activity_type,
            stage_label=stage_label,
            educational_flow_label=flow_label,
            why_today=why_today,
            concept_focus=concept_focus,
            session_stages=session_stages,
            expected_outcome=expected_outcome,
            checkpoint_preview=checkpoint_preview,
            reflection_preview=reflection_preview,
            explanation=explanation,
            journey_update_label=journey_update,
            finish_outcome_label=finish_outcome,
            learning_insights=insights,
            next_recommendation=next_rec,
            completion_headline=headline,
            what_studied=what_studied,
            performance_summary=performance_summary,
            progress_explanation=progress_explanation,
            tomorrow_preview=tomorrow_preview,
            assessment_mode_active=assessment_mode_active,
            assessment_summary=assessment_summary,
            exercises_assigned=exercises_assigned,
            exercises_completed=exercises_completed,
            strengthened=strengthened,
            needs_reinforcement=needs_reinforcement,
            syllabus_refs=syllabus_refs,
            sitting_report_ready=sitting_report_ready,
            strategy_title=strategy_title,
            strategy_body=strategy_body,
            strategy_explanation=strategy_explanation,
            strategy_spacing_guidance=strategy_spacing_guidance,
            strategy_momentum_guidance=strategy_momentum_guidance,
            strategy_confidence_guidance=strategy_confidence_guidance,
            diagnostic_guidance=diagnostic_guidance,
            diagnostic_explanation=diagnostic_explanation,
            difficulty_title=difficulty_title,
            difficulty_guidance=difficulty_guidance,
            difficulty_explanation=difficulty_explanation,
            effectiveness_feedback=effectiveness_feedback,
            effectiveness_explanation=effectiveness_explanation,
            workflow_steps=workflow_steps,
            workflow_step_index=workflow_step_index,
            page_eyebrow=page_eyebrow,
            estimated_time_label=estimated_time_label,
        )

    @staticmethod
    def _page_title(page: SessionPageViewModel, surface: SessionSurface) -> str:
        """Professional topic title for session chrome (KWP-002)."""
        topic = (page.shell.topic_title or "").strip()
        if surface is SessionSurface.COMPLETE and page.completion:
            if page.completion.primary_topic:
                return f"Today: {page.completion.primary_topic}"
            return "Sitting Report"
        if topic:
            return f"Today: {topic}"
        return _PAGE_TITLE

    @staticmethod
    def _reading_progress_percent(
        page: SessionPageViewModel, surface: SessionSurface
    ) -> int:
        """Map session position to a calm 0–100 reading bar (presentation only)."""
        if page.progress and page.progress.has_progress and page.progress.total:
            done = max(0, int(page.progress.completed))
            total = max(1, int(page.progress.total))
            # Show current step as in-progress (not yet complete).
            pct = int(round(100 * min(total, done + 1) / total))
            return max(0, min(100, pct))
        steps = page.shell.steps or ()
        if steps:
            active = next((s for s in steps if s.is_active), None)
            if active:
                return max(
                    0,
                    min(100, int(round(100 * active.step_number / len(steps)))),
                )
            if surface in {SessionSurface.SUMMARY, SessionSurface.COMPLETE}:
                return 100
        surface_pct = {
            SessionSurface.OVERVIEW: 15,
            SessionSurface.ACTIVITY: 45,
            SessionSurface.REFLECTION: 75,
            SessionSurface.SUMMARY: 90,
            SessionSurface.COMPLETE: 100,
        }
        return surface_pct.get(surface, 0)

    def _context(
        self, page: SessionPageViewModel, surface: SessionSurface
    ) -> SessionPersistentContext:
        subject = (page.shell.topic_title or "").strip() or "Today's practice"
        chapter = ""
        objective = ""
        activity_label = ""
        progress = ""
        elapsed = ""

        if page.overview:
            objective = (page.overview.objective or "").strip()
            if page.overview.topics:
                chapter = page.overview.topics[0]
            # PX-003: keep Overview duration out of the live Timer slot.

        if page.activity:
            activity_label = page.activity.position_label or "Learning activity"
            if page.activity.topic_title:
                chapter = chapter or page.activity.topic_title
            if page.activity.has_explanation:
                activity_label = f"Review · {activity_label}"

        if page.progress and page.progress.has_progress:
            progress = (
                f"Session step {page.progress.completed + 1} of "
                f"{page.progress.total}"
                if page.progress.remaining > 0
                else f"Session step {page.progress.total} of {page.progress.total}"
            )
            if page.progress.remaining_time_label and not elapsed:
                elapsed = page.progress.remaining_time_label
            if page.progress.current_topic:
                chapter = chapter or page.progress.current_topic

        if page.reflection:
            activity_label = activity_label or "Session reflection"
            if page.reflection.topic_title:
                subject = page.reflection.topic_title or subject

        if page.completion:
            activity_label = activity_label or "Session complete"
            if page.completion.primary_topic:
                subject = page.completion.primary_topic or subject
            if page.completion.time_studied_label:
                elapsed = page.completion.time_studied_label

        if not activity_label:
            activity_label = {
                SessionSurface.OVERVIEW: "Begin practice",
                SessionSurface.ACTIVITY: "Learning activity",
                SessionSurface.REFLECTION: "Session reflection",
                SessionSurface.SUMMARY: "Session complete",
                SessionSurface.COMPLETE: "Return Home",
            }.get(surface, "Practice")

        if not progress and page.shell.steps:
            active = next((s for s in page.shell.steps if s.is_active), None)
            total = len(page.shell.steps)
            if active:
                progress = f"Session step {active.step_number} of {total}"
            elif surface is SessionSurface.COMPLETE:
                progress = f"Session step {total} of {total}"

        if not objective:
            # Never dump activity.context into sticky chrome: for package
            # Reading activities that field is the full L1 body. Package LO
            # text is not on ActivityViewModel when overview is absent
            # (activity surface), so prefer short overview fields, else a
            # type-aware one-liner matching existing session tone.
            if page.overview and page.overview.learning_goal:
                objective = page.overview.learning_goal.strip()
            elif page.overview and page.overview.learning_objectives:
                lead = (page.overview.learning_objectives[0] or "").strip()
                if lead:
                    objective = lead
            else:
                stage = ""
                if page.activity:
                    stage = (
                        page.activity.activity_type
                        or page.activity.stage_label
                        or ""
                    ).strip().lower()
                if stage in {"read", "reading"}:
                    objective = "Complete today's reading"
                else:
                    objective = "Complete the current practice step"

        if not chapter:
            chapter = subject

        return SessionPersistentContext(
            subject=subject,
            chapter=chapter,
            objective=objective,
            activity_label=activity_label,
            session_progress=progress,
            elapsed_label=elapsed,
        )

    def _task(
        self,
        page: SessionPageViewModel,
        surface: SessionSurface,
        *,
        product: bool = False,
        substance: bool = False,
    ) -> LearningTask:
        duration = ""
        next_milestone = ""
        expected = ""
        instruction = "Complete the current practice step."
        activity = "Practice"

        if surface is SessionSurface.OVERVIEW and page.overview:
            activity = "Begin session" if substance else "Begin practice"
            expected = page.overview.objective or "Start today's practice"
            duration = page.overview.estimated_duration_label
            next_milestone = (
                "Reading"
                if substance
                else (page.overview.activity_count_label or "First activity")
            )
            instruction = (
                "Review today's learning objectives, then start reading."
                if substance
                else "Start the session to open the first learning activity."
            )
            if page.overview.why_studying:
                # One concise line only — strip essay padding.
                why = page.overview.why_studying.strip()
                if why and len(why) <= 160:
                    instruction = why

        elif surface is SessionSurface.ACTIVITY and page.activity:
            stage = (page.activity.activity_type or "").strip()
            if page.activity.has_explanation:
                activity = "Review finding"
                expected = "Acknowledge the explanation, then continue"
                instruction = (
                    "Review the explanation, then continue to the next step."
                    if not page.activity.is_final
                    else "Review the explanation, then continue to reflection."
                )
                next_milestone = (
                    "Reflection"
                    if page.activity.is_final
                    else "Next activity"
                )
            elif stage == "read":
                activity = "Reading"
                expected = "Study the reading, then note one key idea"
                instruction = "Read carefully, then capture what stood out."
                next_milestone = "Worked example"
            elif stage == "worked_example":
                activity = "Worked example"
                expected = "Follow the method, then note the step you will reuse"
                instruction = (
                    "Stay with the worked example before moving to practice."
                )
                next_milestone = "Practice"
            elif stage == "practice":
                activity = "Practice"
                expected = "Submit your answer for this practice step"
                instruction = "Use the reading and worked example to answer."
                next_milestone = (
                    "Reflection" if page.activity.is_final else "Next practice"
                )
            else:
                activity = "Answer question"
                expected = "Submit your answer for this activity"
                instruction = "Read the question, write your answer, then submit."
                next_milestone = "Immediate feedback"
            if page.progress and page.progress.remaining_time_label:
                duration = page.progress.remaining_time_label

        elif surface is SessionSurface.REFLECTION and page.reflection:
            from app.application.student_experience.student_microcopy import (
                REFLECTION_ACTIVITY_LABEL,
                REFLECTION_EXPECTED_LABEL,
            )

            activity = REFLECTION_ACTIVITY_LABEL
            expected = REFLECTION_EXPECTED_LABEL
            instruction = (
                page.reflection.reflection_prompt
                or "What mattered in this practice?"
            )
            next_milestone = "Ready to finish" if product else "Return Home"
            if page.reflection.topic_title:
                expected = f"Reflect on {page.reflection.topic_title}"

        elif surface in {SessionSurface.SUMMARY, SessionSurface.COMPLETE}:
            if product and surface is SessionSurface.SUMMARY:
                activity = "Finish review"
                expected = "Record Yes, Partially, or No for today's planned study"
                instruction = (
                    "Completing a session means today's planned learning "
                    "activity occurred. It does not mean mastery increased."
                )
                next_milestone = "Home"
            else:
                activity = "Complete session"
                expected = "Close practice and return to Home"
                instruction = "Practice for this session is finished."
                next_milestone = "Home"
                if page.completion and page.completion.primary_topic:
                    instruction = (
                        f"Practice on {page.completion.primary_topic} is finished."
                    )
                if page.completion and page.completion.time_studied_label:
                    duration = page.completion.time_studied_label

        return LearningTask(
            activity=activity,
            expected_outcome=expected,
            estimated_duration=duration,
            next_milestone=next_milestone,
            instruction=instruction,
        )

    def _primary(
        self,
        page: SessionPageViewModel,
        surface: SessionSurface,
        *,
        product: bool = False,
    ) -> tuple[str, str, bool, str]:
        if surface is SessionSurface.OVERVIEW and page.overview:
            label = page.overview.begin_label or "Begin Session"
            if label.strip().lower() in {"start session", "start"}:
                label = "Begin Session"
            return label, "begin_form", page.overview.begin_enabled, ""

        if surface is SessionSurface.ACTIVITY and page.activity:
            if page.activity.has_explanation:
                label = page.activity.next_action_label or "Continue"
                return label, "advance_form", True, ""
            return "Submit Answer", "answer_form", True, ""

        if surface is SessionSurface.REFLECTION and page.reflection:
            if product:
                label = "Finish Session"
                return label, "request_finish_form", True, ""
            label = page.reflection.next_action_label or "Continue to Summary"
            return label, "reflection_form", True, ""

        if surface is SessionSurface.SUMMARY:
            if product:
                return "Finish Session", "finish_review_form", True, ""
            if page.completion:
                label = page.completion.return_home_label or "Return Home"
                return (
                    label,
                    "complete_form",
                    page.completion.return_home_enabled,
                    "",
                )
            return "Return Home", "complete_form", True, ""

        if surface is SessionSurface.COMPLETE:
            if page.completion:
                label = page.completion.return_home_label or "Return Home"
                return (
                    label,
                    "complete_form",
                    page.completion.return_home_enabled,
                    "",
                )
            return "Return Home", "complete_form", True, ""

        return "", "none", False, ""

    def _content(
        self,
        page: SessionPageViewModel,
        surface: SessionSurface,
        *,
        product: bool = False,
        substance: bool = False,
    ) -> dict[str, object]:
        empty = {
            "title": "",
            "body": "",
            "support": "",
            "answer_prompt": "Your answer",
            "show_answer_input": False,
            "feedback_outcome": "",
            "feedback_explanation": "",
            "model_answer": "",
            "common_mistake": "",
            "feedback_next_action": "",
        }

        if surface is SessionSurface.OVERVIEW and page.overview:
            # UX-001: educational detail lives in the briefing block — keep L1 lean.
            objective = (page.overview.objective or "").strip()
            return {
                **empty,
                "title": "Today's Session",
                "body": objective,
                "support": "",
            }

        if surface is SessionSurface.ACTIVITY and page.activity:
            act = page.activity
            feedback_outcome = ""
            feedback_explanation = ""
            model_answer = act.model_answer or ""
            common_mistake = act.common_mistake or ""
            feedback_next_action = act.next_action or ""
            if act.has_explanation:
                feedback_outcome = act.feedback_outcome or "Reviewed"
                feedback_explanation = act.explanation or ""
            title = act.question or "Learning activity"
            if act.stage_label:
                title = f"{act.stage_label}: {act.question or act.stage_label}"
            return {
                "title": title,
                "body": act.context or "",
                "support": act.supporting_material or "",
                "answer_prompt": act.answer_prompt or "Your answer",
                "show_answer_input": not act.has_explanation,
                "feedback_outcome": feedback_outcome,
                "feedback_explanation": feedback_explanation,
                "model_answer": model_answer if act.has_explanation else "",
                "common_mistake": common_mistake if act.has_explanation else "",
                "feedback_next_action": (
                    feedback_next_action if act.has_explanation else ""
                ),
            }

        if surface is SessionSurface.REFLECTION and page.reflection:
            from app.application.student_experience.student_microcopy import (
                REFLECTION_VALUE_FRAMING,
                REFLECTION_VALUE_TITLE,
            )

            body = page.reflection.reflection_prompt or ""
            support = ""
            if page.reflection.key_insight:
                support = page.reflection.key_insight
            else:
                support = REFLECTION_VALUE_FRAMING
            return {
                **empty,
                "title": REFLECTION_VALUE_TITLE,
                "body": body,
                "support": support,
            }

        if surface is SessionSurface.SUMMARY and product:
            return {
                **empty,
                "title": "Finish review",
                "body": (
                    "Did you complete today's planned study? "
                    "Choose Yes, Partially, or No."
                ),
            }

        if surface in {SessionSurface.SUMMARY, SessionSurface.COMPLETE}:
            topic = ""
            headline = ""
            journey_update = ""
            if page.completion:
                topic = page.completion.primary_topic or ""
                headline = page.completion.headline or ""
                journey_update = page.completion.journey_update_label or ""
            if surface is SessionSurface.COMPLETE:
                title = headline or "Sitting Report"
                body_parts: list[str] = []
                if page.completion and page.completion.what_studied:
                    body_parts.append(page.completion.what_studied)
                elif journey_update:
                    body_parts.append(journey_update)
                elif topic:
                    body_parts.append(
                        f"You completed practice on {topic}. Your Journey is updated."
                    )
                else:
                    body_parts.append(
                        "Honest practice recorded. "
                        "Your Journey is ready with the next step."
                    )
                if page.completion and page.completion.performance_summary:
                    body_parts.append(page.completion.performance_summary)
                if page.completion and page.completion.strategy_explanation:
                    body_parts.append(
                        f"Why: {page.completion.strategy_explanation}"
                    )
                elif page.completion and page.completion.next_recommendation:
                    body_parts.append(
                        f"Up next: {page.completion.next_recommendation}"
                    )
                elif page.completion and page.completion.tomorrow_preview:
                    body_parts.append(page.completion.tomorrow_preview)
                return {
                    **empty,
                    "title": title,
                    "body": "\n".join(body_parts),
                }
            body = "Session practice complete."
            if topic:
                body = f"Session practice on {topic} is complete."
            return {**empty, "title": "Session complete", "body": body}

        return empty

    def _checklist(
        self, page: SessionPageViewModel
    ) -> tuple[tuple[str, str, bool], ...]:
        """Best-effort checklist from overview/completion metadata (P2)."""
        # Checklist is injected via overview technical metadata when available.
        # Presentation stays honest when empty.
        return ()

    def _disclosures(
        self, page: SessionPageViewModel, surface: SessionSurface
    ) -> tuple[SessionDisclosure, ...]:
        items: list[SessionDisclosure] = []

        if surface is SessionSurface.ACTIVITY and page.activity:
            if page.activity.has_hints and not page.activity.has_explanation:
                hints = "\n".join(f"• {h}" for h in page.activity.hints if h)
                if hints:
                    items.append(
                        SessionDisclosure(title="Hint", body=hints, open=False)
                    )
            if page.activity.supporting_material and page.activity.has_explanation:
                items.append(
                    SessionDisclosure(
                        title="Reference",
                        body=page.activity.supporting_material,
                        open=False,
                    )
                )

        if surface is SessionSurface.REFLECTION and page.reflection:
            if page.reflection.concept_confidence:
                items.append(
                    SessionDisclosure(
                        title="Concept confidence",
                        body=page.reflection.concept_confidence,
                        open=False,
                    )
                )
            if page.reflection.suggested_improvement:
                items.append(
                    SessionDisclosure(
                        title="Suggested improvement",
                        body=page.reflection.suggested_improvement,
                        open=False,
                    )
                )

        if surface is SessionSurface.OVERVIEW and page.overview:
            if page.overview.learning_goal:
                items.append(
                    SessionDisclosure(
                        title="Learning goal",
                        body=page.overview.learning_goal,
                        open=False,
                    )
                )
            if page.overview.topics and len(page.overview.topics) > 1:
                topics = "\n".join(f"• {t}" for t in page.overview.topics)
                items.append(
                    SessionDisclosure(title="Topics", body=topics, open=False)
                )

        return tuple(items)

    @staticmethod
    def _overview_briefing(
        page: SessionPageViewModel,
        *,
        flow_label: str,
    ) -> dict[str, object]:
        """UX-001 — project Session Overview briefing (presentation only).

        Prefers overview VM fields; optionally enriches via Educational
        Authoring for concept focus / stages / checkpoint / reflection.
        """
        empty: dict[str, object] = {
            "why_today": "",
            "concept_focus": (),
            "session_stages": (),
            "expected_outcome": "",
            "checkpoint_preview": "",
            "reflection_preview": "",
            "learning_objectives": (),
        }
        overview = page.overview
        if overview is None:
            return empty

        why = (overview.why_studying or "").strip()
        expected = (overview.expected_improvement_label or "").strip()
        objectives = tuple(overview.learning_objectives or ())
        stages: tuple[str, ...] = ()
        if flow_label:
            stages = tuple(
                part.strip() for part in flow_label.split("→") if part.strip()
            )

        concept_focus: tuple[str, ...] = ()
        checkpoint = ""
        reflection = ""
        topic = (page.shell.topic_title or "").strip()
        if not topic and overview.topics:
            topic = (overview.topics[0] or "").strip()
        if topic:
            try:
                from app.application.educational_authoring import (
                    get_educational_authoring_engine,
                )

                composition = get_educational_authoring_engine().author_from_topic(
                    topic_title=topic,
                    objective_text=(
                        objectives[0]
                        if objectives
                        else (overview.objective or overview.learning_goal or "")
                    ),
                )
                if composition is not None:
                    episodes = getattr(composition, "episodes", ()) or ()
                    if episodes:
                        ep = episodes[0]
                        concepts = tuple(
                            c for c in (getattr(ep, "concept_focus", ()) or ()) if c
                        )
                        if concepts:
                            concept_focus = concepts
                        labels = tuple(
                            a
                            for a in (getattr(ep, "activity_labels", ()) or ())
                            if a
                        )
                        if labels:
                            stages = labels
                        criteria = tuple(
                            c
                            for c in (getattr(ep, "success_criteria", ()) or ())
                            if c
                        )
                        if criteria and not expected:
                            expected = criteria[0]
                        ep_obj = (getattr(ep, "learning_objective", "") or "").strip()
                        if ep_obj and not objectives:
                            objectives = (ep_obj,)
                    checkpoint = (
                        getattr(composition, "checkpoint_prompt", "") or ""
                    ).strip()
                    reflection = (
                        getattr(composition, "reflection_prompt", "") or ""
                    ).strip()
                    narrative = (
                        getattr(composition, "mission_narrative", "") or ""
                    ).strip()
                    if narrative and not why:
                        why = narrative
            except Exception:  # noqa: BLE001 — briefing is best-effort
                pass

        return {
            "why_today": why,
            "concept_focus": concept_focus,
            "session_stages": stages,
            "expected_outcome": expected,
            "checkpoint_preview": checkpoint,
            "reflection_preview": reflection,
            "learning_objectives": objectives,
        }

    def _technical(self, page: SessionPageViewModel) -> tuple[str, ...]:
        lines = [f"Session ID · {page.shell.session_id}"]
        if page.activity and page.activity.activity_id:
            lines.append(f"Activity ID · {page.activity.activity_id}")
        if page.overview and page.overview.mission_id:
            lines.append(f"Mission ID · {page.overview.mission_id}")
        return tuple(lines)
