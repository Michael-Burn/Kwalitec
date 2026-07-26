# P-004.1 — High-Leverage Improvements

**Programme:** P-004.1 — KSI Gap Analysis & Improvement Roadmap  
**Date:** 2026-07-26  
**Status:** Analysis / planning only — no implementation in this programme  
**Constraint:** No speculative AI features without evidence; no second educational brain; no estimate stacking  

---

## 1. Scoring rubric (prioritisation matrix)

Each improvement is scored 1–5 (higher = better for prioritisation), then ranked by **Priority score**.

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| **Educational impact** | Cosmetic | Material category lift | Unblocks Strong-band / V1 pillar |
| **Evidence strength** | Speculative | Supported assumption / residual Tier B | High-confidence open root cause |
| **Engineering effort** *(inverted)* | Multi-quarter / multi-system | 1–2 focused programmes | ≤1 focused programme or ops |
| **Governance risk** *(inverted)* | High honesty / constitution risk | Manageable with gates | Low / already lawful |
| **Student value** | Indirect | Daily-path clarity or trust | Direct “what now / why / next” |
| **Expected KSI improvement** | &lt; +0.8 | +0.8–1.9 | ≥ +2.0 composite if successful |

**Priority score** = Educational impact + Evidence strength + Student value + Expected KSI + Engineering effort (inverted) + Governance risk (inverted).  
Max 30. Prefer constitution-safe ties.

---

## 2. Improvement catalogue

### IMP-01 — Recommendation trust surfaces (inspectable why → next)

| Field | Content |
|---|---|
| **Identifier** | IMP-01 |
| **Problem addressed** | PP-001, RC-05 |
| **Student benefit** | Can see why the primary tip was chosen, what evidence supports it, what alternatives/refusal mean, and what to do next — without reverse-engineering |
| **Educational rationale** | Trust precedes acceptance; P-001.2/1.3 already require inspectability; corpus distrusts unverifiable speech |
| **Expected KSI dimensions** | K2 primary; K8 secondary |
| **Expected KSI movement** | **+1.5 to +2.5** (validated range if Tier B + prefer-lower) |
| **Complexity** | Medium (presentation + DTO completeness; ranking change only if defects found) |
| **Risk** | Low–Medium (over-claiming effectiveness if copy overreaches) |
| **Dependencies** | Existing MES / Decision Framework; DR-050 single CTA |
| **Recommended priority** | **P0** |
| **Scores** | Edu 5 · Evid 5 · Effort 3 · Gov 4 · Student 5 · KSI 5 → **Priority 27** |

---

### IMP-02 — Recommendation acceptance instrumentation (approved PRD)

| Field | Content |
|---|---|
| **Identifier** | IMP-02 |
| **Problem addressed** | PP-001, PP-002 (measurement), PA-014 |
| **Student benefit** | Indirect — enables product to learn whether tips are followed and to stop guessing |
| **Educational rationale** | Without uptake metrics, K2 Strong-band and freeze lift (DR-036) stay blocked |
| **Expected KSI dimensions** | K2 (claimability); confidence on all |
| **Expected KSI movement** | **+0.5 to +1.5** when paired with IMP-01 + Stage 1; alone mostly unlocks validation |
| **Complexity** | Medium (PRD + telemetry + privacy checklist) |
| **Risk** | Medium (privacy / analytics pilot gates) |
| **Dependencies** | EFF-06 analytics pilot; approved PRD; IMP-01 preferred first |
| **Recommended priority** | **P0** (parallel with IMP-03 ops where possible) |
| **Scores** | Edu 4 · Evid 4 · Effort 3 · Gov 3 · Student 3 · KSI 4 → **Priority 21** |

---

### IMP-03 — Stage 1 external cohort execution (privacy → scorecards → interviews)

| Field | Content |
|---|---|
| **Identifier** | IMP-03 |
| **Problem addressed** | PP-002, RC-07, G1.9 |
| **Student benefit** | Real students get invite-only beta with honest measurement; product learns whether usefulness is behavioural |
| **Educational rationale** | Perception ≠ effectiveness (DR-033); G1 cannot PASS while effectiveness NO-GO |
| **Expected KSI dimensions** | All (confidence + possible validated lifts); G1.9 |
| **Expected KSI movement** | **Claimability critical**; direct ΔKSI **+1 to +4** only if behaviours/interviews support — do not pre-claim |
| **Complexity** | Large ops (privacy signatures first) |
| **Risk** | Medium (ethics if rushed; Low if EFF path followed) |
| **Dependencies** | EFF-02 Privacy Review; EFF-01 invites; EP-007.3 design |
| **Recommended priority** | **P0** (orthogonal critical path) |
| **Scores** | Edu 5 · Evid 5 · Effort 2 · Gov 4 · Student 5 · KSI 5 → **Priority 26** |

---

### IMP-04 — Controlled personalisation / feedback activation (dogfood → soak → G12)

| Field | Content |
|---|---|
| **Identifier** | IMP-04 |
| **Problem addressed** | PP-003, PP-004 (partial), RC-06 |
| **Student benefit** | Plan and tips adapt to evidenced profile factors; students can see *which* factors applied |
| **Educational rationale** | Estimated K4/K6 value is currently zero in W-PROD; activation without provenance is honesty risk |
| **Expected KSI dimensions** | K4, K6; secondary K1, K2 |
| **Expected KSI movement** | **+2.0 to +4.0** if soak succeeds and re-validated (upper bound optimistic; prefer under-claim) |
| **Complexity** | Medium–Large (dogfood + G12 matrix + rollback) |
| **Risk** | Medium–High if flipped casually (PR-012, PR-016) |
| **Dependencies** | PA-033 / DR-043; EP-003.4 / EP-004.1–.3 code already present |
| **Recommended priority** | **P1** (after or tightly gated with P0 trust work) |
| **Scores** | Edu 5 · Evid 4 · Effort 2 · Gov 2 · Student 5 · KSI 5 → **Priority 23** |

---

### IMP-05 — Decision-grade analytics / history (link trends → next action)

| Field | Content |
|---|---|
| **Identifier** | IMP-05 |
| **Problem addressed** | PP-004, RC-09 |
| **Student benefit** | Progress surfaces answer “what should I change?” not “how busy was I?” |
| **Educational rationale** | Vision: measure learning not activity; K6 floor is a V1-K2 bare risk |
| **Expected KSI dimensions** | K6; secondary K8 |
| **Expected KSI movement** | **+1.0 to +2.0** |
| **Complexity** | Medium |
| **Risk** | Medium (vanity dashboard temptation; emit honesty) |
| **Dependencies** | Partly IMP-04 / lawful evidence; DR-047 claim discipline |
| **Recommended priority** | **P1** |
| **Scores** | Edu 4 · Evid 4 · Effort 3 · Gov 3 · Student 4 · KSI 4 → **Priority 22** |

---

### IMP-06 — Revision workspace usefulness (weak-topic / spaced return)

| Field | Content |
|---|---|
| **Identifier** | IMP-06 |
| **Problem addressed** | PP-005, RC-10, PP-013 |
| **Student benefit** | Revision prioritises evidenced gaps; earns place beside external tools |
| **Educational rationale** | Professional exams won in revision; K7 lag blocks portfolio ≥80 |
| **Expected KSI dimensions** | K7; secondary K4 if personalisation ON |
| **Expected KSI movement** | **+1.0 to +2.0** |
| **Complexity** | Medium–Large |
| **Risk** | Medium (contradicting Learning Mode without authority) |
| **Dependencies** | Prefer after IMP-01; stronger with IMP-04 |
| **Recommended priority** | **P1 / Medium-term** |
| **Scores** | Edu 4 · Evid 3 · Effort 2 · Gov 4 · Student 4 · KSI 4 → **Priority 21** |

---

### IMP-07 — Cold-start honesty + sparse onboarding orientation

| Field | Content |
|---|---|
| **Identifier** | IMP-07 |
| **Problem addressed** | PP-006, PP-007, PR-017 |
| **Student benefit** | New students understand what is unknown vs estimated; less false precision |
| **Educational rationale** | Unknown must remain unknown; cold-start is when trust is set |
| **Expected KSI dimensions** | K3, K8, K5 |
| **Expected KSI movement** | **+0.5 to +1.2** |
| **Complexity** | Small–Medium |
| **Risk** | Low |
| **Dependencies** | Existing readiness MES patterns |
| **Recommended priority** | **Quick win / P1** |
| **Scores** | Edu 3 · Evid 4 · Effort 5 · Gov 5 · Student 4 · KSI 3 → **Priority 24** |

---

### IMP-08 — Restorative restart after miss / fail

| Field | Content |
|---|---|
| **Identifier** | IMP-08 |
| **Problem addressed** | PP-008, RC-08 |
| **Student benefit** | Clear smaller restart that counts; no shame streaks |
| **Educational rationale** | Consistency is Vision success; motivation must be restorative not hype |
| **Expected KSI dimensions** | K5, K1 |
| **Expected KSI movement** | **+0.5 to +1.5** |
| **Complexity** | Small–Medium |
| **Risk** | Low if no gamification theatre |
| **Dependencies** | None hard |
| **Recommended priority** | **P2 / supporting** |
| **Scores** | Edu 3 · Evid 3 · Effort 4 · Gov 5 · Student 4 · KSI 3 → **Priority 22** |

---

### IMP-09 — G1.7 second-assessor KSI formality

| Field | Content |
|---|---|
| **Identifier** | IMP-09 |
| **Problem addressed** | PP-014, RC-13, PR-009 |
| **Student benefit** | None direct — Board confidence |
| **Educational rationale** | PSF tolerance procedure before declaration |
| **Expected KSI dimensions** | Process only |
| **Expected KSI movement** | **0** |
| **Complexity** | Small |
| **Risk** | Low |
| **Dependencies** | Current evidence package |
| **Recommended priority** | **Declaration hygiene (before GO board)** |
| **Scores** | Edu 1 · Evid 5 · Effort 5 · Gov 5 · Student 1 · KSI 1 → **Priority 18** |

---

### IMP-10 — Sparse-content night honesty / session completeness

| Field | Content |
|---|---|
| **Identifier** | IMP-10 |
| **Problem addressed** | PP-009 |
| **Student benefit** | Session overview is complete or honestly empty — never a hollow template |
| **Educational rationale** | Thin overview destroys “intelligence” perception (SV-003) |
| **Expected KSI dimensions** | K1, K5 |
| **Expected KSI movement** | **+0.3 to +0.9** |
| **Complexity** | Small–Medium |
| **Risk** | Low |
| **Dependencies** | Content ops may dominate engineering |
| **Recommended priority** | **Quick win** |
| **Scores** | Edu 3 · Evid 4 · Effort 4 · Gov 5 · Student 3 · KSI 2 → **Priority 21** |

---

### IMP-11 — Claim-window recommendation precision sample (conditional)

| Field | Content |
|---|---|
| **Identifier** | IMP-11 |
| **Problem addressed** | PP-010, RC-11 |
| **Student benefit** | Only if defects found — better topic selection |
| **Educational rationale** | Fix evidenced precision defects; do not invent a new ranking brain |
| **Expected KSI dimensions** | K2, K1 |
| **Expected KSI movement** | **0 to +1.5** (conditional on defects) |
| **Complexity** | Medium |
| **Risk** | Medium if used as pretext for algorithm churn |
| **Dependencies** | IMP-01/02 preferred; Stage 1 helps |
| **Recommended priority** | **Conditional P1** — only after trust surfaces and sample shows defects |
| **Scores** | Edu 3 · Evid 2 · Effort 3 · Gov 3 · Student 3 · KSI 2 → **Priority 16** |

---

## 3. Explicit non-improvements (do not schedule)

| Rejected | Why | Score note |
|---|---|---|
| Opaque LLM coach personality | Constitution / Art. IV / P-001.2; corpus distrust | Disqualified |
| New second educational runtime / Twin-as-authority ON for marketing | Architecture; Twin T7 not declared; flags OFF | Disqualified |
| Inflating readiness / Exam Ready copy | Honesty / Never-Build adjacent | Disqualified |
| Stacking estimated ΔKSI as “current progress” | DR-026 | Disqualified |
| Immediate all-flags-ON personalisation | PR-012 / PA-033 | Disqualified as IMP; use IMP-04 gated path |
| Rebuilding dual-home/duration on W-PROD as primary | Already closed EP-007.2 | Negative leverage |
| Operational GA alone as KSI programme | Orthogonal | ΔKSI ≈ 0 educational |

---

## 4. Prioritisation matrix (ranked)

| Rank | ID | Title | Priority score | Band | Est. ΔKSI |
|---|---|---|---:|---|---|
| 1 | **IMP-01** | Recommendation trust surfaces | **27** | P0 | +1.5–2.5 |
| 2 | **IMP-03** | Stage 1 cohort execution | **26** | P0 | claimability (+1–4 if earned) |
| 3 | **IMP-07** | Cold-start honesty + onboarding | **24** | Quick win | +0.5–1.2 |
| 4 | **IMP-04** | Controlled personalisation activation | **23** | P1 | +2.0–4.0 |
| 5 | **IMP-05** | Decision-grade analytics | **22** | P1 | +1.0–2.0 |
| 5 | **IMP-08** | Restorative restart | **22** | P2 | +0.5–1.5 |
| 7 | **IMP-02** | Acceptance instrumentation | **21** | P0 | +0.5–1.5 |
| 7 | **IMP-06** | Revision usefulness | **21** | P1 | +1.0–2.0 |
| 7 | **IMP-10** | Sparse-content honesty | **21** | Quick win | +0.3–0.9 |
| 10 | **IMP-09** | G1.7 second assessor | **18** | Declaration | 0 |
| 11 | **IMP-11** | Precision sample (conditional) | **16** | Conditional | 0–1.5 |

---

## 5. What matters vs what does not

### Matters most now

1. Make recommendations **trustworthy and measurable** (IMP-01, IMP-02).  
2. Start **external evidence** (IMP-03).  
3. Realise **gated personalisation/analytics value** carefully (IMP-04, IMP-05).  
4. Fill **revision** and **restart** gaps for portfolio math (IMP-06, IMP-08).  
5. Ship **honest cold-start / sparse-state** quick wins (IMP-07, IMP-10).

### Does not matter (for KSI 80 path)

- New AI coach features without evidence  
- Re-litigating closed W-PROD journey themes as P0  
- Estimate-only programme theatre  
- Premature flag marketing  

Engineering programme mapping: [`ENGINEERING_PRIORITIES.md`](ENGINEERING_PRIORITIES.md).  
Portfolio math: [`EXPECTED_KSI_IMPACT.md`](EXPECTED_KSI_IMPACT.md).

---

**End of HIGH_LEVERAGE_IMPROVEMENTS**
