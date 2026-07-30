"""UX-001 — Student Tutor presentation (no new educational reasoning).

Projects existing Intelligent Tutor + certified curriculum context onto a
minimal student surface. Soft-fails when Twin / package is unavailable.
"""

from __future__ import annotations

from dataclasses import dataclass

from flask import url_for


@dataclass(frozen=True)
class TutorCitation:
    label: str
    detail: str = ""


@dataclass(frozen=True)
class StudentTutorPage:
    page_title: str
    page_question: str
    topic_title: str
    learning_objective: str
    certified_source: str
    conversation_context: str
    explanation_summary: str
    suggested_next_action: str
    citations: tuple[TutorCitation, ...]
    can_explain: bool
    empty_reason: str
    empty_action_label: str
    empty_action_href: str
    loading_hint: str
    error_message: str
    home_href: str
    mission_id: str


class StudentTutorPresentationService:
    """Assemble Tutor UI from existing Home VM + optional Tutor response."""

    def build(
        self,
        page,
        *,
        explanation_summary: str = "",
        suggested_next_action: str = "",
        error_message: str = "",
        citations: tuple[TutorCitation, ...] = (),
        certified_source: str = "",
    ) -> StudentTutorPage:
        home = getattr(page, "home", None) if page is not None else None
        topic = ""
        objective = ""
        mission_id = ""
        context = ""
        if home is not None:
            mission_id = (home.mission_id or "").strip()
            topic = (
                (home.primary_mission_title or "").strip()
                or (
                    home.recommendation.title
                    if home.recommendation and home.recommendation.title
                    else ""
                )
                or (
                    (home.start_session.topic_title or "").strip()
                    if home.start_session
                    else ""
                )
            )
            objective = (home.session_learning_objective or topic).strip()
            edu = home.educational
            if edu and getattr(edu, "active", False):
                topic = (edu.today_topic_title or edu.mission_title or topic).strip()
                if edu.learning_objectives:
                    objective = edu.learning_objectives[0]
                if not certified_source:
                    code = (edu.subject_code or "").strip()
                    label = (edu.examination_label or "").strip()
                    certified_source = (
                        f"Certified curriculum · {code or label}".strip(" ·")
                    )
            if home.tutor_guidance:
                context = home.tutor_guidance.strip()
            elif home.explanation and home.explanation.why_recommended:
                context = home.explanation.why_recommended.strip()
            elif home.why_it_matters:
                context = home.why_it_matters.strip()

        if not certified_source:
            if home and home.examination_label:
                certified_source = (
                    f"Published syllabus · {home.examination_label}"
                )
            else:
                certified_source = "Certified curriculum source unavailable"

        can_explain = bool(home and (home.mission_id or home.tutor_available or topic))
        empty_reason = ""
        empty_action = "Return Home"
        empty_href = url_for("student.home")
        if home is None or not topic:
            empty_reason = (
                "Tutor guidance appears once today's mission is available."
            )
            can_explain = False

        return StudentTutorPage(
            page_title="Tutor",
            page_question="Why this mission — and what should I understand?",
            topic_title=topic or "Today's topic",
            learning_objective=objective or "Complete today's learning objective",
            certified_source=certified_source,
            conversation_context=context,
            explanation_summary=(explanation_summary or "").strip(),
            suggested_next_action=(suggested_next_action or "").strip(),
            citations=citations,
            can_explain=can_explain,
            empty_reason=empty_reason,
            empty_action_label=empty_action,
            empty_action_href=empty_href,
            loading_hint="Preparing an evidence-backed explanation…",
            error_message=(error_message or "").strip(),
            home_href=empty_href,
            mission_id=mission_id,
        )
