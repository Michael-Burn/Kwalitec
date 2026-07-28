# OM-001 — Experimentation Guide

**Programme:** OM-001 — Outcomes Measurement  
**Version:** 1.0  
**Status:** Active — educational experimentation guide (design only)  
**Effective:** 2026-07-28  
**Companion to:** `OM001_OUTCOME_MODEL.md`, `OM001_MEASUREMENT_STANDARD.md`, `OM001_EVIDENCE_REQUIREMENTS.md`  
**Constraint:** No trials enabled, advisory fields expanded, or algorithms changed by this programme.

---

## 1. Purpose

Define how Kwalitec designs, runs, reviews, and interprets **educational experiments** so that research evidence stays distinct from production behaviour and marketing claims.

This guide operationalises SI-001 research principles and P4-MS001 trial law into permanent experimentation doctrine. It does **not** authorise any experiment.

---

## 2. Research vs production (hard separation)

| Domain | May do | Must not do |
|--------|--------|-------------|
| **Research / L5** | Pre-registered trials; exploratory analyses labelled C0; consented L4 protocols | Silently rewrite production policy from thin lift |
| **Production Runtime A** | Serve authorised educational behaviour under flags and claim class | Apply unreviewed treatment; invent second educational brain |
| **Marketing / release language** | Cite Independent Review packs within claim class | Narrate exploratory or underpowered results as “proven” |
| **Engineering shadow / dual-run** | Measure agreement (L3) | Equate shadow agreement with educational benefit |

**Invariant:** Experimentation informs production via OA-001 Feature Lifecycle (Blueprint → Implementation → Independent Review) and ADR when structural. Lift alone never auto-promotes policy (PC-12; P4 stop condition).

```
Research question (SI Research Backlog / OM protocol)
        ↓
Blueprint + pre-registration (metrics, MDE, ethics)
        ↓
Implementation under flag (default OFF)
        ↓
Observation window
        ↓
Immutable summary / evidence pack
        ↓
Independent Review
        ↓
    ┌───┴───┐
 STOP     Promote via dedicated programme + ADR (if structural)
```

---

## 3. Experiment classes

| Class | Description | Confidence class | Production impact |
|-------|-------------|------------------|-------------------|
| **E0 Exploratory analysis** | Offline / ops query on existing logs | C0 | None — hypothesis only |
| **E1 Instrumentation-only** | New metric collection without behavioural change | C1 | None to recommendations |
| **E2 Controlled operational trial** | Deterministic baseline vs treatment on locked surface | C3 | Treatment only under trial gate + flags |
| **E3 Quasi-experiment / observational comparative** | Natural cohorts, before/after | C2 | None automatic |
| **E4 Longitudinal transfer study** | Consented exam / pass-probability linkage | C4 | Research only until separate product decision |

**P4-MS001** is the existing **E2** instrument: advisory field locked to `consistency_summary`; `ENABLE_EDUCATIONAL_TRIALS` default OFF.

---

## 4. Pre-registration requirements (E2–E4)

Before treatment exposure (or before outcome peek for E3/E4), record:

1. **Hypothesis** — educational benefit in student language  
2. **Primary metric** — one `metric_id` from the catalogue (or versioned new metric)  
3. **Secondary metrics** — limited list; no fishing for the “best” story  
4. **MDE / success criterion** — what lift would justify continuation  
5. **Window** — start/end or duration rule  
6. **Eligibility** — inclusion/exclusion; consistent-user definition if used  
7. **Assignment method** — for E2: salt, rollout %, deterministic rule  
8. **Stop / harm rules** — when to pause (worsening consistency, trust, workload)  
9. **Claim boundary** — what the result may and may not say  
10. **Ethics / privacy checklist** — §8  

Artefact path becomes part of the evidence pack (`OM001_EVIDENCE_REQUIREMENTS.md`).

---

## 5. Trial design standards (E2)

Aligned with `EDUCATIONAL_TRIAL_ARCHITECTURE.md`.

| Requirement | Standard |
|-------------|----------|
| Config immutability | Trial config frozen once active |
| Deterministic cohorts | Same `(trial_id, salt, student_id)` → same bucket |
| Opaque keys | No raw PII on observation / summary DTOs |
| Locked treatment surface | Only authorised advisory fields / behaviours |
| Nested gates | Trial gate + policy/engine gates both apply |
| Fail-open | Flag OFF → prior production behaviour |
| Reversible | Pause / rollout 0% / flag OFF restores baseline path |
| Runtime A authority | Trial does not become a second educational write brain |
| Summaries immutable | `TrialSummary`-class artefacts for review |

**Expansion rule:** Expanding beyond `consistency_summary` requires a dedicated programme + architecture review + ADR if structural — not an OM-001 exception.

---

## 6. Analysis standards

1. Analyse primary metric first; secondaries are supportive.  
2. Report absolute rates and `n` for baseline and treatment — not relative lift alone.  
3. Disclose contamination (other flags, concurrent programmes).  
4. Do not infer mastery or exam success from operational acceptance/completion alone.  
5. Engineering dual-run divergence is reported separately (L3), never as L5 lift.  
6. Multiple comparisons: if many secondaries, pre-state adjustment or label exploratory.  
7. Underpowered non-significant results → **inconclusive**, not “no effect proven.”  
8. Harm signals (drop in consistency, spike in dismiss-without-alternative, workload distress) trigger STOP review even if primary metric “wins.”

---

## 7. Independent Review and promotion

Per Product Constitution PC-07 and SI research principles:

| Step | Owner capacity (Founder-operated) | Output |
|------|-----------------------------------|--------|
| Design freeze | Product Owner + Educational Gate Owner | Pre-registration artefact |
| Implementation | Engineering Owner | Flagged code / config (future programmes) |
| Summary | Ops / research | Immutable summary |
| Independent Review | Educational Gate Owner (+ Privacy when L4) | Pass / Fail / Conditional |
| Claim language update | Product Owner | Bounded by review |
| Structural promote | Engineering + ADR | Only if needed |

**Promotion never means:** silent weight increase, unlocked advisory fields, or marketing of flag-OFF behaviour.

---

## 8. Ethical evaluation principles

These principles bind all OM experiment classes.

### 8.1 Beneficence and non-maleficence

- Experiments must aim at measurable educational benefit (learning or trustworthy guidance), not engagement vanity.  
- STOP if treatment plausibly harms sustainable study, trust, or honest readiness.  
- Prefer humble refusal patterns over fabricated certainty in treatment arms.

### 8.2 Autonomy (student agency)

- Students may defer/reject recommendations; metrics treat agency as valid (PC-11).  
- Reflection remains optional and non-coercive.  
- No dark-pattern UI to force treatment acceptance.

### 8.3 Justice and fairness

- Cohort assignment is algorithmic and reproducible — not cherry-picked “good students.”  
- Report differential effects when sample allows (without leaking individual identity).  
- Curriculum V1 and V2 students remain first-class; experiments must not silently break flat curricula.

### 8.4 Privacy and data minimisation

- Student data belongs to the student.  
- Prefer opaque keys; minimise PII in extracts.  
- Exam outcome linkage is opt-in with Privacy Owner review.  
- Reflection content: default non-persistence until ADR.  
- No silent vendor exfiltration.

### 8.5 Transparency of claims

- Research results disclosed with limitations.  
- Marketing/release language never exceeds verified evidence (PC-03).  
- Exploratory (C0) results stay internal or clearly labelled.

### 8.6 Integrity of science vs product

- Pre-registration before peek.  
- No autonomous policy promotion from thin lift.  
- Separate educational vs engineering boards (PC-02).

---

## 9. Mapping to SI Research Backlog

SI-001 themes (RB-A…F) remain the question catalogue. OM-001 adds the **method** layer:

| Backlog theme | Typical experiment class | Primary catalogue families |
|---------------|--------------------------|----------------------------|
| A Recommendation effectiveness | E2 / E3 | OM-REC-*, OM-BHV-* |
| B Twin understanding quality | E2 after Twin gates; E3 | OM-TWN-*, OM-RDY-* |
| C Readiness calibration | E3 → E4 | OM-RDY-*, OM-LNG-* |
| D Mission & workload | E2 / E3 | OM-MSN-*, OM-CON-* |
| E Reflection Intelligence | E1 → E2 (after Evidence ADR) | OM-REF-* |
| F Explainability | E1 sampling + E3 perception | OM-EXP-* |

Research backlog items are **questions**, not authorised experiments, until a programme files pre-registration under this guide.

---

## 10. Forbidden experiment practices

- Running treatment while narrating “baseline product”  
- Expanding advisory fields inside an “analytics” programme  
- Using page views / streak length as primary educational endpoints  
- Peeking at outcomes then choosing the primary metric  
- Declaring north-star pass-rate proof from Alpha operational lift  
- Equating Twin shadow agreement with learning improvement  
- Coercive reflection or acceptance to inflate metrics  

---

## 11. Explicit non-goals

- Enabling `ENABLE_EDUCATIONAL_TRIALS`  
- Expanding `consistency_summary` lock  
- Implementing new trial services in OM-001  
- Replacing EVF or Privacy Review procedures  

---

**End of OM001_EXPERIMENTATION_GUIDE**
