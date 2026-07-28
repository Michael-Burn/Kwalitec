# Release Candidate Fingerprint Process

**Programme:** EI-001 — Engineering Improvements  
**Work Package:** EI-001.1 — CI Integrity & Release Evidence  
**Authority:** ER-001.1 (ER-RB-05) · P-002.1 Gate G11 · `docs/process/RELEASE_PROTOCOL.md`  
**Status:** Binding for engineering release evidence  
**Date:** 2026-07-28

---

## 1. Purpose

A **Release Candidate (RC) fingerprint** is the reproducible identity of a candidate build used for Version 1 (and Internal Alpha) release decisions. It links:

1. **Git identity** (commit SHA ± annotated tag)  
2. **Canonical CI execution** (sole workflow `.github/workflows/ci.yml`)  
3. **Release documentation** (notes, checklist, evidence pack references)

Without a fingerprint, “CI was green” and “we deployed something” cannot be proven to refer to the same artefact.

---

## 2. Sole CI authority

| Rule | Detail |
|------|--------|
| Canonical workflow | `.github/workflows/ci.yml` (`name: Kwalitec CI`) |
| Retired workflow | `.github/workflows/tests.yml` — **removed** (EI-001.1 / ER-RB-01) |
| Supported Python | Unit matrix **3.11 / 3.12 / 3.13**; other jobs pin **3.13** |
| Merge / RC signal | Only jobs in `ci.yml` may be cited as engineering green |

Do **not** invent parallel workflow files for “extra confidence.” Extend `ci.yml` or document an intentional HOLD.

Architecture regression: `tests/architecture/test_ci_integrity.py`.

---

## 3. Fingerprint fields (required record)

| Field | Source | Notes |
|-------|--------|-------|
| `commit_sha` | `git rev-parse HEAD` (full SHA) | Immutable once tagged |
| `branch` | Branch that produced the candidate (usually `main`) | Informational |
| `tag` | Annotated tag (e.g. `v1.0.0-rc.N` or release tag) | Required for G11 claim packages |
| `version_file` | Contents of `VERSION` | Must match claimed version / tag policy |
| `ci_workflow` | `Kwalitec CI` / path `ci.yml` | Sole authority |
| `ci_run_url` | GitHub Actions run URL for that SHA | Prefer `main` push or PR merge run |
| `ci_conclusion` | `success` for all required jobs | See §4 |
| `recorded_at` | UTC ISO-8601 | When the fingerprint was filed |
| `recorder` | Engineering or Release owner | Named |

Optional but recommended: Alembic head id, `pip-audit` note path, deploy health commit once live.

---

## 4. Required CI jobs (G11 engineering suites)

A fingerprinted RC is **engineering-green** only when **all** of the following `ci.yml` jobs conclude successfully on `commit_sha`:

| Job id | Gate intent |
|--------|-------------|
| `architecture` | Architecture / curriculum invariants (G11.3) |
| `unit` | Unit matrix on supported Python (G11.1) |
| `integration` | Broad integration + founder/automation suites (G11.1) |
| `educational-intelligence-certification` | EI cert + release-doc presence |
| `lint` | Ruff policy (G11.2) |
| `production-gates` | PR/GA ops tests, Alembic head pin, soft `pip-audit`, production docs |
| `release-build` | VERSION / render.yaml / factory / dependency artefact checks |

Local reproduction (engineering evidence, not a substitute for Actions on the tagged SHA):

```bash
python -m pytest tests/architecture/ -v --tb=short
python -m pytest tests/education_os/ tests/domain/ tests/architecture/ -v --tb=short
ruff check app/ src/ tests/ --ignore=F401
# Full remote green remains the G11 claim source of truth for a tagged RC.
```

---

## 5. Procedure — create a green RC fingerprint

1. **Stabilize** — intended content on `main` (or release branch policy); working tree clean for the tagged commit.  
2. **Confirm sole CI** — `.github/workflows/` contains only `ci.yml`; architecture CI integrity tests green.  
3. **Wait for Actions** — GitHub run for that SHA: all §4 jobs `success`. Record `ci_run_url`.  
4. **Tag** — annotated tag pointing at the SHA (`docs/production/VERSIONING_POLICY.md`).  
5. **File the fingerprint** — complete the template in §7 under the release evidence pack (or link from Go/No-Go).  
6. **Link documentation** — release notes / checklist / G11 pack cite the same `commit_sha` + `tag` + `ci_run_url`.  
7. **Deploy (when in scope)** — verify live `/health` commit matches fingerprint (`RELEASE_PROTOCOL.md` §8).

Mismatch at any step → **STOP**. Do not advance smoke or Version 1 claims on a different SHA.

---

## 6. Engineering evidence chain

```
Commit SHA  ──►  Kwalitec CI (ci.yml) green
                      │
                      ▼
              Annotated RC / release tag
                      │
                      ▼
         Fingerprint record (§7) + release notes
                      │
                      ▼
         Deploy / health commit match (ops)
                      │
                      ▼
         G11 / Go-No-Go evidence package citation
```

| Link | Artefact |
|------|----------|
| CI execution | Actions run for SHA; job list §4 |
| RC verification | Tag → SHA; VERSION alignment; fingerprint record |
| Release documentation | Notes, checklist, P-002.1 G11 pack paths |

---

## 7. Fingerprint record template

Copy into the release evidence pack:

```markdown
### RC Fingerprint

| Field | Value |
|-------|-------|
| commit_sha | |
| branch | |
| tag | |
| version_file | |
| ci_workflow | .github/workflows/ci.yml (Kwalitec CI) |
| ci_run_url | |
| ci_conclusion | success / fail |
| recorded_at (UTC) | |
| recorder | |

Required jobs (all success): architecture · unit · integration · educational-intelligence-certification · lint · production-gates · release-build
```

---

## 8. Explicit non-claims

- Filing this process document does **not** by itself declare Version 1 production-ready.  
- Educational gates G1–G6 remain Product / Educational authorities.  
- Soft `pip-audit` in `ci.yml` remains a separate engineering residual (ER-RB-07) until hardened.  
- Local pytest green is supporting evidence; **tagged SHA + Actions success** is required for G11 claim packages.

---

## References

- `knowledge/release/EI-001/EI001_1_IMPLEMENTATION_REPORT.md`  
- `knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md` (G11)  
- `docs/process/RELEASE_PROTOCOL.md` (§8 Deployment Fingerprint)  
- `docs/production/RELEASE_PROCESS.md`  
- `docs/production/VERSIONING_POLICY.md`
