"""Deterministic intervention effectiveness rules (KWP-010).

Answers the educational questions:
- Did consolidation help?
- Did reduced session length help?
- Did increased spacing help?
- Did challenge improve performance?
- Did reinforcement reduce mistakes?

No AI. Same inputs → same verdict + rule_id.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.intervention_effectiveness.dto import (
    EffectivenessEvidenceInput,
    EffectivenessVerdict,
    InterventionKind,
)


@dataclass(frozen=True)
class EffectivenessDecision:
    verdict: EffectivenessVerdict
    rule_id: str
    evidence_codes: tuple[str, ...]
    intervention_kind: InterventionKind


def evaluate_effectiveness(
    evidence: EffectivenessEvidenceInput,
) -> EffectivenessDecision:
    """Select a deterministic effectiveness verdict from prior + subsequent."""
    prior = evidence.prior
    kind = prior.kind

    if not prior.has_recommendation and kind is InterventionKind.OTHER:
        return EffectivenessDecision(
            verdict=EffectivenessVerdict.INSUFFICIENT_EVIDENCE,
            rule_id="eff.insufficient.no_prior",
            evidence_codes=("no_prior_recommendation",),
            intervention_kind=InterventionKind.OTHER,
        )

    subsequent_practice = (
        evidence.practice_attempted > 0
        or evidence.practice_correct + evidence.practice_incorrect > 0
    )
    if not subsequent_practice and not evidence.progress_advanced:
        return EffectivenessDecision(
            verdict=EffectivenessVerdict.INSUFFICIENT_EVIDENCE,
            rule_id="eff.insufficient.no_subsequent",
            evidence_codes=("no_subsequent_practice",),
            intervention_kind=kind,
        )

    # Abandoned after intervention → ineffective unless recovery still mid-flight.
    if evidence.abandoned and kind is not InterventionKind.RECOVERY:
        return EffectivenessDecision(
            verdict=EffectivenessVerdict.INEFFECTIVE,
            rule_id="eff.abandoned",
            evidence_codes=("subsequent_abandoned",),
            intervention_kind=kind,
        )

    if kind is InterventionKind.CONSOLIDATION:
        return _consolidation(evidence)
    if kind is InterventionKind.REINFORCEMENT:
        return _reinforcement(evidence)
    if kind is InterventionKind.REDUCE_SESSION_LENGTH:
        return _reduce_length(evidence)
    if kind is InterventionKind.INCREASE_SPACING:
        return _increase_spacing(evidence)
    if kind is InterventionKind.DECREASE_SPACING:
        return _decrease_spacing(evidence)
    if kind is InterventionKind.INCREASE_CHALLENGE:
        return _increase_challenge(evidence)
    if kind is InterventionKind.RECOVERY:
        return _recovery(evidence)
    if kind is InterventionKind.SLOW_PROGRESSION:
        return _slow_progression(evidence)
    if kind is InterventionKind.ADVANCE:
        return _advance(evidence)
    return _maintain(evidence)


def _accuracy(correct: int, incorrect: int) -> float | None:
    total = correct + incorrect
    if total <= 0:
        return None
    return correct / total


def _delta_incorrect(evidence: EffectivenessEvidenceInput) -> int | None:
    if not evidence.prior.has_baseline_practice:
        return None
    return evidence.practice_incorrect - evidence.prior.baseline_incorrect


def _improved_accuracy(evidence: EffectivenessEvidenceInput) -> bool | None:
    prior = evidence.prior
    if not prior.has_baseline_practice:
        return None
    before = _accuracy(prior.baseline_correct, prior.baseline_incorrect)
    after = _accuracy(evidence.practice_correct, evidence.practice_incorrect)
    if before is None or after is None:
        return None
    return after > before + 0.05


def _strong_sitting(evidence: EffectivenessEvidenceInput) -> bool:
    after = _accuracy(evidence.practice_correct, evidence.practice_incorrect)
    if after is not None and after >= 0.67 and evidence.practice_incorrect <= 1:
        return True
    if evidence.progress_advanced and evidence.practice_incorrect == 0:
        return True
    if evidence.finish_verdict == "yes" and evidence.practice_incorrect == 0:
        return True
    return False


def _weak_sitting(evidence: EffectivenessEvidenceInput) -> bool:
    if evidence.weak_topic or evidence.retention_risk:
        return True
    after = _accuracy(evidence.practice_correct, evidence.practice_incorrect)
    if after is not None and after < 0.4:
        return True
    if evidence.practice_incorrect >= 2 and evidence.practice_correct == 0:
        return True
    return False


def _consolidation(evidence: EffectivenessEvidenceInput) -> EffectivenessDecision:
    improved = _improved_accuracy(evidence)
    delta_inc = _delta_incorrect(evidence)
    strong = _strong_sitting(evidence)
    weak = _weak_sitting(evidence)
    codes: list[str] = ["kind_consolidation"]

    if strong and (improved is True or (delta_inc is not None and delta_inc < 0)):
        codes.append("accuracy_up")
        if evidence.progress_advanced:
            codes.append("progress_advanced")
        return EffectivenessDecision(
            EffectivenessVerdict.EFFECTIVE,
            "eff.consolidation.effective",
            tuple(codes),
            InterventionKind.CONSOLIDATION,
        )
    if improved is True or (delta_inc is not None and delta_inc < 0):
        codes.append("partial_improvement")
        if weak:
            codes.append("still_weak")
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.consolidation.partial",
            tuple(codes),
            InterventionKind.CONSOLIDATION,
        )
    if evidence.recovered_after_misses and not weak:
        codes.append("recovered_after_misses")
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.consolidation.recovered",
            tuple(codes),
            InterventionKind.CONSOLIDATION,
        )
    if improved is None and not evidence.prior.has_baseline_practice:
        # Subsequent strong without baseline → partial credit for consolidation.
        if strong:
            codes.append("strong_without_baseline")
            return EffectivenessDecision(
                EffectivenessVerdict.PARTIALLY_EFFECTIVE,
                "eff.consolidation.strong_no_baseline",
                tuple(codes),
                InterventionKind.CONSOLIDATION,
            )
        return EffectivenessDecision(
            EffectivenessVerdict.INSUFFICIENT_EVIDENCE,
            "eff.consolidation.insufficient_baseline",
            ("missing_baseline",),
            InterventionKind.CONSOLIDATION,
        )
    codes.append("no_improvement")
    return EffectivenessDecision(
        EffectivenessVerdict.INEFFECTIVE,
        "eff.consolidation.ineffective",
        tuple(codes),
        InterventionKind.CONSOLIDATION,
    )


def _reinforcement(evidence: EffectivenessEvidenceInput) -> EffectivenessDecision:
    improved = _improved_accuracy(evidence)
    delta_inc = _delta_incorrect(evidence)
    strong = _strong_sitting(evidence)
    codes: list[str] = ["kind_reinforcement"]

    mistakes_down = delta_inc is not None and delta_inc < 0
    if mistakes_down and (strong or improved is True):
        codes.extend(["mistakes_down", "accuracy_up"])
        return EffectivenessDecision(
            EffectivenessVerdict.EFFECTIVE,
            "eff.reinforcement.effective",
            tuple(codes),
            InterventionKind.REINFORCEMENT,
        )
    if mistakes_down or improved is True or evidence.recovered_after_misses:
        codes.append("mistakes_reduced_or_recovered")
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.reinforcement.partial",
            tuple(codes),
            InterventionKind.REINFORCEMENT,
        )
    if delta_inc is None and strong:
        codes.append("strong_without_baseline")
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.reinforcement.strong_no_baseline",
            tuple(codes),
            InterventionKind.REINFORCEMENT,
        )
    if delta_inc is None and not evidence.prior.has_baseline_practice:
        return EffectivenessDecision(
            EffectivenessVerdict.INSUFFICIENT_EVIDENCE,
            "eff.reinforcement.insufficient_baseline",
            ("missing_baseline",),
            InterventionKind.REINFORCEMENT,
        )
    codes.append("mistakes_persist")
    return EffectivenessDecision(
        EffectivenessVerdict.INEFFECTIVE,
        "eff.reinforcement.ineffective",
        tuple(codes),
        InterventionKind.REINFORCEMENT,
    )


def _reduce_length(evidence: EffectivenessEvidenceInput) -> EffectivenessDecision:
    codes: list[str] = ["kind_reduce_length"]
    prior_dur = evidence.prior.baseline_duration_minutes
    curr_dur = evidence.session_duration_minutes
    shorter = (
        prior_dur is not None
        and curr_dur is not None
        and curr_dur < prior_dur
        and curr_dur > 0
    )
    not_worse = not _weak_sitting(evidence)
    improved = _improved_accuracy(evidence)
    strong = _strong_sitting(evidence)

    if shorter and (strong or improved is True or not_worse):
        codes.append("duration_down")
        if strong or improved is True:
            codes.append("performance_held_or_improved")
            return EffectivenessDecision(
                EffectivenessVerdict.EFFECTIVE,
                "eff.reduce_length.effective",
                tuple(codes),
                InterventionKind.REDUCE_SESSION_LENGTH,
            )
        codes.append("performance_stable")
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.reduce_length.partial",
            tuple(codes),
            InterventionKind.REDUCE_SESSION_LENGTH,
        )
    if shorter and _weak_sitting(evidence):
        codes.extend(["duration_down", "still_weak"])
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.reduce_length.partial_weak",
            tuple(codes),
            InterventionKind.REDUCE_SESSION_LENGTH,
        )
    if prior_dur is None or curr_dur is None:
        # Without duration, fall back to performance-only signal.
        if strong or improved is True:
            codes.append("performance_only")
            return EffectivenessDecision(
                EffectivenessVerdict.PARTIALLY_EFFECTIVE,
                "eff.reduce_length.performance_only",
                tuple(codes),
                InterventionKind.REDUCE_SESSION_LENGTH,
            )
        return EffectivenessDecision(
            EffectivenessVerdict.INSUFFICIENT_EVIDENCE,
            "eff.reduce_length.insufficient_duration",
            ("missing_duration",),
            InterventionKind.REDUCE_SESSION_LENGTH,
        )
    codes.append("duration_not_reduced")
    return EffectivenessDecision(
        EffectivenessVerdict.INEFFECTIVE,
        "eff.reduce_length.ineffective",
        tuple(codes),
        InterventionKind.REDUCE_SESSION_LENGTH,
    )


def _increase_spacing(evidence: EffectivenessEvidenceInput) -> EffectivenessDecision:
    codes: list[str] = ["kind_increase_spacing"]
    gap = evidence.days_since_topic_practice
    strong = _strong_sitting(evidence)
    weak = _weak_sitting(evidence)

    if weak or evidence.retention_risk:
        codes.append("retention_struggle")
        return EffectivenessDecision(
            EffectivenessVerdict.INEFFECTIVE,
            "eff.increase_spacing.ineffective",
            tuple(codes),
            InterventionKind.INCREASE_SPACING,
        )
    if strong and (gap is None or gap >= 2):
        codes.append("stable_after_space")
        return EffectivenessDecision(
            EffectivenessVerdict.EFFECTIVE,
            "eff.increase_spacing.effective",
            tuple(codes),
            InterventionKind.INCREASE_SPACING,
        )
    if not weak and evidence.finish_verdict in {"yes", "partially"}:
        codes.append("held_after_space")
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.increase_spacing.partial",
            tuple(codes),
            InterventionKind.INCREASE_SPACING,
        )
    if gap is None and not strong:
        return EffectivenessDecision(
            EffectivenessVerdict.INSUFFICIENT_EVIDENCE,
            "eff.increase_spacing.insufficient",
            ("missing_gap_signal",),
            InterventionKind.INCREASE_SPACING,
        )
    return EffectivenessDecision(
        EffectivenessVerdict.PARTIALLY_EFFECTIVE,
        "eff.increase_spacing.neutral",
        tuple(codes + ["neutral_hold"]),
        InterventionKind.INCREASE_SPACING,
    )


def _decrease_spacing(evidence: EffectivenessEvidenceInput) -> EffectivenessDecision:
    codes: list[str] = ["kind_decrease_spacing"]
    improved = _improved_accuracy(evidence)
    strong = _strong_sitting(evidence)
    weak = _weak_sitting(evidence)

    if strong or (improved is True and not weak):
        codes.append("closer_practice_helped")
        return EffectivenessDecision(
            EffectivenessVerdict.EFFECTIVE,
            "eff.decrease_spacing.effective",
            tuple(codes),
            InterventionKind.DECREASE_SPACING,
        )
    if improved is True or evidence.recovered_after_misses:
        codes.append("partial_closer_practice")
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.decrease_spacing.partial",
            tuple(codes),
            InterventionKind.DECREASE_SPACING,
        )
    if weak:
        codes.append("still_weak")
        return EffectivenessDecision(
            EffectivenessVerdict.INEFFECTIVE,
            "eff.decrease_spacing.ineffective",
            tuple(codes),
            InterventionKind.DECREASE_SPACING,
        )
    if not evidence.prior.has_baseline_practice:
        return EffectivenessDecision(
            EffectivenessVerdict.INSUFFICIENT_EVIDENCE,
            "eff.decrease_spacing.insufficient",
            ("missing_baseline",),
            InterventionKind.DECREASE_SPACING,
        )
    return EffectivenessDecision(
        EffectivenessVerdict.PARTIALLY_EFFECTIVE,
        "eff.decrease_spacing.neutral",
        tuple(codes + ["neutral"]),
        InterventionKind.DECREASE_SPACING,
    )


def _increase_challenge(evidence: EffectivenessEvidenceInput) -> EffectivenessDecision:
    codes: list[str] = ["kind_increase_challenge"]
    strong = _strong_sitting(evidence)
    weak = _weak_sitting(evidence)

    if strong and (evidence.progress_advanced or evidence.finish_verdict == "yes"):
        codes.append("challenge_sustained")
        return EffectivenessDecision(
            EffectivenessVerdict.EFFECTIVE,
            "eff.challenge.effective",
            tuple(codes),
            InterventionKind.INCREASE_CHALLENGE,
        )
    if strong or (
        evidence.practice_correct > evidence.practice_incorrect
        and not weak
    ):
        codes.append("challenge_held")
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.challenge.partial",
            tuple(codes),
            InterventionKind.INCREASE_CHALLENGE,
        )
    if weak:
        codes.append("challenge_too_hard")
        return EffectivenessDecision(
            EffectivenessVerdict.INEFFECTIVE,
            "eff.challenge.ineffective",
            tuple(codes),
            InterventionKind.INCREASE_CHALLENGE,
        )
    return EffectivenessDecision(
        EffectivenessVerdict.INSUFFICIENT_EVIDENCE,
        "eff.challenge.insufficient",
        ("thin_challenge_signal",),
        InterventionKind.INCREASE_CHALLENGE,
    )


def _recovery(evidence: EffectivenessEvidenceInput) -> EffectivenessDecision:
    codes: list[str] = ["kind_recovery"]
    if evidence.abandoned:
        codes.append("still_abandoned")
        return EffectivenessDecision(
            EffectivenessVerdict.INEFFECTIVE,
            "eff.recovery.ineffective_abandon",
            tuple(codes),
            InterventionKind.RECOVERY,
        )
    if _strong_sitting(evidence) or (
        evidence.recovered_after_misses and not _weak_sitting(evidence)
    ):
        codes.append("recovered")
        return EffectivenessDecision(
            EffectivenessVerdict.EFFECTIVE,
            "eff.recovery.effective",
            tuple(codes),
            InterventionKind.RECOVERY,
        )
    if evidence.practice_attempted > 0 and not _weak_sitting(evidence):
        codes.append("re_engaged")
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.recovery.partial",
            tuple(codes),
            InterventionKind.RECOVERY,
        )
    if _weak_sitting(evidence):
        codes.append("still_weak")
        return EffectivenessDecision(
            EffectivenessVerdict.INEFFECTIVE,
            "eff.recovery.ineffective",
            tuple(codes),
            InterventionKind.RECOVERY,
        )
    return EffectivenessDecision(
        EffectivenessVerdict.INSUFFICIENT_EVIDENCE,
        "eff.recovery.insufficient",
        ("thin_recovery_signal",),
        InterventionKind.RECOVERY,
    )


def _slow_progression(evidence: EffectivenessEvidenceInput) -> EffectivenessDecision:
    codes: list[str] = ["kind_slow_progression"]
    partials = evidence.consecutive_partial_finishes
    strong = _strong_sitting(evidence)
    if strong and partials <= 1:
        codes.append("pace_stabilised")
        return EffectivenessDecision(
            EffectivenessVerdict.EFFECTIVE,
            "eff.slow.effective",
            tuple(codes),
            InterventionKind.SLOW_PROGRESSION,
        )
    if evidence.finish_verdict in {"yes", "partially"} and not _weak_sitting(evidence):
        codes.append("pace_improving")
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.slow.partial",
            tuple(codes),
            InterventionKind.SLOW_PROGRESSION,
        )
    if partials >= 2 or _weak_sitting(evidence):
        codes.append("still_unstable")
        return EffectivenessDecision(
            EffectivenessVerdict.INEFFECTIVE,
            "eff.slow.ineffective",
            tuple(codes),
            InterventionKind.SLOW_PROGRESSION,
        )
    return EffectivenessDecision(
        EffectivenessVerdict.INSUFFICIENT_EVIDENCE,
        "eff.slow.insufficient",
        ("thin_pace_signal",),
        InterventionKind.SLOW_PROGRESSION,
    )


def _advance(evidence: EffectivenessEvidenceInput) -> EffectivenessDecision:
    codes: list[str] = ["kind_advance"]
    if evidence.progress_advanced and _strong_sitting(evidence):
        codes.append("advance_confirmed")
        return EffectivenessDecision(
            EffectivenessVerdict.EFFECTIVE,
            "eff.advance.effective",
            tuple(codes),
            InterventionKind.ADVANCE,
        )
    if evidence.progress_advanced or _strong_sitting(evidence):
        codes.append("advance_held")
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.advance.partial",
            tuple(codes),
            InterventionKind.ADVANCE,
        )
    if _weak_sitting(evidence):
        codes.append("advance_premature")
        return EffectivenessDecision(
            EffectivenessVerdict.INEFFECTIVE,
            "eff.advance.ineffective",
            tuple(codes),
            InterventionKind.ADVANCE,
        )
    return EffectivenessDecision(
        EffectivenessVerdict.INSUFFICIENT_EVIDENCE,
        "eff.advance.insufficient",
        ("thin_advance_signal",),
        InterventionKind.ADVANCE,
    )


def _maintain(evidence: EffectivenessEvidenceInput) -> EffectivenessDecision:
    codes: list[str] = ["kind_maintain"]
    if _strong_sitting(evidence) and not _weak_sitting(evidence):
        codes.append("pace_maintained")
        return EffectivenessDecision(
            EffectivenessVerdict.EFFECTIVE,
            "eff.maintain.effective",
            tuple(codes),
            InterventionKind.MAINTAIN,
        )
    if not _weak_sitting(evidence) and evidence.practice_attempted > 0:
        codes.append("pace_held")
        return EffectivenessDecision(
            EffectivenessVerdict.PARTIALLY_EFFECTIVE,
            "eff.maintain.partial",
            tuple(codes),
            InterventionKind.MAINTAIN,
        )
    if _weak_sitting(evidence):
        codes.append("pace_slipped")
        return EffectivenessDecision(
            EffectivenessVerdict.INEFFECTIVE,
            "eff.maintain.ineffective",
            tuple(codes),
            InterventionKind.MAINTAIN,
        )
    return EffectivenessDecision(
        EffectivenessVerdict.INSUFFICIENT_EVIDENCE,
        "eff.maintain.insufficient",
        ("thin_maintain_signal",),
        InterventionKind.MAINTAIN,
    )
