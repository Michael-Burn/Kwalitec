# V1S-004 — Founder Dogfooding & Educational Validation

**Programme:** V1S-004 · Version 1 Stabilisation  
**Phase:** Founder dogfooding + educational validation  
**Date:** 2026-07-31  
**Nature:** Validation only — **no new educational capabilities**  
**Authority:** V1S-003 · V1S-002 · V1S-001 · KWP-015 · `PRODUCT_BLUEPRINT.md` · `V1_RELEASE_CRITERIA.md`

---

## Executive Summary

V1S-004 audited whether Kwalitec can support **consistent daily study** without external planning. The dogfood spine (PublishedCurriculumAuthority → Educational Runtime → Certified Mission → Student Runtime Coordinator → Learning Session → Educational Authoring → Adaptive Workspace) is **structurally ready**. Educational Authoring, empty/quiet states, and the Home→Session→Sitting Report loop **work well**.

The product does **not** yet clear the success bar of “a complete week of real study without workarounds.” Preconditions and frictions that force workarounds:

1. **Founder-published CS1 package** still required (V1S-002 condition).
2. **Silent Learning Episode failure** can hide today’s lesson.
3. **Journey vs My Learning Journey** naming/nav dual-model.
4. **Non-functional Start Early / Start Tomorrow** CTAs.
5. **Progress singularity residuals** remain an educational-trust risk.

**Verdict:** **HOLD — dogfood GO WITH CONDITIONS.** Begin exclusive CS1 study after packages are active; treat the Issue Register as the only improvement queue. Do not add features in this programme.

Canonical registry: `app/services/dogfood_validation.py` · Founder board: `/founder/v1-readiness`.

---

## Validation Audit

Mandatory surfaces reviewed and classified:

| Surface | Verdict | Summary |
|---|---|---|
| Learning Episodes | **WORKS WELL** | Objective, context, success criteria, CMP rejection, scrubbing. Display-only activities and silent compose failure are follow-ups. |
| Adaptive Workspace | **FRICTION** | Strong Morning Brief → Episode → Plan → Focus → Tomorrow arc; Home density and secondary CTAs create daily friction. |
| Mission Runtime | **WORKS WELL** | Single spine ERE + CertifiedMissionEngine + StudentRuntimeCoordinator + LSR. |
| Educational Authoring | **WORKS WELL** | Composition-only (A8); tomorrow/extra-study capacity gates hold; narrative under-rendered on Home. |
| Student Journey | **FRICTION** | Syllabus Journey and My Learning Journey both valuable; nav label “Journey” confuses them. |
| Founder Readiness | **WORKS WELL** | Honest HOLD status; V1S-004 adds Dogfood Progress, Validation Issues, Educational Improvements, Resolved, Outstanding. |

### Taxonomy counts (registry)

| Class | Count |
|---|---|
| WORKS WELL | 4 |
| FRICTION | 5 |
| BUG | 2 |
| DESIGN IMPROVEMENT | 4 |
| EDUCATIONAL IMPROVEMENT | 1 (issue) + 5 EI backlog items |

---

## Validation Log

Structured log fields (also on Founder board):

| Field | Purpose |
|---|---|
| Study date | Calendar day of sitting |
| Mission completed | What was attempted / finished |
| Time spent | Minutes |
| Points of confusion | Cognitive / copy confusion |
| Missing content | Gaps in episode / syllabus substance |
| Poor wording | Terminology / prose issues |
| Navigation friction | Dead ends, wrong destinations |
| Unexpected behaviour | Bugs / silent failures |
| Suggestions | Improvement ideas |
| Four-question notes | Educational review answers |

### Recorded sittings (2026-07-31)

#### Sitting A — Pre-enrol / empty-state audit (CS1) · 45 min · `code_audit`

| Field | Notes |
|---|---|
| Mission completed | Home empty/quiet + Journey surfaces; exclusive sitting blocked until published package |
| Confusion | Nav “Journey” ≠ My Learning Journey; Home section overlap |
| Missing content | Rich episodes / curriculum why need published package |
| Poor wording | Archive `strategy_title` risk |
| Navigation | My Learning Journey off primary nav; Session “Open Journey” → syllabus |
| Unexpected | Start Early → Home only; authoring bare-except → None |
| Suggestions | Publish CS1; relabel Journey; surface authoring failure |

#### Sitting B — Spine walkthrough (CS1) · 60 min · `code_audit`

| Field | Notes |
|---|---|
| Mission completed | Adaptive Workspace → Begin Session path → Sitting Report → History |
| Confusion | Forecast Quick Action shares Learning Journey URL; Home activities not checklist |
| Missing content | `mission_narrative` unused; activity prompts titles-only |
| Poor wording | Footer “Diagnostics”; `complete_runtime_c` DOM attrs |
| Navigation | Home 10+ sections |
| Unexpected | Mark-complete Runtime C rollback path still visible |
| Suggestions | Collapse arc; honest CTAs; scrub engine nouns |

**Live exclusive week:** not started — **HOLD** pending DF-001. Append further rows as `evidence_kind=live_sitting`.

---

## Educational Findings

Blueprint daily questions (Vision / Product Blueprint):

### What am I learning today?

| Status | Partial PASS |
|---|---|
| Works | Morning Brief today line; Mission panel; Learning Episode `learning_objective`; Session Plan objective |
| Gap | Quiet state or silent authoring failure leaves Q1 unanswered (**EI-001**, **DF-003**) |
| Class | **EDUCATIONAL IMPROVEMENT** when package/authoring missing |

### Why am I learning it?

| Status | Conditional PASS |
|---|---|
| Works | Episode educational context; “Why this Session?”; KA curriculum why when graph present |
| Gap | Without published package graph, why becomes generic (**EI-002**, **DF-001**) |
| Class | **EDUCATIONAL IMPROVEMENT** / **FRICTION** |

### How do I know I succeeded?

| Status | Partial PASS |
|---|---|
| Works | Home success criteria; Checkpoint / Reflection prompts; Sitting Report post-session |
| Gap | Criteria are pre-session targets; activities display-only; confirmation only after Session (**EI-003**, **DF-009**) |
| Class | **EDUCATIONAL IMPROVEMENT** |

### What should I do next?

| Status | Conditional PASS |
|---|---|
| Works | Begin / Continue Session primary CTA; Tomorrow Preview continuity; Sitting Report next step |
| Gap | Start Early / Extra Study misleading; dual Journey destinations (**EI-004**, **DF-006**, **DF-004**) |
| Class | **FRICTION** / **EDUCATIONAL IMPROVEMENT** |

### Educational Improvements backlog (EI)

| ID | Question | Priority | Status |
|---|---|---|---|
| EI-001 | What am I learning today? | P0 | OPEN |
| EI-002 | Why am I learning it? | P0 | OPEN |
| EI-003 | How do I know I succeeded? | P1 | OPEN |
| EI-004 | What should I do next? | P1 | OPEN |
| EI-005 | What am I learning today? (under-exposed narrative) | P1 | OPEN |

---

## Product Findings

| Area | Score (1–5) | Finding |
|---|---|---|
| Loading states | **2** | Skeleton tokens unused on Home |
| Empty states | **4** | Calm `ds_empty_operational` across Home / Journey / Map |
| Navigation | **3** | Dual Journey model; Forecast duplicate href |
| Typography | **4** | Design-system hierarchy holds |
| Spacing | **3** | Home section stack cognitively heavy |
| Motion | **3** | Subtle; Focus mode in Session |
| Terminology | **3** | Mostly Product Language Guide; Diagnostics / strategy_title leaks |
| Daily workflow | **4** | Coherent when packages + flags set |

Overall product posture: **usable for daily study with conditions** — not yet “invisible infrastructure.”

---

## Engineering Findings

| Area | Finding | Class |
|---|---|---|
| Mission spine | Single documented spine; ME/MEV2/Adapter off path | WORKS WELL |
| Authoring failure handling | Bare `except` in `_mission_composition` → None | **BUG** (DF-003) |
| Progress writes | ProgressEngine on Runtime C; Runtime A mastery residual | **BUG** risk (DF-002) |
| Presentation purity | Adaptive Workspace does not write Evidence/Progress/Twin | WORKS WELL (A7) |
| Authoring purity | Does not select/reschedule missions | WORKS WELL (A8) |
| Secondary CTAs | Start Early / start_tomorrow → `student.home` | FRICTION (DF-006) |
| Unused composition | `mission_narrative` projected, not rendered | DESIGN (DF-008) |
| Repo / lifecycle | V1S-003 ownership unchanged; no educational behaviour change | WORKS WELL |

No new educational algorithms, curriculum cutovers, or student UI redesigns were introduced in V1S-004 beyond Founder readiness observability.

---

## Issue Register

| ID | Title | Class | Priority | Status |
|---|---|---|---|---|
| DF-001 | Published packages required before exclusive CS1 dogfood | FRICTION | P0 | OPEN |
| DF-002 | Progress singularity residuals | BUG | P0 | OPEN |
| DF-003 | Silent Learning Episode failure on Home | BUG | P0 | OPEN |
| DF-004 | Journey vs My Learning Journey navigation | FRICTION | P1 | OPEN |
| DF-005 | Home information density / duplicated arc | DESIGN IMPROVEMENT | P1 | OPEN |
| DF-006 | Start Early / Start Tomorrow CTAs do not advance | FRICTION | P1 | OPEN |
| DF-007 | strategy_title leak on Learning Journey archives | FRICTION | P1 | OPEN |
| DF-008 | mission_narrative authored but not shown | DESIGN IMPROVEMENT | P1 | OPEN |
| DF-009 | Episode activities display-only on Home | EDUCATIONAL IMPROVEMENT | P1 | OPEN |
| DF-010 | Forecast Quick Action duplicates Journey URL | DESIGN IMPROVEMENT | P2 | OPEN |
| DF-011 | Footer Diagnostics link | FRICTION | P2 | OPEN |
| DF-012 | No loading skeleton on Home | DESIGN IMPROVEMENT | P2 | OPEN |
| DF-W01 | Deterministic Educational Authoring + CMP rejection | WORKS WELL | — | RESOLVED |
| DF-W02 | Adaptive Workspace consumes engines (E9) | WORKS WELL | — | RESOLVED |
| DF-W03 | Single mission spine | WORKS WELL | — | RESOLVED |
| DF-W04 | Empty / quiet / day-complete states | WORKS WELL | — | RESOLVED |

Full detail: `app/services/dogfood_validation.py`.

---

## Improvement Backlog

Prioritised for programmes **after** V1S-004 (do not implement as feature creep here):

### P0 — before claiming a clean study week

1. **Publish CS1 package** and confirm `dogfood_curriculum_cutover` (DF-001).
2. **Surface authoring failure** as quiet educational copy (DF-003 / EI-001).
3. **Isolate dogfood progress** to ProgressEngine / Runtime C only; no JSON mastery theatre (DF-002).

### P1 — reduce daily friction

4. Resolve Journey naming / nav / Sitting Report CTA (DF-004).
5. Collapse Home Mission / Episode / Plan / Focus duplication (DF-005).
6. Wire or demote Start Early / Start Tomorrow (DF-006 / EI-004).
7. Scrub `strategy_title` on student archives (DF-007).
8. Render or drop `mission_narrative` (DF-008 / EI-005).
9. Preview Session stages from episode activities (DF-009 / EI-003).

### P2 — polish

10. Forecast deep-link or remove duplicate Quick Action (DF-010).
11. Relabel footer Diagnostics (DF-011).
12. Optional Home loading skeleton (DF-012).

### Deferred (engineering programmes)

- MissionEngineV2 / MissionAdapter REMOVE gates (V1S-003)
- `src/` adopt-or-archive
- RI-002 Runtime A hard removal
- Progress singularity completion programme

---

## Release Impact

| Gate set | Impact |
|---|---|
| `V1_RELEASE_CRITERIA.md` Educational E1–E9 | **HOLD** pending live package spot-check; code path supports PASS with conditions |
| Product P1–P8 | **HOLD** on P6 (Journey dual-surface) and residual P8 leaks |
| Architecture A1–A8 | Unchanged from V1S-002/003 — **PASS** with documented HOLDs |
| Technical T9–T11 | Unchanged — **PASS** |
| Dogfooding go/no-go | Remains **DOGFOOD GO WITH CONDITIONS** |
| P-002.1 production-ready | **NO-GO** (G1 KSI still FAIL; exclusive week incomplete) |

Release criteria document updated to reference V1S-004 and dogfood validation registry.

---

## Recommendation

1. **Do not** declare a complete dogfood week yet.
2. **Do** founder-publish CS1 immediately; enrol Runtime C; keep `SR_SESSION_PRIMARY` on.
3. **Run** a 5–7 day exclusive CS1 week using only Kwalitec; append every sitting to the Validation Log (`live_sitting`).
4. **Fix** only P0 items (DF-001 operational; DF-003 code; DF-002 isolation) before claiming Success.
5. **Triage** all other findings through the Improvement Backlog — no parallel feature programmes from founder frustration.
6. Use `/founder/v1-readiness` Dogfood Progress / Outstanding Issues as the living board.

**Next programme suggestion:** V1S-005 (or focused fix train) — P0/P1 dogfood remediation only; still no new educational intelligence.

---

## Student Impact Assessment

| Lens | Assessment |
|---|---|
| Student problem | Daily study still requires founder workarounds (packages, Journey mental model, misleading CTAs) |
| Student benefit | Clear map of what blocks consistent learning; Founder board makes issues visible |
| Learning benefit | No new learning algorithms; validation protects educational trust |
| Success metrics | Exclusive week completed; P0 closed; four questions answerable every sitting |
| Risks | Treating code-audit as live week completion; adding features instead of fixing P0 |
| Assumptions | Founder will publish packages and log live sittings honestly |

---

## Estimated KSI contribution

**ΔKSI = 0** (provisional). Validation/observability programme; no validated student-value measurement. Live exclusive week is the prerequisite for any KSI claim from dogfood.

---

## Evidence collected

- `app/services/dogfood_validation.py` — registry  
- `app/services/v1_readiness_dashboard.py` — snapshot sections  
- `app/founder/dashboard/templates/founder_dashboard/v1_readiness.html` — UI  
- `tests/test_v1s004_dogfood_validation.py`  
- Prior: `V1S001` / `V1S002` / `V1S003` reports; `V1_RELEASE_CRITERIA.md`  
- Code anchors: `adaptive_workspace.py` `_mission_composition`, `_quick_actions`; `educational_authoring/`; `home.html`; `journey.html`; `learning_journey.html`

---

## Lessons learned for student value

Architecture completeness does not equal study fitness. The spine can be correct while the day still fails: missing packages, silent omissions, and CTAs that look like next steps but are not. **Dogfood is the only way to discover those failures.** Founder frustration must become prioritised issues — not new engines.

---

## Explainability Review

**N/A for new intelligence** — no recommendation/forecast algorithms changed.  
**In-scope observation:** Current Focus and curriculum why remain explainable when graph data exists; package absence degrades explanation quality (EI-002).

---

## Recommendation Quality Review

**N/A** — no ranking/selection changes. Secondary CTA honesty (DF-006, DF-010) is a presentation-quality issue affecting perceived recommendation quality.

---

## Version 1 readiness residual

Open gates (dogfood board):

- Exclusive CS1 live week  
- DF-001 / DF-002 / DF-003  
- Gate G1 validated KSI  
- Progress singularity  
- RI-002 Runtime A hard removal  
- Mission package physical REMOVE  
- `src/` adopt-or-archive  

---

## CRI domains improved

None material (validation/observability). **ΔCRI = 0** provisional.

---

## Estimated CRI delta

**0** — no commercial surface change.

---

## Evidence supporting the increase

N/A.

---

## Remaining blockers

See Issue Register outstanding + Founder Remaining blockers.

---

## Provisional or validated

All scores and ΔKSI / ΔCRI claims are **provisional**. Live `live_sitting` logs are required to validate educational confidence.

---

## Tests Executed

```
python3 -m pytest tests/test_v1s004_dogfood_validation.py \
  tests/test_v1s003_repository_health.py -q
```

Outcome: **16 passed**.

```
ruff check app/services/dogfood_validation.py \
  app/services/v1_readiness_dashboard.py \
  tests/test_v1s004_dogfood_validation.py
```

Outcome: clean.
---

## Migration Impact

**None** — no Alembic / schema changes.

---

## Files Created

- `app/services/dogfood_validation.py`
- `tests/test_v1s004_dogfood_validation.py`
- `V1S004_DOGFOOD_REPORT.md`

## Files Modified

- `app/services/v1_readiness_dashboard.py`
- `app/founder/dashboard/templates/founder_dashboard/v1_readiness.html`
- `tests/test_v1s003_repository_health.py`
- `V1_RELEASE_CRITERIA.md`

## Architecture Compliance

- Layering preserved: Founder observability + static registry only.
- **No** redesign of Learning Runtime, Evidence, Progress, Strategy, Diagnostics, Difficulty, Intervention Effectiveness, Educational Memory, Forecast, Knowledge Architecture, Educational Authoring algorithms, or Adaptive Workspace composition logic.
- Curriculum V1/V2 loader singularity unchanged.
- V1S-002 dogfood cutover and mission spine unchanged.
- Application code limited to dogfood registry + readiness dashboard.

## Technical Debt

Introduced: none educational. Catalogued student-facing debt into DF/EI registers (owned).

## Known Limitations

1. Validation sittings are **code_audit** — not a completed exclusive live week.
2. Live episode quality across real published CS1 content still unvalidated (E1–E4 human spot-check).
3. Does not claim P-002.1 production-ready / Gate G1.
4. Does not implement P0/P1 fixes (discovery programme by design).

## Success criteria

| Criterion | Result |
|---|---|
| Complete validation audit with taxonomy | **PASS** |
| Validation log structured and seeded | **PASS** (code_audit; live week HOLD) |
| Educational four-question review | **PASS** (gaps recorded as EI) |
| Product area ratings | **PASS** |
| Founder V1 Readiness extended (Dogfood Progress / Issues / Educational / Resolved / Outstanding) | **PASS** |
| No new educational capabilities | **PASS** |
| Complete week without workarounds | **HOLD** — blocked by DF-001…DF-003 + live week |
| Every issue prioritised | **PASS** |
