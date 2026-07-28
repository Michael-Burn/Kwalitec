# AP-002D — Evidence Boundary

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D — Educational Intelligence Integration  
**Status:** Design (authoritative)  
**Related:** [`INTEGRATION_SPECIFICATION.md`](INTEGRATION_SPECIFICATION.md), [`ARCHITECTURE_INVARIANTS.md`](../../engineering/ARCHITECTURE_INVARIANTS.md)

---

## 1. Purpose

Define a hard boundary between Assessment evidence production and Educational Intelligence consumption.

**No overlaps. No duplicated authority.**

---

## 2. Boundary diagram

```
┌─────────────────────────────────────────┐
│           ASSESSMENT SIDE               │
│  Session · Observations · EvidenceBundle│
│  (producer of facts & packaged evidence)│
└───────────────────┬─────────────────────┘
                    │ Evidence Boundary
                    │ (AP-001 ingress + DTOs)
                    ▼
┌─────────────────────────────────────────┐
│     EDUCATIONAL INTELLIGENCE SIDE       │
│  Reasoning · Twin · Graph · Mission     │
│  · Tutor                                │
└─────────────────────────────────────────┘
```

Crossing the boundary is a **one-way fact handoff**. Educational meaning is created only after the handoff, by Reasoning.

---

## 3. Ownership matrix (exclusive)

### 3.1 What Assessment owns

| Owns | Does not own |
|---|---|
| Assessment sessions, instruments, responses | Learner mastery / Estimated Knowledge |
| Engine observations and evidence dimensions | Knowledge gaps as Twin inferences |
| Evidence packaging (`EvidenceBundle`, strength bands as **quality**) | Recommendations / educational decisions |
| Session performance summaries (evidence-only) | Mission schedules |
| Export DTO for AP-001 (`export_for_ap001`) | Tutor prose as educational authority |
| Domain events: packaged / validated / created (facts) | Learning Graph relationship SoT |

Assessment remains an **evidence producer only**.

### 3.2 What Reasoning owns

| Owns | Does not own |
|---|---|
| Educational inference policy (`RuleRegistry`) | Raw response capture |
| Transformation of observations → mastery, gaps, confidence, recommendations | Instrument delivery UX |
| Deterministic decisions and explanations | Competing learner-state store |
| Refusal / honesty rules for thin evidence | Fabricating missing observations |

Only `StudentReasoningService` may transform evidence into educational understanding.

### 3.3 What Twin owns

| Owns | Does not own |
|---|---|
| Sole long-term learner educational belief (SoT) | Assessment scoring rules |
| Append-only observation store (facts) | Evidence packaging algorithms |
| Inferences written **via Reasoning** | Mission construction |
| Reasoning history / timeline for audit | Tutor conversation memory as SoT |

### 3.4 What Learning Graph owns

| Owns | Does not own |
|---|---|
| Structural relationships (prerequisites, recovery, related concepts) | Learner mastery as SoT |
| Projections refreshed from Twin belief | Independent recommendation engine |
| Traversal helpers for Mission / Reasoning | Assessment evidence packaging |

### 3.5 What Mission owns

| Owns | Does not own |
|---|---|
| Scheduling / structuring activities from decisions | Educational inferences |
| Eligibility / workload / density gates | Twin mastery writes |
| Assessment **intent** placement (AP-002E) | Re-scoring evidence |

### 3.6 What Tutor owns

| Owns | Does not own |
|---|---|
| Explanation, encouragement, next-action narration | Grades / alternate mastery |
| Session-scoped conversation memory | Twin inference mutation |

---

## 4. Boundary interface

### Lawful crossing artefacts

| Artefact | Direction | Notes |
|---|---|---|
| `EvidenceBundleDTO` / export payload | Assessment → Pipeline | Clean application boundary; no Twin types |
| AP-001 `AssessmentEvent` | Pipeline internal | Carries observation-shaped facts + metadata |
| Twin `Observation` | Pipeline → Twin | Append-only facts |
| `triggered_by` + observation ids | Pipeline → Reasoning | Audit linkage |

### Unlawful crossings

| Crossing | Why forbidden |
|---|---|
| Engine → `MasteryService` / Twin inference mutators | Bypasses Reasoning |
| Engine → Educational Reasoning Engine private API | Creates shadow policy / dual authority |
| Mission → Engine “set mastery” | Invents learner belief |
| Tutor → Twin write | Conversation ≠ SoT |
| Graph ← copy of mastery as durable SoT | Duplicate authority |
| Soft signal alone → high mastery language | Violates evidence-before-inference / EIP-002 |

---

## 5. Separation rules

1. **Assessment does not know the learner** as educational belief — only opaque student/twin ids for routing facts.
2. **Evidence is not knowledge** — packaging organises facts; it does not conclude understanding.
3. **Evidence strength ≠ confidence ≠ mastery** — three distinct concepts; never conflate in code or copy.
4. **No dual writers** — inference fields have exactly one write path: StudentReasoningService.
5. **No policy in adapters** — infrastructure maps persistence; it does not invent educational rules.

---

## 6. Cold-start at the boundary

When the Twin is thin:

- Assessment may still produce diagnostic evidence.
- Boundary still only admits facts.
- Reasoning must remain honest (uncertainty preserved).
- Mission must not invent certainty from empty belief.

Honesty is a Reasoning/Twin responsibility, not an Assessment packaging responsibility.

---

## 7. Enforcement (implementation expectations)

AP-002D implementation **shall**:

- Keep Assessment packages free of Twin / Reasoning imports that write inferences.
- Route bundle → AP-001 → ObservationService → StudentReasoningService.
- Add architecture tests that fail on Engine mastery writes.
- Version packaging (`PACKAGING_VERSION`) and reasoning (`ENGINE_VERSION`) independently.

See [`REASONING_CONTRACT.md`](REASONING_CONTRACT.md) and [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md).
