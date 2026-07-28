# OM-001 — Evidence Requirements

**Programme:** OM-001 — Outcomes Measurement  
**Version:** 1.0  
**Status:** Active — educational evidence requirements (design only)  
**Effective:** 2026-07-28  
**Companion to:** `OM001_OUTCOME_MODEL.md`, `OM001_MEASUREMENT_STANDARD.md`, `OM001_METRIC_CATALOGUE.md`, `OM001_EXPERIMENTATION_GUIDE.md`  
**Constraint:** Defines evidence packs only — does not collect production evidence in this programme.

---

## 1. Purpose

Specify the **measurable supporting evidence** required before Kwalitec may make educational claims about Student Intelligence or related outcomes.

**Rule:** Every educational claim requires measurable supporting evidence. Aspiration, roadmap intent, and estimated ΔKSI are not evidence.

---

## 2. Claim classes and required packs

| Claim class (examples) | Minimum evidence pack | Layer | Forbidden substitutes |
|------------------------|----------------------|-------|------------------------|
| “Recommendations are useful” | P-001.3 Recommendation Review **Pass** (or waiver) + Decision Journal metrics (OM-REC-03,07,10) | L1/L2 | Tip chrome clicks; founder anecdote alone |
| “Explainable guidance” | P-001.2 Explainability Review **Pass** (or waiver) + OM-EXP-01/02 sample | L1/L2 | Marketing “AI explains” copy |
| “Twin-powered” | Flag matrix + Twin Ready/Authority status artefacts + OM-TWN provenance sample | L3 honesty | Narrating flag-OFF as live |
| “Improves learning” | OM-REC-08 and/or OM-LRN-* with CB `learning_signal` or pre-registered `learning_depth` | L1/L5 | Completion rate alone |
| “Improves pass rates” / north star | L4 protocol + OM-NS-* results + Privacy consent artefacts + Independent Review | L4 | Alpha vanity; KSI alone |
| “Experimentally proven lift” | Pre-registration + immutable trial summary + OM-TRIAL-06 + Independent Review | L5 | Peeked exploratory C0 |
| “Readiness is accurate” | OM-RDY-04 (and honesty OM-RDY-02/03); OM-RDY-06 only under L4 | L1→L4 | Precision theatre without calibration |
| “Students reflect usefully” | OM-REF-02/04 + non-coercion attestation | L1 | Participation rate alone |
| “Mission quality improved” | OM-MSN-04/06 + OM-CON-01 — not duration alone | L1 | Longer Sessions as success |
| “Version 1 production-ready” | Full P-002.1 / P-003.1 evidence package | All gates | Estimated ΔKSI; OM docs alone |
| “KSI improved” | Validated reassessment per P-001.1 methodology | L1 | Programme estimate alone for G1 |

---

## 3. Evidence pack schema (design)

Every pack filed for claim language MUST include:

| Field | Content |
|-------|---------|
| `pack_id` | Stable id |
| `claim_statement` | Exact claim language bounded |
| `claim_class` | From §2 |
| `layer` | L1–L5 |
| `claim_boundary` | Evidence Model tag |
| `metric_ids[]` | Catalogue IDs + versions |
| `window` | Observation period |
| `n` / eligibility | Cohort rules |
| `confidence_class` | C0–C4 |
| `artefact_paths[]` | Review checklists, summaries, protocols |
| `limitations[]` | Mandatory |
| `flag_state` | Relevant feature flags at observation |
| `decision` | Supports / Does not support / Inconclusive |
| `reviewer` | Capacity + date (Founder Review record when required) |

---

## 4. SI capability measurable success criteria

Acceptance criterion: **every Student Intelligence capability has measurable success criteria.**

| Capability | Success criteria (measurable) | Evidence artefacts |
|------------|------------------------------|--------------------|
| **SI-C1** Digital Twin | Completeness, provenance, unknown discipline meet programme targets; shadow agreement reported as L3 only; no certainty theatre (OM-TWN-01…04) | Twin health pack; flag honesty |
| **SI-C2** Recommendation Engine | Acceptance→complete chain improves without coercion; learning movement where claimed (OM-REC-03,07,08,10); K2 Pass | Decision Journal pack; P-001.3 checklist |
| **SI-C3** Study Readiness | Overconfidence gap shrinks or is disclosed; calibration tables with cell `n`; drivers traceable (OM-RDY-01…05) | Readiness honesty pack; P-001.2 if speech changed |
| **SI-C4** Mission Intelligence | Completion with practice evidence + consistency; sustainable workload (OM-MSN-01,04,06; OM-CON-01) | Mission quality pack |
| **SI-C5** Reflection Intelligence | Optional participation; return-to-revision or perceived usefulness without coercion (OM-REF-01,02,04) | Reflection usefulness pack; privacy note |
| **SI-C6** Curriculum adaptation | Coverage progress under curriculum truth; V1/V2 still loadable (OM-LRN-04) | Curriculum traversal attestation |
| **SI-C7** Explainability | Schema compliance + student-understood rates; low empty-evidence strong language (OM-EXP-*) | P-001.2 checklist + sample |
| **SI-C8** Learning analytics | Reproducible aggregates; Decision Journal completeness; no dual scoring brain (OM-REC-10; OM-TWN-05) | Analytics integrity pack |
| **SI-C9** Outcome measurement | Claims cite OM catalogue IDs, layers, packs | This corpus + filed packs |
| **SI-C10** Experimentation | Pre-registration; research≠production; Independent Review before promote (OM-TRIAL-*; Experimentation Guide) | Trial design + summary + review |

---

## 5. Programme completion evidence (EP / P / SI implementation)

When a future programme changes student-facing intelligence, its completion report must include (per Governance §4 and reporting rules):

1. Student Impact Assessment (or N/A with rationale)  
2. Estimated KSI contribution with category deltas  
3. Evidence collected (paths)  
4. Explainability Review when in scope (K8 claims need Pass/waiver)  
5. Recommendation Quality Review when in scope (K2 claims need Pass/waiver)  
6. Metric IDs from this catalogue that will be used to evaluate success  
7. Version 1 residual note when claiming V1 progress  

OM-001 itself: docs-only → ΔKSI = 0; checklists N/A.

---

## 6. Relationship to release and educational gates

| Gate / board | How OM evidence feeds it | What OM does not replace |
|--------------|--------------------------|--------------------------|
| EVF Educational Release Gate | L2 quality / trust to release | North-star proof |
| P-002.1 G1 (validated KSI) | L1 usefulness evidence may support reassessment programmes | Estimated ΔKSI; OM framework alone |
| P-002.1 G2–G4 quality contracts | Explainability / recommendation / readiness packs | Full gate package |
| ER-002 claim class | Flag honesty in packs | Engineering Conditional GO |
| Product Board (P-003.1) | Synthesised packs | Declaration by OM docs |

---

## 7. Minimal evidence by confidence class

| Confidence | Minimum pack contents |
|------------|----------------------|
| **C0** | Hypothesis note; “exploratory” label; no marketing use |
| **C1** | Metric IDs, window, `n`, flag state, absolute rates |
| **C2** | C1 + pre-stated comparison + limitations + confounding note |
| **C3** | Pre-registration + immutable summary + primary metric result + Independent Review |
| **C4** | Ethics/privacy consent + protocol + Independent/Privacy review + OM-NS results |

---

## 8. STOP conditions (evidence insufficient)

File **Does not support** or **Inconclusive** and halt claim expansion when:

- Primary metric underpowered relative to pre-registered MDE  
- Flag state contradicts the claim narrative  
- Only organisation metrics are offered for a learning-depth claim  
- Reflection or acceptance appears coerced  
- Curriculum V1/V2 breakage risk untested for curriculum-scoped claims  
- L4 exam claims lack consent  
- Review checklist required for K2/K8 claim is missing or Fail without waiver  

---

## 9. Traceability to Product Constitution

| Principle | Evidence requirement element |
|-----------|------------------------------|
| PC-02 | Separate educational vs engineering packs |
| PC-03 | Claim statement bounded by pack decision |
| PC-04 | Artefact paths mandatory |
| PC-07 | Independent Review for significant experiments / features |
| PC-12 | STOP conditions §8 |

---

## 10. Explicit non-goals

- Generating validated KSI in OM-001  
- Filing production evidence packs in this programme  
- Amending P-002.1 gates  
- Authorising marketing claims  

---

**End of OM001_EVIDENCE_REQUIREMENTS**
