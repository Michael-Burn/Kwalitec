"""Study Session service — Persistent context / Learning Task / Practice.

Authority: DX-005C Focused Study Session.
Presentation projection only. Does not alter session, mission, or
question engines.
"""

from __future__ import annotations

from flask import url_for

from app.domain.session_experience.session_workspace import SessionSurface
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
        context = self._context(page, surface)
        task = self._task(page, surface)
        primary_label, primary_kind, primary_enabled, blocking = self._primary(
            page, surface
        )
        content = self._content(page, surface)
        disclosures = self._disclosures(page, surface)
        technical = self._technical(page)

        return StudySessionPage(
            page_title=_PAGE_TITLE,
            surface=surface.value,
            context=context,
            task=task,
            primary_label=primary_label,
            primary_kind=primary_kind,
            primary_enabled=primary_enabled,
            blocking_issue=blocking,
            exit_href=url_for("student.home"),
            exit_label="Exit",
            content_title=content["title"],
            content_body=content["body"],
            content_support=content["support"],
            answer_prompt=content["answer_prompt"],
            show_answer_input=content["show_answer_input"],
            feedback_outcome=content["feedback_outcome"],
            feedback_explanation=content["feedback_explanation"],
            disclosures=disclosures,
            technical_lines=technical,
            session_id=page.shell.session_id,
            activity_id=(page.activity.activity_id if page.activity else ""),
            mission_id=(page.overview.mission_id if page.overview else "") or "",
        )

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
            if page.overview.estimated_duration_label:
                elapsed = page.overview.estimated_duration_label
            if page.overview.topics:
                chapter = page.overview.topics[0]

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
            if page.activity and page.activity.context:
                objective = page.activity.context.strip()
            elif page.overview and page.overview.learning_goal:
                objective = page.overview.learning_goal.strip()
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
        self, page: SessionPageViewModel, surface: SessionSurface
    ) -> LearningTask:
        duration = ""
        next_milestone = ""
        expected = ""
        instruction = "Complete the current practice step."
        activity = "Practice"

        if surface is SessionSurface.OVERVIEW and page.overview:
            activity = "Begin practice"
            expected = page.overview.objective or "Start today's practice"
            duration = page.overview.estimated_duration_label
            next_milestone = page.overview.activity_count_label or "First activity"
            instruction = "Start the session to open the first learning activity."
            if page.overview.why_studying:
                # One concise line only — strip essay padding.
                why = page.overview.why_studying.strip()
                if why and len(why) <= 160:
                    instruction = why

        elif surface is SessionSurface.ACTIVITY and page.activity:
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
            else:
                activity = "Answer question"
                expected = "Submit your answer for this activity"
                instruction = "Read the question, write your answer, then submit."
                next_milestone = "Immediate feedback"
            if page.progress and page.progress.remaining_time_label:
                duration = page.progress.remaining_time_label

        elif surface is SessionSurface.REFLECTION and page.reflection:
            activity = "Session reflection"
            expected = "Capture what mattered in this practice"
            instruction = (
                page.reflection.reflection_prompt
                or "What mattered in this practice?"
            )
            next_milestone = "Return Home"
            if page.reflection.topic_title:
                expected = f"Reflect on {page.reflection.topic_title}"

        elif surface in {SessionSurface.SUMMARY, SessionSurface.COMPLETE}:
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
        self, page: SessionPageViewModel, surface: SessionSurface
    ) -> tuple[str, str, bool, str]:
        if surface is SessionSurface.OVERVIEW and page.overview:
            label = page.overview.begin_label or "Start Session"
            return label, "begin_form", page.overview.begin_enabled, ""

        if surface is SessionSurface.ACTIVITY and page.activity:
            if page.activity.has_explanation:
                label = page.activity.next_action_label or "Continue"
                return label, "advance_form", True, ""
            return "Submit Answer", "answer_form", True, ""

        if surface is SessionSurface.REFLECTION and page.reflection:
            label = page.reflection.next_action_label or "Continue to Summary"
            return label, "reflection_form", True, ""

        if surface in {SessionSurface.SUMMARY, SessionSurface.COMPLETE}:
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
        self, page: SessionPageViewModel, surface: SessionSurface
    ) -> dict[str, object]:
        empty = {
            "title": "",
            "body": "",
            "support": "",
            "answer_prompt": "Your answer",
            "show_answer_input": False,
            "feedback_outcome": "",
            "feedback_explanation": "",
        }

        if surface is SessionSurface.OVERVIEW and page.overview:
            body_parts = []
            if page.overview.objective:
                body_parts.append(page.overview.objective)
            return {
                **empty,
                "title": "Current objective",
                "body": " ".join(body_parts),
                "support": "",
            }

        if surface is SessionSurface.ACTIVITY and page.activity:
            act = page.activity
            feedback_outcome = ""
            feedback_explanation = ""
            if act.has_explanation:
                feedback_outcome = "Reviewed"
                feedback_explanation = act.explanation or ""
            return {
                "title": act.question or "Learning activity",
                "body": act.context or "",
                "support": act.supporting_material or "",
                "answer_prompt": act.answer_prompt or "Your answer",
                "show_answer_input": not act.has_explanation,
                "feedback_outcome": feedback_outcome,
                "feedback_explanation": feedback_explanation,
            }

        if surface is SessionSurface.REFLECTION and page.reflection:
            body = page.reflection.reflection_prompt or ""
            support = ""
            if page.reflection.key_insight:
                support = page.reflection.key_insight
            return {
                **empty,
                "title": "Reflection",
                "body": body,
                "support": support,
            }

        if surface in {SessionSurface.SUMMARY, SessionSurface.COMPLETE}:
            topic = ""
            if page.completion and page.completion.primary_topic:
                topic = page.completion.primary_topic
            body = "Session practice complete."
            if topic:
                body = f"Session practice on {topic} is complete."
            return {**empty, "title": "Session complete", "body": body}

        return empty

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

    def _technical(self, page: SessionPageViewModel) -> tuple[str, ...]:
        lines = [f"Session ID · {page.shell.session_id}"]
        if page.activity and page.activity.activity_id:
            lines.append(f"Activity ID · {page.activity.activity_id}")
        if page.overview and page.overview.mission_id:
            lines.append(f"Mission ID · {page.overview.mission_id}")
        return tuple(lines)
