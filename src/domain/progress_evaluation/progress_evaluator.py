"""ProgressEvaluator — deterministic ProgressReport from Educational OS inputs.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
    EDUCATIONAL_PRIORITY_MODEL.md
Concept
    Progress Evaluation

Rules
    No AI. No prompting. No randomness. No persistence. No visualization.
    Same educational inputs always yield the same ProgressReport.
"""

from __future__ import annotations

from domain.education.digital_twin.aggregates.educational_digital_twin import (
    EducationalDigitalTwin,
)
from domain.education.digital_twin.enums import (
    MasteryBand,
    MisconceptionPresence,
    RetentionBand,
    TwinStatus,
)
from domain.education.digital_twin.value_objects.learning_trajectory import (
    LearningTrajectory,
)
from domain.education.evidence.aggregates.evidence_record import EvidenceRecord
from domain.education.evidence.enums import EvidenceItemKind, EvidenceStrengthLevel
from domain.education.foundation.enums import ConfidenceLevel
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.progress_evaluation.completed_mission import CompletedMission
from domain.progress_evaluation.confidence_trend import ConfidenceTrend
from domain.progress_evaluation.enums import (
    InterventionUrgency,
    ProgressMetricCode,
    RevisionEffectivenessBand,
    StabilityBand,
    TrendDirection,
    VelocityBand,
)
from domain.progress_evaluation.ids import ProgressReportId
from domain.progress_evaluation.intervention_signal import InterventionSignal
from domain.progress_evaluation.learning_velocity import LearningVelocity
from domain.progress_evaluation.mastery_trend import MasteryTrend
from domain.progress_evaluation.progress_metric import ProgressMetric
from domain.progress_evaluation.progress_report import ProgressReport
from domain.progress_evaluation.revision_effectiveness import RevisionEffectiveness
from domain.study_planning.study_plan import StudyPlan

# --- deterministic catalogues (integer millipoints) -------------------------

_MASTERY_BAND_MILLIPOINTS: dict[MasteryBand, int | None] = {
    MasteryBand.UNKNOWN: None,
    MasteryBand.NASCENT: 125,
    MasteryBand.DEVELOPING: 375,
    MasteryBand.PROFICIENT: 625,
    MasteryBand.MASTERED: 875,
}

_CONFIDENCE_MILLIPOINTS: dict[ConfidenceLevel, int | None] = {
    ConfidenceLevel.UNKNOWN: None,
    ConfidenceLevel.VERY_LOW: 100,
    ConfidenceLevel.LOW: 300,
    ConfidenceLevel.MEDIUM: 500,
    ConfidenceLevel.HIGH: 700,
    ConfidenceLevel.VERY_HIGH: 900,
}

_STRENGTH_MILLIPOINTS: dict[EvidenceStrengthLevel, int] = {
    EvidenceStrengthLevel.WEAK: 250,
    EvidenceStrengthLevel.MODERATE: 500,
    EvidenceStrengthLevel.STRONG: 750,
    EvidenceStrengthLevel.VERY_STRONG: 1000,
}

_RETENTION_STABILITY: dict[RetentionBand, StabilityBand] = {
    RetentionBand.UNKNOWN: StabilityBand.UNKNOWN,
    RetentionBand.FADING: StabilityBand.UNSTABLE,
    RetentionBand.FRAGILE: StabilityBand.FRAGILE,
    RetentionBand.STABLE: StabilityBand.STABLE,
    RetentionBand.DURABLE: StabilityBand.DURABLE,
}

_RETENTION_SCORE: dict[RetentionBand, int | None] = {
    RetentionBand.UNKNOWN: None,
    RetentionBand.FADING: 150,
    RetentionBand.FRAGILE: 400,
    RetentionBand.STABLE: 700,
    RetentionBand.DURABLE: 900,
}

# Half-window trend sensitivity (millipoints).
_TREND_DELTA_THRESHOLD = 80

# Intervention thresholds.
_ACTIVE_MISCONCEPTION_THRESHOLD = 1
_LOW_CONFIDENCE_LEVELS = frozenset(
    {ConfidenceLevel.VERY_LOW, ConfidenceLevel.LOW}
)
_STALLED_EVENTS_PER_DAY_MP = 100  # 0.1 events/day
_SLOW_EVENTS_PER_DAY_MP = 500
_FAST_EVENTS_PER_DAY_MP = 1500

_HINT_KINDS = frozenset({EvidenceItemKind.HINT_USAGE})
_RETRIEVAL_KINDS = frozenset(
    {EvidenceItemKind.RETRIEVAL_ATTEMPT, EvidenceItemKind.TRANSFER_ATTEMPT}
)

_URGENCY_RANK: dict[InterventionUrgency, int] = {
    InterventionUrgency.NONE: 0,
    InterventionUrgency.ADVISORY: 1,
    InterventionUrgency.ELEVATED: 2,
    InterventionUrgency.CRITICAL: 3,
}


class ProgressEvaluator:
    """Pure domain service that evaluates learner progress.

    Evaluation is fully deterministic and explainable from Digital Twin,
    Learning Evidence, Completed Missions, Study Plans, and Learning Trajectory.
    """

    @classmethod
    def evaluate(
        cls,
        twin: EducationalDigitalTwin,
        evidence: tuple[EvidenceRecord, ...] | list[EvidenceRecord],
        completed_missions: tuple[CompletedMission, ...] | list[CompletedMission],
        study_plans: tuple[StudyPlan, ...] | list[StudyPlan],
        trajectory: LearningTrajectory | None = None,
    ) -> ProgressReport:
        """Evaluate progress and return an immutable ProgressReport.

        Args:
            twin: Educational Digital Twin memory for the learner.
            evidence: Learning evidence records (observational inputs).
            completed_missions: Missions already completed by the learner.
            study_plans: Study plans (including review schedules) to assess.
            trajectory: Optional trajectory override; defaults to twin.trajectory.

        Returns:
            Immutable ProgressReport with trends, velocity, stability,
            revision effectiveness, confidence, and intervention signal.

        Raises:
            EducationalInvariantViolation: When inputs are inconsistent.
        """
        evidence_tuple = tuple(evidence)
        missions_tuple = tuple(completed_missions)
        plans_tuple = tuple(study_plans)
        active_trajectory = (
            trajectory if trajectory is not None else twin.trajectory
        )
        cls._assert_inputs(
            twin, evidence_tuple, missions_tuple, plans_tuple, active_trajectory
        )

        ordered_evidence = cls._order_evidence(evidence_tuple)
        ordered_missions = cls._order_missions(missions_tuple)

        mastery_trend = cls._mastery_trend(twin, ordered_evidence, ordered_missions)
        confidence_trend = cls._confidence_trend(twin, ordered_evidence)
        learning_velocity = cls._learning_velocity(
            ordered_evidence, ordered_missions, mastery_trend
        )
        knowledge_stability = cls._knowledge_stability(twin)
        revision_effectiveness = cls._revision_effectiveness(
            twin, ordered_evidence, plans_tuple
        )
        confidence_level = twin.confidence.overall
        intervention_signal = cls._intervention_signal(
            twin=twin,
            mastery_trend=mastery_trend,
            confidence_trend=confidence_trend,
            learning_velocity=learning_velocity,
            knowledge_stability=knowledge_stability,
            revision_effectiveness=revision_effectiveness,
            confidence_level=confidence_level,
        )
        metrics = cls._build_metrics(
            mastery_trend=mastery_trend,
            confidence_trend=confidence_trend,
            learning_velocity=learning_velocity,
            knowledge_stability=knowledge_stability,
            revision_effectiveness=revision_effectiveness,
            confidence_level=confidence_level,
            intervention_signal=intervention_signal,
        )
        explanation = cls._build_explanation(
            twin=twin,
            trajectory=active_trajectory,
            mastery_trend=mastery_trend,
            learning_velocity=learning_velocity,
            knowledge_stability=knowledge_stability,
            revision_effectiveness=revision_effectiveness,
            confidence_level=confidence_level,
            intervention_signal=intervention_signal,
            evidence_count=len(ordered_evidence),
            mission_count=len(ordered_missions),
            plan_count=len(plans_tuple),
        )
        report_id = cls._report_id(
            twin, ordered_evidence, ordered_missions, plans_tuple
        )
        return ProgressReport(
            report_id=report_id,
            student_id=twin.student_id,
            twin_id=twin.twin_id,
            mastery_trend=mastery_trend,
            learning_velocity=learning_velocity,
            knowledge_stability=knowledge_stability,
            revision_effectiveness=revision_effectiveness,
            confidence_level=confidence_level,
            confidence_trend=confidence_trend,
            intervention_signal=intervention_signal,
            metrics=metrics,
            educational_explanation=explanation,
            evidence_ids=tuple(record.evidence_id for record in ordered_evidence),
            mission_ids=tuple(mission.mission_id for mission in ordered_missions),
            plan_ids=tuple(plan.plan_id for plan in plans_tuple),
        )

    # --- validation ---------------------------------------------------------

    @staticmethod
    def _assert_inputs(
        twin: EducationalDigitalTwin,
        evidence: tuple[EvidenceRecord, ...],
        missions: tuple[CompletedMission, ...],
        plans: tuple[StudyPlan, ...],
        trajectory: LearningTrajectory,
    ) -> None:
        if not isinstance(twin, EducationalDigitalTwin):
            raise EducationalInvariantViolation(
                "twin must be an EducationalDigitalTwin",
                invariant="ProgressEvaluator.twin.type",
            )
        if twin.status is TwinStatus.ARCHIVED:
            raise EducationalInvariantViolation(
                "archived Twin cannot be evaluated for progress",
                invariant="ProgressEvaluator.twin.archived",
            )
        if not isinstance(trajectory, LearningTrajectory):
            raise EducationalInvariantViolation(
                "trajectory must be a LearningTrajectory",
                invariant="ProgressEvaluator.trajectory.type",
            )
        for record in evidence:
            if not isinstance(record, EvidenceRecord):
                raise EducationalInvariantViolation(
                    "evidence must contain EvidenceRecord values",
                    invariant="ProgressEvaluator.evidence.item_type",
                )
            if record.student_id != twin.student_id:
                raise EducationalInvariantViolation(
                    "evidence student_id must match Twin student_id",
                    invariant="ProgressEvaluator.evidence.student_alignment",
                )
        evidence_ids = [record.evidence_id.value for record in evidence]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise EducationalInvariantViolation(
                "evidence must declare unique evidence identities",
                invariant="ProgressEvaluator.evidence.unique",
            )
        for mission in missions:
            if not isinstance(mission, CompletedMission):
                raise EducationalInvariantViolation(
                    "completed_missions must contain CompletedMission values",
                    invariant="ProgressEvaluator.missions.item_type",
                )
            if mission.student_id != twin.student_id:
                raise EducationalInvariantViolation(
                    "completed missions student_id must match Twin student_id",
                    invariant="ProgressEvaluator.missions.student_alignment",
                )
        mission_ids = [mission.mission_id.value for mission in missions]
        if len(mission_ids) != len(set(mission_ids)):
            raise EducationalInvariantViolation(
                "completed missions must declare unique mission identities",
                invariant="ProgressEvaluator.missions.unique",
            )
        sequences = [mission.completion_sequence for mission in missions]
        if len(sequences) != len(set(sequences)):
            raise EducationalInvariantViolation(
                "completed missions must declare unique completion sequences",
                invariant="ProgressEvaluator.missions.sequence_unique",
            )
        for plan in plans:
            if not isinstance(plan, StudyPlan):
                raise EducationalInvariantViolation(
                    "study_plans must contain StudyPlan values",
                    invariant="ProgressEvaluator.plans.item_type",
                )
            if plan.student_id != twin.student_id:
                raise EducationalInvariantViolation(
                    "study plans student_id must match Twin student_id",
                    invariant="ProgressEvaluator.plans.student_alignment",
                )
        plan_ids = [plan.plan_id.value for plan in plans]
        if len(plan_ids) != len(set(plan_ids)):
            raise EducationalInvariantViolation(
                "study plans must declare unique plan identities",
                invariant="ProgressEvaluator.plans.unique",
            )

    # --- ordering -----------------------------------------------------------

    @staticmethod
    def _order_evidence(
        evidence: tuple[EvidenceRecord, ...],
    ) -> tuple[EvidenceRecord, ...]:
        active = [record for record in evidence if record.is_active()]
        return tuple(
            sorted(
                active,
                key=lambda record: (
                    record.timestamp.occurred_at,
                    record.evidence_id.value,
                ),
            )
        )

    @staticmethod
    def _order_missions(
        missions: tuple[CompletedMission, ...],
    ) -> tuple[CompletedMission, ...]:
        return tuple(
            sorted(
                missions,
                key=lambda mission: (
                    mission.completion_sequence,
                    mission.mission_id.value,
                ),
            )
        )

    # --- mastery trend ------------------------------------------------------

    @classmethod
    def _mastery_trend(
        cls,
        twin: EducationalDigitalTwin,
        evidence: tuple[EvidenceRecord, ...],
        missions: tuple[CompletedMission, ...],
    ) -> MasteryTrend:
        current = cls._current_mastery_millipoints(twin)
        signals = [cls._evidence_mastery_signal(record) for record in evidence]
        signals.extend(mission.outcome_millipoints for mission in missions)
        sample_size = len(signals)
        direction, delta = cls._trend_from_signals(signals)
        regression = direction is TrendDirection.DECLINING
        explanation = (
            f"Mastery trend {direction.value} from {sample_size} progress "
            f"signal(s); current mastery {current} millipoints; "
            f"half-window delta {delta:+d} millipoints"
            + ("; regression detected" if regression else "")
            + "."
        )
        return MasteryTrend(
            direction=direction,
            current_millipoints=current,
            delta_millipoints=delta,
            sample_size=sample_size,
            regression_detected=regression,
            explanation=explanation,
        )

    @classmethod
    def _current_mastery_millipoints(cls, twin: EducationalDigitalTwin) -> int:
        scores: list[int] = []
        for state in sorted(
            twin.concept_states, key=lambda item: item.concept_id.value
        ):
            score = cls._mastery_state_millipoints(
                state.mastery.band, state.mastery.ratio
            )
            if score is not None:
                scores.append(score)
        if not scores:
            return 0
        return sum(scores) // len(scores)

    @staticmethod
    def _mastery_state_millipoints(
        band: MasteryBand, ratio: float | None
    ) -> int | None:
        if ratio is not None:
            return int(round(float(ratio) * 1000))
        return _MASTERY_BAND_MILLIPOINTS[band]

    @classmethod
    def _evidence_mastery_signal(cls, record: EvidenceRecord) -> int:
        base = _STRENGTH_MILLIPOINTS[record.strength.level]
        kinds = {item.kind for item in record.items}
        if kinds & _HINT_KINDS and not (kinds - _HINT_KINDS):
            return base // 2
        if EvidenceItemKind.HINT_USAGE in kinds:
            return (base * 3) // 4
        return base

    @staticmethod
    def _trend_from_signals(signals: list[int]) -> tuple[TrendDirection, int]:
        if len(signals) < 2:
            return TrendDirection.INSUFFICIENT_DATA, 0
        mid = len(signals) // 2
        first = signals[:mid]
        second = signals[mid:]
        first_avg = sum(first) // len(first)
        second_avg = sum(second) // len(second)
        delta = second_avg - first_avg
        if delta > 1000:
            delta = 1000
        elif delta < -1000:
            delta = -1000
        if delta >= _TREND_DELTA_THRESHOLD:
            return TrendDirection.IMPROVING, delta
        if delta <= -_TREND_DELTA_THRESHOLD:
            return TrendDirection.DECLINING, delta
        return TrendDirection.STABLE, delta

    # --- confidence trend ---------------------------------------------------

    @classmethod
    def _confidence_trend(
        cls,
        twin: EducationalDigitalTwin,
        evidence: tuple[EvidenceRecord, ...],
    ) -> ConfidenceTrend:
        current_level = twin.confidence.overall
        current = cls._confidence_millipoints(current_level, twin.confidence.ratio)
        if current is None:
            current = 0
        signals = [
            cls._confidence_millipoints(
                record.confidence.level, record.confidence.ratio
            )
            or 0
            for record in evidence
        ]
        direction, delta = cls._trend_from_signals(signals)
        explanation = (
            f"Confidence trend {direction.value} from {len(signals)} evidence "
            f"confidence signal(s); Twin posture {current_level.value} "
            f"({current} millipoints); half-window delta {delta:+d}."
        )
        return ConfidenceTrend(
            direction=direction,
            current_level=current_level,
            current_millipoints=current,
            delta_millipoints=delta,
            sample_size=len(signals),
            explanation=explanation,
        )

    @staticmethod
    def _confidence_millipoints(
        level: ConfidenceLevel, ratio: float | None
    ) -> int | None:
        if ratio is not None:
            return int(round(float(ratio) * 1000))
        return _CONFIDENCE_MILLIPOINTS[level]

    # --- learning velocity --------------------------------------------------

    @classmethod
    def _learning_velocity(
        cls,
        evidence: tuple[EvidenceRecord, ...],
        missions: tuple[CompletedMission, ...],
        mastery_trend: MasteryTrend,
    ) -> LearningVelocity:
        window_days = cls._evidence_window_days(evidence)
        event_count = len(evidence)
        if window_days == 0:
            events_per_day_mp = 0
        else:
            events_per_day_mp = (event_count * 1000) // window_days
        missions_completed = len(missions)
        mastery_delta = mastery_trend.delta_millipoints
        band = cls._velocity_band(events_per_day_mp, mastery_delta, event_count)
        explanation = (
            f"Learning velocity {band.value}: {event_count} evidence event(s) "
            f"across {window_days} day(s) "
            f"({events_per_day_mp} millipoints events/day), "
            f"{missions_completed} completed mission(s), mastery delta "
            f"{mastery_delta:+d} millipoints."
        )
        return LearningVelocity(
            band=band,
            events_per_day_millipoints=events_per_day_mp,
            mastery_delta_millipoints=mastery_delta,
            missions_completed=missions_completed,
            window_days=window_days,
            explanation=explanation,
        )

    @staticmethod
    def _evidence_window_days(evidence: tuple[EvidenceRecord, ...]) -> int:
        if not evidence:
            return 0
        first = evidence[0].timestamp.occurred_at
        last = evidence[-1].timestamp.occurred_at
        delta = last - first
        days = delta.days
        # Include partial final day so a same-day burst is still a 1-day window.
        if delta.seconds > 0 or delta.microseconds > 0 or days == 0:
            days += 1
        return days

    @staticmethod
    def _velocity_band(
        events_per_day_mp: int,
        mastery_delta: int,
        event_count: int,
    ) -> VelocityBand:
        if event_count == 0:
            return VelocityBand.UNKNOWN
        if (
            events_per_day_mp <= _STALLED_EVENTS_PER_DAY_MP
            and mastery_delta <= 0
        ):
            return VelocityBand.STALLED
        if events_per_day_mp < _SLOW_EVENTS_PER_DAY_MP:
            return VelocityBand.SLOW
        if events_per_day_mp >= _FAST_EVENTS_PER_DAY_MP:
            return VelocityBand.FAST
        return VelocityBand.MODERATE

    # --- knowledge stability ------------------------------------------------

    @classmethod
    def _knowledge_stability(cls, twin: EducationalDigitalTwin) -> StabilityBand:
        overall = _RETENTION_STABILITY[twin.retention.band]
        concept_bands: list[StabilityBand] = []
        for state in twin.concept_states:
            concept_bands.append(_RETENTION_STABILITY[state.retention.band])
        if not concept_bands:
            return overall
        # Majority vote among concept retention; ties defer to Twin overall.
        counts: dict[StabilityBand, int] = {}
        for band in concept_bands:
            counts[band] = counts.get(band, 0) + 1
        best = max(
            sorted(counts.items(), key=lambda item: item[0].value),
            key=lambda item: item[1],
        )[0]
        if overall is StabilityBand.UNKNOWN:
            return best
        if best is StabilityBand.UNKNOWN:
            return overall
        # Prefer the more fragile of Twin overall vs concept majority.
        order = (
            StabilityBand.UNSTABLE,
            StabilityBand.FRAGILE,
            StabilityBand.STABLE,
            StabilityBand.DURABLE,
        )
        if best in order and overall in order:
            return order[min(order.index(best), order.index(overall))]
        return overall

    # --- revision effectiveness ---------------------------------------------

    @classmethod
    def _revision_effectiveness(
        cls,
        twin: EducationalDigitalTwin,
        evidence: tuple[EvidenceRecord, ...],
        plans: tuple[StudyPlan, ...],
    ) -> RevisionEffectiveness:
        review_count = sum(len(plan.schedule.review_sessions()) for plan in plans)
        probe_count = sum(
            1
            for record in evidence
            if any(item.kind in _RETRIEVAL_KINDS for item in record.items)
        )
        if review_count == 0:
            return RevisionEffectiveness(
                band=RevisionEffectivenessBand.INAPPLICABLE,
                review_session_count=0,
                retention_probe_count=probe_count,
                score_millipoints=0,
                explanation=(
                    "Revision effectiveness inapplicable: no review sessions "
                    "scheduled across study plans."
                ),
            )
        retention_score = _RETENTION_SCORE[twin.retention.band]
        if retention_score is None:
            band = RevisionEffectivenessBand.UNKNOWN
            score = 500
        elif twin.retention.band is RetentionBand.DURABLE:
            band = RevisionEffectivenessBand.EFFECTIVE
            score = min(1000, retention_score + min(probe_count * 25, 100))
        elif twin.retention.band is RetentionBand.STABLE:
            band = RevisionEffectivenessBand.EFFECTIVE
            score = retention_score
        elif twin.retention.band is RetentionBand.FRAGILE:
            band = RevisionEffectivenessBand.MIXED
            score = retention_score
        else:
            band = RevisionEffectivenessBand.INEFFECTIVE
            score = retention_score
        explanation = (
            f"Revision effectiveness {band.value} from {review_count} review "
            f"session(s) and {probe_count} retrieval/transfer probe(s); "
            f"Twin retention {twin.retention.band.value} yields score "
            f"{score} millipoints."
        )
        return RevisionEffectiveness(
            band=band,
            review_session_count=review_count,
            retention_probe_count=probe_count,
            score_millipoints=score,
            explanation=explanation,
        )

    # --- intervention signal ------------------------------------------------

    @classmethod
    def _intervention_signal(
        cls,
        *,
        twin: EducationalDigitalTwin,
        mastery_trend: MasteryTrend,
        confidence_trend: ConfidenceTrend,
        learning_velocity: LearningVelocity,
        knowledge_stability: StabilityBand,
        revision_effectiveness: RevisionEffectiveness,
        confidence_level: ConfidenceLevel,
    ) -> InterventionSignal:
        reasons: list[str] = []
        urgency = InterventionUrgency.NONE

        def raise_urgency(candidate: InterventionUrgency) -> None:
            nonlocal urgency
            if _URGENCY_RANK[candidate] > _URGENCY_RANK[urgency]:
                urgency = candidate

        if mastery_trend.regression_detected:
            reasons.append("mastery_regression")
            raise_urgency(InterventionUrgency.CRITICAL)

        active_misconceptions = sum(
            1
            for state in twin.misconception_states
            if state.presence
            in {MisconceptionPresence.ACTIVE, MisconceptionPresence.SUSPECTED}
        )
        if active_misconceptions >= _ACTIVE_MISCONCEPTION_THRESHOLD:
            reasons.append(f"active_misconceptions:{active_misconceptions}")
            raise_urgency(InterventionUrgency.ELEVATED)

        if knowledge_stability is StabilityBand.UNSTABLE:
            reasons.append("knowledge_unstable")
            raise_urgency(InterventionUrgency.ELEVATED)

        if confidence_level in _LOW_CONFIDENCE_LEVELS:
            reasons.append(f"low_confidence:{confidence_level.value}")
            if confidence_trend.direction is TrendDirection.DECLINING:
                raise_urgency(InterventionUrgency.ELEVATED)
            else:
                raise_urgency(InterventionUrgency.ADVISORY)

        if revision_effectiveness.band is RevisionEffectivenessBand.INEFFECTIVE:
            reasons.append("revision_ineffective")
            raise_urgency(InterventionUrgency.ELEVATED)

        if (
            learning_velocity.band is VelocityBand.STALLED
            and mastery_trend.direction is TrendDirection.DECLINING
        ):
            reasons.append("stalled_declining_velocity")
            raise_urgency(InterventionUrgency.CRITICAL)

        # Deterministic reason order for identical reports.
        reasons = sorted(set(reasons))
        required = urgency is not InterventionUrgency.NONE
        if required:
            explanation = (
                f"Intervention required at {urgency.value} urgency due to: "
                + ", ".join(reasons)
                + "."
            )
        else:
            explanation = (
                "No intervention threshold breached; progress metrics remain "
                "within acceptable educational bands."
            )
        return InterventionSignal(
            required=required,
            urgency=urgency,
            reasons=tuple(reasons),
            explanation=explanation,
        )

    # --- metrics / identity / explanation -----------------------------------

    @staticmethod
    def _build_metrics(
        *,
        mastery_trend: MasteryTrend,
        confidence_trend: ConfidenceTrend,
        learning_velocity: LearningVelocity,
        knowledge_stability: StabilityBand,
        revision_effectiveness: RevisionEffectiveness,
        confidence_level: ConfidenceLevel,
        intervention_signal: InterventionSignal,
    ) -> tuple[ProgressMetric, ...]:
        stability_mp = {
            StabilityBand.UNKNOWN: 0,
            StabilityBand.UNSTABLE: 150,
            StabilityBand.FRAGILE: 400,
            StabilityBand.STABLE: 700,
            StabilityBand.DURABLE: 900,
        }[knowledge_stability]
        velocity_mp = {
            VelocityBand.UNKNOWN: 0,
            VelocityBand.STALLED: 100,
            VelocityBand.SLOW: 350,
            VelocityBand.MODERATE: 650,
            VelocityBand.FAST: 900,
        }[learning_velocity.band]
        confidence_mp = _CONFIDENCE_MILLIPOINTS.get(confidence_level) or 0
        return (
            ProgressMetric(
                code=ProgressMetricCode.MASTERY_TREND,
                label="Mastery Trend",
                value_millipoints=mastery_trend.delta_millipoints,
                band=mastery_trend.direction.value,
                explanation=mastery_trend.explanation,
            ),
            ProgressMetric(
                code=ProgressMetricCode.CONFIDENCE_TREND,
                label="Confidence Trend",
                value_millipoints=confidence_trend.delta_millipoints,
                band=confidence_trend.direction.value,
                explanation=confidence_trend.explanation,
            ),
            ProgressMetric(
                code=ProgressMetricCode.LEARNING_VELOCITY,
                label="Learning Velocity",
                value_millipoints=velocity_mp,
                band=learning_velocity.band.value,
                explanation=learning_velocity.explanation,
            ),
            ProgressMetric(
                code=ProgressMetricCode.KNOWLEDGE_STABILITY,
                label="Knowledge Stability",
                value_millipoints=stability_mp,
                band=knowledge_stability.value,
                explanation=(
                    f"Knowledge stability band {knowledge_stability.value} "
                    f"from Twin and concept retention memory."
                ),
            ),
            ProgressMetric(
                code=ProgressMetricCode.REVISION_EFFECTIVENESS,
                label="Revision Effectiveness",
                value_millipoints=revision_effectiveness.score_millipoints,
                band=revision_effectiveness.band.value,
                explanation=revision_effectiveness.explanation,
            ),
            ProgressMetric(
                code=ProgressMetricCode.CONFIDENCE_LEVEL,
                label="Confidence Level",
                value_millipoints=confidence_mp,
                band=confidence_level.value,
                explanation=(
                    f"Twin confidence posture is {confidence_level.value}."
                ),
            ),
            ProgressMetric(
                code=ProgressMetricCode.INTERVENTION_REQUIRED,
                label="Intervention Required",
                value_millipoints=1000 if intervention_signal.required else 0,
                band=intervention_signal.urgency.value,
                explanation=intervention_signal.explanation,
            ),
        )

    @staticmethod
    def _report_id(
        twin: EducationalDigitalTwin,
        evidence: tuple[EvidenceRecord, ...],
        missions: tuple[CompletedMission, ...],
        plans: tuple[StudyPlan, ...],
    ) -> ProgressReportId:
        evidence_part = (
            "_".join(record.evidence_id.value for record in evidence) or "none"
        )
        mission_part = (
            "_".join(mission.mission_id.value for mission in missions) or "none"
        )
        plan_part = "_".join(plan.plan_id.value for plan in plans) or "none"
        return ProgressReportId(
            f"progress-{twin.twin_id.value}-e{len(evidence)}"
            f"-m{len(missions)}-p{len(plans)}-"
            f"{evidence_part}-{mission_part}-{plan_part}"
        )

    @staticmethod
    def _build_explanation(
        *,
        twin: EducationalDigitalTwin,
        trajectory: LearningTrajectory,
        mastery_trend: MasteryTrend,
        learning_velocity: LearningVelocity,
        knowledge_stability: StabilityBand,
        revision_effectiveness: RevisionEffectiveness,
        confidence_level: ConfidenceLevel,
        intervention_signal: InterventionSignal,
        evidence_count: int,
        mission_count: int,
        plan_count: int,
    ) -> str:
        last = trajectory.last()
        trajectory_clause = (
            f"trajectory length {trajectory.length()}"
            + (
                f", last point {last.kind.value}:{last.label}"
                if last is not None
                else ", empty trajectory"
            )
        )
        return (
            f"Progress report for student {twin.student_id} "
            f"(twin {twin.twin_id.value}) evaluates {evidence_count} evidence "
            f"record(s), {mission_count} completed mission(s), and "
            f"{plan_count} study plan(s). Mastery is "
            f"{mastery_trend.direction.value} "
            f"(delta {mastery_trend.delta_millipoints:+d}); learning velocity "
            f"{learning_velocity.band.value}; knowledge stability "
            f"{knowledge_stability.value}; revision "
            f"{revision_effectiveness.band.value}; confidence "
            f"{confidence_level.value}. Intervention "
            f"{'required' if intervention_signal.required else 'not required'} "
            f"({intervention_signal.urgency.value}). Based on {trajectory_clause}."
        )


def trend_delta_threshold() -> int:
    """Return the half-window millipoint threshold for trend direction."""
    return _TREND_DELTA_THRESHOLD


def active_misconception_threshold() -> int:
    """Return the active-misconception count that triggers intervention."""
    return _ACTIVE_MISCONCEPTION_THRESHOLD
