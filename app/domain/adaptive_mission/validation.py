"""Mission validation — reject inconsistent daily plans before publication."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.adaptive_mission.adaptive_mission import AdaptiveMission
from app.domain.adaptive_mission.mission_step import ActivityType
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin


class ValidationSeverity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class MissionValidationIssue:
    code: str
    severity: ValidationSeverity
    message: str

    def __post_init__(self) -> None:
        severity = (
            self.severity
            if isinstance(self.severity, ValidationSeverity)
            else ValidationSeverity(str(self.severity))
        )
        object.__setattr__(self, "severity", severity)


@dataclass(frozen=True)
class MissionValidationResult:
    passed: bool
    issues: tuple[MissionValidationIssue, ...]
    summary: str

    @property
    def errors(self) -> tuple[MissionValidationIssue, ...]:
        return tuple(
            i for i in self.issues if i.severity == ValidationSeverity.ERROR
        )


def validate_mission(
    mission: AdaptiveMission,
    *,
    twin: StudentDigitalTwin | None = None,
    learning_graph: LearningGraph | None = None,
    existing_active_mission_id: str | None = None,
    require_evidence: bool = True,
) -> MissionValidationResult:
    """Validate educational consistency before publishing a mission."""
    issues: list[MissionValidationIssue] = []

    if not mission.goal.strip():
        issues.append(
            MissionValidationIssue(
                code="missing_goal",
                severity=ValidationSeverity.ERROR,
                message="Mission goal is required.",
            )
        )
    if not mission.reason.educational_explanation.strip():
        issues.append(
            MissionValidationIssue(
                code="missing_explanation",
                severity=ValidationSeverity.ERROR,
                message="Every mission requires an educational explanation.",
            )
        )
    if not mission.steps:
        issues.append(
            MissionValidationIssue(
                code="missing_steps",
                severity=ValidationSeverity.ERROR,
                message="Mission must contain at least one activity step.",
            )
        )
    if not mission.concepts_covered:
        issues.append(
            MissionValidationIssue(
                code="missing_concepts",
                severity=ValidationSeverity.ERROR,
                message="Mission must cover at least one curriculum concept.",
            )
        )

    primary = mission.objective.primary_concept_id
    if primary and primary not in mission.concepts_covered:
        issues.append(
            MissionValidationIssue(
                code="objective_concept_mismatch",
                severity=ValidationSeverity.ERROR,
                message=(
                    "Educational objective primary concept is not listed in "
                    "concepts covered."
                ),
            )
        )

    # Educational consistency with Twin decisions.
    if twin is not None:
        rec_ids = {r.recommendation_id for r in twin.recommendations}
        gap_ids = {g.gap_id for g in twin.knowledge_gaps}
        for rid in mission.source_recommendation_ids:
            if rid and rid not in rec_ids:
                issues.append(
                    MissionValidationIssue(
                        code="unknown_recommendation",
                        severity=ValidationSeverity.ERROR,
                        message=(
                            f"Mission cites recommendation {rid!r} not present "
                            "on the Student Digital Twin."
                        ),
                    )
                )
        for gid in mission.source_gap_ids:
            if gid and gid not in gap_ids:
                issues.append(
                    MissionValidationIssue(
                        code="unknown_gap",
                        severity=ValidationSeverity.ERROR,
                        message=(
                            f"Mission cites knowledge gap {gid!r} not present "
                            "on the Student Digital Twin."
                        ),
                    )
                )
        twin_concepts = set(twin.mastery.by_concept()) if twin.mastery else set()
        twin_concepts.update(g.concept_id for g in twin.knowledge_gaps)
        twin_concepts.update(
            r.curriculum_entity_id
            for r in twin.recommendations
            if r.curriculum_entity_id
        )
        for concept_id in mission.concepts_covered:
            if twin_concepts and concept_id not in twin_concepts:
                # Supporting prerequisites may come only from the Learning Graph.
                node = (
                    None
                    if learning_graph is None
                    else learning_graph.get_node(concept_id)
                )
                if node is None:
                    issues.append(
                        MissionValidationIssue(
                            code="curriculum_alignment",
                            severity=ValidationSeverity.ERROR,
                            message=(
                                f"Concept {concept_id!r} is not aligned to Twin "
                                "state or Learning Graph nodes."
                            ),
                        )
                    )

    # Prerequisite validity via Learning Graph recovery structure.
    if learning_graph is not None and primary:
        recovery = learning_graph.recovery_path(primary)
        weak_foundations = tuple(
            c for c in recovery.concept_ids if c != primary
        )[:2]
        prereq_steps = {
            s.activity.concept_id
            for s in mission.steps
            if s.activity.activity_type == ActivityType.PREREQUISITE_REVIEW
        }
        for foundation in weak_foundations:
            if (
                foundation not in prereq_steps
                and foundation not in mission.concepts_covered
            ):
                issues.append(
                    MissionValidationIssue(
                        code="prerequisite_validity",
                        severity=ValidationSeverity.ERROR,
                        message=(
                            f"Recovery path requires prerequisite {foundation!r} "
                            "but mission omits it."
                        ),
                    )
                )
            elif foundation not in prereq_steps:
                issues.append(
                    MissionValidationIssue(
                        code="prerequisite_step_missing",
                        severity=ValidationSeverity.WARNING,
                        message=(
                            f"Prerequisite {foundation!r} is covered but lacks a "
                            "dedicated prerequisite_review step."
                        ),
                    )
                )

    # Evidence availability.
    if require_evidence and not mission.evidence_references:
        if mission.source_gap_ids:
            issues.append(
                MissionValidationIssue(
                    code="evidence_availability",
                    severity=ValidationSeverity.ERROR,
                    message=(
                        "Gap-driven missions require curriculum evidence "
                        "references."
                    ),
                )
            )
        else:
            issues.append(
                MissionValidationIssue(
                    code="evidence_availability",
                    severity=ValidationSeverity.WARNING,
                    message="Mission has no curriculum evidence references.",
                )
            )

    # Duplicate avoidance — one active mission per learner.
    if (
        existing_active_mission_id
        and existing_active_mission_id != mission.mission_id
    ):
        issues.append(
            MissionValidationIssue(
                code="duplicate_active",
                severity=ValidationSeverity.ERROR,
                message=(
                    f"Learner already has active mission "
                    f"{existing_active_mission_id!r}; supersede it first."
                ),
            )
        )

    # Reflection step recommended for explainability / closure.
    if not any(
        s.activity.activity_type == ActivityType.REFLECTION for s in mission.steps
    ):
        issues.append(
            MissionValidationIssue(
                code="missing_reflection",
                severity=ValidationSeverity.WARNING,
                message="Mission has no reflection activity.",
            )
        )

    errors = [i for i in issues if i.severity == ValidationSeverity.ERROR]
    passed = not errors
    if passed:
        summary = (
            "Mission validation passed."
            if not issues
            else f"Mission validation passed with {len(issues)} warning(s)."
        )
    else:
        summary = (
            f"Mission validation failed with {len(errors)} error(s): "
            + "; ".join(i.code for i in errors)
        )
    return MissionValidationResult(
        passed=passed,
        issues=tuple(issues),
        summary=summary,
    )
