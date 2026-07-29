"""Student Home service — Mission / Learning Queue / Recent Progress.

Authority: DX-005A Student Home Architecture.
Presentation projection only. Does not alter learning, recommendation, or
session engines.
"""

from __future__ import annotations

from flask import url_for

from app.presentation.student.dto.student_home import (
    HomeMission,
    HomeQueueRow,
    StudentHomePage,
)
from app.presentation.student.view_models import (
    HistoryPageViewModel,
    HomePageViewModel,
    RevisionPageViewModel,
    StudentPageViewModel,
)

_QUEUE_MAX = 5
_RECENT_MAX = 5

_EMPTY_REASON = "No exam selected yet. Choose an exam to begin studying."
_EMPTY_ACTION_LABEL = "Choose Exam"
_DAY_COMPLETE_MESSAGE = (
    "Today's mission is finished. Return tomorrow to continue."
)
_QUIET_REASON = (
    "A session will be ready when today's mission is available."
)


class StudentHomeService:
    """Build the DX-005A Student Home page from existing experience VMs."""

    def build_home(
        self,
        page: StudentPageViewModel | None,
        *,
        show_revision_acknowledgement: bool = False,
        revision_ack_title: str = "",
        revision_ack_body: str = "",
    ) -> StudentHomePage:
        """Assemble L0 Mission, L1 Queue, and L2 Recent Progress."""
        choose_exam_href = url_for("study_plan.index")
        if page is None or page.home is None:
            return StudentHomePage(
                mission=None,
                learning_queue=(),
                recent_progress=(),
                state="empty",
                empty_reason=_EMPTY_REASON,
                empty_action_label=_EMPTY_ACTION_LABEL,
                empty_action_href=choose_exam_href,
            )

        home = page.home
        history = page.history
        revision = page.revision
        recent = self._recent_progress(history)
        queue = self._learning_queue(home, revision=revision)

        if show_revision_acknowledgement:
            mission = self._revision_ack_mission(
                home,
                title=revision_ack_title,
                body=revision_ack_body,
            )
            return StudentHomePage(
                mission=mission,
                learning_queue=queue,
                recent_progress=recent,
                state="mission",
                empty_reason="",
                empty_action_label="",
                empty_action_href="",
            )

        if home.day_complete or (
            home.unified_journey_enabled
            and home.completion_status == "complete"
            and not home.primary_cta_enabled
            and home.session_control != "resume"
        ):
            subject = self._subject_name(home)
            return StudentHomePage(
                mission=HomeMission(
                    subject_name=subject or "Today's study",
                    objective="Complete for today",
                    status_label="Complete for today",
                    why_now="",
                    after_completion="",
                    primary_label="",
                    primary_kind="none",
                ),
                learning_queue=queue,
                recent_progress=recent,
                state="day_complete",
                empty_reason="",
                empty_action_label="",
                empty_action_href="",
                day_complete_message=_DAY_COMPLETE_MESSAGE,
            )

        mission = self._select_mission(home)
        if mission is not None:
            return StudentHomePage(
                mission=mission,
                learning_queue=self._queue_without_l0_duplicate(queue, mission),
                recent_progress=recent,
                state="mission",
                empty_reason="",
                empty_action_label="",
                empty_action_href="",
            )

        if self._has_study_plan_signal(home):
            return StudentHomePage(
                mission=None,
                learning_queue=queue,
                recent_progress=recent,
                state="quiet",
                empty_reason=_QUIET_REASON,
                empty_action_label=_EMPTY_ACTION_LABEL,
                empty_action_href=choose_exam_href,
            )

        return StudentHomePage(
            mission=None,
            learning_queue=(),
            recent_progress=recent,
            state="empty",
            empty_reason=_EMPTY_REASON,
            empty_action_label=_EMPTY_ACTION_LABEL,
            empty_action_href=choose_exam_href,
        )

    def _select_mission(self, home: HomePageViewModel) -> HomeMission | None:
        """Selection algorithm per DX-005A Architecture §5."""
        subject = self._subject_name(home)
        objective = self._objective(home)
        why_now = self._why_now(home)
        after = self._after_completion(home)
        duration = (
            home.estimated_duration_label
            or home.estimated_study_label
            or ""
        ).strip()
        mission_id = (home.mission_id or "").strip()
        session_id = (home.session_id or "").strip()
        rec_key = ""
        if home.commitment and home.commitment.recommendation_key:
            rec_key = home.commitment.recommendation_key

        # 1. Open session → Continue Session (deep link, no re-commit).
        if home.session_control == "resume" and session_id:
            return HomeMission(
                subject_name=subject or "Current subject",
                objective=objective or "Continue your open session",
                status_label=self._status_line("In progress", duration),
                why_now=why_now or "Open session — continue where you left off",
                after_completion=after,
                primary_label="Continue Session",
                primary_kind="link",
                primary_href=url_for(
                    "session.overview", session_id=session_id
                ),
                duration_label=duration,
                mission_id=mission_id,
                session_id=session_id,
                recommendation_key=rec_key,
            )

        if (
            home.guided_session_active
            and home.session_control == "finish"
            and session_id
        ):
            return HomeMission(
                subject_name=subject or "Current subject",
                objective=objective or "Wrap up your open session",
                status_label=self._status_line("In progress", duration),
                why_now=why_now or "Open session — finish and record progress",
                after_completion=after,
                primary_label="Continue Session",
                primary_kind="link",
                primary_href=url_for(
                    "session.overview", session_id=session_id
                ),
                duration_label=duration,
                mission_id=mission_id,
                session_id=session_id,
                recommendation_key=rec_key,
            )

        # 2–3. Mission ready → Start Session (POST preserves commitment path).
        if home.primary_cta_enabled and (
            home.session_control in ("start", "resume", "")
            or not home.session_control
        ):
            label = self._start_primary_label(home)
            if not subject and not objective:
                return None
            return HomeMission(
                subject_name=subject or "Current subject",
                objective=objective or "Today's study focus",
                status_label=self._status_line(
                    home.completion_status_label
                    or home.session_status
                    or "Ready",
                    duration,
                ),
                why_now=why_now,
                after_completion=after,
                primary_label=label,
                primary_kind="start_form",
                duration_label=duration,
                mission_id=mission_id,
                session_id=session_id,
                recommendation_key=rec_key,
            )

        return None

    def _revision_ack_mission(
        self,
        home: HomePageViewModel,
        *,
        title: str,
        body: str,
    ) -> HomeMission:
        subject = self._subject_name(home) or "Syllabus"
        objective = (title or "Syllabus complete").strip()
        why = (body or "Acknowledge syllabus completion to continue.").strip()
        if len(why) > 140:
            why = why[:137].rstrip() + "…"
        return HomeMission(
            subject_name=subject,
            objective=objective,
            status_label="Ready",
            why_now=why,
            after_completion="Returns you to today's focus mission.",
            primary_label="Continue",
            primary_kind="revision_ack",
            mission_id=(home.mission_id or "").strip(),
            session_id=(home.session_id or "").strip(),
        )

    def _learning_queue(
        self,
        home: HomePageViewModel,
        *,
        revision: RevisionPageViewModel | None,
    ) -> tuple[HomeQueueRow, ...]:
        """Attention-only rows — max 5; never history or motivation."""
        rows: list[HomeQueueRow] = []

        # Open session already owns L0 when resume — skip duplicate Resume row.
        if (
            home.session_control == "resume"
            and home.session_id
            and not home.primary_cta_enabled
        ):
            rows.append(
                HomeQueueRow(
                    title="Resume Session",
                    status_label=self._subject_name(home),
                    meta_label=self._objective(home),
                    href=url_for(
                        "session.overview", session_id=home.session_id
                    ),
                )
            )

        if (
            revision is not None
            and revision.has_revision
            and revision.primary is not None
            and home.session_control != "resume"
        ):
            focus = revision.primary.topic_title or "Supporting revision"
            subject = self._subject_name(home)
            meta = f"{subject} · {focus}" if subject else focus
            rows.append(
                HomeQueueRow(
                    title="Revision Due",
                    status_label=meta,
                    href=url_for("student.revision"),
                )
            )

        return tuple(rows[:_QUEUE_MAX])

    @staticmethod
    def _queue_without_l0_duplicate(
        queue: tuple[HomeQueueRow, ...],
        mission: HomeMission,
    ) -> tuple[HomeQueueRow, ...]:
        """Omit Resume Session queue row when L0 already Continues Session."""
        if mission.primary_kind != "link":
            return queue
        return tuple(r for r in queue if r.title != "Resume Session")

    def _recent_progress(
        self,
        history: HistoryPageViewModel | None,
    ) -> tuple[HomeQueueRow, ...]:
        if history is None or not history.sessions:
            return ()
        rows: list[HomeQueueRow] = []
        for session in history.sessions[:_RECENT_MAX]:
            title = session.topic_title or "Session"
            activity = session.outcome_label or "Session"
            rows.append(
                HomeQueueRow(
                    title=f"{activity} · {title}",
                    meta_label=session.completed_at or "",
                    href=(
                        url_for(
                            "session.overview", session_id=session.session_id
                        )
                        if session.session_id
                        else url_for("student.history")
                    ),
                )
            )
        return tuple(rows)

    @staticmethod
    def _subject_name(home: HomePageViewModel) -> str:
        return (
            (home.examination_label or "").strip()
            or (home.primary_mission_title or "").strip()
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

    @staticmethod
    def _objective(home: HomePageViewModel) -> str:
        return (
            (home.session_learning_objective or "").strip()
            or (
                home.recommendation.title
                if home.recommendation and home.recommendation.title
                else ""
            )
            or (home.primary_mission_title or "").strip()
            or (
                (home.start_session.topic_title or "").strip()
                if home.start_session
                else ""
            )
        )

    @staticmethod
    def _why_now(home: HomePageViewModel) -> str:
        """Exactly one operational why-now line (≤140 chars preferred)."""
        candidates: list[str] = []
        if home.session_control == "resume":
            candidates.append("Open session — continue where you left off")
        if home.explanation and home.explanation.timeliness_line:
            candidates.append(home.explanation.timeliness_line.strip())
        if home.explanation and home.explanation.why_recommended:
            candidates.append(home.explanation.why_recommended.strip())
        if home.why_it_matters:
            candidates.append(home.why_it_matters.strip())
        if home.recommendation and (
            home.recommendation.reason or home.recommendation.summary
        ):
            candidates.append(
                (
                    home.recommendation.reason
                    or home.recommendation.summary
                    or ""
                ).strip()
            )
        for line in candidates:
            if line:
                return line[:140]
        return ""

    @staticmethod
    def _after_completion(home: HomePageViewModel) -> str:
        mi = home.mission_intelligence
        if mi is not None:
            after = getattr(mi, "what_happens_after_completion", "") or ""
            if after.strip():
                return after.strip()[:140]
        if home.expected_outcome:
            return home.expected_outcome.strip()[:140]
        if home.explanation and home.explanation.suggested_next_action:
            return home.explanation.suggested_next_action.strip()[:140]
        if home.session_next_step:
            return home.session_next_step.strip()[:140]
        return ""

    @staticmethod
    def _start_primary_label(home: HomePageViewModel) -> str:
        raw = (
            home.session_control_label
            or home.primary_cta_label
            or "Start Session"
        ).strip()
        lowered = raw.lower()
        if "continue" in lowered and "session" not in lowered:
            return "Continue Session"
        if lowered in {"start", "resume", "begin"}:
            return "Start Session"
        if "resume mission" in lowered:
            return "Resume Mission"
        if "start session" in lowered or "resume" in lowered:
            return raw if "session" in lowered or "mission" in lowered else (
                "Start Session"
            )
        if raw in {"Start Today's Session", "Start", "Begin"}:
            return "Start Session"
        # Prefer DX-005A vocabulary when legacy label is generic.
        if lowered == "continue":
            return "Continue Session"
        return raw if raw else "Start Session"

    @staticmethod
    def _status_line(status: str, duration: str) -> str:
        status = (status or "").strip() or "Ready"
        duration = (duration or "").strip()
        if duration:
            return f"{status} · {duration}"
        return status

    @staticmethod
    def _has_study_plan_signal(home: HomePageViewModel) -> bool:
        """True when the learner has an active study context.

        Canonical signals: examination label (Study Plan / Twin), today's
        recommendation (or mission topic title), Unified Journey, or Runtime C
        educational enrolment.

        Do not treat bare demo ``mission_id`` / ``session_id`` stubs alone as
        proof of an active plan — those can exist without an exam selection.
        """
        topic = ""
        if home.start_session:
            topic = (home.start_session.topic_title or "").strip()
        return bool(
            home.examination_label
            or (
                home.recommendation and home.recommendation.has_recommendation
            )
            or topic
            or home.unified_journey_enabled
            or (home.educational and getattr(home.educational, "active", False))
        )
