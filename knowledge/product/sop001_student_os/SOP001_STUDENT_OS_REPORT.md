# SOP-001 — Student Operating System Premium Experience Report

**Programme:** Product Experience  
**Status:** Complete (presentation pass)  
**Date:** 2026-07-29  
**Scope:** Redesign Student Home, Journey, History, and Revision as a cohesive mastery OS. No Founder Console changes. No learning-algorithm or business-logic changes.

---

## Summary

SOP-001 turns the Student Experience into a premium operating system for mastery: four surfaces, four questions, one clear purpose each. Home is a command centre that answers “what should I do now?” within five seconds. Journey is a visual syllabus path. History is the definitive archive. Revision recommends what deserves attention. Presentation projects existing Experience view models through UX-005 semantic tokens and shared design-system components — engines, recommendations, and session algorithms were not altered.

---

## Design rationale

Students should never wonder which page owns which decision. Prior Student OS surfaces still carried overlapping signals (session lists on Home, readiness KPI heritage, competing chrome, inconsistent card systems). SOP-001 applies a strict one-question law:

| Surface | Question | Design intent |
|---------|----------|---------------|
| **Home** | What should I do now? | Command centre — one Primary, calm context, no analytics wall |
| **Journey** | Where am I? | Motivating syllabus path — subject, progress, current/upcoming/completed |
| **History** | What have I accomplished? | Definitive archive — sessions, time, topics, milestones, readiness trends |
| **Revision** | What deserves my attention? | Recommendation surface — primary + ranked alternatives, not a flat list |

Premium means hierarchy and restraint: semantic tokens only, shared `.ds-*` primitives, no hard-coded colours in OS styles, exactly one Primary action on Home.

---

## Information architecture

```
Student OS shell
├── Home          → decide & act (Mission / Continue Session)
├── Journey       → locate self on syllabus
├── Revision      → attend to weak / overdue / high-value work
├── History       → review accomplishment archive
├── Choose Exam   → discovery (system nav; not a second Home)
├── Settings      → configuration
└── Help          → unblock
```

### Ownership matrix (no duplication)

| Concern | Owner | Removed / relocated from |
|---------|-------|--------------------------|
| Today's / Continue Session Primary | Home | — |
| Current Examination identity | Home (context) + Journey (path) | KPI walls elsewhere |
| Study Health (one calm line) | Home | Multi-KPI readiness panels |
| Contextual Quick Actions (≤3) | Home | Shell-nav clones / equal-weight CTA rows |
| Upcoming Deadlines | Home | — |
| Session archive / study time / mastered topics / achievements / readiness trends | **History** | Home Recent Progress |
| Syllabus position / learning path | Journey | Home educational dump |
| Weak / overdue / high-value revision | Revision | Home as competing mission |

---

## Screens redesigned

### Home — premium command centre

Sections (SOP-001):

1. **Today's Mission** / **Continue Session** (state-dependent L0; exactly one Primary)
2. **Current Examination**
3. **Study Health** (single status line — not a KPI wall)
4. **Quick Actions** (contextual ≤3; empty-state Primary already covers Choose Exam)
5. **Upcoming Deadlines**

Removed from Home:

- Recent Progress session list (History owns archives)
- Learning Queue as a parallel attention theatre (folded into Quick Actions)
- Legacy dashboard panels, coach walls, commitment chrome, MES trust walls

### Journey — visual syllabus

- Subject / examination identity
- Motivating progress track
- Current topic + upcoming topic
- Completed work timeline + path ahead
- Quiet return to Home (ghost), not a second daily Primary

### History — definitive archive

- Study time
- Readiness trends
- Sessions
- Completed topics
- Milestones / achievements
- Revision archive
- Compact bridge to Decision Journal / Educational Timeline (meaning layer)

### Revision — intelligent recommendation surface

- Primary recommendation with why / time / benefit / confidence
- Mission-primacy sentence retained (RR-001.3D)
- “Also deserves attention” alternatives
- Empty states teach return to Mission

---

## Components created

| Component | Location | Role |
|-----------|----------|------|
| `HomeExamination` | `app/presentation/student/dto/student_home.py` | Current exam context |
| `HomeStudyHealth` | same | Calm health signal |
| `HomeDeadline` | same | Deadline / milestone row |
| `HomeQuickAction` | same | Contextual next-step shortcut |
| `.ds-os-*` styles | `app/static/css/design_system.css` | Token-only OS presentation |
| `.ds-visually-hidden` | same | A11y helper |

Extended: `StudentHomePage`, `StudentHomeService.build_home` (projection only).

---

## Components removed

| Removed from UI | Rationale |
|-----------------|-----------|
| Home **Recent Progress** | Duplicated History sessions |
| Home **Learning Queue** section | Replaced by contextual Quick Actions |
| Home commitment / defer / MES trust / reflection preview chrome | Violates one-question Home; already DX-005A-incompatible |
| Journey heavy educational experience dump as primary chrome | Reduced cognitive load; syllabus path is primary |
| Parallel `student-card` / Bootstrap primary patterns on OS surfaces | Migrated to `.ds-*` |

---

## Navigation impact

- Canonical primary surfaces unchanged: Home · Journey · Revision · History · Settings (+ Choose Exam · Help).
- Shell page descriptions updated to the one-question phrases.
- Founder Console untouched (UX-001 routing preserved).
- No new routes; no endpoint renames.
- `student-page-title` retained on OS H1s for responsive shell contracts.

---

## Accessibility review

| Check | Status |
|-------|--------|
| Single H1 per surface | Pass — page-owned headers; shell header suppressed |
| Section headings (h2/h3) for OS blocks | Pass |
| One Primary CTA on Home | Pass — `ds-btn--primary` count ≤ 1 |
| Focus rings | Pass — design-system focus tokens |
| Progressbar semantics on Journey | Pass — `role="progressbar"` + valuemin/max/now |
| Colour-alone status | Improved — Study Health uses text status (avoids badge-only / gamification “badge” leakage) |
| Reduced motion | Pass — OS progress fill respects `prefers-reduced-motion` |
| Contrast | Relies on UX-005 tokens; no new hard-coded text colours |

---

## Performance impact

- Home no longer renders session archive rows (less DOM on daily entry).
- Journey / History / Revision load `design_system.css` (already cached across EOS).
- No new network calls, no engine recomputation, no additional snapshots beyond existing Home `include_all_surfaces` aggregate.
- Token-only CSS additions are small and cascade-friendly.

---

## Before vs after

| Aspect | Before | After |
|--------|--------|-------|
| Home purpose | Mission-first (DX-005A) but still overlapped History via Recent Progress | Command centre; archives off Home |
| Home sections | Mission + Queue + Recent Progress | Mission/Continue · Examination · Study Health · Quick Actions · Deadlines |
| Journey | Timeline + progress card + educational dump | Visual path with subject, progress, current/next, completed |
| History | Mixed archive + long epistemology bridge | Clear archive sections + short memory bridge |
| Revision | Card list with primacy copy | Recommendation hero + “also deserves attention” |
| Styling | Mixed `student-card` / Bootstrap | Shared `.ds-*` + `.ds-os-*` tokens |
| Page questions | Long descriptions | One sentence each |

---

## Files Created

- `knowledge/product/sop001_student_os/SOP001_STUDENT_OS_REPORT.md` (this file)
- `tests/presentation/test_sop001_student_os.py`

## Files Modified

- `app/presentation/student/dto/student_home.py`
- `app/presentation/student/services/student_home_service.py`
- `app/presentation/student/view_models.py`
- `app/presentation/student/views.py`
- `app/presentation/student/educational_view_models.py`
- `app/templates/student/home.html`
- `app/templates/student/journey.html`
- `app/templates/student/history.html`
- `app/templates/student/revision.html`
- `app/templates/design_system/macros.html`
- `app/static/css/design_system.css`
- `src/presentation/design_system/components/operational.py`
- Presentation tests updated for SOP-001 / HTML entity apostrophes / command-centre contracts

---

## Tests Executed

```text
python3 -m pytest \
  tests/presentation/test_sop001_student_os.py \
  tests/test_dx006b_student_home.py \
  tests/presentation/student/test_responsive.py \
  tests/presentation/student/test_recommendation_commitment_contract.py \
  tests/presentation/student/test_rr001_1_critical_remediation.py \
  tests/presentation/student/test_templates.py \
  tests/presentation/student/test_routes.py \
  tests/presentation/student/test_home_template_mes.py \
  -q
```

**Outcome:** 118 passed.

---

## Migration Impact

None.

---

## Architecture Compliance

- Layering preserved: templates + presentation DTOs/services only; no route math; no service dependence on `flask.request` beyond existing URL building for hrefs.
- Curriculum V1/V2 traversal: N/A (presentation only); both remain loadable.
- Learning / recommendation / session engines untouched.
- Founder Console untouched.
- UX-005 token policy: OS styles use semantic tokens only (no hex in SOP block).

---

## Technical Debt

1. Parallel button systems (`.ds-btn` / `.student-btn` / Bootstrap) remain outside these four surfaces.
2. Commitment / MES / reflection chrome still exist in application VMs but are intentionally not rendered on Home — a future surface (or Session complete) should own visible commitment continuity if product wants it again.
3. Journey still flattens topics (current / completed / upcoming) rather than full subject → section → topic tree when Runtime C section metadata is absent.
4. History still uses `history_card` student-card micro-template inside the DS page shell (thin residual).
5. Unified Journey nav labels (Today / Archive / …) unchanged when flag on — feature-mode SOP copy is the primary certification path.

---

## Known Limitations

- Presentation redesign only — recommendation ranking quality and readiness math unchanged.
- No screenshot gallery committed; dogfood Light/Dark recommended before Premium certification.
- Quick Actions are contextual and capped; they are not a second navigation tree.
- Study Health is a calm projection of existing readiness fields — not a new health engine.

---

## Remaining technical debt

See Technical Debt. Highest follow-ups: (1) nest Journey by section when educational position is available, (2) migrate `history_card` fully to `.ds-panel`, (3) decide permanent home for commitment continuity chrome outside Home.

---

## Success criteria

| Criterion | Status |
|-----------|--------|
| Students know what to do (Home) | Pass — Mission/Continue + one Primary |
| Students know where they are (Journey) | Pass — subject + path + progress |
| Students know what they've achieved (History) | Pass — archive ownership |
| Students know what deserves attention (Revision) | Pass — recommendation-first |
| Cohesive Student OS | Pass — shared DS + one-question IA |
| No Founder redesign / no algorithm change | Pass |
