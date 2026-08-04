# KSI-002 — Evidence Acceptance Criteria

**Programme:** KSI-002 — Educational Effectiveness Validation Protocol  
**Version:** 1.0  
**Status:** PROTOCOL COMPLETE — AWAITING FOUNDER REVIEW  
**Effective:** 2026-08-04  
**Authority:** `KSI002_VALIDATION_PROTOCOL.md` · PSF §5.6 · VERSION_1_RELEASE_FRAMEWORK Gate G1 · KSI-001 honesty rules  

**Defines what may enter a validated KSI / G1.9 package.** Does not accept or reject any live package in this programme.

---

## 1. Purpose

Make acceptance/rejection of educational-effectiveness evidence **mechanical enough to resist optimism**.

---

## 2. What counts as evidence

Evidence **counts** only if it meets **all** of:

1. **Claim-window matched** — platform posture (W-PROD / W-GATED) and flag matrix stated.  
2. **Protocol-version cited** — KSI-002 (or successor) version that governed collection.  
3. **Traceable** — paths to raw or summarised artefacts (scorecards, coded interviews, rate tables).  
4. **Pseudonymous** — no prohibited PII in git.  
5. **Class-labelled** — correctness / usefulness / effectiveness / confidence / recommendation usefulness (one primary).  
6. **Dated** — collection and assessment dates recorded.  
7. **Consent-bounded** — measurement/interview consent respected.  

### 2.1 Accepted evidence types (ranked)

| Rank | Type | May support |
|------|------|-------------|
| A | External longitudinal Stage 1/2 behavioural scorecards (M1–M9) under this protocol | G1.9; K5/K1/K7 corroboration |
| A | Structured interviews coded per Participant Protocol | G1.9; K1–K8 rationales |
| A | Observational recommendation rates with declared TTL | K2 Strong-band *discussion* |
| B | Independent second-assessor KSI re-score of same package | G1.7 |
| C | Internal Tier B perception packs with N, instrument, limitations | Partial / Strong-floor usefulness |
| D | Stage 0 dogfood / Founder walkthrough defect class | Operability; **not** usefulness lifts |
| E | Checklist Pass (Explainability / Recommendation / Planning / Readiness) | Structural eligibility; G2–G6 context |

---

## 3. What does NOT count

| Artefact / move | Why rejected as validated KSI / G1.9 input |
|-----------------|-------------------------------------------|
| Programme **estimated ΔKSI** | PSF §5.6 — planning only |
| **Premium** PASS / Conditional PASS | Craft ≠ usefulness index |
| **Progressive Confidence** / PB simulation PASS | Confidence ≠ effectiveness |
| Educational **Content Freeze** / Approver count | Correctness ≠ usefulness |
| Founder enthusiasm without coded evidence | Observer / Founder bias |
| Marketing copy, landing pages, sales decks | Not measurement |
| Exam **pass-rate** anecdotes | Wrong estimand; north-star separate |
| Telemetry vanity (logins, page views) | Violates learning-over-activity |
| Flag-OFF capability counted as live personalisation / analytics | Honesty violation |
| Mid-study redefined metrics | Protocol breach |
| Quotes without consent / with identifying detail in git | Privacy breach |
| Single Tier B pack used to clear G1.9 | Insufficient rank |
| Summing overlapping EP estimates to “≥80” | Forbidden composite |

---

## 4. When evidence expires

| Clock | Rule |
|-------|------|
| **Declaration clock** | Validated KSI assessment &gt; **90 days** before Version 1 declaration → **expired** for G1.3 |
| **Behavioural pack clock** | Stage 1/2 scorecards older than **90 days** with no continuity refresh → cannot solely support G1.9 PASS |
| **Perception pack clock** | Tier B packs &gt; **90 days** → supporting only; re-run before using for category *lifts* |
| **Claim-window change** | Material flag / runtime / educational-surface change → prior pack **expired** for the new window until re-measured |
| **Consent withdrawal** | Individual’s data expires from numerators immediately |

Expired evidence may remain in historical registers labelled **historical — not declaration-grade**.

---

## 5. When evidence must be repeated

Repeat (full or targeted) when **any** hold:

1. Package aged past validity window and a G1 board is planned.  
2. Prefer-lower dispute unresolved after G1.7.  
3. Honesty incident related to the claim window (G1.10).  
4. N floors were met with waiver that has since been revoked.  
5. Moving a category into **Strong-band** when prior evidence was perception-only (especially K2 rates).  
6. Switching claim window (W-PROD ↔ W-GATED).  

---

## 6. When evidence can be combined

| Combination | Allowed? | Conditions |
|-------------|----------|------------|
| Stage 1 behaviour + Stage 1 interviews | **Yes** | Same wave / claim window |
| Tier B perception + Stage 1 behaviour | **Yes** | Perception cannot override worse behaviour; prefer-lower |
| Multiple Tier B packs across surfaces | **Yes** | De-duplicate overlapping themes; no score double-counting |
| W-PROD + W-GATED | **No** as one board | Publish separate boards; never blend |
| Estimated ΔKSI + validated board | **No** | Estimates stay in planning annex only |
| PB confidence + KSI | **No** substitution | May appear as *context* footnote only |
| Historical expired + fresh | **Yes** for narrative | Only fresh drives scores |

---

## 7. When lower evidence overrides higher estimates

**Binding override rule (constitutional):**

> If a lower-rank or more conservative evidence item conflicts with a higher *estimate*, programme hope, Premium result, or older optimistic perception pack, the **validated score / verdict follows the more conservative evidence**.

Examples:

| Conflict | Outcome |
|----------|---------|
| Estimated K2 +10 vs observational rates missing | Hold Partial; no Strong-band |
| Tier B Strong-floor vs Stage 1 poor M6 | Prefer lower category / withhold G1.9 |
| Premium Conditional PASS vs validated KSI 64 | KSI unchanged |
| PB-017 9.00/9 vs effectiveness NO-GO | Effectiveness remains NO-GO |
| Old KSI 64 package vs new independent re-score 61 | Investigate; do not average up; resolve per ±3 rule |

---

## 8. Acceptance checklist (future package gate)

A future evidence package is **ACCEPTABLE for G1 consideration** only if:

- [ ] Protocol version cited  
- [ ] Claim window + flag matrix stated  
- [ ] Analysis sets N-flow present  
- [ ] Primary endpoints reported per SAP  
- [ ] Q1–Q5 worksheet linked  
- [ ] K1–K8 table with paths, rationales, confidence, limitations  
- [ ] Prefer-lower decisions listed  
- [ ] Non-claims section present  
- [ ] No estimated/Premium/PB substitution  
- [ ] Assessment date ≤90 days at use  
- [ ] G1.7 filed or explicitly HOLD with no declaration  

Else: **REJECT** for declaration use (may still inform engineering backlog outside KSI-002).

---

## 9. Rejection classes

| Code | Meaning |
|------|---------|
| R-SUBST | Substitution of confidence/correctness/Premium for usefulness |
| R-WINDOW | Claim-window mismatch or flag dishonesty |
| R-AGE | Expired clock |
| R-N | Insufficient N without waiver |
| R-MIX | Mixed estimands in one verdict |
| R-PII | Privacy breach in artefacts |
| R-POSTHOC | Undocumented metric/target change after unblinding |
| R-RANK | Wrong evidence rank for claimed gate |

---

## 10. Exit

**STOP.** Criteria published for Founder review. No live package adjudicated in KSI-002.
