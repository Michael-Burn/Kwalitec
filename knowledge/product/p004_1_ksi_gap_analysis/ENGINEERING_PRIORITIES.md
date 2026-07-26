# P-004.1 — Engineering Priorities

**Programme:** P-004.1 — KSI Gap Analysis & Improvement Roadmap  
**Date:** 2026-07-26  
**Status:** Recommended programme sequence (planning only)  
**Constraint:** Analysis does not authorise runtime work; Product Board commissions subsequent EPs  
**North star for sequencing:** Maximise probability of **validated KSI ≥ 80** + **G1.9 trajectory**, subject to constitutions

---

## 1. Sequencing principles

1. **Educational impact over feature novelty** (PSF §8.1).  
2. **Do not re-solve closed W-PROD pains** (MES primary, dual-home, duration).  
3. **Presentation / trust before new educational brains.**  
4. **Evidence programmes are engineering-adjacent first-class work** (privacy, cohort, scorecards).  
5. **Gated activation requires G12 discipline** (DR-043).  
6. **Estimated ΔKSI ≠ validated progress** (DR-026).  
7. **STOP** on opaque AI educational truth or second runtime authority.

---

## 2. Recommended next programmes (ordered)

Suggested EP identifiers are **proposals** for Board commissioning — not created by this programme.

| Order | Proposed programme | Maps to | Primary KSI | Est. effort | Why now |
|---|---|---|---|---|---|
| **1** | **EP-008.1 — Recommendation Trust Delivery** | IMP-01 | K2, K8 | M | Largest remaining weight×gap; MES exists — finish trust speech on daily path |
| **2** | **EP-008.2 — Stage 1 Private Beta Execution** | IMP-03 (EFF-02…08) | G1.9 + confidence | L (ops) | Hard gate; privacy first; no algorithm required |
| **3** | **EP-008.3 — Recommendation Acceptance Instrumentation** | IMP-02 | K2 claimability | M | Enables Strong-band evidence; needs PRD + analytics pilot |
| **4** | **EP-008.4 — Cold-Start & Sparse-State Honesty** | IMP-07, IMP-10 | K3, K8, K1, K5 | S–M | Quick validated residual clear; low governance risk |
| **5** | **EP-009.1 — Personalisation Dogfood & Soak** | IMP-04 (phase 1) | K4 readiness | M | Realise latent value without production default flip |
| **6** | **EP-009.2 — Decision-Grade Analytics** | IMP-05 | K6 | M | Raise floor; link history → next action |
| **7** | **EP-009.3 — Personalisation / Feedback Default Cutover** | IMP-04 (phase 2) | K4, K6, K1, K2 | M–L | Only after soak + G12 PASS package |
| **8** | **EP-010.1 — Revision Usefulness** | IMP-06 | K7 | M–L | Portfolio filler toward 80 |
| **9** | **EP-010.2 — Restorative Restart** | IMP-08 | K5, K1 | S–M | Supporting motivation |
| **10** | **EP-011.x — Validated KSI Re-score + G1.7** | IMP-09 + methodology | Composite | S–M | After Waves A–C; declaration hygiene |
| **C** | **Conditional: Recommendation Precision Sample** | IMP-11 | K2, K1 | M | Only if trust surfaces + sample show defects |

**Parallelism:** Items **1** and **2** should run **in parallel** (product engineering vs beta ops). Item **3** can start once PRD/privacy allow. Do not wait for KSI 80 before starting Stage 1.

---

## 3. What engineering should *not* start next

| Anti-priority | Reason |
|---|---|
| New recommendation ranking algorithm as default first move | Contracts Pass; trust/acceptance gap dominates |
| LLM / generative coach | Constitutional STOP risk |
| Twin production authority / cutover for marketing | Flags OFF; T7 not declared; PR-016 |
| Re-architecture of sole-runtime Home | Closed on W-PROD |
| Broad vanity analytics dashboards | Harms K6 honesty |
| “Quick” all-flags-ON | PR-012 / PA-033 |
| Docs-only estimate stacking programmes | Already falsified |

---

## 4. Dependency graph

```
Privacy signatures (EFF-02)
        ↓
Stage 1 invites + scorecards (EP-008.2) ────────────────┐
                                                        ↓
Recommendation trust UI (EP-008.1) → Acceptance KPI (EP-008.3) → K2 revalidation
        ↓
Cold-start / sparse honesty (EP-008.4)
        ↓
Personalisation dogfood (EP-009.1) → Analytics UX (EP-009.2)
        ↓
G12 pack + soak health → Default cutover (EP-009.3)
        ↓
Revision (EP-010.1) + Restorative restart (EP-010.2)
        ↓
Validated KSI re-score + G1.7 (EP-011.x)
        ↓
Only then: consider G1 declaration board (still needs G2–G12 package)
```

---

## 5. Definition of done per priority band

### P0 done when

- Home/Coach/Mission primary recommendation shows inspectable why + evidence + next (IMP-01).  
- Privacy signed; Stage 1 invites issued; weekly scorecards filing started (IMP-03).  
- Acceptance events defined under approved PRD (IMP-02) — instrumentation may land slightly after trust UI.

### P1 done when

- Dogfood pack for profile/personalisation/feedback complete with visible factors.  
- Decision-grade analytics links at least one trend to a next action without vanity.  
- G12 matrix scored for any proposed ON default.  
- Revision path shows evidenced weak-topic priority (or honest empty).

### Declaration hygiene done when

- New validated KSI board ≤90 days; G1.7 second assessor filed; G1.9 not NO-GO; Evidence Package G1–G12 assembled.

---

## 6. Mapping to open REM / EFF IDs

| Legacy ID | Status | Successor |
|---|---|---|
| REM-01…05, REM-02/03 | Closed / closed on W-PROD | Do not reopen as P0 |
| REM-06 | Open | EP-008.1 / IMP-01 |
| REM-07 | Open (design only) | EP-008.2 / IMP-03 |
| REM-08 | Open | EP-009.1 → EP-009.3 |
| REM-09 | Open | EP-010.2 |
| REM-10 | Open | EP-009.2 |
| REM-11 | Open | EP-010.1 |
| REM-12 | Open | EP-011.x |
| EFF-02…08 | Open | EP-008.2 |

---

## 7. Resourcing guidance (Board)

| Stream | Owner archetype | Capacity note |
|---|---|---|
| Trust presentation | Product engineering | Highest leverage eng hours |
| Stage 1 ops | Product + Privacy | Critical path; not optional |
| Activation / G12 | Eng + Product | Do not starve after trust |
| Revision / restart | Product eng | After activation wave |
| Validation | Product measurement | Mandatory between waves |

If capacity allows only **one** engineering stream and **one** ops stream: choose **EP-008.1** and **EP-008.2**.

---

## References

- [`HIGH_LEVERAGE_IMPROVEMENTS.md`](HIGH_LEVERAGE_IMPROVEMENTS.md)  
- [`ROADMAP.md`](ROADMAP.md)  
- `../ep005_2_educational_experience_validation/PRIORITISED_REMEDIATION_PLAN.md`  
- `../ep007_3_educational_effectiveness_validation_stage1/PRIORITISED_REMEDIATION.md`  
- `../p003_8_version1_exit_criteria/CURRENT_RELEASE_POSITION.md`  

---

**End of ENGINEERING_PRIORITIES**
