# RF-001 — Release Checklist

**Programme:** Release Freeze Programme RF-001 — Founder Validation Build Preparation  
**Date:** 2026-07-31  
**Authority:** V1S-008 PASS · RC-002 · UX-001 PASS · PX-001…PX-004 PASS

---

## Phase checklist

| Phase | Gate | Result |
|-------|------|--------|
| 1 | Repository health | **PASS** — no PX TODOs, no debug leftovers, no temp artefacts committed; validation commit cleans working tree |
| 2 | Dependency verification | **PASS** — `requirements.txt` + Waitress; no npm build; `pip check` clean in `.venv` |
| 3 | Production configuration | **PASS** — verification only (see deployment report) |
| 4 | Render deployment | **PUSH+TAG DONE** — Manual Deploy required (auto-deploy not observed; live still `d94d514…`) |
| 5 | Founder smoke walkthrough | **PASS** (17/17 path checks + workflow suite) |
| 5 | Student smoke walkthrough | **PASS** (17/17 path checks + workflow suite) |
| 6 | Performance sanity | **PASS** — no broken assets / login & static 200; no release blockers |
| 7 | Automated tests | **PASS (release gates)** — residual full-tree debt accepted (RC-002 posture) |
| 8 | Founder Validation Build documented | **PASS** — `FOUNDER_VALIDATION_BUILD.md` / `RF001_VALIDATION_BUILD.md` |
| 9 | Release freeze | **PASS** — freeze declared in `RF001_RELEASE_FREEZE_REPORT.md` |

---

## Absolute constraints obeyed

- No features added
- No redesign / architecture refactor
- No opinionated UX polish beyond establishing the validation baseline
- Only hygiene: static asset fingerprint `2.0.0-beta.1-rf001` for PX CSS cutover cache-bust
- Blocker-only fix rule applied (no residual Category A product defects on primary paths)

---

## Operator cutover steps

1. Confirm RF-001 commit is on `origin/main`.
2. Render → service `kwalitec` → **Manual Deploy** latest `main` (auto-deploy may be off).
3. Wait for build + `flask db upgrade` (head `202607300005`).
4. Confirm `/health` `commit` matches RF-001 hash and static `?v=2.0.0-beta.1-rf001`.
5. Begin **G1 — Founder Validation** study; no feature/UX work without evidence.

---

## Companion artefacts

- `RF001_DEPLOYMENT_REPORT.md`
- `RF001_SMOKE_TEST_REPORT.md`
- `RF001_VALIDATION_BUILD.md`
- `FOUNDER_VALIDATION_BUILD.md`
- `RF001_RELEASE_FREEZE_REPORT.md`
