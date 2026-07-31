"""Deterministic Learning Strategy decision rules (KWP-007).

Priority-ordered rules. Extends educational patterns already present in
Twin RecommendationPolicy, Adaptive revision urgency, and Progress advance
gates — does not re-validate evidence or re-rank Runtime A decisions.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.learning_strategy.calibration import (
    calibrate,
    performance_band,
)
from app.application.learning_strategy.dto import (
    ConfidenceCalibration,
    StrategyAction,
    StrategyEvidenceInput,
)

# Long gap since practice — align with spaced-revision medium/long windows.
_LONG_GAP_DAYS = 14
_REPEATED_INCORRECT_MIN = 2


@dataclass(frozen=True)
class StrategyDecision:
    """Internal decision before explainability packaging."""

    action: StrategyAction
    rule_id: str
    reason_codes: tuple[str, ...]
    calibration: ConfidenceCalibration


def select_strategy(evidence: StrategyEvidenceInput) -> StrategyDecision:
    """Apply priority-ordered deterministic strategy rules."""
    calibration = calibrate(evidence)
    perf = performance_band(evidence)
    correct = evidence.practice_correct
    incorrect = evidence.practice_incorrect
    unscored = evidence.practice_unscored

    # 1. Recovery — abandoned / interrupted / retention risk with weakness
    if evidence.abandoned:
        return StrategyDecision(
            action=StrategyAction.RECOVER_PRIOR_KNOWLEDGE,
            rule_id="recover_abandoned",
            reason_codes=("abandoned_session", "recover_prior"),
            calibration=calibration,
        )
    if evidence.retention_risk and (
        evidence.weak_topic or incorrect > 0 or perf == "weak"
    ):
        return StrategyDecision(
            action=StrategyAction.RECOVER_PRIOR_KNOWLEDGE,
            rule_id="recover_retention_risk",
            reason_codes=("retention_risk", "recover_prior"),
            calibration=calibration,
        )
    if (
        evidence.days_since_topic_practice is not None
        and evidence.days_since_topic_practice >= _LONG_GAP_DAYS
        and (evidence.weak_topic or incorrect > correct)
    ):
        return StrategyDecision(
            action=StrategyAction.RECOVER_PRIOR_KNOWLEDGE,
            rule_id="recover_long_gap_weak",
            reason_codes=("long_gap", "weak_signal", "recover_prior"),
            calibration=calibration,
        )

    # 2. Incorrect + high confidence → conceptual misunderstanding → consolidate
    if incorrect > 0 and calibration is ConfidenceCalibration.OVER_CONFIDENT:
        return StrategyDecision(
            action=StrategyAction.CONSOLIDATE_UNDERSTANDING,
            rule_id="consolidate_overconfident_errors",
            reason_codes=(
                "incorrect_outcomes",
                "confidence_performance_mismatch",
                "conceptual_check",
            ),
            calibration=calibration,
        )

    # 3. Repeated incorrect → consolidate / immediate reinforcement
    if incorrect >= _REPEATED_INCORRECT_MIN and correct == 0:
        return StrategyDecision(
            action=StrategyAction.IMMEDIATE_REINFORCEMENT,
            rule_id="reinforce_repeated_incorrect",
            reason_codes=("repeated_incorrect", "immediate_reinforcement"),
            calibration=calibration,
        )
    if incorrect >= _REPEATED_INCORRECT_MIN and incorrect > correct:
        return StrategyDecision(
            action=StrategyAction.CONSOLIDATE_UNDERSTANDING,
            rule_id="consolidate_repeated_incorrect",
            reason_codes=("repeated_incorrect", "consolidate"),
            calibration=calibration,
        )

    # 4. Correct but low confidence → practice for certainty
    if (
        correct > 0
        and incorrect == 0
        and calibration is ConfidenceCalibration.UNDER_CONFIDENT
    ):
        return StrategyDecision(
            action=StrategyAction.PRACTICE_FOR_CERTAINTY,
            rule_id="practice_underconfident_correct",
            reason_codes=(
                "correct_outcomes",
                "low_confidence",
                "build_certainty",
            ),
            calibration=calibration,
        )

    # 5. Repeated partial understanding → slow progression
    if evidence.consecutive_partial_finishes >= 2:
        return StrategyDecision(
            action=StrategyAction.SLOW_PROGRESSION,
            rule_id="slow_repeated_partial",
            reason_codes=("repeated_partial", "slow_progression"),
            calibration=calibration,
        )
    if (
        evidence.finish_verdict == "partially"
        and (incorrect > 0 or unscored > 0)
    ):
        return StrategyDecision(
            action=StrategyAction.SLOW_PROGRESSION,
            rule_id="slow_partial_mixed",
            reason_codes=("partial_finish", "mixed_practice", "slow_progression"),
            calibration=calibration,
        )

    # 6. Single incorrect cluster → reinforce or repeat
    if incorrect > 0 and correct == 0:
        return StrategyDecision(
            action=StrategyAction.REPEAT_PRACTICE,
            rule_id="repeat_all_incorrect",
            reason_codes=("incorrect_outcomes", "repeat_practice"),
            calibration=calibration,
        )
    if incorrect > 0:
        return StrategyDecision(
            action=StrategyAction.IMMEDIATE_REINFORCEMENT,
            rule_id="reinforce_mixed_errors",
            reason_codes=("mixed_practice", "immediate_reinforcement"),
            calibration=calibration,
        )

    # 7. Long gap since mastery / strong prior → scheduled revision
    if (
        evidence.days_since_topic_practice is not None
        and evidence.days_since_topic_practice >= _LONG_GAP_DAYS
        and perf in {"strong", "unknown"}
        and not evidence.progress_advanced
    ):
        return StrategyDecision(
            action=StrategyAction.SCHEDULED_REVISION,
            rule_id="schedule_long_gap_reinforcement",
            reason_codes=("long_gap", "scheduled_revision"),
            calibration=calibration,
        )
    if evidence.retention_risk and perf != "weak":
        return StrategyDecision(
            action=StrategyAction.SCHEDULED_REVISION,
            rule_id="schedule_retention_reinforcement",
            reason_codes=("retention_risk", "scheduled_revision"),
            calibration=calibration,
        )

    # 8. Strong sustained performance → advance or increase challenge
    if (
        correct > 0
        and incorrect == 0
        and evidence.progress_advanced
        and evidence.consecutive_strong_sittings >= 2
        and calibration
        in {ConfidenceCalibration.HEALTHY, ConfidenceCalibration.UNKNOWN}
    ):
        return StrategyDecision(
            action=StrategyAction.INCREASE_CHALLENGE,
            rule_id="challenge_sustained_strong",
            reason_codes=("sustained_strong", "increase_challenge"),
            calibration=calibration,
        )
    if (
        correct > 0
        and incorrect == 0
        and (evidence.progress_advanced or evidence.mission_completed)
        and evidence.finish_verdict in {"yes", ""}
    ):
        return StrategyDecision(
            action=StrategyAction.ADVANCE_TOPIC,
            rule_id="advance_strong_accepted",
            reason_codes=("strong_performance", "accepted_study", "advance"),
            calibration=calibration,
        )
    if correct > 0 and incorrect == 0 and evidence.finish_verdict == "yes":
        return StrategyDecision(
            action=StrategyAction.ADVANCE_TOPIC,
            rule_id="advance_strong_finish",
            reason_codes=("strong_performance", "honest_finish", "advance"),
            calibration=calibration,
        )

    # 9. Default — maintain pace
    return StrategyDecision(
        action=StrategyAction.MAINTAIN_CURRENT_PACE,
        rule_id="maintain_default",
        reason_codes=("insufficient_signal_for_change", "maintain_pace"),
        calibration=calibration,
    )
