# CP-002 — Confidence Calibration

**Programme:** CP-002 — Capability Programme  
**Version:** 1.0  
**Status:** Active — confidence calibration architecture (design only)  
**Effective:** 2026-07-28  
**Companion to:** `CP002_LEARNING_FEEDBACK_ARCHITECTURE.md`, `CP002_EVIDENCE_INGESTION_MODEL.md`  
**Constraint:** Design only — no readiness scores, tip speech, or Twin confidence fields modified by this programme.

---

## 1. Purpose

Define how the Learning Feedback Loop may update **confidence and calibration** — the honesty of how strongly Kwalitec claims understanding or guidance usefulness — without converting feedback into false certainty or silent ranking power.

**Thesis:** Calibration improves *trustworthiness of claims*. It does not invent mastery, and it does not auto-re-rank recommendations.

---

## 2. What “confidence” means here

Three distinct confidence concepts must not be conflated:

| Concept | Owner | Loop may update? | Meaning |
|---------|-------|------------------|---------|
| **Guidance confidence (speech)** | P-001.2 Explanation schema | Only via LU-CAL + explainability review | Strength language shown to students |
| **Operational calibration** | SI-C3 / OM-RDY / SI-C9 | Via LU-CAL from EF-READY / packs | Predicted vs observed agreement tables |
| **Evidence confidence class** | OM-001 / CP-002 ingestion | Via qualification | C0–C4 warrant of a signal or pack |
| **Twin provisional confidence** | Twin Constitution | Via LU-TWN only as understanding metadata | How strongly Twin *believes* a facet — never destiny |
| **Profile attribute confidence** | EP-004.1 | Unchanged by CP-002 design | `min(1.0, n/10)` behavioural sample confidence |

CP-002 calibration work targets the first four as *architecture*. EP-004.1 formula remains the product baseline for profile attributes unless a future ADR changes it.

---

## 3. Calibration objects (conceptual)

### 3.1 CalibrationRecord

| Field | Meaning |
|-------|---------|
| `calibration_id` | Stable id |
| `target_kind` | `readiness_band` \| `recommendation_usefulness` \| `explainability_strength` \| `twin_facet` |
| `target_ref` | Band / tip family / facet id |
| `window` | Observation period |
| `predicted` | What the system claimed / predicted |
| `observed` | What qualified evidence later showed |
| `agreement_metric` | Deterministic summary (e.g. hit rate, Brier-style design metric) |
| `n` / eligibility | Cohort rules |
| `confidence_class` | C0–C4 of this calibration |
| `educational_meaning_codes[]` | EF-READY / EF-LEARN / EF-EXPLAIN / … |
| `om_metric_ids[]` | e.g. OM-RDY-04 |
| `limitations[]` | Mandatory |
| `proposal_id?` | Link to LearningProposal if promoting a LU-CAL update |

### 3.2 ConfidencePolicyVersion

Versioned policy governing how calibration affects **disclosure**, not ranking:

| Field | Meaning |
|-------|---------|
| `policy_version` | Monotonic version |
| `rules[]` | e.g. “if cell n < N → disclose sparse”; “if overconfident → soften speech” |
| `affects_ranking` | **Must be false** for pure LU-CAL policies |
| `review_refs` | P-001.2 checklist / Founder Review when student-facing |
| `rollback_to` | Prior policy_version |

If a change would affect ranking or selection, it is **LU-POL**, not LU-CAL — see Architecture §6.

---

## 4. Calibration update rules

| Rule | Statement |
|------|-----------|
| **C-R1** | Calibration may **lower** claimed confidence more freely than it may **raise** it |
| **C-R2** | Raising student-facing confidence requires C3+ evidence and P-001.2 Pass (or waiver) |
| **C-R3** | Empty cells (`n` below threshold) yield “unknown / sparse” — never imputed certainty |
| **C-R4** | Accept rate is not a calibration of educational usefulness (P-001.3) |
| **C-R5** | ExplanationSnapshot at decision time stays frozen; calibration affects *future* speech only |
| **C-R6** | Calibration tables are reproducible from declared inputs (PC-09) |
| **C-R7** | Conflicted EF-CONFLICT signals block upward calibration until human resolution |

---

## 5. Readiness calibration loop (SI-C3)

Aligned with SI-001 Outcome Framework and OM-RDY-*:

```
Readiness band / drivers predicted
        │
        ▼
Later attempt / learning evidence (qualified EF-READY / EF-LEARN)
        │
        ▼
CalibrationRecord (agreement by band, topic family, sparsity)
        │
        ▼
LU-CAL proposal → review → ConfidencePolicyVersion
        │
        ▼
Future readiness honesty disclosure (not silent score mutation)
```

**Forbidden:** Using calibration residuals to silently rewrite historical readiness scores shown to the student, or to mint Twin Estimated Knowledge.

---

## 6. Recommendation usefulness calibration (SI-C2)

| Signal | Calibrates | Does not calibrate |
|--------|----------|--------------------|
| EF-ACCEPT / EF-REJECT | Preference / agency patterns | Tip “correctness” |
| EF-FOLLOW | Follow-through | Mastery |
| EF-LEARN (pack-backed) | Educational usefulness of guidance families | Automatic weight update |
| EF-REFLECT | Perceived usefulness (elevated, optional) | Ranking alone |
| EF-EXPLAIN | Strength-language honesty | Ranking |

Useful recommendation claims still require OM evidence packs per OM-001 Evidence Requirements. Calibration metadata supports honesty; LU-POL is required before behaviour change.

---

## 7. Digital Twin calibration inputs

| Allowed | Required fields | Forbidden |
|---------|-----------------|-----------|
| Facet-level provisional confidence metadata | evidence_refs, limitations, claim_boundary, C-class | Treating tip accept as knowledge certainty |
| Behaviour preference strength (provisional) | sample_size, window | Identity / motivation labels as facts |
| Calibration residual as *understanding caveat* | links to CalibrationRecord | Silent Knowledge State overwrite |

Twin Article II remains binding: unknown stays unknown; feedback that is thin must not manufacture confidence.

---

## 8. Explainability interaction

| Situation | Required action |
|-----------|-----------------|
| Softening future tip confidence language | P-001.2 checklist; cite CalibrationRecord |
| Strengthening language | C3+ pack + checklist Pass; PC-12 if thin |
| Student asks “why less confident?” | Trace to calibration limitations — no opaque score |
| Historical journal entry | Show frozen explanation; optionally append later evaluation stub (CP-001) |

---

## 9. Human review triggers for calibration

Mandatory review before applying LU-CAL that is student-facing when any of:

- Upward confidence change  
- New target_kind introduced  
- Cross-capability coupling (e.g. readiness band ↔ tip family)  
- n below pre-declared threshold but change still proposed  
- EF-CONFLICT unresolved  

Downward honesty disclosures with C2+ tables may use a lighter product-ops review if ADR so classifies — but must still be versioned and rollback-ready.

---

## 10. Non-goals

- No change to EP-004.1 confidence formula in this programme  
- No production calibration dashboards  
- No mutation of recommendation ranking via “confidence scores”  
- No LLM-estimated confidence  

---

**End of CP-002 Confidence Calibration**
