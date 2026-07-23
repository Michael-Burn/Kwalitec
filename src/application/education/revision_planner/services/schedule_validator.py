"""ScheduleValidator — structural and policy validation for StudySchedules."""

from __future__ import annotations

from application.education.revision_planner.enums import DayKind, SessionStatus
from application.education.revision_planner.errors import ScheduleValidationError
from application.education.revision_planner.models.study_schedule import StudySchedule


class ScheduleValidator:
    """Deterministic validation of StudySchedule invariants and policies."""

    @staticmethod
    def validate(schedule: StudySchedule) -> None:
        """Validate schedule or raise ScheduleValidationError."""
        errors = ScheduleValidator.collect_errors(schedule)
        if errors:
            raise ScheduleValidationError(errors[0], code="schedule_invalid")

    @staticmethod
    def collect_errors(schedule: StudySchedule) -> tuple[str, ...]:
        errors: list[str] = []
        errors.extend(ScheduleValidator._check_horizon(schedule))
        errors.extend(ScheduleValidator._check_day_kinds(schedule))
        errors.extend(ScheduleValidator._check_daily_caps(schedule))
        errors.extend(ScheduleValidator._check_session_membership(schedule))
        errors.extend(ScheduleValidator._check_dependencies(schedule))
        return tuple(errors)

    @staticmethod
    def is_valid(schedule: StudySchedule) -> bool:
        return not ScheduleValidator.collect_errors(schedule)

    @staticmethod
    def _check_horizon(schedule: StudySchedule) -> list[str]:
        errors: list[str] = []
        if schedule.end_date < schedule.start_date:
            errors.append("end_date precedes start_date")
        for day in schedule.days:
            if day.day_date < schedule.start_date or day.day_date > schedule.end_date:
                errors.append(
                    f"day {day.day_date.isoformat()} is outside schedule horizon"
                )
        return errors

    @staticmethod
    def _check_day_kinds(schedule: StudySchedule) -> list[str]:
        errors: list[str] = []
        for day in schedule.days:
            if day.kind is DayKind.REST and day.sessions:
                active = [
                    s
                    for s in day.sessions
                    if s.status
                    not in (SessionStatus.CANCELLED, SessionStatus.RESCHEDULED)
                ]
                if active:
                    errors.append(
                        f"rest day {day.day_date.isoformat()} has active sessions"
                    )
        return errors

    @staticmethod
    def _check_daily_caps(schedule: StudySchedule) -> list[str]:
        errors: list[str] = []
        constraints = schedule.constraints
        if constraints is None:
            return errors
        daily_cap = constraints.effective_daily_cap_minutes()
        for day in schedule.days:
            allocated = day.active_allocated_minutes()
            if day.available_minutes > 0 and allocated > day.available_minutes:
                errors.append(
                    f"day {day.day_date.isoformat()} exceeds available minutes"
                )
            if allocated > daily_cap:
                errors.append(
                    f"day {day.day_date.isoformat()} exceeds daily study cap"
                )
        return errors

    @staticmethod
    def _check_session_membership(schedule: StudySchedule) -> list[str]:
        errors: list[str] = []
        day_session_ids = {
            s.session_id.value for day in schedule.days for s in day.sessions
        }
        for session in schedule.sessions:
            if session.session_id.value not in day_session_ids:
                # Sessions may exist on days rebuilt later; warn only when days
                # are present and the date has a StudyDay.
                day = schedule.day_for(session.session_date)
                if day is not None and session not in day.sessions:
                    errors.append(
                        f"session {session.session_id.value} missing from its StudyDay"
                    )
        return errors

    @staticmethod
    def _check_dependencies(schedule: StudySchedule) -> list[str]:
        errors: list[str] = []
        constraints = schedule.constraints
        if constraints is None or not constraints.honour_mission_dependencies:
            return errors

        # Prerequisite scheduled missions must not start after same-subject
        # non-prerequisite missions.
        by_subject: dict[str, list] = {}
        for scheduled in schedule.scheduled_missions:
            subject = scheduled.subject_id or ""
            by_subject.setdefault(subject, []).append(scheduled)

        for subject, items in by_subject.items():
            if not subject:
                continue
            prereqs = [m for m in items if m.is_prerequisite]
            dependents = [m for m in items if not m.is_prerequisite]
            if not prereqs or not dependents:
                continue
            latest_prereq = max(m.scheduled_date for m in prereqs)
            earliest_dependent = min(m.scheduled_date for m in dependents)
            if earliest_dependent < latest_prereq:
                errors.append(
                    f"dependency violation for subject {subject}: "
                    "dependent scheduled before prerequisite"
                )
        return errors
