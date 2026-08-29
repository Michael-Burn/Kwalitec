"""Study Session service — Persistent context / Learning Task / Practice.

Authority: DX-005C Focused Study Session + LXP-003 session product completion.
Presentation projection only. Does not alter session, mission, or
question engines.
"""

from __future__ import annotations

import re

from flask import url_for

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.domain.session_experience.session_workspace import SessionSurface
from app.presentation.session.content_sections import (
    parse_session_content_body,
    present_practice_content,
    present_reading_content,
    present_worked_example_content,
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
_SYLLABUS_CODE_IN_TEXT = re.compile(r"Syllabus\s+(\d+(?:\.\d+)*)", re.IGNORECASE)
# Concise journey labels for the stage indicator (SURFACE_LABELS stay product-long).
_STAGE_INDICATOR_LABELS = {
    "Session Overview": "Overview",
    "Learning Activity": "Activity",
    "Reflection": "Reflection",
    "Session Summary": "Summary",
    "Sitting Report": "Summary",
}


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
        content_intro_line = ""
        content_sections_more = ()
        if surface is SessionSurface.ACTIVITY and page.activity:
            stage = _activity_stage_key(page.activity)
            if _is_reading_activity(page.activity) and content_sections:
                presented = present_reading_content(content_sections)
                content_intro_line = presented.intro_line
                content_sections = presented.primary
                content_sections_more = presented.more
            elif stage == "worked_example" and content_sections:
                presented = present_worked_example_content(content_sections)
                content_intro_line = presented.intro_line
                content_sections = presented.primary
                content_sections_more = presented.more
            elif stage == "practice":
                # Prompt is the real question; assemble once (never title-dump).
                # Skip when feedback is showing — keep explanation chrome intact.
                if not getattr(page.activity, "has_explanation", False):
                    presented = present_practice_content(
                        prompt=str(content.get("practice_prompt") or ""),
                        body=content_body,
                    )
                    content_intro_line = presented.intro_line
                    content_sections = presented.primary
                    content_sections_more = presented.more
                    if content_sections:
                        content_body = ""
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
        confidence_calibration = ""
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
        strategy_confidence_guidance = ""
        diagnostic_guidance = ""
        diagnostic_explanation = ""
        difficulty_guidance = ""
        difficulty_explanation = ""
        effectiveness_feedback = ""
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
            confidence_calibration = completion.confidence_calibration or ""
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
            strategy_confidence_guidance = (
                completion.strategy_confidence_guidance or ""
            )
            diagnostic_guidance = completion.diagnostic_guidance or ""
            diagnostic_explanation = completion.diagnostic_explanation or ""
            difficulty_guidance = completion.difficulty_guidance or ""
            difficulty_explanation = completion.difficulty_explanation or ""
            effectiveness_feedback = completion.effectiveness_feedback or ""
            if completion.learning_objectives and not learning_objectives:
                learning_objectives = completion.learning_objectives

        why_today = ""
        concept_focus: tuple[str, ...] = ()
        session_stages: tuple[str, ...] = ()
        expected_outcome = ""
        checkpoint_preview = ""
        reflection_preview = ""
        prior_reflection_excerpt = ""
        explanation = None
        if surface is SessionSurface.OVERVIEW:
            briefing = self._overview_briefing(page, flow_label=flow_label)
            why_today = briefing["why_today"]
            concept_focus = briefing["concept_focus"]
            session_stages = briefing["session_stages"]
            expected_outcome = briefing["expected_outcome"]
            checkpoint_preview = briefing["checkpoint_preview"]
            reflection_preview = briefing["reflection_preview"]
            # Briefing is authoritative for Overview Session details — including
            # quiet omit when the mission title is a generic decision placeholder.
            learning_objectives = tuple(briefing["learning_objectives"] or ())
            if page.overview is not None:
                explanation = page.overview.explanation
            prior_reflection_excerpt = _prior_reflection_excerpt_for_overview(
                page
            )

        workflow_steps: tuple[str, ...] = ()
        workflow_step_index = 0
        page_eyebrow = (page.shell.page_eyebrow or "").strip()
        estimated_time_label = ""
        if page.shell.steps:
            workflow_steps = tuple(
                _STAGE_INDICATOR_LABELS.get(step.label, step.label)
                for step in page.shell.steps
            )
            active = next((s for s in page.shell.steps if s.is_active), None)
            if active:
                workflow_step_index = max(0, active.step_number - 1)
            elif surface is SessionSurface.COMPLETE:
                workflow_step_index = max(0, len(workflow_steps) - 1)
        if surface is SessionSurface.OVERVIEW and page.overview:
            estimated_time_label = (
                page.overview.estimated_duration_label or ""
            ).strip()

        topic_display = (page.shell.topic_title or "").strip()
        if not topic_display and page.overview and page.overview.topics:
            topic_display = (page.overview.topics[0] or "").strip()
        if (
            not topic_display
            and surface is SessionSurface.COMPLETE
            and page.completion
        ):
            topic_display = (page.completion.primary_topic or "").strip()
        if topic_display.lower().startswith("today:"):
            topic_display = topic_display.split(":", 1)[1].strip()
        subject_code = ""
        if page.overview:
            subject_code = (page.overview.subject_code or "").strip()
        context_eyebrow = _context_eyebrow(subject_code, topic_display)
        meta_duration = _compact_duration_label(estimated_time_label)
        meta_mode = _meta_mode_label(surface, page)

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
            content_intro_line=content_intro_line,
            content_sections_more=content_sections_more,
            answer_prompt=content["answer_prompt"],
            show_answer_input=content["show_answer_input"],
            feedback_outcome=content["feedback_outcome"],
            feedback_explanation=content["feedback_explanation"],
            model_answer=str(content.get("model_answer") or ""),
            common_mistake=str(content.get("common_mistake") or ""),
            feedback_next_action=str(content.get("feedback_next_action") or ""),
            response_type=str(content.get("response_type") or ""),
            practice_choices=tuple(content.get("practice_choices") or ()),
            disclosures=disclosures,
            technical_lines=technical,
            session_id=page.shell.session_id,
            activity_id=(page.activity.activity_id if page.activity else ""),
            mission_id=(page.overview.mission_id if page.overview else "") or "",
            confidence_prompt=str(content.get("confidence_prompt") or ""),
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
            prior_reflection_excerpt=prior_reflection_excerpt,
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
            confidence_calibration=confidence_calibration,
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
            strategy_confidence_guidance=strategy_confidence_guidance,
            diagnostic_guidance=diagnostic_guidance,
            diagnostic_explanation=diagnostic_explanation,
            difficulty_guidance=difficulty_guidance,
            difficulty_explanation=difficulty_explanation,
            effectiveness_feedback=effectiveness_feedback,
            workflow_steps=workflow_steps,
            workflow_step_index=workflow_step_index,
            page_eyebrow=page_eyebrow,
            estimated_time_label=estimated_time_label,
            context_eyebrow=context_eyebrow,
            topic_display=topic_display,
            meta_duration=meta_duration,
            meta_mode=meta_mode,
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
                elif stage == "worked_example":
                    objective = "Follow today's worked example"
                elif stage == "practice":
                    objective = "Answer today's practice question"
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
            # Question lives in L1 / the reflection textarea — do not repeat it here.
            instruction = "Write a short note, then continue."
            next_milestone = "Ready to finish" if product else "Return Home"
            if page.reflection.topic_title:
                expected = f"Reflect on {page.reflection.topic_title}"

        elif surface in {SessionSurface.SUMMARY, SessionSurface.COMPLETE}:
            if product and surface is SessionSurface.SUMMARY:
                activity = "Finish review"
                expected = "Record Yes, Partially, or No for today's planned study"
                # Question lives on the finish-review form legend — keep task lean.
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
            # Approved Session UI: keep "Start Session" on Overview CTA.
            label = (page.overview.begin_label or "Start Session").strip()
            if label.lower() in {"start", "begin", "begin session"}:
                label = "Start Session"
            return label, "begin_form", page.overview.begin_enabled, ""

        if surface is SessionSurface.ACTIVITY and page.activity:
            if page.activity.has_explanation:
                label = page.activity.next_action_label or "Continue"
                return label, "advance_form", True, ""
            return "Submit Answer", "answer_form", True, ""

        if surface is SessionSurface.REFLECTION and page.reflection:
            # Always use reflection_form so the student can answer the prompt.
            # Product mode still advances to Finish Review via reflection_continue
            # → summary; do not swap to request_finish_form (that hid the input).
            if product:
                label = "Finish Session"
            else:
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
            "confidence_prompt": "",
            "feedback_outcome": "",
            "feedback_explanation": "",
            "model_answer": "",
            "common_mistake": "",
            "feedback_next_action": "",
            "practice_prompt": "",
            "response_type": "",
            "practice_choices": (),
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
            title = _activity_content_title(act)
            stage = _activity_stage_key(act)
            body = act.context or ""
            support = act.supporting_material or ""
            practice_prompt = ""
            if stage == "practice" and not act.has_explanation:
                # Prompt is the question; keep it out of the H2 title path.
                practice_prompt = act.question or ""
                # Prefer structured present_practice_content; leave stub as body.
                body = act.context or ""
                # Avoid dumping the same prompt again as support when it matches.
                if (
                    support
                    and practice_prompt
                    and support.strip() == practice_prompt.strip()
                ):
                    support = ""
            return {
                "title": title,
                "body": body,
                "support": support,
                "answer_prompt": act.answer_prompt or "Your answer",
                "show_answer_input": not act.has_explanation,
                "feedback_outcome": feedback_outcome,
                "feedback_explanation": feedback_explanation,
                "model_answer": model_answer if act.has_explanation else "",
                "common_mistake": common_mistake if act.has_explanation else "",
                "feedback_next_action": (
                    feedback_next_action if act.has_explanation else ""
                ),
                "practice_prompt": practice_prompt,
                "response_type": (act.response_type or "").strip().lower(),
                "practice_choices": tuple(act.choices or ()),
            }

        if surface is SessionSurface.REFLECTION and page.reflection:
            from app.application.student_experience.student_microcopy import (
                REFLECTION_VALUE_FRAMING,
                REFLECTION_VALUE_TITLE,
            )

            prompt = (page.reflection.reflection_prompt or "").strip()
            confidence_prompt = (page.reflection.confidence_prompt or "").strip()
            support = ""
            if page.reflection.key_insight:
                support = page.reflection.key_insight
            else:
                support = REFLECTION_VALUE_FRAMING
            # Show the question once as the textarea label; keep L1 framing lean.
            return {
                **empty,
                "title": REFLECTION_VALUE_TITLE,
                "body": "",
                "support": support,
                "answer_prompt": prompt or "Your reflection",
                "confidence_prompt": confidence_prompt,
                "show_answer_input": True,
            }

        if surface is SessionSurface.SUMMARY and product:
            # Form legend owns the Yes/Partially/No question — do not repeat it.
            # Task instruction already carries the mastery disclaimer.
            return {
                **empty,
                "title": "Finish review",
                "body": "",
                "support": "",
            }

        if surface in {SessionSurface.SUMMARY, SessionSurface.COMPLETE}:
            topic = ""
            headline = ""
            if page.completion:
                topic = page.completion.primary_topic or ""
                headline = page.completion.headline or ""
            if surface is SessionSurface.COMPLETE:
                # Structured Sitting Report fields render separately in the
                # template — keep content_body empty to avoid duplication.
                return {
                    **empty,
                    "title": headline or "Sitting Report",
                    "body": "",
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

        # Generic / decision-framed titles (e.g. "Continue with CS1") are not
        # syllabus concepts — omit concept focus, checkpoint, reflection, and
        # learning-objective mad-libs rather than invent false specificity.
        from app.application.educational_authoring.writing import (
            is_generic_session_topic_title,
        )

        if is_generic_session_topic_title(topic):
            return {
                "why_today": why,
                "concept_focus": (),
                "session_stages": stages,
                "expected_outcome": expected,
                "checkpoint_preview": "",
                "reflection_preview": "",
                "learning_objectives": (),
            }

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
                    educational_package_id=(
                        overview.educational_package_id or ""
                    ),
                    subject_code=overview.subject_code or "",
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


def _activity_stage_key(activity: object) -> str:
    """Normalised stage key from activity_type / stage_label."""
    stage = (
        getattr(activity, "activity_type", None)
        or getattr(activity, "stage_label", None)
        or ""
    )
    return str(stage).strip().lower().replace(" ", "_")


def _is_reading_activity(activity: object) -> bool:
    """True when the activity is Guided Reading (or revision reading)."""
    normalized = _activity_stage_key(activity)
    return normalized in {"read", "reading"} or "reading" in normalized


def _activity_content_title(activity: object) -> str:
    """Short L1 title. Never dump a full-sentence prompt into the heading."""
    label = str(getattr(activity, "stage_label", None) or "").strip()
    question = str(getattr(activity, "question", None) or "").strip()
    topic = str(getattr(activity, "topic_title", None) or "").strip()
    stage = _activity_stage_key(activity)

    if _is_reading_activity(activity):
        stage_label = label or "Reading"
        code_match = _SYLLABUS_CODE_IN_TEXT.search(question)
        if code_match:
            return f"{stage_label} · {code_match.group(1)}"
        if topic and len(topic) <= 48:
            return f"{stage_label}: {topic}"
        return stage_label

    if stage == "worked_example":
        stage_label = label or "Worked example"
        if topic and len(topic) <= 48:
            return f"{stage_label}: {topic}"
        return stage_label

    if stage == "practice":
        stage_label = label or "Practice"
        # Prefer a short topic/code tag when available — never the prompt.
        code_match = _SYLLABUS_CODE_IN_TEXT.search(question)
        if code_match:
            return f"{stage_label} · {code_match.group(1)}"
        if topic and len(topic) <= 48:
            return f"{stage_label}: {topic}"
        return stage_label

    # Unknown stages: keep short — never concatenate a long prompt into H2.
    stage_label = label or "Learning activity"
    if question and len(question) <= 64 and "\n" not in question:
        return f"{stage_label}: {question}" if label else question
    if topic and len(topic) <= 48:
        return f"{stage_label}: {topic}"
    return stage_label


def _context_eyebrow(subject_code: str, topic: str) -> str:
    """One muted eyebrow line: ``CS1 · Topic`` (omit empty parts)."""
    code = (subject_code or "").strip()
    title = (topic or "").strip()
    if code and title and title.lower() != code.lower():
        return f"{code} · {title}"
    return code or title


def _compact_duration_label(label: str) -> str:
    """Compact duration for Overview meta line, e.g. ``30 min``."""
    text = (label or "").strip()
    if not text:
        return ""
    if text.lower().startswith("about "):
        text = text[6:].strip()
    text = (
        text.replace(" minutes", " min")
        .replace(" minute", " min")
        .replace("Minutes", "min")
        .replace("Minute", "min")
    )
    return text


def _meta_mode_label(surface: SessionSurface, page: SessionPageViewModel) -> str:
    """Second essential meta fact — mode / stage, not a third chip."""
    if surface is SessionSurface.OVERVIEW:
        return "Learning"
    if surface is SessionSurface.ACTIVITY and page.activity:
        stage = (page.activity.stage_label or page.activity.activity_type or "").strip()
        if stage:
            # Title-case short stage names; keep existing casing if already phrased.
            if stage.islower() or "_" in stage:
                return stage.replace("_", " ").title()
            return stage
        return "Learning"
    if surface is SessionSurface.REFLECTION:
        return "Reflection"
    if surface in {SessionSurface.SUMMARY, SessionSurface.COMPLETE}:
        return "Summary"
    return "Learning"


def _prior_reflection_excerpt_for_overview(page: SessionPageViewModel) -> str:
    """Resurface the student's own prior note for this topic (Tier A).

    Best-effort: failures never break Overview. Truncates like Sitting Report
    (120 chars). Does not overwrite authored ``reflection_preview``.
    """
    try:
        from app.infrastructure.adapters.learning_session.persistence import (
            LearningSessionPersistenceAdapter,
        )
        from app.presentation.session.factory import (
            get_session_experience_composition,
        )

        composition = get_session_experience_composition()
        store = composition.store if composition is not None else None
        persistence = LearningSessionPersistenceAdapter(store=store)
        session_id = (page.shell.session_id or "").strip()
        student_id = (page.shell.student_id or "").strip()
        if not session_id or not student_id:
            return ""

        handle = persistence.load(session_id=session_id) or {}
        topic_id = str(handle.get("topic_id") or "").strip()
        mission_instance_id = str(
            handle.get("mission_instance_id") or ""
        ).strip()
        if not topic_id and mission_instance_id:
            try:
                from app.models.educational_runtime_engine import (
                    RuntimeMissionInstance,
                )

                row = RuntimeMissionInstance.query.filter_by(
                    mission_instance_id=mission_instance_id
                ).first()
                if row is not None:
                    topic_id = str(row.topic_id or "").strip()
            except Exception:  # noqa: BLE001 — optional topic resolution
                topic_id = ""
        if not topic_id:
            return ""

        note = persistence.find_prior_reflection_note(
            student_id=student_id,
            topic_id=topic_id,
            exclude_session_id=session_id,
        )
        if not note:
            return ""
        if len(note) <= 120:
            return note
        return f"{note[:117]}…"
    except Exception:  # noqa: BLE001 — briefing enrichment is best-effort
        return ""
