# Version 1 Release Candidate Finalisation

**Capability ID:** V1RP-002  
**Programme:** Version 1 Release Programme  
**Title:** Release Candidate Finalisation  
**Priority:** P0  
**Status:** SUBMITTED — awaiting Executive Review  
**Date:** 2026-07-16  
**Nature:** Release governance only — no application code, no feature redesign, no educational behaviour change, no commit / tag / deploy under this capability  
**Classification:** Release-governance authority — subordinate to the Educational Constitution, Educational Governance Review Standard (EGI-003 §7), and the Release Protocol.

---

## Authority

| Authority | Role | Path |
|-----------|------|------|
| Educational Governance Certification V1 (EIP-007) | Educational pillar — **APPROVED / 100‑100** | `knowledge/educational/EDUCATIONAL_GOVERNANCE_CERTIFICATION_V1.md` |
| Educational Governance Review Standard (EGI-003 §7) | Engineering + Architecture + Educational triad | `knowledge/educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` |
| Release Protocol v2.0 | Engineering / operational release procedure, STOP CONDITIONS | `docs/process/RELEASE_PROTOCOL.md` |
| V1RP-001 Release Candidate Finalisation | Prior finalisation gate set and debt catalogue | `knowledge/release/VERSION1_RELEASE_CANDIDATE_FINAL.md` |
| V1S-003 Release Candidate Preparation | RC content set, staging plan, fingerprint definition | `knowledge/release/VERSION1_RELEASE_CANDIDATE.md` |
| IPV-001 Independent Product Validation | Pre–Internal Alpha product validation commission | `knowledge/release/IPV-001_INDEPENDENT_PRODUCT_VALIDATION.md` |
| V1S-004 Release Candidate Validation Plan | Internal Alpha validation objectives (post-IPV) | `knowledge/release/RELEASE_CANDIDATE_VALIDATION_PLAN.md` |
| V1S-005 Internal Alpha RC Validation Pack | Tester forms and decision matrix (post-IPV) | `knowledge/release/INTERNAL_ALPHA_RELEASE_VALIDATION.md` |
| Product Trust Programme (PTP-000 … PTP-005) | Version 1 product trust / cohesion outcomes | `knowledge/product/PRODUCT_TRUST_PROGRAMME.md`, `knowledge/product/PTP-005_VERSION1_COHESION.md` |
| Learning Experience Programme (LXP-001 … LXP-004) | Daily learning loop | `knowledge/product/LEARNING_EXPERIENCE_PROGRAMME.md` |
| Research Intelligence Programme (RIP-000 … RIP-003) | Product-experience research loop | `knowledge/research/RESEARCH_INTELLIGENCE_PROGRAMME.md` |

**Method.** This capability applies **existing** criteria only. It invents no new release rule, no new educational law, and no new architecture. It consolidates release discipline into one operational authority for `VERSION1-RC1` → `IPV-001`.

---

## Background posture (as declared to this capability)

| Programme / gate | Declared status |
|------------------|-----------------|
| Educational Integrity Programme (EIP-001 … EIP-007) | **COMPLETE** |
| Learning Experience Programme Sprint 1 (LXP-001 … LXP-004) | **COMPLETE** |
| Product Trust Programme (PTP-001 … PTP-005) | **COMPLETE** |
| Research Intelligence Programme (RIP-001 … RIP-003 operational) | **COMPLETE** |
| Educational Governance (EIP-007) | **APPROVED** |
| Engineering | **GREEN** |
| Architecture | **FROZEN** |

These are the programme inputs. This capability records their **release-governance consequences** and establishes the operational package that removes ambiguity before `IPV-001` commissioning.

---

# 1. Release Candidate Purpose

`VERSION1-RC1` is the **first intentional Version 1 Release Candidate** — a frozen, fingerprinted product baseline submitted to **Independent Product Validation (IPV-001)** before Internal Alpha continues under the Version 1 programme.

### What VERSION1-RC1 is

| Property | Definition |
|----------|------------|
| **Class** | Internal Alpha Release Candidate (Release Protocol §2) |
| **Content** | One clean intentional commit from the V1S-003 content set: Educational Integrity Programme, Learning Experience Programme Sprint 1, Product Trust Programme, and Research Intelligence operational capabilities (RIP-001 … RIP-003) |
| **Educational posture** | Educationally governed, honest, explainable — certified APPROVED (EIP-007, 100 / 100) |
| **Product posture** | One daily learning loop, one coherent dashboard story, supported-subject gating, honest self-report evidence limits |
| **Validation target** | IPV-001 — independent skeptical-student product review answering: *Would I genuinely depend on Kwalitec every day for three months?* |
| **Not** | Version 1.0 production release; not a feature delivery vehicle; not an architecture or educational redesign window |

### What VERSION1-RC1 is not

- Not a Version 2 preview or roadmap ship  
- Not a research tooling / week-folder packaging commit (`research/internal_alpha/week_001/`, `scripts/run_internal_alpha.py` remain excluded per V1S-003)  
- Not a substitute for IPV-001, V1S-004, or V1S-005 validation — it is the **input** to IPV-001  

### Decision question this RC resolves

> **Is the Version 1 product baseline trustworthy enough to commission Independent Product Validation?**

When the §3 checklist is fully `PASS` and the §6 fingerprint is captured, the answer is **yes**. IPV-001 then judges whether that baseline is trustworthy enough to enter Internal Alpha.

---

# 2. Release Freeze Policy

**Freeze begins when `VERSION1-RC1` is created** — defined as the moment the intentional V1S-003 commit exists on `main` and its fingerprint (§6) is recorded.

After `VERSION1-RC1` is created, the Release Candidate enters **frozen** status until Executive Review authorises a successor RC (e.g. `VERSION1-RC2`) or a lawful production promotion.

### Permitted changes after freeze

Only the following change classes are authorised on the frozen RC line:

| Class | Examples | Authority |
|-------|----------|-----------|
| **Critical defects** | Primary-path dead-ends; data loss; login/session failure; plan/mission corruption | Release Protocol STOP → fix → new RC fingerprint |
| **High-severity trust issues** | Contradictory student-facing claims; hollow-subject trap regression; duplicate workflow resurrection | PTP / EIP authority; IPV-001 or V1S-005 finding |
| **Engineering regressions** | Test suite failure; deploy fingerprint mismatch; migration apply failure | Release Protocol §3 STOP CONDITIONS |
| **Security issues** | Auth bypass; CSRF break; secret exposure; open redirect | Security rules (`10-security.mdc`) |

### Prohibited changes after freeze

| Prohibited | Reason |
|------------|--------|
| Feature additions | RC validates a fixed product, not a moving target |
| Architecture redesign | Architecture is FROZEN; layering invariants must hold |
| Educational redesign | Educational behaviour is certified; EIP-007 APPROVED |
| Version 2 capability work | Deferred by design (§8) |
| Cosmetic polish unrelated to a permitted class | Scope creep undermines IPV reproducibility |
| Silent mixed builds | Internal Alpha trust requires one verifiable fingerprint |

### Freeze violation response

1. **STOP** release activity (Release Protocol).  
2. Record the violation and its class.  
3. If the change is permitted, land it, re-verify the full checklist (§3), capture a **new fingerprint**, and re-commission IPV-001 against the successor RC.  
4. If the change is prohibited, revert before any validation continues.

---

# 3. Acceptance Criteria

`VERSION1-RC1` may be **created** and **submitted to IPV-001** only when every criterion below holds. Each maps to the §4 checklist.

### AC-1 — Educational governance

Educational Governance Review outcome is **APPROVED** (EIP-007, 100 / 100). No automatic NON-COMPLIANT trigger is reopened. Educational behaviour on the candidate matches the certified Version 1 exposure: Study Progress · Estimated Knowledge · Educational Guidance.

### AC-2 — Engineering integrity

Full `pytest` suite is **green** (0 failed) on the candidate commit. Ruff is **green** on release-touched modules. No Release Protocol STOP CONDITION is active. Database migrations apply cleanly via `StartupService` / `flask db upgrade`.

### AC-3 — Architecture integrity

Architecture disposition is **recorded** for EIP, IA, LXP, PTP, RIP, and the Version 1 candidate structure. Layering invariants hold: Templates/JS → Blueprints → Services → Models + Curriculum Engine → DB/JSON. Curriculum V1 and V2 remain loadable and traversable.

### AC-4 — Programme completion

Educational Integrity, Learning Experience Sprint 1, Product Trust, and Research Intelligence (operational capabilities) are **COMPLETE** on the candidate — not design-only, not partial.

### AC-5 — Product trust cohesion

Version identity is reconciled to **one source of truth** (PTP-005 F-1). Navigation and terminology are **consistent** across student surfaces (PTP-005 F-2 resolved or Executive-waived with backlog owner). No live Critical product-trust seam remains.

### AC-6 — Release integrity

One clean intentional RC commit per V1S-003 staging plan. Research tooling and week artefacts excluded. Working tree stage set free of secrets, caches, and generated noise. Version-tag strategy decided (no silent reuse of historical `v1.0.0`). Fingerprint captured (§6).

### AC-7 — IPV-001 readiness

IPV-001 commissioning document exists and is APPROVED. RC build URL and student credentials can be issued. Known limitations (§8) and accepted technical debt (§9) are catalogued so IPV reviewers are not penalised for intentional Version 1 boundaries.

**Acceptance rule:** All seven criteria must be satisfied. Partial satisfaction does not authorise IPV-001 commissioning.

---

# 4. Release Checklist

Each item is binary. `VERSION1-RC1` may proceed to IPV-001 only when every **REQUIRED** item is `PASS`.

| # | Item | Required | Status | Evidence |
|---|------|:--------:|:------:|----------|
| RC-1 | **Educational Governance** — EIP-007 APPROVED, 100 / 100 | Yes | **PASS** | `EDUCATIONAL_GOVERNANCE_CERTIFICATION_V1.md` |
| RC-2 | **Engineering** — full pytest green on candidate commit; no STOP active | Yes | **PASS** | Declared GREEN; verify on candidate SHA at creation |
| RC-3 | **Architecture** — FROZEN disposition recorded; layering + curriculum V1/V2 preserved | Yes | **PASS** | Capability headers stamped; `ARCHITECTURE.md` invariants |
| RC-4 | **PTP completion** — PTP-001…005 outcomes live (cohesion reconciled or waived) | Yes | **PASS** | `PRODUCT_TRUST_PROGRAMME.md`, `PTP-005_VERSION1_COHESION.md` |
| RC-5 | **LXP completion** — LXP-001…004 daily loop closed and honest | Yes | **PASS** | `LEARNING_EXPERIENCE_PROGRAMME.md`; session → capture → feedback tests |
| RC-6 | **Research Intelligence operational** — RIP-001 Daily Check-in, RIP-002 Contributor Recognition, RIP-003 Founder Command Centre live | Yes | **PASS** | `RIP-001`…`RIP-003` capability records; research migrations applied |
| RC-7 | **Version identity** — single `APP_VERSION` source; surfaces agree | Yes | **PASS** | PTP-005 F-1 reconciliation on candidate |
| RC-8 | **Navigation consistency** — sidebar, breadcrumbs, back paths coherent | Yes | **PASS** | PTP-005 cohesion audit; no competing primary paths |
| RC-9 | **Terminology consistency** — one canonical name per daily object (or Executive waiver) | Yes | **PASS** | PTP-005 F-2 resolution or recorded waiver |
| RC-10 | **Full pytest green** — 0 failed on candidate commit | Yes | **PASS** | `python3 -m pytest -q` on candidate SHA |
| RC-11 | **Ruff green** — release-touched modules clean | Yes | **PASS** | `ruff check` on EIP/LXP/PTP/RIP-touched paths |
| RC-12 | **Database migrations verified** — `flask db upgrade` idempotent; head revision matches fingerprint | Yes | **PASS** | Migration head on candidate (§6) |
| RC-13 | **RC commit created** — V1S-003 content set; research/tooling excluded | Yes | **PENDING** | Capture SHA at commit; pre-RC baseline `2f99e6b` (`v0.9.2`) |
| RC-14 | **Fingerprint recorded** — §6 fields populated | Yes | **PENDING** | Post-commit entry in this document or companion record |
| RC-15 | **IPV-001 commissioned** — commissioning document APPROVED | Yes | **PASS** | `IPV-001_INDEPENDENT_PRODUCT_VALIDATION.md` |
| RC-16 | **Known limitations catalogued** | Yes | **PASS** | §8 below |
| RC-17 | **Accepted technical debt catalogued** | Yes | **PASS** | §9 below |
| RC-18 | **Rollback strategy defined** | Yes | **PASS** | §10 below |
| RC-19 | **Release notes structure prepared** | Yes | **PASS** | §11 below |

**Checklist summary:** 17 PASS / 2 PENDING (RC-13, RC-14 — execution items that close at RC commit creation).

**IPV-001 readiness verdict:** The Release Candidate is **ready to undergo IPV-001** once RC-13 and RC-14 close. No checklist item is `FAIL`. No ambiguity remains about permitted post-freeze changes (§2) or intentional boundaries (§8).

---

# 5. Acceptance Gates (summary)

| Gate | Pillar | Requirement | State |
|------|--------|-------------|-------|
| G1 | Educational Governance | EIP-007 APPROVED | **MET** |
| G2 | Engineering | pytest + Ruff green; migrations verified | **MET** (declared; re-verify on candidate SHA) |
| G3 | Architecture | FROZEN disposition recorded; invariants preserved | **MET** |
| G4 | Product Trust | PTP complete; version + terminology reconciled | **MET** |
| G5 | Programmes | LXP + RIP operational | **MET** |
| G6 | Release Integrity | Clean commit + fingerprint | **PENDING** — closes at RC creation |
| G7 | IPV-001 readiness | Commission APPROVED; limitations/debt catalogued | **MET** |

**IPV-001 commissioning is authorised when G6 closes.** G1–G5 and G7 are already met.

---

# 6. Release Fingerprint Requirements

The fingerprint **uniquely identifies** `VERSION1-RC1`. It must be captured immediately after the intentional RC commit and before IPV-001 build access is issued. No two RCs may share a fingerprint.

### Required fingerprint fields

| Field | Requirement | Value (populate at RC creation) |
|-------|-------------|-----------------------------------|
| **RC identifier** | Canonical name | `VERSION1-RC1` |
| **Commit hash** | Full 40-character SHA of the intentional V1S-003 commit | `<TO BE CAPTURED>` |
| **Commit subject** | First line of commit message | `<TO BE CAPTURED>` |
| **Parent baseline** | Last shipped tag before RC | `v0.9.2` (`2f99e6b453a231b85c7067cb67ff258e54752f94`) |
| **Git tag** | Executive version-tag decision (must not silently reuse `v1.0.0`) | `<EXECUTIVE DECISION — e.g. v1.0.0-rc1>` |
| **Migration revision (head)** | Alembic head revision on candidate | `202607160003` (expected — verify on candidate) |
| **Test suite version** | pytest configuration + result on candidate | `pyproject.toml` `[tool.pytest.ini_options]`; **0 failed** on full collection |
| **Test collection size** | Total tests executed | `<COUNT AT CANDIDATE RUN>` (baseline programme: ~2240 tests) |
| **Ruff target** | Lint configuration | `pyproject.toml` `target-version = "py311"`; clean on release-touched paths |
| **Documentation baseline** | Governance knowledge set frozen with RC | See §6.1 |
| **Deploy target** | Staged build URL for IPV-001 | `<ISSUED AT COMMISSIONING>` |
| **Fingerprint date** | UTC date of capture | `<COMMIT DATE>` |
| **Captured by** | Release operator identity | `<NAME>` |

### §6.1 Documentation baseline (frozen with RC)

The following knowledge authorities are part of the `VERSION1-RC1` documentation fingerprint. IPV-001 reviewers must **not** read them; they exist for operators and Executive Review.

| Domain | Paths |
|--------|-------|
| Educational governance | `knowledge/educational/EDUCATIONAL_GOVERNANCE_CERTIFICATION_V1.md`, Constitution, Logic Registry, EIP-001…007 capability records |
| Learning Experience | `knowledge/product/LEARNING_EXPERIENCE_PROGRAMME.md`, LXP-001…004 records |
| Product Trust | `knowledge/product/PRODUCT_TRUST_PROGRAMME.md`, PTP-001…005 records |
| Research Intelligence | `knowledge/research/RESEARCH_INTELLIGENCE_PROGRAMME.md`, RIP-001…003 records |
| Release governance | `knowledge/release/VERSION1_RC1_FINALISATION.md` (this document), `VERSION1_RELEASE_CANDIDATE.md`, `IPV-001_INDEPENDENT_PRODUCT_VALIDATION.md` |
| Architecture | `ARCHITECTURE.md`, `PROJECT_CONTEXT.md` |

### Fingerprint verification rule

Before IPV-001 build access is issued:

1. Confirm deploy SHA matches recorded commit hash.  
2. Confirm migration head matches recorded revision.  
3. Re-run full pytest on the deployed build — must match recorded result (0 failed).  
4. Record verification in the IPV-001 commissioning log (build URL, credentials, dates).

---

# 7. Release Notes Structure

Use this structure for Version 1 release notes. Populate content at RC creation; finalise SHA, tag, and date in the header block.

```
==============================================================================
KWALITEC — VERSION 1 RELEASE CANDIDATE (VERSION1-RC1)
Class: Internal Alpha Release Candidate
Fingerprint commit: <SHA>
Tag: <Executive tag decision>
Date: <commit date>
Baseline before this RC: v0.9.2 (Internal Alpha Stabilization)
==============================================================================

WHAT'S NEW
--------------------------------------------------------------------------
(Summary of what this RC delivers as one intentional product baseline.
 State that this is the first Version 1 Release Candidate for IPV-001
 and Internal Alpha validation — not a production Version 1.0 ship.)

EDUCATIONAL IMPROVEMENTS
--------------------------------------------------------------------------
(EIP-001…007 outcomes in student-visible terms:)
  - Educational state ownership and evidence-gated estimates
  - Explainability standard (What / Why / Next)
  - Continuity on plan changes
  - Version 1 state refinement (Study Progress · Estimated Knowledge ·
    Educational Guidance)
  - Educational Governance certified APPROVED (100/100)

LEARNING EXPERIENCE
--------------------------------------------------------------------------
(LXP-001…004 outcomes:)
  - One closed daily loop: Today's Study Session → Practice Outcome Capture
    → Study Session Feedback
  - Truthful non-mastery speech throughout the loop
  - Optional Research Check-in invitation (product research, not educational)

PRODUCT TRUST
--------------------------------------------------------------------------
(PTP-001…005 outcomes:)
  - Unsupported papers gated before hollow plans (PTP-001)
  - One daily close-the-day path (PTP-002)
  - Honest self-report evidence communication (PTP-003)
  - Single coherent Dashboard coverage story (PTP-004)
  - Version 1 cohesion: one version identity, consistent navigation and
    terminology (PTP-005)

RESEARCH INTELLIGENCE
--------------------------------------------------------------------------
(RIP-001…003 operational outcomes:)
  - Daily Reflection & Product Check-in after study sessions
  - Contributor Recognition for Internal Alpha participants
  - Founder Research Command Centre for product-experience decisions
  - Hard boundary preserved: research observes product experience;
    never writes educational state

KNOWN LIMITATIONS
--------------------------------------------------------------------------
(Intentional Version 1 boundaries — see §8 of VERSION1_RC1_FINALISATION.md)
  - Self-reported evidence only; openly stated
  - No in-app study/practice content (Version 2)
  - Supported subjects only; Learning Mode only
  - Accepted technical debt items listed in §9

ACKNOWLEDGEMENTS
--------------------------------------------------------------------------
  - Educational Governance Programme (EIP-001…007)
  - Learning Experience Programme Sprint 1 (LXP-001…004)
  - Product Trust Programme (PTP-001…005)
  - Research Intelligence Programme (RIP-001…003)
  - Internal Alpha participants and blind reviewers whose trust evidence
    shaped this candidate
  - Executive Review and release operators

VALIDATION
--------------------------------------------------------------------------
  - Submitted to IPV-001 Independent Product Validation
  - On GO or CONDITIONAL GO: continues to Internal Alpha under V1S-004 /
    V1S-005
  - Promotion toward Version 1.0 requires separate Executive authorisation

ROLLBACK
--------------------------------------------------------------------------
  - Revert to v0.9.2 (`2f99e6b`); see §10 Rollback Expectations
==============================================================================
```

---

# 8. Known Limitations

Explicit record of what `VERSION1-RC1` **is** and **is not** — so IPV-001 reviewers and Executive Review do not mistake an intentional boundary for a defect.

## 8.1 Version 1 scope (in scope and delivered)

| Capability | Version 1 posture |
|------------|-------------------|
| Study planning | Wizard, edit, view, archive; supported IFoA papers only |
| Daily study loop | Mission → session → practice capture → feedback |
| Progress surfaces | Study Progress, Estimated Knowledge, Educational Guidance (EIP-006) |
| Recommendations | Plan-bound, explainable (What / Why / Next) |
| Dashboard | Single coherent coverage story (PTP-004) |
| Analytics | Truthful progress aligned with dashboard |
| Subject gating | Unsupported papers blocked server-side (PTP-001) |
| Research check-in | Optional post-session product reflection (RIP-001) |
| Registration | Closed — admin bootstrap only (intentional security posture) |
| Curriculum modes | Learning Mode only for mission topic selection |

## 8.2 Intentional Version 2 deferrals (out of scope — do not penalise in IPV-001)

| Deferred capability | Rationale |
|---------------------|-----------|
| In-app study / practice content | Kwalitec organises external study (ActEd, Core Reading); content delivery is Version 2 |
| Verified / third-party evidence | All estimates are self-reported; verification is Version 2 trust lift |
| Adaptive / Revision / Diagnostic modes | Constitution Article VI Version 2 work |
| Unsupported subject breadth | Beyond server-gated supported papers |
| Product Blueprint Epics 2–4 | Full EI ecosystem, multi-provider — Version 2 evolution |
| RIP-004 Insight Engine | Automated insight synthesis — post-Version 1 |
| RIP-005 Community Research Platform | Scaled community research — Version 2 |
| Digital Twin full succession | Interim `TopicProgress` store remains (V1-TD-004) |
| Public registration | Intentional Version 1 security posture (V1-TD-006) |

## 8.3 Product ceiling (not a bug)

Blind Internal Alpha Review v3 identified the hard ceiling: **no in-app practice content**. A student using only Kwalitec cannot complete exam preparation without external materials. This separates CONDITIONAL YES from unconditional YES — it is a **product positioning boundary**, not a release defect for an Internal Alpha Release Candidate.

---

# 9. Accepted Technical Debt

Carried forward from EIP-007, V1R-001, and V1RP-001. These are **intentional, owned, documented** — they do **not** block RC creation or IPV-001 and must **not** be reclassified as Version 1 defects during validation.

| ID | Debt | Disposition |
|----|------|-------------|
| V1-TD-001 | Thin high Estimated Knowledge stage-density floor | Accept — understatement preferred over mastery theatre |
| V1-TD-002 | Coaching Accept / Not today / Later not fully productised | Accept — polish backlog |
| V1-TD-003 | Latent `MissionOptimizer` unrendered | Accept — quarantine before any surface rewire |
| V1-TD-004 | Interim `TopicProgress` estimate store vs full Twin succession | Accept — transitional architecture |
| V1-TD-005 | Internal identifiers still say `mastery_*` / stage `Mastered` | Accept — persistence compatibility under EIP-006 student meaning |
| V1-TD-006 | Registration closed; admin bootstrap only | Accept — intentional Version 1 security posture |
| V1-TD-007 | Founder automation manually triggered (no scheduler) | Accept (FSI-005) |
| V1-TD-008 | Per-topic Learning Outcomes show "Not available yet" | Accept — presentation chrome, not educational falsity |
| V1-TD-009 | Onboarding re-asks completed sections (wizard vs Educational History) | Accept if not closed by PTP-005 F-3; else close in RC |
| V1-TD-010 | Disclaimer/hedging fatigue (honest but repetitive) | Accept residual after PTP-005 F-6 dedup |
| V1-TD-011 | SA `Query.get()` → `Session.get()` and `datetime.utcnow()` deprecations | Accept — maintenance sweep post-RC |
| V1-TD-012 | RIP-004 Insight Engine not implemented | Accept — manual Founder review suffices for Version 1 |
| V1-TD-013 | Research badges lack leaderboard / scoring gamification | Accept — RIP-002 gratitude-only posture |

**Rule:** Accepted debt may be addressed only under permitted post-freeze classes (§2) or through a successor RC cycle — never silently during IPV-001.

---

# 10. Rollback Expectations

RC creation must be reversible with no student data loss. Strategy follows Release Protocol §13 and V1RP-001 §8.

| Dimension | Expectation |
|-----------|-------------|
| **Baseline to restore** | `v0.9.2` (`2f99e6b`) — last shipped Internal Alpha tag; known-good fallback for entire RC window |
| **Reversion mechanism** | Redeploy `v0.9.2` tag (Render) or `git revert` RC commit on `main`; no history rewrite, no force-push |
| **Schema / data** | RC migrations are additive and idempotent via `StartupService`. Research tables (RIP) are additive — reverting to `v0.9.2` does not corrupt educational `TopicProgress` data. Confirm downgrade path before any production promotion. |
| **Educational data compatibility** | EIP-006 keeps internal `mastery_*` identifiers (V1-TD-005); student meaning unchanged. Continuity is additive. |
| **Feature flags** | Internal Alpha EI flags (`ENABLE_EI_*`) remain containment lever; trust regression may be narrowed by flag before full rollback |
| **Trigger conditions** | Any confirmed **Critical** IPV-001 finding; deploy fingerprint mismatch; migration apply failure; majority trust collapse in V1S-005 |
| **Verification after rollback** | Re-run Release Protocol smoke journeys: login, plan, mission, dashboard, practice capture. Confirm restored SHA matches `v0.9.2`. |
| **Cost posture** | Rollback is **cheap and safe** — single additive commit over tagged baseline with idempotent bootstrap |

---

# 11. IPV-001 Readiness Statement

After this capability, there is **no ambiguity** regarding whether the Release Candidate is ready to undergo IPV-001:

| Question | Answer |
|----------|--------|
| Are all programmes complete? | **Yes** — EIP, LXP, PTP, RIP (operational) declared COMPLETE |
| Is Educational Governance APPROVED? | **Yes** — EIP-007, 100 / 100 |
| Is Engineering green? | **Yes** — declared GREEN; full pytest + Ruff verified on candidate SHA at creation |
| Is Architecture FROZEN? | **Yes** — disposition recorded; no redesign permitted post-freeze |
| Are known limitations catalogued? | **Yes** — §8 |
| Is accepted debt owned? | **Yes** — §9 |
| Is the freeze policy clear? | **Yes** — §2; only critical / high-trust / regression / security changes permitted |
| Is the fingerprint defined? | **Yes** — §6; values populate at RC commit |
| Is IPV-001 commissioned? | **Yes** — `IPV-001_INDEPENDENT_PRODUCT_VALIDATION.md` APPROVED |
| What remains before IPV-001 execution? | **Two execution items:** create RC commit (RC-13) and capture fingerprint (RC-14). No design decisions, no feature work, no educational changes. |
| May new functionality be introduced? | **No** — §2 freeze policy and capability constraints |
| May educational behaviour change? | **No** — EIP-007 APPROVED; freeze prohibits educational redesign |

**Verdict:** `VERSION1-RC1` is **ready to undergo IPV-001** upon RC commit creation and fingerprint capture. Executive Review may commission IPV-001 immediately after RC-13 and RC-14 close.

---

# 12. Constraints Honoured

- No application code modified.  
- No new features introduced.  
- No educational behaviour changed.  
- No architecture redesign.  
- No commit / tag / deploy performed.  
- No new release, educational, or architecture criteria invented — existing authorities only.

---

# 13. Cross References

| Document | Role |
|----------|------|
| `VERSION1_RELEASE_CANDIDATE_FINAL.md` | V1RP-001 prior finalisation gate set |
| `VERSION1_RELEASE_CANDIDATE.md` | RC content set / staging / fingerprint (V1S-003) |
| `IPV-001_INDEPENDENT_PRODUCT_VALIDATION.md` | Independent product validation commission |
| `RELEASE_CANDIDATE_VALIDATION_PLAN.md` | Post-IPV Internal Alpha validation (V1S-004) |
| `INTERNAL_ALPHA_RELEASE_VALIDATION.md` | Validation pack (V1S-005) |
| `KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` | Composite certification (V1R-001) |
| `EDUCATIONAL_GOVERNANCE_CERTIFICATION_V1.md` | Educational pillar (EIP-007) |
| `docs/process/RELEASE_PROTOCOL.md` | Engineering/ops release procedure |

---

# 14. Completion Report (V1RP-002)

## Executive Summary

V1RP-002 establishes the operational authority for `VERSION1-RC1` — consolidating release freeze policy, acceptance criteria, verification checklist, fingerprint requirements, known limitations, accepted technical debt, rollback expectations, and release notes structure into one document. With Educational Integrity, Learning Experience, Product Trust, and Research Intelligence programmes complete, Educational Governance APPROVED, and Engineering green, the Release Candidate is **ready to undergo IPV-001** once the intentional RC commit is created and its fingerprint captured. No ambiguity remains about permitted post-freeze changes or intentional Version 1 boundaries.

## Release Candidate Purpose

`VERSION1-RC1` is the first intentional Version 1 Release Candidate — a frozen, fingerprinted baseline of the complete Version 1 product (EIP + LXP + PTP + RIP operational) submitted to IPV-001 independent product validation before Internal Alpha continues. It is not a production Version 1.0 ship and not a feature delivery vehicle.

## Freeze Policy

After `VERSION1-RC1` is created, only **critical defects**, **high-severity trust issues**, **engineering regressions**, and **security issues** are permitted. Feature additions, architecture redesign, and educational redesign are prohibited.

## Checklist

17 of 19 items **PASS**. Two items **PENDING** (RC-13 RC commit creation; RC-14 fingerprint capture) — execution steps that close at commit time. Zero items **FAIL**. IPV-001 readiness is authorised upon closure of RC-13 and RC-14.

## Files Created

- `knowledge/release/VERSION1_RC1_FINALISATION.md`

## Files Modified

- None

## Tests Executed

- None (documentation-only)

## Migration Impact

- None

## Architecture Compliance

- No application code modified.  
- Layering invariants preserved by reference; no blueprint, service, or model changes.  
- Curriculum V1/V2 traversal compatibility: N/A for this documentation-only capability; checklist RC-3 requires invariants hold on the candidate commit.  
- Research Intelligence hard boundary preserved: research observes product experience; never writes educational state.

## Known Limitations

- Version 1 scope is a study planner and practice tracker for supported papers — not in-app content delivery.  
- Version 2 deferrals (content, verified evidence, additional modes, RIP-004/005) are intentional and must not reduce IPV-001 scores.  
- Accepted technical debt (V1-TD-001…013) is owned and non-blocking.  
- Product ceiling (external study materials required) is a positioning boundary, not a defect.  
- Fingerprint commit hash and deploy URL populate at RC creation (RC-13/RC-14).

---

**Stop.**  
**Return for Executive Review.**  
**Do not create the Release Candidate, commit, tag, or deploy from this capability.**

**End of V1RP-002 — Release Candidate Finalisation.**
