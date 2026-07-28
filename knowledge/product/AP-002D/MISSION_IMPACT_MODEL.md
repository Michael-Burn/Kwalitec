# AP-002D — Mission Impact Model

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D — Educational Intelligence Integration  
**Status:** Design (authoritative)  
**Related:** [`AP-002/MISSION_INTEGRATION.md`](../AP-002/MISSION_INTEGRATION.md), [`INTEGRATION_SPECIFICATION.md`](INTEGRATION_SPECIFICATION.md)

---

## 1. Principle

New educational evidence influences future mission planning **only after** Reasoning updates Twin decisions.

Mission Engine continues consuming **decisions only**. It never consumes raw Evidence Bundles as authority and never invents inferences.

```
Evidence Bundle
    → Observations
    → StudentReasoningService
    → Twin decisions / gaps / recommendations
    → Mission Engine (next plan / refresh)
```

---

## 2. What changes for Mission after AP-002D

| Before richer evidence | After lawful integration |
|---|---|
| Missions see Twin state from existing practice / AP-001 paths | Missions additionally see Twin state informed by Assessment Engine evidence (same Twin SoT) |
| Assessment activities may be abstract placeholders | Evidence density/quality improves Twin usefulness; **scheduling of assessment intents remains AP-002E** |

AP-002D does **not** require Mission Engine redesign. It improves the decision inputs Mission already reads.

---

## 3. Decision inputs Mission may use

| Twin / Reasoning output | Mission use |
|---|---|
| Persistent gap + misconception tags | Prefer recovery path targeting that misconception |
| Stronger mastery confidence (reasoned) | Reduce redundant probes; advance Learning Mode lawfully |
| Unchanged / high uncertainty | Avoid declaring success; schedule teaching or alternate evidence |
| Calibration issues (confidence vs correctness) | Prefer confidence-aware practice + Tutor encouragement |
| Recommendations / educational decisions | Map to activity selection and ordering |
| Learning Graph recovery / prerequisite paths | Structure lawful sequencing |

Mission must still honour workload, burnout, density, and Learning Mode authority.

---

## 4. What Mission must never do

| Prohibition | Rationale |
|---|---|
| Read EvidenceBundle as mastery | Crosses Evidence Boundary unlawfully |
| Re-score assessment responses | Dual evaluation path |
| Write Twin inferences | Violates Reasoning authority |
| Force quizzes for product theatre | Over-assessment / anxiety risk |
| Treat thin evidence as “passed checkpoint → mastered” | Educational dishonesty |

---

## 5. Mission refresh trigger

Existing AP-001 pipeline may optionally refresh missions after reasoning (`refresh_mission`). AP-002D preserves that pattern:

1. Evidence ingress + Reasoning completes.
2. Twin decisions update.
3. Optional mission refresh consumes **new decisions**.
4. If refresh is off, next generation cycle picks up updated Twin state.

Refresh is a **consumer convenience**, not a second reasoning engine.

---

## 6. Forward link to AP-002E

Adaptive triggering (when missions schedule diagnostic / revision / checkpoint / recovery / verification assessments) is **out of scope for AP-002D implementation**.

AP-002D only ensures that when those assessments later run, their evidence improves Twin decisions that Mission already consumes.

Eligibility gates and intent policies remain as designed in `AP-002/MISSION_INTEGRATION.md`.
