# Version 1 Release Candidate — VERSION1-RC1

**Capability ID:** V1RP-004  
**Programme:** Version 1 Release Programme  
**Title:** Promote Build to VERSION1-RC1  
**Priority:** RELEASE CRITICAL  
**Status:** PROMOTED — frozen Release Candidate authorised for IPV-001  
**Nature:** Release operations only — records, fingerprints, commit, and tag; no application behaviour change under this capability  
**Classification:** Release-governance authority — subordinate to the Educational Constitution, Educational Governance Review Standard (EGI-003 §7), Release Protocol, and `VERSION1_RC1_FINALISATION.md` (V1RP-002).

---

## Authority

| Authority | Role | Path |
|-----------|------|------|
| FC-001 Founder Certification (final re-run) | Authorises promotion — **RELEASE TO IPV** | Agent certification record 2026-07-16 |
| V1RP-002 Release Candidate Finalisation | Freeze policy, checklist, fingerprint requirements | `VERSION1_RC1_FINALISATION.md` |
| V1S-003 Release Candidate Preparation | RC content set and staging plan | `VERSION1_RELEASE_CANDIDATE.md` |
| IPV-001 Independent Product Validation | Validation commission for this RC | `IPV-001_INDEPENDENT_PRODUCT_VALIDATION.md` |
| EIP-007 Educational Governance Certification | Educational pillar — **APPROVED / 100–100** | `EDUCATIONAL_GOVERNANCE_CERTIFICATION_V1.md` |
| Release Protocol v2.0 | Engineering STOP conditions and deploy procedure | `docs/process/RELEASE_PROTOCOL.md` |

**Method.** This capability promotes the exact build that passed FC-001 after RR-001. It does not modify application behaviour, educational logic, templates, services, curriculum, or migrations. It records and certifies the product as approved.

---

# 1. Executive Summary

`VERSION1-RC1` is the **official Version 1 Release Candidate** — a frozen, fingerprinted product baseline of the complete Version 1 programme stack submitted to **Independent Product Validation (IPV-001)**.

| Gate | Result |
|------|--------|
| Educational Integrity Programme | **COMPLETE** |
| Learning Experience Programme | **COMPLETE** |
| Product Trust Programme | **COMPLETE** |
| Research Intelligence Programme | **COMPLETE** (operational RIP-001…003; RIP-004 deferred) |
| Quality Sprint | **COMPLETE** |
| Release Stabilisation | **COMPLETE** |
| Student Trust Sprint (RR-001) | **COMPLETE** |
| Founder Certification (FC-001 final re-run) | **PASSED — RELEASE TO IPV** |

**Pre-RC baseline:** `v0.9.2` (`2f99e6b453a231b85c7067cb67ff258e54752f94`).  
**Release status:** **FROZEN** — authorised for IPV-001.

---

# 2. Working Tree Verification (V1RP-004 Step 1)

| Check | Result |
|-------|--------|
| RR-001 changes present | **PASS** — RR-001A…D tests and trust fixes present; CS1/CM1/CB2 only at `2026.json` |
| Placeholder curriculum fixtures | **ABSENT** — no `cs1/2027`, `cs1/2028`, or `cs9/2099`; no "Topic A1"/"Topic B1" titles in production syllabus |
| Temporary logs / caches | **ABSENT** from stage set (`importtime.log` / `server.log` removed before promotion) |
| Research tooling excluded | **PASS** — `research/internal_alpha/week_001/` and `scripts/` left unstaged |
| Unexpected files (unstaged) | Root Blind Internal Alpha Review drafts: `BLIND_INTERNAL_ALPHA_REVIEW.md`, `BLIND_INTERNAL_ALPHA_REVIEW_V2.md`, `BLIND_INTERNAL_ALPHA_REVIEW_V3.md` — review artefacts, not product RC |

---

# 3. Engineering State (V1RP-004 Step 2)

Recorded at promotion from existing validated evidence (no re-implementation).

| Field | Value |
|-------|-------|
| **Branch** | `main` |
| **Pre-promotion HEAD** | `2f99e6b453a231b85c7067cb67ff258e54752f94` (`v0.9.2`) |
| **Migration head** | `202607160003` (verified `flask db heads`) |
| **Application version** | `1.0.0` — `app/version.py` (`APP_VERSION`) aligned with `pyproject.toml` |
| **Programme regression** | **GREEN** (RR-001 evidence) — EIP/LXP/PTP/RIP/QS/IA/RR targeted suites passed (213 + 59 + 33 + 205 passed across validation batches); `ruff check` on changed files passed |
| **Founder Certification** | **PASSED** — FC-001 final re-run decision **RELEASE TO IPV** (2026-07-16) |

---

# 4. Release Snapshot

| Programme | Scope | Status | Evidence |
|-----------|-------|--------|----------|
| **Educational Integrity Programme** | EIP-001 … EIP-007 | **COMPLETE** | `knowledge/educational/`; `tests/test_eip00*.py` |
| **Learning Experience Programme** | LXP-001 … LXP-004 | **COMPLETE** | LXP records; session → practice → feedback; `tests/test_lxp00*.py` |
| **Product Trust Programme** | PTP-001 … PTP-005 | **COMPLETE** | PTP records; `tests/test_ptp00*.py` |
| **Research Intelligence Programme** | RIP-001 … RIP-003 operational | **COMPLETE** | Migrations `202607160001`–`202607160003`; `tests/test_rip001*.py` … `test_rip003*.py` |
| **Quality Sprint** | QS-001 | **COMPLETE** | `tests/test_qs001_ptp005_cohesion.py` |
| **Student Trust Sprint** | RR-001A … RR-001D | **COMPLETE** | Authentic syllabus, onboarding note, Study Session terminology, post-session check-in; `tests/test_rr001*.py` |
| **Educational Governance** | EIP-007 | **APPROVED** | 100 / 100 |
| **Architecture** | Layering + curriculum V1/V2 | **FROZEN** | `ARCHITECTURE.md` |
| **Founder Certification** | FC-001 | **PASSED** | RELEASE TO IPV |

### Trust evidence (context)

| Evidence | Result |
|----------|--------|
| Blind Internal Alpha Review v3 | **64 / 100, CONDITIONAL YES** — referenced; root draft files left unstaged |
| Product ceiling | No in-app study content; self-reported evidence only — intentional Version 1 boundary |

---

# 5. Fingerprint

| Field | Value |
|-------|-------|
| **Release Candidate Name** | `VERSION1-RC1` |
| **Creation timestamp** | `2026-07-16T11:06:43Z` |
| **Branch** | `main` |
| **Commit SHA** | `40c4fe698d94ab206be851ee304829b05076e7d4` |
| **Commit timestamp** | `2026-07-16 13:10:57 +0200` |
| **Annotated Git Tag** | `VERSION1-RC1` |
| **Parent Baseline** | `v0.9.2` (`2f99e6b453a231b85c7067cb67ff258e54752f94`) |
| **Migration Head** | `202607160003` |
| **Application Version** | `1.0.0` |
| **Programme regression** | **GREEN** — RR-001 / programme validation batches passed (existing evidence) |
| **Founder Certification** | **PASSED — RELEASE TO IPV** (FC-001 final re-run, 2026-07-16) |
| **Release status** | **FROZEN** |
| **Authorised for IPV-001** | **YES** |
| **Builder** | Release Programme operator (V1RP-004) |
| **Fingerprint Date** | 2026-07-16 |

### §5.1 Documentation baseline (frozen with RC)

| Domain | Paths |
|--------|-------|
| Educational governance | `knowledge/educational/` |
| Learning Experience | `knowledge/product/LEARNING_EXPERIENCE_PROGRAMME.md`, LXP-002…004 |
| Product Trust | `knowledge/product/PRODUCT_TRUST_PROGRAMME.md`, PTP-001…005 |
| Research Intelligence | `knowledge/research/` |
| Release governance | `knowledge/release/` including this document |
| Architecture | `ARCHITECTURE.md`, `PROJECT_CONTEXT.md` |

---

# 6. Freeze Declaration

**VERSION1-RC1 is now frozen.**

Only the following changes are permitted after this point:

- Critical defects
- Security fixes
- Engineering regressions
- IPV-confirmed release blockers

All other work is deferred to Version 2.

| Prohibited | Reason |
|------------|--------|
| Feature additions | RC validates a fixed product |
| Educational redesign | Educational behaviour certified APPROVED (EIP-007) |
| Architecture redesign | Architecture FROZEN |
| Database redesign | Schema locked to migration head `202607160003` unless critical |
| Product redesign | Product trust posture validated for IPV-001 |

**Freeze violation response:** STOP release activity (Release Protocol). If permitted, land fix, re-verify, capture **new fingerprint**, re-commission IPV-001 against a successor RC.

---

# 7. Ready for IPV-001

| Question | Answer |
|----------|--------|
| Are all Version 1 programmes complete? | **Yes** |
| Is Educational Governance APPROVED? | **Yes** — EIP-007, 100 / 100 |
| Did Founder Certification pass? | **Yes** — RELEASE TO IPV |
| Is the RC fingerprint recorded? | **Yes** — §5 (SHA completed post-commit) |
| Is IPV-001 commissioned? | **Yes** — `IPV-001_INDEPENDENT_PRODUCT_VALIDATION.md` APPROVED |
| Is the freeze policy clear? | **Yes** — §6 |

**Verdict:** `VERSION1-RC1` is **PROMOTED** and **READY FOR IPV-001**.

---

# 8. Checklist

| # | Item | Status | Evidence |
|---|------|:------:|----------|
| C-1 | RC commit created | **PASS** | `release: VERSION1-RC1` on `main` |
| C-2 | Annotated tag `VERSION1-RC1` created | **PASS** | Git annotated tag |
| C-3 | Fingerprint captured | **PASS** | §5 |
| C-4 | Migration head `202607160003` | **PASS** | `flask db heads` |
| C-5 | Application version `1.0.0` | **PASS** | `app/version.py` / `pyproject.toml` |
| C-6 | Programme regression GREEN | **PASS** | RR-001 validated evidence |
| C-7 | Founder Certification PASSED | **PASS** | FC-001 RELEASE TO IPV |
| C-8 | Freeze complete | **PASS** | §6 |
| C-9 | Authorised for IPV-001 | **PASS** | This document |

---

# 9. Known Limitations

Intentional Version 1 boundaries — IPV-001 reviewers must not penalise these as defects.

| Deferred / boundary | Rationale |
|---------------------|-----------|
| In-app study / practice content | Version 2 |
| Verified / third-party evidence | Self-reported estimates only |
| Adaptive / Revision / Diagnostic modes | Constitution Article VI Version 2 |
| Unsupported subject breadth | Server-gated supported papers only |
| RIP-004 Insight Engine automation | Accepted debt V1-TD-012 |
| Public registration | Closed — admin / coordinator provisioning |
| Recommendation-card staleness after session complete | Accepted cosmetic risk (FC-001) |
| Syllabus coverage % not advanced by session alone | Explained in product copy (FC-001) |

---

# 10. Accepted Technical Debt

Carried forward from V1RP-002 / V1RP-003. Intentional, owned, documented.

| ID | Debt | Disposition |
|----|------|-------------|
| V1-TD-001 … V1-TD-013 | As catalogued in V1RP-002 §9 | Accept (non-blocking for IPV-001) |

---

# 11. Completion Report (V1RP-004)

## Executive Summary

`VERSION1-RC1` is promoted from the FC-001-validated build. Release commit and annotated tag created. Fingerprint recorded. Release Candidate frozen. Ready for IPV-001.

## Release Promotion Result

**VERSION1-RC1 PROMOTED**  
**READY FOR IPV-001**

## Files Modified

- `knowledge/release/VERSION1_RC1.md` (this promotion record)

## Files Created

- None under this capability (product artefacts were already present in the validated working tree and are landed by the release commit)

## Migration Impact

- None under this capability. RC includes additive migrations `202607160001`–`202607160003` already present in the validated build. Head: `202607160003`.

## Architecture Compliance

- No application behaviour modified under V1RP-004.  
- Layering and curriculum V1/V2 invariants preserved as certified.  
- Research Intelligence hard boundary preserved.

## Technical Debt

- None introduced by promotion.

## Known Limitations

- See §9.

---

**Stop.**  
**Return for Executive Review.**

**End of V1RP-004 — Promote Build to VERSION1-RC1.**
