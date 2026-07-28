# CP-001 — Decision Journal Traceability Model

**Programme:** CP-001 — Capability Programme  
**Version:** 1.0  
**Status:** Active — traceability architecture (design only)  
**Effective:** 2026-07-28  
**Companion to:** `CP001_DECISION_JOURNAL_ARCHITECTURE.md`  
**Constraint:** Traceability maps only — no runtime tracing code changed by this programme.

---

## 1. Purpose

Make every Decision Journal concern **traceable** to Vision 2030, OA-001, SI-001, OM-001, explainability/recommendation law, Twin Constitution, and educational purpose — so future claims and implementations cannot invent orphan metrics or silent second brains.

---

## 2. Authority stack

```
Vision 2030 (philosophy; north star; agency; reflection)
        ↓
OA-001 Product Constitution (PC-01…PC-12 operating law)
        ↓
SI-001 Student Intelligence (capability map; horizons)
        ↓
OM-001 Outcomes Measurement (layers; catalogue; evidence packs)
        ↓
P-001.2 / P-001.3 (explainability + recommendation quality)
        ↓
Student Digital Twin Constitution (understanding ≠ certainty)
        ↓
ILE-011 Decision Framework + ILE-002 Journal product baseline
        ↓
CP-001 Decision Journal Capability Architecture (this programme)
        ↓
Future ADR-gated implementation programmes
```

**Conflict rule:** Higher authorities win. CP-001 specialises; it does not amend.

---

## 3. Educational purpose traceability

Every DecisionRecord carries `educational_purpose_code` (Architecture §8). Mapping:

| Purpose code | Vision / educational intent | Primary SI | Primary OM families |
|--------------|-----------------------------|------------|---------------------|
| **EV-NEXT** | Highest-value next action | SI-C2 | OM-REC-* |
| **EV-REVISE** | Revision / weak-topic repair | SI-C2, SI-C6 | OM-REC-*, OM-LRN-02/03 |
| **EV-MISSION** | Consistency via Mission/Session | SI-C4 | OM-MSN-*, OM-REC-07 |
| **EV-RECOVER** | Sustainable recovery | SI-C4 | OM-BHV-02, OM-CON-05 |
| **EV-READY** | Readiness honesty | SI-C3 | OM-RDY-*, OM-EXP-05 |
| **EV-REFLECT** | Reflect regularly | SI-C5 | OM-REF-* |
| **EV-MILESTONE** | Continuity of learning journey | SI-C8 | OM-LNG-* (supporting) |
| **EV-REFUSE** | Honest incompleteness / agency | SI-C7 | OM-EXP-05, OM-REC-09 |

**Acceptance criterion:** No recorded decision without a purpose code that maps to this table.

---

## 4. SI-001 capability traceability

| SI capability | Journal contribution | Horizon note |
|---------------|----------------------|--------------|
| SI-C1 Twin | Behaviour/preference signals only | DJ-H3 for reflection→Evidence |
| SI-C2 Recommendations | Disposition + chain links | DJ-H1 completeness |
| SI-C3 Readiness | Advisory honesty entries; never certainty theatre | Humble EV-READY |
| SI-C4 Mission Intelligence | Commit/complete mirrors | Link OM-MSN |
| SI-C5 Reflection | Optional attachments | Non-coercive |
| SI-C6 Curriculum adaptation | Curriculum refs on snapshots | V1/V2 via CurriculumService |
| SI-C7 Explainability | ExplanationSnapshot freeze | Continuous |
| SI-C8 Analytics | Source of truth for decision completeness | No parallel scoring brain |
| SI-C9 Outcome measurement | L1 guidance evidence substrate | OM packs |
| SI-C10 Experimentation | Pre/post disposition evidence for trials | Research ≠ production |

---

## 5. OM-001 metric traceability

### 5.1 Guidance causal chain

| Chain stage (OM Outcome Model §8) | Journal artefact |
|-----------------------------------|------------------|
| Eligible guidance shown | DecisionRecord + eligibility |
| Understood | ExplanationSnapshot (+ OM-REC-02 / OM-EXP-*) |
| Accepted / deferred / refused | StudentChoice disposition |
| Started | OutcomeLink `mission_started` / EvidenceEvent |
| Completed | OutcomeLink `mission_completed` |
| Behavioural consistency | Aggregate dispositions over windows (ops) |
| Learning movement | OutcomeLink with `learning_signal` boundary — never invented |
| Calibrated prediction / L4 | Outside journal authority; journal may supply covariates only |

### 5.2 Catalogue ID ownership

| OM ID | Journal role |
|-------|--------------|
| OM-REC-01…05 | Impressions + dispositions |
| OM-REC-06…08 | Time-to-start / accept→complete / learning movement via OutcomeLinks |
| OM-REC-09 | Chronic dismiss signal (ops) |
| OM-REC-10 | Completeness of disposition capture |
| OM-EXP-01…05 | Frozen explanation compliance / refusal |
| OM-REF-01…04 | ReflectionAttachment participation / sensitivity |
| OM-MSN-* | When Mission outcomes linked |
| OM-BHV-* / OM-CON-* | Supporting aggregates from dispositions — never sole success |

---

## 6. Explainability & recommendation law traceability

| Law artefact | Journal binding |
|--------------|-----------------|
| P-001.2 Mandatory Schema | ExplanationSnapshot fields |
| P-001.2 Levels 1–3 | `explanation_level` |
| P-001.2 P9 (no AI-authored truth) | No post-hoc reason invention |
| P-001.3 Decision Framework | Eligible primary recommendations are journal-eligible |
| P-001.3 acceptance/effectiveness | OM-REC chain via journal |
| Explainability Review Checklist | Required for future speech-changing programmes |
| Recommendation Review Checklist | Required for future ranking/selection programmes |

---

## 7. Twin Constitution traceability

| Twin article / domain | Journal rule |
|-----------------------|--------------|
| Understanding ≠ certainty | Dispositions ≠ mastery |
| Unknown remains unknown | Sparse evidence → EV-REFUSE / humble confidence |
| Knowledge domain | Journal must not write Estimated Knowledge |
| Performance domain | May link practice OutcomeLinks; does not own performance math |
| Behaviour domain | Primary lawful Twin input class from dispositions/tags |
| Memory domain | Journal *is* educational continuity memory — complementary, not Twin replacement |
| Goals domain | May reference exam-date context in snapshots; no destiny claims |
| Evidence before opinion | Freeze evidence_summary at show time |

---

## 8. OA-001 / Product Constitution traceability

| Principle | Journal enforcement |
|-----------|---------------------|
| PC-01 Trust > features | Significant decisions only; no spam |
| PC-03 Claims ≤ evidence | Acceptance ≠ learning claim |
| PC-04 Traceable evidence | decision_id + recommendation_ref + OM packs |
| PC-06 ADR before structure | Schema/Twin-write changes need ADR |
| PC-09 Deterministic cores | Journal records; does not re-rank |
| PC-10 Curriculum truth | CurriculumService refs; V1/V2 |
| PC-11 Agency | Optional rationale; no coercion |
| PC-12 STOP | Thin evidence → refuse certainty theatre |

---

## 9. Baseline product artefact traceability

| Artefact | Relationship |
|----------|--------------|
| ILE-002 Philosophy / Lifecycle / Retention | Product baseline substrate |
| ILE-003 Educational Timeline | Reader of journal; not second store |
| ILE-004 Daily Mission Intelligence | May mirror Mission moments into journal |
| ILE-005 Feedback Loop | Reviews outcomes; never rewrites history |
| ILE-011 Decision Framework / Lifecycle | Agency and Sensei loop philosophy |
| EP-008.3 Commitment | Mission commit/defer/complete mirror posture |
| SI001 Recommendation Roadmap | Journal as accept/dismiss substrate |
| SI001 Outcome Measurement Framework | Seed; OM-001 permanent law |
| Product Analytics Architecture | Distinct from educational memory |

---

## 10. End-to-end join keys (design)

For future instrumentation programmes, the following conceptual keys make the recommendation → choice → behaviour → outcome chain reconstructable:

| Key | Joins |
|-----|-------|
| `learner_id` | Ownership scope |
| `decision_id` | Journal aggregate |
| `recommendation_ref` | Engine / tip / brief identity |
| `catalogue_decision_id` | ILE-011 catalogue |
| `mission_id` / `session_id` | Authoritative study commitment |
| `evidence_ref` | Runtime A / Evidence facts |
| `reflection_ref` | Guided reflection experience |
| `om_pack_id` / metric window | Measurement membership |

Missing keys must be disclosed as completeness gaps (OM-REC-10), not imputed.

---

## 11. Claim → evidence quick map

| Claim language | Minimum evidence (design) |
|----------------|---------------------------|
| “Recommendations are useful” | P-001.3 Pass + OM-REC-03,07,10 Decision Journal pack |
| “Students understand why” | OM-EXP-01/03 + frozen ExplanationSnapshots |
| “Improves learning” | OM-REC-08 and/or OM-LRN-* with lawful claim boundary |
| “Reflection helps” | OM-REF-* non-coercive; no participation inflation |
| “Twin knows the student” | Twin health packs — **not** journal accept rates alone |
| “Raises exam pass probability” | L4 consented protocol only — journal insufficient |

---

## 12. Explicit non-goals

- Implementing distributed tracing or OpenTelemetry in this programme  
- Recomputing KSI or clearing Gate G1  
- Amending SI-001 / OM-001 documents in place  

---

**End of CP001_TRACEABILITY_MODEL**
