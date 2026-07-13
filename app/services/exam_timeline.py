"""Exam timeline service for phase detection and schedule tracking."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from app.models.learning import StudyAttempt
from app.services.educational_kpi_status import EducationalKpiStatusService
from app.services.readiness_service import ReadinessService
from app.services.study_plan_service import StudyPlanService
from app.services.time_engine_service import TimeEngineService


class ExamTimeline:
    """Generates exam timeline data for the dashboard widget.

    Provides days remaining, phase detection (curriculum, revision, mock),
    and educationally honest schedule status (Capability 4.7).

    Schedule status is owned by ``EducationalKpiStatusService`` and derived
    only from calendar + TimeEngine evidence — never from a fictional
    expected-coverage curve or predictive risk labels.
    """

    @staticmethod
    def get_timeline(user_id: int) -> dict | None:
        """Get the exam timeline for a user."""
        active_plan = StudyPlanService.get_user_active_plan(user_id)
        if not active_plan or not active_plan.exam_date:
            return None

        today = date.today()
        exam_date = active_plan.exam_date
        if isinstance(exam_date, datetime):
            exam_date = exam_date.date()

        days_remaining = (exam_date - today).days

        coverage = ReadinessService.get_curriculum_coverage(user_id)
        readiness = ReadinessService.get_overall_readiness(user_id)
        coverage_pct = coverage["coverage_percentage"]
        mastery_pct = readiness["avg_mastery"]

        phase = ExamTimeline._determine_phase(days_remaining, coverage_pct, mastery_pct)
        status = ExamTimeline._determine_status(
            days_remaining=days_remaining,
            coverage_pct=coverage_pct,
            active_plan=active_plan,
        )
        completion_date = ExamTimeline._estimate_completion_date(
            user_id, coverage_pct, coverage["topics_not_started"], active_plan
        )

        return {
            "exam_name": active_plan.exam_name,
            "exam_date": exam_date.isoformat(),
            "days_remaining": days_remaining,
            "curriculum_coverage_pct": round(coverage_pct, 1),
            "average_mastery_pct": round(mastery_pct, 1),
            "current_phase": phase["name"],
            "phase_description": phase["description"],
            "next_phase": phase["next_phase"],
            "schedule_status": status.code,
            "status_label": status.label,
            "status_severity": status.severity,
            "status_symbol": status.symbol,
            "status_evidence": status.evidence_summary,
            "status_kind": status.kind,
            # Reserved future presentation slots (always None for now)
            "status_readiness": status.readiness,
            "status_risk": status.risk,
            "status_study_velocity": status.study_velocity,
            "status_predicted_completion": status.predicted_completion,
            "estimated_completion_date": (
                completion_date.isoformat() if completion_date else None
            ),
            "topics_started": coverage["topics_started"],
            "topics_not_started": coverage["topics_not_started"],
            "total_topics": coverage["total_leaf_topics"],
        }

    @staticmethod
    def _determine_phase(
        days_remaining: int,
        coverage_pct: float,
        mastery_pct: float,
    ) -> dict:
        if days_remaining <= 0:
            return {
                "name": "Exam Period",
                "description": (
                    "The exam date has arrived or passed. "
                    "Focus on last-minute revision and exam-day preparation."
                ),
                "next_phase": None,
            }

        if days_remaining <= 14:
            return {
                "name": "Final Revision",
                "description": (
                    "Two weeks or less remaining. Focus exclusively on mock exams, "
                    "past papers, and targeted revision of weak areas. "
                    "Do not start new topics."
                ),
                "next_phase": "Exam Period",
            }

        if days_remaining <= 30:
            if coverage_pct >= 70:
                return {
                    "name": "Revision Phase",
                    "description": (
                        "One month remaining with good coverage. "
                        "Shift to revision mode: "
                        "focus on weak topics, past papers, and consolidation. "
                        "Minimise new topic learning."
                    ),
                    "next_phase": "Final Revision",
                }
            else:
                return {
                    "name": "Intensive Catch-Up",
                    "description": (
                        f"One month remaining but only {coverage_pct:.0f}% coverage. "
                        "Prioritise high-weight topics and accelerate coverage. "
                        "Consider increasing study hours."
                    ),
                    "next_phase": "Final Revision",
                }

        if days_remaining <= 60:
            return {
                "name": "Mock Exam Phase",
                "description": (
                    f"{days_remaining} days remaining. Incorporate regular mock exams "
                    "while continuing curriculum coverage. Aim for at least one "
                    "full mock exam per week with thorough review."
                ),
                "next_phase": "Revision Phase",
            }

        if days_remaining <= 90:
            return {
                "name": "Curriculum Phase",
                "description": (
                    f"{days_remaining} days remaining. Focus on systematic curriculum "
                    "coverage. Start mock exam practice on covered sections. "
                    "Maintain consistent study schedule."
                ),
                "next_phase": "Mock Exam Phase",
            }

        return {
            "name": "Foundation Phase",
            "description": (
                f"{days_remaining} days remaining. Build strong foundations through "
                "systematic curriculum coverage. Establish good study habits "
                "and maintain the review schedule."
            ),
            "next_phase": "Curriculum Phase",
        }

    @staticmethod
    def _determine_status(
        *,
        days_remaining: int,
        coverage_pct: float,
        active_plan,
    ):
        """Educationally honest schedule/pace status (Capability 4.7).

        Prefers TimeEngine hours balance; falls back to calendar facts only.
        Never uses a fictional expected-coverage curve.
        """
        time_summary = TimeEngineService.calculate_time_summary(active_plan)
        if time_summary is not None:
            return EducationalKpiStatusService.from_time_summary(
                time_summary,
                days_remaining,
                coverage_pct=coverage_pct,
            )
        return EducationalKpiStatusService.from_days_remaining(days_remaining)

    @staticmethod
    def _estimate_completion_date(
        user_id: int,
        coverage_pct: float,
        topics_not_started: int,
        active_plan,
    ) -> date | None:
        """Internal velocity estimate — not a dashboard KPI (Capability 4.7).

        Reserved for future Predicted Completion presentation; not surfaced
        as student-facing certainty on the dashboard.
        """
        if topics_not_started <= 0:
            return date.today()

        today = date.today()
        four_weeks_ago = today - timedelta(days=28)

        recent_attempts = StudyAttempt.query.filter(
            StudyAttempt.user_id == user_id,
            StudyAttempt.study_date >= four_weeks_ago,
            StudyAttempt.topic_id.isnot(None),
        ).all()

        recent_topic_ids = set()
        for a in recent_attempts:
            if a.topic_id:
                recent_topic_ids.add(a.topic_id)

        topics_per_week = len(recent_topic_ids) / 4.0 if recent_topic_ids else 0.5
        if topics_per_week < 0.1:
            topics_per_week = 1.0

        weeks_needed = topics_not_started / topics_per_week
        days_needed = int(weeks_needed * 7)

        return today + timedelta(days=days_needed)
