# P-004.1 — Student Pain Points

**Programme:** P-004.1 — KSI Gap Analysis & Improvement Roadmap  
**Date:** 2026-07-26  
**Status:** Analysis only  
**Claim window:** W-PROD (sole-runtime) unless noted  
**Sources:** EP-004 blind corpus · EP-005.2 journey review · EP-006/007 Tier B residuals · Decision/Risk/Assumption registers  

---

## 1. Journey map (canonical W-PROD)

```
First login / onboarding / calibration
        ↓
Student Home (single canonical entry)
        ↓
┌─── Mission / Daily focus ───┐
│         Planning            │
└─────────────┬───────────────┘
              ↓
        Study Session
   (overview → activity → summary)
              ↓
     Completion / Outcome
              ↓
   Reflection / return Home
              ↓
 Analytics / Readiness surfaces
```

Legacy `/dashboard` dual-home friction is **cleared on W-PROD sole-runtime** (EP-007.1/007.2). Dual-run Alpha residual remains **out of W-PROD claim window**.

---

## 2. Pain-point catalogue

Severity scale: **Critical** (blocks trust or V1 gate) · **High** (frequent / large KSI drag) · **Medium** · **Low**.

Likely KSI impact is **planning estimate** of composite points if the pain is substantially resolved and re-validated — not a validated forecast.

---

### PP-001 — Recommendation trust incomplete (why / evidence / alternatives thin)

| Field | Content |
|---|---|
| **Identifier** | PP-001 |
| **Journey stage** | Home · Mission tip · Coach / Insight |
| **Severity** | **Critical** |
| **Evidence** | K2=55; REM-06 open; historical Coach opacity (SV-014 class) partially mitigated by MES but acceptance unproven; DR-036 freeze; PA-014 Hypothesis |
| **Likely KSI impact** | **+2.0 to +3.5** (primarily K2; secondary K8) |
| **Root cause** | RC-05 |
| **Related decisions** | DR-036, DR-050, DR-052 |
| **Related risks** | PR-001, PR-002 |
| **Student experience** | “I see a tip, but I am not sure I should follow it over my own notes.” |
| **Failure modes** | Confusion · educational uncertainty · trust loss |
| **Potential solutions** | IMP-01 trust surfaces; IMP-02 acceptance instrumentation; refuse opaque LLM coach |

---

### PP-002 — No external proof that following guidance improves study behaviour

| Field | Content |
|---|---|
| **Identifier** | PP-002 |
| **Journey stage** | Cross-cutting (effectiveness) |
| **Severity** | **Critical** (gate) |
| **Evidence** | N_external=0; EP-007.3 G1.9 FAIL; effectiveness NO-GO; PR-001, PR-006, PR-007; privacy unsigned PR-003 |
| **Likely KSI impact** | **Claimability + confidence** (enables Strong-band); direct ΔKSI uncertain until scorecards |
| **Root cause** | RC-07 |
| **Related decisions** | DR-033, DR-041; EFF-02…EFF-08 |
| **Related risks** | PR-001, PR-003, PR-006, PR-007, PR-008 |
| **Student experience** | Product may feel organised; student cannot know it helps *them* pass. |
| **Failure modes** | Trust loss · motivation loss · educational uncertainty |
| **Potential solutions** | IMP-03 Stage 1 cohort ops (privacy → invites → M1–M9 → interviews) |

---

### PP-003 — Personalisation invisible under production defaults

| Field | Content |
|---|---|
| **Identifier** | PP-003 |
| **Journey stage** | Home · Planning · Recommendations |
| **Severity** | **High** |
| **Evidence** | K4=55; flags OFF DR-038/039; EP-004.* estimated Δ unsupported; PA-011 Hypothesis; PR-016 |
| **Likely KSI impact** | **+1.5 to +3.0** after activation + validation (K4 primary; K1/K2 secondary) |
| **Root cause** | RC-06 |
| **Related decisions** | DR-038, DR-039, DR-043 |
| **Related risks** | PR-012, PR-016 |
| **Student experience** | “It feels like a structured default, not *my* plan.” |
| **Failure modes** | Educational uncertainty · motivation loss |
| **Potential solutions** | IMP-04 controlled dogfood → soak → G12; visible provenance factors |

---

### PP-004 — Analytics not decision-grade (progress without next action)

| Field | Content |
|---|---|
| **Identifier** | PP-004 |
| **Journey stage** | Analytics · History · Journey surfaces |
| **Severity** | **High** |
| **Evidence** | K6=50 floor; feedback OFF; Journey emit deferred; RC-09; PR-011 |
| **Likely KSI impact** | **+1.0 to +2.0** (K6) |
| **Root cause** | RC-09 (+ RC-06) |
| **Related decisions** | DR-038, DR-047 |
| **Related risks** | PR-011 |
| **Student experience** | “I can see charts, but not what to change tonight.” |
| **Failure modes** | Cognitive overload · educational uncertainty · dead ends |
| **Potential solutions** | IMP-05 decision-linked analytics; avoid vanity metrics |

---

### PP-005 — Revision support does not displace external stacks

| Field | Content |
|---|---|
| **Identifier** | PP-005 |
| **Journey stage** | Revision · weak-topic return |
| **Severity** | **High** |
| **Evidence** | K7=58; blind near-universal stack retention; SV-006 late-crunch; REM-11 open; RC-10 |
| **Likely KSI impact** | **+1.0 to +2.0** (K7) |
| **Root cause** | RC-10 |
| **Related decisions** | Blueprint revision scope |
| **Related risks** | PR-002 (portfolio) |
| **Student experience** | “For revision I still open Anki / past papers / notes first.” |
| **Failure modes** | Trust loss · motivation loss · dead ends |
| **Potential solutions** | IMP-06 weak-topic / spaced return inspectability |

---

### PP-006 — Cold-start readiness / MES thin or absent

| Field | Content |
|---|---|
| **Identifier** | PP-006 |
| **Journey stage** | First login · early Home · readiness |
| **Severity** | **Medium–High** |
| **Evidence** | PERC-02; RDY-PERC-01; RC-12; PR-005; PR-017 sparse onboarding |
| **Likely KSI impact** | **+0.5 to +1.2** (K3/K8/K5) |
| **Root cause** | RC-12 |
| **Related decisions** | Honesty / unknown-as-unknown law |
| **Related risks** | PR-005, PR-017 |
| **Student experience** | “New account → empty intelligence theatre or silence.” |
| **Failure modes** | Confusion · trust loss · educational uncertainty |
| **Potential solutions** | IMP-07 honest cold-start copy + onboarding orientation |

---

### PP-007 — “On Track” / calm chrome can soothe without inspectability

| Field | Content |
|---|---|
| **Identifier** | PP-007 |
| **Journey stage** | Home readiness |
| **Severity** | **Medium** |
| **Evidence** | RDY-PERC-02; PA-018 Supported; SV-013 class overconfidence risk |
| **Likely KSI impact** | **+0.3 to +0.8** (K3/K8 integrity) |
| **Root cause** | RC-04 residual |
| **Related decisions** | Exam Ready blocked (correct) |
| **Related risks** | PR-005 |
| **Student experience** | “Green language without drivers feels like false precision.” |
| **Failure modes** | Trust loss · educational uncertainty |
| **Potential solutions** | Prefer provisional + drivers; reduce soothing-without-evidence chrome |

---

### PP-008 — Protective motivation without restorative restart

| Field | Content |
|---|---|
| **Identifier** | PP-008 |
| **Journey stage** | Post-miss · post-fail · return after gap |
| **Severity** | **Medium** |
| **Evidence** | K5=63; RC-08; REM-09; PA-039 Hypothesis (perception→behaviour) |
| **Likely KSI impact** | **+0.5 to +1.5** (K5/K1) |
| **Root cause** | RC-08 |
| **Related decisions** | Never-Build gamification constraints |
| **Related risks** | — |
| **Student experience** | “After I miss days, I am not sure how to restart in a way that counts.” |
| **Failure modes** | Motivation loss · friction |
| **Potential solutions** | IMP-08 smaller restart that counts; explicit post-fail adaptation narrative |

---

### PP-009 — Sparse-content / thin session nights

| Field | Content |
|---|---|
| **Identifier** | PP-009 |
| **Journey stage** | Session overview · study |
| **Severity** | **Medium** |
| **Evidence** | JRN-PERC-02; historical thin overview (SV-003); K1 prefer-lower cap |
| **Likely KSI impact** | **+0.3 to +0.9** (K1/K5) |
| **Root cause** | RC-11 adjacent / content thinness |
| **Related decisions** | — |
| **Related risks** | — |
| **Student experience** | “Tonight’s session looks like a template with missing fields.” |
| **Failure modes** | Confusion · cognitive overload · motivation loss |
| **Potential solutions** | Honest sparse-state UX; content completeness on primary path |

---

### PP-010 — Topic selection quality unproven (coherence ≠ best topic)

| Field | Content |
|---|---|
| **Identifier** | PP-010 |
| **Journey stage** | Planning · Mission · Recommendation |
| **Severity** | **Medium** |
| **Evidence** | K1=72 clears path friction but not topic excellence; PA-014; no precision sample |
| **Likely KSI impact** | **+0.5 to +1.5** (K1/K2) if precision defects found and fixed |
| **Root cause** | RC-11 |
| **Related decisions** | DR-052 |
| **Related risks** | PR-001 |
| **Student experience** | “The plan is clear, but is this *the* highest-value topic?” |
| **Failure modes** | Educational uncertainty |
| **Potential solutions** | Claim-window precision sample; fix only evidenced defects — no new brain by default |

---

### PP-011 — Dual-home residual outside W-PROD (Alpha / dual-run)

| Field | Content |
|---|---|
| **Identifier** | PP-011 |
| **Journey stage** | Entry (non–sole-runtime) |
| **Severity** | **Low for W-PROD claim** · **Medium if SOLE_RUNTIME off** |
| **Evidence** | JRN-PERC-01; EP-007.2 residual; maturity Runtime A outstanding work |
| **Likely KSI impact** | **0 in W-PROD** if sole-runtime held; regression risk if flag off |
| **Root cause** | RC-02 residual |
| **Related decisions** | Sole-runtime production claim window |
| **Related risks** | Claim honesty if environments mix |
| **Student experience** | Two directors (only when dual-run enabled). |
| **Failure modes** | Confusion · friction · trust loss |
| **Potential solutions** | Keep W-PROD sole-runtime; legacy redirect shells; do not reopen as P0 product work |

---

### PP-012 — Duration mismatch residual outside W-PROD

| Field | Content |
|---|---|
| **Identifier** | PP-012 |
| **Journey stage** | Home / Session (non–sole-runtime) |
| **Severity** | **Low for W-PROD** |
| **Evidence** | Universal theme historically; cleared EP-007.2 on sole-runtime |
| **Likely KSI impact** | **0** if integrity held |
| **Root cause** | RC-03 residual |
| **Related decisions** | — |
| **Related risks** | Regression in dual-run |
| **Student experience** | 30 vs 90 distrust (historical). |
| **Failure modes** | Friction · trust loss |
| **Potential solutions** | Regression tests / smoke; not a new feature programme |

---

### PP-013 — Students retain external materials (stack substitution unearned)

| Field | Content |
|---|---|
| **Identifier** | PP-013 |
| **Journey stage** | Cross-cutting |
| **Severity** | **Medium** (positioning) |
| **Evidence** | Near-universal blind theme; product best as workflow director beside CMP/papers |
| **Likely KSI impact** | Indirect — improves when K2/K7/K4 rise |
| **Root cause** | Composite of PP-001, PP-005, PP-003 |
| **Related decisions** | EP-004 strategy identity |
| **Related risks** | Overclaim as adaptive tutor |
| **Student experience** | “Kwalitec did not earn a deletion in my stack.” |
| **Failure modes** | Trust loss · motivation loss |
| **Potential solutions** | Earn revision + recommendation trust; do not claim stack replacement prematurely |

---

### PP-014 — G1.7 independent re-score unfinished (process pain for Board)

| Field | Content |
|---|---|
| **Identifier** | PP-014 |
| **Journey stage** | N/A (governance) |
| **Severity** | **Medium (declaration process)** |
| **Evidence** | PR-009; GAP-05; REM-12 |
| **Likely KSI impact** | **0** educational; required for declaration hygiene |
| **Root cause** | RC-13 |
| **Related decisions** | PSF §5.5 |
| **Related risks** | PR-009 |
| **Student experience** | None directly |
| **Failure modes** | Board confidence |
| **Potential solutions** | IMP-09 second-assessor formality before declaration board |

---

## 3. Journey-stage heat map

| Stage | Dominant pain IDs | Primary failure modes | Posture |
|---|---|---|---|
| First login | PP-006, PP-007 | Confusion, trust loss | Residual after MES/readiness |
| Home | PP-001, PP-003, PP-007 | Uncertainty, trust | Primary CTA exists; trust Partial |
| Mission / Planning | PP-010, PP-003 | Uncertainty | Path clear (K1=72); quality unproven |
| Study | PP-009 | Friction, overload | Thin nights residual |
| Analytics | PP-004 | Dead ends, uncertainty | Floor K6 |
| Completion | (legacy strength) | — | Honest close valued |
| Reflection | PP-008 | Motivation | Restorative gap |
| Revision | PP-005, PP-013 | Dead ends, stack retention | K7 lag |
| Cross-cutting | PP-002 | Trust / effectiveness | G1.9 FAIL |

---

## 4. Closed pains (do not re-prioritise as Critical on W-PROD)

| Former theme | Closed by | Residual ID if any |
|---|---|---|
| Invisible MES / Coach without working | EP-006.2/006.3 | PP-006, PP-001 (trust remainder) |
| Empty Home readiness drivers | EP-006.4/006.5 | PP-006, PP-007 |
| Dual homes on production | EP-007.1/007.2 | PP-011 (non–W-PROD) |
| 30-vs-90 duration on production | EP-007.1/007.2 | PP-012 (non–W-PROD) |

---

## 5. Pain → improvement crosswalk

| Pain | Primary improvement |
|---|---|
| PP-001 | IMP-01, IMP-02 |
| PP-002 | IMP-03 |
| PP-003 | IMP-04 |
| PP-004 | IMP-05 |
| PP-005 | IMP-06 |
| PP-006 | IMP-07 |
| PP-007 | IMP-07 (honesty), readiness spot-check |
| PP-008 | IMP-08 |
| PP-009 | IMP-10 (sparse-state) |
| PP-010 | IMP-01 / precision sample (conditional) |
| PP-011/012 | Hold sole-runtime; regression only |
| PP-013 | Consequence of IMP-01/04/06 |
| PP-014 | IMP-09 |

Improvement definitions: [`HIGH_LEVERAGE_IMPROVEMENTS.md`](HIGH_LEVERAGE_IMPROVEMENTS.md).

---

**End of STUDENT_PAIN_POINTS**
