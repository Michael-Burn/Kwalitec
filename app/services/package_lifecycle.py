"""Package lifecycle registry — V1S-003 repository health.

Classifies repository packages by lifecycle, owner, and recommended action.
Consumed by the Founder Version 1 Readiness dashboard.
Does not change educational algorithms or delete packages.
"""

from __future__ import annotations

from dataclasses import dataclass

# Lifecycle values (Package Lifecycle Policy).
LIFECYCLE_ACTIVE = "ACTIVE"
LIFECYCLE_MAINTENANCE = "MAINTENANCE"
LIFECYCLE_DEPRECATED = "DEPRECATED"
LIFECYCLE_ARCHIVED = "ARCHIVED"
LIFECYCLE_REMOVE = "REMOVE"

LIFECYCLE_VALUES = frozenset(
    {
        LIFECYCLE_ACTIVE,
        LIFECYCLE_MAINTENANCE,
        LIFECYCLE_DEPRECATED,
        LIFECYCLE_ARCHIVED,
        LIFECYCLE_REMOVE,
    }
)


@dataclass(frozen=True)
class PackageEntry:
    """One owned package with a single lifecycle disposition."""

    path: str
    layer: str
    responsibility: str
    owner: str
    lifecycle: str  # ACTIVE | MAINTENANCE | DEPRECATED | ARCHIVED | REMOVE
    recommendation: str  # retain | split | merge | extract | archive | remove
    notes: str


@dataclass(frozen=True)
class EngineeringMetric:
    """Provisional engineering-quality signal for founder review."""

    name: str
    score: int  # 0–100 provisional
    status: str  # PASS | HOLD | FAIL | IN_PROGRESS
    summary: str
    actions: tuple[str, ...] = ()


@dataclass(frozen=True)
class CodeDebtItem:
    """Engineering debt distinct from educational runtime debt."""

    item: str
    category: str  # size | duplication | lifecycle | dual-tree | docs | tests
    severity: str
    owner: str
    recommendation: str


# ---------------------------------------------------------------------------
# Top-level repository trees
# ---------------------------------------------------------------------------

TOP_LEVEL_PACKAGES: tuple[PackageEntry, ...] = (
    PackageEntry(
        path="app/",
        layer="product",
        responsibility="Commercial Flask product (dogfood / Runtime C spine)",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Canonical student + founder product surface.",
    ),
    PackageEntry(
        path="src/",
        layer="education-os",
        responsibility="Version 2 Educational Operating System (parallel tree)",
        owner="Architecture governance (APP-003)",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="archive",
        notes=(
            "On pytest pythonpath; zero production imports into app/. "
            "Treat as Education OS library under maintenance until "
            "adoption or physical archive."
        ),
    ),
    PackageEntry(
        path="tests/",
        layer="verification",
        responsibility="Behaviour, independence, and architecture tests",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="split",
        notes=(
            "~1100 test modules; prefer programme suites + architecture/ "
            "over duplicate independence matrices for archived packages."
        ),
    ),
    PackageEntry(
        path="docs/",
        layer="governance",
        responsibility="Engineering charter, dependency rules, ADRs",
        owner="Architecture",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Governing for src/; V1S-003 adds docs/engineering for app/.",
    ),
    PackageEntry(
        path="knowledge/",
        layer="governance",
        responsibility="Product, educational, and constitutional corpora",
        owner="Founder / educational governance",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Authoritative product law; not runtime code.",
    ),
    PackageEntry(
        path="migrations/",
        layer="persistence",
        responsibility="Alembic schema versions",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Sole schema-change path.",
    ),
    PackageEntry(
        path="ops/",
        layer="operations",
        responsibility="Deploy / ops helpers",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Operational scripts; keep thin.",
    ),
    PackageEntry(
        path="scripts/",
        layer="tooling",
        responsibility="Developer and recovery scripts",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Not imported by the request path.",
    ),
    PackageEntry(
        path="research/",
        layer="research",
        responsibility="Research programme assets",
        owner="Founder research",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Separate from student product spine.",
    ),
    PackageEntry(
        path="prompts/",
        layer="tooling",
        responsibility="Agent / reviewer prompt library",
        owner="Founder tooling",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Cursor / reviewer framework inputs.",
    ),
    PackageEntry(
        path="tools/",
        layer="tooling",
        responsibility="Misc developer tools",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Low traffic.",
    ),
)


# ---------------------------------------------------------------------------
# app/ top-level packages
# ---------------------------------------------------------------------------

APP_TOP_LEVEL: tuple[PackageEntry, ...] = (
    PackageEntry(
        path="app/application/",
        layer="application",
        responsibility="Use-case engines and educational authorities",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="split",
        notes="~70 packages; lifecycle matrix below is authoritative.",
    ),
    PackageEntry(
        path="app/domain/",
        layer="domain",
        responsibility="Domain models / pure educational meaning under app/",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Paired with application packages; learning_events unused.",
    ),
    PackageEntry(
        path="app/presentation/",
        layer="presentation",
        responsibility="HTTP blueprints, VMs, Adaptive Workspace composer",
        owner="Student experience",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Must consume engines; never reimplement KWP math.",
    ),
    PackageEntry(
        path="app/services/",
        layer="services",
        responsibility="Flask-era orchestration + metrics + readiness",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="split",
        notes=(
            "Several god modules (planning/recommendation >1400 LOC). "
            "Ownership registry + lifecycle live here."
        ),
    ),
    PackageEntry(
        path="app/infrastructure/",
        layer="infrastructure",
        responsibility="Adapters, persistence, session composition",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Opaque demo bridges scheduled for fail-closed.",
    ),
    PackageEntry(
        path="app/curriculum/",
        layer="curriculum",
        responsibility="On-disk syllabus JSON + load_auto repository",
        owner="Curriculum",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Loader singularity (A1).",
    ),
    PackageEntry(
        path="app/models/",
        layer="persistence",
        responsibility="SQLAlchemy ORM models",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Must not import blueprints.",
    ),
    PackageEntry(
        path="app/founder/",
        layer="founder",
        responsibility="Console, feedback hub, operational health, V1 readiness",
        owner="Founder OS",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Admin-only; observability not educational authority.",
    ),
    PackageEntry(
        path="app/auth/",
        layer="auth",
        responsibility="Login / invite-only auth",
        owner="Security",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="No public registration.",
    ),
    PackageEntry(
        path="app/mission/",
        layer="presentation",
        responsibility="Legacy mission blueprint shell",
        owner="Runtime A coexistence",
        lifecycle=LIFECYCLE_DEPRECATED,
        recommendation="archive",
        notes="Redirect / coexistence under sole runtime; RI-002 retirement.",
    ),
    PackageEntry(
        path="app/dashboard/",
        layer="presentation",
        responsibility="Legacy dashboard shell",
        owner="Runtime A coexistence",
        lifecycle=LIFECYCLE_DEPRECATED,
        recommendation="archive",
        notes="Redirect shell under sole runtime policy.",
    ),
    PackageEntry(
        path="app/analytics/",
        layer="presentation",
        responsibility="Legacy analytics shell",
        owner="Runtime A coexistence",
        lifecycle=LIFECYCLE_DEPRECATED,
        recommendation="archive",
        notes="History redirect under sole runtime.",
    ),
    PackageEntry(
        path="app/study_plan/",
        layer="presentation",
        responsibility="Study plan wizard HTTP",
        owner="Study planning",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Shared workflow; Runtime A planning until RI-002.",
    ),
    PackageEntry(
        path="app/settings/",
        layer="presentation",
        responsibility="Account settings",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Thin HTTP.",
    ),
    PackageEntry(
        path="app/calibration/",
        layer="presentation",
        responsibility="Operator calibration UI",
        owner="Founder / ops",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Operator surface; application.calibration is tests-heavy.",
    ),
    PackageEntry(
        path="app/research/",
        layer="presentation",
        responsibility="Product check-in intake",
        owner="Founder research",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Student research feedback path.",
    ),
    PackageEntry(
        path="app/security/",
        layer="security",
        responsibility="Security headers / helpers",
        owner="Security",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Preserve CSP behaviour.",
    ),
    PackageEntry(
        path="app/alpha/",
        layer="alpha",
        responsibility="Internal alpha helpers",
        owner="Internal alpha",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Dogfood enablement support.",
    ),
    PackageEntry(
        path="app/automation/",
        layer="automation",
        responsibility="Background / job automation",
        owner="Platform engineering",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Not on student request critical path.",
    ),
)


# ---------------------------------------------------------------------------
# app/application — complete package matrix
# ---------------------------------------------------------------------------

APPLICATION_PACKAGES: tuple[PackageEntry, ...] = (
    # --- Dogfood / KWP ACTIVE spine ---
    PackageEntry(
        path="app/application/educational_runtime_engine",
        layer="application",
        responsibility="Mission instance authority (enrol / accept / complete)",
        owner="Educational Runtime",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="split",
        notes="service.py ~1400 LOC — candidate extract for coexistence helpers.",
    ),
    PackageEntry(
        path="app/application/learning_session",
        layer="application",
        responsibility="Sitting FSM / evidence candidates",
        owner="Learning Session Runtime",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Canonical session spine with StudentRuntimeCoordinator.",
    ),
    PackageEntry(
        path="app/application/student_runtime",
        layer="application",
        responsibility="Spine glue: accept ≡ session start",
        owner="Student Runtime Coordinator",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="No substance invention.",
    ),
    PackageEntry(
        path="app/application/educational_experience",
        layer="application",
        responsibility="Runtime C Home projection snapshots",
        owner="Educational Experience",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Consumed by Adaptive Workspace.",
    ),
    PackageEntry(
        path="app/application/educational_packages",
        layer="application",
        responsibility="Certified educational package loader and chrome (EA-006)",
        owner="Educational Packages",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Runtime C mission/session substance from certified packages.",
    ),
    PackageEntry(
        path="app/application/student_baseline",
        layer="application",
        responsibility="SB-001A baseline declarations after plan wizard",
        owner="Student Baseline",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Canonical post-plan onboarding; replaces legacy calibration-only path.",
    ),
    PackageEntry(
        path="app/application/adaptive_decision",
        layer="application",
        responsibility="ADR-027 M0 SittingDecisionOrchestrator + Policy V0",
        owner="Adaptive Decision",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes=(
            "Flag-gated (KWALITEC_ADR027_M0_DECISION_BOUNDARY default OFF). "
            "Runtime C must not import this package."
        ),
    ),
    PackageEntry(
        path="app/application/curriculum_intelligence",
        layer="application",
        responsibility="Certified packages + CertifiedMissionEngine",
        owner="Curriculum Intelligence",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="split",
        notes="Largest application package (~13.7k LOC / 61 files).",
    ),
    PackageEntry(
        path="app/application/curriculum_studio",
        layer="application",
        responsibility="Founder curriculum studio workflows",
        owner="Curriculum Studio",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Founder authoring / publish path.",
    ),
    PackageEntry(
        path="app/application/curriculum_studio_foundation",
        layer="application",
        responsibility="PublishedCurriculumAuthority + foundation services",
        owner="Curriculum Studio Foundation",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Dogfood student curriculum authority (V1S-002).",
    ),
    PackageEntry(
        path="app/application/progress_engine",
        layer="application",
        responsibility="Progress singularity write path",
        owner="Progress Engine",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Singularity residuals scheduled separately.",
    ),
    PackageEntry(
        path="app/application/learning_strategy",
        layer="application",
        responsibility="Learning Strategy authority (KWP-007)",
        owner="Learning Strategy",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="CLEAN — presentation consumes only.",
    ),
    PackageEntry(
        path="app/application/learning_diagnostics",
        layer="application",
        responsibility="Learning Diagnostics authority (KWP-008)",
        owner="Learning Diagnostics",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="CLEAN.",
    ),
    PackageEntry(
        path="app/application/learning_difficulty",
        layer="application",
        responsibility="Learning Difficulty authority (KWP-009)",
        owner="Learning Difficulty",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="CLEAN.",
    ),
    PackageEntry(
        path="app/application/intervention_effectiveness",
        layer="application",
        responsibility="Intervention Effectiveness authority (KWP-010)",
        owner="Intervention Effectiveness",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="CLEAN.",
    ),
    PackageEntry(
        path="app/application/educational_memory",
        layer="application",
        responsibility="Educational Memory authority (KWP-011)",
        owner="Educational Memory",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="CLEAN.",
    ),
    PackageEntry(
        path="app/application/readiness_forecast",
        layer="application",
        responsibility="Readiness Forecast authority (KWP-012)",
        owner="Readiness Forecast",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="CLEAN.",
    ),
    PackageEntry(
        path="app/application/knowledge_architecture",
        layer="application",
        responsibility="Knowledge Architecture / Curriculum Map (KWP-014)",
        owner="Knowledge Architecture",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="CLEAN.",
    ),
    PackageEntry(
        path="app/application/educational_authoring",
        layer="application",
        responsibility="Learning Episode composition (KWP-015)",
        owner="Educational Authoring",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Composition only — never selects missions.",
    ),
    PackageEntry(
        path="app/application/session_experience",
        layer="application",
        responsibility="Session HTTP/navigation adapter facade",
        owner="Session Experience",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Presentation adapter; not educational math.",
    ),
    PackageEntry(
        path="app/application/platform_integration",
        layer="application",
        responsibility="Runtime routing + founder/student bridge flags",
        owner="Platform Integration",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Dogfood cutover allowlist lives here.",
    ),
    PackageEntry(
        path="app/application/config",
        layer="application",
        responsibility="V2 / feature flag configuration",
        owner="Platform configuration",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Widely imported; keep flag ownership here.",
    ),
    PackageEntry(
        path="app/application/curriculum",
        layer="application",
        responsibility="Thin curriculum application facade",
        owner="Curriculum",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="merge",
        notes="Small facade; prefer CurriculumService / studio foundation.",
    ),
    PackageEntry(
        path="app/application/educational_engine_foundation",
        layer="application",
        responsibility="Derive foundation state for ERE",
        owner="Educational Engine Foundation",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="On mission spine (derive step).",
    ),
    PackageEntry(
        path="app/application/educational_quality",
        layer="application",
        responsibility="Educational quality certification",
        owner="Educational Quality",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Certifier used by curriculum intelligence path.",
    ),
    PackageEntry(
        path="app/application/student_twin",
        layer="application",
        responsibility="Student twin consumption / daily loop codec",
        owner="Student Twin",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="merge",
        notes="Overlaps student_digital_twin / twin — consolidate vocabulary.",
    ),
    PackageEntry(
        path="app/application/student_experience",
        layer="application",
        responsibility="Student experience projections (legacy + adaptive)",
        owner="Student Experience",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="split",
        notes="Large; Adaptive Workspace presentation is the dogfood surface.",
    ),
    PackageEntry(
        path="app/application/unified_journey",
        layer="application",
        responsibility="Unified journey experience contracts",
        owner="Student Experience",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Still referenced from presentation / adapters.",
    ),
    # --- Founder / EI ACTIVE (not student Home spine) ---
    PackageEntry(
        path="app/application/adaptive_mission",
        layer="application",
        responsibility="Founder Adaptive Mission + MissionPlanning bridge",
        owner="Adaptive Mission / EI",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="extract",
        notes="Depends on mission_engine.planning — extract before ME delete.",
    ),
    PackageEntry(
        path="app/application/mission_engine",
        layer="application",
        responsibility="Legacy MissionEngine shell + planning/",
        owner="Mission consolidation",
        lifecycle=LIFECYCLE_DEPRECATED,
        recommendation="extract",
        notes=(
            "V1S-002 DEPRECATED shell. Keep planning/ ACTIVE via extract to "
            "mission_planning/; then archive shell."
        ),
    ),
    PackageEntry(
        path="app/application/mission_engine_v2",
        layer="application",
        responsibility="Unwired MissionEngineV2",
        owner="Mission consolidation",
        lifecycle=LIFECYCLE_ARCHIVED,
        recommendation="remove",
        notes="Tests-only consumers. Gate: migrate independence tests.",
    ),
    PackageEntry(
        path="app/application/mission_adapter",
        layer="application",
        responsibility="V1/V2 mission migration router",
        owner="Mission consolidation",
        lifecycle=LIFECYCLE_ARCHIVED,
        recommendation="remove",
        notes="Tests-only. Archive with MissionEngineV2.",
    ),
    PackageEntry(
        path="app/application/curriculum_extraction",
        layer="application",
        responsibility="CMP / curriculum extraction pipeline",
        owner="Curriculum Extraction (EI)",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Founder/EI path; not student Home.",
    ),
    PackageEntry(
        path="app/application/curriculum_ingestion",
        layer="application",
        responsibility="Curriculum ingestion workflows",
        owner="Curriculum Ingestion",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Studio / import adjacent.",
    ),
    PackageEntry(
        path="app/application/curriculum_publishing",
        layer="application",
        responsibility="Curriculum publishing workflows",
        owner="Curriculum Publishing",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Zero direct presentation imports; studio path.",
    ),
    PackageEntry(
        path="app/application/curriculum_management",
        layer="application",
        responsibility="Curriculum management operations",
        owner="Curriculum Management",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Founder management surface.",
    ),
    PackageEntry(
        path="app/application/curriculum_retrieval",
        layer="application",
        responsibility="Curriculum retrieval queries",
        owner="Curriculum Retrieval",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Query helpers for studio / intelligence.",
    ),
    PackageEntry(
        path="app/application/educational_intelligence_pipeline",
        layer="application",
        responsibility="EI pipeline registry / health / orchestrator",
        owner="Educational Intelligence Pipeline",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Still references mission_engine — update on ME extract.",
    ),
    PackageEntry(
        path="app/application/educational_reasoning",
        layer="application",
        responsibility="Educational reasoning application shell",
        owner="Educational Reasoning",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="merge",
        notes="Overlaps educational_reasoning_engine naming.",
    ),
    PackageEntry(
        path="app/application/educational_reasoning_engine",
        layer="application",
        responsibility="Educational reasoning engine application API",
        owner="Educational Reasoning Engine",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Prefer single public entry; fold sibling if unused.",
    ),
    PackageEntry(
        path="app/application/intelligent_tutor",
        layer="application",
        responsibility="Intelligent tutor application service",
        owner="Intelligent Tutor",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Not on Adaptive Workspace dogfood spine.",
    ),
    PackageEntry(
        path="app/application/adaptive_assessment",
        layer="application",
        responsibility="Adaptive assessment / quick check",
        owner="Adaptive Assessment",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Presentation blueprint exists; not Home primary path.",
    ),
    PackageEntry(
        path="app/application/assessment_pipeline",
        layer="application",
        responsibility="Assessment pipeline orchestration",
        owner="Assessment Pipeline",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Adjacent to adaptive assessment.",
    ),
    PackageEntry(
        path="app/application/adaptive_learning",
        layer="application",
        responsibility="Adaptive learning application services",
        owner="Adaptive Learning",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Runtime A adjacent; not KWP engine.",
    ),
    PackageEntry(
        path="app/application/learning_orchestrator",
        layer="application",
        responsibility="Learning orchestrator (flag-gated)",
        owner="Learning Orchestrator",
        lifecycle=LIFECYCLE_DEPRECATED,
        recommendation="archive",
        notes="ENABLE_EDUCATIONAL_ORCHESTRATOR default OFF.",
    ),
    PackageEntry(
        path="app/application/orchestration",
        layer="application",
        responsibility="Generic orchestration helpers",
        owner="Orchestration",
        lifecycle=LIFECYCLE_DEPRECATED,
        recommendation="merge",
        notes="Zero presentation imports; fold or archive.",
    ),
    PackageEntry(
        path="app/application/learning_loop",
        layer="application",
        responsibility="Learning loop experiment shell",
        owner="Learning Loop",
        lifecycle=LIFECYCLE_ARCHIVED,
        recommendation="remove",
        notes="Zero production / cross-application consumers.",
    ),
    PackageEntry(
        path="app/application/learning_activity",
        layer="application",
        responsibility="Learning activity application models",
        owner="Learning Activity",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Tests-heavy; domain consumers exist.",
    ),
    PackageEntry(
        path="app/application/learning_evidence",
        layer="application",
        responsibility="Learning evidence application helpers",
        owner="Evidence (prefer EducationalEvidenceAuthority)",
        lifecycle=LIFECYCLE_DEPRECATED,
        recommendation="merge",
        notes="Authority is services.educational_evidence_authority.",
    ),
    PackageEntry(
        path="app/application/learning_graph",
        layer="application",
        responsibility="Learning graph application services",
        owner="Learning Graph",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="merge",
        notes="Prefer knowledge_architecture for student Curriculum Map.",
    ),
    PackageEntry(
        path="app/application/learning_journey",
        layer="application",
        responsibility="Learning journey application services",
        owner="Learning Journey",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Distinct from Educational Memory narrative journey.",
    ),
    PackageEntry(
        path="app/application/instructional_blueprint",
        layer="application",
        responsibility="Instructional blueprint generation",
        owner="Instructional Blueprint",
        lifecycle=LIFECYCLE_ARCHIVED,
        recommendation="remove",
        notes="Zero production / cross-application consumers; tests-only.",
    ),
    PackageEntry(
        path="app/application/calibration",
        layer="application",
        responsibility="Calibration application services",
        owner="Calibration",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Paired with app/calibration blueprint.",
    ),
    PackageEntry(
        path="app/application/constraints",
        layer="application",
        responsibility="Planning constraints",
        owner="Planning constraints",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Small; Runtime A planning adjacent.",
    ),
    PackageEntry(
        path="app/application/reasoning",
        layer="application",
        responsibility="Generic reasoning application shell",
        owner="Reasoning",
        lifecycle=LIFECYCLE_DEPRECATED,
        recommendation="merge",
        notes="Prefer educational_reasoning_engine naming.",
    ),
    PackageEntry(
        path="app/application/runtime_integration",
        layer="application",
        responsibility="Runtime A/C integration bridges",
        owner="Runtime Integration",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Coexistence until RI-002.",
    ),
    PackageEntry(
        path="app/application/education_platform",
        layer="application",
        responsibility="Education platform composition helpers",
        owner="Education Platform",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Broad facade; avoid new student math here.",
    ),
    PackageEntry(
        path="app/application/dashboard",
        layer="application",
        responsibility="Dashboard application helpers",
        owner="Dashboard",
        lifecycle=LIFECYCLE_DEPRECATED,
        recommendation="archive",
        notes="Legacy dashboard application layer.",
    ),
    PackageEntry(
        path="app/application/decision_journal",
        layer="application",
        responsibility="Decision journal application API",
        owner="Decision Journal",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Founder / research adjacent.",
    ),
    PackageEntry(
        path="app/application/daily_mission_intelligence",
        layer="application",
        responsibility="Daily mission intelligence briefs",
        owner="Daily Mission Intelligence",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Not sole Home mission authority.",
    ),
    PackageEntry(
        path="app/application/educational_experience_engine",
        layer="application",
        responsibility="Educational experience engine (parallel naming)",
        owner="Educational Experience Engine",
        lifecycle=LIFECYCLE_DEPRECATED,
        recommendation="merge",
        notes="Prefer educational_experience for Runtime C snapshots.",
    ),
    PackageEntry(
        path="app/application/educational_feedback_loop",
        layer="application",
        responsibility="Educational feedback loop application",
        owner="Educational Feedback Loop",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Thin; metrics via services.",
    ),
    PackageEntry(
        path="app/application/educational_state",
        layer="application",
        responsibility="Educational state ownership helpers",
        owner="Educational State",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="EIP-001 adjacent.",
    ),
    PackageEntry(
        path="app/application/educational_timeline",
        layer="application",
        responsibility="Educational timeline application",
        owner="Educational Timeline",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Narrative timeline projections.",
    ),
    PackageEntry(
        path="app/application/founder_validation",
        layer="application",
        responsibility="Founder validation workflows",
        owner="Founder Validation",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Console / quality gates.",
    ),
    PackageEntry(
        path="app/application/learner_lifecycle",
        layer="application",
        responsibility="Learner lifecycle orchestration",
        owner="Learner Lifecycle",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Enrolment / checkpoint hooks.",
    ),
    PackageEntry(
        path="app/application/learner_progress",
        layer="application",
        responsibility=(
            "Honest Progress read-side: qualifying study days, streaks, milestones"
        ),
        owner="Learner Progress",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes=(
            "Flag-independent index over Accepted Educational+ evidence packages. "
            "Does not write Twin state."
        ),
    ),
    PackageEntry(
        path="app/application/student_curriculum_binding",
        layer="application",
        responsibility="Student ↔ curriculum binding",
        owner="Student Curriculum Binding",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="EI-004 path; not presentation-direct.",
    ),
    PackageEntry(
        path="app/application/student_digital_twin",
        layer="application",
        responsibility="Student digital twin application API",
        owner="Student Digital Twin",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="merge",
        notes="Triple twin naming with twin/ and student_twin/.",
    ),
    PackageEntry(
        path="app/application/twin",
        layer="application",
        responsibility="Twin foundation application API",
        owner="Twin",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="merge",
        notes="Widely cross-imported; designate canonical twin package.",
    ),
    PackageEntry(
        path="app/application/twin_inference",
        layer="application",
        responsibility="Twin inference application",
        owner="Twin Inference",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="EI-006; not Home presentation-direct.",
    ),
    PackageEntry(
        path="app/application/twin_repository",
        layer="application",
        responsibility="Twin repository ports / adapters glue",
        owner="Twin Repository",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Persistence-facing twin access.",
    ),
    PackageEntry(
        path="app/application/twin_update",
        layer="application",
        responsibility="Twin update application",
        owner="Twin Update",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="Update path; keep behind Evidence Authority.",
    ),
)


# ---------------------------------------------------------------------------
# Domain packages with notable dispositions
# ---------------------------------------------------------------------------

DOMAIN_PACKAGES: tuple[PackageEntry, ...] = (
    PackageEntry(
        path="app/domain/curriculum",
        layer="domain",
        responsibility="Curriculum domain value objects / aggregates",
        owner="Curriculum domain",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Highest domain consumer count.",
    ),
    PackageEntry(
        path="app/domain/mission",
        layer="domain",
        responsibility="MissionIntelligence + mission domain types",
        owner="Mission domain",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="retain",
        notes="MissionIntelligence SCHEDULED off Home (orchestrator OFF).",
    ),
    PackageEntry(
        path="app/domain/learning_events",
        layer="domain",
        responsibility="Learning event domain types",
        owner="Learning Events",
        lifecycle=LIFECYCLE_REMOVE,
        recommendation="remove",
        notes="Zero application/services/presentation/infra consumers.",
    ),
    PackageEntry(
        path="app/domain/student_twin",
        layer="domain",
        responsibility="Student twin domain",
        owner="Student Twin domain",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="merge",
        notes="Overlaps twin / student_digital_twin domains.",
    ),
    PackageEntry(
        path="app/domain/twin",
        layer="domain",
        responsibility="Twin domain foundation",
        owner="Twin domain",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="merge",
        notes="Canonical twin domain TBD in twin consolidation.",
    ),
    PackageEntry(
        path="app/domain/student_digital_twin",
        layer="domain",
        responsibility="Student digital twin domain",
        owner="Student Digital Twin domain",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="merge",
        notes="Third twin domain package.",
    ),
    PackageEntry(
        path="app/domain/educational_runtime_engine",
        layer="domain",
        responsibility="ERE domain state / events",
        owner="Educational Runtime domain",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Paired with application ERE.",
    ),
    PackageEntry(
        path="app/domain/session_experience",
        layer="domain",
        responsibility="Session experience projections",
        owner="Session Experience domain",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Navigation / workspace projections.",
    ),
    PackageEntry(
        path="app/domain/curriculum_studio_foundation",
        layer="domain",
        responsibility="Published curriculum foundation types",
        owner="Curriculum Studio Foundation domain",
        lifecycle=LIFECYCLE_ACTIVE,
        recommendation="retain",
        notes="Authority substrate.",
    ),
)


# ---------------------------------------------------------------------------
# src/ Education OS (tree-level; detailed purity owned by docs/DEPENDENCY_RULES)
# ---------------------------------------------------------------------------

SRC_TREE_PACKAGES: tuple[PackageEntry, ...] = (
    PackageEntry(
        path="src/domain/",
        layer="education-os-domain",
        responsibility="Pure educational core (~55k LOC)",
        owner="Education OS",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="archive",
        notes="Architecture purity tests active; not wired into app dogfood.",
    ),
    PackageEntry(
        path="src/application/",
        layer="education-os-application",
        responsibility="Education OS use-cases / pipeline / student_experience",
        owner="Education OS",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="archive",
        notes="Parallel to app/application — do not dual-implement features.",
    ),
    PackageEntry(
        path="src/infrastructure/",
        layer="education-os-infrastructure",
        responsibility="Education OS persistence / AI enrichment",
        owner="Education OS",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="archive",
        notes="AI enrichment must not own educational decisions.",
    ),
    PackageEntry(
        path="src/presentation/",
        layer="education-os-presentation",
        responsibility="Education OS presentation / design system extracts",
        owner="Education OS",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="archive",
        notes="Design system overlap with app/templates.",
    ),
    PackageEntry(
        path="src/web/",
        layer="education-os-web",
        responsibility="Education OS Flask web shell",
        owner="Education OS",
        lifecycle=LIFECYCLE_ARCHIVED,
        recommendation="remove",
        notes="Not the create_app product factory.",
    ),
    PackageEntry(
        path="src/adapters/",
        layer="education-os-adapters",
        responsibility="Education OS Flask adapters",
        owner="Education OS",
        lifecycle=LIFECYCLE_ARCHIVED,
        recommendation="remove",
        notes="Parallel adapters; product uses app/infrastructure.",
    ),
)


ROOT_DOC_CLUTTER: tuple[PackageEntry, ...] = (
    PackageEntry(
        path="*.md (repository root programme reports)",
        layer="docs-clutter",
        responsibility="Programme implementation reports at repo root",
        owner="Documentation hygiene",
        lifecycle=LIFECYCLE_MAINTENANCE,
        recommendation="archive",
        notes=(
            "50+ KWP/V1S/MISSION reports at root. Move completed reports to "
            "docs/reports/ or knowledge/archive/ — keep only active gates."
        ),
    ),
)


ALL_PACKAGE_ENTRIES: tuple[PackageEntry, ...] = (
    TOP_LEVEL_PACKAGES
    + APP_TOP_LEVEL
    + APPLICATION_PACKAGES
    + DOMAIN_PACKAGES
    + SRC_TREE_PACKAGES
    + ROOT_DOC_CLUTTER
)


ENGINEERING_QUALITY_METRICS: tuple[EngineeringMetric, ...] = (
    EngineeringMetric(
        name="Repository navigability",
        score=62,
        status="IN_PROGRESS",
        summary=(
            "Dogfood spine is documented (V1S-002), but ~70 application "
            "packages plus a parallel src/ tree and 50+ root reports still "
            "make first navigation hard."
        ),
        actions=(
            "Use package lifecycle matrix as the map",
            "Relocate root programme reports",
            "Do not add features under src/ for dogfood",
        ),
    ),
    EngineeringMetric(
        name="Package lifecycle clarity",
        score=78,
        status="PASS",
        summary=(
            "Every audited package now has one lifecycle and one owner in "
            "package_lifecycle.py. Physical deletes remain gated."
        ),
        actions=(
            "Execute REMOVE gates for MissionEngineV2 / MissionAdapter",
            "Extract MissionPlanningService before ME shell delete",
        ),
    ),
    EngineeringMetric(
        name="Module size / god classes",
        score=55,
        status="HOLD",
        summary=(
            "Multiple >1000 LOC modules remain (planning_service, "
            "recommendation_service, ERE service, student view_models, "
            "evidence_platform contracts)."
        ),
        actions=(
            "Split planning_service along Runtime A retirement seams",
            "Cap new modules at ~400 LOC guidance (Module Standards)",
        ),
    ),
    EngineeringMetric(
        name="Naming consistency",
        score=58,
        status="HOLD",
        summary=(
            "Triple twin packages (twin / student_twin / "
            "student_digital_twin) and dual reasoning / experience engine "
            "names increase cognitive load."
        ),
        actions=(
            "Publish canonical twin package name",
            "Alias-and-deprecate sibling packages",
        ),
    ),
    EngineeringMetric(
        name="Dependency direction",
        score=72,
        status="PASS",
        summary=(
            "app/ layering (presentation → application/services → domain → "
            "infra) largely holds. src/ has stricter architecture tests. "
            "Cross-tree imports between app and src are essentially zero."
        ),
        actions=(
            "Keep zero app↔src runtime coupling",
            "Enforce no new archived-package imports on student spine",
        ),
    ),
    EngineeringMetric(
        name="Test quality",
        score=68,
        status="IN_PROGRESS",
        summary=(
            "Strong architecture purity and programme suites exist, but "
            "archived packages still carry large independence suites and "
            "some tests assert implementation details."
        ),
        actions=(
            "Prefer behaviour tests on ACTIVE packages",
            "Retire independence suites when packages are removed",
        ),
    ),
)


CODE_DEBT_REGISTER: tuple[CodeDebtItem, ...] = (
    CodeDebtItem(
        item="Parallel Education OS tree (src/) unwired from product",
        category="dual-tree",
        severity="High",
        owner="Architecture / V1S follow-up",
        recommendation="Decide adopt-or-archive; freeze new dogfood work in src/",
    ),
    CodeDebtItem(
        item="MissionEngineV2 + MissionAdapter source still in tree",
        category="lifecycle",
        severity="High",
        owner="Mission consolidation",
        recommendation="REMOVE after independence-test migration",
    ),
    CodeDebtItem(
        item="MissionEngine shell + planning/ co-located",
        category="lifecycle",
        severity="High",
        owner="Mission consolidation",
        recommendation="Extract mission_planning/; archive shell",
    ),
    CodeDebtItem(
        item="Triple twin package naming",
        category="duplication",
        severity="Medium",
        owner="Twin consolidation",
        recommendation="Pick canonical package; deprecate aliases",
    ),
    CodeDebtItem(
        item="God services (planning / recommendation / research_insight)",
        category="size",
        severity="Medium",
        owner="Platform engineering",
        recommendation="Split along seam lines; no behaviour change",
    ),
    CodeDebtItem(
        item="curriculum_intelligence package size (~13.7k LOC)",
        category="size",
        severity="Medium",
        owner="Curriculum Intelligence",
        recommendation="Split certified mission vs generation store facets",
    ),
    CodeDebtItem(
        item="Root-level programme report clutter (50+ markdown)",
        category="docs",
        severity="Low",
        owner="Documentation hygiene",
        recommendation="Move completed reports under docs/reports/",
    ),
    CodeDebtItem(
        item="domain/learning_events zero consumers",
        category="lifecycle",
        severity="Low",
        owner="Domain housekeeping",
        recommendation="REMOVE after confirming no dynamic import",
    ),
    CodeDebtItem(
        item="application/learning_loop + instructional_blueprint unused",
        category="lifecycle",
        severity="Medium",
        owner="Application housekeeping",
        recommendation="REMOVE after dropping tests-only references",
    ),
    CodeDebtItem(
        item="Legacy presentation shells (mission/dashboard/analytics)",
        category="lifecycle",
        severity="Medium",
        owner="RI-002",
        recommendation="Archive when sole-runtime redirects retire",
    ),
    CodeDebtItem(
        item="Opaque Phase-I demo bridges",
        category="lifecycle",
        severity="Medium",
        owner="Runtime hygiene",
        recommendation="Fail closed before stub deletion",
    ),
    CodeDebtItem(
        item="Archived-package independence test surface",
        category="tests",
        severity="Medium",
        owner="Test hygiene",
        recommendation="Migrate or delete with package REMOVE gates",
    ),
)


REPOSITORY_HEALTH_SUMMARY = (
    "V1S-003 audited app/ + src/ trees. Dogfood product authority lives "
    "under app/ with an owned package lifecycle matrix. src/ is "
    "MAINTENANCE / ARCHIVED relative to the commercial dogfood path. "
    "No educational behaviour changed; physical deletes remain gated."
)


def packages_by_lifecycle(lifecycle: str) -> tuple[PackageEntry, ...]:
    """Return all registry entries with the given lifecycle value."""
    return tuple(e for e in ALL_PACKAGE_ENTRIES if e.lifecycle == lifecycle)


def lifecycle_counts() -> dict[str, int]:
    """Count packages per lifecycle status."""
    counts = {value: 0 for value in sorted(LIFECYCLE_VALUES)}
    for entry in ALL_PACKAGE_ENTRIES:
        counts[entry.lifecycle] = counts.get(entry.lifecycle, 0) + 1
    return counts


def assert_registry_integrity() -> None:
    """Validate lifecycle values and unique paths (dev / test helper)."""
    seen: set[str] = set()
    for entry in ALL_PACKAGE_ENTRIES:
        if entry.lifecycle not in LIFECYCLE_VALUES:
            raise AssertionError(
                f"Invalid lifecycle {entry.lifecycle!r} for {entry.path}"
            )
        if entry.path in seen:
            raise AssertionError(f"Duplicate package path {entry.path!r}")
        seen.add(entry.path)
