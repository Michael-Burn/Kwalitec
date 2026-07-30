"""Student Home service — SOP-001 command centre projection.

Authority: SOP-001 Student Operating System + DX-005A Mission selection.
Presentation projection only. Does not alter learning, recommendation, or
session engines.
"""

from __future__ import annotations

from flask import url_for

from app.presentation.student.dto.student_home import (
    HomeDeadline,
    HomeExamination,
    HomeMission,
    HomeQueueRow,
    HomeQuickAction,
    HomeStudyHealth,
    HomeStudySignals,
    StudentHomePage,
)
from app.presentation.student.view_models import (
    HomePageViewModel,
    JourneyPageViewModel,
    ProfilePageViewModel,
    RevisionPageViewModel,
    StudentPageViewModel,
)

_QUEUE_MAX = 5
_QUICK_ACTION_MAX = 3
_DEADLINE_MAX = 4

_EMPTY_REASON = "No exam selected yet. Choose an exam to begin studying."
_EMPTY_ACTION_LABEL = "Choose Exam"
_DAY_COMPLETE_MESSAGE = "Today's mission is finished. Return tomorrow to continue."
_QUIET_REASON = "A session will be ready when today's mission is available."


class StudentHomeService:
    """Build the SOP-001 Student Home command centre from experience VMs."""

    def build_home(
        self,
        page: StudentPageViewModel | None,
        *,
        show_revision_acknowledgement: bool = False,
        revision_ack_title: str = "",
        revision_ack_body: str = "",
    ) -> StudentHomePage:
        """Assemble command-centre sections from existing Experience VMs."""
        choose_exam_href = url_for("study_plan.index")
        if page is None or page.home is None:
            return StudentHomePage(
                mission=None,
                learning_queue=(),
                recent_progress=(),
                examination=None,
                study_health=None,
                quick_actions=(
                    HomeQuickAction(
                        label=_EMPTY_ACTION_LABEL,
                        href=choose_exam_href,
                        detail="Begin by selecting your examination",
                    ),
                ),
                deadlines=(),
                state="empty",
                empty_reason=_EMPTY_REASON,
                empty_action_label=_EMPTY_ACTION_LABEL,
                empty_action_href=choose_exam_href,
            )

        home = page.home
        revision = page.revision
        queue = self._learning_queue(home, revision=revision)
        examination = self._examination(home)
        study_health = self._study_health(home)
        signals = self._study_signals(
            home,
            examination=examination,
            journey=page.journey,
            profile=page.profile,
        )
        # Exam countdown lives in the signal strip — avoid a duplicate widget.
        deadlines = self._deadlines(
            home,
            omit_exam_countdown=bool(
                signals and (signals.countdown_label or "").strip()
            ),
        )
        # History owns session archives — do not mirror Recent Progress on Home.
        recent: tuple[HomeQueueRow, ...] = ()

        if show_revision_acknowledgement:
            mission = self._revision_ack_mission(
                home,
                title=revision_ack_title,
                body=revision_ack_body,
            )
            return self._assemble(
                mission=mission,
                queue=queue,
                recent=recent,
                examination=examination,
                study_health=study_health,
                deadlines=deadlines,
                signals=signals,
                state="mission",
                home=home,
                revision=revision,
            )

        if home.day_complete or (
            home.unified_journey_enabled
            and home.completion_status == "complete"
            and not home.primary_cta_enabled
            and home.session_control != "resume"
        ):
            subject = self._subject_name(home)
            mission = HomeMission(
                subject_name=subject or "Today's study",
                objective="Complete for today",
                status_label="Complete for today",
                why_now="",
                after_completion="",
                primary_label="",
                primary_kind="none",
                title="Complete for today",
            )
            return self._assemble(
                mission=mission,
                queue=queue,
                recent=recent,
                examination=examination,
                study_health=study_health,
                deadlines=deadlines,
                signals=signals,
                state="day_complete",
                home=home,
                revision=revision,
                day_complete_message=_DAY_COMPLETE_MESSAGE,
            )

        mission = self._select_mission(home)
        if mission is not None:
            cleaned_queue = self._queue_without_l0_duplicate(queue, mission)
            return self._assemble(
                mission=mission,
                queue=cleaned_queue,
                recent=recent,
                examination=examination,
                study_health=study_health,
                deadlines=deadlines,
                signals=signals,
                state="mission",
                home=home,
                revision=revision,
            )

        if self._has_study_plan_signal(home):
            return self._assemble(
                mission=None,
                queue=queue,
                recent=recent,
                examination=examination,
                study_health=study_health,
                deadlines=deadlines,
                signals=signals,
                state="quiet",
                home=home,
                revision=revision,
                empty_reason=_QUIET_REASON,
                empty_action_label=_EMPTY_ACTION_LABEL,
                empty_action_href=choose_exam_href,
            )

        return self._assemble(
            mission=None,
            queue=(),
            recent=recent,
            examination=examination,
            study_health=study_health,
            deadlines=deadlines,
            signals=signals,
            state="empty",
            home=home,
            revision=revision,
            empty_reason=_EMPTY_REASON,
            empty_action_label=_EMPTY_ACTION_LABEL,
            empty_action_href=choose_exam_href,
            force_choose_exam_action=True,
        )

    def _assemble(
        self,
        *,
        mission: HomeMission | None,
        queue: tuple[HomeQueueRow, ...],
        recent: tuple[HomeQueueRow, ...],
        examination: HomeExamination | None,
        study_health: HomeStudyHealth | None,
        deadlines: tuple[HomeDeadline, ...],
        state: str,
        home: HomePageViewModel,
        revision: RevisionPageViewModel | None,
        empty_reason: str = "",
        empty_action_label: str = "",
        empty_action_href: str = "",
        day_complete_message: str = "",
        force_choose_exam_action: bool = False,
        signals: HomeStudySignals | None = None,
    ) -> StudentHomePage:
        section_title = self._mission_section_title(mission)
        quick_actions = self._quick_actions(
            home,
            revision=revision,
            queue=queue,
            mission=mission,
            state=state,
            force_choose_exam=force_choose_exam_action or state in {"empty", "quiet"},
        )
        tutor_available = bool(home.tutor_available)
        tutor_href = ""
        if tutor_available or state == "mission":
            tutor_href = url_for("student.tutor")
        return StudentHomePage(
            mission=mission,
            learning_queue=queue,
            recent_progress=recent,
            examination=examination,
            study_health=study_health,
            quick_actions=quick_actions,
            deadlines=deadlines,
            state=state,
            empty_reason=empty_reason,
            empty_action_label=empty_action_label,
            empty_action_href=empty_action_href,
            day_complete_message=day_complete_message,
            mission_section_title=section_title,
            signals=signals,
            tutor_available=tutor_available,
            tutor_href=tutor_href,
        )

    @staticmethod
    def _mission_section_title(mission: HomeMission | None) -> str:
        if mission is None:
            return "Today's Mission"
        if mission.primary_kind == "link":
            return "Continue Session"
        if mission.primary_kind == "revision_ack":
            return "Today's Mission"
        return "Today's Mission"

    def _select_mission(self, home: HomePageViewModel) -> HomeMission | None:
        """Selection algorithm per DX-005A Architecture §5 (unchanged)."""
        subject = self._subject_name(home)
        objective = self._objective(home)
        title = self._mission_title(home, objective=objective)
        why_now = self._why_now(home)
        after = self._after_completion(home)
        difficulty = self._difficulty_label(home)
        duration = (
            home.estimated_duration_label or home.estimated_study_label or ""
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
                primary_href=url_for("session.overview", session_id=session_id),
                duration_label=duration,
                mission_id=mission_id,
                session_id=session_id,
                recommendation_key=rec_key,
                title=title or "Continue Session",
                difficulty_label=difficulty,
                learning_objective=objective or "Continue your open session",
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
                primary_href=url_for("session.overview", session_id=session_id),
                duration_label=duration,
                mission_id=mission_id,
                session_id=session_id,
                recommendation_key=rec_key,
                title=title or "Finish Session",
                difficulty_label=difficulty,
                learning_objective=objective or "Wrap up your open session",
            )

        # 2a. Runtime C mission ready → Mark mission complete (PR-001B).
        # session_control is complete_runtime_c — not a Guided Session start.
        if (
            home.primary_cta_enabled
            and home.session_control == "complete_runtime_c"
            and mission_id
        ):
            label = (
                home.session_control_label
                or home.primary_cta_label
                or "Mark mission complete"
            ).strip()
            return HomeMission(
                subject_name=subject or "Current subject",
                objective=objective or "Today's study focus",
                status_label=self._status_line(
                    home.completion_status_label or home.session_status or "Ready",
                    duration,
                ),
                why_now=why_now,
                after_completion=after,
                primary_label=label,
                primary_kind="complete_runtime_c",
                duration_label=duration,
                mission_id=mission_id,
                session_id=session_id,
                recommendation_key=rec_key,
                title=title or objective or "Today's Mission",
                difficulty_label=difficulty,
                learning_objective=objective or "Today's study focus",
            )

        # 2–3. Mission ready → Start Session (POST preserves commitment path).
        if home.primary_cta_enabled and (
            home.session_control in ("start", "resume", "") or not home.session_control
        ):
            label = self._start_primary_label(home)
            if not subject and not objective:
                return None
            return HomeMission(
                subject_name=subject or "Current subject",
                objective=objective or "Today's study focus",
                status_label=self._status_line(
                    home.completion_status_label or home.session_status or "Ready",
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
                title=title or objective or "Today's Mission",
                difficulty_label=difficulty,
                learning_objective=objective or "Today's study focus",
            )

        return None

    def _study_signals(
        self,
        home: HomePageViewModel,
        *,
        examination: HomeExamination | None,
        journey: JourneyPageViewModel | None,
        profile: ProfilePageViewModel | None,
    ) -> HomeStudySignals | None:
        """Compact orientation strip — no duplicate exam/deadline widgets."""
        subject = ""
        if examination and examination.label:
            subject = examination.label
        else:
            subject = self._subject_name(home)
        if not subject and not self._has_study_plan_signal(home):
            return None

        streak = ""
        if profile and (profile.streak_label or "").strip():
            streak = profile.streak_label.strip()
            if streak == "0 days":
                streak = "No streak yet"
            elif not streak.lower().endswith("streak"):
                streak = f"{streak} streak"

        progress_label = ""
        progress_percent: int | None = None
        if journey is not None and journey.progress_percent is not None:
            progress_percent = int(journey.progress_percent)
            progress_label = (
                journey.progress_label
                or f"{progress_percent}% complete"
            ).strip()
        elif home.educational and getattr(home.educational, "active", False):
            progress_percent = int(home.educational.progress_percent or 0)
            progress_label = (
                home.educational.progress_label
                or home.educational.coverage_label
                or f"{progress_percent}% complete"
            ).strip()
        elif home.readiness and home.readiness.has_readiness:
            raw = (
                home.readiness.readiness_percent_label
                or home.readiness.readiness_label
                or ""
            ).strip()
            if raw:
                progress_label = raw

        countdown = ""
        if examination and examination.countdown_label:
            countdown = examination.countdown_label
        elif home.countdown and home.countdown.has_countdown:
            countdown = (
                home.countdown.label
                or (
                    f"{home.countdown.days} days"
                    if home.countdown.days is not None
                    else ""
                )
            ).strip()

        estimated = (
            home.estimated_duration_label or home.estimated_study_label or ""
        ).strip()

        if not any(
            (subject, streak, progress_label, countdown, estimated)
        ):
            return None
        return HomeStudySignals(
            subject_label=subject,
            streak_label=streak,
            progress_label=progress_label,
            progress_percent=progress_percent,
            countdown_label=countdown,
            estimated_study_label=estimated,
        )

    @staticmethod
    def _mission_title(home: HomePageViewModel, *, objective: str) -> str:
        edu = home.educational
        if edu and getattr(edu, "active", False):
            title = (edu.mission_title or edu.today_topic_title or "").strip()
            if title:
                return title
        if home.primary_mission_title:
            return home.primary_mission_title.strip()
        if home.recommendation and home.recommendation.title:
            return home.recommendation.title.strip()
        if home.start_session and home.start_session.topic_title:
            return home.start_session.topic_title.strip()
        return (objective or "").strip()

    @staticmethod
    def _difficulty_label(home: HomePageViewModel) -> str:
        mi = home.mission_intelligence
        if mi is not None:
            for attr in ("difficulty_label", "difficulty", "mission_difficulty"):
                raw = getattr(mi, attr, None)
                if isinstance(raw, str) and raw.strip():
                    return raw.strip()[:40]
        edu = home.educational
        if edu and getattr(edu, "active", False):
            for attr in ("difficulty_label", "feasibility_label"):
                raw = getattr(edu, attr, None)
                if isinstance(raw, str) and raw.strip():
                    return raw.strip()[:40]
        return ""

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

    def _examination(self, home: HomePageViewModel) -> HomeExamination | None:
        label = (home.examination_label or "").strip()
        if not label:
            edu = home.educational
            if edu and getattr(edu, "active", False):
                label = (edu.examination_label or "").strip() or (
                    edu.subject_code or ""
                ).strip()
        if not label:
            return None
        countdown = ""
        if home.countdown and home.countdown.has_countdown:
            countdown = (
                home.countdown.label
                or (
                    f"{home.countdown.days} days"
                    if home.countdown.days is not None
                    else ""
                )
            ).strip()
        detail = ""
        if home.educational and getattr(home.educational, "active", False):
            section = (home.educational.section_title or "").strip()
            position = (home.educational.position_label or "").strip()
            if section or position:
                detail = " · ".join(p for p in (section, position) if p)
        return HomeExamination(
            label=label,
            countdown_label=countdown,
            detail=detail,
        )

    def _study_health(self, home: HomePageViewModel) -> HomeStudyHealth | None:
        """Single calm line — never a multi-KPI analytics wall."""
        readiness = home.readiness
        if readiness and readiness.has_readiness:
            status = (
                readiness.readiness_label
                or readiness.readiness_percent_label
                or "On track"
            ).strip()
            detail_parts: list[str] = []
            if readiness.trend_label:
                detail_parts.append(readiness.trend_label)
            if readiness.suggested_next_action:
                detail_parts.append(readiness.suggested_next_action[:100])
            tone = "neutral"
            lowered = (readiness.trend_label or "").lower()
            if any(w in lowered for w in ("up", "improv", "gain", "strong")):
                tone = "positive"
            elif any(w in lowered for w in ("down", "declin", "weak", "risk")):
                tone = "caution"
            return HomeStudyHealth(
                status_label=status,
                detail=" · ".join(detail_parts),
                tone=tone,
            )
        if home.day_complete:
            return HomeStudyHealth(
                status_label="Day complete",
                detail="Rest — return tomorrow for the next mission.",
                tone="positive",
            )
        if self._has_study_plan_signal(home):
            return HomeStudyHealth(
                status_label="Building evidence",
                detail="Complete today's mission to strengthen your readiness signal.",
                tone="neutral",
            )
        return None

    def _deadlines(
        self,
        home: HomePageViewModel,
        *,
        omit_exam_countdown: bool = False,
    ) -> tuple[HomeDeadline, ...]:
        rows: list[HomeDeadline] = []
        if (
            not omit_exam_countdown
            and home.countdown
            and home.countdown.has_countdown
        ):
            title = home.countdown.examination_label or home.examination_label
            label = home.countdown.label or (
                f"{home.countdown.days} days"
                if home.countdown.days is not None
                else "Upcoming exam"
            )
            rows.append(
                HomeDeadline(
                    title=(title or "Examination").strip(),
                    detail=label.strip(),
                )
            )
        for milestone in (home.milestones or ())[:_DEADLINE_MAX]:
            title = (milestone.title or "").strip()
            if not title:
                continue
            rows.append(
                HomeDeadline(
                    title=title,
                    detail=(milestone.detail or "").strip(),
                )
            )
        # Deduplicate by title, preserve order.
        seen: set[str] = set()
        unique: list[HomeDeadline] = []
        for row in rows:
            key = row.title.lower()
            if key in seen:
                continue
            seen.add(key)
            unique.append(row)
        return tuple(unique[:_DEADLINE_MAX])

    def _quick_actions(
        self,
        home: HomePageViewModel,
        *,
        revision: RevisionPageViewModel | None,
        queue: tuple[HomeQueueRow, ...],
        mission: HomeMission | None,
        state: str,
        force_choose_exam: bool,
    ) -> tuple[HomeQuickAction, ...]:
        """Contextual actions only — never a shell-nav duplicate wall."""
        actions: list[HomeQuickAction] = []
        choose_exam_href = url_for("study_plan.index")

        if force_choose_exam or state == "empty":
            actions.append(
                HomeQuickAction(
                    label=_EMPTY_ACTION_LABEL,
                    href=choose_exam_href,
                    detail="Select an examination to unlock today's mission",
                )
            )
            return tuple(actions[:_QUICK_ACTION_MAX])

        for row in queue:
            if not row.href:
                continue
            if (
                mission
                and mission.primary_kind == "link"
                and row.title == ("Resume Session")
            ):
                continue
            actions.append(
                HomeQuickAction(
                    label=row.title,
                    href=row.href,
                    detail=(row.status_label or row.meta_label or "").strip(),
                )
            )

        if (
            revision is not None
            and revision.has_revision
            and revision.primary is not None
            and not any(a.label == "Revision Due" for a in actions)
            and (mission is None or mission.primary_kind != "link")
        ):
            focus = revision.primary.topic_title or "Supporting revision"
            actions.append(
                HomeQuickAction(
                    label="Revision Due",
                    href=url_for("student.revision"),
                    detail=focus,
                )
            )

        if state == "quiet":
            actions.append(
                HomeQuickAction(
                    label=_EMPTY_ACTION_LABEL,
                    href=choose_exam_href,
                    detail="Adjust exam selection if your plan feels stuck",
                )
            )

        # UX-001 — contextual Tutor / Knowledge Map without cloning shell nav.
        if state == "mission" and len(actions) < _QUICK_ACTION_MAX:
            if not any(a.label == "Ask Tutor" for a in actions):
                actions.append(
                    HomeQuickAction(
                        label="Ask Tutor",
                        href=url_for("student.tutor"),
                        detail="Why this mission was chosen",
                    )
                )
        if state in {"mission", "quiet", "day_complete"} and len(actions) < _QUICK_ACTION_MAX:
            if not any(a.label == "Knowledge Map" for a in actions):
                actions.append(
                    HomeQuickAction(
                        label="Knowledge Map",
                        href=url_for("student.knowledge_graph"),
                        detail="See your syllabus hierarchy",
                    )
                )

        return tuple(actions[:_QUICK_ACTION_MAX])

    def _learning_queue(
        self,
        home: HomePageViewModel,
        *,
        revision: RevisionPageViewModel | None,
    ) -> tuple[HomeQueueRow, ...]:
        """Attention-only rows — max 5; never history or motivation."""
        rows: list[HomeQueueRow] = []

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
                    href=url_for("session.overview", session_id=home.session_id),
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
                    home.recommendation.reason or home.recommendation.summary or ""
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
            home.session_control_label or home.primary_cta_label or "Start Session"
        ).strip()
        lowered = raw.lower()
        if "continue" in lowered and "session" not in lowered:
            return "Continue Session"
        if lowered in {"start", "resume", "begin"}:
            return "Start Session"
        if "resume mission" in lowered:
            return "Resume Mission"
        if "start session" in lowered or "resume" in lowered:
            return (
                raw
                if "session" in lowered or "mission" in lowered
                else ("Start Session")
            )
        if raw in {"Start Today's Session", "Start", "Begin"}:
            return "Start Session"
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
        """True when the learner has an active study context."""
        topic = ""
        if home.start_session:
            topic = (home.start_session.topic_title or "").strip()
        return bool(
            home.examination_label
            or (home.recommendation and home.recommendation.has_recommendation)
            or topic
            or home.unified_journey_enabled
            or (home.educational and getattr(home.educational, "active", False))
        )
