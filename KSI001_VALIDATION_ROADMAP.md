# KSI-001 — Validation Roadmap

**Programme:** KSI-001 — Validated Educational Effectiveness Programme  
**Date:** 2026-08-04  
**Status:** ROADMAP COMPLETE — AWAITING FOUNDER REVIEW  
**Authority:** `KSI001_VALIDATED_KSI_ANALYSIS.md` · `KSI001_EVIDENCE_GAP_ANALYSIS.md` · EP-007.3 · EP-008.x · PSF · P-002.1  

**Principle:** Highest-value **evidence** first. Avoid engineering unless absolutely necessary. Do not modify Runtime, Twin, Recommendation ranking, Educational Framework, Curriculum, Packages, or Premium Experience under this roadmap.

---

## 1. North-star of this roadmap

Prove educational usefulness enough to:

1. Move educational effectiveness away from **NO-GO / PENDING EVIDENCE** (G1.9).  
2. Re-score validated KSI from **64 → ≥ 80** with Medium/High confidence (G1.1).  
3. File G1.7 independent re-score.  

**Not** ship features to “feel” ready.

---

## 2. Priority waves

### Wave V0 — Founder decision gate (this programme exit)

| Step | Action | Owner capacity | Output |
|------|--------|----------------|--------|
| V0.1 | Review `KSI001_VALIDATED_KSI_ANALYSIS.md` | Founder / Product | Accept / amend analysis |
| V0.2 | Accept that G1 FAIL is evidence-bound (not UX debt) | Founder | Decision record |
| V0.3 | Authorise **or** defer Stage 1 Privacy + enrollment | Privacy + Product | Go / Hold |

**STOP until V0 complete.** KSI-001 does not start Stage 1 ops.

---

### Wave V1 — Claimability (G1.9) — **P0**

Highest value: without this, Strong-band KSI remains poorly claimable and G1 cannot PASS.

| Step | Evidence work | Depends on | Exit artefact |
|------|---------------|------------|---------------|
| V1.1 | Complete / sign Privacy Review for Stage 1 measurement | Founder authority | Signed Privacy Review |
| V1.2 | Issue invites under Private Beta Protocol; accept N per EP-007.3 design | V1.1 | Cohort registry (pseudonymous) |
| V1.3 | Weekly M1–M9 scorecards for ≥4 weeks | V1.2 | Scorecard pack in evidence/ |
| V1.4 | Structured interviews (≥8 or 25% active) | V1.2–V1.3 | Interview code book |
| V1.5 | Fill EP-003 Q1–Q5 with linked paths | V1.3–V1.4 | Effectiveness worksheet |
| V1.6 | Update EP-003 / EP-004 educational verdict; re-file G1.9 | V1.5 | `G1_9_STATUS.md` → PASS (or CONDITIONAL with waiver) |

**Engineering required?** No — ops, privacy, measurement, interviews.  
**If N&lt;20:** Product + Educational written waiver with claim restrictions, or extend to Stage 2 before GO-path effectiveness.

---

### Wave V2 — Behavioural recommendation evidence (K2 Strong-band) — **P0**

| Step | Evidence work | Depends on | Exit artefact |
|------|---------------|------------|---------------|
| V2.1 | Define privacy-bounded observational metrics (commit / defer / complete / follow-through) using **existing** chrome | EP-008.3B open items | Metric definition note |
| V2.2 | Collect rates in Stage 0/1 under approved bounds | V1 + V2.1 | Rate tables |
| V2.3 | Re-open Strong-band K2 discussion only if floors met; prefer-lower | V2.2 | K2 revalidation memo |

**Engineering required?** Only if existing events cannot be observed at all — then minimal instrumentation to **record** behaviour (not change ranking). Prefer zero product change; use manual / ops tally if events already exist.  
**Forbidden:** New recommendation algorithm, Twin cutover, LLM coach opacity.

---

### Wave V3 — Portfolio fillers (K6 / K4 / K7) — **P1**

Order by weighted gap × claimability:

| Step | Focus | Evidence work | Engineering? |
|------|-------|---------------|--------------|
| V3.1 | **K6** | Decision-grade analytics perception study; founder scorecard use; one-sentence progress test | No new vanity dashboards; study existing Journey / analytics surfaces |
| V3.2 | **K4** | If Founder authorises: controlled flag-ON dogfood of **existing** profile / personalisation → soak → honesty check vs G12 | Flag flip + soak ops — **not** new personalisation features |
| V3.3 | **K7** | Revision usefulness interviews + adherence proxies on existing revision surfaces | No Wave 16 / package rewrite |

If flag-ON dogfood is refused, document K4/K6 as **capped** and plan portfolio ≥80 using other pillars + Stage 1 corroboration — honesty over optimism.

---

### Wave V4 — Incremental Strong deepen (K3 / K5 / K1 residual) — **P2**

| Step | Focus | Evidence work |
|------|-------|---------------|
| V4.1 | K3 | Multi-week preparedness interviews inside Stage 1 |
| V4.2 | K5 | Miss/return tallies; tone trust codes (no streak theatre) |
| V4.3 | K1 | Topic-selection quality interviews (RC-11) — only after V1–V3 |

---

### Wave V5 — Full validated re-score + declaration formality — **P0 at board time**

| Step | Action | Exit |
|------|--------|------|
| V5.1 | Assemble fresh Evidence Register (paths, rationales, limitations, confidence) | Package ≤90 days |
| V5.2 | Publish validated category table + composite | Target ≥80 **or** honest shortfall |
| V5.3 | Independent second assessor (G1.7) | ±3 agreement or Product dispute resolution |
| V5.4 | Re-run G1.1–G1.10 board | PASS only if both G1.1 and G1.9 clear |
| V5.5 | **Do not** auto-declare Version 1 — still need full P-002.1 G2–G12 | Separate release programme |

---

## 3. Sequencing diagram

```
Founder review (V0)
        │
        ▼
Privacy + Stage 1 ops (V1)  ──►  G1.9 claimability
        │
        ├──► Observational reco rates (V2)  ──►  K2 Strong-band eligibility
        │
        ├──► K6 / K4 / K7 evidence (V3)
        │
        └──► K3 / K5 / K1 deepen (V4)
                    │
                    ▼
           Full re-score + G1.7 (V5)
                    │
                    ▼
           G1 board refresh → still NO Version 1 declaration
           until separate P-002.1 GO with all gates
```

---

## 4. Expected validated movement (planning bands only)

Prefer-lower; **not** validated forecasts; do not sum into “current KSI.”

| Wave | Plausible validated effect if evidence is favourable | If evidence is weak |
|------|------------------------------------------------------|---------------------|
| V1 | Confidence ↑; G1.9 may clear; enables Strong-band claims | G1.9 remains FAIL — stop overclaim |
| V2 | K2 68 → 72–78 band **possible** | Hold 68 |
| V3 | K6 / K4 / K7 material lifts **possible** only with real use evidence | Keep floors / Partial |
| V4 | +1–3 composite possible | Prefer 0 |
| V5 | Publishes truth — may still be &lt;80 | Honest FAIL preserved |

**Portfolio reminder:** All-at-70 ≈ KSI 70. Reaching ≥80 requires several mid-Strong pillars. If Stage 1 shows usefulness but scores still &lt;80, the honest board is **still G1.1 FAIL** — then decide whether further **evidence** on existing product can lift scores, or whether a *future* Founder-authorised product programme is needed. KSI-001 does not authorise that product programme.

---

## 5. Explicit non-roadmap (reject list)

| Proposal | Why rejected here |
|----------|-------------------|
| Rebuild Recommendation Engine | Residual is trust + evidence, not missing brain |
| Twin production cutover for KSI theatre | Flags OFF; marketing forbidden |
| Unfreeze Educational Framework | EF-001 — no EF classification failure |
| Wave 16 / package rewrite for G1 | Content Freeze; correctness already PASS |
| Premium UX polish as G1 plan | PX provisional ΔKSI ≠ validated |
| LLM opaque coach | Constitution / Art. IV |
| Declare V1 after V1 Stage 1 design alone | Ops outcomes required |

---

## 6. Success metrics for the roadmap itself

| Metric | Pass |
|--------|------|
| G1.9 | Not NO-GO (PASS or approved CONDITIONAL with restrictions) |
| G1.1 | Validated KSI ≥ 80 **or** honest documented shortfall with no fake PASS |
| G1.7 | Second assessor filed |
| Product changes by KSI-001 | **Zero** |
| Overclaim incidents | **Zero** |

---

## 7. Exit

This roadmap is **advice for Founder review**, not an authorisation to start invites or flip flags.

Signed: KSI-001 Validation Roadmap · 2026-08-04
