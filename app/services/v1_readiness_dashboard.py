"""Version 1 Readiness Dashboard — founder observability (V1S-001…006).

Static readiness snapshot for internal dogfooding. Does not change
educational algorithms or declare production-ready status.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.services.dogfood_validation import (
    DOGFOOD_PROGRESS,
    DOGFOOD_PROGRESS_SUMMARY,
    EDUCATIONAL_IMPROVEMENTS,
    PRODUCT_RATINGS,
    SURFACE_AUDIT,
    DogfoodPackageReadiness,
    DogfoodProgressEntry,
    EducationalImprovement,
    LearningFrictionRecord,
    ProductAreaRating,
    SurfaceAuditEntry,
    ValidationIssue,
    assess_dogfood_package_readiness,
    dogfood_completion_trend,
    dogfood_confidence_trend,
    dogfood_friction_trend,
    dogfood_metrics_summary,
    dogfood_motivation_trend,
    dogfood_study_consistency,
    open_educational_improvements,
    open_friction_issues,
    outstanding_issues,
    resolved_friction_records,
    resolved_issues,
    validation_issue_counts,
)
from app.services.package_lifecycle import (
    ALL_PACKAGE_ENTRIES,
    APPLICATION_PACKAGES,
    CODE_DEBT_REGISTER,
    ENGINEERING_QUALITY_METRICS,
    REPOSITORY_HEALTH_SUMMARY,
    CodeDebtItem,
    EngineeringMetric,
    PackageEntry,
    lifecycle_counts,
)
from app.services.runtime_ownership import (
    CURRICULUM_AUTHORITY_MATRIX,
    MISSION_RUNTIME_MATRIX,
    MISSION_SPINE,
    RUNTIME_OWNERSHIP_MATRIX,
    TECHNICAL_DEBT_REGISTER,
    DebtEntry,
    OwnershipEntry,
)


@dataclass(frozen=True)
class ReadinessDimension:
    """One scored readiness dimension for founder review."""

    name: str
    score: int  # 0–100 provisional
    status: str  # PASS | HOLD | FAIL | IN_PROGRESS
    summary: str
    blockers: tuple[str, ...] = ()


@dataclass(frozen=True)
class V1ReadinessSnapshot:
    """Founder Version 1 Readiness Dashboard payload."""

    programme: str
    claim: str
    overall_status: str
    recommendation: str
    dimensions: tuple[ReadinessDimension, ...]
    remaining_blockers: tuple[str, ...]
    evidence_paths: tuple[str, ...]
    curriculum_authority: tuple[OwnershipEntry, ...]
    mission_runtime: tuple[OwnershipEntry, ...]
    runtime_ownership: tuple[OwnershipEntry, ...]
    technical_debt: tuple[DebtEntry, ...]
    mission_spine: tuple[str, ...]
    # V1S-003 — repository / engineering health
    repository_health_summary: str
    lifecycle_counts: dict[str, int]
    package_lifecycle: tuple[PackageEntry, ...]
    application_packages: tuple[PackageEntry, ...]
    engineering_quality: tuple[EngineeringMetric, ...]
    code_debt: tuple[CodeDebtItem, ...]
    # V1S-004 / V1S-005 — founder dogfood validation + friction
    dogfood_progress_summary: str
    dogfood_progress: tuple[DogfoodProgressEntry, ...]
    validation_issues: tuple[ValidationIssue, ...]
    validation_issue_counts: dict[str, int]
    educational_improvements: tuple[EducationalImprovement, ...]
    resolved_issues: tuple[ValidationIssue, ...]
    outstanding_issues: tuple[ValidationIssue, ...]
    product_ratings: tuple[ProductAreaRating, ...]
    surface_audit: tuple[SurfaceAuditEntry, ...]
    # V1S-005 / V1S-006 Learning Friction board
    learning_friction_open: tuple[ValidationIssue, ...]
    learning_friction_resolved: tuple[LearningFrictionRecord, ...]
    dogfood_confidence_trend: tuple[str, ...]
    dogfood_motivation_trend: tuple[str, ...]
    dogfood_completion_trend: tuple[str, ...]
    dogfood_study_consistency: tuple[str, ...]
    dogfood_friction_trend: tuple[str, ...]
    dogfood_metrics: dict[str, float | int | str]
    package_readiness: DogfoodPackageReadiness


def build_v1_readiness_snapshot() -> V1ReadinessSnapshot:
    """Return the V1S-006 readiness snapshot for dogfooding review.

    Scores are provisional founder assessments — not validated KSI / CRI.
    """
    package_ready = assess_dogfood_package_readiness("CS1")
    metrics = dogfood_metrics_summary()
    friction_open = open_friction_issues()
    friction_resolved = resolved_friction_records()
    live_days = int(metrics.get("live_days") or 0)
    open_p0 = sum(1 for i in friction_open if i.priority == "P0")

    dimensions = (
        ReadinessDimension(
            name="Architecture completeness",
            score=88,
            status="PASS",
            summary=(
                "V1S-002 cutover retained. V1S-005 isolates ProgressEngine "
                "for Runtime C enrolments without redesigning authorities."
            ),
            blockers=(
                "Runtime A substrate retained until RI-002 hard removal",
                "MissionEngine shell archive pending planning/ extraction",
            ),
        ),
        ReadinessDimension(
            name="Repository health",
            score=70,
            status="IN_PROGRESS",
            summary=(
                "Complete package audit published. Parallel src/ tree and "
                "root report clutter remain the primary navigability taxes."
            ),
            blockers=(
                "Adopt-or-archive decision for src/ Education OS",
                "Relocate completed root programme reports",
                "Execute REMOVE gates for archived mission packages",
            ),
        ),
        ReadinessDimension(
            name="Engineering quality",
            score=66,
            status="IN_PROGRESS",
            summary=(
                "Standards published under docs/engineering/. God modules "
                "and twin naming debt remain HOLD."
            ),
            blockers=(
                "Split oversized planning / recommendation services",
                "Canonical twin package naming",
            ),
        ),
        ReadinessDimension(
            name="Technical debt",
            score=74,
            status="IN_PROGRESS",
            summary=(
                "Dogfood P0/P1 student friction closed. RI-002 and mission "
                "package REMOVE gates remain owned technical debt."
            ),
            blockers=(
                "Archive MissionEngineV2 + MissionAdapter packages",
                "Extract MissionPlanningService before ME shell delete",
                "RI-002 Runtime A hard removal",
            ),
        ),
        ReadinessDimension(
            name="Presentation quality",
            score=86,
            status="PASS",
            summary=(
                "V1S-005 closed Syllabus naming, Home density, CTA honesty, "
                "mission narrative, and Session stage clarity."
            ),
            blockers=(
                "Optional Home loading skeleton (DF-012 deferred)",
            ),
        ),
        ReadinessDimension(
            name="Educational completeness",
            score=62 if open_p0 else (80 if package_ready.ready else 70),
            status="HOLD" if open_p0 or not package_ready.ready else "PASS",
            summary=(
                "V1S-008 closed DF-013 (xp scrub) and DF-016 (title/duration "
                "continuity). Educational verbs and Home↔Session labels align. "
                "Exclusive consecutive live week still incomplete."
            ),
            blockers=(
                (() if package_ready.ready else (
                    "Founder-published CS1 package before exclusive dogfood",
                ))
                + tuple(
                    f"{i.issue_id}: {i.title}"
                    for i in friction_open
                    if i.priority == "P0"
                )
                + ("5–7 consecutive live_sitting days incomplete",)
            ),
        ),
        ReadinessDimension(
            name="Dogfood validation",
            score=48 if open_p0 else (72 if package_ready.ready else 64),
            status="HOLD" if open_p0 or live_days < 5 else "IN_PROGRESS",
            summary=(
                f"Package gate "
                f"{'READY' if package_ready.ready else 'NOT READY'}. "
                f"Live days {live_days}/5. "
                f"Open P0 friction: {open_p0}. "
                "Exclusive week resumes after integrity PASS (V1S-008)."
            ),
            blockers=(
                (() if package_ready.ready else (
                    "Publish active CS1 package (DF-001 gate)",
                ))
                + tuple(
                    f"{i.issue_id}: {i.title}"
                    for i in friction_open
                    if i.priority == "P0"
                )
                + (
                    "Complete 5–7 consecutive CS1 live days without "
                    "undocumented workarounds",
                )
            ),
        ),
        ReadinessDimension(
            name="Learning friction",
            score=55 if open_p0 else (84 if not friction_open else 70),
            status=(
                "HOLD"
                if open_p0
                else ("PASS" if not friction_open else "IN_PROGRESS")
            ),
            summary=(
                f"{len(friction_resolved)} friction records resolved; "
                f"{len(friction_open)} open friction/bug/UX items remaining "
                f"({open_p0} P0)."
            ),
            blockers=tuple(f"{i.issue_id}: {i.title}" for i in friction_open[:5]),
        ),
        ReadinessDimension(
            name="Commercial readiness",
            score=55,
            status="HOLD",
            summary=(
                "Internal dogfooding bar approachable. Production-ready "
                "still blocked by P-002.1 (validated KSI / G1 FAIL)."
            ),
            blockers=(
                "Gate G1 validated KSI FAIL",
                "Stage 1 private beta enrollment HOLD",
                "Public launch / pricing not started (CR9)",
            ),
        ),
        ReadinessDimension(
            name="Risk assessment",
            score=58 if open_p0 else (82 if package_ready.ready else 70),
            status="HOLD" if open_p0 or not package_ready.ready else "PASS",
            summary=(
                "Day 1 live sitting reopened P0 educational-trust risks: "
                "mangled prose (xp scrub) and Session Runtime A fallback "
                "without SCI."
            ),
            blockers=(
                (() if package_ready.ready else (
                    "Ensure founder-published packages exist before dogfood enrol",
                ))
                + tuple(
                    f"{i.issue_id}: {i.title}"
                    for i in friction_open
                    if i.priority == "P0"
                )
                + ("Block new imports of ARCHIVED / REMOVE packages",)
            ),
        ),
    )
    edu_improvements = open_educational_improvements()
    if not edu_improvements:
        edu_improvements = EDUCATIONAL_IMPROVEMENTS

    remaining = [
        "Close remaining P0: DF-013 (xp scrub in Educational Authoring)",
        "Close DF-016 title/duration continuity",
        "Resume exclusive CS1 live week to 5–7 consecutive days",
        "Validated KSI >= 80 (Gate G1)",
        "Archive/delete MissionEngineV2 / MissionAdapter (REMOVE gates)",
        "Extract MissionPlanningService; retire ME shell",
        "Adopt-or-archive src/ Education OS tree",
        "RI-002 Runtime A hard removal gates (A9 fallback already REMOVED)",
        "Optional Home loading skeleton (DF-012)",
    ]
    if not package_ready.ready:
        remaining.insert(
            0,
            f"CS1 package gate: {package_ready.reason}",
        )

    week_ok = live_days >= 5 and open_p0 == 0 and package_ready.ready
    return V1ReadinessSnapshot(
        programme="V1S-008",
        claim=(
            "V1S-008 educational integrity PASS (DF-013 / DF-016 closed); "
            "exclusive consecutive live week still incomplete"
        ),
        overall_status=(
            "DOGFOOD WEEK GO"
            if week_ok
            else (
                "HOLD — live week blocked (P0 friction)"
                if open_p0
                else (
                    "HOLD — exclusive week incomplete "
                    f"({live_days}/5 live days)"
                )
            )
        ),
        recommendation=(
            "Educational integrity defects closed. Do not proceed to private "
            "beta until 5–7 consecutive live days complete without "
            "undocumented workarounds."
        ),
        dimensions=dimensions,
        remaining_blockers=tuple(remaining),
        evidence_paths=(
            "V1S008_EDUCATIONAL_INTEGRITY_VALIDATION_REPORT.md",
            "V1S007_EDUCATIONAL_RUNTIME_SINGULARITY_REPORT.md",
            "V1S006_DOGFOOD_WEEK_REPORT.md",
            "V1_RELEASE_CRITERIA.md",
            "V1S005_IMPLEMENTATION_REPORT.md",
            "V1S004_DOGFOOD_REPORT.md",
            "V1S003_IMPLEMENTATION_REPORT.md",
            "V1S002_IMPLEMENTATION_REPORT.md",
            "V1S001_IMPLEMENTATION_REPORT.md",
            "app/services/dogfood_validation.py",
            "app/services/package_lifecycle.py",
            "app/services/runtime_ownership.py",
            "docs/engineering/REPOSITORY_STANDARDS.md",
            "knowledge/product/p002_1_version_1_release_framework/"
            "VERSION_1_RELEASE_FRAMEWORK.md",
        ),
        curriculum_authority=CURRICULUM_AUTHORITY_MATRIX,
        mission_runtime=MISSION_RUNTIME_MATRIX,
        runtime_ownership=RUNTIME_OWNERSHIP_MATRIX,
        technical_debt=TECHNICAL_DEBT_REGISTER,
        mission_spine=MISSION_SPINE,
        repository_health_summary=REPOSITORY_HEALTH_SUMMARY,
        lifecycle_counts=lifecycle_counts(),
        package_lifecycle=ALL_PACKAGE_ENTRIES,
        application_packages=APPLICATION_PACKAGES,
        engineering_quality=ENGINEERING_QUALITY_METRICS,
        code_debt=CODE_DEBT_REGISTER,
        dogfood_progress_summary=DOGFOOD_PROGRESS_SUMMARY,
        dogfood_progress=DOGFOOD_PROGRESS,
        validation_issues=outstanding_issues() + resolved_issues(),
        validation_issue_counts=validation_issue_counts(),
        educational_improvements=edu_improvements,
        resolved_issues=resolved_issues(),
        outstanding_issues=outstanding_issues(),
        product_ratings=PRODUCT_RATINGS,
        surface_audit=SURFACE_AUDIT,
        learning_friction_open=friction_open,
        learning_friction_resolved=friction_resolved,
        dogfood_confidence_trend=dogfood_confidence_trend(),
        dogfood_motivation_trend=dogfood_motivation_trend(),
        dogfood_completion_trend=dogfood_completion_trend(),
        dogfood_study_consistency=dogfood_study_consistency(),
        dogfood_friction_trend=dogfood_friction_trend(),
        dogfood_metrics=metrics,
        package_readiness=package_ready,
    )
