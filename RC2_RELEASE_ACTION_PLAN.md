# RC2_RELEASE_ACTION_PLAN.md

**Programme:** VERSION1-RC2 — Release Stabilization Sprint  
**Date:** 2026-08-01  
**Purpose:** Prioritized checklist from **current NO-GO** to an **unconditional GO** (RR-001 criteria + Release Protocol)  
**Rule:** Evidence-only; no feature work in this plan

---

## Current state (evidence)

| Fact | Value |
|------|-------|
| RR-001 decision | **NO-GO** |
| LIVE commit | `613722c` |
| Local HEAD | `f066bcf` (unpushed) |
| Working tree | Dirty |
| Alembic head | `202607310002` (single; LIVE matched) |
| App version | `2.0.0-beta.1` |

Supporting docs: `REPOSITORY_AUDIT.md`, `RC2_INTEGRITY_REPORT.md`, `DEPLOYMENT_CHECKLIST.md`, `KNOWN_ISSUES_RC2.md`, `VERSION1_RELEASE_MANIFEST.md`, RR001_*.

---

## Definition of unconditional GO

All must be true:

1. LIVE `/health.commit` equals the intended tagged Git commit.  
2. Founder + Student smoke PASS including session overview → start → completion.  
3. No open **Required before GO = Yes** issues in `KNOWN_ISSUES_RC2.md` Critical/High (or explicitly waived in writing with scope).  
4. Educational inventory on LIVE matches the release manifest.  
5. Release Protocol gates: pytest + ruff green on tip; changelog + tag published.

---

## Priority 0 — Stop conditions (do first)

| # | Action | Clears | Done? |
|---|--------|--------|-------|
| P0.1 | Freeze feature/UI/refactor work during RC cut | Release Protocol boundary | ☐ |
| P0.2 | Decide RC **scope**: (A) released Pilot Arc PB-001 path vs (B) Validation-mode inventory only | KI-H1, KI-H4, KI-C3 | ☐ |
| P0.3 | Choose **distinct git tag name** (do not reuse `v1.0.0-rc2`) | KI-M4 | ☐ |

---

## Priority 1 — Repository hygiene (RR-001 S1-OPS)

| # | Action | Evidence / how | Clears | Done? |
|---|--------|----------------|--------|-------|
| P1.1 | Exclude `.ev001_evidence/` and `.ev001_evidence.html` from commit set (archive/delete manually later) | `REPOSITORY_AUDIT.md` §4 | KI-M3 | ☑ |
| P1.2 | Exclude all `__pycache__` / `*.pyc` | gitignore already covers pattern | KI-M3 | ☑ |
| P1.3 | Stage **keep** set: educational_packages module + campaigns + package JSON + 8 app overlays + tests | `REPOSITORY_AUDIT.md` §7 | KI-C1 | ☑ |
| P1.4 | Stage EF-001 unstaged deltas + `EF001_OPERATIONAL_REVIEW_TEMPLATE.md` | Dirty EF files | KI-H3 | ☑ |
| P1.5 | Stage programme evidence markdown (EA/EO/TV/EJ/EW/EP/PR/EV/FV/RR001/…) or park under agreed docs path — **do not leave dirty** | Audit §3 | KI-C1 | ☑ |
| P1.6 | Create release commit(s) on `main` (Conventional Commits; no secrets) | User-authorized commit | KI-C1 | ☑ |
| P1.7 | Confirm `git status` clean | `git status -sb` | KI-C1 | ☑ |
| P1.8 | Push `main` to `origin/main` | `git push` | KI-H3, KI-C2 | ☐ (out of Sprint A; no deploy) |

---

## Priority 2 — RC integrity verification

| # | Action | Evidence / how | Clears | Done? |
|---|--------|----------------|--------|-------|
| P2.1 | `flask db heads` → still single expected head | CLI | Integrity | ☑ |
| P2.2 | Upgrade local SQLite (or use Postgres) to head before local smoke/tests | `flask db upgrade` | KI-M2 | ☐ (operator workstation; not blocking tip cut) |
| P2.3 | Run `ruff check app/ src/ tests/` on tip | Release Protocol | Protocol | ☑ (touched paths; full tree has pre-existing debt) |
| P2.4 | Run pytest (full or documented RC subset + architecture suite) | Release Protocol / CI | Protocol | ☑ (RC subset + architecture green) |
| P2.5 | Confirm VERSION triad; bump only if tag policy requires | `VERSION`, pyproject, `app/version.py` | Manifest | ☑ (unchanged `2.0.0-beta.1`) |
| P2.6 | Update `CHANGELOG.md` for this RC | Release Protocol | A8 | ☑ |
| P2.7 | Create annotated git tag; push tag | `git tag -a …` | Manifest | ☑ tag local; ☐ push |
| P2.8 | Fill `VERSION1_RELEASE_MANIFEST.md` fingerprint block with tip SHA/tag | Manifest | — | ☑ |

---

## Priority 3 — Deploy intended tip to Render

| # | Action | Evidence / how | Clears | Done? |
|---|--------|----------------|--------|-------|
| P3.1 | Confirm Render env vars per `DEPLOYMENT_CHECKLIST.md` §D | Dashboard | Deploy | ☐ |
| P3.2 | Optional: set `KWALITEC_BUILD_NUMBER` / date (avoid `local`) | Dashboard | KI-M1 | ☐ |
| P3.3 | Take DB snapshot if any migration beyond `202607310002` (none expected) | Render Postgres | Rollback safety | ☐ |
| P3.4 | Manual deploy of **tagged** commit to service `kwalitec` | Render dashboard | KI-C2, KI-H2 | ☐ |
| P3.5 | Verify build + `flask db upgrade` + waitress start in logs | Render logs | Deploy | ☐ |
| P3.6 | Probe `/health/live`, `/health/ready`, `/health` | curl/JSON | Deploy | ☐ |
| P3.7 | Assert `/health.commit` == tagged tip SHA | Fingerprint | KI-C2 | ☐ |
| P3.8 | Assert migrations `current=head` | `/health` | Deploy | ☐ |

---

## Priority 4 — Educational inventory + trust

| # | Action | Evidence / how | Clears | Done? |
|---|--------|----------------|--------|-------|
| P4.1 | Record deployed inventory (campaigns/packages/EF) vs manifest | Console / filesystem on tip / Founder surfaces | KI-C1 inventory leg | ☐ |
| P4.2 | If scope A (released path): Publication Approver + activation engineering for CS1-001/002 | `PR001_*`, KI-H1/H4 | High blockers | ☐ |
| P4.3 | Re-check EV-001 class failures on **new** tip (placeholder/reading/address) | Focused educational smoke | KI-C3 | ☐ |
| P4.4 | Do **not** redesign EF law; use `EF001_OPERATIONAL_REVIEW_TEMPLATE.md` for any observation | EF-001 | Freeze | ☐ |

---

## Priority 5 — Full smoke → RR-001 re-issue

| # | Action | Evidence / how | Clears | Done? |
|---|--------|----------------|--------|-------|
| P5.1 | Founder: login → experience → console → student home | Browser or scripted | KI-C4 | ☐ |
| P5.2 | Student: Today's Mission → session overview → **cold start** → **completion** | Live | KI-C4 | ☐ |
| P5.3 | Logout CSRF POST | Live | Smoke | ☐ |
| P5.4 | Update `RR001_LIVE_SMOKE_REPORT.md` with new tip evidence | Docs | RR-001 | ☐ |
| P5.5 | Update `RR001_DEPLOYMENT_VERIFICATION.md` fingerprints | Docs | RR-001 | ☐ |
| P5.6 | Re-score `RR001_RELEASE_READINESS_REPORT.md` | Docs | RR-001 | ☐ |
| P5.7 | Issue `RR001_RELEASE_DECISION.md` = **GO** only if all criteria pass | Decision | Unconditional GO | ☐ |

---

## Priority 6 — Post-GO (out of unconditional GO path)

| # | Action | Notes |
|---|--------|-------|
| P6.1 | Commence PB-001 only after GO | Per RR-001 mission |
| P6.2 | Architecture Guardian debt paydown | KI-M5 — not GO-blocking |
| P6.3 | Migration ID rename hygiene | KI-L1 — never rewrite published history casually |

---

## Ordered blocker burn-down (shortest path)

```
P0 scope + tag name
  → P1 clean commit + push (inventory + overlays + EF)
    → P2 tests/ruff/changelog/tag
      → P3 Render deploy + fingerprint match
        → P4 inventory/trust verification (activation if scope A)
          → P5 full smoke + RR-001 GO
            → unconditional GO
```

Any failure: **STOP**, update `KNOWN_ISSUES_RC2.md`, do not expand into features.

---

## Explicit non-actions (this plan)

- Do not add features, redesign UI, or optimize unrelated code.  
- Do not delete files automatically without operator approval (`REPOSITORY_AUDIT.md` plan first).  
- Do not unfreeze Educational Framework (EF-001).  
- Do not treat `publication_ready` as `released`.

---

## Exit criterion

When Priorities 0–5 are checked and RR-001 is reissued **GO**, update:

- `VERSION1_RELEASE_MANIFEST.md` fingerprint → **GO**  
- `RR001_RELEASE_DECISION.md` → **GO**  
- This file → mark all Done? = ☑  

**Present exit status:** **NOT MET** — Release Candidate Ready = **NO**.
