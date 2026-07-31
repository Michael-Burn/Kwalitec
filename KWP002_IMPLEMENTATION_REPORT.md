# KWP-002 — Student Value Activation

**Programme:** KWP-002 · Student Value Activation  
**Phase:** Commercialisation Phase 2  
**Date:** 2026-07-30  
**Nature:** Experience-layer activation — **no runtime redesign**  
**Authority:** KWP-001 · SR-001 · SR-001A · SR-003 · `PRODUCT_BLUEPRINT.md` · Product Language Guide  

---

## Executive Summary

KWP-002 converts the completed SR-001A Student Runtime into a commercial student experience. The programme enables a single **Commercial Loop Profile**, scrubs engine terminology from learner surfaces, and mounts calm Home / Session / Journey moments that already exist in authorities — without changing Progress, Evidence, Twin, or Mission selection math.

With `KWALITEC_COMMERCIAL_LOOP=1` (enabled in `render.yaml` for production Alpha):

| Flag | Effect |
|---|---|
| `SR_SESSION_PRIMARY` | One Session primary on Home |
| `SR_SESSION_SUBSTANCE` | Read → Worked example → Practice → Reflection |
| `SR_SESSION_COMPLETION_PRODUCT` | Finish Review + pause/resume |
| `SR_EVIDENCE_GATE` | Honest completion before progress advances |
| `SR_TWIN_DAILY_LOOP` | Twin observes Accepted Educational+ only |
| `SR_PROGRESS_SINGULARITY` | Singular Study Progress narrative |

Pilot Mark-complete remains off and is never part of the commercial bundle. Individual `SR_*=0` overrides still win for emergency rollback.

**Verdict:** The product can now feel like a premium actuarial study companion — one defended Session, explainable why, honest finish, Journey movement — while SR-001A authorities stay invisible.

---

## Student Experience Before / After

| Moment | Before (defaults) | After (Commercial Loop) |
|---|---|---|
| Home primary | Often **Mark mission complete** (Runtime C rollback) | **Start Today's Session** / **Continue** |
| Home lexicon | Today's Mission · Building evidence | Today's Session · Getting started / Study Health |
| Why today? | L1 `why_now` only | **Why this Session?** disclosure + Exam Readiness card |
| Session title | Generic “Session” | **Today: {topic}** |
| Gate flash | “educational evidence” | Outcome language (“need a bit more practice…”) |
| Completion | Thin summary | Completion moment + Journey update + Learning Insights |
| Journey | “Overall mastery” | **Syllabus Progress** · Up Next · Needs Attention · Remaining Topics · Learning Insights |
| Knowledge Map | “N nodes · M links” | “N topics · M connections” |
| Technical IDs | Learner-visible details | Hidden from session chrome |

---

## Screens Updated

| Surface | Change |
|---|---|
| Student Home | Session lexicon, Why this Session?, Study Health copy, Exam Readiness card, Mark-complete demoted |
| Session overview / activity / reflection / summary / complete | Topic titles, educational flow label, completion moment, Journey update, technical details removed |
| Journey | Syllabus Progress, Learning Insights, Up Next, Needs Attention, Remaining Topics |
| Knowledge Map | Topics/connections language |
| History | Practice record (not “practice evidence”) |
| Tutor | Learning Insights empty state; no Twin/authorised jargon |
| Decision Journal | “What this was based on” (not “Evidence at the time”) |
| Assessment chrome | Session-aligned practice language |

---

## Language Guide Compliance

Aligned with `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` and `app/presentation/product_language.py`.

**Learner UI now prefers:** Session · Today's Session · Journey · Learning Insights · Exam Readiness · Home · History

**Removed from student surfaces (P4 audit):**

- Mission Engine (never shown)
- Twin / learning Twin
- Educational / practice / building evidence wording
- Overall mastery
- Nodes / links / curriculum nodes
- Authority jargon in Tutor/Home flashes
- Technical Session/Activity/Mission IDs on session chrome
- Learner-visible Mark mission complete under Commercial Loop

`REJECTED_SYNONYMS` extended with: `learning twin`, `building evidence`, `educational evidence`, `practice evidence`, `overall mastery`, `mark mission complete`.

Rollback Mark-complete remains available only when `SR_SESSION_PRIMARY` is OFF or `SR_PILOT_MARK_COMPLETE` is ON — never the commercial default.

---

## Commercial Loop Activation

### Profile

| Env | Role |
|---|---|
| `KWALITEC_COMMERCIAL_LOOP=1` | Master switch (also `SR_COMMERCIAL_LOOP`) |
| Individual `SR_*` | Explicit override when set |
| `SR_PILOT_MARK_COMPLETE` | Never inherited from Commercial Loop |

### Resolution

```
if SR_* env set → use explicit truthy/falsy
else if Commercial Loop ON → enable SR bundle flag
else → OFF
```

### Production

`render.yaml` sets `KWALITEC_COMMERCIAL_LOOP=1` alongside sole-runtime Alpha flags. `.env.example` documents the profile and per-flag overrides.

### Defaults in bare process / tests

Commercial Loop remains **OFF** unless env-enabled — existing SR programme tests that assert default OFF stay green.

---

## Files Created

- `tests/test_kwp002_student_value_activation.py`
- `KWP002_IMPLEMENTATION_REPORT.md` (this file)

## Files Modified

### Config / ops

- `app/application/config/v2_flags.py` — Commercial Loop Profile + SR bundle inheritance
- `render.yaml` — `KWALITEC_COMMERCIAL_LOOP=1`
- `.env.example` — profile documentation
- `tests/operational/helpers.py` — `ALPHA_ENV_VARS` includes commercial loop

### Presentation — Home / Journey / language

- `app/presentation/student/services/student_home_service.py`
- `app/presentation/student/educational_view_models.py`
- `app/presentation/student/view_models.py` — Journey narrative fields
- `app/presentation/student/dto/student_home.py`
- `app/presentation/student/routes.py`
- `app/presentation/product_language.py`
- `app/templates/student/home.html`
- `app/templates/student/journey.html`
- `app/templates/student/knowledge_graph.html`
- `app/templates/student/history.html`
- `app/templates/student/tutor.html`
- `app/templates/student/decision_journal.html`
- `app/templates/student/components/explanation_card.html`
- `app/templates/student/assessment/base.html`
- `app/templates/student/assessment/complete.html`

### Presentation — Session

- `app/presentation/session/messages.py`
- `app/presentation/session/view_models.py`
- `app/presentation/session/dto/study_session.py`
- `app/presentation/session/services/study_session_service.py`
- `app/templates/session/partials/session_body.html`

### Tests updated for lexicon

- `tests/test_dx006b_student_home.py`
- `tests/test_sr002_session_spine.py`
- `tests/presentation/student/test_templates.py`
- `tests/presentation/test_sop001_student_os.py`

---

## Tests Added

`tests/test_kwp002_student_value_activation.py` covers:

- Commercial Loop default OFF / bundle ON / alias / explicit override
- `render.yaml` commercial activation
- Rejected synonym extensions + outcome-language flashes
- Student route / template forbidden-term scrub
- Home Session lexicon + Why/Readiness hooks
- Journey Syllabus Progress / Insights / Up Next structure
- Session completion-moment hooks

### Tests Executed

```bash
python3 -m pytest \
  tests/test_kwp002_student_value_activation.py \
  tests/test_sr002_session_spine.py \
  tests/test_dx006b_student_home.py \
  tests/test_lxp003_session_product.py \
  tests/test_lxp004a_session_substance.py \
  tests/test_ev001b_evidence_gate.py \
  tests/test_sdt004_twin_activation.py \
  tests/test_sr003_progress_singularity.py \
  tests/presentation/session/test_product_language.py \
  tests/presentation/student/test_templates.py \
  -q
```

**Outcome:** Pass (KWP-002 + SR flag suites + language/template guards).

```bash
python3 -m ruff check app/application/config/v2_flags.py \
  app/presentation/student/services/student_home_service.py \
  app/presentation/session/services/study_session_service.py \
  app/presentation/session/messages.py \
  app/presentation/product_language.py \
  tests/test_kwp002_student_value_activation.py
```

**Outcome:** Clean on touched modules after E501 fixes.

---

## Migration Impact

**None.** No Alembic revisions. Flag resolution and presentation only.

---

## Architecture Compliance

| Invariant | Status |
|---|---|
| LearningSessionRuntime sole session AUTHORITY | Unchanged |
| EducationalEvidenceAuthority sole Evidence AUTHORITY | Unchanged — copy only |
| StudentTwinEngine estimate AUTHORITY | Unchanged — surfaced as Learning Insights |
| ProgressEngine sole Progress AUTHORITY | Unchanged — Journey narrates coverage as Syllabus Progress |
| Mission selection AUTHORITY | Unchanged |
| Curriculum V1/V2 loadable | N/A — no curriculum engine edits |
| Layering | Presentation + config only; no engine math |

**Explicit non-goals respected:** no Progress redesign, no Evidence redesign, no Twin redesign, no SR-001A authority changes.

---

## Accessibility Review

| Check | Result |
|---|---|
| Why this Session? uses `<details>` / summary disclosure | Pass — keyboard expandable |
| Exam Readiness card labelled section | Pass — existing `aria-labelledby` pattern |
| Journey progressbar retained | Pass — `role="progressbar"` with valuemin/max/now |
| Primary CTA strip `role="group"` / aria-label | Preserved |
| Technical details removed (reduces noise) | Pass |
| Completion moment `role="status"` | Pass |
| Focus mode / landmarks on session | Unchanged |
| Colour/contrast | Uses existing design-system tokens — no new low-contrast chrome |

**Residual:** Needs Attention empty state is calm text; when Progress weak-topic annotations are later projected into Journey VMs, ensure list items remain list-marked (already `<ul class="ds-list">`).

---

## Student Impact Assessment

Template: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Value |
|---|---|
| **Programme** | KWP-002 |
| **Student-visible change?** | Yes — gated by Commercial Loop (ON in production Alpha) |
| **Production activation?** | Yes via `KWALITEC_COMMERCIAL_LOOP=1` in `render.yaml` |
| **Related KSI** | K1 (decision clarity), K2 (recommendation acceptance), K3 (progress honesty), K7 (trust/language), K8 (explainability) |

### 1. Student problem

Students with a working Educational OS still saw an Internal Alpha operating system: Mark-complete pilot CTAs, evidence/Twin jargon, mastery mislabels, and no “why this Session” or post-session Journey moment. Latent premium capability was flag-gated OFF.

**Evidence:** KWP-001 audit (`KWP001_STUDENT_VALUE_ROADMAP.md`).

### 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | Yes | One Session primary; Start Today's Session |
| How am I progressing? | Yes | Syllabus Progress + Journey update after Session |
| What is stopping me? | Partial | Needs Attention scaffold + Study Health / Readiness |
| What happens next? | Yes | Up Next + completion teaser |

**Final Test:** Does this help students become better professionals? **Yes** — clearer daily decisions, honest completion culture, syllabus-faithful progress language without engine noise.

### 3. Learning benefit

Integrity Progress remains lawful (Evidence Gate ON under Commercial Loop). Learning Insights and Syllabus Progress teach that progress means demonstrated practice on the official syllabus — not vanity completion.

### Success metrics (provisional)

- Higher Start Today's Session rate vs Mark-complete era
- Finish Review completion under Evidence Gate
- Qualitative: “I know why today” / “progress feels real”

### Risks / assumptions

- Enabling Evidence Gate without substance feels punitive → mitigated by Substance ON in same bundle + outcome-language flashes
- Twin silence read as broken → Learning Insights “building” empty states
- Coverage ≠ understanding → Syllabus Progress naming

---

## Commercial Readiness Assessment

| Domain (CRI lens) | Movement | Notes |
|---|---|---|
| CR1 Product clarity | Improved (provisional) | Commercial Loop packages the paid daily loop |
| CR2 Student trust / language | Improved (provisional) | Language Guide scrub on student + session templates |
| CR3 Study loop reliability | Improved (provisional) | Session Primary + Substance + Completion + Gate ON together |
| CR4 Explainability | Improved (provisional) | Why this Session + Readiness on Home |
| Pass probability marketing | Unchanged | No guarantee language introduced |

**Estimated CRI delta:** provisional **+2 to +4** on clarity/trust/loop domains — **not validated**. Do not mint `cri-*` tags on this report alone.

**Remaining blockers:** weak-topic Needs Attention still scaffolded (awaits Progress projection wiring into Journey VM); practice correctness UX and pace-to-exam (KWP-001 P3) not in this milestone; Assessment/Exam Briefing premium pack deferred.

**Provisional or validated:** **Provisional.**

---

## Technical Debt

1. Journey `needs_attention` is presentation-ready but not yet filled from Progress Engine `weak_topic_ids` (lawful consumer wiring remains a follow-up — not an authority change).
2. Legacy `/dashboard` and `/missions` templates still contain “Study Session” lexicon (outside sole-runtime student chrome; not activated by Commercial Loop).
3. `CompleteRuntimeMissionForm` still labels Mark-complete for rollback/pilot paths.
4. Founder-only technical session diagnostics were removed from learner chrome; re-add behind a founder diagnostic gate if ops need them.

---

## Known Limitations

- Does not redesign Progress / Evidence / Twin / Mission engines.
- Does not ship weekly Exam Briefing or mock assessment reports (KWP-001 premium later).
- Does not soften “Internal Alpha” login chrome (M6 residual).
- Needs Attention remains honest empty/building until Progress weak annotations are projected.
- Commercial Loop OFF in bare test process — local `.env` must set `KWALITEC_COMMERCIAL_LOOP=1` to dogfood the paid path.

---

## Architecture stance

> The architecture should become less visible as the product becomes more valuable.

KWP-002 delivers that packaging mandate for Phase 2. SR-001A remains the Educational Operating System; students meet a study companion.

---

**Document status:** Complete — KWP-002 implementation deliverable  
**Next:** Dogfood Commercial Loop on published CS1; optional Progress→Journey weak-topic projection (presentation consumer only)  
