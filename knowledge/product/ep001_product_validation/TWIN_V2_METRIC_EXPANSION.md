# Twin V2 Metric Expansion

**Programme:** EP-001 — Workstream 3  
**Version:** 1.0  
**Status:** Design — no algorithm implementation in this document  
**Updated:** 2026-07-23  
**Authority:** EP-001 (explicit Twin programme authority for *evidence-backed* metric expansion only)

---

## 1. Purpose

Expand the Student Digital Twin with dimensions that improve recommendations — each with evidence, explainability, and a clear educational use.

No speculative scores. No dual Twin brains.

---

## 2. Existing dimensions (do not reinvent)

Already specified / present in `app/domain/student_twin/` and `knowledge/version2/STUDENT_DIGITAL_TWIN.md`:

| Dimension | Status | Notes |
|---|---|---|
| Confidence | Present | `ConfidenceState`, bands, evidence ids |
| Learning velocity | Present | `LearningVelocity` |
| Knowledge / mastery | Present | Topic beliefs |
| Retention (durability) | Present | Overlaps intended “knowledge decay” signal |
| Readiness | Present | With confidence band |
| Recommendations | Present | Why / evidence / expected benefit / confidence fields |

**Rule:** Prefer strengthening evidence inputs and explainability of existing dimensions before inventing parallel fields.

---

## 3. Proposed expansions

Every candidate must pass the gate in §4 before implementation PRD.

### M1 — Consistency (new composite)

| Field | Spec |
|---|---|
| **Meaning** | Evidence-backed study consistency posture (maps to Validation Framework O1). |
| **Evidence** | Session completion chronology + planned windows (when available). |
| **Explainability** | Rationale cites completed weeks, gaps, and evidence ids. |
| **Improves recommendations** | Prefer sustainable next actions when consistency is fragile; avoid overload when recent gaps. |
| **Relation** | Projection/summary — must not replace Mission/plan authorities. |

### M2 — Knowledge decay (clarify vs Retention)

| Field | Spec |
|---|---|
| **Meaning** | Rate / risk of retention decline after evidence gaps — **derived view of Retention**, not a second belief store. |
| **Evidence** | Same as RetentionEstimator + gap timing. |
| **Explainability** | “Decay risk high because last successful recall was N days ago (evidence ids…)”. |
| **Improves recommendations** | Surfaces revise_topic with urgency when decay risk rises. |
| **Implementation preference** | Expose as explainable derived metric on RetentionState / estimator output — avoid duplicate `decay_score` authority. |

### M3 — Revision efficiency

| Field | Spec |
|---|---|
| **Meaning** | Educational gain per completed revision window (maps to O3 + O4). |
| **Evidence** | Revision completed + subsequent recall/practice outcomes within benefit window. |
| **Explainability** | Cites before/after evidence ids and window id. |
| **Improves recommendations** | Prefer revision strategies that historically lift retention for this learner; deprioritise low-yield patterns. |
| **Phase** | Requires Phase 2 analytics pairing — not Phase 1. |

### M4 — Prediction confidence (readiness calibration meta)

| Field | Spec |
|---|---|
| **Meaning** | Confidence in the *prediction itself* (meta-uncertainty), distinct from learner self-confidence. |
| **Evidence** | Evidence volume, conflict, staleness, historical calibration error when available (O6). |
| **Explainability** | “Prediction confidence low: sparse evidence / conflicting outcomes”. |
| **Improves recommendations** | Softens strong claims when meta-confidence is low; prompts evidence-gathering Sessions. |
| **Relation** | Align with existing `ConfidenceBand` on readiness — extend explanation, avoid opaque second score unless necessary. |

### M5 — Confidence (learner) — enhancement only

Strengthen calibration pairing (Validation Framework O5). No new vanity confidence UI.

---

## 4. Admission gate (mandatory)

A Twin metric ships only if all are true:

1. **Evidence** — defined EvidenceType(s) or lawful derived inputs documented.
2. **Explainable** — every value carries rationale + evidence ids (or explicit insufficient_evidence).
3. **Improves recommendations** — at least one RecommendationKind behaviour change specified.
4. **Deterministic** — same evidence → same metric.
5. **No parallel truth** — does not override Mission, Curriculum, or Educational Evidence authorities.
6. **PRD approved** — implementation behind a numbered PRD under EP-001.
7. **Mapped to Validation Framework** outcome ID.

Fail any gate → defer.

---

## 5. Sequencing

1. Freeze Validation Framework (done).
2. Phase 1 analytics events (PRD-001) — feed consistency & Twin evolution observation.
3. PRD for M1 Consistency (first expansion candidate).
4. Clarify M2 as Retention derived view (docs + estimator explanation).
5. M3 / M4 after Phase 2 recommendation & outcome pairing.

---

## 6. Non-goals

- AI-owned Twin mutations
- Psychology diagnosis beyond evidence-backed confidence calibration
- Replacing Epic Twin production path without an explicit integration programme
- Learner-facing jargon “digital twin” (Product Language: learning profile)

---

## References

- `knowledge/version2/STUDENT_DIGITAL_TWIN.md`
- `docs/architecture/DIGITAL_TWIN_CONSTITUTION.md`
- `EDUCATIONAL_VALIDATION_FRAMEWORK.md`
- `app/domain/student_twin/`
