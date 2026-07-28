# RP-002 — Authority Conflict Register

**Programme:** RP-002 — Independent Educational Recertification  
**Date:** 2026-07-28  
**Status:** Active — independent authority re-score from live product  
**Authority:** DG-001.2 Educational Authority Model · `RP002_EDUCATIONAL_AUDIT_REPORT.md`  
**Constraint:** Does not modify product. RR-001 / DG-001 AC-* registers are historical — this register re-measures conflicts in the current product.

Severity: **Critical / High / Medium / Low**  
Likelihood: **Likely / Possible / Unlikely**  
Status: **Clear** · **Watch** · **Open** · **Contained** · **Accepted Residual**

---

## Purpose

Identify educational **authority** defects on the live product:

- competing authorities  
- duplicated authority  
- authority overlap  
- authority gaps  
- hidden authority transitions  
- inappropriate ownership  

---

## Summary

| ID | Conflict | Type | Severity | Likelihood | Status |
|----|----------|------|----------|------------|--------|
| RP002-AC-01 | KW→SS handoff | Gap (historical) | High | — | **Clear** on onboarding/Help/welcome |
| RP002-AC-02 | Home dual chrome (Your learning + Study Sensei) | Overlap / density | Low–Med | Possible | **Watch** (naming-density policy mitigates) |
| RP002-AC-03 | Commitment “What we updated” unnamed | Hidden attribution | Low–Med | Possible | **Open** → RP002-NCR-002 |
| RP002-AC-04 | Share Feedback vs Product Check-in | Duplicated concept naming | Medium | Possible | **Open** → RP002-NCR-001 |
| RP002-AC-05 | Learning Check “Kwalitec understand” | Inappropriate ownership | Medium | Possible if path used | **Open** → RP002-NCR-004 |
| RP002-AC-06 | Legacy session feedback Kwalitec observer | Inappropriate ownership | High | Unlikely under sole ON | **Contained** → RP002-NCR-006 |
| RP002-AC-07 | Legacy dashboard Recommendation-as-focus | Duplicated focus authority | High | Unlikely under sole ON | **Contained** → RP002-NCR-007 |
| RP002-AC-08 | Latent recommendation_card eyebrow | Duplicated focus noun risk | Medium | Unlikely until rewired | **Contained** → RP002-NCR-005 |
| RP002-AC-09 | History vs Journal/Timeline | Competing epistemology | Medium | Unlikely | **Clear** (bridge live) |
| RP002-AC-10 | Revision vs Mission | Competing focus | Medium | Unlikely | **Clear** (primacy sentence live) |
| RP002-AC-11 | Feature-flag / gated mentor speech | Inappropriate if ON | Medium–High | Unlikely while Contained | **Accepted Residual** |
| RP002-AC-12 | Notifications as Sensei | Overlap if built | Medium | Unlikely (absent) | **Accepted Residual** |
| RP002-AC-13 | Parallel reflection stacks as second map | Fragmentation risk | Medium | Unlikely on Alpha map | **Accepted Residual** (D08) |
| RP002-AC-14 | MI + MES density | Authority noise | Medium | Possible | **Watch** (mitigated disclosure) |

---

## Conflict detail

### RP002-AC-01 — KW→SS handoff

| Field | Detail |
|-------|--------|
| **Type** | Authority gap (historical ED-01) |
| **Live evidence** | Handoff sentence in onboarding step 2, welcome modal, Help orientation |
| **Status** | **Clear** |
| **Clause** | DG-001.2-D04; DG-001.1-D01 |

### RP002-AC-02 — Home dual chrome

| Field | Detail |
|-------|--------|
| **Type** | Authority overlap / naming density |
| **Live evidence** | Shell `page_eyebrow="Your learning"`; hero `Study Sensei` |
| **Status** | **Watch** — HOME_SENSEI_NAMING_POLICY intends single mentor name in hero |
| **Clause** | D05; OQ-02 lineage |
| **Follow-up** | Cohort dogfood; do not re-add Sensei eyebrows on secondary panels |

### RP002-AC-03 — Unnamed commitment update

| Field | Detail |
|-------|--------|
| **Type** | Hidden attribution |
| **Live evidence** | “What we updated” on Home commitment reflection |
| **Status** | **Open** |
| **Clause** | D05; CP-04 |
| **NCR** | RP002-NCR-002 |

### RP002-AC-04 — Check-in entry naming

| Field | Detail |
|-------|--------|
| **Type** | Duplicated concept naming (felt authority blur with “feedback”) |
| **Live evidence** | Nav **Share Feedback** vs page **Product Check-in** |
| **Status** | **Open** |
| **Clause** | D02; D10; CI-03 |
| **NCR** | RP002-NCR-001 |

### RP002-AC-05 — Learning Check product-as-supporter

| Field | Detail |
|-------|--------|
| **Type** | Inappropriate ownership |
| **Live evidence** | Assessment entry: answers help **Kwalitec** understand how to support you |
| **Status** | **Open** (orphan/deferred path) |
| **Clause** | D01; D02; CP-10 |
| **NCR** | RP002-NCR-004 |

### RP002-AC-06 — Legacy Kwalitec observer

| Field | Detail |
|-------|--------|
| **Type** | Inappropriate ownership |
| **Live evidence** | `session_recorded.html` Kwalitec observe/conclude; sole-runtime redirect |
| **Status** | **Contained** |
| **Clause** | D01–D03; CP-10 |
| **NCR** | RP002-NCR-006 |

### RP002-AC-07 — Legacy dashboard Recommendation focus

| Field | Detail |
|-------|--------|
| **Type** | Duplicated daily-focus authority |
| **Live evidence** | Dashboard **Today's Recommendation**; redirected under sole runtime |
| **Status** | **Contained** |
| **Clause** | D02 lexicon Mission-led; D05 |
| **NCR** | RP002-NCR-007 |

### RP002-AC-08 — Latent recommendation card

| Field | Detail |
|-------|--------|
| **Type** | Duplicated focus noun risk |
| **Live evidence** | Macro eyebrow **Today's Recommendation**; not on sole Home |
| **Status** | **Contained** |
| **NCR** | RP002-NCR-005 |

### RP002-AC-09 — History epistemology

| Field | Detail |
|-------|--------|
| **Type** | Competing epistemology (historical AC-03) |
| **Live evidence** | History bridge paragraph + Journal/Timeline CTAs |
| **Status** | **Clear** |
| **Clause** | D06 |

### RP002-AC-10 — Revision primacy

| Field | Detail |
|-------|--------|
| **Type** | Competing focus (historical AC-08) |
| **Live evidence** | Revision primacy sentence on Revision surface |
| **Status** | **Clear** |
| **Clause** | D09 |

### RP002-AC-11 — Feature flags

| Field | Detail |
|-------|--------|
| **Type** | Inappropriate ownership if mentor speech rides flags |
| **Status** | **Accepted Residual** Contained OFF |
| **Clause** | D07 |

### RP002-AC-12 — Notifications

| Field | Detail |
|-------|--------|
| **Type** | Overlap / inappropriate if educationalised |
| **Status** | **Accepted Residual** (capability absent) |
| **Clause** | D08 |

### RP002-AC-13 — Parallel reflection stacks

| Field | Detail |
|-------|--------|
| **Type** | Fragmentation risk |
| **Status** | **Accepted Residual** |
| **Clause** | DG-001.3-D08 |

### RP002-AC-14 — MI density

| Field | Detail |
|-------|--------|
| **Type** | Authority noise |
| **Status** | **Watch** |
| **Clause** | D05 |
| **Note** | Prior disclosure mitigated; monitor cognitive load |

---

## Authority clarity score (independent)

| Domain | Primary authority on sole-runtime | Clarity |
|--------|-----------------------------------|---------|
| Educational judgement / Mission | Study Sensei | Clear |
| Product / auth / Check-in page | Kwalitec | Clear (entry label Watch/Open) |
| Mechanical status | System / unnamed | Clear |
| History | Context (not mentor) | Clear |
| Latent dual-run educational chrome | Contained / conflicting | Contained |

**Overall authority posture:** **Conditional Clear** on sole-runtime Alpha — Open polish conflicts do not restore pre-DG-001 dual-mentor failure mode; Contained dual-run paths would.

---

**End of RP002_AUTHORITY_CONFLICT_REGISTER**
