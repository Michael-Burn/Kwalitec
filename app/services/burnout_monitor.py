"""Study-activity pattern notice service using deterministic thresholds.

Observes:
- Falling accuracy (week-over-week decline)
- Falling confidence
- Excessive study duration (single session)
- Long streaks without breaks

Capability 4.7: presentations must not claim burnout prediction — only
observed study-activity patterns the platform can defend.
"""

from __future__ import annotations

from datetime import date, timedelta

from app.models.learning import StudyAttempt
from app.services.adaptive_learning_service import AdaptiveLearningService
from app.services.readiness_service import ReadinessService


class BurnoutMonitor:
    """Detects burnout warning signs using deterministic thresholds."""

    # Thresholds
    ACCURACY_DECLINE_THRESHOLD = 10.0
    CONFIDENCE_THRESHOLD = 30.0
    EXCESSIVE_DURATION_MINUTES = 180
    STREAK_BREAK_THRESHOLD = 14

    @staticmethod
    def detect_burnout(user_id: int) -> dict:
        """Detect burnout risk for a user.

        Evaluates multiple indicators and computes an overall risk level.
        """
        indicators: list[dict] = []
        risk_score = 0

        accuracy_check = BurnoutMonitor._check_accuracy_decline(user_id)
        if accuracy_check["triggered"]:
            indicators.append(accuracy_check)
            risk_score += accuracy_check["weight"]

        confidence_check = BurnoutMonitor._check_confidence_decline(user_id)
        if confidence_check["triggered"]:
            indicators.append(confidence_check)
            risk_score += confidence_check["weight"]

        duration_check = BurnoutMonitor._check_excessive_duration(user_id)
        if duration_check["triggered"]:
            indicators.append(duration_check)
            risk_score += duration_check["weight"]

        streak_check = BurnoutMonitor._check_long_streak(user_id)
        if streak_check["triggered"]:
            indicators.append(streak_check)
            risk_score += streak_check["weight"]

        if risk_score >= 8:
            risk_level = "high"
        elif risk_score >= 5:
            risk_level = "moderate"
        elif risk_score >= 2:
            risk_level = "low"
        else:
            risk_level = "none"

        if not indicators:
            explanation = (
                "No concerning study-activity patterns detected. "
                "Keep maintaining a healthy study rhythm."
            )
        else:
            descs = [i["description"] for i in indicators]
            explanation = (
                "Observed study-activity patterns: " + "; ".join(descs) + "."
            )

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "indicators": indicators,
            "explanation": explanation,
        }

    @staticmethod
    def _check_accuracy_decline(user_id: int) -> dict:
        today = date.today()
        current_week_start = today - timedelta(days=today.weekday())
        prev_week_start = current_week_start - timedelta(days=7)
        prev_week_end = current_week_start - timedelta(days=1)

        current_attempts = StudyAttempt.query.filter(
            StudyAttempt.user_id == user_id,
            StudyAttempt.study_date >= current_week_start,
            StudyAttempt.study_date <= today,
        ).all()

        cur_q = sum(a.questions_attempted or 0 for a in current_attempts)
        cur_c = sum(a.questions_correct or 0 for a in current_attempts)
        cur_acc = (cur_c / cur_q * 100) if cur_q > 0 else None

        prev_attempts = StudyAttempt.query.filter(
            StudyAttempt.user_id == user_id,
            StudyAttempt.study_date >= prev_week_start,
            StudyAttempt.study_date <= prev_week_end,
        ).all()

        prev_q = sum(a.questions_attempted or 0 for a in prev_attempts)
        prev_c = sum(a.questions_correct or 0 for a in prev_attempts)
        prev_acc = (prev_c / prev_q * 100) if prev_q > 0 else None

        triggered = False
        description = ""

        if cur_acc is not None and prev_acc is not None:
            decline = prev_acc - cur_acc
            if decline >= BurnoutMonitor.ACCURACY_DECLINE_THRESHOLD:
                triggered = True
                description = (
                    f"Accuracy dropped from {prev_acc:.0f}% to {cur_acc:.0f}% "
                    f"(a decline of {decline:.0f} percentage points this week)"
                )
            elif decline > 0:
                description = (
                    f"Accuracy slightly declined from {prev_acc:.0f}% to "
                    f"{cur_acc:.0f}% (within normal range)"
                )
            else:
                description = "Accuracy is stable or improving."

        return {
            "type": "accuracy_decline",
            "triggered": triggered,
            "weight": 3,
            "description": description,
            "current_accuracy": round(cur_acc, 1) if cur_acc is not None else None,
            "previous_accuracy": round(prev_acc, 1) if prev_acc is not None else None,
        }

    @staticmethod
    def _check_confidence_decline(user_id: int) -> dict:
        today = date.today()
        recent = (
            StudyAttempt.query.filter(
                StudyAttempt.user_id == user_id,
                StudyAttempt.study_date >= today - timedelta(days=7),
                StudyAttempt.confidence_after.isnot(None),
            )
            .order_by(StudyAttempt.study_date.desc())
            .limit(10)
            .all()
        )

        if len(recent) < 3:
            return {
                "type": "confidence_decline",
                "triggered": False,
                "weight": 2,
                "description": "Not enough recent data to assess confidence trends.",
                "average_confidence": None,
            }

        conf_values = []
        for a in recent:
            val = AdaptiveLearningService.get_confidence_numeric(a.confidence_after)
            if val is not None:
                conf_values.append(val)

        if not conf_values:
            return {
                "type": "confidence_decline",
                "triggered": False,
                "weight": 2,
                "description": "No confidence data available for recent attempts.",
                "average_confidence": None,
            }

        avg_conf = sum(conf_values) / len(conf_values)
        triggered = avg_conf < BurnoutMonitor.CONFIDENCE_THRESHOLD
        description = (
            f"Average confidence over the last {len(conf_values)} sessions "
            f"is {avg_conf:.0f}/100. "
            + (
                "This is below the healthy threshold. Low confidence can indicate "
                "burnout, overwhelm, or knowledge gaps."
                if triggered
                else "This is within the healthy range."
            )
        )

        return {
            "type": "confidence_decline",
            "triggered": triggered,
            "weight": 2,
            "description": description,
            "average_confidence": round(avg_conf, 1),
        }

    @staticmethod
    def _check_excessive_duration(user_id: int) -> dict:
        today = date.today()
        seven_days_ago = today - timedelta(days=7)

        recent = StudyAttempt.query.filter(
            StudyAttempt.user_id == user_id,
            StudyAttempt.study_date >= seven_days_ago,
            StudyAttempt.duration_minutes.isnot(None),
        ).all()

        excessive = [
            a for a in recent
            if a.duration_minutes
            and a.duration_minutes > BurnoutMonitor.EXCESSIVE_DURATION_MINUTES
        ]

        if not excessive:
            return {
                "type": "excessive_duration",
                "triggered": False,
                "weight": 3,
                "description": "No excessively long study sessions detected this week.",
                "excessive_count": 0,
            }

        total = len(excessive)
        max_dur = max(a.duration_minutes or 0 for a in excessive)
        triggered = total >= 2 or max_dur > 300

        description = (
            f"{total} study session(s) exceeded "
            f"{BurnoutMonitor.EXCESSIVE_DURATION_MINUTES} minutes "
            f"this week (longest: {max_dur} min). "
            + (
                "Sessions this long are counterproductive — fatigue reduces "
                "learning efficiency and increases burnout risk."
                if triggered
                else "Monitor duration to ensure quality over quantity."
            )
        )

        return {
            "type": "excessive_duration",
            "triggered": triggered,
            "weight": 3,
            "description": description,
            "excessive_count": total,
            "max_duration_minutes": max_dur,
        }

    @staticmethod
    def _check_long_streak(user_id: int) -> dict:
        current_streak = ReadinessService.get_current_streak(user_id)
        triggered = current_streak >= BurnoutMonitor.STREAK_BREAK_THRESHOLD

        description = (
            f"Current study streak: {current_streak} days. "
            + (
                f"Streaks longer than {BurnoutMonitor.STREAK_BREAK_THRESHOLD} days "
                "without a rest day increase burnout risk. Even elite athletes "
                "schedule rest days. Consider taking one day off to recharge."
                if triggered
                else "Streak is within a healthy range. Keep going!"
            )
        )

        return {
            "type": "long_streak",
            "triggered": triggered,
            "weight": 2,
            "description": description,
            "current_streak": current_streak,
        }
