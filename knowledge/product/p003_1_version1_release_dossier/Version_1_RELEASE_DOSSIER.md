# Version 1 Release Dossier

**Programme:** P-003.1 — Version 1 Release Dossier  
**Document:** Primary Product Board reference  
**Date:** 2026-07-26  
**Status:** Complete — evidence synthesis only  
**Does not:** Change runtime, educational algorithms, UI, or declare Version 1 production-ready  

**Evidence standard:** Every conclusion cites existing artefacts. Missing evidence is labelled **Evidence currently unavailable.** Estimated ΔKSI is never treated as validated Gate G1 input.

Companion briefs: [`Executive_Summary.md`](Executive_Summary.md) · [`Release_Timeline.md`](Release_Timeline.md) · [`Architecture_Summary.md`](Architecture_Summary.md) · [`Evidence_Summary.md`](Evidence_Summary.md) · [`KSI_Evolution.md`](KSI_Evolution.md) · [`Release_Gates.md`](Release_Gates.md) · [`Risk_Summary.md`](Risk_Summary.md) · [`Version1_State.md`](Version1_State.md)

---

# 1 Executive Summary

Kwalitec is a commercial adaptive learning product for professional-exam candidates. Vision 2030 defines the north star as materially higher exam pass probability for consistent users, expressed daily as: *what is the highest-value thing this student should do next?* Educational philosophy measures learning over activity; AI must be explainable and evidence-based; absence of evidence remains unknown.

**Target users:** Primary — students preparing for IFoA, SOA, CAA, CAS and related qualifications. Secondary — training providers and employers. Public registration is not exposed.

**Runtime A** is the student Education OS path (Home → Session → review). Under production defaults, legacy Runtime A services own student-visible educational authority; Twin cutover flags default OFF. Recommendation, Planning, and Readiness services are the educational authorities; presentation delivers explanations without inventing evaluation.

**Current release status:** Validated KSI **62** (target ≥ 80). Gate **G1 FAIL** (G1.1 and G1.9 blocking; G1.5 PASS at K8 **70**). Educational effectiveness **NO-GO / PENDING EVIDENCE** (external N = 0). Private beta execution **GO WITH CONDITIONS**. Version 1 production-ready declaration is **not permitted**.

Full two-page brief: [`Executive_Summary.md`](Executive_Summary.md).

---

# 2 Programme History

Board-level outcomes only. Implementation detail lives in programme folders. Chronological narrative: [`Release_Timeline.md`](Release_Timeline.md).

### Foundation (pre–P-001; context for Runtime A)

| Programme | Objective | Key deliverables | Evidence | Outcome | Release impact |
|---|---|---|---|---|---|
| **Architecture consolidation / Education OS** | One student runtime | Sole runtime navigation; ADRs; System Architecture | `ARCHITECTURE.md`; `VERSION_1_READINESS` Architecture COMPLETE | Complete | Operational prerequisite; insufficient for V1 declaration |
| **EP-001 Product Validation** | Educational validation + analytics design | Outcome catalogue; recommendation validation framework; V1 exit criteria | `knowledge/product/ep001_product_validation/` | Framework complete; marketing freeze retained | Feeds G1.9 / claim honesty |
| **EP-001.* / EP-002.* Student Intelligence Surface** | Twin-gated consumer chain + presentation facade | Foundation → Planner → Readiness → Insight; dual-run/cutover; EP-002.9 baseline | `AUTHORITATIVE_ARCHITECTURE_BASELINE.md` | Complete; production defaults fail-open to legacy Runtime A | Defines Runtime A authority split; G12 flag discipline |
| **Analytics EP-002** | Operational analytics readiness | Instrumentation; privacy; go-live checklist | `knowledge/product/analytics/ep002/` | COMPLETE (flag OFF) | G9 posture: ops ready, Journey emit deferred |

### P-001 — Product success law

| Programme | Objective | Key deliverables | Evidence | Outcome | Release impact |
|---|---|---|---|---|---|
| **P-001.1** | Measure educational usefulness | Product Success Framework; baseline KSI **58**; SIA mandate | `p001_1_ksi_baseline/` | Complete (docs) | Defines V1 usefulness bar KSI ≥ 80 → Gate G1 |
| **P-001.2** | Explainability law | Standard, patterns, review checklist | `p001_2_explainability_standard/` | Complete (docs) | Enables G3 / V1-K3 (K8 ≥ 70) |
| **P-001.3** | Recommendation quality law | Standard, decision framework, scorecard, checklist | `p001_3_recommendation_quality_standard/` | Complete (docs) | Enables G4 / K2 floor |

### P-002 — Release declaration law

| Programme | Objective | Key deliverables | Evidence | Outcome | Release impact |
|---|---|---|---|---|---|
| **P-002.1** | Define when V1 may be declared production-ready | Gates G1–G12; evidence requirements; go/no-go guide | `p002_1_version_1_release_framework/` | Complete (docs); no declaration made | Binding declaration authority |

### EP-003 — Quality contracts + effectiveness framework

| Programme | Objective | Key deliverables | Evidence | Outcome | Release impact |
|---|---|---|---|---|---|
| **EP-003** (umbrella) | Educational effectiveness validation framework | Metrics M1–M9; beta protocol; scorecard; Go/No-Go | `ep003_educational_effectiveness/` | Framework COMPLETE; effectiveness **PENDING EVIDENCE** | G1.9 input = NO-GO for effectiveness claims |
| **EP-003.1** | Recommendation quality contract in Runtime A | Schema-complete recommendations; Decision Framework | Tests + Explainability/Recommendation reviews Pass | Complete | Structural G3/G4 input |
| **EP-003.2** | Readiness explainability contract | Drivers, confidence, next action | Tests + Explainability Pass | Complete | Structural G6 input |
| **EP-003.3** | Planning quality contract | Schema-complete plans; duration honesty | Tests + Explainability Pass | Complete | Structural G5 input |
| **EP-003.4** | Learning feedback (record-only) | Observed behavioural evidence; flag OFF default | Adapter tests | Complete; **unsupported in W-PROD** while OFF | No validated K4/K6 lift in production defaults |

### EP-004 — Personalisation + private beta

| Programme | Objective | Key deliverables | Evidence | Outcome | Release impact |
|---|---|---|---|---|---|
| **EP-004** (umbrella) | Controlled private beta | Cohort, rollout, scorecards, Go/No-Go | `ep004_private_beta/GO_NO_GO_DECISION.md` | **GO WITH CONDITIONS**; Stage 1–2 HOLD on privacy | Allows Stage 0; blocks effectiveness GO until C5–C6 |
| **EP-004.1** | Personal Learning Profile | Behavioural profile; no educational authority; flag OFF | Profile tests | Complete; W-PROD unsupported while OFF | G12 gated |
| **EP-004.2** | Recommendation personalisation | Bounded profile influence; flag OFF | Reviews Pass | Complete; W-PROD unsupported while OFF | G12 gated |
| **EP-004.3** | Planning personalisation | Bounded pacing; flag OFF | Reviews Pass | Complete; W-PROD unsupported while OFF | G12 gated |

### EP-005 — Validation honesty

| Programme | Objective | Key deliverables | Evidence | Outcome | Release impact |
|---|---|---|---|---|---|
| **EP-005.1** | Validate estimated ΔKSI against G1 | Validated board; G1 status; evidence register | `VALIDATED_KSI_REPORT.md` | Validated KSI **59**; **G1 FAIL** | Established that estimate stacks are not claimable |
| **EP-005.2** | Root-cause why KSI remains low | Gap analysis; REM-01…12 remediation plan | `PRIORITISED_REMEDIATION_PLAN.md` | Complete (docs) | Drove EP-006 / EP-007 remediation sequence |

### EP-006 — MES + readiness experience

| Programme | Objective | Key deliverables | Evidence | Outcome | Release impact |
|---|---|---|---|---|---|
| **EP-006.1** | Audit MES field loss; design K8 path | Delivery specification; K8 remediation plan | Docs | Complete (design) | Unblocked G1.5 critical path |
| **EP-006.2** | Deliver MES to Home/Coach/Mission | Presentation pass-through | Contract tests; Explainability Pass | Complete | Ready for Tier B |
| **EP-006.3** | Tier B MES perception (N=9) | Perception report; K8 revalidation | `G1_5_STATUS.md` | **K8 = 70**; **G1.5 PASS**; KSI **60** | Cleared explainability floor criterion |
| **EP-006.4** | Home readiness experience | Drivers / confidence / review / next | Delivery tests | Complete | Ready for Tier B |
| **EP-006.5** | Tier B readiness perception (N=9) | K3 revalidation | `G1_READINESS_STATUS.md` | **K3 = 65**; KSI **61** | G1 still FAIL |

### EP-007 — Journey + effectiveness Stage 1

| Programme | Objective | Key deliverables | Evidence | Outcome | Release impact |
|---|---|---|---|---|---|
| **EP-007.1** | Single Home; one duration fact | Journey consolidation (REM-02/03) | Journey tests | Complete | Cleared dual-home / duration residual on W-PROD |
| **EP-007.2** | Tier B journey perception (N=9) | K1 revalidation | `K1_REVALIDATION.md` | **K1 = 72**; **KSI = 62** | Latest validated board; G1 still FAIL |
| **EP-007.3** | Stage 1 effectiveness design + assessment | Cohort design; G1.9 status | `G1_9_STATUS.md` | Design complete; ops blocked; **G1.9 FAIL**; ΔKSI **0** | Reaffirmed effectiveness NO-GO |

### P-003.1 — This dossier

| Programme | Objective | Key deliverables | Evidence | Outcome | Release impact |
|---|---|---|---|---|---|
| **P-003.1** | Board release dossier | This package | All cited paths | Complete (docs); ΔKSI **0** | Primary reference for future release decisions |

---

# 3 Architecture Summary

Board language only. Detail: [`Architecture_Summary.md`](Architecture_Summary.md).

**Runtime A** is the student-facing Education OS. Production defaults keep Twin/Authority/Cutover flags **OFF**; legacy Runtime A services remain fail-open student-visible authority. Production hard-gates block HTTP cutovers in `production` / `prod` regardless of flag values.

| Authority | Owns | Must not |
|---|---|---|
| **Recommendation** | Next-action guidance / MES | Invent readiness or plans |
| **Planning** | Today’s mission / daily plan / ORM mission persistence | Compete with a second planner |
| **Readiness** | Readiness estimate, drivers, confidence honesty | Exam Ready marketing without gates |
| **Presentation** | Deliver authored explanations; journey chrome | Invent evaluation or planning |
| **Curriculum Engine** | Syllabus structure / ordering | Be duplicated in cutover/presentation |
| **Twin / consumer chain** (gated) | Read models / dual-run / cutover orchestration | Write educational state; replace Runtime A writes |

**Educational ownership:** EGI Educational Constitution owns lawful educational meaning. EVF owns whether educational quality is sufficient to release. Product Success Framework owns usefulness measurement (KSI). P-002.1 owns production-ready declaration gates.

**Boundaries:** One Education OS runtime; no second educational brain in production defaults; curriculum V1 and V2 remain loadable.

---

# 4 Student Journey

Canonical W-PROD sole-runtime journey (EP-007.1):

```
Login
  ↓
(no plan) Study Plan wizard → Calibration (optional)
  ↓
Student Home
  ↓
Start / Resume Mission (Study Session)
  ↓
Overview → Activity → Reflection → Summary → Complete
  ↓
Student Home (Review / readiness / tomorrow’s next action)
```

| Stage | Student need | Runtime A support |
|---|---|---|
| **Login** | Reach one home | Canonical home routing when sole runtime ON |
| **Home** | Know what to do tonight and for how long | Planning mission + recommendation MES + readiness block; one duration fact |
| **Mission** | Start the right session | Planning-owned mission; Home CTA |
| **Study** | Execute with feedback | Session surfaces; learning feedback record-only when flag ON (default OFF) |
| **Review** | Understand outcome and readiness | Session summary; readiness drivers / confidence / next (EP-006.4) |
| **Tomorrow** | Continue without dual-home confusion | Return to single Student Home; continue/resume path |

Dual-home / conflicting duration themes were cleared on W-PROD perception packs (EP-007.2). Dual-run Alpha residual may still present dual-home outside W-PROD sole-runtime claim window — evidence: EP-007.2 prefer-lower notes.

---

# 5 Educational Evidence

Detail: [`Evidence_Summary.md`](Evidence_Summary.md).

| Validation programme | What was measured | What changed | Confidence | Educational impact | Outstanding |
|---|---|---|---|---|---|
| **EP-001** | Validation frameworks / outcomes | Design + freeze rules | Framework only | Claim discipline | Pass-rate methodology open |
| **EP-003** | M1–M9 definition; Q1–Q5 | Framework PASS; claims OPEN | N/A until cohort | No effectiveness claim | G5/G7/G8 OPEN |
| **EP-004 Stage 0** | Ops health; exploratory scorecard | Execution GO WITH CONDITIONS | External N=0 | No effectiveness claim | Privacy C1; C5–C6 |
| **EP-004 blind reviews** | Student-only qualitative corpus | Themes for KSI / remediation | Medium (persona pack) | Trust / workflow themes | Not Stage 1 interviews |
| **EP-005.1** | Validated vs estimated KSI | KSI **59**; estimate stacks rejected | Medium | Honesty of G1 | G1 FAIL |
| **EP-005.2** | Experience root causes | REM backlog | High on themes | Drove remediation | Does not raise KSI alone |
| **EP-006.3 Tier B** | MES perception | K8 **70**; KSI **60**; G1.5 PASS | Medium | Explainability floor met | External N=0 |
| **EP-006.5 Tier B** | Readiness perception | K3 **65**; KSI **61** | Medium | Unpackability improved | G1.1/G1.9 open |
| **EP-007.2 Tier B** | Journey perception | K1 **72**; KSI **62** | Medium | Single Home validated on W-PROD | Gap 18 to ≥80 |
| **EP-007.3** | Effectiveness Stage 1 posture | Design frozen; ops blocked | High on *absence* | Effectiveness still NO-GO | Privacy; invites; M1–M9 |

**Outstanding questions (evidence currently unavailable for answers):** Does Kwalitec measurably improve learning outcomes in an external cohort? What is exam pass-rate lift (north star)? Are personalisation flags educationally useful when ON in production defaults?

---

# 6 KSI Evolution

Detail: [`KSI_Evolution.md`](KSI_Evolution.md).

```
Estimated baseline (P-001.1)     58
        ↓  EP-005.1 validation (W-PROD)
Validated baseline               59
        ↓  EP-006.3 MES perception
Validated (K8 cleared)           60
        ↓  EP-006.5 readiness perception
Validated                        61
        ↓  EP-007.2 journey perception
Current validated KSI            62
```

| Step | Why it moved | What did *not* move |
|---|---|---|
| 58 → 59 | First validated board; structural EP-003.1–.3 credit under prefer-lower; gated EP-003.4/004.* Δ rejected | Naive ~+12 estimate stack |
| 59 → 60 | K8 65→70 after MES delivery + Tier B | G1.1; G1.9 |
| 60 → 61 | K3 →65 after readiness experience + Tier B | KSI ≥80 |
| 61 → 62 | K1 68→72; K5 60→63 after single Home + Tier B | Effectiveness; personalisation ON |

**Target:** ≥ 80. **Gap:** 18. **Do not invent** category scores beyond published boards.

Latest board (EP-007.2): K1 **72**, K2 **55**, K3 **65**, K4 **55**, K5 **63**, K6 **50**, K7 **58**, K8 **70** → KSI **62**.

---

# 7 Release Gates

Detail: [`Release_Gates.md`](Release_Gates.md). Authority: P-002.1.

| Gate | Status | Board note |
|---|---|---|
| **G1 Validated KSI** | **FAIL** | Blocking: G1.1 (62&lt;80), G1.9 (effectiveness NO-GO); G1.5 PASS; G1.7 HOLD |
| **G2 Constitutional** | **IN PROGRESS** / incomplete board | Architecture COMPLETE; EVF educational outcome not APPROVED for V1 claim class — Evidence currently unavailable for full G2 declaration pack |
| **G3 Explainability** | Partially met | EP-003 checklists Pass; G1.5 PASS; full spot-check pack for declaration — incomplete |
| **G4 Recommendation Quality** | Partially met | EP-003.1 checklist Pass; scorecard instrumentation gaps |
| **G5 Planning Quality** | Partially met | EP-003.3 tests green; K1 72; full smoke pack for declaration — incomplete |
| **G6 Readiness Quality** | Partially met | EP-003.2 tests green; K3 65; honesty path verified in programmes |
| **G7 Performance** | IN PROGRESS | CI soft budgets green; production load test NOT STARTED |
| **G8 Reliability** | IN PROGRESS | Health/smoke pass; production load residual open |
| **G9 Telemetry** | COMPLETE (flag OFF) | Ops ready; Journey emit deferred; no overclaim of live metrics |
| **G10 Security** | IN PROGRESS | GA review pass; CSP residual; Stage 1 privacy signatures open |
| **G11 Tests** | IN PROGRESS | Broad suite; continuous green required for tag |
| **G12 Flag readiness** | Not scored as declaration board | Matrix discipline required; personalisation OFF in W-PROD |

**Board recommendation on gates:** Do not declare until G1 PASS (or approved HOLD path that does not overclaim) and remaining hard gates PASS or HOLD under P-002.1 rules.

---

# 8 Release Risks

Detail: [`Risk_Summary.md`](Risk_Summary.md). Engineering defects are out of scope unless they create release risk.

| ID | Risk | Severity | Evidence | Mitigation posture |
|---|---|---|---|---|
| R1 | Educational effectiveness unproven | Critical | EP-003/007.3 NO-GO; N_external=0 | Stage 1 ops after privacy; refuse effectiveness marketing |
| R2 | KSI gap to ≥80 (18 pts) | Critical | EP-007.2 board | Continue evidence-driven remediation; no estimate stacking |
| R3 | Privacy / Stage 1 expansion blocked | High | PRIVACY_REVIEW unsigned | Complete checklist signatures before invites |
| R4 | Premature production-ready claim | Critical | G1 FAIL; incomplete package | This dossier + P-002.1 NO-GO discipline |
| R5 | Personalisation flags marketed while OFF | High | EP-005.1 unsupported Δ | G12 matrix; claim language excludes OFF flags |
| R6 | Cold-start / sparse evidence honesty | Medium | Prefer-lower scores; readiness refusal path | Keep unknown-as-unknown; no Exam Ready theatre |
| R7 | External evidence / interview floor unmet | High | C5–C6; EP-007.3 | Meet N/duration/interview floors or written waiver |
| R8 | Operational load / production sampling open | Medium | VERSION_1_READINESS G7/G8 | HOLD or complete before high-traffic claims |
| R9 | Rollback / flag kill-switch readiness | Medium | Architecture rollback model exists; declaration G12 unscored | Publish V1 flag matrix before ON defaults |
| R10 | Commercial / support not ready | Medium | Commercial NOT STARTED; founder-operated support | Keep invite-only; no public launch |

---

# 9 Lessons Learned

### Validated assumptions

- Quality contracts in Runtime A (EP-003.1–.3) can raise structural explainability/planning/readiness floors — but only when student-visible delivery exists (EP-006).  
- Estimated ΔKSI stacks overstate claimable usefulness (EP-005.1).  
- Presentation pass-through of MES is necessary for K8 (EP-006.1–.3).  
- Dual-home / duration conflict is a real student-value blocker; consolidation moves K1/K5 (EP-007.1–.2).  
- Perception (Tier B) ≠ educational effectiveness (EP-007.3 correctly refused substitution).

### Rejected assumptions

- “Ship quality contracts → claim KSI ≥ 80.” Rejected by EP-005.1.  
- “Gated personalisation Δ counts in W-PROD while flags OFF.” Rejected.  
- “Tier B N=9 clears G1.9.” Rejected.  
- “Operational GA / architecture cutover = Version 1 production-ready.” Rejected by P-002.1.

### Unexpected discoveries

- MES authored in services was not reaching Home/Coach — field loss, not missing algorithms (EP-006.1).  
- Prefer-lower discipline kept K8 at exactly 70 (floor) despite delivery success.  
- Stage 1 design can complete while ops remain fully blocked on privacy signatures.

### Educational insights

- Students need one coherent tonight plan and visible *why + next*.  
- Readiness must unpack (drivers, confidence, review) or trust stalls.  
- Honesty about unknown evidence protects Final Test more than soothing composites.

### Governance insights

- Separate: private-beta GO WITH CONDITIONS vs educational effectiveness GO vs Version 1 production-ready declaration.  
- Gate G1 requires validated KSI + effectiveness non-NO-GO — not programme optimism.  
- Docs-only programmes correctly record ΔKSI = 0.

### Architecture insights

- One runtime + fail-open legacy under production defaults protects students during Twin soak.  
- Presentation must not become a third narrator.  
- Flag OFF capabilities must not be marketed as live.

---

# 10 Version 2 Guidance

**This section is not a Version 2 roadmap.** It records evidence posture for future research only.

### Supported by evidence (keep)

- Curriculum-first deterministic Runtime A authorities.  
- Mandatory explainability schema and recommendation decision ladder on production defaults.  
- Single canonical Home / duration fact.  
- Student-visible MES delivery on daily path.  
- Validated KSI methodology + prefer-lower honesty.  
- Separation of Twin cutover from legacy fail-open.

### Remain hypotheses (unproven)

- Personalisation flags ON improve K4/K1/K2 in live cohorts.  
- Learning feedback + profile loops improve long-term adaptation.  
- Twin cutover ON as production default improves student outcomes vs legacy.  
- M1–M9 will show measurable educational improvement at C5 floors.  
- Exam pass-rate lift for consistent users (north star) — **Evidence currently unavailable.**

### Require more research

- Pass-rate measurement methodology (EP-001 O9 open).  
- Strong-band K2 with instrumented acceptance KPIs.  
- Revision workspace usefulness (K7) at scale.  
- Decision-grade analytics that avoid vanity (K6).  
- Multi-country privacy / DPA posture for 2030 vision (noted open in Privacy Review).

---

# 11 Board Recommendation

# NO GO

### Evidence supporting NO GO (P-002.1)

1. **Hard Gate G1 FAIL** — Validated KSI **62** &lt; **80** (G1.1 FAIL). Sources: EP-007.2 `K1_REVALIDATION.md`; EP-007.3 `G1_9_STATUS.md`.  
2. **Hard Gate G1.9 FAIL** — Educational effectiveness remains **NO-GO / PENDING EVIDENCE**; external N = **0**; Privacy Review unsigned. Sources: EP-003 `GO_NO_GO_REPORT.md`; EP-004 `GO_NO_GO_DECISION.md`; EP-007.3 `G1_9_STATUS.md`.  
3. **Incomplete Version 1 Evidence Package** — G1 slice exists; full G2–G12 declaration package not assembled. Source: P-002.1 evidence folder; `VERSION_1_READINESS.md`.  
4. **P-002.1 decision rule** — Any hard-gate FAIL → overall **NO-GO**. Validated KSI &lt; 80 → **NO-GO**.

### What NO GO allows

- Continue Stage 0 private beta under EP-004 **GO WITH CONDITIONS**.  
- Continue remediation and evidence collection toward G1.1 / G1.9.  
- Maintain claim freezes (recommendation-effectiveness marketing; Exam Ready; public launch).

### What NO GO forbids

- Declaring “Kwalitec Version 1 is production-ready.”  
- Public registration / marketing launch.  
- Claiming measurable educational effectiveness or exam pass-rate lift from current evidence.

### Minimum path before a future declaration board (not a commitment to GO)

1. Privacy Review signed → Stage 1 cohort ops → M1–M9 + interviews → effectiveness verdict update (G1.9).  
2. Further validated KSI movement to ≥ 80 with Medium/High confidence (G1.1) + G1.7 formality.  
3. Assemble complete G1–G12 Evidence Package and signed go/no-go under P-002.1.

Until those conditions are evidenced, the Product Board recommendation remains **NO GO**.

---

**End of Version 1 Release Dossier**
