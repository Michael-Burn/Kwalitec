# ER-001.1 — Release Blockers

**Programme:** ER-001 — Engineering Readiness  
**Work Package:** ER-001.1 — Version 1 Engineering Baseline Assessment  
**Date:** 2026-07-28  
**Nature:** Engineering release-blocker inventory only  
**Authority:** P-002.1 Version 1 Release Framework (engineering gates G7–G12) + CI/ops integrity  
**Out of scope blockers:** Educational G1–G6 (Product / Educational) — acknowledged, not owned by ER-001.1

---

## 1. Scope of “blocker”

A **Version 1 engineering release blocker** is any item that prevents Engineering from recommending:

> Engineering clearance for Version 1 production-ready declaration

Invite-only Alpha operation may continue under existing conditions while these remain open.

---

## 2. Engineering blockers (must clear or HOLD)

| ID | Blocker | Gate / area | Class | Owner | Clearance criterion |
|----|---------|-------------|-------|-------|---------------------|
| **ER-RB-01** | Stale secondary CI workflow `.github/workflows/tests.yml` (Python 3.14, unscoped pytest) | CI integrity / G11 | **Critical** | Engineering | Workflow retired or made identical in spirit to `ci.yml` (supported Python, same gate intent) — **Closed by EI-001.1** (`tests.yml` removed; `ci.yml` sole authority; `tests/architecture/test_ci_integrity.py`) |
| **ER-RB-02** | G7 Performance evidence incomplete (no staging/production operator sample; load test NOT STARTED) | G7 | **High** | Engineering + Release | G7.2 sample filed **or** approved HOLD with high-traffic claim restriction — **Closed by EI-001.3** (`docs/production/G7_PERFORMANCE_HOLD.md`; G7.1 CI soft budgets re-verified; load sample remains residual to lift HOLD) |
| **ER-RB-03** | G8 Reliability evidence incomplete (rollback drill note; backup/recovery acknowledgement for claim class) | G8 | **High** | Engineering + Release | G8.4 + G8.5 artefacts filed for claim window — **Closed by EI-001.3** (`docs/production/G8_RELIABILITY_EVIDENCE.md`) |
| **ER-RB-04** | G10 Security claim-class residuals (privacy signatures; dependency critical policy for tag) | G10 | **High** | Security | G10.5 policy + privacy pack for intended claim class; no open Criticals — **Partial:** G10.5 Closed by EI-001.2; operational G10.2/G10.6/G10.7 ack by EI-001.3 (`G10_OPERATIONAL_EVIDENCE.md`); privacy pack residual remains |
| **ER-RB-05** | G11 continuous green on fingerprinted release candidate | G11 | **High** | Engineering + Release | Tagged RC with green canonical `ci.yml` required suites — **Process closed by EI-001.1** (`docs/production/RELEASE_CANDIDATE_FINGERPRINT.md`); formal Version 1 RC tag still uses this process when Release cuts the candidate |
| **ER-RB-06** | G12 Version 1 flag matrix not published / Not scored | G12 | **High** | Product + Release + Engineering | Published matrix with owners, defaults, rollback, kill-switch; `.env.example` / `render.yaml` aligned — **Closed by EI-001.3** (`docs/production/VERSION_1_FLAG_MATRIX.md`) |
| **ER-RB-07** | `pip-audit` soft gate allows known Flask advisory to ship without hard policy | G10.5 | **High** | Security + Release | Critical findings fail CI **or** Security HOLD recorded on tag — **Closed by EI-001.2** (`DEPENDENCY_ASSURANCE_POLICY.md`; hard `scripts/dependency_audit.sh`; accepted HOLDs register) |

---

## 3. Structural blockers to unqualified “one-runtime / one-authority” claims

These do **not** necessarily stop invite-only Alpha, but they **block** architecture claims of full consolidation:

| ID | Blocker | Class | Owner | Notes |
|----|---------|-------|-------|-------|
| **ER-RB-08** | Parallel `src/` stack bridged into runtime | High | Architecture | Quarantined residual — do not overclaim |
| **ER-RB-09** | Dual legacy vs EIP educational authorities in code | High | Engineering + Product | Contained for Alpha; consolidation epic required |
| **ER-RB-10** | Legacy Contained presentation shells still registered | Medium | Engineering | RR-002.3 soak — retirement WP separate |

---

## 4. Explicitly NOT engineering blockers (this programme)

| Item | Why excluded |
|------|----------------|
| G1 Validated KSI FAIL | Product / Educational gate — educational governance baseline |
| G2–G6 educational quality gates | Product + Educational authorities |
| Educational copy / Mission model / Sensei / Reflection | Frozen educational surfaces |
| DG-001 / EGC-001 / RR-001 / RP-002 / RR-002 residuals | Approved Contained / Accepted — no new regression found |
| Historical V1S-001 F1/F2 pytest flash failures | Superseded by V1S-002 alignment (2026-07-15); re-verify on RC via G11 |

---

## 5. Blocker dependency graph

```
ER-RB-01 (CI integrity) [Closed EI-001.1]
        ↓
ER-RB-05 (green fingerprinted RC) ←── ER-RB-07 (dependency policy) [Closed EI-001.2]
        ↓
ER-RB-02 [Closed EI-001.3 HOLD] / ER-RB-03 [Closed EI-001.3] / ER-RB-06 [Closed EI-001.3]
        ↓
ER-RB-04 privacy residual (G10)  ←── ops ack EI-001.3; signatures still open
        ↓
Engineering GO for Version 1 declaration (still subject to Product G1–G6 + privacy for claim class)
```

Structural ER-RB-08…10 may remain as **Accepted / Contained** with disclosure if Product accepts claim language limits; they still block “architecture fully converged” marketing.

---

## 6. Recommended HOLD language (if used)

Per P-002.1, G7–G9 may HOLD only when:

1. Residual documented in debt / readiness tracker  
2. Claim language excludes high-traffic / cohort expansion the residual blocks  
3. Product + Release operator sign the HOLD  

Security Criticals and G10 Criticals must not be HOLD-waived.

---

## 7. Engineering release recommendation

| Decision | Status |
|----------|--------|
| Proceed with invite-only Alpha under existing ops | **Allowed** |
| Engineering APPROVED for Version 1 production-ready | **Blocked** — ER-RB-04 privacy residual open; ER-RB-05 formal RC tag pending Release; educational G1–G6; G7 HOLD restricts high-traffic claims. ER-RB-01 / 02 / 03 / 06 / 07 closed (02 via HOLD) |
| Educational governance reopened | **No** |

---

**End of ER-001.1 Release Blockers**
