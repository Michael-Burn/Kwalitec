"""Student Home service — SOP-001 command centre + KWP-013 workspace.

Authority: SOP-001 Student Operating System + DX-005A Mission selection +
KWP-013 Adaptive Study Workspace.
Presentation projection only. Does not alter learning, recommendation, or
session engines.
"""

from __future__ import annotations

from flask import url_for

from app.presentation.student.adaptive_workspace import (
    compose_adaptive_workspace,
    home_continuity_line,
)
from app.presentation.student.dto.student_home import (
    HomeBriefingSection,
    HomeDeadline,
    HomeExamination,
    HomeInsightRow,
    HomeMission,
    HomeQueueRow,
    HomeQuickAction,
    HomeStudyHealth,
    HomeStudySignals,
    StudentHomePage,
)
from app.presentation.student.exam_week_briefing import (
    build_exam_week_briefing,
    build_home_insights,
)
from app.presentation.student.view_models import (
    HistoryPageViewModel,
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
_DAY_COMPLETE_MESSAGE = (
    "Today's Session is finished. Return tomorrow to continue."
)
_QUIET_REASON = "A session will be ready when today's focus is available."
_PAGE_QUESTION = "What should I do now?"
_DEFAULT_GREETING = "Welcome back."


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
                page_question=_PAGE_QUESTION,
                greeting=_DEFAULT_GREETING,
            )

        home = page.home
        revision = page.revision
        journey = page.journey
        history = page.history
        profile = page.profile
        queue = self._learning_queue(home, revision=revision)
        examination = self._examination(home)
        study_health = self._study_health(home)
        signals = self._study_signals(
            home,
            examination=examination,
            journey=journey,
            profile=profile,
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
        briefing_vm = build_exam_week_briefing(
            home=home,
            history=history,
            journey=journey,
            revision=revision,
            profile=profile,
        )
        forecast_title, forecast_guidance = self._forecast_insight(
            home=home,
        )
        insights_vm = build_home_insights(
            home=home,
            history=history,
            journey=journey,
            revision=revision,
            briefing=briefing_vm,
            forecast_title=forecast_title,
            forecast_guidance=forecast_guidance,
        )
        briefing = self._briefing_section(briefing_vm)
        insights = tuple(
            HomeInsightRow(kind=c.kind, label=c.label, body=c.body)
            for c in insights_vm
        )
        syllabus_position = next(
            (c.body for c in insights_vm if c.kind == "position"),
            "",
        )

        if show_revision_acknowledgement:
            mission = self._revision_ack_mission(
                home,
                title=revision_ack_title,
                body=revision_ack_body,
            )
            return self._with_workspace(
                page,
                self._assemble(
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
                briefing=briefing,
                insights=insights,
                syllabus_position=syllabus_position,
                history=history,
                ),
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
            return self._with_workspace(
                page,
                self._assemble(
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
                briefing=briefing,
                insights=insights,
                syllabus_position=syllabus_position,
                history=history,
                ),
            )

        mission = self._select_mission(home)
        if mission is not None:
            cleaned_queue = self._queue_without_l0_duplicate(queue, mission)
            return self._with_workspace(
                page,
                self._assemble(
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
                briefing=briefing,
                insights=insights,
                syllabus_position=syllabus_position,
                history=history,
                ),
            )

        if self._has_study_plan_signal(home):
            return self._with_workspace(
                page,
                self._assemble(
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
                briefing=briefing,
                insights=insights,
                syllabus_position=syllabus_position,
                history=history,
                ),
            )

        return self._with_workspace(
            page,
            self._assemble(
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
            briefing=None,
            insights=(),
            syllabus_position="",
            history=history,
            ),
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
        briefing: HomeBriefingSection | None = None,
        insights: tuple[HomeInsightRow, ...] = (),
        syllabus_position: str = "",
        history: HistoryPageViewModel | None = None,
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
        greeting = (home.greeting or "").strip() or _DEFAULT_GREETING
        density = self._density_presentation(
            state=state,
            mission=mission,
            history=history,
            home=home,
        )
        # PX-B-044 — calm return-after-gap framing (presentation only).
        days_gap = self._days_since_last_session(history)
        gap_copy = None
        try:
            from app.application.student_experience.student_microcopy import (
                return_after_gap_copy,
            )

            gap_copy = return_after_gap_copy(
                days_since_last=days_gap,
                display_name=None,
                in_progress=bool(
                    mission is not None and mission.primary_kind == "link"
                ),
            )
            if gap_copy.greeting and (
                not (home.greeting or "").strip()
                or greeting == _DEFAULT_GREETING
            ):
                greeting = gap_copy.greeting
            if gap_copy.support_line and not density["continuity_line"]:
                density = {**density, "continuity_line": gap_copy.support_line}
        except Exception:
            pass

        exam_horizon_line = ""
        try:
            from app.application.student_experience.student_microcopy import (
                exam_horizon_copy,
            )

            days_to_exam = self._days_to_exam_from_home(home)
            horizon = exam_horizon_copy(days_to_exam)
            if horizon is not None and horizon.support_line:
                exam_horizon_line = horizon.support_line
        except Exception:
            exam_horizon_line = ""

        preparing = bool(
            state == "quiet"
            or (
                mission is not None
                and not (mission.title or "").strip()
                and mission.primary_kind in {"none", "start_form"}
            )
        )

        milestone_acknowledgement = ""
        diligence_line = ""
        try:
            from app.application.student_experience.student_microcopy import (
                continuity_front_milestone_ack,
                diligence_reinforcement_copy,
            )

            if state == "day_complete" and mission is not None:
                ack = continuity_front_milestone_ack(mission.title)
                if ack:
                    milestone_acknowledgement = ack
            dil = diligence_reinforcement_copy(
                days_since_last=days_gap,
                streak_days=None,
            )
            # Prefer gap continuity over diligence when both would speak.
            if (
                dil.support_line
                and not density["continuity_line"]
                and not exam_horizon_line
            ):
                diligence_line = dil.support_line
        except Exception:
            milestone_acknowledgement = ""
            diligence_line = ""

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
            page_question=_PAGE_QUESTION,
            greeting=greeting,
            mission_section_title=section_title,
            signals=signals,
            tutor_available=tutor_available,
            tutor_href=tutor_href,
            briefing=briefing if state != "empty" else None,
            insights=insights if state != "empty" else (),
            syllabus_position=syllabus_position if state != "empty" else "",
            density_mode=density["density_mode"],
            continuity_line=density["continuity_line"],
            show_progress_strip=density["show_progress_strip"],
            show_tomorrow_preview=density["show_tomorrow_preview"],
            show_quick_actions=density["show_quick_actions"],
            exam_horizon_line=exam_horizon_line,
            preparing_mission=preparing,
            milestone_acknowledgement=milestone_acknowledgement,
            diligence_line=diligence_line,
        )

    def _forecast_insight(
        self,
        *,
        home: HomePageViewModel,
    ) -> tuple[str, str]:
        """KWP-012 — optional Study Trajectory line for Home Insights."""
        try:
            from flask_login import current_user

            from app.application.readiness_forecast import (
                get_readiness_forecast_engine,
            )
            from app.presentation.session.factory import (
                get_session_experience_composition,
            )

            composition = get_session_experience_composition()
            store = getattr(composition, "store", None) if composition else None
            if store is None:
                return "", ""
            student_id = str(getattr(current_user, "id", "") or "")
            if not student_id:
                return "", ""
            days = None
            if home.countdown and home.countdown.has_countdown:
                days = home.countdown.days
            readiness_ratio = None
            if home.readiness and home.readiness.has_readiness:
                raw = home.readiness.readiness_percent_label or ""
                digits = "".join(ch for ch in raw if ch.isdigit() or ch == ".")
                if digits:
                    readiness_ratio = float(digits)
                    if readiness_ratio > 1.0:
                        readiness_ratio /= 100.0
            forecast = get_readiness_forecast_engine().forecast_from_store(
                store,
                student_id=student_id,
                days_to_exam=days,
                current_readiness_ratio=readiness_ratio,
            )
            if not forecast.guidance:
                return "", ""
            return forecast.title, forecast.guidance
        except Exception:  # noqa: BLE001
            return "", ""

    @staticmethod
    def _briefing_section(briefing_vm) -> HomeBriefingSection | None:
        if briefing_vm is None or not getattr(briefing_vm, "has_briefing", False):
            return None
        return HomeBriefingSection(
            has_briefing=True,
            title=briefing_vm.title,
            strengthened=tuple(briefing_vm.strengthened or ()),
            needs_reinforcement=tuple(briefing_vm.needs_reinforcement or ()),
            consistency_label=briefing_vm.consistency_label or "",
            recommended_focus=briefing_vm.recommended_focus or "",
            recommended_detail=briefing_vm.recommended_detail or "",
            readiness_stage=briefing_vm.readiness_stage or "",
            summary_line=briefing_vm.summary_line or "",
        )

    @staticmethod
    def _with_workspace(
        page: StudentPageViewModel,
        home: StudentHomePage,
    ) -> StudentHomePage:
        """KWP-013 — attach Adaptive Study Workspace projection."""
        from dataclasses import replace

        workspace = compose_adaptive_workspace(page, home)
        page_question = (
            workspace.page_question if workspace.enabled else home.page_question
        )
        greeting = home.greeting
        continuity = home.continuity_line
        if workspace.enabled and workspace.morning_brief:
            brief_greeting = (workspace.morning_brief.greeting or "").strip()
            if brief_greeting:
                greeting = brief_greeting
            continuity = home_continuity_line(
                workspace.morning_brief,
                fallback=home.continuity_line,
            )
        return replace(
            home,
            workspace=workspace,
            page_question=page_question,
            greeting=greeting,
            continuity_line=continuity,
        )

    @staticmethod
    def _mission_section_title(mission: HomeMission | None) -> str:
        if mission is None:
            return "Today's Mission"
        if mission.primary_kind == "link":
            # PX-B-034: section chrome stays "Today's Mission"; CTA uses Continue.
            return "Today's Mission"
        if mission.primary_kind == "revision_ack":
            return "Today's Mission"
        return "Today's Mission"

    @staticmethod
    def _density_presentation(
        *,
        state: str,
        mission: HomeMission | None,
        history: HistoryPageViewModel | None,
        home: HomePageViewModel,
    ) -> dict[str, object]:
        """PX-B-048 / PX-B-010 — contextual chrome density (presentation only).

        Does not re-select missions. Compresses secondary blocks for day-zero
        and surfaces a continuity line for returning students.
        """
        session_count = 0
        if history is not None:
            session_count = int(getattr(history, "session_count", 0) or 0)
            if session_count <= 0 and getattr(history, "sessions", None):
                session_count = len(history.sessions)

        continuity = ""
        if state == "empty" or (
            session_count == 0 and state in {"quiet", "mission", "day_complete"}
        ):
            mode = "day_zero"
            # Empty still needs choose-exam actions; quiet/mission day-zero
            # keeps the primary CTA and folds secondary chrome.
            show_progress = False
            show_tomorrow = False
            show_actions = state in {"empty", "quiet"}
        elif mission is not None and mission.primary_kind == "link":
            mode = "returning"
            topic = (mission.title or mission.objective or "").strip()
            continuity = (
                f"You left off on {topic}."
                if topic
                else "Continue where you left off."
            )
            show_progress = True
            show_tomorrow = True
            show_actions = True
        elif session_count < 5:
            mode = "returning"
            topic = ""
            if mission is not None:
                topic = (mission.title or mission.objective or "").strip()
            if not topic and home.educational and getattr(
                home.educational, "today_topic_title", ""
            ):
                topic = str(home.educational.today_topic_title).strip()
            continuity = (
                f"Your next sitting: {topic}."
                if topic
                else "Your authorised next sitting is ready below."
            )
            show_progress = True
            show_tomorrow = True
            show_actions = True
        else:
            mode = "established"
            show_progress = True
            show_tomorrow = True
            show_actions = True

        return {
            "density_mode": mode,
            "continuity_line": continuity,
            "show_progress_strip": show_progress,
            "show_tomorrow_preview": show_tomorrow,
            "show_quick_actions": show_actions,
        }

    @staticmethod
    def _days_since_last_session(
        history: HistoryPageViewModel | None,
    ) -> int | None:
        """Calendar days since the most recent History session (presentation)."""
        if history is None:
            return None
        sessions = getattr(history, "sessions", None) or ()
        if not sessions:
            return None
        from datetime import date, datetime

        latest: date | None = None
        for row in sessions:
            raw = (
                getattr(row, "completed_on", None)
                or getattr(row, "date", None)
                or getattr(row, "session_date", None)
                or getattr(row, "completed_at", None)
            )
            if raw is None:
                continue
            if isinstance(raw, datetime):
                d = raw.date()
            elif isinstance(raw, date):
                d = raw
            else:
                text = str(raw).strip()[:10]
                try:
                    d = date.fromisoformat(text)
                except ValueError:
                    continue
            if latest is None or d > latest:
                latest = d
        if latest is None:
            return None
        return max(0, (date.today() - latest).days)

    @staticmethod
    def _days_to_exam_from_home(home: HomePageViewModel) -> int | None:
        """Days until exam from Home VM countdown fields (presentation only)."""
        countdown = getattr(home, "countdown", None)
        if countdown is not None:
            raw = getattr(countdown, "days", None)
            if raw is not None:
                try:
                    return int(raw)
                except (TypeError, ValueError):
                    pass
            label = getattr(countdown, "label", None) or ""
            text = str(label).strip().lower()
            if "today" in text:
                return 0
            if text.startswith("1 day"):
                return 1
            parts = text.split()
            if parts and parts[0].isdigit():
                return int(parts[0])
        return None
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

        # 1. Open session → Continue (deep link, no re-commit).
        if home.session_control == "resume" and session_id:
            resume_label = (
                home.session_control_label
                or home.primary_cta_label
                or "Continue"
            ).strip()
            lowered = resume_label.lower()
            if "resume" not in lowered and "continue" not in lowered:
                resume_label = "Continue"
            return HomeMission(
                subject_name=subject or "Current subject",
                objective=objective or "Continue your open session",
                status_label=self._status_line("In progress", duration),
                why_now=why_now or "Open session — continue where you left off",
                after_completion=after,
                primary_label=resume_label,
                primary_kind="link",
                primary_href=url_for("session.overview", session_id=session_id),
                duration_label=duration,
                mission_id=mission_id,
                session_id=session_id,
                recommendation_key=rec_key,
                title=title or "Today's Session",
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
                primary_label="Continue",
                primary_kind="link",
                primary_href=url_for("session.overview", session_id=session_id),
                duration_label=duration,
                mission_id=mission_id,
                session_id=session_id,
                recommendation_key=rec_key,
                title=title or "Today's Session",
                difficulty_label=difficulty,
                learning_objective=objective or "Wrap up your open session",
            )

        # 2a. Runtime C Mark-complete — rollback / pilot only (SR-002).
        # session_control is complete_runtime_c — not a Guided Session start.
        # Never the default product Primary when SR_SESSION_PRIMARY is ON.
        if (
            home.primary_cta_enabled
            and home.session_control == "complete_runtime_c"
            and mission_id
        ):
            label = (
                home.session_control_label
                or home.primary_cta_label
                or "Confirm today's Mission"
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
                title=title or objective or "Today's Session",
                difficulty_label=difficulty,
                learning_objective=objective or "Today's study focus",
            )

        # 2–3. Mission ready → Start Session (POST preserves commitment path).
        # Prefer Stage A title/id when Experience chrome is empty or weak
        # (common after plan switch / with Mission Read Bridge off / store pollution).
        stage_a = self._peek_stage_a_ready_mission(home)
        if stage_a is not None:
            stage_a_title = (stage_a.title or "").strip()
            edu_owns = bool(
                home.educational and getattr(home.educational, "active", False)
            )
            # Stage A owns today's SQL mission for non–Runtime C Home. Prefer
            # its title/id so polluted Experience chrome (session-scoped store,
            # empty unified journey placeholders, stale package resolve) cannot
            # hide a real ready mission behind quiet/preparing or a wrong hero.
            if stage_a_title and not edu_owns:
                title = stage_a_title
                mission_id = str(stage_a.id)
            elif stage_a_title and (
                not (title or "").strip()
                or (title or "").strip().casefold()
                in {
                    "today's mission",
                    "today's session",
                    "today's study focus",
                    "current subject",
                }
            ):
                title = stage_a_title
                if not mission_id:
                    mission_id = str(stage_a.id)

        stage_a_ready = stage_a is not None and bool((title or "").strip())
        if (home.primary_cta_enabled or stage_a_ready) and (
            home.session_control in ("start", "resume", "") or not home.session_control
        ):
            label = self._start_primary_label(home)
            if not subject and not objective and not (title or "").strip():
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
                title=title or objective or "Today's Session",
                difficulty_label=difficulty,
                learning_objective=objective or "Today's study focus",
            )

        # 4. Experience / Runtime C chrome has a real title but CTA not yet
        # enabled — still show the hero. Never replace a known mission with
        # the quiet/preparing skeleton.
        display_title = (title or objective or "").strip()
        if display_title and (
            mission_id
            or (home.primary_mission_title or "").strip()
            or (
                home.recommendation
                and (home.recommendation.title or "").strip()
            )
            or stage_a is not None
        ):
            return HomeMission(
                subject_name=subject or "Current subject",
                objective=objective or "Today's study focus",
                status_label=self._status_line(
                    home.completion_status_label or home.session_status or "Ready",
                    duration,
                ),
                why_now=why_now,
                after_completion=after,
                primary_label="",
                primary_kind="none",
                duration_label=duration,
                mission_id=mission_id,
                session_id=session_id,
                recommendation_key=rec_key,
                title=display_title,
                difficulty_label=difficulty,
                learning_objective=objective or "Today's study focus",
            )

        return None

    def _peek_stage_a_ready_mission(self, home: HomePageViewModel):
        """Return today's Stage A SQL Mission when it is ready to surface.

        Skips deliberate Runtime C holds (coverage gap / syllabus complete)
        and completed Stage A missions (day_complete path owns those).
        """
        edu = home.educational
        if edu and getattr(edu, "active", False):
            status_label = (home.completion_status_label or "").strip().lower()
            if status_label in {
                "waiting for certified guidance",
                "syllabus complete",
            }:
                return None

        try:
            from flask_login import current_user

            from app.services.mission_service import MissionService
        except Exception:  # noqa: BLE001 — presentation fail-open
            return None

        user_id = getattr(current_user, "id", None) if current_user else None
        if user_id is None:
            return None
        try:
            mission = MissionService.get_today_mission(int(user_id))
        except Exception:  # noqa: BLE001 — presentation fail-open
            return None
        if mission is None:
            return None

        status = (mission.status or "").strip().lower()
        if status == "completed":
            return None
        if not (mission.title or "").strip():
            return None
        return mission

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
            if streak == "0 days" or streak.lower() in {
                "no streak yet",
                "0 day streak",
            }:
                # PX-B-047 — empty rhythm is calm, not punitive.
                try:
                    from app.application.student_experience.student_microcopy import (
                        DILIGENCE_EMPTY_STREAK,
                    )

                    streak = DILIGENCE_EMPTY_STREAK
                except Exception:
                    streak = "Study rhythm builds as you show up"
            elif (
                not streak.lower().endswith("streak")
                and "rhythm" not in streak.lower()
            ):
                streak = f"{streak} streak"

        progress_label = ""
        progress_percent: int | None = None
        # V1S-005 DF-002: Runtime C ProgressEngine coverage before Runtime A
        # journey mastery theatre (educational trust / progress isolation).
        if home.educational and getattr(home.educational, "active", False):
            progress_percent = int(home.educational.progress_percent or 0)
            progress_label = (
                home.educational.progress_label
                or home.educational.coverage_label
                or f"{progress_percent}% of syllabus covered"
            ).strip()
        elif journey is not None and journey.progress_percent is not None:
            progress_percent = int(journey.progress_percent)
            progress_label = (
                journey.progress_label
                or f"{progress_percent}% of syllabus covered"
            ).strip()
        # No readiness→coverage fallback: Home labels this field "Syllabus covered".
        # When genuine coverage is unavailable, leave progress empty (quiet omit).

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

        # UX-001: duration lives once on the mission hero — omit from signals.
        if not any((subject, streak, progress_label, countdown)):
            return None
        return HomeStudySignals(
            subject_label=subject,
            streak_label=streak,
            progress_label=progress_label,
            progress_percent=progress_percent,
            countdown_label=countdown,
            estimated_study_label="",
        )

    @staticmethod
    def _mission_title(home: HomePageViewModel, *, objective: str) -> str:
        # PX-003 / PX-B-002: package-id / Runtime C title first — never
        # soft-match topic_title_keywords for student Home chrome.
        try:
            from app.application.educational_packages.student_chrome import (
                display_title_for_package_id,
                resolve_package_for_student_chrome,
            )

            edu = home.educational
            pack_id = ""
            if edu:
                pack_id = str(
                    getattr(edu, "educational_package_id", "") or ""
                ).strip()
            if pack_id:
                pack_title = display_title_for_package_id(pack_id)
                if pack_title:
                    return pack_title
            pack = resolve_package_for_student_chrome(
                educational_package_id=pack_id,
                subject_id=getattr(edu, "subject_code", "") if edu else "",
                syllabus_topic_code=(
                    getattr(edu, "today_topic_code", "") if edu else ""
                ),
            )
            if pack is not None and (pack.display_title or "").strip():
                return pack.display_title.strip()
        except Exception:  # noqa: BLE001 — presentation must stay resilient
            pass
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
            # Prefer stage language; keep percent as quiet secondary only.
            status = (readiness.readiness_label or "Building").strip()
            if "%" in status:
                status = "Building"
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
            stage_lower = status.lower()
            if "ready for assessment" in stage_lower:
                tone = "positive"
            elif "building" in stage_lower:
                tone = "neutral"
            return HomeStudyHealth(
                status_label=status,
                detail=" · ".join(detail_parts),
                tone=tone,
            )
        if home.day_complete:
            return HomeStudyHealth(
                status_label="Day complete",
                detail="Rest — return tomorrow for the next Session.",
                tone="positive",
            )
        if self._has_study_plan_signal(home):
            return HomeStudyHealth(
                status_label="Getting started",
                detail=(
                    "Complete today's Session to strengthen your "
                    "Exam Readiness signal."
                ),
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
                    detail="Select an examination to unlock today's Session",
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
                        detail="Why this Session was chosen",
                    )
                )
        if (
            state in {"mission", "quiet", "day_complete"}
            and len(actions) < _QUICK_ACTION_MAX
        ):
            if not any(a.label == "Curriculum Map" for a in actions):
                actions.append(
                    HomeQuickAction(
                        label="Curriculum Map",
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
        """Exactly one operational why-now line (≤140 chars preferred).

        MISSION-002: prefer mission rationale (why_recommended) over journey
        timeliness so "Why this mission" describes the mission topic.
        EA-006: prefer certified educational package why_now when present.
        """
        try:
            from app.application.educational_packages.composition_overlay import (
                why_now_for_topic,
            )

            edu = home.educational
            pack_why = why_now_for_topic(
                topic_id=getattr(edu, "today_topic_id", "") if edu else "",
                topic_code=getattr(edu, "today_topic_code", "") if edu else "",
                topic_title=(
                    (getattr(edu, "today_topic_title", "") if edu else "")
                    or (home.primary_mission_title or "")
                ),
                subject_id=getattr(edu, "subject_code", "") if edu else "",
            )
            if pack_why:
                return pack_why[:140]
        except Exception:  # noqa: BLE001 — presentation must stay resilient
            pass
        candidates: list[str] = []
        if home.session_control == "resume":
            candidates.append("Open session — continue where you left off")
        if home.explanation and home.explanation.why_recommended:
            candidates.append(home.explanation.why_recommended.strip())
        if home.explanation and home.explanation.timeliness_line:
            candidates.append(home.explanation.timeliness_line.strip())
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
        try:
            from app.application.educational_packages.student_chrome import (
                expected_benefit_for_package_id,
                resolve_package_for_student_chrome,
            )

            edu = home.educational
            pack_id = ""
            if edu:
                pack_id = str(
                    getattr(edu, "educational_package_id", "") or ""
                ).strip()
            if pack_id:
                benefit = expected_benefit_for_package_id(pack_id)
                if benefit:
                    return benefit[:140]
            pack = resolve_package_for_student_chrome(
                educational_package_id=pack_id,
                subject_id=getattr(edu, "subject_code", "") if edu else "",
                syllabus_topic_code=(
                    getattr(edu, "today_topic_code", "") if edu else ""
                ),
            )
            if pack is not None and pack.expected_benefit:
                return pack.expected_benefit.strip()[:140]
        except Exception:  # noqa: BLE001 — presentation must stay resilient
            pass
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
        from app.application.student_experience.study_verbs import (
            START_TODAY,
            canonical_start_label,
        )

        raw = (
            home.session_control_label
            or home.primary_cta_label
            or START_TODAY
        ).strip()
        in_progress = bool(
            (home.session_id or "").strip()
            or (home.session_control or "").strip().lower()
            in {"resume", "continue"}
        )
        return canonical_start_label(raw, in_progress=in_progress)

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
