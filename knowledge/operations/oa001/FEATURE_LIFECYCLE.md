# Feature Lifecycle

**Programme:** OA-001 — Operational Architecture & Product Lifecycle Framework  
**Version:** 1.0  
**Status:** Active  
**Effective:** 2026-07-28  
**Authority:** Product Constitution PC-07 · `knowledge/GOVERNANCE.md` §4 · Vision 2030 Final Test  
**Constraint:** Process only — does not implement features.

---

## 1. Purpose

Define the permanent lifecycle for **significant features** so delivery is repeatable, explainable, and independently reviewable.

**Law (PC-07):** Every significant feature follows **Blueprint → Implementation → Independent Review**.

---

## 2. What counts as a significant feature

A change is **significant** if any of the following is true:

- New or materially changed student-facing capability.
- Changes recommendations, planning, readiness, missions, Twin, or educational speech.
- Requires a PRD under `knowledge/prd/`.
- Affects claim class, flags, privacy, or educational governance.
- Estimated non-trivial KSI contribution (positive or risk of regression).

### Exceptions (classified thin path)

| Exception | Still required |
|-----------|----------------|
| Hotfix (production incident) | Hotfix lifecycle in Release Governance Model |
| Pure documentation / governance | Completion report if programme-mandated; no silent authority change |
| Pure chore (no behaviour change) | PR notes; Architecture/Educational reviews only if unexpectedly touched |

**No PRD → no significant feature work** (`GOVERNANCE.md` §4).

---

## 3. Lifecycle stages

```
Propose → Align → Blueprint → Implement → Independent Review → Certify → Release → Operate
```

### Stage A — Propose

| Action | Artefact |
|--------|----------|
| Frame student problem | PRD using `knowledge/prd/PRD_TEMPLATE.md` |
| Final Test | Explicit yes/no with rationale |
| Estimated KSI | K1–K8 deltas or ΔKSI = 0 with rationale |
| Change class | Per Change Management Standard |

**Exit:** PRD draft ready for Product review.

### Stage B — Align

| Review | Focus |
|--------|-------|
| Product | Student benefit, Final Test, KSI, roadmap fit |
| Architecture | Runtime / Twin / layering / ADR need |
| Educational Gate | Vocabulary, authority, reflection, EGI impact |
| Privacy | Data collection, cohort, analytics (if any) |

**Exit:** Alignment recorded; STOP if higher authority conflict.

### Stage C — Blueprint

Produce a design freeze covering:

- Student journey touchpoints (sole-runtime paths).
- Service / engine ownership (no second educational brain).
- Explanation / recommendation obligations (P-001.2 / P-001.3).
- Evidence plan (tests, dogfood, perception, cohort as applicable).
- Claim language allowed after ship.
- Feature flags and default OFF/ON posture.
- ADR Accepted if structural (ADR Standard).

**Exit:** Blueprint approved; implementation may start.

### Stage D — Implement

- Follow `knowledge/ENGINEERING_STANDARDS.md` and Quality Manual.
- Services own logic; blueprints stay thin; curriculum via `CurriculumService`.
- Tests at appropriate pyramid layers; architecture tests if invariants added.
- No secrets in repo; CSRF / authz preserved.
- Update debt register for intentional compromises.

**Exit:** Definition of Done met on the implementing PR(s).

### Stage E — Independent Review

Review must be **independent of the implementation narrative** (separate checklist pass; Founder may use a different capacity lens per GP-001, but must not rubber-stamp).

| If the feature affects… | Required review |
|-------------------------|-----------------|
| Student-facing intelligence speech | Explainability Review (P-001.2) |
| Recommendations ranking/selection/tips | Recommendation Quality Review (P-001.3) |
| Educational law / vocabulary / authority | Educational Governance Review (EGI-003 / DG-001) |
| Structural boundaries | ADR Acceptance + architecture review |
| Privacy / Stage 1 enrollment | Privacy Review |

Outcomes: **Pass** · **Conditional Pass** (holds listed) · **Fail** (must not release with the failed claim).

### Stage F — Certify

File programme / milestone completion report with required sections (including EP/P student-value sections when applicable). Update Programme Dashboard.

### Stage G — Release

Follow `RELEASE_GOVERNANCE_MODEL.md` and Release Playbook / Protocol. Obtain EVF gate if educational trust claims are made. Do not declare Version 1 production-ready without P-002.1.

### Stage H — Operate

Monitor residuals, flags, debt, and risks. Schedule perception or cohort validation if Strong-band KSI claims remain open.

---

## 4. RACI (capacities)

| Stage | Product Owner | Engineering Owner | Educational Gate | Operations Owner |
|-------|:-------------:|:-----------------:|:----------------:|:----------------:|
| Propose | A | C | C | I |
| Align | A | R | R | I |
| Blueprint | A | R | C/R | C |
| Implement | C | A | C | I |
| Independent Review | R/A | R | R | I |
| Certify | A | R | R | C |
| Release | C | R | C | A |
| Operate | C | R | C | A |

A = Accountable · R = Responsible · C = Consulted · I = Informed

---

## 5. Definition of done (feature)

A significant feature is done only when:

1. Blueprint exit criteria met and ADR Accepted if required.
2. Implementation DoD met (tests, docs, security, architecture).
3. Required independent reviews recorded Pass or Conditional with holds.
4. Completion report filed; Dashboard updated.
5. Claim language matches evidence; flags honest (G12).
6. Debt and risk registers updated for new residuals.

---

## 6. Anti-patterns

- Building first, writing PRD after merge.
- Skipping Independent Review because “Founder built it”.
- Shipping under Engineering Conditional GO as if Product GO.
- Changing recommendation math inside a “UI polish” programme.
- Dual educational narrators or new reflection systems outside DG-001.

---

**End of Feature Lifecycle**
