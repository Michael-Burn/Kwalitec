# KSI-002 — Study Design

**Programme:** KSI-002 — Educational Effectiveness Validation Protocol  
**Version:** 1.0  
**Status:** PROTOCOL COMPLETE — AWAITING FOUNDER REVIEW  
**Effective:** 2026-08-04  
**Authority:** `KSI002_VALIDATION_PROTOCOL.md` · EP-007.3 `COHORT_DESIGN.md` · `PRIVATE_BETA_PROTOCOL.md` · `EDUCATIONAL_METRICS.md`  

**Defines design rules only.** Does not enroll participants or collect data.

---

## 1. Design classification (binding)

Future educational-effectiveness validation for Gate G1 **must** use the following design class unless Founder amends this document:

| Dimension | Chosen value | Not chosen |
|-----------|--------------|------------|
| Population locus | **Mixed** — internal Stage 0 / Tier B allowed as *supporting*; **external** Stage 1+ required for G1.9 | Purely internal alone |
| Timing | **Prospective** observation from personal start date | Pure retrospective mining of convenience logs as sole evidence |
| Temporal structure | **Longitudinal** (≥ minimum study length with repeated measures) | Cross-sectional snapshot alone for effectiveness GO |
| Assignment | **Observational cohort** (invite-only; no recommendation A/B) | Randomised recommendation-effectiveness trial (out of scope; separate PRD) |

### 1.1 Why this design is appropriate

1. **External** participants are required because internal dogfood and Tier B perception cannot clear G1.9 (KSI-001 EG-02; EP-007.3).  
2. **Prospective** start dating prevents post-hoc window shopping for favourable weeks.  
3. **Longitudinal** measurement matches the construct *sustained* study behaviour (M6, M7, usefulness over weeks) — a cross-section cannot distinguish novelty from habit.  
4. **Mixed** supporting evidence (Tier B, Stage 0) remains useful for Partial-band and defect detection but is ranked below external longitudinal packs (`KSI002_EVIDENCE_ACCEPTANCE_CRITERIA.md`).  
5. **Observational** (not interventional ranking trials) preserves the recommendation-marketing freeze and avoids confounding product change with measurement.

### 1.2 Allowed nested sub-designs

| Sub-design | When allowed | Ceiling |
|------------|--------------|---------|
| Cross-sectional Tier B perception | Surface trust / unpackability | Partial or Strong-floor with Medium confidence; not G1.9 alone |
| Retrospective audit of already-collected protocol-compliant events | After prospective registry exists | May fill missing cells if collection rules were pre-specified |
| Controlled flag-ON dogfood (W-GATED) | Founder-authorised; separate claim window | Cannot silently merge into W-PROD validated board |

---

## 2. Stages

| Stage | Purpose | External N role |
|-------|---------|-----------------|
| **Stage 0** | Internal / Founder dogfood; operability | Does **not** count toward external N |
| **Tier B** | Structured perception packs | Supporting usefulness; not effectiveness GO |
| **Stage 1** | Small external pilot — claimability / directional effectiveness | Design minimum for ops advance |
| **Stage 2** | Larger external cohort — product-decision / effectiveness GO path | Preferred for G1.9 PASS without waiver |
| **Revalidation** | Fresh package within validity window | Required before declaration if prior package aged out |

---

## 3. Duration

| Parameter | Value | Rationale |
|-----------|------:|-----------|
| **Minimum study length** (directional / Stage 1 ops advance) | **4 weeks** from personal start for each counted participant | EP-007.3; enough for rolling consistency |
| **Recommended length** (effectiveness GO path) | **6–8 weeks** | Stabilises M6/M7; reduces novelty bias |
| **Absolute minimum for any effectiveness claim language** | **2 weeks** only for *directional internal memos* — **forbidden** for G1.9 PASS | Protects against novelty theatre |
| **Maximum validity window** of a completed evidence package | **90 days** from assessment publish date | G1.3 / PSF §5.4 |
| **Revalidation interval** | Re-run full validated KSI + effectiveness board before any Version 1 declaration if package &gt;90 days; otherwise on material claim-window change (flags, runtime, major surface) | Honesty |

Personal start = date of invite **acceptance** (not invite send).

---

## 4. Sample size (design targets)

Detailed inclusion/exclusion: `KSI002_PARTICIPANT_PROTOCOL.md`.

| Parameter | Value |
|-----------|------:|
| Stage 1 **minimum** accepted external | **5** |
| Stage 1 **target** | **5–10** |
| Stage 2 / product-decision **floor** for G1.9 without waiver | **20** active (≥4 weeks) |
| **Maximum** concurrent Stage 1+2 under this protocol version (ops capacity) | **50** invite-accepted (align Private Beta Protocol) |
| Interview minimum (GO path) | **≥8** completed structured interviews **or** **≥25%** of active participants, whichever is larger when N≥32 |

**Waiver:** Product + Educational written waiver may allow G1.9 CONDITIONAL with claim restrictions if N&lt;20 — never silent.

---

## 5. Primary and secondary endpoints

### 5.1 Primary (effectiveness — RQ-E)

1. Rolling study consistency (M6) over available weeks.  
2. Session completion rate (M4) with abandon reported.  
3. Educational usefulness over time (structured interview Final Test codes).  
4. Perceived multi-week preparedness (interview; not single-session unpackability alone).

### 5.2 Secondary

- M1 WAL retention among accepted  
- M2 sessions per WAL  
- M3 reflection completion  
- M5 progress velocity (**provisional** until Journey emit policy matches claim window)  
- M7 continuity  
- M8/M9 as defined in Educational Metrics (interpret with exam-date caution)  
- Observational recommendation acceptance / deferral / completion reflection / follow-through  
- Recovery / return-after-miss tallies  
- Time-to-next-session (exploratory)  
- Drop-off and abandonment rates  

### 5.3 Explicit non-endpoints

- Exam pass rate  
- Revenue / conversion  
- Premium craft scores  
- Progressive Confidence simulation means  
- Estimated programme ΔKSI  

---

## 6. Measurement cadence

| Cadence | Activity |
|---------|----------|
| Weekly | M1–M4, M6–M7 scorecard rows for active external participants |
| Bi-weekly | M5 (label provisional if required) |
| Window end | M8–M9; full effectiveness Q1–Q5 worksheet |
| Week 1 | Activation check-in |
| Week 2–3 | Consistency / reflection check-in |
| Week 4+ | Structured interview |
| Continuous | Defect / honesty incident log |

---

## 7. Blinding and independence

| Role | Rule |
|------|------|
| Metric computation | Prefer scripted / checklist computation from EVENT_CATALOGUE definitions; no ad-hoc redefinition mid-study |
| Category scoring | Assessor documents rationale; second assessor for G1.7 |
| Interview coding | Dual-coder when N_interviews ≥8 |
| Founder | May hold multiple capacities under GP-001 but **cannot** solely supply Strong-band evidence without second review |

---

## 8. Platform and interventions

| Rule | Spec |
|------|------|
| Platform | W-PROD sole-runtime defaults unless W-GATED study pre-registered |
| Product changes during window | Freeze educational behaviour changes for the claim window; emergency defect fixes allowed with honesty note |
| Recommendation ranking | **No change** under KSI-002 authority |
| Educational Framework / Packages / Curriculum | **No change** |
| Analytics flag | Follow Privacy Review + EP-002 pilot checklist; production default honesty preserved |

---

## 9. Analysis timing

1. Pre-register SAP version (`KSI002_STATISTICAL_ANALYSIS_PLAN.md`) before Stage 1 week-4 board.  
2. Lock inclusion set (accepted IDs) before primary endpoint computation.  
3. Publish effectiveness worksheet then KSI re-score — not the reverse (avoid score-first rationalisation).  

---

## 10. Design non-claims

This study design does **not** authorise execution, guarantee G1 PASS, or redefine PSF weights.

---

## 11. Exit

**STOP** for design acceptance with Founder review of the KSI-002 pack. No enrollment under this document alone without Privacy sign-off and Founder go.
