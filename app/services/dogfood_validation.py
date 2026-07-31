"""V1S-006 — Live dogfood week evidence + learning friction registry.

Extends V1S-004/005 validation artefacts with exclusive-week live sittings,
before/after confidence & motivation, completion/consistency trends, and
new friction discovered during founder CS1 study.

Observation / evidence only — does not change educational algorithms.
"""

from __future__ import annotations

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Finding classes (V1S-005 remediation taxonomy)
# ---------------------------------------------------------------------------

CLASS_BUG = "BUG"
CLASS_LEARNING_FRICTION = "LEARNING FRICTION"
CLASS_UX_IMPROVEMENT = "UX IMPROVEMENT"
CLASS_TECHNICAL_DEBT = "TECHNICAL DEBT"
CLASS_DEFERRED = "DEFERRED"
CLASS_WORKS_WELL = "WORKS WELL"

FINDING_CLASSES = frozenset(
    {
        CLASS_BUG,
        CLASS_LEARNING_FRICTION,
        CLASS_UX_IMPROVEMENT,
        CLASS_TECHNICAL_DEBT,
        CLASS_DEFERRED,
        CLASS_WORKS_WELL,
    }
)

# Issue status
STATUS_OPEN = "OPEN"
STATUS_RESOLVED = "RESOLVED"
STATUS_DEFERRED = "DEFERRED"

# Priority
PRIORITY_P0 = "P0"
PRIORITY_P1 = "P1"
PRIORITY_P2 = "P2"


@dataclass(frozen=True)
class DogfoodProgressEntry:
    """One dogfood study sitting recorded during validation."""

    study_date: str
    subject: str
    mission_completed: str
    time_spent_minutes: int
    points_of_confusion: tuple[str, ...]
    missing_content: tuple[str, ...]
    poor_wording: tuple[str, ...]
    navigation_friction: tuple[str, ...]
    unexpected_behaviour: tuple[str, ...]
    suggestions: tuple[str, ...]
    four_question_notes: tuple[str, ...] = ()
    # provisional | validated — live sittings escalate confidence
    evidence_kind: str = "code_audit"
    # V1S-005 dogfood metrics
    confusion_score: int = 0  # 0–5 (lower better)
    confidence_score: int = 0  # 1–5 (after sitting; legacy alias)
    motivation_score: int = 0  # 1–5 (after sitting; legacy alias)
    workaround_count: int = 0
    # V1S-006 live-week fields
    confidence_before: int = 0  # 1–5
    confidence_after: int = 0  # 1–5
    motivation_before: int = 0  # 1–5
    motivation_after: int = 0  # 1–5
    completion_status: str = ""  # completed | partial | blocked | abandoned
    external_resources: tuple[str, ...] = ()
    workaround_reasons: tuple[str, ...] = ()
    learning_friction_notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class ValidationIssue:
    """One classified validation finding."""

    issue_id: str
    title: str
    finding_class: str
    priority: str
    status: str
    surface: str
    summary: str
    evidence: str
    recommendation: str


@dataclass(frozen=True)
class LearningFrictionRecord:
    """Before / after learning-friction record for a resolved issue."""

    issue_id: str
    title: str
    before: str
    after: str
    student_benefit: str
    evidence: str


@dataclass(frozen=True)
class EducationalImprovement:
    """One educational improvement from the four-question review."""

    improvement_id: str
    question: str  # which of the four questions
    gap: str
    recommendation: str
    priority: str
    status: str


@dataclass(frozen=True)
class ProductAreaRating:
    """Product review score for one UX area."""

    area: str
    score: int  # 1–5
    summary: str


@dataclass(frozen=True)
class SurfaceAuditEntry:
    """Mandatory surface audit row."""

    surface: str
    verdict: str
    summary: str
    evidence: str


@dataclass(frozen=True)
class DogfoodPackageReadiness:
    """Whether exclusive dogfood study can begin for a subject."""

    subject_code: str
    ready: bool
    reason: str
    enrolment_enabled: bool
    package_active: bool
    routing_reason: str


# ---------------------------------------------------------------------------
# Dogfood progress (validation log)
# ---------------------------------------------------------------------------

DOGFOOD_PROGRESS: tuple[DogfoodProgressEntry, ...] = (
    DogfoodProgressEntry(
        study_date="2026-07-31",
        subject="CS1",
        mission_completed=(
            "Pre-enrol audit: Home empty/quiet states + Journey surfaces "
            "(no exclusive sitting until published package active)"
        ),
        time_spent_minutes=45,
        points_of_confusion=(
            "Primary nav 'Journey' opens syllabus Journey, not My Learning Journey",
            "Home stacks Mission + Episode + Session Plan + Focus with overlap",
        ),
        missing_content=(
            "Rich Learning Episodes require founder-published CS1 package",
            "Curriculum 'why' enrichment absent without package graph",
        ),
        poor_wording=(
            "Sitting Report archives may show strategy_title (engine-adjacent)",
        ),
        navigation_friction=(
            "My Learning Journey only via Quick Actions / History bridge",
            "Session complete 'Open Journey' → syllabus Journey",
        ),
        unexpected_behaviour=(
            "Start Early / Start Tomorrow href returns to Home without advancing topic",
            "Authoring failure swallows episodes silently (bare except → None)",
        ),
        suggestions=(
            "Publish CS1 package before exclusive dogfood week",
            "Rename or dual-label nav Journey surfaces",
            "Surface authoring failure as quiet educational state",
        ),
        four_question_notes=(
            "Q1 What: clear when mission present; quiet otherwise",
            "Q2 Why: strong with graph; generic without package",
            "Q3 Succeeded: criteria on Home; live confirmation only after Session",
            "Q4 Next: Begin Session clear; Start Early misleading",
        ),
        evidence_kind="code_audit",
        confusion_score=4,
        confidence_score=2,
        motivation_score=3,
        workaround_count=3,
    ),
    DogfoodProgressEntry(
        study_date="2026-07-31",
        subject="CS1",
        mission_completed=(
            "Spine walkthrough: Adaptive Workspace → Begin Session path → "
            "Sitting Report → History (flags + package assumed)"
        ),
        time_spent_minutes=60,
        points_of_confusion=(
            "View Readiness Forecast Quick Action reuses Learning Journey URL",
            "Activity labels on Home are not an interactive checklist",
        ),
        missing_content=(
            "mission_narrative composed but not rendered on Home",
            "Full activity prompts authored but only titles shown on Home",
        ),
        poor_wording=(
            "Footer 'Diagnostics' for experience-switch users",
            "HTML data-session-control=complete_runtime_c leaks internal naming",
        ),
        navigation_friction=(
            "Home cognitive load: 10+ stacked sections",
        ),
        unexpected_behaviour=(
            "Mark-complete Runtime C path still present as pilot/rollback",
        ),
        suggestions=(
            "Collapse Mission/Episode/Plan into one primary arc",
            "Wire Forecast Quick Action to forecast anchor or dedicated surface",
            "Remove or relabel complete_runtime_c DOM attrs",
        ),
        four_question_notes=(
            "Daily workflow Home→Session→Sitting Report is coherent",
            "Success criteria are authored targets, not live session feedback",
        ),
        evidence_kind="code_audit",
        confusion_score=3,
        confidence_score=3,
        motivation_score=3,
        workaround_count=2,
    ),
    DogfoodProgressEntry(
        study_date="2026-07-31",
        subject="CS1",
        mission_completed=(
            "V1S-005 remediation verification: quiet episode fallback, "
            "Syllabus nav, honest Start Early, ProgressEngine isolation, "
            "mission narrative + session-stage clarity"
        ),
        time_spent_minutes=40,
        points_of_confusion=(
            "Exclusive live week still waits on founder-published CS1 package "
            "in each environment",
        ),
        missing_content=(),
        poor_wording=(),
        navigation_friction=(),
        unexpected_behaviour=(),
        suggestions=(
            "Publish CS1; enrol Runtime C; append live_sitting rows daily",
        ),
        four_question_notes=(
            "Q1: quiet reason answers when authoring fails",
            "Q2: curriculum why kept when Episode present",
            "Q3: Session stages labelled explicitly on Home",
            "Q4: Begin Session primary; Start Early demoted to preview copy",
        ),
        evidence_kind="code_audit",
        confusion_score=1,
        confidence_score=4,
        motivation_score=4,
        workaround_count=1,
        completion_status="completed",
    ),
    DogfoodProgressEntry(
        study_date="2026-07-31",
        subject="CS1",
        mission_completed=(
            "V1S-006 Day 1 live sitting: Adaptive Workspace Home for CS1 "
            "1.1 (purpose/function of data analysis) → Start Today's Session "
            "→ Session activity opened then blocked (Runtime A fallback)"
        ),
        time_spent_minutes=55,
        points_of_confusion=(
            "Success criteria show 'Elain' / 'elain' instead of Explain",
            "Tomorrow Preview shows 'eloratory' instead of exploratory",
            "Topic title renders as 'Study 1 — .1 …' (missing chapter digit)",
            "Home estimates 125 min / 2h 5m while Session timer shows ~24 min",
            "Session activity labels topic as 'Core methods' vs Home 1.1 title",
        ),
        missing_content=(
            "No Student Curriculum Instance (SCI) for Runtime C CS1 enrolment "
            "(sci_student_curriculum_instances count=0) — Session cannot bind",
            "Authored episode substance does not reliably carry into Session "
            "activity prompts once Runtime A fallback engages",
        ),
        poor_wording=(
            "Authoring scrub strips substring 'xp' from all copy "
            "(Explain→Elain, exploratory→eloratory, experience→eerience)",
            "Circular success criterion: explain role of topic within itself",
        ),
        navigation_friction=(
            "My Learning Journey (/student/learning-journey) TypeError: "
            "shell_vm() called with positional ExperienceSurface",
        ),
        unexpected_behaviour=(
            "POST /student/session/start succeeds then GET activity redirects "
            "to overview with ri001_runtime_a_fallback no_active_sci",
            "Activity answer path unavailable once stuck on overview",
            "Commercial Loop not set in local .env (enabled only for this "
            "observation process via SR_COMMERCIAL_LOOP=1)",
        ),
        suggestions=(
            "Remediate authoring scrub token 'xp' (word-boundary / whole-token)",
            "Ensure Runtime C enrolment creates/binds SCI before Session",
            "Fix learning_journey shell_vm keyword call",
            "Do not continue exclusive week until Session completes without "
            "Runtime A fallback",
        ),
        four_question_notes=(
            "Did today's mission make sense? PARTIAL — Home arc clear; "
            "Session substance drifted to 'Core methods'",
            "Did today's explanation help? NO — xp scrub mangles Explain / "
            "exploratory; criteria circular",
            "Was anything missing? YES — SCI binding; durable Session "
            "activity path; Learning Journey page",
            "Did I know what to do next? YES on Home (Start Today's Session); "
            "NO after Session fallback to overview",
            "Would I willingly return tomorrow? NO until Session completes "
            "without Runtime A fallback and copy is readable",
        ),
        evidence_kind="live_sitting",
        confusion_score=4,
        confidence_score=2,
        motivation_score=2,
        workaround_count=2,
        confidence_before=4,
        confidence_after=2,
        motivation_before=4,
        motivation_after=2,
        completion_status="blocked",
        external_resources=(),
        workaround_reasons=(
            "Observation used process-local SR_COMMERCIAL_LOOP=1 because "
            ".env lacked Commercial Loop (documented)",
            "Session could not be finished — stopped at overview after "
            "no_active_sci Runtime A fallback (no silent workaround)",
        ),
        learning_friction_notes=(
            "DF-013 xp scrub destroys educational verbs",
            "DF-014 Session Runtime A fallback without SCI",
            "DF-015 My Learning Journey shell_vm TypeError",
            "DF-016 Topic title digit drop / duration mismatch",
        ),
    ),
    DogfoodProgressEntry(
        study_date="2026-07-31",
        subject="CS1",
        mission_completed=(
            "V1S-008 educational integrity validation: DF-013/DF-016 remediated; "
            "composed Home arc (Morning Brief → Mission → Episode → Tomorrow) "
            "with Explain/exploratory preserved; title Study 1.1 continuity; "
            "Session overview inherits mission topic (no Core methods); "
            "circular success criteria removed"
        ),
        time_spent_minutes=40,
        points_of_confusion=(),
        missing_content=(),
        poor_wording=(),
        navigation_friction=(),
        unexpected_behaviour=(),
        suggestions=(
            "Resume exclusive live week (5–7 consecutive days) after integrity PASS",
        ),
        four_question_notes=(
            "Did today's mission make sense? YES — Study 1.1 title + Explain prose",
            "Did today's explanation help? YES — educational verbs intact",
            "Was anything missing? NO for integrity scope — consecutive "
            "week still open",
            "Did I know what to do next? YES — Begin Session / Tomorrow Preview",
            "Would I willingly return tomorrow? YES for educational quality; "
            "exclusive-week bar still requires live consecutive sittings",
        ),
        evidence_kind="validation_sitting",
        confusion_score=1,
        confidence_score=4,
        motivation_score=4,
        workaround_count=0,
        confidence_before=4,
        confidence_after=4,
        motivation_before=4,
        motivation_after=4,
        completion_status="completed",
        external_resources=(),
        workaround_reasons=(),
        learning_friction_notes=(
            "DF-013 RESOLVED",
            "DF-016 RESOLVED",
            "DF-014/DF-015 previously RESOLVED (V1S-007)",
        ),
    ),
)


# ---------------------------------------------------------------------------
# Issue register (V1S-005 classification)
# ---------------------------------------------------------------------------

VALIDATION_ISSUES: tuple[ValidationIssue, ...] = (
    ValidationIssue(
        issue_id="DF-001",
        title="Published packages required before exclusive CS1 dogfood",
        finding_class=CLASS_LEARNING_FRICTION,
        priority=PRIORITY_P0,
        status=STATUS_RESOLVED,
        surface="Curriculum Authority / Founder",
        summary=(
            "Package readiness gate verifies enrolment flag + active "
            "published package + published_curriculum routing so exclusive "
            "CS1 study can begin when the founder publishes."
        ),
        evidence=(
            "assess_dogfood_package_readiness; .env.example dogfood checklist; "
            "Founder /founder/v1-readiness Learning Friction panel"
        ),
        recommendation=(
            "Founder-publish active CS1; confirm gate ready=true / "
            "reason=dogfood_curriculum_cutover before the exclusive week."
        ),
    ),
    ValidationIssue(
        issue_id="DF-002",
        title="Progress singularity residuals risk dual educational truths",
        finding_class=CLASS_BUG,
        priority=PRIORITY_P0,
        status=STATUS_RESOLVED,
        surface="Progress Engine / Runtime A substrate",
        summary=(
            "Runtime C enrolment now wins Home/Journey composition; Study "
            "Signals prefer ProgressEngine coverage; Runtime A readiness "
            "card hidden when educational.active."
        ),
        evidence=(
            "views._try_runtime_c_page; student_home_service._study_signals; "
            "home.html readiness gate"
        ),
        recommendation=(
            "Keep SR_PROGRESS_SINGULARITY / Commercial Loop ON for dogfood; "
            "full Runtime A hard removal remains RI-002 (technical debt)."
        ),
    ),
    ValidationIssue(
        issue_id="DF-003",
        title="Silent Learning Episode failure on Home",
        finding_class=CLASS_BUG,
        priority=PRIORITY_P0,
        status=STATUS_RESOLVED,
        surface="Adaptive Workspace",
        summary=(
            "Authoring failures log and return composition_quiet_reason; "
            "Home renders a calm Learning Episode quiet state."
        ),
        evidence=(
            "adaptive_workspace._mission_composition / "
            "_quiet_mission_composition; home.html episode quiet section"
        ),
        recommendation="Retain quiet pattern for any future authoring gaps.",
    ),
    ValidationIssue(
        issue_id="DF-004",
        title="Journey vs My Learning Journey navigation confusion",
        finding_class=CLASS_LEARNING_FRICTION,
        priority=PRIORITY_P1,
        status=STATUS_RESOLVED,
        surface="Student Journey",
        summary=(
            "Primary nav label is Syllabus; Sitting Report links My Learning "
            "Journey and Syllabus map separately."
        ),
        evidence=(
            "experience_workspace.SURFACE_LABELS; session_body.html; "
            "educational_view_models titles"
        ),
        recommendation="Keep Syllabus ≠ My Learning Journey naming stable.",
    ),
    ValidationIssue(
        issue_id="DF-005",
        title="Home information density / duplicated objective arc",
        finding_class=CLASS_UX_IMPROVEMENT,
        priority=PRIORITY_P1,
        status=STATUS_RESOLVED,
        surface="Adaptive Workspace / Home",
        summary=(
            "When a Learning Episode is present, Session Plan is hidden and "
            "Current Focus collapses to curriculum-why only."
        ),
        evidence="home.html DF-005 section gates",
        recommendation="Revisit further collapse only after live-week feedback.",
    ),
    ValidationIssue(
        issue_id="DF-006",
        title="Start Early / Start Tomorrow CTAs do not advance topic",
        finding_class=CLASS_LEARNING_FRICTION,
        priority=PRIORITY_P1,
        status=STATUS_RESOLVED,
        surface="Tomorrow Preview / Extra Study",
        summary=(
            "Start Early removed from Quick Actions; start_early/start_tomorrow "
            "hrefs empty; Tomorrow Preview shows preview-only honesty copy."
        ),
        evidence="adaptive_workspace._extra_study_href / _quick_actions; home.html",
        recommendation="Wire a real start-early path only in a later programme.",
    ),
    ValidationIssue(
        issue_id="DF-007",
        title="strategy_title leak on My Learning Journey archives",
        finding_class=CLASS_LEARNING_FRICTION,
        priority=PRIORITY_P1,
        status=STATUS_RESOLVED,
        surface="My Learning Journey",
        summary=(
            "Archives project sitting_summary (date/topic) instead of "
            "strategy_title."
        ),
        evidence="view_models.learning_journey_vm; learning_journey.html",
        recommendation="Keep Sitting Report strategy body on complete surface only.",
    ),
    ValidationIssue(
        issue_id="DF-008",
        title="mission_narrative authored but not shown on Home",
        finding_class=CLASS_UX_IMPROVEMENT,
        priority=PRIORITY_P1,
        status=STATUS_RESOLVED,
        surface="Educational Authoring / Home",
        summary="Home renders mission_narrative once above Learning Episodes.",
        evidence="home.html data-kwp=015-mission-narrative",
        recommendation="Keep single binding to avoid dual-truth unused fields.",
    ),
    ValidationIssue(
        issue_id="DF-009",
        title="Episode activities display-only on Home",
        finding_class=CLASS_LEARNING_FRICTION,
        priority=PRIORITY_P1,
        status=STATUS_RESOLVED,
        surface="Learning Episodes",
        summary=(
            "Activity titles labelled Session stages with explicit "
            "'become your Session stages' honesty line."
        ),
        evidence="home.html Session stages block",
        recommendation="Optional prompt previews remain deferred (no new EI).",
    ),
    ValidationIssue(
        issue_id="DF-010",
        title="Readiness Forecast Quick Action duplicates Learning Journey URL",
        finding_class=CLASS_UX_IMPROVEMENT,
        priority=PRIORITY_P2,
        status=STATUS_RESOLVED,
        surface="Adaptive Workspace Quick Actions",
        summary=(
            "Forecast Quick Action deep-links Home #ws-forecast-title when "
            "forecast is present."
        ),
        evidence="adaptive_workspace._quick_actions View Readiness Forecast",
        recommendation="Dedicated Forecast surface remains optional polish.",
    ),
    ValidationIssue(
        issue_id="DF-011",
        title="Footer Diagnostics link (engine noun)",
        finding_class=CLASS_LEARNING_FRICTION,
        priority=PRIORITY_P2,
        status=STATUS_RESOLVED,
        surface="Student chrome",
        summary="Footer link relabelled Curriculum Health.",
        evidence="eos_student.html Curriculum Health",
        recommendation="Keep founder-only chrome free of engine nouns.",
    ),
    ValidationIssue(
        issue_id="DF-012",
        title="No loading skeleton on compose-heavy Home",
        finding_class=CLASS_DEFERRED,
        priority=PRIORITY_P2,
        status=STATUS_DEFERRED,
        surface="Product / Home",
        summary=(
            "Design-system skeleton tokens exist but student Home does not "
            "use them — polish only; not blocking exclusive study week."
        ),
        evidence="tokens.css skeletons; home.html page-enter only",
        recommendation="Optional skeleton after live-week latency observation.",
    ),
    ValidationIssue(
        issue_id="DF-013",
        title="Authoring scrub strips 'xp' from educational prose",
        finding_class=CLASS_BUG,
        priority=PRIORITY_P0,
        status=STATUS_RESOLVED,
        surface="Educational Authoring / guidance.scrub",
        summary=(
            "Forbidden-token scrub treated 'xp' as a substring match, destroying "
            "Explain→Elain, exploratory→eloratory, experience→eerience on "
            "Live Home Episode, success criteria, Tomorrow Preview, and "
            "checkpoint/reflection prompts."
        ),
        evidence=(
            "V1S-008: guidance.scrub uses whole-token matching for xp / "
            "gamification tokens; Explain / exploratory / experience preserved. "
            "tests/test_v1s008_educational_integrity.py"
        ),
        recommendation="Resolved — retain word-boundary scrub in authoring.",
    ),
    ValidationIssue(
        issue_id="DF-014",
        title="Runtime C enrolment without SCI blocks Session",
        finding_class=CLASS_BUG,
        priority=PRIORITY_P0,
        status=STATUS_RESOLVED,
        surface="Learning Session / Runtime Integration",
        summary=(
            "Founder has active Runtime C CS1 enrolment and published package, "
            "but sci_student_curriculum_instances is empty. Session start "
            "briefly opens activity then redirects to overview with "
            "ri001_runtime_a_fallback reason=no_active_sci — dual-runtime "
            "path during exclusive dogfood."
        ),
        evidence=(
            "V1S-007: ensure_active_sci provisions CKG bridge from published "
            "package and creates SCI on enrolment / first Home / Session "
            "launch; Runtime C students never fall through to Runtime A "
            "(EducationalPrerequisiteMissing instead)."
        ),
        recommendation=(
            "Resolved by V1S-007 Educational Runtime Singularity (A9)."
        ),
    ),
    ValidationIssue(
        issue_id="DF-015",
        title="My Learning Journey crashes (shell_vm call)",
        finding_class=CLASS_BUG,
        priority=PRIORITY_P1,
        status=STATUS_RESOLVED,
        surface="My Learning Journey",
        summary=(
            "GET /student/learning-journey raises TypeError: shell_vm() takes "
            "0 positional arguments but 1 was given — route passes "
            "ExperienceSurface.HISTORY positionally."
        ),
        evidence=(
            "V1S-007: learning_journey route calls "
            "shell_vm(active_surface=..., page_title=...)."
        ),
        recommendation="Resolved with Educational Runtime Singularity journey fix.",
    ),
    ValidationIssue(
        issue_id="DF-016",
        title="Topic title / duration / Session label mismatch",
        finding_class=CLASS_LEARNING_FRICTION,
        priority=PRIORITY_P1,
        status=STATUS_RESOLVED,
        surface="Home ↔ Session continuity",
        summary=(
            "Home showed mangled title 'Study 1 — .1 …', estimates that could "
            "diverge from Session, and Runtime A fallback labelled Session as "
            "'Core methods' — student lost trust that Session continues today's "
            "mission."
        ),
        evidence=(
            "V1S-008: student_mission_title / student_syllabus_code prefer "
            "fuller syllabus numbers; Session Plan prefers Mission duration; "
            "legacy Core methods fallback → Today's topic; SCI path (V1S-007) "
            "carries mission title into Session overview."
        ),
        recommendation="Resolved — verify continuity in exclusive-week sittings.",
    ),
    ValidationIssue(
        issue_id="DF-W01",
        title="Deterministic Educational Authoring with CMP rejection",
        finding_class=CLASS_WORKS_WELL,
        priority=PRIORITY_P2,
        status=STATUS_RESOLVED,
        surface="Educational Authoring",
        summary=(
            "Episodes compose with learning objective, context, success "
            "criteria, scrubbed guidance; looks_like_cmp_dump enforced. "
            "V1S-008: DF-013 scrub fix restores educational verbs; circular "
            "success criteria (topic within itself) removed."
        ),
        evidence="educational_authoring/; tests/test_v1s008_educational_integrity.py",
        recommendation="Retain; Episode quality PASS after V1S-008.",
    ),
    ValidationIssue(
        issue_id="DF-W02",
        title="Adaptive Workspace consumes engines without reimplementation",
        finding_class=CLASS_WORKS_WELL,
        priority=PRIORITY_P2,
        status=STATUS_RESOLVED,
        surface="Adaptive Workspace",
        summary="Composer orchestrates Strategy…Authoring; E9 holds.",
        evidence="adaptive_workspace.compose_adaptive_workspace; E9",
        recommendation="Keep presentation-only (A7).",
    ),
    ValidationIssue(
        issue_id="DF-W03",
        title="Single mission spine on dogfood path",
        finding_class=CLASS_WORKS_WELL,
        priority=PRIORITY_P2,
        status=STATUS_RESOLVED,
        surface="Mission Runtime",
        summary=(
            "ERE + CertifiedMissionEngine + StudentRuntimeCoordinator + "
            "LearningSessionRuntime documented and code-backed. "
            "V1S-007: SCI ensure + A9 singularity close DF-014 Runtime A fallback."
        ),
        evidence=(
            "runtime_ownership.MISSION_SPINE; "
            "educational_runtime_engine.sci_lifecycle"
        ),
        recommendation="Retain A9; exclusive week may resume after V1S-008.",
    ),
    ValidationIssue(
        issue_id="DF-W04",
        title="Empty / quiet / day-complete educational states",
        finding_class=CLASS_WORKS_WELL,
        priority=PRIORITY_P2,
        status=STATUS_RESOLVED,
        surface="Student Home",
        summary=(
            "Calm operational copy; authoring-failure quiet state added "
            "in V1S-005."
        ),
        evidence="student_home_service quiet/day_complete; home.html DF-003",
        recommendation="Keep quiet vocabulary consistent across surfaces.",
    ),
    ValidationIssue(
        issue_id="DF-TD01",
        title="Runtime A hard removal (RI-002) still pending",
        finding_class=CLASS_TECHNICAL_DEBT,
        priority=PRIORITY_P2,
        status=STATUS_DEFERRED,
        surface="Runtime A substrate",
        summary=(
            "Dogfood isolates ProgressEngine for Runtime C enrolments; "
            "substrate removal remains a separate engineering programme. "
            "V1S-007 A9 removed Runtime C → Runtime A fallback; RI-002 still "
            "needed for hard deletion of legacy packages."
        ),
        evidence="V1_RELEASE_CRITERIA A9; RI-002; runtime_ownership TECHNICAL_DEBT",
        recommendation="Keep RI-002 deferred; A9 fallback already REMOVED.",
    ),
)


LEARNING_FRICTION_REGISTER: tuple[LearningFrictionRecord, ...] = (
    LearningFrictionRecord(
        issue_id="DF-001",
        title="Published package readiness",
        before="Exclusive CS1 week blocked with no checkable ready gate.",
        after=(
            "Founder board shows package readiness (enrolment + active "
            "package + routing reason)."
        ),
        student_benefit=(
            "Founder knows when study can begin without guessing flags."
        ),
        evidence="assess_dogfood_package_readiness; v1_readiness Learning Friction",
    ),
    LearningFrictionRecord(
        issue_id="DF-002",
        title="Progress isolation",
        before=(
            "Runtime A mastery theatre could override Runtime C coverage on "
            "Home signals / readiness."
        ),
        after=(
            "Runtime C enrolment wins page composition; Study Signals use "
            "ProgressEngine coverage; readiness card hidden when edu active."
        ),
        student_benefit="One progress truth — educational trust holds.",
        evidence="views._try_runtime_c_page; _study_signals; home.html",
    ),
    LearningFrictionRecord(
        issue_id="DF-003",
        title="Silent Learning Episode failure",
        before="Authoring exceptions returned None; Episode block vanished.",
        after="Logged failure + calm quiet reason on Home Learning Episode.",
        student_benefit="Student still knows what today is asking of them.",
        evidence="composition_quiet_reason; home.html quiet section",
    ),
    LearningFrictionRecord(
        issue_id="DF-004",
        title="Journey navigation",
        before="Nav 'Journey' ≠ My Learning Journey; Sitting Report CTA wrong.",
        after="Nav 'Syllabus'; Sitting Report links both destinations.",
        student_benefit="Clear where syllabus position vs learning story live.",
        evidence="SURFACE_LABELS; session_body.html",
    ),
    LearningFrictionRecord(
        issue_id="DF-005",
        title="Home information hierarchy",
        before="Mission + Episode + Plan + Focus repeated the objective.",
        after="Episode collapses Plan; Focus demotes to curriculum why.",
        student_benefit="One educational arc for the day — less dashboard feel.",
        evidence="home.html DF-005 gates",
    ),
    LearningFrictionRecord(
        issue_id="DF-006",
        title="Start Early / Extra Study honesty",
        before="Start Early linked Home without advancing tomorrow's topic.",
        after="Preview-only copy; no fake CTA; Extra Study links only when real.",
        student_benefit="Next-step trust: only Begin Session advances the day.",
        evidence="_extra_study_href; _quick_actions; tomorrow preview copy",
    ),
    LearningFrictionRecord(
        issue_id="DF-007",
        title="strategy_title on Learning Journey",
        before="Archive rows showed engine-adjacent strategy_title.",
        after="Student-safe sitting_summary (date) only.",
        student_benefit="Product language stays educational, not engine-speak.",
        evidence="learning_journey_vm; learning_journey.html",
    ),
    LearningFrictionRecord(
        issue_id="DF-008",
        title="Mission narrative visibility",
        before="mission_narrative authored and projected but never rendered.",
        after="Rendered once above Learning Episodes.",
        student_benefit="Authored educational prose reaches the student.",
        evidence="home.html mission-narrative",
    ),
    LearningFrictionRecord(
        issue_id="DF-009",
        title="Session activity clarity",
        before="Activity titles looked like an unfinished checklist.",
        after="Labelled Session stages with explicit Session continuity line.",
        student_benefit="Student knows Home previews Session, not a dead list.",
        evidence="home.html Session stages",
    ),
    LearningFrictionRecord(
        issue_id="DF-013",
        title="Authoring xp scrub",
        before=(
            "Substring scrub of 'xp' destroyed Explain / exploratory / "
            "experience on Episode, criteria, Tomorrow Preview."
        ),
        after=(
            "Whole-token scrub preserves educational verbs; gamification "
            "tokens still removed."
        ),
        student_benefit="Authored tutor prose reads as written — trust restored.",
        evidence="guidance.scrub; tests/test_v1s008_educational_integrity.py",
    ),
    LearningFrictionRecord(
        issue_id="DF-016",
        title="Home ↔ Session educational continuity",
        before=(
            "Study 1 — .1 title digit drop; duration mismatch; Core methods "
            "Session label under Runtime A fallback."
        ),
        after=(
            "Syllabus codes prefer fuller title numbers; Mission duration "
            "anchors Session Plan; Session overview carries mission topic; "
            "no invented Core methods label."
        ),
        student_benefit=(
            "Home, Episode, Session, and Sitting Report describe one activity."
        ),
        evidence=(
            "student_facing_identity; adaptive_workspace._session_plan; "
            "student_runtime coordinator overview"
        ),
    ),
)


EDUCATIONAL_IMPROVEMENTS: tuple[EducationalImprovement, ...] = (
    EducationalImprovement(
        improvement_id="EI-001",
        question="What am I learning today?",
        gap=(
            "When published package or authoring fails, Home may omit the "
            "Learning Episode without explaining what is missing."
        ),
        recommendation=(
            "Always answer Q1 with topic + objective or an explicit quiet reason."
        ),
        priority=PRIORITY_P0,
        status=STATUS_RESOLVED,
    ),
    EducationalImprovement(
        improvement_id="EI-002",
        question="Why am I learning it?",
        gap=(
            "Curriculum why and foundation/successor context require package "
            "graph; without it the 'why' becomes generic."
        ),
        recommendation=(
            "Gate exclusive dogfood on published packages; show syllabus "
            "position fallback when graph unavailable."
        ),
        priority=PRIORITY_P0,
        status=STATUS_RESOLVED,
    ),
    EducationalImprovement(
        improvement_id="EI-003",
        question="How do I know I succeeded?",
        gap=(
            "Home success criteria are pre-session targets; students must "
            "complete a Session to see Sitting Report confirmation. Activity "
            "labels alone do not close the loop."
        ),
        recommendation=(
            "Clarify pre- vs post-session success; label Session stages on Home."
        ),
        priority=PRIORITY_P1,
        status=STATUS_RESOLVED,
    ),
    EducationalImprovement(
        improvement_id="EI-004",
        question="What should I do next?",
        gap=(
            "Primary Begin Session is clear; Start Early / Extra Study CTAs "
            "and dual Journey destinations create false next-steps."
        ),
        recommendation=(
            "One primary next action; demote or wire secondary CTAs honestly."
        ),
        priority=PRIORITY_P1,
        status=STATUS_RESOLVED,
    ),
    EducationalImprovement(
        improvement_id="EI-005",
        question="What am I learning today?",
        gap=(
            "mission_narrative and full activity prompts are authored but "
            "under-exposed — educational substance exists off-screen."
        ),
        recommendation="Surface narrative once; preview Session stages.",
        priority=PRIORITY_P1,
        status=STATUS_RESOLVED,
    ),
)


PRODUCT_RATINGS: tuple[ProductAreaRating, ...] = (
    ProductAreaRating(
        area="Loading states",
        score=2,
        summary="Skeleton tokens unused on Home; page-enter only (DF-012 deferred).",
    ),
    ProductAreaRating(
        area="Empty states",
        score=5,
        summary="Quiet educational copy now covers authoring failure too.",
    ),
    ProductAreaRating(
        area="Navigation",
        score=4,
        summary=(
            "Syllabus vs My Learning Journey distinguished; "
            "Forecast deep-link fixed."
        ),
    ),
    ProductAreaRating(
        area="Typography",
        score=4,
        summary="Design-system page headers and section hierarchy hold.",
    ),
    ProductAreaRating(
        area="Spacing",
        score=4,
        summary="Home arc collapsed when Episode present — lighter stack.",
    ),
    ProductAreaRating(
        area="Motion",
        score=3,
        summary="Subtle enter/success motion; Focus mode in Session; no noise.",
    ),
    ProductAreaRating(
        area="Terminology",
        score=4,
        summary="Syllabus / Curriculum Health; strategy_title scrubbed from archives.",
    ),
    ProductAreaRating(
        area="Daily workflow",
        score=4,
        summary="Home→Session→Sitting Report coherent; secondary CTAs honest.",
    ),
)


SURFACE_AUDIT: tuple[SurfaceAuditEntry, ...] = (
    SurfaceAuditEntry(
        surface="Learning Episodes",
        verdict=CLASS_WORKS_WELL,
        summary=(
            "Quiet failure state + Session stage honesty + narrative binding "
            "close V1S-004 gaps without new authoring algorithms."
        ),
        evidence="educational_authoring/; home.html Learning Episode block",
    ),
    SurfaceAuditEntry(
        surface="Adaptive Workspace",
        verdict=CLASS_WORKS_WELL,
        summary=(
            "Composition spine retained; density and CTA honesty remediated "
            "in V1S-005."
        ),
        evidence="adaptive_workspace.py; home.html",
    ),
    SurfaceAuditEntry(
        surface="Mission Runtime",
        verdict=CLASS_WORKS_WELL,
        summary=(
            "Single spine unchanged. Progress isolation for Runtime C "
            "enrolments closed for dogfood."
        ),
        evidence="runtime_ownership.py; views._try_runtime_c_page",
    ),
    SurfaceAuditEntry(
        surface="Educational Authoring",
        verdict=CLASS_WORKS_WELL,
        summary="Composition-only (A8); narrative now rendered once on Home.",
        evidence="educational_authoring/; home.html mission-narrative",
    ),
    SurfaceAuditEntry(
        surface="Student Journey",
        verdict=CLASS_WORKS_WELL,
        summary="Syllabus nav + dual Sitting Report links resolve naming confusion.",
        evidence="journey.html; learning_journey.html; SURFACE_LABELS",
    ),
    SurfaceAuditEntry(
        surface="Founder Readiness",
        verdict=CLASS_WORKS_WELL,
        summary=(
            "Learning Friction / Resolved / Open / Confidence / Motivation / "
            "Completion / Consistency / Friction Trend panels for V1S-006."
        ),
        evidence="v1_readiness_dashboard.py; /founder/v1-readiness",
    ),
)


DOGFOOD_PROGRESS_SUMMARY = (
    "V1S-008 educational integrity validation PASS for DF-013 / DF-016. "
    "V1S-007 previously closed DF-014 (SCI / A9) and DF-015 (Learning Journey). "
    "Open P0 educational defects: none. Exclusive 5–7 consecutive live-day bar "
    "remains incomplete (1 blocked + 1 validation sitting). Private beta stays "
    "NO-GO until consecutive live week completes without undocumented workarounds."
)


def issues_by_status(status: str) -> tuple[ValidationIssue, ...]:
    return tuple(i for i in VALIDATION_ISSUES if i.status == status)


def open_issues() -> tuple[ValidationIssue, ...]:
    return issues_by_status(STATUS_OPEN)


def resolved_issues() -> tuple[ValidationIssue, ...]:
    return issues_by_status(STATUS_RESOLVED)


def deferred_issues() -> tuple[ValidationIssue, ...]:
    return issues_by_status(STATUS_DEFERRED)


def outstanding_issues() -> tuple[ValidationIssue, ...]:
    """Open issues plus deferred — anything still blocking a clean week."""
    return tuple(
        i
        for i in VALIDATION_ISSUES
        if i.status in {STATUS_OPEN, STATUS_DEFERRED}
        and i.finding_class != CLASS_WORKS_WELL
    )


def open_friction_issues() -> tuple[ValidationIssue, ...]:
    return tuple(
        i
        for i in outstanding_issues()
        if i.finding_class
        in {CLASS_LEARNING_FRICTION, CLASS_BUG, CLASS_UX_IMPROVEMENT}
    )


def resolved_friction_records() -> tuple[LearningFrictionRecord, ...]:
    return LEARNING_FRICTION_REGISTER


def open_educational_improvements() -> tuple[EducationalImprovement, ...]:
    return tuple(
        e for e in EDUCATIONAL_IMPROVEMENTS if e.status == STATUS_OPEN
    )


def validation_issue_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for issue in VALIDATION_ISSUES:
        counts[issue.finding_class] = counts.get(issue.finding_class, 0) + 1
    return counts


def dogfood_confidence_trend() -> tuple[str, ...]:
    """Confidence trend lines from recorded sittings (low → high over time)."""
    lines: list[str] = []
    for entry in DOGFOOD_PROGRESS:
        before = entry.confidence_before or entry.confidence_score
        after = entry.confidence_after or entry.confidence_score
        if entry.confidence_before and entry.confidence_after:
            conf = f"confidence {before}→{after}/5"
        else:
            conf = f"confidence {after}/5"
        lines.append(
            f"{entry.study_date} · {entry.evidence_kind}: "
            f"{conf}, "
            f"confusion {entry.confusion_score}/5, "
            f"motivation "
            f"{(entry.motivation_after or entry.motivation_score)}/5, "
            f"workarounds {entry.workaround_count}"
            + (
                f", completion={entry.completion_status}"
                if entry.completion_status
                else ""
            )
        )
    return tuple(lines)


def dogfood_motivation_trend() -> tuple[str, ...]:
    """Motivation before→after lines for Founder board."""
    lines: list[str] = []
    for entry in DOGFOOD_PROGRESS:
        before = entry.motivation_before or entry.motivation_score
        after = entry.motivation_after or entry.motivation_score
        if entry.motivation_before and entry.motivation_after:
            mot = f"{before}→{after}/5"
        else:
            mot = f"{after}/5"
        lines.append(
            f"{entry.study_date} · {entry.evidence_kind}: motivation {mot}"
        )
    return tuple(lines)


def dogfood_completion_trend() -> tuple[str, ...]:
    """Mission completion status per sitting."""
    return tuple(
        f"{e.study_date} · {e.evidence_kind}: "
        f"{e.completion_status or 'unspecified'} · "
        f"{e.time_spent_minutes} min · {e.mission_completed[:72]}"
        for e in DOGFOOD_PROGRESS
    )


def dogfood_study_consistency() -> tuple[str, ...]:
    """Calendar consistency of live sittings (exclusive-week bar)."""
    live_dates = sorted(
        {
            e.study_date
            for e in DOGFOOD_PROGRESS
            if e.evidence_kind == "live_sitting"
        }
    )
    if not live_dates:
        return (
            "No live_sitting days yet — exclusive week not started.",
        )
    lines = [
        f"Live study days recorded: {len(live_dates)} "
        f"({', '.join(live_dates)})",
        (
            "Exclusive-week bar: 5–7 consecutive days — "
            f"{'MET' if len(live_dates) >= 5 else 'NOT MET'} "
            f"({len(live_dates)}/5 minimum)."
        ),
    ]
    blocked = sum(
        1
        for e in DOGFOOD_PROGRESS
        if e.evidence_kind == "live_sitting"
        and e.completion_status == "blocked"
    )
    if blocked:
        lines.append(
            f"Blocked live sittings: {blocked} — consecutive week cannot "
            "advance until Session completes without Runtime A fallback."
        )
    return tuple(lines)


def dogfood_friction_trend() -> tuple[str, ...]:
    """Open vs resolved friction snapshot for Founder board."""
    open_items = open_friction_issues()
    resolved = resolved_friction_records()
    open_p0 = sum(1 for i in open_items if i.priority == PRIORITY_P0)
    return (
        f"Resolved friction records: {len(resolved)}",
        f"Open friction/bug/UX: {len(open_items)} (P0 open: {open_p0})",
        *(
            f"OPEN {i.issue_id} [{i.priority}] {i.title}"
            for i in open_items[:8]
        ),
    )


def dogfood_metrics_summary() -> dict[str, float | int | str]:
    """Aggregate dogfood metrics for Founder board."""
    if not DOGFOOD_PROGRESS:
        return {
            "sittings": 0,
            "total_minutes": 0,
            "avg_confidence": 0.0,
            "avg_confusion": 0.0,
            "avg_motivation": 0.0,
            "total_workarounds": 0,
            "live_sittings": 0,
            "code_audit_sittings": 0,
            "live_days": 0,
            "blocked_live_sittings": 0,
        }
    n = len(DOGFOOD_PROGRESS)
    live = sum(1 for e in DOGFOOD_PROGRESS if e.evidence_kind == "live_sitting")
    audits = sum(1 for e in DOGFOOD_PROGRESS if e.evidence_kind == "code_audit")
    live_days = len(
        {e.study_date for e in DOGFOOD_PROGRESS if e.evidence_kind == "live_sitting"}
    )
    blocked = sum(
        1
        for e in DOGFOOD_PROGRESS
        if e.evidence_kind == "live_sitting"
        and e.completion_status == "blocked"
    )
    return {
        "sittings": n,
        "total_minutes": sum(e.time_spent_minutes for e in DOGFOOD_PROGRESS),
        "avg_confidence": round(
            sum(e.confidence_score for e in DOGFOOD_PROGRESS) / n, 2
        ),
        "avg_confusion": round(
            sum(e.confusion_score for e in DOGFOOD_PROGRESS) / n, 2
        ),
        "avg_motivation": round(
            sum(e.motivation_score for e in DOGFOOD_PROGRESS) / n, 2
        ),
        "total_workarounds": sum(e.workaround_count for e in DOGFOOD_PROGRESS),
        "live_sittings": live,
        "code_audit_sittings": audits,
        "live_days": live_days,
        "blocked_live_sittings": blocked,
    }


def assess_dogfood_package_readiness(
    subject_code: str = "CS1",
) -> DogfoodPackageReadiness:
    """Check whether exclusive dogfood study can begin for a subject.

    Safe without app context — returns not-ready with an explanatory reason.
    """
    code = (subject_code or "CS1").strip().upper() or "CS1"
    try:
        from app.application.curriculum_studio_foundation.authority import (
            PublishedCurriculumAuthority,
        )
        from app.application.platform_integration.flags import (
            resolve_founder_student_bridge_flags,
        )
        from app.application.platform_integration.routing import (
            RuntimeAuthority,
            RuntimeRoutingService,
        )

        flags = resolve_founder_student_bridge_flags()
        enrolment = bool(flags.ENABLE_RUNTIME_C_ENROLMENT)
        if not enrolment:
            return DogfoodPackageReadiness(
                subject_code=code,
                ready=False,
                reason="runtime_c_enrolment_disabled",
                enrolment_enabled=False,
                package_active=False,
                routing_reason="runtime_c_enrolment_disabled",
            )
        package = PublishedCurriculumAuthority().get_active(code)
        package_active = package is not None
        decision = RuntimeRoutingService(flags=flags).resolve(
            subject_code=code,
            category_code="IFoA",
        )
        ready = (
            package_active
            and decision.runtime_authority == RuntimeAuthority.PUBLISHED_CURRICULUM
        )
        return DogfoodPackageReadiness(
            subject_code=code,
            ready=ready,
            reason=decision.reason if ready else (
                decision.reason
                if package_active
                else "no_active_published_package"
            ),
            enrolment_enabled=True,
            package_active=package_active,
            routing_reason=decision.reason,
        )
    except Exception as exc:  # noqa: BLE001
        return DogfoodPackageReadiness(
            subject_code=code,
            ready=False,
            reason=f"readiness_check_unavailable:{type(exc).__name__}",
            enrolment_enabled=False,
            package_active=False,
            routing_reason="",
        )


def assert_dogfood_registry_integrity() -> None:
    """Raise AssertionError if the dogfood registry is inconsistent."""
    seen_ids: set[str] = set()
    for issue in VALIDATION_ISSUES:
        if issue.finding_class not in FINDING_CLASSES:
            raise AssertionError(
                f"{issue.issue_id}: unknown class {issue.finding_class}"
            )
        if issue.issue_id in seen_ids:
            raise AssertionError(f"Duplicate issue id {issue.issue_id}")
        seen_ids.add(issue.issue_id)
    for entry in DOGFOOD_PROGRESS:
        if entry.time_spent_minutes < 0:
            raise AssertionError("Negative study time in dogfood progress")
        if not 0 <= entry.confusion_score <= 5:
            raise AssertionError("Bad confusion score")
        if entry.confidence_score and not 1 <= entry.confidence_score <= 5:
            raise AssertionError("Bad confidence score")
        for label, score in (
            ("confidence_before", entry.confidence_before),
            ("confidence_after", entry.confidence_after),
            ("motivation_before", entry.motivation_before),
            ("motivation_after", entry.motivation_after),
        ):
            if score and not 1 <= score <= 5:
                raise AssertionError(f"Bad {label}")
        if entry.completion_status and entry.completion_status not in {
            "completed",
            "partial",
            "blocked",
            "abandoned",
            "unspecified",
        }:
            raise AssertionError(
                f"Bad completion_status {entry.completion_status}"
            )
    for rating in PRODUCT_RATINGS:
        if not 1 <= rating.score <= 5:
            raise AssertionError(f"Bad product score for {rating.area}")
    surfaces = {e.surface for e in SURFACE_AUDIT}
    required = {
        "Learning Episodes",
        "Adaptive Workspace",
        "Mission Runtime",
        "Educational Authoring",
        "Student Journey",
        "Founder Readiness",
    }
    if not required.issubset(surfaces):
        raise AssertionError(f"Missing surface audits: {required - surfaces}")
    friction_ids = {r.issue_id for r in LEARNING_FRICTION_REGISTER}
    for issue_id in friction_ids:
        if issue_id not in seen_ids:
            raise AssertionError(f"Friction record without issue: {issue_id}")
