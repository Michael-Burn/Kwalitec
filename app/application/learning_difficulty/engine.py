"""Learning Difficulty Engine — Educational Intelligence Phase 3 (KWP-009).

Deterministic modelling of topic difficulty, learner-specific difficulty,
learning effort, educational pacing, session intensity, and revision
pressure. Produces recommendations — never scores as product, never AI,
never psychological labels.

MUST NOT redesign Learning Strategy, Learning Diagnostics,
LearningSessionRuntime, EducationalEvidenceAuthority, StudentTwinEngine,
ProgressEngine, Mission Runtime, Commercial Loop, or Session FSM.
"""

from __future__ import annotations

import logging
from typing import Any

from app.application.learning_difficulty.dto import (
    DifficultyEvidenceInput,
    DifficultyProfile,
)
from app.application.learning_difficulty.guidance import (
    explanation_for,
    guidance_for,
    scrub,
    title_for,
)
from app.application.learning_difficulty.rules import select_load_recommendation

logger = logging.getLogger(__name__)


class LearningDifficultyEngine:
    """Model educational demand for a topic × learner from existing evidence."""

    AUTHORITY_ID = "learning_difficulty_engine"

    def evaluate(
        self,
        evidence: DifficultyEvidenceInput | dict[str, Any] | None = None,
        *,
        opaque: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
    ) -> DifficultyProfile:
        """Return a deterministic DifficultyProfile.

        Args:
            evidence: Pre-built DifficultyEvidenceInput, or omit to build
                from opaque sitting facts.
            opaque: Sitting / completion opaque summary.
            metadata: Completion metadata pairs / dict.
            twin_signals: Optional Twin-derived enrichments (read-only).
            cadence: Optional streak / session-count enrichments.

        Returns:
            DifficultyProfile with student-safe recommendation + guidance.
        """
        if isinstance(evidence, DifficultyEvidenceInput):
            inputs = evidence
        else:
            merged_opaque = dict(opaque or {})
            if isinstance(evidence, dict):
                merged_opaque = {**merged_opaque, **evidence}
            inputs = DifficultyEvidenceInput.from_opaque(
                merged_opaque,
                metadata=metadata,
                twin_signals=twin_signals,
                cadence=cadence,
            )

        decision = select_load_recommendation(inputs)
        title = title_for(decision.recommendation)
        guidance = scrub(guidance_for(decision, inputs))
        explanation = scrub(explanation_for(decision, inputs))

        profile = DifficultyProfile(
            objective_complexity=decision.objective_complexity,
            observed_difficulty=decision.observed_difficulty,
            learning_effort=decision.learning_effort,
            educational_pacing=decision.educational_pacing,
            session_intensity=decision.session_intensity,
            revision_pressure=decision.revision_pressure,
            recommendation=decision.recommendation,
            recommendation_title=title,
            guidance=guidance,
            explanation=explanation,
            rule_id=decision.rule_id,
            load_points=decision.load_points,
            evidence_codes=decision.evidence_codes,
            topic_title=inputs.topic_title,
            metadata=(
                ("authority", self.AUTHORITY_ID),
                ("rule_id", decision.rule_id),
                ("recommendation", decision.recommendation.value),
                ("objective", decision.objective_complexity.value),
                ("observed", decision.observed_difficulty.value),
                ("pacing", decision.educational_pacing.value),
                ("intensity", decision.session_intensity.value),
            ),
        )
        logger.debug(
            "learning_difficulty rule=%s rec=%s topic=%r load=%s",
            decision.rule_id,
            decision.recommendation.value,
            inputs.topic_title,
            decision.load_points,
        )
        return profile

    def evaluate_opaque(
        self,
        opaque_summary: dict[str, Any] | None,
        *,
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
    ) -> DifficultyProfile:
        """Convenience wrapper for Sitting Report / founder projectors."""
        return self.evaluate(
            opaque=opaque_summary,
            metadata=metadata,
            twin_signals=twin_signals,
            cadence=cadence,
        )


_DEFAULT_ENGINE: LearningDifficultyEngine | None = None


def get_learning_difficulty_engine() -> LearningDifficultyEngine:
    """Process-scoped default engine instance."""
    global _DEFAULT_ENGINE
    if _DEFAULT_ENGINE is None:
        _DEFAULT_ENGINE = LearningDifficultyEngine()
    return _DEFAULT_ENGINE
