# Version 1 Release Framework

**Programme:** P-002.1 — Version 1 Release Framework  
**Version:** 1.1  
**Status:** Active — permanent Version 1 production-readiness authority  
**Effective:** 2026-07-26  
**Amended:** 2026-07-26 — G1 slice pointer (EP-005.1); gates unchanged  
**Authority:** Product release-readiness law  
**Does not:** Change runtime behaviour, Twin algorithms, UI, or APIs  

---

## 1. Purpose

This framework defines **when Kwalitec Version 1 may be declared production-ready**.

It exists so that:

- Version 1 claims rest on **objective, measurable gates**, not optimism or estimated KSI alone;
- educational usefulness, constitutional integrity, quality contracts, and operational safety are evaluated together;
- every gate requires **evidence**, a named **owner**, and an explicit **pass / fail / hold**;
- Product, Educational, Architecture, Engineering, Security, and Release **capacities** share one go / no-go board. Under GP-001 these capacities are founder-held and recorded as Founder Reviews (see `../gp001_founder_governance_model/`). Evidence requirements are unchanged.

**Version 1 production-ready ≠ operational GA alone.  
Version 1 production-ready ≠ KSI ≥ 80 alone.  
Version 1 production-ready ≠ architecture cutover complete alone.**

All material gate families in this document must pass (or carry an approved hold that does not overclaim) before Version 1 may be declared.

---

## 2. Relationship to Product Constitution and peer authorities

| Authority | Relationship |
|---|---|
| **Vision 2030 (Product Constitution)** | Highest product-philosophy authority. Final Test and Never-Build list constrain every gate. This framework never invents a second north star. |
| **Product Blueprint** | Strategy / roadmap map; this framework decides whether Version 1 capability work is *ready to claim*. |
| **Product Success Framework (KSI)** | Owns educational usefulness measurement and V1-K1…V1-K7 criteria. Gate **G1** requires **validated** (not estimated-only) KSI ≥ 80 plus those criteria. |
| **Explainability Standard (P-001.2)** | Owns student-facing explanation law. Gate **G3** requires coverage and checklist Pass. |
| **Recommendation Quality Standard (P-001.3)** | Owns recommendation quality law. Gate **G4** requires scorecard / checklist compliance. |
| **Educational Constitution + EVF Release Gate** | Own educational meaning and educational trust to release. Gate **G2** and EVF outcome are mandatory; this framework does **not** replace EVF. |
| **Architecture Constitution + ADRs** | Own structural law and one runtime. Gate **G2** includes architecture constitutional compliance. |
| **Release Playbook + Protocol** | Own how we ship tags/deploys. This framework owns whether Version 1 *may be declared*; Playbook owns *how* a release executes. |
| **VERSION_1_READINESS.md** | Operational tracker. Status cells must reflect evidence under this framework; the tracker does not invent gates. |

### Authority order (conflict rule)

```
Vision 2030 (Product Constitution)
        ↓
Educational Constitution + EVF Educational Release Gate
        ↓
Architecture Constitution + ADRs
        ↓
Product Success Framework (KSI) + Explainability + Recommendation Quality
        ↓
THIS FRAMEWORK (Version 1 production-ready declaration law)
        ↓
Release Playbook / Protocol / VERSION_1_READINESS tracker
```

If this framework appears to conflict with Vision 2030 or Educational Constitution: **STOP**, document, recommend amendment of the higher authority first. Do not soft-amend constitutions via release convenience.

---

## 3. What “Version 1 production-ready” means

### 3.1 Declaration statement (only when all hard gates pass)

> **Kwalitec Version 1 is production-ready** for the declared cohort / claim window: educational usefulness meets validated KSI ≥ 80 under P-001.1, constitutional and quality-contract gates pass, operational safety gates pass, and the Version 1 Evidence Package is complete and current.

### 3.2 What the declaration is not

| Claim | Allowed under this framework? |
|---|---|
| Exam pass-rate proof in a live population | **No** — north-star outcome; measure later with approved methodology |
| Public marketing of recommendation effectiveness without approved evidence | **No** — EP-001 / EP-003 freeze until lifted |
| “Exam Ready” marketing without readiness gates | **No** — constitutional honesty |
| Operational GA / Twin soak / architecture cutover alone | **Insufficient** — necessary inputs, not the declaration |
| Estimated KSI ≥ 80 without validation artefacts | **Insufficient** — Gate G1 requires validated KSI |

### 3.3 Claim language rules

1. Distinguish **educational usefulness (KSI)** from **exam pass probability (north star)**.
2. Distinguish **production-ready Version 1** from **private-beta GO WITH CONDITIONS**.
3. Distinguish **quality-contract compliance** from **student-perceived excellence**.
4. Never claim dual educational truths, opaque AI guidance as fact, or mastery theatre.

---

## 4. Gate families (normative)

Twelve gate families. Each gate is **PASS**, **FAIL**, or **HOLD** (approved conditional with explicit claim restriction).

Hard-gate failures block Version 1 declaration. HOLDs require Product + owning authority sign-off and must appear in the Go / No-Go record.

| ID | Gate family | Hard? | Primary owner |
|---|---|---|---|
| **G1** | Validated KSI | Yes | Product |
| **G2** | Constitutional compliance | Yes | Product + Educational + Architecture |
| **G3** | Explainability coverage | Yes | Product + Educational |
| **G4** | Recommendation Quality compliance | Yes | Product + Educational |
| **G5** | Planning Quality compliance | Yes | Product + Engineering |
| **G6** | Readiness Quality compliance | Yes | Product + Engineering |
| **G7** | Performance | Yes* | Engineering |
| **G8** | Reliability | Yes* | Engineering |
| **G9** | Production telemetry | Yes* | Product + Engineering |
| **G10** | Security and data integrity | Yes | Security / Engineering |
| **G11** | Test coverage | Yes | Engineering |
| **G12** | Production feature-flag readiness | Yes | Product + Engineering + Release |

\*G7–G9 may carry an approved HOLD only when (a) residual is documented in Technical Debt / Readiness tracker, (b) claim language excludes high-traffic marketing / cohort expansion that the residual blocks, and (c) Product + Release operator sign the HOLD. HOLDs never waive educational honesty or security criticals.

Detailed acceptance criteria: [`VERSION_1_ACCEPTANCE_CHECKLIST.md`](VERSION_1_ACCEPTANCE_CHECKLIST.md).  
Evidence artefacts: [`VERSION_1_EVIDENCE_REQUIREMENTS.md`](VERSION_1_EVIDENCE_REQUIREMENTS.md).  
Decision outcomes: [`VERSION_1_GO_NO_GO_GUIDE.md`](VERSION_1_GO_NO_GO_GUIDE.md).

---

### G1 — Validated KSI

**Objective:** Educational usefulness meets the Version 1 bar with evidence-bound scores — not programme estimates alone.

| Criterion | Measurable rule |
|---|---|
| G1.1 | Published composite **KSI ≥ 80** (nearest integer) per Product Success Framework |
| G1.2 | Assessment confidence **High** or **Medium**; Low confidence → FAIL |
| G1.3 | Assessment dated ≤ **90 days** before declaration (PSF §5.4) |
| G1.4 | **No category below 50** (V1-K2) |
| G1.5 | **K8 Explainability ≥ 70** (V1-K3) |
| G1.6 | Evidence package cites paths, rationales, limitations per category (PSF §5.3) |
| G1.7 | Independent re-score of the same package agrees within **±3** KSI, or dispute resolved by Product owner |
| G1.8 | Claim language distinguishes KSI usefulness from exam pass-rate proof (V1-K7) |
| G1.9 | EP-003 / EP-004 educational Go / No-Go not **NO-GO** for the same claim window (V1-K5) |
| G1.10 | No unresolved educational honesty incident (V1-K6) |

**Example G1 slice (not a declaration package):** `knowledge/product/p002_1_version_1_release_framework/evidence/2026-07-26_ksi_validation/` → canonical scores in `knowledge/product/ep005_1_ksi_validation_evidence/` (Validated KSI **59**; Gate G1 **FAIL** as of 2026-07-26).

---

### G2 — Constitutional compliance

**Objective:** Version 1 declaration does not violate Product, Educational, or Architecture constitutions.

| Criterion | Measurable rule |
|---|---|
| G2.1 | Vision 2030 Final Test recorded **Pass** for the Version 1 claim set |
| G2.2 | No active Never-Build violation in production defaults (activity theatre as success, opaque AI educational truth, mastery theatre, public registration without programme authority) |
| G2.3 | Educational Constitution claim-honesty: absence of evidence remains unknown; no dual educational truths on student surfaces |
| G2.4 | EVF Educational Release Gate outcome **APPROVED** or **CONDITIONAL APPROVAL** with holds cleared for the Version 1 claim class |
| G2.5 | Architecture Constitution: one Education OS runtime; no second educational brain in production defaults |
| G2.6 | Curriculum V1 and V2 remain loadable and traversable |
| G2.7 | Material EP/P programmes since P-001.1 effective date have Student Impact Assessments filed (V1-K4) |
| G2.8 | ADR index current for boundary-affecting changes in the claim window |

---

### G3 — Explainability coverage

**Objective:** Student-facing intelligence explains itself under P-001.2.

| Criterion | Measurable rule |
|---|---|
| G3.1 | Mandatory Explanation Schema attached on production-default Recommendation, Planning, and Readiness student surfaces (EP-003.1 / .2 / .3 contracts) |
| G3.2 | Explainability Review Checklist **Pass** (or Product + Educational waiver) for every in-scope EP/P programme in the claim window that changed student-facing intelligence |
| G3.3 | K8 ≥ 70 with checklist-backed evidence (links G1.5) |
| G3.4 | Runtime A consistency: same decision class yields consistent explanation structure across Dashboard / Coach / Insights / Plan / Readiness / Journey (spot-check pack) |
| G3.5 | Zero open P1 explainability honesty defects (fabricated reasons, hidden confidence, technical jargon on student surfaces) |

---

### G4 — Recommendation Quality compliance

**Objective:** Student-facing recommendations meet P-001.3 quality law.

| Criterion | Measurable rule |
|---|---|
| G4.1 | Recommendation Review Checklist **Pass** (or waiver) for every in-scope EP/P programme in the claim window |
| G4.2 | K2 category score ≥ **50** (V1-K2 floor); aspirational pillar ≥ 70 tracked but not a hard substitute for G1 |
| G4.3 | Decision Framework ladder / plan-coherence labelling present on production-default primary recommendations (EP-003.1) |
| G4.4 | Scorecard evaluation filed for the claim window (precision sample + qualitative proxies where instrumentation incomplete); **0** hard-gate precision failures (wrong topic family / plan fight) in production defaults |
| G4.5 | Recommendation-effectiveness **marketing** remains frozen unless EP-001 O8 / approved PRD evidence lifts the freeze |

---

### G5 — Planning Quality compliance

**Objective:** Daily plans / mission surfaces satisfy the PlanningService Quality Contract.

| Criterion | Measurable rule |
|---|---|
| G5.1 | Schema-complete daily plan and dashboard mission surfaces on production defaults (`explanation_schema_complete = True` when quality module applies) |
| G5.2 | Planning quality automated tests green (`tests/services/test_planning_quality_ep003_3.py` or successor) |
| G5.3 | No conflicting durations or competing “today” directives on the same day in production smoke / dogfood pack |
| G5.4 | Personalisation (if flag ON) remains fail-open, evidence-bound, and non-authoritative (EP-004.3 rules); flag OFF is acceptable if claimed as gated |
| G5.5 | K1 score contributes to G1; planning-specific honesty incidents = FAIL |

---

### G6 — Readiness Quality compliance

**Objective:** Readiness surfaces satisfy the ReadinessService Quality Contract without false certainty.

| Criterion | Measurable rule |
|---|---|
| G6.1 | Schema-complete readiness / intelligence packaging on production defaults |
| G6.2 | Readiness quality automated tests green (`tests/services/test_readiness_quality_ep003_2.py` or successor) |
| G6.3 | Honest refusal / “cannot yet be estimated” path verified; no Exam Ready marketing without gates |
| G6.4 | Drivers, confidence labels, and next action present on reviewed surfaces |
| G6.5 | K3 score contributes to G1; readiness overclaim incidents = FAIL |

---

### G7 — Performance

**Objective:** Student-critical surfaces meet published budgets under CI and agreed operator sampling.

| Criterion | Measurable rule |
|---|---|
| G7.1 | CI soft budgets green: `pytest tests/ga/test_performance_benchmarks.py` per `docs/ga/PERFORMANCE_BASELINE.md` |
| G7.2 | Staging or production operator sample recorded for Dashboard, Journey, health ready (or HOLD with no high-traffic claim) |
| G7.3 | No unexplained P1 latency regression vs previous certified baseline without debt entry + HOLD |

---

### G8 — Reliability

**Objective:** Production posture is stable enough for the declared cohort.

| Criterion | Measurable rule |
|---|---|
| G8.1 | Health `/health/live` and `/health/ready` pass on the tagged deploy fingerprint |
| G8.2 | Production smoke pack pass (Release Protocol + GA checklist as applicable) |
| G8.3 | No open Sev-1 production incidents unresolved for the claim window |
| G8.4 | Rollback path documented and recently verified (playbook / drill note or last successful rollback record) |
| G8.5 | Backup / recovery posture acknowledged per `docs/production/BACKUP_AND_RECOVERY.md` for the release class |

---

### G9 — Production telemetry

**Objective:** Operators can observe learning-relevant and operational signals without inventing educational scores.

| Criterion | Measurable rule |
|---|---|
| G9.1 | Analytics / event instrumentation for the claim window is either (a) production-active under approved go-live, or (b) explicitly gated OFF with no overclaim that metrics are live |
| G9.2 | Foundational operational logs (request, error, slow_request) available for the tagged version |
| G9.3 | Dual-run / soak / cutover telemetry for any flag intended ON in Version 1 defaults reviewed healthy (or flag remains OFF) |
| G9.4 | Privacy / EVENT_CATALOGUE constraints respected — no unlawful educational score invention in telemetry |

---

### G10 — Security and data integrity

**Objective:** Authentication, authorization, secrets, and data integrity meet GA bar for Version 1.

| Criterion | Measurable rule |
|---|---|
| G10.1 | GA security review posture current: `docs/ga/SECURITY_REVIEW.md` residuals acknowledged; no new criticals open |
| G10.2 | Production `SECRET_KEY` not default; factory production validation intact |
| G10.3 | CSRF, session cookies, security headers behaviour preserved |
| G10.4 | Ownership scoping intact for personal resources (plans, missions, progress) |
| G10.5 | Dependency audit (`pip-audit` or successor) reviewed for the tag; criticals blocked or explicitly HOLD-accepted by Security |
| G10.6 | No secrets / `.env` / credentials in release artefacts |
| G10.7 | Data integrity: migrations applied safely; StartupService idempotent path; no casual raw DDL from request handlers |

---

### G11 — Test coverage

**Objective:** Automated verification covers architecture, GA, and Version 1 quality contracts.

| Criterion | Measurable rule |
|---|---|
| G11.1 | `pytest` green for the release candidate (CI required suites) |
| G11.2 | `ruff` clean for changed paths policy (CI) |
| G11.3 | Architecture / curriculum invariant tests green (V1/V2 loadable) |
| G11.4 | GA package relevant to release class green (`tests/ga/` as required) |
| G11.5 | Quality-contract suites for recommendation / planning / readiness green when those surfaces are in production defaults |
| G11.6 | Flake quarantine discipline: quarantined tests listed; no silent skip of hard-gate suites |

---

### G12 — Production feature-flag readiness

**Objective:** Version 1 production defaults are intentional, documented, and reversible.

| Criterion | Measurable rule |
|---|---|
| G12.1 | Published **Version 1 flag matrix**: every student-visible educational flag listed with intended production default (ON / OFF), owner, and rollback switch |
| G12.2 | Flags claimed as Version 1 behaviour are ON in production (or claim language excludes them) |
| G12.3 | Flags that remain OFF are not marketed as live student capability |
| G12.4 | Cutover / dual-run / soak prerequisites satisfied for every flag intended ON (health monitors green or waiver) |
| G12.5 | `.env.example` / config docs match the flag matrix |
| G12.6 | Emergency kill-switch / flag OFF path documented for high-risk educational flags |

---

## 5. Validation process

### 5.1 Process overview

```
1. Freeze claim window + candidate version / tag
2. Assemble Version 1 Evidence Package (see Evidence Requirements)
3. Score each gate G1–G12 → PASS / FAIL / HOLD
4. Educational Gate Owner confirms EVF outcome (feeds G2.4)
5. Product owner drafts Go / No-Go recommendation
6. Sign-off board (see §5.3)
7. Record decision in Go / No-Go artefact + update VERSION_1_READINESS.md
8. Only on GO: allow “Version 1 production-ready” claim language
```

### 5.2 Evidence required (summary)

Full catalogue: [`VERSION_1_EVIDENCE_REQUIREMENTS.md`](VERSION_1_EVIDENCE_REQUIREMENTS.md).

Minimum package contents:

1. Validated KSI assessment (≤ 90 days)  
2. Constitutional compliance memo (Vision / Educational / Architecture + EVF outcome)  
3. Explainability coverage pack (checklists + spot-checks)  
4. Recommendation / Planning / Readiness quality packs  
5. Performance, reliability, telemetry, security, test, flag-matrix packs  
6. Signed Go / No-Go decision record  

### 5.3 Sign-off responsibilities

Under GP-001 (founder-operated), each row is a **capacity** exercised via a Founder Review (Reviewer · Date · Decision · Notes). The same person may hold multiple capacities; each required capacity still needs its own review record. Independent second-assessor duties (G1.7) are **not** satisfied by capacity concentration alone.

| Capacity | Signs | Scope |
|---|---|---|
| **Product Owner** | G1, claim language, overall GO / NO-GO draft | Usefulness bar; Final Test; marketing freeze honesty |
| **Educational Gate Owner** | G2.3–G2.4, G3–G4 educational honesty | EVF outcome; educational claim safety |
| **Engineering Owner (architecture lens)** | G2.5–G2.6, G2.8 | One runtime; curriculum V1/V2; ADR currency |
| **Engineering Owner** | G5–G9, G11–G12 (technical) | Quality contracts, perf, reliability, tests, flags |
| **Privacy Owner (security lens)** | G10 | Security review, secrets, dependency criticals |
| **Operations Owner (release lens)** | Deploy fingerprint, smoke, rollback readiness | Execution of Release Playbook; does not alone declare Version 1 |
| **Product Board Chair** | Overall recommendation record | Publishes GO / CONDITIONAL GO / NO GO / DEFER after capacity reviews |

Any hard-gate FAIL → overall **NO-GO**. Any HOLD → overall **GO WITH CONDITIONS** at best (see Go / No-Go Guide).

Canonical matrix: `../gp001_founder_governance_model/UPDATED_APPROVAL_MATRIX.md`.

### 5.4 Release evidence package

The Version 1 Evidence Package is a dated folder or indexed manifest (recommended path pattern):

`knowledge/product/p002_1_version_1_release_framework/evidence/<YYYY-MM-DD>_v1_declaration/`

Or an equivalent index document that links immutable paths. The package is incomplete if any hard-gate lacks linked evidence.

### 5.5 Go / no-go criteria (summary)

| Outcome | When |
|---|---|
| **GO** | All hard gates PASS; no material HOLDs; EVF APPROVED (or CONDITIONAL with holds cleared); claim language approved |
| **GO WITH CONDITIONS** | All educational honesty / security criticals PASS; remaining residuals are HOLDs with claim restrictions |
| **NO-GO** | Any hard-gate FAIL; EVF REJECTED; unresolved honesty incident; validated KSI < 80; K8 < 70; any category < 50 |
| **DEFER** | Evidence package incomplete or confidence Low on KSI |

Full decision rules: [`VERSION_1_GO_NO_GO_GUIDE.md`](VERSION_1_GO_NO_GO_GUIDE.md).

---

## 6. Compatibility with existing release systems

| System | Continues to own | This framework adds |
|---|---|---|
| EVF Educational Release Gate | Educational trust to release | Consumed as G2.4 input |
| EP-003 / EP-004 Go / No-Go | Cohort / effectiveness experimental decisions | Consumed as G1.9; do not replace this framework |
| Release Playbook / Protocol | How to tag, deploy, smoke, rollback | When Version 1 *declaration* is allowed |
| VERSION_1_READINESS.md | Area status tracker | Must align statuses to G1–G12 evidence |
| GA certification | Operational GA bar | Necessary but insufficient for Version 1 declaration |
| P-001.1 V1-K1…V1-K7 | KSI-lens success criteria | Fully embedded in G1 (+ cross-links in G2–G4) |

---

## 7. Recalculation and re-declaration

| Trigger | Action |
|---|---|
| Material educational behaviour change after GO | Re-run affected gates; may revoke claim language until re-GO |
| KSI assessment older than 90 days | G1 fails until re-score |
| Sev-1 honesty or security incident | Automatic claim freeze → NO-GO until cleared |
| Flag matrix change affecting student-visible defaults | Re-run G12 (+ related quality gates) |

---

## 8. Amendment

Amendments require:

1. Founder Review — Product Owner capacity (GP-001).  
2. Version bump on this document.  
3. Consistency check against Vision 2030, Educational Constitution, Architecture Constitution, PSF, P-001.2, P-001.3.  
4. Update to Acceptance Checklist / Go-No-Go Guide / Evidence Requirements if gate IDs or hard/HOLD rules change.  
5. Note in `knowledge/GOVERNANCE.md` if hierarchy rank or decision type changes.

---

## References

- [`VERSION_1_ACCEPTANCE_CHECKLIST.md`](VERSION_1_ACCEPTANCE_CHECKLIST.md)
- [`VERSION_1_GO_NO_GO_GUIDE.md`](VERSION_1_GO_NO_GO_GUIDE.md)
- [`VERSION_1_EVIDENCE_REQUIREMENTS.md`](VERSION_1_EVIDENCE_REQUIREMENTS.md)
- `knowledge/product/p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md`
- `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md`
- `knowledge/product/p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_STANDARD.md`
- `knowledge/product/vision/PRODUCT_VISION_2030.md`
- `knowledge/educational_validation/EDUCATIONAL_RELEASE_GATE.md`
- `knowledge/RELEASE_PLAYBOOK.md`
- `knowledge/VERSION_1_READINESS.md`
- `docs/ARCHITECTURE_CONSTITUTION.md`
- `docs/ga/PERFORMANCE_BASELINE.md`
- `docs/ga/SECURITY_REVIEW.md`

---

**End of VERSION_1_RELEASE_FRAMEWORK**
