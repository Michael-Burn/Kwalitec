# OM-001 — Measurement Standard

**Programme:** OM-001 — Outcomes Measurement  
**Version:** 1.0  
**Status:** Active — permanent measurement standard (design only)  
**Effective:** 2026-07-28  
**Companion to:** `OM001_OUTCOME_MODEL.md`, `OM001_METRIC_CATALOGUE.md`  
**Constraint:** Design only — no collectors, schema, or product behaviour shipped by this programme.

---

## 1. Purpose

Define **how** Kwalitec measures educational outcomes: units, claim boundaries, reproducibility, sampling, statistical confidence, privacy, and quality bars.

This standard is binding for any future programme that instruments, aggregates, experiments on, or claims educational outcomes. It does not itself instrument production.

---

## 2. Measurement principles

1. **Learning over activity** — prefer mastery movement, adherence, acceptance, readiness calibration over raw clicks or minutes alone.  
2. **One Educational Truth** — metrics project from Runtime A facts, Twin / Evidence / Educational State authorities; analytics must not invent a parallel scoring brain.  
3. **Layer honesty** — every published number carries its measurement layer (L1–L5) and claim boundary.  
4. **Reproducible & auditable** — same inputs + metric version → same aggregate.  
5. **Explainable aggregates** — product decisions based on metrics must be educationally defensible.  
6. **Privacy by design** — student data belongs to the student; research extracts minimise PII; outcome linkage is opted-in where required.  
7. **Agency preserved** — metrics must not coerce reflection, acceptance, or study volume that harms sustainable progress (PC-11).  
8. **STOP on thin evidence** — do not upgrade claim language when N, window, or protocol are insufficient (PC-12).

---

## 3. Metric definition contract

Every metric in the catalogue (and any future metric) MUST specify:

| Field | Required content |
|-------|------------------|
| `metric_id` | Stable ID (e.g. `OM-REC-03`) |
| `name` | Human name |
| `definition` | Precise numerator / denominator or formula |
| `layer` | L1 / L2 / L3 / L4 / L5 |
| `claim_boundary` | Per Evidence Model: `organisation` \| `learning_signal` \| `learning_depth` \| `transfer` \| `trust_inspectability` |
| `si_capabilities` | SI-C1…C10 (one or more) |
| `unit` | Rate, count, band, days, score, … |
| `grain` | impression / session / student-day / student-week / cohort / system |
| `window` | Observation window rules |
| `source_of_truth` | Intended authority (Runtime A, Decision Journal, Twin, …) |
| `exclusions` | What must not inflate the metric |
| `limitations` | Known failure modes |
| `minimum_evidence` | N, duration, or protocol floor before claimable |
| `version` | Metric definition version |

**Rule:** Changing a definition requires a new metric version. Historical series must retain the prior version label.

---

## 4. Claim boundary enforcement

Aligned with `EVIDENCE_MODEL.md` and `OUTCOME_ANALYTICS.md`.

| Boundary | May support claims about | Must not support claims about |
|----------|--------------------------|-------------------------------|
| `organisation` | Start/continue, Session completion, acceptance rates, consistency presence | Learning depth, mastery gain, exam readiness |
| `learning_signal` | Attempt honesty, practice outcomes logged, observational within-topic patterns | Causal “students learned X” without protocol |
| `learning_depth` | Pre-registered constructs with explicit limitations | Exam-mark transfer; completion-as-mastery |
| `transfer` | Consented exam / pass-probability research under L4 protocol | Product-facing exam-mark guarantees |
| `trust_inspectability` | Explanation schema compliance, empty-vs-theatre incidents | Psychological trust as measured fact without instrument |

**Default for new operational metrics:** `organisation` or `learning_signal` until a governed depth programme exists.

---

## 5. Units and normalisation

| Pattern | Rule |
|---------|------|
| Rates | Clamped to `[0.0, 1.0]`; empty cohort → `0.0` with `n=0` disclosed |
| Percentages | Same as rates × 100; always disclose `n` |
| Bands | Ordered categorical; do not average band labels as continuous without defined mapping |
| Deltas | Always pair with baseline window and absolute levels |
| Per-student aggregates | Prefer student-day / student-week over raw event dumps for consistency claims |
| Cross-student | Never join without scoped ids and privacy review |

---

## 6. Reproducibility requirements

1. Metric computation is a pure function of versioned inputs + definition version.  
2. Trial cohort assignment remains deterministic (P4-MS001: hash of salt + trial_id + student_id).  
3. Summaries used for educational or product decisions include: `metric_version`, `as_of`, `window`, `filters`, `n`, `limitations[]`.  
4. Shadow / dual-run engineering agreement is **not** educational lift. Label it L3 / ops.  
5. Founder/ops dashboards consume the same definitions as Independent Review — no private mastery scoring.

---

## 7. Sampling and cohorts

| Mode | When used | Requirements |
|------|-----------|--------------|
| **Census (ops)** | Invite-only Alpha operational monitoring | Disclose eligibility and flag state |
| **Eligible impressions** | Recommendation metrics | Only count surfaces where guidance was eligible under flag honesty |
| **Consistent-user cohort** | North-star and retention analyses | Pre-define “consistent use” (e.g. study days / week thresholds) before looking at outcomes |
| **Research sample** | L4 / L5 studies | Pre-registered inclusion/exclusion; consent artefacts |
| **Dogfood / Founder** | Early signal only | Cannot alone satisfy educational release or north-star claims |

**Contamination controls:** students in active treatment trials are tagged; production claim packs either exclude them or stratify explicitly.

---

## 8. Statistical confidence requirements

These are **minimum design floors** for claim language. They do not replace Independent Review judgment.

### 8.1 Confidence classes

| Class | Intended use | Minimum design floor |
|-------|--------------|----------------------|
| **C0 Exploratory** | Internal hypothesis shaping | Any N; must be labelled exploratory; not for marketing |
| **C1 Operational** | L1 ops monitoring / Decision Journal packs | Pre-defined window; `n` disclosed; no causal language |
| **C2 Comparative observational** | Before/after or cohort comparison without randomisation | Pre-registered metrics; confounding limitations mandatory; no “proven” language |
| **C3 Controlled trial** | L5 educational trials | Deterministic assignment; pre-registered primary metric; Independent Review; see Experimentation Guide |
| **C4 Longitudinal transfer** | L4 north-star / exam linkage | Consent; ethics review; pre-registered protocol; external or Independent assessment as required by Privacy Owner |

### 8.2 Quantitative floors (design defaults)

| Claim type | Design default floor |
|------------|----------------------|
| Rate difference (ops narrative) | Disclose absolute rates + `n`; avoid claiming lift when `|Δ| < 0.05` unless pre-registered and reviewed |
| Controlled trial primary endpoint | Pre-register MDE (minimum detectable effect); do not promote on underpowered “significance theatre” |
| Calibration claims | Reliability diagrams / band-vs-outcome tables with cell `n` floors (default ≥ 30 observations per band cell before strong language) |
| KSI category movement | Validated reassessment methodology per P-001.1 / EP-005.1 — estimated ΔKSI never clears G1 |
| North-star pass probability | Dedicated L4 protocol only; Alpha vanity forbidden |

### 8.3 Uncertainty disclosure

Every comparative claim pack MUST include at least one of: confidence interval, bootstrap interval, or explicit “uncertainty not quantified — exploratory” label. Missing uncertainty + strong causal language = claim violation.

---

## 9. Quality dimensions for measurement itself

| Dimension | Standard |
|-----------|----------|
| **Completeness** | Missingness rate disclosed; do not impute educational mastery from silence |
| **Timeliness** | `as_of` and lag disclosed for readiness / Twin-linked metrics |
| **Provenance** | Trace to Decision Journal / Evidence / Runtime A ids where applicable |
| **Flag honesty** | Metrics from flag-OFF paths must not be narrated as live Twin / trial / cutover behaviour (ER-002 / G12) |
| **Curriculum fidelity** | Topic-level metrics respect CurriculumService ordering; V1 and V2 remain loadable |
| **Student agency** | Acceptance metrics distinguish defer/reject from ignore; refusal is valid |

---

## 10. Privacy and ethics (measurement)

Aligned with Vision data principles and SI-001 §10.

1. Prefer opaque student keys in research extracts (`trialstu-…` pattern).  
2. No personal identifiers on trial observation / advisory outcome DTO surfaces (existing P3/P4 law).  
3. Reflection content is especially sensitive — default non-persistence until ADR.  
4. Exam outcome linkage requires explicit consent and Privacy Owner capacity review.  
5. No silent exfiltration to opaque vendors without security/privacy review.  
6. Metrics must not create coercive gamification that Vision forbids (streaks-as-success).

Detail: `OM001_EXPERIMENTATION_GUIDE.md` § ethics.

---

## 11. Relationship to KSI and release gates

| Instrument | Role under this standard |
|------------|--------------------------|
| KSI K1–K8 | L1 usefulness scores; category claims obey P-001.2/3 review gates |
| Estimated programme ΔKSI | Planning signal only |
| Validated KSI | Required for Gate G1 / V1-K1 — not produced by OM-001 |
| EVF Educational Release Gate | L2 — orthogonal to L4 outcome proof |
| P-002.1 G1–G12 | Production-ready declaration — OM metrics may feed evidence packs but do not replace gates |

---

## 12. Multi-horizon instrumentation (design)

| Horizon | Measurement focus (from SI OM-H*) |
|---------|-----------------------------------|
| **OM-H0** | This standard freeze; outcome model + catalogue |
| **OM-H1** | Decision Journal completeness; explainability compliance sampling; metric definition adoption in SI programmes |
| **OM-H2** | Twin health + readiness honesty ops packs; dual-run divergence labelled L3 |
| **OM-H3** | Closed-loop effectiveness packs; authorised trial lift reports; reflection usefulness (non-coercive) |
| **OM-H4** | Consented longitudinal pass-probability research execution |

OM-001 delivers **OM-H0**. Later horizons require separate OA-001 lifecycle programmes.

---

## 13. Explicit non-goals

- Shipping metric collectors or warehouses in this programme  
- Replacing Product Analytics Architecture or Evidence Model  
- Authorising trial expansion beyond `consistency_summary`  
- Declaring statistical “proof” of north-star outcomes  

---

**End of OM001_MEASUREMENT_STANDARD**
