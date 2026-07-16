"""Educational Explainability — student-facing narrative presentation.

EIP-003: shapes educational communication only. Does not redesign Learning Mode,
recommendations ranking, Educational Evidence, Educational Intelligence, or the
Digital Twin. Does not invent scores or mastery.

Governing refs:
- EDUCATIONAL_EXPLAINABILITY_STANDARD.md
- Constitution Articles II, III, VII
- EL-008, EL-009, EL-010
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# Internal journey stages → student-safe educational labels (EL-010).
_STAGE_LABELS: dict[str, str] = {
    "Not Started": "Not started",
    "Learning": "Learning",
    "Practising": "Practising",
    "Mastered": "Strong estimated knowledge",
    "Needs Review": "Needs more practice",
    "Completed": "Completed studying",
}


@dataclass(frozen=True)
class MissionNarrative:
    """Structured Today's Mission educational story (EIP-003 Mission Narrative)."""

    topic_title: str
    educational_purpose: str
    reason_for_selection: str
    educational_position: str
    next_action: str
    observed_facts: tuple[str, ...]
    estimates: tuple[str, ...]


@dataclass(frozen=True)
class RecommendationNarrative:
    """Recommendation with Observeds / Estimates / Advice distinguished."""

    observed_facts: tuple[str, ...]
    estimates: tuple[str, ...]
    educational_advice: str
    next_action: str
    reason: str
    expected_benefit: str


@dataclass(frozen=True)
class ReadinessNarrative:
    """Readiness speech with evidence basis or cannot-estimate honesty."""

    label: str
    percentage: float | None
    explanation: str
    evidence_basis: str
    can_estimate: bool
    is_estimate: bool


@dataclass(frozen=True)
class StudySessionFeedbackNarrative:
    """LXP-004 post-session feedback — four student questions answered honestly."""

    what_happened: tuple[str, ...]
    what_observed: tuple[str, ...]
    honest_conclusions: tuple[str, ...]
    what_next: str
    scenario: str


class EducationalExplainabilityService:
    """Build student-safe educational narratives from existing educational state.

    Presentation / narration only. Input values come from authorised services;
    this service never recalculates readiness, mastery, or recommendations.
    """

    @staticmethod
    def student_stage_label(stage: str | None) -> str:
        """Map an internal topic stage to student-safe educational wording."""
        if not stage:
            return "Not started"
        return _STAGE_LABELS.get(stage, stage)

    @staticmethod
    def enrich_topic_rows(topics: list[dict] | None) -> list[dict]:
        """Return topic rows with student-safe stage labels (copy; no mutation)."""
        if not topics:
            return []
        enriched: list[dict] = []
        for topic in topics:
            row = dict(topic)
            row["stage_label"] = EducationalExplainabilityService.student_stage_label(
                topic.get("stage")
            )
            enriched.append(row)
        return enriched

    @staticmethod
    def build_mission_narrative(
        *,
        mission_title: str | None,
        mission_status: str | None = None,
        exam_name: str | None = None,
        completed_topics: int | None = None,
        total_topics: int | None = None,
        syllabus_coverage_pct: float | None = None,
    ) -> MissionNarrative | None:
        """Assemble Today's Mission educational narrative.

        Args:
            mission_title: Persisted mission title (Learning Mode topic authority).
            mission_status: Current mission status string.
            exam_name: Active study plan exam name, if any.
            completed_topics: Count of topics with Study Progress complete.
            total_topics: Syllabus topic count when known.
            syllabus_coverage_pct: Weighted syllabus coverage 0–100 when known.

        Returns:
            MissionNarrative, or None when there is no mission to narrate.
        """
        if not mission_title:
            return None

        observed: list[str] = [
            f"Today's Study Session topic is {mission_title}.",
        ]
        if exam_name:
            observed.append(f"Active study plan: {exam_name}.")
        if (
            completed_topics is not None
            and total_topics is not None
            and total_topics > 0
        ):
            observed.append(
                f"Study Progress: {completed_topics} of {total_topics} "
                "syllabus topics marked completed studying."
            )

        estimates: list[str] = []
        if syllabus_coverage_pct is not None:
            estimates.append(
                f"Syllabus coverage (derived from Study Progress): "
                f"{int(round(syllabus_coverage_pct))}% of official syllabus weighting."
            )
            estimates.append(
                "Estimated Knowledge is separate and grows from practice results "
                "over time — completing studying alone is not understanding."
            )
        else:
            estimates.append(
                "Estimated Knowledge cannot yet be summarised here. "
                "It grows from practice results over time."
            )

        if mission_status == "Completed":
            next_action = (
                "Session complete. Open your study plan or dashboard when you are "
                "ready for the next Current Learning Topic."
            )
        elif mission_status == "In Progress":
            next_action = (
                "Resume your Study Session for this topic, then finish when "
                "today's planned study is done."
            )
        else:
            next_action = (
                "Start your Study Session for this topic, then finish when "
                "today's planned study is done."
            )

        if (
            completed_topics is not None
            and total_topics is not None
            and total_topics > 0
        ):
            position = (
                f"You are on your Current Learning Topic after completing "
                f"{completed_topics} of {total_topics} syllabus topics studying."
            )
        else:
            position = (
                "You are on your Current Learning Topic — the next syllabus "
                "topic you have not yet completed studying."
            )

        return MissionNarrative(
            topic_title=mission_title,
            educational_purpose=(
                "Advance Study Progress along the official syllabus in Learning Mode, "
                "one clear topic at a time."
            ),
            reason_for_selection=(
                "In Learning Mode, today's mission follows your Current Learning Topic "
                "in this study plan — the next syllabus topic you have not yet "
                "completed studying."
            ),
            educational_position=position,
            next_action=next_action,
            observed_facts=tuple(observed),
            estimates=tuple(estimates),
        )

    @staticmethod
    def explain_coverage_readiness(
        *,
        readiness_percentage: float | None,
        explanation: str | None = None,
    ) -> ReadinessNarrative:
        """Narrate syllabus-coverage readiness (Derived Fact — not mastery)."""
        if readiness_percentage is None:
            return ReadinessNarrative(
                label="Syllabus coverage",
                percentage=None,
                explanation=(
                    "Syllabus coverage cannot yet be summarised. Create a study plan "
                    "and complete studying topics to unlock this figure."
                ),
                evidence_basis="No Study Progress against an official syllabus yet.",
                can_estimate=False,
                is_estimate=False,
            )

        display = int(round(readiness_percentage * 100))
        text = explanation or (
            f"You have completed studying topics representing {display}% of the "
            "official syllabus weighting."
        )
        if "not Estimated Knowledge" not in text:
            text = (
                f"{text} This is Learning Progress from Study Progress — "
                "not Estimated Knowledge."
            )
        return ReadinessNarrative(
            label="Syllabus coverage",
            percentage=float(display),
            explanation=text,
            evidence_basis=(
                "Derived from topics you have marked or earned as completed studying, "
                "weighted by the official syllabus."
            ),
            can_estimate=True,
            is_estimate=False,
        )

    @staticmethod
    def explain_composite_readiness(
        readiness: dict[str, Any] | None,
    ) -> ReadinessNarrative:
        """Narrate composite readiness as an estimate with supporting basis.

        Does not recalculate the score — only explains an existing readiness dict
        from ReadinessService.get_overall_readiness.
        """
        from app.services.product_communication_service import (
            ProductCommunicationService,
        )

        if not readiness or readiness.get("total_topics", 0) <= 0:
            return ReadinessNarrative(
                label=ProductCommunicationService.ESTIMATED_READINESS_LABEL,
                percentage=None,
                explanation=ProductCommunicationService.READINESS_UNAVAILABLE,
                evidence_basis=(
                    "No syllabus topics available for this student yet. "
                    + ProductCommunicationService.READINESS_UNAVAILABLE_BASIS
                ),
                can_estimate=False,
                is_estimate=True,
            )

        topics_started = int(readiness.get("topics_started") or 0)
        score = float(readiness.get("score") or 0.0)

        if topics_started <= 0 and score <= 0:
            return ReadinessNarrative(
                label=ProductCommunicationService.ESTIMATED_READINESS_LABEL,
                percentage=None,
                explanation=ProductCommunicationService.READINESS_UNAVAILABLE,
                evidence_basis=(
                    "No topics started yet — coverage and practice history are empty. "
                    + ProductCommunicationService.READINESS_UNAVAILABLE_BASIS
                ),
                can_estimate=False,
                is_estimate=True,
            )

        coverage = float(readiness.get("coverage_pct") or 0.0)
        avg_mastery = float(readiness.get("avg_mastery") or 0.0)
        review = float(readiness.get("review_discipline") or 0.0)

        return ReadinessNarrative(
            label=ProductCommunicationService.ESTIMATED_READINESS_LABEL,
            percentage=float(int(round(score))),
            explanation=(
                f"Estimated readiness is about {int(round(score))}%. "
                "This is a provisional study-preparation judgement — not proof "
                "that the syllabus is fully understood."
            ),
            evidence_basis=(
                f"Based on syllabus coverage (~{int(round(coverage))}%), "
                f"average Estimated Knowledge across started topics "
                f"(~{int(round(avg_mastery))}%), and recent review habits "
                f"(~{int(round(review))}%). "
                f"{ProductCommunicationService.ESTIMATED_READINESS_SELF_REPORT}"
            ),
            can_estimate=True,
            is_estimate=True,
        )

    @staticmethod
    def explain_recommendation(
        recommendation: dict[str, Any],
    ) -> RecommendationNarrative:
        """Split a legacy recommendation dict into Observed / Estimate / Advice.

        Preserves educational meaning already present in title/reason; does not
        re-rank or invent new recommendation targets.
        """
        category = (recommendation.get("category") or "").strip()
        title = (recommendation.get("title") or "Today's suggested focus").strip()
        reason = (recommendation.get("reason") or "").strip()
        benefit = (recommendation.get("expected_benefit") or "").strip()

        builder = {
            "Review": EducationalExplainabilityService._narrative_review,
            "Weak Topic": EducationalExplainabilityService._narrative_weak_topic,
            "New Topic": EducationalExplainabilityService._narrative_new_topic,
            "Mock Exam": EducationalExplainabilityService._narrative_mock,
            "Rest": EducationalExplainabilityService._narrative_rest,
            "Revision": EducationalExplainabilityService._narrative_revision,
            "Exam Technique": (
                EducationalExplainabilityService._narrative_exam_technique
            ),
        }.get(category, EducationalExplainabilityService._narrative_generic)

        return builder(title=title, reason=reason, benefit=benefit, raw=recommendation)

    @staticmethod
    def enrich_recommendations(
        recommendations: list[dict] | None,
    ) -> list[dict]:
        """Attach narrative fields onto recommendation dicts for templates."""
        if not recommendations:
            return []
        enriched: list[dict] = []
        for rec in recommendations:
            row = dict(rec)
            narrative = EducationalExplainabilityService.explain_recommendation(row)
            row["observed_facts"] = list(narrative.observed_facts)
            row["estimates"] = list(narrative.estimates)
            row["educational_advice"] = narrative.educational_advice
            row["next_action"] = narrative.next_action
            row["reason"] = narrative.reason
            row["expected_benefit"] = narrative.expected_benefit
            enriched.append(row)
        return enriched

    # ── Category narrators (communication only) ─────────────────────────

    @staticmethod
    def _narrative_review(
        *, title: str, reason: str, benefit: str, raw: dict[str, Any]
    ) -> RecommendationNarrative:
        del raw
        facts = (
            reason.split(".")[0].strip() + "."
            if reason
            else "Review topics are waiting on your schedule."
        )
        return RecommendationNarrative(
            observed_facts=(facts,),
            estimates=(
                "Estimated retention can fade when reviews stay overdue — "
                "this is a judgement, not proof of loss.",
            ),
            educational_advice=(
                f"Suggested: {title}. Keeping reviews current supports lasting recall."
            ),
            next_action="Open Today's Study Session or schedule a short review session.",
            reason=(
                f"Suggested: {title}. "
                "Keeping scheduled reviews current supports lasting recall."
            ),
            expected_benefit=(
                benefit or "Stay current on reviews so fewer topics slip overdue."
            ),
        )

    @staticmethod
    def _narrative_weak_topic(
        *, title: str, reason: str, benefit: str, raw: dict[str, Any]
    ) -> RecommendationNarrative:
        del raw
        estimate_line = reason if reason else (
            "Estimated Knowledge is lower on one or more started topics."
        )
        if "estimated" not in estimate_line.lower():
            estimate_line = f"Estimated: {estimate_line}"
        return RecommendationNarrative(
            observed_facts=(
                "These topics already appear in your study history as started areas.",
            ),
            estimates=(estimate_line,),
            educational_advice=(
                f"Suggested: practise the lower Estimated Knowledge areas named in "
                f"“{title}”. This is optional coaching — today's Learning Mode study session "
                "still follows your Current Learning Topic."
            ),
            next_action=(
                "Continue Today's Study Session first; "
                "optionally practise weaker topics later."
            ),
            reason=(
                f"{estimate_line} Suggested focus: foundational practice on these "
                "topics. This advice does not replace Today's Study Session."
            ),
            expected_benefit=(
                benefit
                or "Raise Estimated Knowledge on foundational topics through practice."
            ),
        )

    @staticmethod
    def _narrative_new_topic(
        *, title: str, reason: str, benefit: str, raw: dict[str, Any]
    ) -> RecommendationNarrative:
        del raw
        fact = reason if reason else "Syllabus topics remain to complete studying."
        return RecommendationNarrative(
            observed_facts=(fact,),
            estimates=(),
            educational_advice=(
                f"Suggested: {title}. "
                "Continuing syllabus order advances Study Progress."
            ),
            next_action="Open Today's Study Session to continue your Current Learning Topic.",
            reason=(
                f"{fact} Suggested next step: keep advancing through the syllabus "
                "in Learning Mode."
            ),
            expected_benefit=(
                benefit
                or "Increase syllabus coverage so fewer topics remain unstudied."
            ),
        )

    @staticmethod
    def _narrative_mock(
        *, title: str, reason: str, benefit: str, raw: dict[str, Any]
    ) -> RecommendationNarrative:
        del raw
        return RecommendationNarrative(
            observed_facts=(
                (
                    "Your study plan timeline and syllabus coverage support timed "
                    "practice when readiness estimates are mid-to-high."
                )
                if not reason
                else reason.split(".")[0].strip() + ".",
            ),
            estimates=(
                "Estimated readiness and coverage figures are provisional judgements, "
                "not proof of exam outcome.",
            ),
            educational_advice=f"Suggested: {title}.",
            next_action=(
                "Plan a mock or exam-style section when you next have a free block."
            ),
            reason=(
                f"Suggested: {title}. Timed practice helps reveal remaining gaps "
                "without treating estimates as guarantees."
            ),
            expected_benefit=(
                benefit or "Reveal remaining gaps and build exam-day familiarity."
            ),
        )

    @staticmethod
    def _narrative_rest(
        *, title: str, reason: str, benefit: str, raw: dict[str, Any]
    ) -> RecommendationNarrative:
        del raw
        fact = reason.split("Taking")[0].split("A lighter")[0].strip()
        if fact and not fact.endswith("."):
            fact = fact + "."
        return RecommendationNarrative(
            observed_facts=(
                fact or "Recent study activity shows a heavier-than-usual pattern.",
            ),
            estimates=(),
            educational_advice=f"Suggested: {title}.",
            next_action="Choose a lighter session or a rest day, then return tomorrow.",
            reason=(
                f"{fact or 'Recent study patterns look heavy.'} "
                f"Suggested: {title}."
            ),
            expected_benefit=benefit or "Protect focus while keeping study momentum.",
        )

    @staticmethod
    def _narrative_revision(
        *, title: str, reason: str, benefit: str, raw: dict[str, Any]
    ) -> RecommendationNarrative:
        del raw
        return RecommendationNarrative(
            observed_facts=(reason or "Exam date is approaching on your study plan.",),
            estimates=(),
            educational_advice=f"Suggested: {title}.",
            next_action="Shift spare study blocks toward consolidation and revision.",
            reason=(
                f"{reason} Suggested: {title}." if reason else f"Suggested: {title}."
            ),
            expected_benefit=benefit or "Consolidate coverage before the exam.",
        )

    @staticmethod
    def _narrative_exam_technique(
        *, title: str, reason: str, benefit: str, raw: dict[str, Any]
    ) -> RecommendationNarrative:
        del raw
        return RecommendationNarrative(
            observed_facts=(
                reason or "Your exam date is within the final preparation window.",
            ),
            estimates=(),
            educational_advice=f"Suggested: {title}.",
            next_action="Add a short timing or technique drill to an upcoming session.",
            reason=(
                f"{reason} Suggested: {title}." if reason else f"Suggested: {title}."
            ),
            expected_benefit=(
                benefit or "Improve pacing and exam technique alongside content study."
            ),
        )

    @staticmethod
    def _narrative_generic(
        *, title: str, reason: str, benefit: str, raw: dict[str, Any]
    ) -> RecommendationNarrative:
        del raw
        facts = (
            (reason,)
            if reason
            else ("Your active study plan guides today's focus.",)
        )
        return RecommendationNarrative(
            observed_facts=facts,
            estimates=(),
            educational_advice=f"Suggested: {title}.",
            next_action="Open Today's Study Session to take the next clear step.",
            reason=reason or f"Suggested: {title}.",
            expected_benefit=benefit or "Reduce decisions and keep learning moving.",
        )

    # ── LXP-004 Study Session Feedback ───────────────────────────────────

    @staticmethod
    def build_study_session_feedback(
        *,
        topic_title: str,
        scenario: str,
        questions_attempted: int | None = None,
        questions_correct: int | None = None,
        duration_minutes: int | None = None,
        study_progress_updated: bool = False,
        mission_status: str = "Completed",
    ) -> StudySessionFeedbackNarrative:
        """Build truthful post-session feedback after Practice Outcome Capture.

        Presentation only — does not recalculate estimates, readiness, or
        recommendations. Never claims knowledge, mastery, or readiness increased.

        Args:
            topic_title: Student-facing topic label for today's session.
            scenario: One of StudySessionService FEEDBACK_* scenario constants.
            questions_attempted: Recorded practice count when applicable.
            questions_correct: Recorded correct count when applicable.
            duration_minutes: Optional reported practice duration.
            study_progress_updated: Whether Study Progress was lawfully updated.
            mission_status: Current mission status after the session.

        Returns:
            Structured feedback narrative for the recorded / feedback screen.
        """
        topic = (topic_title or "Today's topic").strip()
        from app.services.study_session_service import (
            FEEDBACK_ABANDONED,
            FEEDBACK_NO_PRACTICE,
            FEEDBACK_PARTIAL,
            FEEDBACK_PRACTICE_RECORDED,
        )

        if scenario == FEEDBACK_PRACTICE_RECORDED:
            return EducationalExplainabilityService._feedback_practice_recorded(
                topic=topic,
                questions_attempted=questions_attempted or 0,
                questions_correct=questions_correct or 0,
                duration_minutes=duration_minutes,
            )
        if scenario == FEEDBACK_NO_PRACTICE:
            return EducationalExplainabilityService._feedback_no_practice(
                topic=topic,
                study_progress_updated=study_progress_updated,
            )
        if scenario == FEEDBACK_PARTIAL:
            return EducationalExplainabilityService._feedback_partial_session(
                topic=topic,
                study_progress_updated=study_progress_updated,
            )
        if scenario == FEEDBACK_ABANDONED:
            return EducationalExplainabilityService._feedback_abandoned_session(
                topic=topic,
                mission_status=mission_status,
            )

        return EducationalExplainabilityService._feedback_no_practice(
            topic=topic,
            study_progress_updated=study_progress_updated,
        )

    @staticmethod
    def _feedback_practice_recorded(
        *,
        topic: str,
        questions_attempted: int,
        questions_correct: int,
        duration_minutes: int | None,
    ) -> StudySessionFeedbackNarrative:
        from app.services.study_session_service import FEEDBACK_PRACTICE_RECORDED

        happened = [
            "You completed today's study session.",
            f"You studied {topic}.",
            f"You attempted {questions_attempted} practice question"
            f"{'s' if questions_attempted != 1 else ''}.",
            f"You answered {questions_correct} correctly.",
        ]
        from app.services.product_communication_service import (
            ProductCommunicationService,
        )

        observed = [
            ProductCommunicationService.PRACTICE_RESULTS_BASIS,
            "You recorded practice question counts for today's session.",
        ]
        if duration_minutes is not None and duration_minutes > 0:
            observed.append(
                f"You reported {duration_minutes} minute"
                f"{'s' if duration_minutes != 1 else ''} spent on practice questions."
            )

        conclusions = [
            "Practice outcomes have been recorded.",
            (
                "Future educational guidance can become more reliable as "
                "additional practice sessions are completed."
            ),
            (
                "Estimated Knowledge updates are based on your recorded "
                "practice outcomes."
            ),
        ]

        return StudySessionFeedbackNarrative(
            what_happened=tuple(happened),
            what_observed=tuple(observed),
            honest_conclusions=tuple(conclusions),
            what_next=(
                "Tomorrow's mission will continue your current learning journey. "
                "Keep studying consistently to build a stronger picture of your "
                "understanding."
            ),
            scenario=FEEDBACK_PRACTICE_RECORDED,
        )

    @staticmethod
    def _feedback_no_practice(
        *,
        topic: str,
        study_progress_updated: bool,
    ) -> StudySessionFeedbackNarrative:
        from app.services.study_session_service import FEEDBACK_NO_PRACTICE

        happened = [
            "You completed today's study session.",
            f"You studied {topic}.",
            "No practice questions were recorded today.",
        ]
        observed = [
            "You closed today's session without practice question counts.",
        ]
        conclusions = [
            (
                "No practice outcomes were available today, so Kwalitec cannot yet "
                "update its educational estimates for this topic."
            ),
        ]
        if study_progress_updated:
            conclusions.append(
                "Today's planned study was recorded — separate from practice results."
            )

        return StudySessionFeedbackNarrative(
            what_happened=tuple(happened),
            what_observed=tuple(observed),
            honest_conclusions=tuple(conclusions),
            what_next=(
                "Tomorrow's mission will continue your current learning journey. "
                "When you practise questions, record your results so future guidance "
                "can reflect your practice."
            ),
            scenario=FEEDBACK_NO_PRACTICE,
        )

    @staticmethod
    def _feedback_partial_session(
        *,
        topic: str,
        study_progress_updated: bool,
    ) -> StudySessionFeedbackNarrative:
        from app.services.study_session_service import FEEDBACK_PARTIAL

        happened = [
            "You partially completed today's study session.",
            f"You studied {topic}.",
            "Today's planned study was not fully finished.",
        ]
        observed = [
            "You reported that today's planned study was only partially completed.",
            "No practice question counts were recorded.",
        ]
        conclusions = [
            (
                "Today's session was recorded as partial. Kwalitec cannot treat "
                "this as full planned study or update practice-based guidance "
                "for this topic."
            ),
        ]
        if not study_progress_updated:
            conclusions.append("Your study progress was not advanced.")

        return StudySessionFeedbackNarrative(
            what_happened=tuple(happened),
            what_observed=tuple(observed),
            honest_conclusions=tuple(conclusions),
            what_next=(
                "You can return to finish remaining study for this topic when you "
                "are ready. Tomorrow's mission will continue your current learning "
                "journey."
            ),
            scenario=FEEDBACK_PARTIAL,
        )

    @staticmethod
    def _feedback_abandoned_session(
        *,
        topic: str,
        mission_status: str,
    ) -> StudySessionFeedbackNarrative:
        from app.services.study_session_service import FEEDBACK_ABANDONED

        happened = [
            "Today's study session was not completed.",
            f"Today's topic is {topic}.",
        ]
        observed = [
            "You reported that today's planned study did not happen.",
        ]
        if mission_status == "In Progress":
            observed.append(
                "Today's mission remains open so you can study when you are ready."
            )

        conclusions = [
            (
                "Nothing from today changes your practice-based guidance. "
                "No practice outcomes were recorded."
            ),
        ]

        return StudySessionFeedbackNarrative(
            what_happened=tuple(happened),
            what_observed=tuple(observed),
            honest_conclusions=tuple(conclusions),
            what_next=(
                "Return to Today's Study Session when you are ready to study. "
                "You can start a fresh study session for this topic."
            ),
            scenario=FEEDBACK_ABANDONED,
        )
