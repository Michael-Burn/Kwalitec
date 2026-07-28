# SI-001 — Digital Twin Evolution

**Programme:** SI-001 — Student Intelligence  
**Version:** 1.0  
**Status:** Active — architectural evolution roadmap (design only)  
**Effective:** 2026-07-28  
**Companion to:** `SI001_STUDENT_INTELLIGENCE_ARCHITECTURE.md`  
**Constraint:** No Twin algorithms, persistence cutover, flags, or UI modified by this programme.

---

## 1. Purpose

Define how the **Student Digital Twin** evolves from the MS-004 / EP-001 / EP-002 baseline into the longitudinal educational understanding model required by Vision 2030 — while obeying the Digital Twin Constitution and Product Constitution.

The Twin’s permanent question:

> Given everything we know about this learner today, what educational decision is most likely to improve long-term mastery?

The Twin answers by holding **provisional understanding**, never certainty.

---

## 2. Authority

| Authority | Binding effect |
|-----------|----------------|
| Vision 2030 | One Educational State; evidence before opinion; reproducible calculations |
| Digital Twin Constitution | Understanding ≠ certainty; unknown remains unknown; five domains of meaning |
| Twin Philosophy | Why Twin exists — improve guidance quality |
| Product Blueprint | Future capabilities improve Twin rather than bypass it |
| Product Constitution PC-09, PC-10, PC-11 | Determinism; curriculum truth; agency |
| MS-004 architecture + EP-001.1 Foundation | Implemented contracts; CanonicalLearnerState consumer read model |
| EP-002.9 Baseline | Ownership chain; Twin Ready (T7) not declared by EP-002 |
| ER-002 / G12 | Flag-OFF honesty; no Twin-live marketing |

---

## 3. Current state (honest baseline)

| Layer | Posture |
|-------|---------|
| T0–T6 (contracts → shadow validation) | Implemented under `ENABLE_DIGITAL_TWIN` (default OFF) |
| EP-001.1 Foundation | CanonicalLearnerState / Foundation packages; Authority routing optional OFF |
| EP-001.2–4 consumers | Planner / Readiness / Insight consume Foundation when gated |
| EP-002 surface | Controlled-pilot architecture certified; production defaults OFF |
| Twin Ready (T7) | **Not declared** |
| Experience cutover / Twin-first sole authority | **Not complete** |
| Contained dual-stack residuals | Disclosed under ER-002 (no “fully converged” claims) |

SI-001 evolution presupposes this honesty. Aspiration is not cutover.

---

## 4. Constitutional domains (unchanged meaning)

Evolution deepens *evidence and trajectory* within Twin Constitution domains; it does not invent new educational metaphysics.

| Domain (meaning) | Evolution emphasis |
|------------------|--------------------|
| Knowledge / mastery understanding | Stronger evidence aggregation; never fabricate mastery |
| Performance / retention understanding | Longitudinal retention trajectories (design) |
| Behaviour / consistency understanding | Rhythm, persistence, session habits as evidence |
| Confidence / readiness understanding | Honest bands; calibration research (Outcome Framework) |
| Goals / trajectory understanding | Exam-date and multi-horizon goals without destiny claims |

---

## 5. Evolution horizons

### DT-H1 — Integrity & consumer trust (SI-H1)

**Intent:** Keep Twin understanding trustworthy for invite-only intelligence surfaces without declaring Twin Ready.

| Design workstream | Outcome |
|-------------------|---------|
| Provenance completeness | Every consumer-facing Twin field retains Runtime A provenance |
| Sparse-evidence discipline | Unavailable facets stay unavailable — no estimation theatre |
| Explainability parity | Facet/Snapshot explanations align with P-001.2 levels |
| Shadow / dual-run discipline | Continue fail-open; document residuals |
| Claim language freeze | No Twin-live marketing while flags OFF |

### DT-H2 — Persistence & authority readiness (SI-H2)

**Intent:** Prepare Twin as durable, versioned educational understanding with lawful authority path.

| Design workstream | Outcome |
|-------------------|---------|
| Snapshot persistence design | Immutable versioned snapshots; no in-place mutation |
| Authority ADR | When Foundation becomes Experience / student-port authority |
| Write-boundary clarity | Runtime A remains sole educational write authority for facts |
| Completeness semantics | Structural completeness ≠ educational certainty |
| Adaptive attach maturity | Twin as optional enrichment under determinism tests |
| Twin Ready (T7) criteria | Explicit checklist programme — not implied by SI-001 |

**Gate:** Persistence/authority implementation requires ADR (PC-06), Independent Review, EVF educational quality, engineering claim-class compliance.

### DT-H3 — Closed evidence loops (SI-H3)

**Intent:** Lawful evidence types from Mission completion, revision, and optional Reflection update Twin understanding.

| Design workstream | Outcome |
|-------------------|---------|
| Evidence taxonomy expansion | Typed events; reflection as weak, consented signal |
| Timeline / comparison services | Longitudinal views for diagnostics (not vanity streaks) |
| Feedback to Planner/Readiness | Consumers remain pure; Twin remains understanding layer |
| Uncertainty visualisation | Product speech for incomplete twins |

### DT-H4 — Longitudinal professional Twin (SI-H4)

**Intent:** Multi-exam, multi-year educational understanding supporting Vision 2030 “operating system for professional learning.”

| Design workstream | Outcome |
|-------------------|---------|
| Cross-qualification identity | One learner; multiple syllabus graphs; no forked truths |
| Career-trajectory goals | Goals domain without psychometric destiny |
| Institutional read models | Secondary audience projections; student ownership of data |
| Research interfaces | Privacy-preserving outcome study hooks (Outcome Framework) |

---

## 6. Target logical architecture

```
Evidence Events (Runtime A facts + typed observations)
        ↓
Evidence Aggregator (deterministic)
        ↓
Twin Engine (mastery / confidence / retention / behaviour / goals)
        ↓
Immutable TwinSnapshot (+ completeness + provenance)
        ↓
Explainability projection
        ↓
Consumers: Planner | Readiness | Insight | Analytics | Trials
```

**Hard boundaries:**

| Twin may | Twin must not |
|----------|---------------|
| Interpret evidence into provisional understanding | Teach content |
| Expose explainable facets/snapshots | Store curriculum PDFs or UI state |
| Feed consumers as read model | Execute missions / generate questions |
| Say “unknown” | Manufacture certainty or destiny |
| Evolve when evidence warrants | Depend on opaque LLM state |

---

## 7. Relationship to One Educational State

Product Blueprint / Vision require **One Educational State**.

| Concept | Role |
|---------|------|
| Educational State (product) | Unified learning truth presented to experience |
| Twin Foundation / Snapshot | Authoritative *understanding* substrate for that truth when cut over |
| Runtime A facts | Write authority for what happened |

Evolution rule: improve Twin and its projections; **do not** create a competing EducationalStateService narrative for the same student moment. Governance-only programmes must not modify Twin (Blueprint post-consolidation directive); SI implementation programmes must use ADR.

---

## 8. Facet evolution (design catalogue)

Existing MS-004 facets remain the starting set. Future facets require constitutionality review.

| Facet family | Evolution note |
|--------------|----------------|
| Learning Rhythm | Longitudinal stability metrics (design) |
| Consistency | Align with Vision consistency success metric |
| Persistence | Distinguish healthy persistence vs burnout risk |
| Revision Behaviour | Feed revision recommendation family (RE roadmap) |
| Confidence Trend | Couple to readiness honesty — not vanity |
| Session Habits | Mission Intelligence input |
| Cognitive Load Indicators | Soft constraint for workload recommendations |

**Rule:** New facets derive from Runtime A evidence only; no facet depends on another facet’s invented score; missing → unavailable.

---

## 9. Risks and mitigations (architecture)

| Risk | Mitigation |
|------|------------|
| False Twin Ready claims | Explicit T7 programme; ER-002 C7 |
| Parallel educational truths | One State invariant; Contained disclosure until retired |
| Estimation drift | Constitution “unknown remains unknown” |
| Privacy expansion with longitudinal data | Vision data principles; student ownership |
| Consumer coupling that mutates Twin | Read-only consumer law (EP-001.5) |

---

## 10. Traceability

| Vision 2030 | Twin evolution |
|-------------|----------------|
| One Educational State | DT-H2 authority; §7 |
| Evidence before opinion | All horizons |
| Reproducible / auditable | Deterministic engine; provenance |
| Become professionals | Guidance quality via honest understanding |
| Never-build opaque AI | No LLM Twin authority |

| Product Constitution | Twin evolution |
|----------------------|----------------|
| PC-03–PC-04 | Claim honesty for Twin status |
| PC-06 | ADR before persistence/authority |
| PC-09 | Deterministic snapshots |
| PC-10 | Curriculum remains outside Twin |
| PC-11 | Twin does not coerce via certainty theatre |

---

## 11. Explicit non-goals

- Declaring Twin Ready (T7) in SI-001  
- Enabling production Twin flags  
- Schema migrations or persistence implementation  
- Bypassing Twin with ad-hoc recommendation heuristics  
- Psychometric “ability” scoring as educational destiny  

---

**End of SI001_DIGITAL_TWIN_EVOLUTION**
