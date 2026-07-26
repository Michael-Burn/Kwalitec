"""ExperienceFeedbackAssembler — Evidence read-model → ExperienceFeedback.

Maps factual Evidence observations into presentation-ready feedback.
Does not calculate new metrics or infer educational meaning.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.adapters.evidence_platform.contracts import (
    EvidenceFactualSummary,
)
from app.infrastructure.adapters.experience_feedback.contracts import (
    AUTHORITY_EXPERIENCE_FEEDBACK,
    CONTRACT_VERSION,
    DEFAULT_SOURCE_DESCRIPTION,
    REPORTING_PERIOD_LABELS,
    ExperienceFeedback,
    ExperienceFeedbackFact,
    deterministic_feedback_id,
)

_ASSEMBLER_VIA = "experience_feedback_assembler"


class ExperienceFeedbackAssembler:
    """Convert EvidenceFactualSummary into immutable ExperienceFeedback.

    Responsibilities:
    - map factual observations
    - format presentation-ready summaries
    - preserve provenance

    Non-responsibilities: new metric calculation, educational inference,
    scoring, recommendations, Evidence writes, repository access.
    """

    ASSEMBLER_VERSION = "1.0.0-p2.ms008"

    def assemble(
        self,
        summary: EvidenceFactualSummary,
        *,
        generated_at: str | None = None,
    ) -> ExperienceFeedback:
        """Map an Evidence factual summary into ExperienceFeedback."""
        if not isinstance(summary, EvidenceFactualSummary):
            raise TypeError("summary must be an EvidenceFactualSummary")
        as_of = (generated_at or summary.generated_at or "").strip()
        if not as_of:
            # Deterministic placeholder — no wall-clock invent when Evidence
            # retained no timestamps (empty observation buffer).
            as_of = f"period:{(summary.reporting_period or 'this_week').strip()}"
        source = (
            (summary.source_description or "").strip() or DEFAULT_SOURCE_DESCRIPTION
        )
        period = (summary.reporting_period or "this_week").strip().lower()
        period_label = REPORTING_PERIOD_LABELS.get(
            period, period.replace("_", " ").title()
        )
        facts = (
            ExperienceFeedbackFact(
                key="completed_missions",
                label="Missions completed this week"
                if period == "this_week"
                else "Missions completed",
                value=summary.completed_missions,
                value_label=_count_label(
                    summary.completed_missions, singular="mission", plural="missions"
                ),
                source_description=source,
            ),
            ExperienceFeedbackFact(
                key="study_sessions",
                label="Study sessions completed",
                value=summary.study_sessions,
                value_label=_count_label(
                    summary.study_sessions, singular="session", plural="sessions"
                ),
                source_description=source,
            ),
            ExperienceFeedbackFact(
                key="completed_reflections",
                label="Reflection consistency",
                value=summary.completed_reflections,
                value_label=_count_label(
                    summary.completed_reflections,
                    singular="reflection",
                    plural="reflections",
                ),
                source_description=source,
            ),
            ExperienceFeedbackFact(
                key="active_streak",
                label="Current study streak",
                value=summary.active_streak,
                value_label=_streak_label(summary.active_streak),
                source_description=source,
            ),
        )
        evidence_summary_id = (summary.summary_id or "").strip()
        feedback_id = deterministic_feedback_id(
            student_id=summary.student_id,
            reporting_period=period,
            completed_missions=summary.completed_missions,
            completed_reflections=summary.completed_reflections,
            study_sessions=summary.study_sessions,
            active_streak=summary.active_streak,
            generated_at=as_of,
            evidence_summary_id=evidence_summary_id,
        )
        provenance: dict[str, Any] = {
            "via": _ASSEMBLER_VIA,
            "assembler_version": self.ASSEMBLER_VERSION,
            "evidence_authority": summary.authority,
            "evidence_summary_id": evidence_summary_id,
            "evidence_provenance": dict(summary.provenance),
            "evidence_refs": list(summary.evidence_refs),
        }
        return ExperienceFeedback(
            feedback_id=feedback_id,
            reporting_period=period,
            completed_missions=summary.completed_missions,
            completed_reflections=summary.completed_reflections,
            study_sessions=summary.study_sessions,
            active_streak=summary.active_streak,
            generated_at=as_of,
            facts=facts,
            student_id=summary.student_id,
            evidence_summary_id=evidence_summary_id,
            evidence_refs=tuple(summary.evidence_refs),
            provenance=provenance,
            source_description=source,
            reporting_period_label=period_label,
            contract_version=CONTRACT_VERSION,
            authority=AUTHORITY_EXPERIENCE_FEEDBACK,
        )


def _count_label(count: int, *, singular: str, plural: str) -> str:
    unit = singular if count == 1 else plural
    return f"{count} {unit}"


def _streak_label(days: int) -> str:
    if days <= 0:
        return "No active streak"
    if days == 1:
        return "1 day"
    return f"{days} days"


def build_experience_feedback_assembler(
    *,
    enabled: bool,
) -> ExperienceFeedbackAssembler | None:
    """DI helper — construct assembler only when ENABLE_EXPERIENCE_FEEDBACK is ON."""
    if not enabled:
        return None
    return ExperienceFeedbackAssembler()


__all__ = [
    "ExperienceFeedbackAssembler",
    "build_experience_feedback_assembler",
]
