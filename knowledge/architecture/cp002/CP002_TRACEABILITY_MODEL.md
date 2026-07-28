# CP-002 — Learning Feedback Loop Traceability Model

**Programme:** CP-002 — Capability Programme  
**Version:** 1.0  
**Status:** Active — traceability architecture (design only)  
**Effective:** 2026-07-28  
**Companion to:** `CP002_LEARNING_FEEDBACK_ARCHITECTURE.md`  
**Constraint:** Traceability maps only — no runtime tracing code changed by this programme.

---

## 1. Purpose

Make every Learning Feedback Loop concern **traceable** to Vision 2030, OA-001, SI-001, OM-001, CP-001, explainability/recommendation law, Twin Constitution, and educational meaning — so future claims and implementations cannot invent orphan adaptation, silent re-ranking, or second brains.

---

## 2. Authority stack

```
Vision 2030 (philosophy; north star; agency; learning ≠ activity)
        ↓
OA-001 Product Constitution (PC-01…PC-12 operating law)
        ↓
SI-001 Student Intelligence (capability map; SI-H3 closed loops)
        ↓
OM-001 Outcomes Measurement (layers; catalogue; evidence packs)
        ↓
CP-001 Decision Journal Capability Architecture
        ↓
P-001.2 / P-001.3 (explainability + recommendation quality)
        ↓
Student Digital Twin Constitution (understanding ≠ certainty)
        ↓
EP-003.4 / ILE-005 / EP-004.1 (observation, educational review, profile baselines)
        ↓
CP-002 Learning Feedback Loop Capability Architecture (this programme)
        ↓
Future ADR-gated implementation programmes (LF-H1…)
```

**Conflict rule:** Higher authorities win. CP-002 specialises; it does not amend.

---

## 3. Educational meaning traceability (EF-*)

| EF code | Vision / educational intent | Primary SI | Primary OM / packs | Update class ceiling* |
|---------|-----------------------------|------------|--------------------|------------------------|
| **EF-ACCEPT** | Agency; highest-value next action offered | SI-C2 | OM-REC-03 | LU-OBS / LU-TWN behaviour |
| **EF-REJECT** | Honest incompleteness; lawful refusal | SI-C2, SI-C7 | OM-REC-09 | LU-OBS / LU-TWN behaviour |
| **EF-DEFER** | Agency without shame | SI-C2 | OM-REC-* | LU-OBS |
| **EF-FOLLOW** | Consistency; action after guidance | SI-C2, SI-C4 | OM-REC-07, OM-MSN-* | LU-OBS / LU-CAL |
| **EF-LEARN** | Learning ≠ activity; useful guidance | SI-C2, SI-C9 | OM-REC-08, OM-LRN-* | LU-POL candidate (gated) |
| **EF-READY** | Readiness honesty / calibration | SI-C3 | OM-RDY-04 | LU-CAL |
| **EF-REFLECT** | Reflect regularly; optional | SI-C5 | OM-REF-* | LU-CAL / elevated evidence |
| **EF-HABIT** | Consistency substrate | SI-C4, SI-C8 | OM-BHV-*, OM-CON-* | LU-OBS / LU-TWN |
| **EF-RECOVER** | Sustainable recovery | SI-C4 | OM-BHV-02 | LU-OBS / LU-CAL |
| **EF-EXPLAIN** | Explainable guidance | SI-C7 | OM-EXP-* | LU-CAL |
| **EF-INSUFF** | Prefer STOP / humility | SI-C9 | — | None behavioural |
| **EF-CONFLICT** | Prefer STOP; human review | SI-C9 | — | Checkpoint only |

\*Ceiling without additional governance; LU-POL always requires full gate regardless of EF code.

**Acceptance criterion:** Every feedback signal maps to this table via a required EF-* code.

---

## 4. SI-001 capability traceability

| SI capability | Loop contribution | Horizon note |
|---------------|-------------------|--------------|
| SI-C1 Twin | LU-TWN behaviour / calibration understanding inputs | LF-H3; Constitution binds |
| SI-C2 Recommendations | Qualified usefulness → LU-POL *proposals* only | Full gate; P-001.3 |
| SI-C3 Readiness | EF-READY → CalibrationRecord → LU-CAL | LF-H2 |
| SI-C4 Mission Intelligence | EF-FOLLOW / EF-RECOVER joins | Via CP-001 OutcomeLink |
| SI-C5 Reflection | EF-REFLECT elevated optional evidence | Non-coercive |
| SI-C6 Curriculum adaptation | Curriculum refs on aggregates | V1/V2 via CurriculumService |
| SI-C7 Explainability | Freeze preserved; speech gated | Continuous |
| SI-C8 Analytics | Reproducible qualified aggregates | No dual scoring brain |
| SI-C9 Outcome measurement | Consume OM packs; emit calibration honesty | Continuous |
| SI-C10 Experimentation | LU-EXP promote path only | Research ≠ production auto-apply |

SI-H3 “closed learning loops” is the primary horizon home for CP-002 without inventing SI-C11.

---

## 5. OM-001 layer and pack traceability

| Loop artefact | Primary OM layer | Example catalogue / pack use |
|---------------|------------------|------------------------------|
| EF-ACCEPT/REJECT/FOLLOW aggregates | L1 | OM-REC-03,07,09,10 |
| EF-LEARN proposals | L1 / L5 | OM-REC-08, OM-LRN-*; trial metrics |
| EF-READY calibration | L1 → L4 honesty | OM-RDY-04 (OM-RDY-06 only under L4) |
| EF-REFLECT | L1 | OM-REF-* |
| EF-EXPLAIN | L1 / L2 | OM-EXP-*; P-001.2 |
| LU-EXP promote | L5 | OM-TRIAL-*; Experimentation Guide |
| North-star claims from loop alone | **Forbidden** | L4 requires dedicated protocol — loop may inform, not declare |

Evidence pack schema fields (`pack_id`, `claim_boundary`, `confidence_class`, `limitations[]`, …) from OM-001 Evidence Requirements bind LU-POL / claim language.

---

## 6. CP-001 Decision Journal join map

| Journal element | Loop use |
|-----------------|----------|
| GuidanceSnapshot | What was offered (immutable) |
| ExplanationSnapshot | Freeze; never rewritten by loop |
| StudentChoice | EF-ACCEPT / EF-REJECT / EF-DEFER |
| OutcomeLink | EF-FOLLOW / EF-LEARN joins |
| ReflectionAttachment | EF-REFLECT |
| EvaluationStub | Append ILE-005-style review states / loop assessments |
| educational_purpose_code (EV-*) | Complementary to EF-*; both required when journal-sourced |

EV-* (purpose of the *decision*) and EF-* (meaning of the *feedback signal*) are distinct catalogues. A single DecisionRecord may emit multiple FeedbackSignals over time.

---

## 7. Product Constitution (PC) traceability

| PC | Loop obligation |
|----|-----------------|
| PC-01 | No engagement optimiser |
| PC-02 | Educational vs engineering boards for promotes |
| PC-03 / PC-04 | Claims cite audit + packs |
| PC-05 | Single authoritative policy version register (future impl) |
| PC-06 | ADR before structural apply |
| PC-07 | Blueprint → impl → Independent Review for significant LU-POL |
| PC-08 | Residual risks owned if deferred |
| PC-09 | Deterministic approved policies |
| PC-10 | CurriculumService ordering |
| PC-11 | Agency; no coercion scores |
| PC-12 | STOP when thin |

---

## 8. Explainability & recommendation law traceability

| Standard | Loop binding |
|----------|--------------|
| P-001.2 | Freeze; LU-CAL student speech gated; checklist on speech change |
| P-001.3 | Acceptance ≠ effectiveness; LU-POL requires review Pass/waiver |
| Explainability Review Checklist | Required when student-facing intelligence speech changes |
| Recommendation Review Checklist | Required when ranking/selection behaviour changes |

---

## 9. Twin Constitution traceability

| Article / principle | Loop binding |
|---------------------|--------------|
| Understanding ≠ certainty | LU-TWN provisional only |
| Unknown remains unknown | EF-INSUFF / sparse cells |
| Evidence before opinion | Qualification checklist |
| Not the student | No identity/destiny from feedback |
| Guidance quality purpose | Loop exists to improve honesty of guidance — not surveillance theatre |

---

## 10. Baseline substrate traceability

| Baseline | Relationship |
|----------|--------------|
| EP-003.4 | Class A observational input; remains record-only at emission |
| ILE-005 | Educational review semantics; Sensei self-review ≠ ranking engine |
| EP-004.1 | Optional behavioural summary consumer; not educational authority |
| LEARNING_FEEDBACK_ARCHITECTURE.md | Implementation architecture for EP-003.4 — not superseded |
| PERSONAL_LEARNING_PROFILE_ARCHITECTURE.md | Profile remains summariser; CP-002 governs *learning proposals* above it |

---

## 11. Acceptance criteria map

| Acceptance criterion | Trace |
|----------------------|-------|
| Every feedback signal has defined educational meaning | §3 EF-*; Ingestion Model mandatory `educational_meaning_code` |
| No feedback directly changes recommendation behaviour without governed review | Architecture §6–§7; Governance §4 |
| Feedback remains explainable and traceable | Architecture §10; this document; Governance §5 |
| Integrates with SI-001, CP-001, OM-001 | §4–§6; Architecture §3–§4 |
| No application behaviour changes | Programme constraint; Completion Report |
| Architecture only | Deliverable set under `knowledge/architecture/cp002/` |

---

## 12. Non-goals

- No OpenTelemetry / runtime span schema in this programme  
- No amendment of SI-001 / OM-001 / CP-001 files in place  
- No PROGRAMME_DASHBOARD row required by this package  

---

**End of CP-002 Traceability Model**
