# AP-002D — Implementation Plan

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D — Educational Intelligence Integration  
**Status:** Design — future implementation roadmap  
**Constraint:** Documentation in this folder is complete; **implementation is a separate engineering milestone**. Keep changes small and independently testable.

---

## 1. Goal

Wire AP-002C `EvidenceBundle` export across the Evidence Boundary into AP-001 → Twin observations → `StudentReasoningService`, with full traceability and no authority violations.

**Does not:** Redesign Twin / Reasoning / Mission / Graph / Tutor; implement AP-002E adaptive triggering; add LLM scoring.

---

## 2. Engineering tasks

### Task D1 — Freeze observation metadata contract

**Deliver:** Documented + tested schema for assessment observation metadata (correctness, confidence, hints, retries, timing, misconception tags, evidence_strength, packaging_version, session/instrument/intent ids).

**Tests:** Contract fixture round-trip; unknown keys ignored by Reasoning safely.

**Exit:** Schema published; packaging export aligns.

---

### Task D2 — Evidence Boundary adapter (Bundle → AP-001 events)

**Deliver:** Application adapter mapping `EvidenceBundleDTO` → one or more AP-001 `AssessmentEvent`s (or equivalent pipeline intake) without Twin inference writes.

**Tests:** Mapping preserves observation ids / evidence refs; invalid bundle refused; idempotent replay.

**Exit:** Export path callable; Architecture: no Engine → mastery imports.

---

### Task D3 — Pipeline ingress + Observation append

**Deliver:** Ensure events create Twin observations via `ObservationService` with lawful provenance (`assessment_pipeline:…`, session id).

**Tests:** Append-only; duplicate evidence_reference skipped; Twin inferences unchanged until Reasoning.

**Exit:** Facts land on Twin; mastery untouched pre-reason.

---

### Task D4 — Trigger StudentReasoningService

**Deliver:** After successful append, call `reason(twin, triggered_by=…, observation_ids=…)` through existing pipeline orchestration (prefer extending AP-001 rather than a new write channel).

**Tests:** Same inputs → same inferences; thin evidence does not promote high-mastery language; Reasoning history links observation ids.

**Exit:** End-to-end assessment → Twin belief update via Reasoning only.

---

### Task D5 — Reasoning rule consumption (minimal)

**Deliver:** Only the rule updates **needed** to consume new evidence dimensions / strength bands. No speculative rule rewrite.

**Tests:** Soft signals alone insufficient; strength gates respected; misconception tags influence gap specificity where rules already allow.

**Exit:** Rule diffs reviewed against educational integrity; `ENGINE_VERSION` bumped if semantics change.

---

### Task D6 — Traceability + Graph projection verification

**Deliver:** Audit helpers / tests reconstructing session → bundle → event → observation → reasoning run → Twin fields; confirm Graph `refresh_projections` still runs after persist.

**Tests:** Traceability reconstruction test; Graph not treated as mastery SoT.

**Exit:** Founder-diagnosable chain green.

---

### Task D7 — Architecture & regression guards

**Deliver:** Architecture tests forbidding Assessment Engine direct Twin inference writes; purity tests remain green; V1/V2 curriculum untouched.

**Tests:** Import boundary tests; existing AP-001 / SDT / packaging suites still pass.

**Exit:** CI green; no migrations unless additive and justified (prefer zero if metadata fits existing JSON fields).

---

## 3. Suggested sequence

```
D1 → D2 → D3 → D4 → D5 → D6 → D7
```

D5 may start in parallel after D1 freeze, but must not ship student-visible without D4.

---

## 4. Explicit non-goals (this implementation milestone)

- Mission adaptive assessment triggering (AP-002E)  
- Tutor deep interpret patterns beyond existing explain path  
- Founder analytics dashboards (AP-002F)  
- Twin aggregate redesign / new ObservationKind without coordination  
- LLM in Reasoning  

---

## 5. Release rules

1. Prefer feature flag if student-visible belief changes widen.  
2. Additive schema only; no Twin table drops.  
3. Completion report required on implementation.  
4. Explainability / recommendation checklists if student-facing intelligence surfaces change.  

---

## 6. Definition of done (implementation)

1. Evidence Bundle can update Twin **only** via Reasoning.  
2. Determinism holds.  
3. Traceability reconstructable.  
4. Architecture tests enforce Evidence Boundary.  
5. No Mission / Tutor authority creep.  
