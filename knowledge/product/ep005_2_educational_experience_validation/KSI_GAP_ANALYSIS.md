# EP-005.2 — KSI Gap Analysis

**Programme:** EP-005.2 — Educational Experience Validation  
**Version:** 1.0  
**Date:** 2026-07-26  
**Status:** Evidence analysis (no runtime / UI / API changes)  
**Authority scores:** EP-005.1 Validated KSI **59** (W-PROD)  
**Target:** KSI ≥ **80** (Product Success Framework)  
**Gap:** **21** composite points  

---

## 1. Gap statement

> Architectural and quality-contract improvements from EP-003.1–.3 produced only **+1** validated composite KSI under production defaults. The remaining **21-point** gap to Version 1 is explained primarily by (a) incomplete student-visible explainability, (b) unresolved journey frictions that cap planning trust, (c) flag-OFF personalisation/feedback leaving K4/K6 flat, and (d) absence of Tier B perception and cohort evidence needed for Strong-band scores and Gate G1.9.

This is **not** a claim that engines are useless. It is a claim that **implemented capability ≠ validated educational value** until students can see, trust, and act on it.

---

## 2. Scoreboard (validated W-PROD)

| ID | Category | Weight | Validated | Band | Weighted | Points to Strong (70) | Points to Excellent contribution |
|---|---|---:|---:|---|---:|---:|---|
| K1 | Planning | 15 | 68 | Partial | 10.20 | +2 cat ≈ +0.3 KSI | Dual-home/duration first |
| K2 | Recommendation | 15 | 53 | Partial | 7.95 | +17 cat ≈ +2.6 KSI | Presentation + trust + acceptance |
| K3 | Readiness | 12 | 57 | Partial | 6.84 | +13 cat ≈ +1.6 KSI | Drivers + unpackability |
| K4 | Personalisation | 12 | 55 | Partial | 6.60 | +15 cat ≈ +1.8 KSI | Flag-ON + visible factors |
| K5 | Motivation | 10 | 60 | Partial | 6.00 | +10 cat ≈ +1.0 KSI | Restorative restart, not hype |
| K6 | Learning analytics | 10 | 50 | Partial | 5.00 | +20 cat ≈ +2.0 KSI | Decision-grade UX; feedback ON with honesty |
| K7 | Revision | 12 | 58 | Partial | 6.96 | +12 cat ≈ +1.4 KSI | Workspace usefulness; not random re-read |
| K8 | Explainability | 14 | 65 | Partial | 9.10 | +5 cat ≈ +0.7 to floor 70 | Visibility of MES (hard G1.5) |
| | **KSI** | **100** | **59** | | **58.65→59** | | |

Illustrative: lifting every category to **70** would yield KSI ≈ **70**, still **short of 80**. Version 1 therefore requires a **portfolio** of Strong-band pillars (especially K1/K2/K8 and at least one of K3/K4/K7), not a single feature.

---

## 3. Why estimates overstated movement

| Mechanism | Effect |
|---|---|
| Double-counted category claims vs same baseline | Naive +12 → ~70 not claimable |
| Flag-OFF EP-003.4 / EP-004.1–.3 | K4/K6 validated Δ = 0 |
| Structural Pass ≠ perception Pass | K8/K2/K3 haircut under EP-005.1 methodology |
| Weighted composite math | Large category lifts still small in KSI (e.g. K1 +6 → +0.9) |
| No Tier B post-change pack | Caps Strong-band; blocks G1.5 clear |

---

## 4. Root-cause catalogue

Each root cause (RC) links categories, evidence confidence, and G1 impact.

### RC-01 — Explanation pipeline drop (MES → student)

**Mechanism:** Services attach complete schemas; adapters compress; templates omit `review_point`, drivers, confidence chips, personalisation factors; Coach collapses to opaque prose.  
**Affects:** K8 (primary), K2, K3, K1.  
**Evidence confidence:** **High** (template inventory + EV-EXP-001 vs EV-EXP-003).  
**G1 impact:** Directly blocks **G1.5** (K8 ≥ 70) and limits **G1.1**.

### RC-02 — Dual home / dual start path

**Mechanism:** Legacy Dashboard and canonical Student Home both reachable; competing “today” directors.  
**Affects:** K1, K5 (friction), K8 consistency (P7).  
**Evidence confidence:** **High** (Near Universal blind theme).  
**G1 impact:** Caps K1 Strong; undermines claim of reduced decision burden.

### RC-03 — Same-day duration mismatch (commonly 30 vs 90)

**Mechanism:** Multiple duration sources (plan, session, projection, recommendation) disagree.  
**Affects:** K1, K5, completion likelihood.  
**Evidence confidence:** **High** (Universal; 14+ reviewers).  
**G1 impact:** Caps K1; threatens G5 planning honesty if persists in production smoke.

### RC-04 — Readiness unpackability

**Mechanism:** Percentage prominent; drivers/review/change reasoning not first-class; composites anxiety-inducing for resitters.  
**Affects:** K3, K8.  
**Evidence confidence:** **High** (SV-013; EV-RDY-005).  
**G1 impact:** Limits K3; honesty risk if soothing language outruns inspectability.

### RC-05 — Recommendation trust limited by speech, not ranking

**Mechanism:** Decision Framework present; student sees restatement / generic evidence language; no acceptance KPI.  
**Affects:** K2, K8.  
**Evidence confidence:** **Medium–High** (contracts Pass + perception Weak; no post-change re-test).  
**G1 impact:** K2 floor met (53) but Strong-band and effectiveness GO blocked.

### RC-06 — Closed-loop capabilities invisible in W-PROD

**Mechanism:** Learning feedback, Personal Learning Profile, rec/plan personalisation default OFF; no template provenance when ON.  
**Affects:** K4, K6, secondary K1/K2.  
**Evidence confidence:** **High** (flags + EP-005.1).  
**G1 impact:** Estimated ~+6–8 W-GATED points unavailable to validated G1 until dogfood + activation discipline.

### RC-07 — Missing Tier B / cohort evidence

**Mechanism:** No post-MES blind re-review; external N=0; M1–M9 exploratory; effectiveness NO-GO.  
**Affects:** Confidence on all categories; claimable Strong-band; **G1.9**.  
**Evidence confidence:** **High** (GAP-01, GAP-02, EV-PERC-003…005).  
**G1 impact:** Hard fail path for educational usefulness declaration even if UI improves.

### RC-08 — Motivation is protective, not restorative

**Mechanism:** Calm tone avoids shame; missing smaller restart that “counts,” explicit post-failure adaptation narrative.  
**Affects:** K5; secondary K1 completion.  
**Evidence confidence:** **Medium** (perception themes; no dedicated motivation programme).  
**G1 impact:** Soft drag on composite; consequential after K1/K2/K8 fixes.

### RC-09 — Analytics not decision-grade

**Mechanism:** Charts and honesty tooltips exist; students do not reliably change next study decision; Journey emit deferred; feedback OFF.  
**Affects:** K6 (floor 50).  
**Evidence confidence:** **Medium–High**.  
**G1 impact:** Floor risk if regressions; large upside only with decision-linked UX + lawful evidence.

### RC-10 — Revision support stagnant

**Mechanism:** No dedicated W-PROD revision usefulness lift; personalisation-gated revision timing unsupported.  
**Affects:** K7.  
**Evidence confidence:** **Medium**.  
**G1 impact:** Needed for portfolio path to 80; not the first G1.5 blocker.

---

## 5. Root-cause → KSI contribution model (planning)

Estimated **validated** composite recovery if root causes are addressed (not a new validated score; planning ranges only):

| Priority band | Root causes | Est. validated ΔKSI if fixed | Notes |
|---|---|---:|---|
| Critical (G1 unblocking) | RC-01, RC-07 (K8 pack), RC-02, RC-03 | +4 to +8 | Clears path toward K8≥70 and K1 Strong; still need portfolio |
| High (pillar lifts) | RC-04, RC-05 | +3 to +6 | K2/K3 toward Strong |
| Activation (gated value) | RC-06 after dogfood | +2 to +5 | Only after soak; never claim while OFF |
| Supporting | RC-08, RC-09, RC-10 | +2 to +5 | Needed to approach 80 as portfolio |
| **Illustrative total if all succeed** | | **~+11 to +24** | Upper bound optimistic; prefer under-claim; re-validate |

Reaching ≥80 remains **uncertain** without Strong-band evidence on multiple pillars. Do not treat this table as G1 PASS forecast.

---

## 6. What is *not* the primary gap

| Non-primary explanation | Why rejected as #1 |
|---|---|
| “Need another recommendation algorithm” | Contracts Pass; perception fails on inspectability |
| “Need LLM coach copy” | Violates opaque-AI / Art. IV risk; corpus distrusts unverifiable intelligence speech |
| “Stack more estimated ΔKSI programmes” | EP-005.1 falsified naive stacking |
| “Turn all personalisation flags ON immediately” | Without dogfood + visible provenance, risks honesty and G12 discipline |
| “Operational GA / architecture cutover alone” | Orthogonal; insufficient for G1 |

---

## 7. Version 1 G1 failure mapping

| G1 criterion | Link to root causes |
|---|---|
| G1.1 KSI ≥ 80 | RC-01…RC-10 portfolio shortfall |
| G1.5 K8 ≥ 70 | **RC-01**, RC-07 |
| G1.9 effectiveness not NO-GO | **RC-07** (cohort / Stage 1–2) |
| G1.7 second assessor | Process gap (GAP-05), not experience RC |

---

## 8. Implications

1. Next programmes should buy **rendered explainability + single-path planning honesty + Tier B evidence**, not new educational brains.  
2. Treat presentation completeness of MES as a **hard quality gate** (G3 spirit) equal to service schema completeness.  
3. Activate gated personalisation only after controlled dogfood with visible factors.  
4. Re-score validated KSI only after Tier B pack — do not amend EP-005.1 scores from this docs programme.

Detail ranking: [`PRIORITISED_REMEDIATION_PLAN.md`](PRIORITISED_REMEDIATION_PLAN.md).

---

## References

- `../ep005_1_ksi_validation_evidence/VALIDATED_KSI_REPORT.md`  
- `../ep005_1_ksi_validation_evidence/KSI_EVIDENCE_REGISTER.md`  
- `../ep005_1_ksi_validation_evidence/VERSION_1_G1_STATUS.md`  
- [`EDUCATIONAL_EXPERIENCE_REVIEW.md`](EDUCATIONAL_EXPERIENCE_REVIEW.md)  
- [`STUDENT_JOURNEY_REVIEW.md`](STUDENT_JOURNEY_REVIEW.md)  

---

**End of KSI_GAP_ANALYSIS**
