# RC-002 — Release Blockers (Category A)

**Programme:** RC-002  
**Date:** 2026-07-27  
**Count:** **0**

---

## Definition (charter)

Critical release blockers include: runtime failure, broken workflow, data corruption, security/privacy issue, migration issue, startup failure, production crash, accessibility blocker, truthfulness violation.

These **must** block deployment.

---

## Inventory

| Test | Category A? | Why not A |
|------|:-----------:|-----------|
| *(none)* | — | — |

No residual failure meets Category A criteria after implementation inspection.

---

## Explicitly examined and rejected as A

| Candidate | Why inspected | Why not A |
|-----------|---------------|-----------|
| `test_empty_database_applies_migrations_and_creates_admin` | Startup / migration | Migrations apply (`Applying migrations…` / `Migrations complete.`); admin is created. Failure is log string `'Admin created.'` vs `'Admin created with Founder RBAC.'` → **D** |
| `test_custom_500_page_in_production_mode` | Production crash UX | 500 handler returns student-safe page; missing literal `Internal Server Error` → **D** |
| EIP / IA “Learning Mode” / “Estimated Knowledge” absences | Truthfulness / explainability | Page still explains selection (`Why you are studying this`, Observed Facts, Estimates). No false exam/readiness claim. Vocabulary gap vs EIP-003 → **B**, not A |
| `test_student_templates_forbid_engineering_terms` | Truthfulness | Offender is Jinja comment documenting B10 rename of Digital Twin; rendered label is `Personalised recommendations` → **D** |
| EOS page / token snapshots | Broken UI | HTTP 200; PX-004 polish drift; `/eos/` not Stage 1 prod mount → **D** |
| Architecture independence / purity | Structural risk | Layering debt; no evidence of Stage 1 runtime breakage → **C** |
| Dual-run / simulation / recovery equality | Recommendation truth | Field-level diff is `generated_at` only → **D** |
| CSS budget `70362 < 70000` | Performance | Soft budget overrun of 362 bytes → **C** |
| PIL `ModuleNotFoundError` | Brand integrity | Logo files present and byte-equal; missing test dependency → **D** |

---

## Conclusion

**Category A count = 0 → does not trigger DO NOT DEPLOY.**
