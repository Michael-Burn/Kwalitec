# SI-001 — Research Backlog

**Programme:** SI-001 — Student Intelligence  
**Version:** 1.0  
**Status:** Active — research & experimentation backlog (design only)  
**Effective:** 2026-07-28  
**Companion to:** `SI001_STUDENT_INTELLIGENCE_ARCHITECTURE.md`, `SI001_OUTCOME_MEASUREMENT_FRAMEWORK.md`  
**Constraint:** No trials enabled, advisory fields expanded, or algorithms changed by this programme.

---

## 1. Purpose

Catalogue the **educational research and experimentation** questions that future Student Intelligence programmes must answer with evidence — so Kwalitec improves student outcomes under Vision 2030 without shipping unvalidated intelligence theatre.

This backlog feeds SI-H3/H4 and OA-001 Feature Lifecycle (Blueprint → Implementation → Independent Review). It does not authorise experiments.

---

## 2. Authority

| Authority | Binding effect |
|-----------|----------------|
| Vision 2030 | Evidence before opinion; north star; never-build opaque AI / activity metrics |
| Product Constitution PC-07, PC-09, PC-12 | Lifecycle; determinism; STOP when evidence thin |
| Educational trial architecture (P4-MS001) | Controlled, deterministic cohorts; locked advisory fields; flag OFF by default |
| Outcome Measurement Framework | Layer separation L1–L5; claim discipline |
| P-001.2 / P-001.3 | Explainability & recommendation quality gates for treatments |
| ER-002 / G12 | No marketing of flag-OFF or unproven lift |

---

## 3. Experimentation principles

1. **Educational benefit first** — every behavioural expansion justified by measurable learning benefit (P4 purpose statement).  
2. **Deterministic assignment** — reproducible cohort membership from explicit rules.  
3. **Locked treatment surface** — advisory fields / policy weights expanded only by dedicated programme + ADR.  
4. **No autonomous promotion** — trial lift does not silently rewrite production policy.  
5. **Independent Review** — significant experiments follow PC-07.  
6. **STOP** — thin or harmful signals halt expansion (PC-12).  
7. **Privacy** — student ownership; consented L4 outcome linkage.  
8. **Fail-open safety** — production defaults remain safe when trials OFF.

---

## 4. Existing foundation (do not reinvent)

| Artefact | Role |
|----------|------|
| `EducationalTrialService` / P4-MS001 | Operational trial framework; `consistency_summary` only |
| `ENABLE_EDUCATIONAL_TRIALS` | Default OFF |
| Decision Journal | Acceptance / dismissal substrate |
| Product Analytics Architecture | Metric definitions (design) |
| Shadow / dual-run Twin paths | Engineering agreement evidence — not educational lift alone |

**Stop condition inherited:** Await architecture review before expanding advisory influence beyond `consistency_summary`.

---

## 5. Research themes

Themes map to SI capabilities and Vision Final Test.

### Theme A — Recommendation effectiveness

| ID | Question | Hypothesis (design) | Primary metrics | Horizon | Depends on |
|----|----------|---------------------|-----------------|---------|------------|
| **RB-A1** | Does a single primary recommendation raise completion vs tip lists? | Fewer, clearer next actions increase Session start/complete | Accept→complete chain | H1–H3 | Decision Journal completeness |
| **RB-A2** | Does P-001.3 prioritisation beat legacy tip ordering? | Quality-ranked tips improve educational movement | Mastery/revision deltas; acceptance | H2–H3 | Dual-run capability |
| **RB-A3** | When should the system refuse to recommend? | Lawful refusal beats fabricated certainty for trust | Dismiss reasons; satisfaction; overconfidence gap | H1–H3 | Explainability patterns |
| **RB-A4** | Do readiness-coupled actions outperform generic focus tips? | Driver-linked actions improve weak-area repair | Weak-topic mastery movement | H2–H3 | Readiness honesty |

### Theme B — Twin understanding quality

| ID | Question | Hypothesis (design) | Primary metrics | Horizon | Depends on |
|----|----------|---------------------|-----------------|---------|------------|
| **RB-B1** | Does Twin-enriched planning improve Session completion vs non-Twin path? | Foundation inputs improve plan fit | Completion; workload sustainability | H2–H3 | Twin dual-run / cutover ADR |
| **RB-B2** | Are Twin facets predictive of later readiness movement? | Consistency/revision facets forecast useful interventions | Calibration; facet→outcome correlations | H3 | Twin health metrics |
| **RB-B3** | Does showing incompleteness improve trust vs hiding gaps? | Sparse-evidence speech increases appropriate reliance | Satisfaction; overconfidence gap | H1–H3 | P-001.2 patterns |

### Theme C — Readiness calibration

| ID | Question | Hypothesis (design) | Primary metrics | Horizon | Depends on |
|----|----------|---------------------|-----------------|---------|------------|
| **RB-C1** | How well do readiness bands predict short-horizon performance? | Bands correlate with subsequent attempt success | Calibration curves | H2–H3 | Attempt evidence density |
| **RB-C2** | Does readiness honesty coaching reduce overconfidence? | Humble speech reduces false high bands without harming consistency | Overconfidence gap; consistency | H2–H3 | Readiness UX programme |
| **RB-C3** | Pre-exam readiness vs exam outcome (consented) | Calibrated readiness associates with pass probability | L4 outcome study | H4 | Privacy protocol; cohort size |

### Theme D — Mission & workload intelligence

| ID | Question | Hypothesis (design) | Primary metrics | Horizon | Depends on |
|----|----------|---------------------|-----------------|---------|------------|
| **RB-D1** | Do workload soft-caps reduce burnout signals without lowering mastery growth? | Sustainable pacing improves net learning | Cognitive load flags; mastery velocity | H2–H3 | Mission Intelligence design |
| **RB-D2** | Recovery recommendations vs “push harder” defaults | Recovery tips improve next-week consistency | Consistency; completion | H2–H3 | RE recovery family |

### Theme E — Reflection Intelligence

| ID | Question | Hypothesis (design) | Primary metrics | Horizon | Depends on |
|----|----------|---------------------|-----------------|---------|------------|
| **RB-E1** | Does optional reflection increase mistake-aware revision? | Light reflection → better weak-topic return | Revision adherence; qualitative | H3 | Evidence taxonomy ADR |
| **RB-E2** | Does persisting reflection harm agency or privacy perception? | Non-coercive, ephemeral default preferred until trust proven | Opt-out; satisfaction; PC-11 checks | H3 | Privacy review |
| **RB-E3** | Can reflection evidence improve Twin without becoming mastery proof? | Weak prior only; no certainty inflation | Twin unknown discipline metric | H3 | Twin Constitution compliance |

### Theme F — Curriculum adaptation

| ID | Question | Hypothesis (design) | Primary metrics | Horizon | Depends on |
|----|----------|---------------------|-----------------|---------|------------|
| **RB-F1** | Within-syllabus reordering vs fixed order — learning impact? | Evidence-aware order improves coverage efficiency | Coverage pace; mastery | H2–H3 | CurriculumService-only changes |
| **RB-F2** | V1 flat vs V2 hierarchical — adaptation parity? | Both curricula remain effective under same intelligence | Traversal tests + learning metrics | Continuous | Architecture invariant |

### Theme G — North-star & ecosystem

| ID | Question | Hypothesis (design) | Primary metrics | Horizon | Depends on |
|----|----------|---------------------|-----------------|---------|------------|
| **RB-G1** | Do consistent Kwalitec users pass at higher rates than matched non-users / light users? | North star holds under confounder control | Pass rate differential | H4 | L4 protocol; ethics |
| **RB-G2** | Which L1 metrics mediate pass outcomes? | Consistency + recommendation completion mediate | Mediation analysis | H4 | RB-G1 data |
| **RB-G3** | Multi-qualification Twin — interference effects? | Shared identity without syllabus crosstalk harm | Per-syllabus mastery integrity | H4 | DT-H4 |

---

## 6. Prioritisation (architectural)

Priority scores are **design guidance**, not a shipping schedule.

| Priority | Items | Rationale |
|----------|-------|-----------|
| **P0 — Trust substrate** | RB-A1, RB-A3, RB-B3 | Unlocks honest H1 intelligence without Twin Ready claims |
| **P1 — Closed loop** | RB-A2, RB-A4, RB-B1, RB-D1 | Requires Twin/consumer maturity (H2–H3) |
| **P2 — Reflection & adaptation** | RB-E1–E3, RB-F1–F2 | After evidence taxonomy + curriculum ADR |
| **P3 — North star** | RB-C3, RB-G1–G3 | Longitudal; privacy-heavy; post claim-class expansion |

**Blocked until:** Educational advisory field expansion beyond `consistency_summary` receives architecture review; Stage 1 / high-traffic claims remain gated by ER-002 / G10 as applicable.

---

## 7. Educational experimentation framework (target)

```
Research question (this backlog)
        ↓
Blueprint (hypotheses, metrics, ethics, claim limits)
        ↓
ADR if structural / authority / advisory-field change
        ↓
Implementation (trial config; deterministic assignment)
        ↓
Independent Review + Explainability/Recommendation checklists
        ↓
Run under flag / cohort gates
        ↓
Evidence pack (Outcome Framework L5)
        ↓
Decision: promote / iterate / STOP
        ↓
Update claim language (never exceed evidence)
```

**Promotion rule:** Policy or ranking promotion requires explicit product decision citing evidence pack — never automatic.

---

## 8. Out-of-backlog (rejected research directions)

Aligned with Vision never-build:

- Engagement maximisation experiments (time-on-site as success)  
- Dark-pattern acceptance maximisation  
- Opaque model A/B without educational explanation  
- Coercive reflection scoring / ranking students by “mindset”  
- Unconsented exam-result scraping  

---

## 9. Traceability

| Vision 2030 | Backlog |
|-------------|---------|
| North star | Theme G |
| Four questions / next action | Theme A |
| Explainable AI | RB-A3, RB-B3 |
| Consistency / reflection / revision | Themes D, E, F |
| Final Test | Gate on every RB item before Blueprint |

| Product Constitution | Backlog |
|----------------------|---------|
| PC-07 | Experimentation framework §7 |
| PC-09 | Deterministic trials |
| PC-11 | Reflection non-coercion (Theme E) |
| PC-12 | STOP / no silent promotion |

---

## 10. Explicit non-goals

- Enabling `ENABLE_EDUCATIONAL_TRIALS`  
- Expanding advisory fields  
- Running RB-* studies in SI-001  
- Claiming experimental lift  

---

**End of SI001_RESEARCH_BACKLOG**
