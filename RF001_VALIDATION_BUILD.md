# RF-001 — Validation Build

**Programme:** Release Freeze Programme RF-001  
**Date:** 2026-07-31  

Canonical baseline document: **[`FOUNDER_VALIDATION_BUILD.md`](FOUNDER_VALIDATION_BUILD.md)** (`FV-001`).

---

## Build record

| Field | Value |
|-------|--------|
| Build identifier | `FV-001` |
| Product version | `2.0.0-beta.1` |
| Static fingerprint | `2.0.0-beta.1-rf001` |
| Environment | Production (`https://kwalitec.onrender.com`) |
| Database version | Alembic `202607300005` |
| Commit hash | `8915930c913d5cd08f19c1ab69fc8a8f6bf37696` |
| Deployment date | 2026-07-31 |

---

## Authority chain

V1S-008 PASS → RC-002 → UX-001 PASS → PX-001 PASS → PX-002 PASS → PX-003 PASS → PX-004 PASS → **RF-001 freeze**

---

## Test summary (sealed)

- Smoke: Founder **PASS**, Student **PASS** (17/17)
- Release gates: 773 passed (presentation / workflows / integrity critical path)
- Full tree: 45616 passed / 159 failed / 9 skipped — residual debt accepted, not Category A

---

## Known accepted limitations

See `FOUNDER_VALIDATION_BUILD.md`.

---

## Outstanding non-blocking debt

See `FOUNDER_VALIDATION_BUILD.md`.

---

## Validation objectives

This build is the immutable baseline for **G1 — Founder Validation**. All future product changes must be justified by evidence from real study sessions.
