# CP-002 — Learning Feedback Loop Capability Architecture

**Programme:** CP-002 — Capability Programme  
**Version:** 1.0  
**Status:** Active — Learning Feedback Loop capability architecture (design only)  
**Effective:** 2026-07-28  
**Change class:** Architecture & Product Capability  
**Constraint:** No application behaviour, schema, recommendation algorithms, or UI modified by this programme.

---

## 1. Purpose

Define the **Learning Feedback Loop** as a durable Student Intelligence capability: the governed path that connects validated educational outcomes back into Student Intelligence — so Kwalitec can learn from evidence without uncontrolled self-modification.

The loop answers one architectural question:

> How does evidence of educational usefulness improve future understanding and guidance **without** letting observations silently re-rank, re-plan, or invent certainty?

This package is **capability architecture only**. It does not implement collectors, change ranking, mutate Twin Knowledge State, or amend EP-003.4 / ILE-005 / EP-004.1 runtimes.

---

## 2. Authority and non-contradiction

| Authority | Binding effect |
|-----------|----------------|
| **Vision 2030** | Learning ≠ activity; agency; reflection; never-build opaque AI / coercive optimisation |
| **OA-001 Product Constitution** | PC-01 trust; PC-03–PC-04 claims ≤ evidence; PC-06 ADR-before-implementation; PC-09 determinism; PC-11 agency; PC-12 STOP |
| **SI-001** | Closed learning loops at SI-H3; SI-C2/C3/C5/C7/C8/C9 ownership; no second educational brain |
| **OM-001** | Outcome layers L1–L5; evidence packs; catalogue IDs; claim boundaries |
| **CP-001** | Decision Journal as primary guidance-memory and OM substrate |
| **P-001.2 Explainability Standard** | Explanation schema; confidence honesty; freeze at guidance time |
| **P-001.3 Recommendation Quality Standard** | Acceptance ≠ effectiveness; ranking changes require review |
| **Student Digital Twin Constitution** | Understanding ≠ certainty; feedback must not mint mastery or destiny |
| **EP-003.4 Learning Feedback** | Observational behavioural evidence baseline (record-only; flag OFF default) |
| **ILE-005 Educational Feedback Loop** | Educational calibration philosophy — measure/reflect; do not re-rank |
| **EP-004.1 Personal Learning Profile** | Behavioural summarisation with confidence — not educational authority |

**Conflict rule:** Vision 2030 and Educational Constitution win on philosophy and educational meaning. Twin Constitution wins on understanding vs certainty. OA-001 wins on claim discipline. OM-001 wins on outcome semantics. CP-001 wins on decision-memory structure. EP-003.4 / ILE-005 / EP-004.1 remain product baselines for observation, educational review philosophy, and profile aggregation. CP-002 specialises *capability architecture* for governed learning from evidence; it does not soft-amend those authorities.

---

## 3. Capability definition

### 3.1 What the Learning Feedback Loop is

The Learning Feedback Loop is the **governed pipeline** that:

1. **Ingests** qualified signals from Decision Journal, observational Learning Feedback, outcome packs, and optional reflection  
2. **Qualifies** each signal with educational meaning, claim boundary, and confidence class  
3. **Proposes** bounded learning updates (confidence calibration, Twin behaviour inputs, recommendation-policy candidates)  
4. **Requires** human / ADR / educational-governance checkpoints before any change that affects recommendation behaviour  
5. **Preserves** explainability freeze, audit trail, and rollback

| Property | Meaning |
|----------|---------|
| **Educational learning** | Improves honesty of understanding and usefulness of guidance from evidence |
| **Governed adaptation** | Behaviour-affecting changes only after review — never silent auto-re-rank |
| **Explainable loop** | Every accepted update cites evidence refs, purpose codes, and limitations |
| **Constitutional humility** | Sparse or conflicting evidence yields STOP / inconclusive — not invented certainty |
| **SI substrate** | Serves SI-H3 closed loops without inventing SI-C11 or a second brain |

### 3.2 What the Learning Feedback Loop is not

| Not | Why |
|-----|-----|
| Online reinforcement / auto-tuning of ranking weights | Violates PC-09 and P-001.3 review law |
| Telemetry vanity optimiser | Engagement ≠ learning (Vision 2030) |
| Twin mastery writer from clicks | Twin Constitution Art. II / V |
| Replacement for Recommendation / Planning / Readiness authority | EP-002.9 ownership intact |
| Product Analytics clickstream | Analytics remains organisational; this loop is educational |
| Unbounded LLM self-improvement | Never-build opaque AI in core learning path |

### 3.3 Relationship to existing substrates

| Layer | Owner | CP-002 role |
|-------|-------|-------------|
| Observational events (record-only) | EP-003.4 | **Input class A** — behavioural observations |
| Decision Journal memory | CP-001 / ILE-002 | **Input class B** — guidance + choice + explanation freeze |
| Educational review philosophy | ILE-005 | **Review semantics** — supported / inconclusive / insufficient |
| Personal Learning Profile | EP-004.1 | **Optional behavioural summary** — confidence-gated evidence only |
| Outcome packs / catalogue | OM-001 | **Qualification law** — layers, claim boundaries, pack schema |
| Capability architecture (governed learning) | **This programme (CP-002)** | Pipeline, boundaries, checkpoints, rollback |
| Ranking / planning / readiness maths | Runtime A owners | **Unchanged** unless future ADR-gated programme cites CP-002 + review Pass |

CP-002 **does not** reopen EP-003.4, ILE-005, EP-004.1, or recommendation algorithm implementation. Future enhancement programmes must cite CP-002 + ADR (PC-06) before structural change.

---

## 4. Placement in Student Intelligence

### 4.1 Capability map placement

Learning Feedback Loop is a **cross-cutting capability substrate**, not an eleventh SI capability ID. It serves SI-H3 (“closed learning loops”) across:

| SI capability | Loop role |
|---------------|-----------|
| **SI-C2** Recommendation Engine | Qualified outcome → *proposal* for policy/review; never silent re-rank |
| **SI-C3** Study Readiness | Calibration tables and honesty updates (predicted vs later outcome) |
| **SI-C5** Reflection Intelligence | Optional reflection as elevated evidence class (privacy-bound) |
| **SI-C7** Explainability | Preserve freeze; attach loop provenance to any future speech change |
| **SI-C8** Learning analytics | Reproducible aggregates of qualified feedback — no dual scoring brain |
| **SI-C9** Outcome measurement | Consume OM packs; feed L1→L5 honesty |
| **SI-C1** Digital Twin | Lawful behaviour / preference / calibration *understanding* inputs only |
| **SI-C10** Experimentation | Trial-gated promotes only; research ≠ production auto-apply |

### 4.2 Layering (normative)

```
Templates/JS → Blueprints → Services → Models + Curriculum Engine → DB/JSON
                     ↑
         Learning Feedback Loop Capability (governed learning proposals)
                     ↑
         Qualification + Review Gate (human / ADR / EVF as required)
                     ↑
         Decision Journal (CP-001) + Observational Feedback (EP-003.4) + OM packs
                     ↑
         Twin Foundation (may read lawful loop outputs as understanding)
                     ↑
         Runtime A educational writes / recommendation authority (unchanged by loop alone)
```

| Layer | May | Must not |
|-------|-----|----------|
| Presentation | Show student-safe reflection prompts; never expose Sensei self-review as ranking | Auto-apply ranking changes |
| Blueprints | Authz, ownership scope | Planning / recommendation math |
| Loop services (future) | Ingest, qualify, propose, audit, rollback metadata | Depend on `flask.request` globals; mutate ranking without gate |
| Twin | Interpret lawful loop outputs as provisional understanding | Treat accept rates as mastery certainty |
| Recommendation / Planning / Readiness | Consume only **approved**, confidence-gated evidence via Ports | Delegate constitutional authority to the loop |

---

## 5. End-to-end loop (normative stages)

```
[1] Signal sources
        │  Decision Journal · EP-003.4 events · OM evidence packs · optional reflection
        ▼
[2] Educational taxonomy tagging   ← every signal gets EF-* meaning (see §8)
        ▼
[3] Evidence qualification         ← claim boundary, confidence class, eligibility
        ▼
[4] Learning proposal draft        ← calibration / Twin input / policy candidate
        ▼
[5] Human / governance checkpoint  ← required before recommendation-behaviour change
        ▼
[6] Approved update application    ← versioned; auditable; explainable
        ▼
[7] Audit trail + rollback handle
```

**Hard stop:** Stages [4]→[6] for recommendation-behaviour changes **may not skip** [5]. Observational recording alone (EP-003.4 style) may stop at [1]–[3] without proposals.

---

## 6. Learning update classes

Every proposal belongs to exactly one primary update class:

| Class | Meaning | May affect student-facing recommendation behaviour? | Gate |
|-------|---------|-----------------------------------------------------|------|
| **LU-OBS** | Record / aggregate observation only | No | None beyond existing flags |
| **LU-CAL** | Confidence / calibration metadata update | Indirect only (honesty bands, disclosure) | Review for student-facing speech |
| **LU-TWN** | Twin behaviour / preference / calibration understanding | No ranking; Twin understanding only | Twin Constitution + ADR if write path new |
| **LU-POL** | Recommendation / planning *policy candidate* | Yes, if applied | **Mandatory** human + ADR + P-001.3 (and P-001.2 if speech) |
| **LU-EXP** | Experiment promote / reject | Yes only via SI-C10 promote path | Pre-registration + Independent Review |

**Acceptance criterion (programme):** No feedback directly changes recommendation behaviour without governed review — i.e. LU-POL / LU-EXP always pass checkpoint [5].

---

## 7. Recommendation learning boundaries

| Bound | Rule |
|-------|------|
| **B1 — Observe ≠ decide** | Accept / dismiss / complete events never auto-adjust ranking weights |
| **B2 — Effectiveness ≠ acceptance** | OM-REC learning movement required before “useful recommendation” claims (P-001.3 / OM-001) |
| **B3 — Determinism preserved** | Any approved policy change remains reproducible from versioned inputs (PC-09) |
| **B4 — No opaque optimisers** | No black-box RL / LLM weight updates in the core path |
| **B5 — Curriculum truth first** | Feedback cannot invent topic order outside CurriculumService |
| **B6 — Agency intact** | Rejection / deferral remain lawful; never coerced into “bad student” scores (PC-11) |
| **B7 — Flag honesty** | Loop outputs under OFF flags must not be narrated as live adaptation |

Personal Learning Profile (EP-004.1) and any future personalisation remain **evidence consumers** with confidence gates — they do not own ranking.

---

## 8. Educational feedback taxonomy (EF-*)

Every feedback signal carries exactly one primary **educational meaning code**. Dual primary codes are forbidden; secondary tags allowed.

| Code | Educational meaning | Typical sources | Typical OM families |
|------|---------------------|-----------------|---------------------|
| **EF-ACCEPT** | Student accepted offered guidance | Decision Journal choice; EP-003.4 accept | OM-REC-03 |
| **EF-REJECT** | Student rejected / dismissed guidance (lawful agency) | Decision Journal; EP-003.4 dismiss | OM-REC-09 |
| **EF-DEFER** | Student deferred guidance | Decision Journal | OM-REC-* |
| **EF-FOLLOW** | Student started / completed linked learning action | OutcomeLink; plan_completed | OM-REC-07, OM-MSN-* |
| **EF-LEARN** | Evidence-backed learning movement after guidance | OM learning packs; attempts | OM-REC-08, OM-LRN-* |
| **EF-READY** | Readiness prediction vs later outcome (calibration) | Readiness + attempts | OM-RDY-04 |
| **EF-REFLECT** | Optional student reflection on guidance usefulness | Reflection attachment | OM-REF-* |
| **EF-HABIT** | Study habit / consistency observation | EP-003.4 consistency | OM-BHV-*, OM-CON-* |
| **EF-RECOVER** | Recovery / revision adherence signals | planning feedback events | OM-BHV-02 |
| **EF-EXPLAIN** | Explainability usefulness / emptiness signals | Explanation review samples | OM-EXP-* |
| **EF-INSUFF** | Explicitly insufficient evidence to judge | ILE-005 review state | — |
| **EF-CONFLICT** | Conflicting signals requiring STOP / human review | Multi-source conflict | — |

**Acceptance criterion:** Every feedback signal has a defined educational meaning (EF-* required at ingestion).

Full qualification rules: `CP002_EVIDENCE_INGESTION_MODEL.md`.

---

## 9. Digital Twin learning inputs

| Allowed Twin input (provisional) | Forbidden Twin conclusion from feedback alone |
|----------------------------------|-----------------------------------------------|
| Behaviour preference refs (accept/dismiss patterns) | Estimated Knowledge / mastery minting |
| Habit / consistency observations (with limitations) | Destiny, worth, or “unmotivated” identity |
| Calibration residuals for readiness honesty | Certainty of understanding from tip acceptance |
| Provenance-linked confidence about *understanding quality* | Silent Knowledge State overwrite without authority |

Twin remains understanding, never certainty. Loop outputs entering Twin must carry `evidence_refs`, `claim_boundary`, `limitations`, and confidence class. Details: `CP002_CONFIDENCE_CALIBRATION.md` § Twin.

---

## 10. Explainability preservation

| Rule | Meaning |
|------|---------|
| **Freeze intact** | Decision-time ExplanationSnapshot (CP-001 / P-001.2) is never rewritten by later feedback |
| **Append only** | Loop assessments append evaluation stubs; history is immutable |
| **Speech changes gated** | Any student-facing confidence or tip speech change requires P-001.2 checklist Pass (or waiver) |
| **Disclose uncertainty** | Calibrated confidence may lower claimed strength; it must not invent stronger certainty |
| **Sensei self-review private** | ILE-005-style internal educational review is governance memory — not a second tip engine |

Companions: `CP002_GOVERNANCE_SAFEGUARDS.md`, P-001.2.

---

## 11. Audit trail and rollback (summary)

Every accepted LU-CAL / LU-TWN / LU-POL / LU-EXP update must produce:

- Versioned proposal id  
- Evidence refs + EF-* codes + OM metric ids  
- Reviewer / gate decision + date  
- Before/after parameter or policy version pointers  
- Rollback handle to prior version  

Rollback is first-class — silent irreversible adaptation is forbidden. Detail: `CP002_GOVERNANCE_SAFEGUARDS.md`.

---

## 12. Constitutional safeguards (summary)

| Safeguard | Source |
|-----------|--------|
| STOP on thin evidence | PC-12 |
| Claims ≤ filed packs | PC-03, PC-04, OM-001 |
| ADR before structural apply | PC-06 |
| Deterministic cores | PC-09 |
| Student agency | PC-11 |
| Understanding ≠ certainty | Twin Constitution |
| No second educational brain | EP-002.9 / SI-001 |
| Observe ≠ adapt without gate | This architecture §6–§7 |

Full table: `CP002_GOVERNANCE_SAFEGUARDS.md`.

---

## 13. Horizons (design only)

| Horizon | Intent | Not claimed by CP-002 |
|---------|--------|------------------------|
| **LF-H0** | Architecture freeze (this package) | Runtime |
| **LF-H1** | Durable qualification + audit stores joined to CP-001 / OM packs | Implementation |
| **LF-H2** | Calibration dashboards + readiness honesty loops (LU-CAL) | Production claims |
| **LF-H3** | Governed LU-POL under P-001.3 + ADR; Twin LU-TWN under Constitution | Auto-adaptation |
| **LF-H4** | SI-C10 experimental promote path integrated | North-star overclaim |

---

## 14. Non-goals of this programme

- No application code, schema, UI, or algorithm changes  
- No enabling of `ENABLE_LEARNING_FEEDBACK` or profile flags  
- No KSI raise or Version 1 production-ready claim  
- No amendment of SI-001 / OM-001 / CP-001 documents in place (references only)

---

## 15. Companion documents

| Document | Role |
|----------|------|
| `CP002_EVIDENCE_INGESTION_MODEL.md` | Ingestion + qualification + taxonomy binding |
| `CP002_CONFIDENCE_CALIBRATION.md` | Calibration update model |
| `CP002_GOVERNANCE_SAFEGUARDS.md` | Review checkpoints, constitutional safeguards, rollback |
| `CP002_TRACEABILITY_MODEL.md` | Vision → SI → OM → CP-001 → CP-002 maps |
| `CP002_COMPLETION_REPORT.md` | Programme completion |

---

**End of CP-002 Learning Feedback Loop Architecture**
