"""Runtime ownership registry — V1S-002 / V1S-007 consolidation spine.

Single source of truth for which package owns each student-facing runtime
responsibility. Consumed by the Founder Version 1 Readiness dashboard.
Does not execute educational algorithms.

## A9 — Educational Runtime Singularity (V1S-007)

Every student educational interaction executes through one Educational Runtime.
Legacy implementations may remain in-repo as substrate or TEMPORARY paths for
students without Runtime C enrolment, but must never become an alternate
educational execution path once the Educational Runtime owns the student.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OwnershipEntry:
    """One owned runtime or curriculum responsibility."""

    capability: str
    owner: str
    entry_point: str
    status: str  # ACTIVE | SUBSTRATE | DEPRECATED | ARCHIVE | SCHEDULED
    notes: str


@dataclass(frozen=True)
class DebtEntry:
    """Scheduled or residual technical debt with an explicit owner."""

    item: str
    severity: str
    owner: str
    disposition: str  # REMOVED | SCHEDULED | RETAIN
    gate: str


# Version 1 dogfood subjects — one published authority when package is active.
DOGFOOD_SUBJECTS: tuple[str, ...] = ("CS1", "CB2", "CM1")

# Permanent architecture principle (V1S-007).
A9_EDUCATIONAL_RUNTIME_SINGULARITY = (
    "Every student educational interaction shall execute through one "
    "Educational Runtime. Missing prerequisites are resolved or surfaced by "
    "the Educational Runtime itself — never by routing into Runtime A."
)

CURRICULUM_AUTHORITY_MATRIX: tuple[OwnershipEntry, ...] = (
    OwnershipEntry(
        capability="Student curriculum authority (dogfood)",
        owner="PublishedCurriculumAuthority",
        entry_point=(
            "app.application.curriculum_studio_foundation.authority"
        ),
        status="ACTIVE",
        notes=(
            "When an active published package exists for CS1/CB2/CM1 and "
            "Runtime C enrolment is enabled, students enrol on "
            "PUBLISHED_CURRICULUM only (V1S-002 dogfood cutover)."
        ),
    ),
    OwnershipEntry(
        capability="On-disk syllabus loader",
        owner="CurriculumRepository.load_auto",
        entry_point="app.curriculum.repository",
        status="SUBSTRATE",
        notes=(
            "Canonical V1/V2 format detection. Not a student authority when "
            "a published package is active for the subject."
        ),
    ),
    OwnershipEntry(
        capability="DB import / traversal (Runtime A substrate)",
        owner="CurriculumService",
        entry_point="app.services.curriculum_service",
        status="SUBSTRATE",
        notes=(
            "Idempotent import and ordered topic traversal for JSON-backed "
            "paths and historical plans. Retained until RI-002 retirement."
        ),
    ),
    OwnershipEntry(
        capability="Certified package intelligence",
        owner="CertifiedLearningService / CertifiedMissionEngine",
        entry_point="app.application.curriculum_intelligence",
        status="ACTIVE",
        notes="Consumes published certified packages only.",
    ),
)


MISSION_RUNTIME_MATRIX: tuple[OwnershipEntry, ...] = (
    OwnershipEntry(
        capability="Mission instance authority",
        owner="EducationalRuntimeEngineService",
        entry_point="app.application.educational_runtime_engine.service",
        status="ACTIVE",
        notes="Accept / defer / complete / generate_daily_mission.",
    ),
    OwnershipEntry(
        capability="Mission topic selection",
        owner="CertifiedMissionEngine",
        entry_point=(
            "app.application.curriculum_intelligence.certified_mission_engine"
        ),
        status="ACTIVE",
        notes="Syllabus-order selection on certified packages (MISSION-002).",
    ),
    OwnershipEntry(
        capability="Session spine glue",
        owner="StudentRuntimeCoordinator",
        entry_point="app.application.student_runtime.coordinator",
        status="ACTIVE",
        notes="Accept ≡ Learning Session Runtime start; no substance invention.",
    ),
    OwnershipEntry(
        capability="Student Home projection",
        owner="EducationalExperienceService",
        entry_point="app.application.educational_experience.service",
        status="ACTIVE",
        notes="Runtime C → student-safe snapshots for Adaptive Workspace.",
    ),
    OwnershipEntry(
        capability="Application MissionEngine shell",
        owner="app.application.mission_engine (except planning/)",
        entry_point="app.application.mission_engine.engine",
        status="DEPRECATED",
        notes="Zero production student wiring. Schedule package archive.",
    ),
    OwnershipEntry(
        capability="MissionEngineV2",
        owner="app.application.mission_engine_v2",
        entry_point="app.application.mission_engine_v2.engine",
        status="ARCHIVE",
        notes="Unwired from app/ presentation and services. Tests-only.",
    ),
    OwnershipEntry(
        capability="MissionAdapter (migration router)",
        owner="app.application.mission_adapter",
        entry_point="app.application.mission_adapter.adapter",
        status="ARCHIVE",
        notes="Tests-only V1/V2 router. Not on student spine.",
    ),
    OwnershipEntry(
        capability="MissionIntelligence (domain)",
        owner="app.domain.mission.engine.MissionIntelligence",
        entry_point="app.domain.mission.engine",
        status="SCHEDULED",
        notes=(
            "Twin/orchestrator path; ENABLE_EDUCATIONAL_ORCHESTRATOR default "
            "OFF. Not student Home authority."
        ),
    ),
    OwnershipEntry(
        capability="MissionPlanningService",
        owner="app.application.mission_engine.planning",
        entry_point=(
            "app.application.mission_engine.planning.mission_planning_service"
        ),
        status="ACTIVE",
        notes=(
            "Founder Adaptive Mission + EI pipeline only. Extract before "
            "deleting mission_engine shell."
        ),
    ),
    OwnershipEntry(
        capability="Runtime A ORM missions",
        owner="PlanningService / MissionService",
        entry_point="app.services.planning_service",
        status="SCHEDULED",
        notes="Coexistence for non–Runtime C enrolments until RI-002.",
    ),
)


RUNTIME_OWNERSHIP_MATRIX: tuple[OwnershipEntry, ...] = (
    OwnershipEntry(
        capability="Educational Runtime (journey) — A9 singularity owner",
        owner="educational_runtime_engine",
        entry_point="EducationalRuntimeEngineService + ensure_active_sci",
        status="ACTIVE",
        notes=(
            "V1S-007: sole student educational execution path for Runtime C "
            "enrolments. Owns SCI ensure / readiness messaging."
        ),
    ),
    OwnershipEntry(
        capability="Student Curriculum Instance",
        owner="student_curriculum_binding + sci_lifecycle",
        entry_point=(
            "app.application.educational_runtime_engine.sci_lifecycle"
        ),
        status="ACTIVE",
        notes=(
            "Mandatory educational object. Created on enrolment / first "
            "launch via ensure_active_sci (CKG bridge from published package)."
        ),
    ),
    OwnershipEntry(
        capability="Learning Session Runtime",
        owner="learning_session",
        entry_point="LearningSessionRuntime",
        status="ACTIVE",
        notes="Sitting FSM / evidence candidates. Assumes SCI exists.",
    ),
    OwnershipEntry(
        capability="Student Runtime Coordinator",
        owner="student_runtime",
        entry_point="StudentRuntimeCoordinator",
        status="ACTIVE",
        notes="Spine glue only — never selects Runtime A.",
    ),
    OwnershipEntry(
        capability="Evidence",
        owner="EducationalEvidenceAuthority",
        entry_point="app.services.educational_evidence_authority",
        status="ACTIVE",
        notes="CLEAN — do not redesign in V1S-007.",
    ),
    OwnershipEntry(
        capability="Progress",
        owner="ProgressEngine",
        entry_point="app.application.progress_engine",
        status="ACTIVE",
        notes="Sole progress truth on Educational Runtime path (V1S-005).",
    ),
    OwnershipEntry(
        capability="Learning Journey",
        owner="educational_memory + readiness_forecast",
        entry_point="get_educational_memory_service / forecast engine",
        status="ACTIVE",
        notes="Narrative + forecast; no Runtime A execution.",
    ),
    OwnershipEntry(
        capability="Educational Authoring",
        owner="educational_authoring",
        entry_point="app.application.educational_authoring",
        status="ACTIVE",
        notes="Composition only — out of V1S-007 redesign scope.",
    ),
    OwnershipEntry(
        capability="Published Curriculum",
        owner="PublishedCurriculumAuthority",
        entry_point="app.application.curriculum_studio_foundation.authority",
        status="ACTIVE",
        notes="Student curriculum authority when package active.",
    ),
    OwnershipEntry(
        capability="Strategy → Authoring + Adaptive Workspace",
        owner="KWP-007…015 packages",
        entry_point="get_*_engine / compose_adaptive_workspace",
        status="ACTIVE",
        notes="Consumed, not reimplemented. Out of V1S-007 redesign scope.",
    ),
)


TECHNICAL_DEBT_REGISTER: tuple[DebtEntry, ...] = (
    DebtEntry(
        item="MissionEngineV2 package (unwired)",
        severity="High",
        owner="V1S-002 / Mission consolidation",
        disposition="SCHEDULED",
        gate="Archive after independence-test migration or delete tests",
    ),
    DebtEntry(
        item="MissionAdapter migration router (unwired)",
        severity="High",
        owner="V1S-002 / Mission consolidation",
        disposition="SCHEDULED",
        gate="Archive with MissionEngineV2",
    ),
    DebtEntry(
        item="MissionEngine application shell (except planning/)",
        severity="High",
        owner="V1S-002 follow-up",
        disposition="SCHEDULED",
        gate="Extract MissionPlanningService → mission_planning/",
    ),
    DebtEntry(
        item="Runtime A PlanningService.generate_today_mission",
        severity="High",
        owner="RI-002 retirement",
        disposition="SCHEDULED",
        gate=(
            "All RI-002 retirement gates PASS. V1S-007: blocked as fallback "
            "for Runtime C enrolments (A9); TEMPORARY for non–Runtime-C only."
        ),
    ),
    DebtEntry(
        item="Runtime C → Runtime A educational fallback",
        severity="Critical",
        owner="V1S-007 Educational Runtime Singularity",
        disposition="REMOVED",
        gate="A9 — ensure_active_sci + EducationalPrerequisiteMissing",
    ),
    DebtEntry(
        item="Progress singularity (CertifiedProgress + Runtime A mastery)",
        severity="High",
        owner="Progress singularity programme",
        disposition="SCHEDULED",
        gate="Out of V1S-007 scope",
    ),
    DebtEntry(
        item="Domain CurriculumRepository port (unimplemented)",
        severity="Low",
        owner="Curriculum housekeeping",
        disposition="SCHEDULED",
        gate="Rename port or wire adapter",
    ),
    DebtEntry(
        item="curriculum/seed.py vs import_curricula",
        severity="Low",
        owner="Curriculum housekeeping",
        disposition="SCHEDULED",
        gate="Document substrate; prefer import_curricula",
    ),
    DebtEntry(
        item="Opaque Phase-I demo bridges",
        severity="Medium",
        owner="Runtime hygiene",
        disposition="SCHEDULED",
        gate="Fail closed before stub deletion",
    ),
)


MISSION_SPINE = (
    "PublishedCurriculumPackage",
    "PublishedCurriculumAuthority.get_active",
    "ensure_active_sci (SCI mandatory)",
    "EducationalEngineFoundationService.derive",
    "EducationalRuntimeEngineService.generate_daily_mission",
    "CertifiedMissionEngine.generate (selection)",
    "EducationalExperienceService.load_for_user",
    "StudentHomeService + compose_adaptive_workspace",
    "StudentRuntimeCoordinator.accept_and_start_session",
    "LearningSessionRuntime",
    "Evidence → ProgressEngine → Learning Journey",
)


def curriculum_authority_for_dogfood_subject(
    subject_code: str,
    *,
    has_published_package: bool,
    runtime_c_enrolment_enabled: bool,
) -> str:
    """Resolve the intended student curriculum authority for a dogfood subject.

    Returns a RuntimeAuthority value string.
    """
    code = (subject_code or "").strip().upper()
    if code not in DOGFOOD_SUBJECTS:
        return "json_bundled"
    if runtime_c_enrolment_enabled and has_published_package:
        return "published_curriculum"
    return "json_bundled"
