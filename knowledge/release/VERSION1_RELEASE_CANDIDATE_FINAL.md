# Version 1 Release Candidate Finalisation

**Capability ID:** V1RP-001  
**Programme:** Version 1 Release Programme  
**Title:** Release Candidate Finalisation  
**Priority:** P0  
**Status:** SUBMITTED — awaiting Executive Review  
**Version:** 1.0  
**Date:** 2026-07-16  
**Nature:** Release governance only — no application code, no feature redesign, no Version 2 work, no commit / tag / deploy under this capability  
**Classification:** Release-governance authority — subordinate to the Educational Constitution, Educational Governance Review Standard (EGI-003 §7), and the Release Protocol.

---

## Purpose

Define exactly what must be true before `VERSION1-RC1` is **created** and **submitted to Internal Alpha**.

This document is the single decision authority for the question:

> **Can a Version 1 Release Candidate be created now — yes or no — and if not, precisely what remains?**

It does not create the Release Candidate. It removes all uncertainty about whether one may be created, by consolidating every prior release-governance artefact into one finalisation gate set, one checklist, one evidence list, and one promotion rule.

---

## Authority

| Authority | Role | Path |
|-----------|------|------|
| Educational Governance Certification V1 (EIP-007) | Educational pillar — **APPROVED / 100‑100** | `knowledge/educational/EDUCATIONAL_GOVERNANCE_CERTIFICATION_V1.md` |
| Educational Governance Review Standard (EGI-003 §7) | Engineering + Architecture + Educational triad | `knowledge/educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` |
| Release Protocol v2.0 | Engineering / operational release procedure, STOP CONDITIONS | `docs/process/RELEASE_PROTOCOL.md` |
| V1R-001 Version 1 Release Certification | Prior composite certification (NOT READY at assessment) | `knowledge/release/KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` |
| V1S-001 Engineering Stabilisation Backlog | Engineering blocker inventory (ES / AR / RB items) | `knowledge/release/ENGINEERING_STABILISATION_BACKLOG.md` |
| V1S-002 Engineering Review | Critical test STOP closure record | `knowledge/release/V1S002_ENGINEERING_REVIEW.md` |
| V1S-003 Release Candidate Preparation | RC content set, staging plan, fingerprint definition | `knowledge/release/VERSION1_RELEASE_CANDIDATE.md` |
| V1S-004 Release Candidate Validation Plan (APPROVED) | Internal Alpha validation objectives, gates, thresholds | `knowledge/release/RELEASE_CANDIDATE_VALIDATION_PLAN.md` |
| V1S-005 Internal Alpha RC Validation Pack | Tester forms, classification, decision matrix, executive summary | `knowledge/release/INTERNAL_ALPHA_RELEASE_VALIDATION.md` |
| Product Trust Programme (PTP-000 … PTP-005) | Version 1 product trust / cohesion outcomes | `knowledge/product/PRODUCT_TRUST_PROGRAMME.md`, `knowledge/product/PTP-005_VERSION1_COHESION.md` |
| Learning Experience Programme (LXP-001 … LXP-004) | Daily learning loop | `knowledge/product/LEARNING_EXPERIENCE_PROGRAMME.md` |
| Blind Internal Alpha Review v3 (BIAR-V3) | Student trust evidence — **64 / 100, CONDITIONAL YES** | `BLIND_INTERNAL_ALPHA_REVIEW_V3.md` |

**Method.** This capability applies **existing** criteria only. It invents no new release rule, no new educational law, and no new architecture. It scores the finalisation state against the authorities above and against the current repository state on `main`.

---

## Background posture (as declared to this capability)

| Programme / gate | Declared status |
|------------------|-----------------|
| Educational Integrity Programme (EIP-001 … EIP-007) | **COMPLETE** |
| Learning Experience Programme Sprint 1 (LXP-001 … LXP-004) | **COMPLETE** |
| Product Trust Programme (PTP-001 … PTP-005) | **COMPLETE** |
| Blind Internal Alpha Review v3 | **COMPLETE** (64 / 100, CONDITIONAL YES) |
| Architecture | **FROZEN** |

These are the programme inputs. This capability confirms their **release-governance consequences** and identifies the residual conditions between the current tree and a lawfully created `VERSION1-RC1`.

---

## 1. Executive Summary

The Version 1 educational, learning-experience, and product-trust programmes are complete. The two Blind Review v2 criticals (hollow-subject trap, duplicate practice-capture flow) are closed, the dashboard tells one coherent coverage story, guidance is explainable (What / Why / Next), and the product now openly states that its estimates are self-reported and unverified. Blind Internal Alpha Review v3 — the programme's designated external trust test — returned **CONDITIONAL YES (64 / 100)** with **no new critical release blocker**.

That is the strongest release posture in the product's history and materially better than the V1R-001 certification snapshot (NOT READY, 73 / 100), which failed principally on a two-test engineering STOP, an unrecorded Architecture disposition, and unconfirmed Internal Alpha trust.

Against existing gates, this finalisation finds the situation as follows:

| Pillar | Finding |
|--------|---------|
| Educational Governance | **APPROVED** — EIP-007, 100 / 100. No condition remains on this pillar. |
| Engineering | **One active STOP condition.** The two legacy delete-flash assertions (ES-C-001 / F1 / F2) are reconciled to the EIP-005 continuity flash in the working tree (confirmed PASS). However, a full-suite run on the current tree (2026-07-16) returns **1 failed / 2239 passed** — a **new time-dependent failure** (`test_recommendation_card_rendered_when_composer_succeeds`) where the dashboard renders no "Today's Study Session" card because today's date now falls outside the fixture plan's date range, so `planning_service` generates no mission and the asserted `Start Today's Session` CTA is absent. Release Protocol STOP ("tests fail") is therefore **active**. This must be reconciled (ES-C-004) before RC. |
| Architecture | **Frozen; documentation closure outstanding.** Architecture is declared FROZEN, but numerous capability headers still read "awaiting / pending Architecture Review." The recorded Architecture disposition must be stamped before RC (documentation gate, not a redesign). |
| Product Trust / Cohesion | **One residual trust seam.** PTP-005 Version 1 Cohesion is an **approved design that is not yet implemented**. Its two Critical findings — **F-1 version identity contradiction** (`1.0.0` / `v1.1` / `4.3` / none) and **F-2 the daily object has five names** — remain live in the tree, and BIAR-V3 independently flagged the version contradiction as a High, three reviews running. |
| Release Integrity | **No candidate exists yet.** `HEAD` is still `2f99e6b` (`v0.9.2`); the Integrity + LXP + PTP delta is uncommitted; no `VERSION1-RC1` commit, fingerprint, or tag decision exists. |
| Internal Alpha readiness | **Ready to run, not run.** V1S-004 plan is APPROVED and V1S-005 provides the validation pack; execution is a post-RC activity, not a pre-RC blocker. |

**Finalisation verdict.** A Version 1 Release Candidate **cannot be created today** but **can be created** once the finalisation checklist (§2) is satisfied. The remaining work is bounded, authorised, and contains **no new Version 1 feature design**:

1. **Fix the one active test STOP (ES-C-004).** A full-suite run on the current tree returns **1 failed / 2239 passed**; the failure is a brittle, wall-clock-dependent dashboard test expectation (the product behaves correctly). This is a Release Protocol STOP and must be green on the candidate commit (§Gate G2).
2. **Reconcile version identity** (single source of truth; gate G4 / PTP-005 F-1). This is the one cheap, in-scope, trust-brand-damaging item that BIAR-V3 named as a must-fix and that PTP-005 classifies Critical. It is satisfied by an authorised implementation capability (PTP-005 execution), **not** by V1RP-001.
3. **Record the (FROZEN) Architecture disposition**, run release-touched Ruff, then create the single intentional V1S-003 commit, capture its fingerprint, and take a version-tag decision.

Everything else is either already true (educational governance, learning loop, subject gating, single workflow, dashboard IA) or explicitly **accepted debt / Version 2** (§Accepted Technical Debt, §Known Limitations). No open item requires a feature to be built.

---

## 2. Release Candidate Checklist

Each item is binary. `VERSION1-RC1` may be created only when every **REQUIRED** item is `PASS`. `PENDING` means the evidence has not yet been produced; it is not a failure, but it blocks creation until produced.

| # | Item | Required | Status | Evidence / owner |
|---|------|:-------:|:------:|------------------|
| C-1 | Educational Governance APPROVED (EIP-007, 100 / 100) | Yes | **PASS** | `EDUCATIONAL_GOVERNANCE_CERTIFICATION_V1.md` |
| C-2 | EIP-001…007 educational programme COMPLETE | Yes | **PASS** | Educational knowledge set + regression suite |
| C-3 | LXP Sprint 1 daily loop COMPLETE (LXP-001…004) | Yes | **PASS** | Session → Practice Outcome → Feedback templates + tests |
| C-4 | Product Trust PTP-001…004 implemented (subject gate, single workflow, evidence honesty, dashboard IA) | Yes | **PASS** | PTP-001…004 docs; BIAR-V3 confirms v2 criticals closed |
| C-5 | Legacy delete-flash assertions reconciled to EIP-005 continuity (ES-C-001 / F1 / F2) | Yes | **PASS** | `tests/test_routes.py:503,505`; `tests/test_smoke.py:976,978,990,992` assert continuity flash — confirmed passing |
| C-6 | Full automated suite green on the **candidate commit** | Yes | **FAIL** | Current tree run (2026-07-16): **1 failed / 2239 passed**. Failing node `tests/dashboard/test_educational_dashboard_integration.py::TestDashboardFeatureFlagOn::test_recommendation_card_rendered_when_composer_succeeds`. Must reach 0 failed (see ES-C-004 / E-2) |
| C-7 | Ruff clean on release-touched modules (Protocol hygiene, ES-H-003) | Yes | **PENDING** | Ruff on EIP/LXP/PTP-touched paths |
| C-8 | Architecture disposition **recorded** for EIP + IA + LXP + PTP + V1 candidate (Architecture FROZEN) | Yes | **PENDING** | Update capability headers from "awaiting Architecture Review" to recorded outcome (AR-A / AR-D) |
| C-9 | Version identity reconciled to one source of truth (PTP-005 F-1) | Yes | **PENDING** | `APP_VERSION` single source; Settings / footers / error pages agree (implementation via PTP-005) |
| C-10 | Daily-object naming reconciled (PTP-005 F-2) **or** Executive waiver recorded | Yes | **PENDING** | One canonical student noun, or written waiver with backlog owner |
| C-11 | Clean intentional RC commit staged per V1S-003 content set; research/tooling excluded | Yes | **PENDING** | V1S-003 staging plan; `research/internal_alpha/week_001/`, `scripts/` excluded |
| C-12 | Working tree contains no secrets / caches / generated noise in the stage set | Yes | **PASS** | V1S-003 Task 3 cleanliness — none observed |
| C-13 | Version tag strategy decided (no silent reuse of historical `v1.0.0`) | Yes | **PENDING** | Executive version-tag decision (see §Version Identity) |
| C-14 | RC fingerprint (commit SHA) captured after commit | Yes | **PENDING** | Post-commit; recorded into `knowledge/release/` |
| C-15 | Internal Alpha validation plan APPROVED (V1S-004) and pack ready (V1S-005) | Yes | **PASS** | `RELEASE_CANDIDATE_VALIDATION_PLAN.md` (APPROVED); `INTERNAL_ALPHA_RELEASE_VALIDATION.md` |
| C-16 | Release Notes drafted for `VERSION1-RC1` | Yes | **PASS (this doc §Release Notes)** | §Release Notes below; finalise SHA/date on commit |
| C-17 | Rollback strategy defined | Yes | **PASS (this doc §Rollback Strategy)** | §Rollback Strategy below |
| C-18 | Accepted Technical Debt + Known Limitations catalogued and owned | Yes | **PASS (this doc)** | §Accepted Technical Debt, §Known Limitations |
| C-19 | BIAR-V3 residual product-ceiling items confirmed as Version 2 (no new critical) | Yes | **PASS** | BIAR-V3 §15 — no new critical; in-app practice is a product ceiling / V2 |

**Checklist summary:** 11 PASS / 7 PENDING / **1 FAIL (C-6)**. The single FAIL is a time-dependent test-expectation defect (ES-C-004), not a missing Version 1 feature. Every PENDING item is a documentation, evidence-capture, hygiene, or already-authorised-implementation (PTP-005) action. RC creation is blocked until C-6 is green and the PENDING REQUIRED items close.

---

## 3. Approval Gates

RC creation is authorised only when all gates below hold. Each gate maps to an existing authority; none is new.

### Gate G1 — Educational Governance (EGI-003 §7 educational pillar)
- **Requirement:** Educational Governance Review outcome APPROVED, no automatic NON-COMPLIANT trigger reopened.
- **State:** **MET.** EIP-007 APPROVED, 100 / 100, Categories A–H FULL.

### Gate G2 — Engineering (Release Protocol §3 / STOP CONDITIONS + EGI-003 §7 engineering pillar)
- **Requirement:** Full `pytest` green on the candidate commit; Ruff clean on release-touched modules; no open Release Protocol STOP CONDITION.
- **State:** **FAIL — active STOP.** The historical two-test STOP (F1/F2) is reconciled in-tree, but a current full-suite run returns **1 failed / 2239 passed**. Release Protocol STOP ("tests fail") is active. Gate closes only after ES-C-004 is fixed, the suite is green on the candidate commit (C-6 / E-2), and release-touched Ruff (C-7) is recorded.

#### ES-C-004 — Time-dependent dashboard recommendation-card test failure (new engineering-stabilisation item)

| Field | Assessment |
|-------|------------|
| **Failing node** | `tests/dashboard/test_educational_dashboard_integration.py::TestDashboardFeatureFlagOn::test_recommendation_card_rendered_when_composer_succeeds` (line 197) |
| **Observed** | HTTP 200; the EI recommendation card renders, but the dashboard contains **no "Today's Study Session" card**, so the asserted `b"Start Today's Session"` CTA is absent. |
| **Root cause** | Wall-clock dependence. The current date (2026-07-16) falls **outside** the `study_plan` fixture's date range, so `planning_service` logs `Today … is outside study plan 1 date range; no mission generated` and the session card is correctly suppressed. The product behaves correctly; the **test expectation is brittle** (it assumes "today" always lies inside the fixture plan window). |
| **Classification** | **Legacy / brittle expectation** — same family as ES-C-001 (F1/F2): the product path is intentional; the test is stale/time-dependent. **Not** a product, educational, or architecture defect. |
| **Regression risk** | **Low** if fixed by injecting a deterministic in-range date (per testing rule 05: "prefer date injection", "no reliance on wall-clock flakiness"). **High** if "fixed" by loosening the mission date gate — that would regress `planning_service` correctness. |
| **Coupling** | The asserted CTA string `"Start Today's Session"` is one of the drifting variants in PTP-005 F-8 / F-2. If PTP-005 renames the daily-object CTA, this assertion must be updated in the same pass. |
| **Recommended action** | Under an authorised engineering-stabilisation step (not this capability): make the fixture plan window deterministically include the session date (freeze/inject date), then re-run the full suite to green. Do **not** change the mission date-range gate or the delete-flash copy. |

### Gate G3 — Architecture (EGI-003 §7 architecture pillar; Architecture FROZEN)
- **Requirement:** Architecture disposition recorded APPROVED (or FROZEN-accepted) for the Integrity Programme, IA stabilisation, LXP, PTP, and the Version 1 candidate structure; layering + curriculum V1/V2 invariants preserved.
- **State:** **CONDITIONAL — documentation closure pending.** Architecture is FROZEN; the recorded disposition must replace "awaiting Architecture Review" headers (C-8). Layering / curriculum invariants are directionally preserved on reviewed paths (V1R-001 §7).

### Gate G4 — Product Trust / Cohesion (Product Trust Programme; BIAR-V3)
- **Requirement:** PTP-001–004 outcomes live (MET). PTP-005 Version 1 Cohesion Criticals resolved: **F-1 one version identity** (required) and **F-2 one daily-object name** (required, or Executive-waived with backlog).
- **State:** **CONDITIONAL.** PTP-005 is approved design, not implemented. F-1 is the single BIAR-V3 must-fix that is in-scope and cheap; it must land (via authorised PTP-005 implementation) before RC1, or the RC ships a self-contradicting version number into a trust-first product — which this gate forbids.

### Gate G5 — Release Integrity (Release Protocol repository / fingerprint gates; V1S-003)
- **Requirement:** One clean intentional RC commit from the V1S-003 content set; research/tooling excluded; tree free of secrets/noise; fingerprint captured; version-tag strategy decided (no silent `v1.0.0` reuse).
- **State:** **CONDITIONAL — candidate not yet created.** All preconditions are specified (V1S-003); execution is a separate Executive-authorised step.

### Gate G6 — Internal Alpha Validation readiness (V1S-004 / V1S-005)
- **Requirement:** Validation plan APPROVED and pack ready so the RC can be submitted to Internal Alpha immediately after creation.
- **State:** **MET.** V1S-004 APPROVED; V1S-005 pack ready. Execution (ACCEPT / CONDITIONAL / REJECT / INCOMPLETE) is post-RC and governed by §Promotion Criteria.

### Gate summary

| Gate | Pillar | State | Blocking? |
|------|--------|-------|:---------:|
| G1 | Educational Governance | MET | No |
| G2 | Engineering | **FAIL — 1 failing test (ES-C-004); Ruff pending (C-7)** | Yes — active STOP |
| G3 | Architecture | Doc closure pending (C-8) | Yes until recorded |
| G4 | Product Trust / Cohesion | F-1 required; F-2 required-or-waived | Yes until resolved/waived |
| G5 | Release Integrity | Candidate not created (C-11…C-14) | Yes until executed |
| G6 | Internal Alpha readiness | MET | No |

**RC creation is authorised when G2–G5 close.** G1 and G6 are already met.

---

## 4. Required Evidence

The following artefacts must exist and be attached (in `knowledge/release/` or referenced from the RC commit) before RC creation is declared complete.

| ID | Evidence | Satisfies | Producer | State |
|----|----------|-----------|----------|-------|
| E-1 | EIP-007 Educational Governance Certification (APPROVED, 100/100) | G1 / C-1 | Educational Governance | **Exists** |
| E-2 | Full-suite `pytest` **green** (0 fail) on the candidate commit | G2 / C-6 | Engineering | **FAIL now — current run 1 failed / 2239 passed (ES-C-004); must reach 0 fail on candidate commit** |
| E-3 | Ruff report on release-touched modules (clean, or documented residual) | G2 / C-7 | Engineering | **To produce** |
| E-4 | Recorded Architecture disposition for EIP / IA / LXP / PTP / V1 candidate | G3 / C-8 | Architecture | **To record (FROZEN)** |
| E-5 | PTP-005 F-1 version-identity fix landed (single `APP_VERSION`) | G4 / C-9 | PTP-005 implementation | **To land** |
| E-6 | PTP-005 F-2 daily-object naming resolution or Executive waiver | G4 / C-10 | PTP-005 impl / Executive | **To land or waive** |
| E-7 | RC commit SHA + staged content manifest per V1S-003 | G5 / C-11, C-14 | Release engineering | **On commit** |
| E-8 | Version-tag decision record (RC identifier ↔ git tag) | G5 / C-13 | Executive | **To decide** |
| E-9 | BIAR-V3 review recorded as trust evidence (CONDITIONAL YES) | G4 / C-19 | Product | **Exists** |
| E-10 | V1S-004 APPROVED plan + V1S-005 validation pack | G6 / C-15 | Release | **Exists** |

**Evidence rule.** E-2 must be produced on the *actual candidate commit* (post-stage, post-PTP-005-F-1), not on a historical tree — a green run on a stale tree does not satisfy G2.

---

## 5. Accepted Technical Debt

Carried forward from EIP-007 / V1R-001 and reaffirmed. These are **intentional, owned, documented** — they do **not** block RC creation and must **not** be reclassified as Version 1 defects.

| ID | Debt | Disposition |
|----|------|-------------|
| V1-TD-001 | Thin high Estimated Knowledge stage-density floor | Accept — understatement preferred over mastery theatre |
| V1-TD-002 | Coaching Accept / Not today / Later not fully productised | Accept — polish backlog |
| V1-TD-003 | Latent `MissionOptimizer` unrendered | Accept — quarantine before any surface rewire (ES-H-002) |
| V1-TD-004 | Interim `TopicProgress` estimate store vs full Twin succession | Accept — transitional architecture |
| V1-TD-005 | Internal identifiers still say `mastery_*` / stage `Mastered` | Accept — persistence compatibility under EIP-006 student meaning |
| V1-TD-006 | Registration closed; admin bootstrap only | Accept — intentional Version 1 security posture |
| V1-TD-007 | Founder automation manually triggered (no scheduler) | Accept (FSI-005) |
| V1-TD-008 | Per-topic Learning Outcomes show "Not available yet" | Accept — presentation chrome, not educational falsity (BIAR-V3 Medium) |
| V1-TD-009 | Onboarding re-asks completed sections (wizard vs Educational History) | Accept for RC **only if** not resolved by PTP-005 F-3; else close (BIAR-V3 Medium / PTP-005 F-3) |
| V1-TD-010 | Disclaimer/hedging fatigue (honest but repetitive) | Accept residual after PTP-005 F-6 dedup; honesty preserved |
| V1-TD-011 | SA `Query.get()` → `Session.get()` and `datetime.utcnow()` deprecations | Accept — maintenance sweep post-RC (ES-M-001/002) |

**Engineering-hygiene note (not educational falsity):** release-touched Ruff (E-3) is required for the "clean" claim; broader historical lint remains non-blocking maintenance.

---

## 6. Known Limitations

The boundaries of what `VERSION1-RC1` is — stated so no reviewer mistakes a boundary for a defect.

1. **Self-reported evidence only.** All Estimated Knowledge / readiness signals derive from student-entered practice counts; nothing verifies them. The product now states this openly (PTP-003). This is the hard trust ceiling BIAR-V3 identifies and it is **Version 2** to lift.
2. **No in-app study or practice content.** Kwalitec organises, schedules, and records study done in external materials (ActEd, Core Reading). Providing in-app content/question banks is explicitly **Version 2** (LXP §9, PTP-000 §7.2). This is the BIAR-V3 High that separates "CONDITIONAL YES" from unconditional YES — a **product ceiling, not a bug**.
3. **Supported subjects only.** Unsupported papers are gated server-side (PTP-001); breadth beyond supported subjects is out of Version 1 scope.
4. **Learning Mode only.** Mission topic selection is sequential Learning Mode; Adaptive / Revision / Diagnostic modes are Constitution Article VI Version 2 work.
5. **Product Blueprint Epics 2–4** (full EI ecosystem, multi-provider) are Version 2 evolution, not Version 1 holes.
6. **Roadmap document** remains draft — an operator documentation gap, not a student-facing feature hole.

None of the above is a release blocker for an **Internal Alpha Release Candidate**; each is an intentional Version 1 boundary or a Version 2 line item.

---

## 6A. Version Identity (verification)

Version identity is both a **product-trust** concern (PTP-005 F-1; BIAR-V3 High) and a **release-integrity** concern (which git tag names this candidate). Current observed state:

| Surface | Value | Source |
|---------|-------|--------|
| `pyproject.toml` | `1.0.0` | `pyproject.toml:3` |
| Settings → General → "Version" | `1.0.0` (hardcoded) | `settings/index.html:55` |
| Settings → Internal Alpha → "Application version" | `1.0.0` (dynamic) | `internal_alpha_status_service.py:21` |
| Settings → Internal Alpha → "Internal Alpha version" | `4.3` | `internal_alpha_status_service.py:22` |
| Auth + error page footers | `Kwalitec v1.1` | `auth_base.html:34`, `errors/*.html` |
| Authenticated app shell | *(no version shown)* | `layouts/base.html` |
| Existing git tags on ancestry | `v1.0.0`, `v1.2.0`, `v1.3.0`, `v1.4.0-beta` (plus `v0.9.x`) | `git tag` |
| Current `HEAD` | `2f99e6b` = tag `v0.9.2` | `git log` |

**Two decisions are required before RC creation:**

1. **Displayed product version (PTP-005 F-1 / C-9).** Establish one `APP_VERSION` source of truth and render it identically on Settings, footers, error pages, and (recommended) the authenticated shell. Keep "Internal Alpha version" (`4.3`) as a **distinct, clearly-labelled internal build track**, never a competing product version. This is implemented by the authorised PTP-005 execution, not here.
2. **Release tag (C-13 / E-8).** The historical tags `v1.0.0`, `v1.2.0`, `v1.3.0`, `v1.4.0-beta` already exist on ancestry from earlier work and **do not represent this Version 1 programme's ship**. `VERSION1-RC1` must be given an unambiguous tag decided by Executive Review — it **must not silently reuse `v1.0.0`**. Recommended: an RC-explicit tag (e.g. `v1.0.0-rc1`) for the Internal Alpha candidate, reserving an immutable production `v1.0.0`-class tag for a later lawful production release once the EGI-003 §7 triad and validation ACCEPT are recorded.

Until both are settled, the product would ship the same self-contradiction BIAR-V3 has flagged for three consecutive reviews. Gate G4 (product) and Gate G5 (release integrity) both depend on this.

---

## 6B. Testing (verification)

| Item | Result |
|------|--------|
| Command | `python3 -m pytest -q` (full configured collection: `tests/` + founder + automation packages) |
| Date | 2026-07-16 |
| Result | **1 failed / 2239 passed** (~320s) |
| Failing node | `tests/dashboard/test_educational_dashboard_integration.py::TestDashboardFeatureFlagOn::test_recommendation_card_rendered_when_composer_succeeds` |
| Classification | Time-dependent / brittle test expectation (ES-C-004) — product behaves correctly; test assumes "today" is inside the fixture plan window |
| Legacy delete-flash (F1/F2 / ES-C-001) | **Reconciled — passing** (continuity flash asserted) |
| Deprecation noise | Non-blocking `Query.get()` (SA 2.0) + `datetime.utcnow()` warnings (ES-M-001/002 maintenance) |

**Gate consequence:** Release Protocol STOP ("tests fail") is **active**. C-6 / E-2 / G2 remain closed only when the suite is green (0 failed) on the actual candidate commit — after ES-C-004 is fixed and after any PTP-005 CTA rename is reflected in the assertion.

---

## 7. Release Notes

Draft release notes for `VERSION1-RC1`. Finalise the commit SHA, tag, and date at commit time.

```
==============================================================================
KWALITEC — VERSION 1 RELEASE CANDIDATE (VERSION1-RC1)
Class: Internal Alpha Release Candidate
Baseline before this RC: v0.9.2 (Internal Alpha Stabilization)
Commit SHA: <captured at commit>
Tag: <Executive version-tag decision — do not silently reuse v1.0.0>
Date: <commit date>
==============================================================================

WHAT THIS RELEASE IS
--------------------------------------------------------------------------
The first Version 1 Release Candidate: an honest, consistent study planner
and practice tracker for supported IFoA papers. It lands the Educational
Integrity Programme, the complete daily Learning Experience loop, and the
Product Trust Programme as one intentional candidate for Internal Alpha
validation.

HIGHLIGHTS
--------------------------------------------------------------------------
Educational Integrity (EIP-001…007)
  - Educational state ownership, evidence-gated estimates, explainability
    (What / Why / Next), continuity on plan changes, and Version 1 state
    refinement (Study Progress · Estimated Knowledge · Educational Guidance).
  - Educational Governance certified APPROVED (100/100).

Learning Experience (LXP-001…004)
  - One closed daily loop: Today's Study Session → Practice Outcome Capture
    → Study Session Feedback, with truthful non-mastery speech.

Product Trust (PTP-001…005)
  - Unsupported papers gated before a hollow plan can be created (PTP-001).
  - One daily close-the-day path; duplicate reflection retired (PTP-002).
  - Honest, self-report-limited evidence communication (PTP-003).
  - Single coherent Dashboard coverage story (PTP-004).
  - Version 1 cohesion: one version identity, one daily-object name,
    de-duplicated onboarding and disclaimers (PTP-005).

TRUST EVIDENCE
--------------------------------------------------------------------------
  - Blind Internal Alpha Review v3: 64/100, CONDITIONAL YES.
  - v2 criticals closed (hollow-subject trap; duplicate capture flow).
  - No new critical release blocker.

KNOWN LIMITATIONS (intentional Version 1 boundaries)
--------------------------------------------------------------------------
  - Evidence is self-reported and unverified (openly stated).
  - No in-app study/practice content (Version 2).
  - Supported subjects only; Learning Mode only.

ACCEPTED TECHNICAL DEBT
--------------------------------------------------------------------------
  - See VERSION1_RELEASE_CANDIDATE_FINAL.md §Accepted Technical Debt
    (V1-TD-001…011). None blocks Internal Alpha validation.

VALIDATION
--------------------------------------------------------------------------
  - Submitted to Internal Alpha under V1S-004 (plan) / V1S-005 (pack).
  - Promotion toward Version 1.0 requires an ACCEPT or CONDITIONAL ACCEPT
    outcome from the RC validation window.

ROLLBACK
--------------------------------------------------------------------------
  - Revert to v0.9.2; no forward-only schema migration is introduced by
    this RC beyond the already-shipped study_plan_id mission column.
==============================================================================
```

---

## 8. Rollback Strategy

RC creation must be reversible with no student data loss. Strategy follows Release Protocol §13.

| Dimension | Strategy |
|-----------|----------|
| **Baseline to restore** | `v0.9.2` (`2f99e6b`) — the last shipped Internal Alpha tag. It remains the known-good fallback for the entire RC window. |
| **Reversion mechanism** | RC1 is a single intentional commit (V1S-003). Rollback = redeploy the `v0.9.2` tag (Render) or `git revert` the RC commit on `main`; no history rewrite, no force-push. |
| **Schema / data** | RC1 introduces **no new forward-only migration** beyond the already-present `202607150001_add_study_plan_id_to_missions.py` (on the candidate, not net-new here). StartupService migrate is idempotent; downgrade path must be confirmed present before any production promotion (not required for Internal Alpha RC). |
| **Educational data compatibility** | EIP-006 keeps internal `mastery_*` identifiers (V1-TD-005); student meaning is unchanged. Reverting to `v0.9.2` does not corrupt stored `TopicProgress` — continuity is additive. |
| **Feature flags** | Internal Alpha EI flags (`ENABLE_EI_*`) remain the containment lever; a trust regression can be narrowed by flag before full rollback. |
| **Trigger conditions** | Any confirmed **Critical** finding during validation (V1S-005 §5) pauses validation and may trigger rollback to `v0.9.2` pending a new RC. |
| **Verification after rollback** | Re-run Release Protocol smoke journeys against the restored baseline; confirm login, plan, mission, dashboard, and practice capture. |

Rollback is **cheap and safe** because RC1 is a single additive commit over a tagged baseline with idempotent bootstrap and no destructive migration.

---

## 9. Promotion Criteria

Two distinct promotions are governed here. Neither is executed by this capability.

### 9.1 Promotion into existence: create `VERSION1-RC1`
Authorised when **all G2–G5 gates close** (G1, G6 already met) and the §2 checklist has **zero PENDING REQUIRED items**. Concretely: fresh green suite (E-2), release-touched Ruff (E-3), recorded Architecture disposition (E-4), version identity reconciled (E-5) with daily-object naming resolved or waived (E-6), clean intentional commit staged per V1S-003, and a version-tag decision (E-8). At that point the RC is created, fingerprinted (E-7), and submitted to Internal Alpha.

### 9.2 Promotion toward Version 1.0: after the Internal Alpha RC window
Governed by V1S-004 §6–§7 and the V1S-005 decision matrix. The RC is promoted only on:

| Outcome | Meaning | Next |
|---------|---------|------|
| **ACCEPT** | Hard gates pass; soft gates largely pass | Proceed under Release Protocol toward a lawful `v1.0.0` production operation (separate Executive authorisation) |
| **CONDITIONAL ACCEPT** | Hard gates pass; Medium backlog / soft gates missed | Continue Internal Alpha with an owned remediation backlog; no Critical/High open |
| **REJECT** | Any hard gate fails (open Critical, un-waived High, educational contradiction, dead-end, stability failure, or majority "do not trust") | Return to remediation; new RC cycle |
| **INCOMPLETE** | Coverage minimums unmet | Extend window / add testers; do not score |

**Hard gates (V1S-004 §6.1):** zero open Critical; zero un-waived High; no open educational contradiction; no primary-path dead-end; stable daily use; majority positive educational confidence. **Version 1.0 production** additionally requires the full EGI-003 §7 triad recorded APPROVED, a clean tagged `v1.0.0`, a fingerprinted deploy, and a Release Report — none of which is claimed here.

---

## 10. Success Statement

After this capability there is **no uncertainty** about whether a Release Candidate can be created:

- **Can `VERSION1-RC1` be created today, as-is?** **No** — gate G2 is a live STOP (1 failing test) and gates G3–G5 are `PENDING`.
- **Is there a hard failure?** **Yes, one** — checklist item C-6 (ES-C-004), a brittle time-dependent test expectation, not a product/educational/architecture defect and not a missing Version 1 feature. There is no open Critical educational or product finding.
- **Exactly what stands between now and a lawful RC?** Five concrete, authorised actions: (1) fix ES-C-004 (inject a deterministic in-range date; re-run to green) and record the green full-suite result on the candidate commit; (2) reconcile version identity (PTP-005 F-1) and resolve/waive daily-object naming (F-2); (3) run release-touched Ruff; (4) record the (FROZEN) Architecture disposition over the stale "awaiting review" headers; (5) create the single intentional V1S-003 commit, capture its fingerprint, and take a version-tag decision.
- **After those five?** The RC is created and submitted to Internal Alpha under the already-APPROVED V1S-004 plan and V1S-005 pack.

There are no unknowns, no new design decisions, and no application code to be written **under this governance capability** (ES-C-004 and PTP-005 F-1 are executed by their own authorised capabilities).

---

## 11. Constraints Honoured

- No application code modified.  
- No Version 1 feature redesigned.  
- No Version 2 work created.  
- No commit / tag / deploy performed.  
- No new release, educational, or architecture criteria invented — existing authorities only.

---

## 12. Cross References

| Document | Role |
|----------|------|
| `KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` | Prior composite certification (V1R-001) |
| `ENGINEERING_STABILISATION_BACKLOG.md` | Engineering blocker inventory (V1S-001) |
| `VERSION1_RELEASE_CANDIDATE.md` | RC content set / staging / fingerprint (V1S-003) |
| `RELEASE_CANDIDATE_VALIDATION_PLAN.md` | Validation plan (V1S-004, APPROVED) |
| `INTERNAL_ALPHA_RELEASE_VALIDATION.md` | Validation pack (V1S-005) |
| `EDUCATIONAL_GOVERNANCE_CERTIFICATION_V1.md` | Educational pillar (EIP-007) |
| `EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` | EGI-003 §7 triad |
| `docs/process/RELEASE_PROTOCOL.md` | Engineering/ops release procedure |
| `PRODUCT_TRUST_PROGRAMME.md` / `PTP-005_VERSION1_COHESION.md` | Product trust / cohesion outcomes |
| `LEARNING_EXPERIENCE_PROGRAMME.md` | Daily learning loop |
| `BLIND_INTERNAL_ALPHA_REVIEW_V3.md` | Student trust evidence (CONDITIONAL YES) |

---

**Stop.**  
**Return for Executive Review.**  
**Do not create the Release Candidate, commit, tag, or deploy from this capability.**

**End of V1RP-001 — Release Candidate Finalisation.**
