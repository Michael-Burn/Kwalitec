# Kwalitec Release Protocol

**Version:** 2.0  
**Status:** Canonical operational release procedure  
**Audience:** Release operator  
**Nature:** Process only — not architecture, not design

---

## OBJECTIVE

Answer one question:

> Can this version be safely released?

This protocol is an operational workflow. It does not restate architecture. It does not invent features. It does not redesign the product.

If a release blocker is found: **STOP**, report it, and do not silently fix unrelated issues.

---

## RELEASE BOUNDARIES

### Allowed

- Verify repository state
- Run verification (tests, Ruff, config, DB, curriculum)
- Stage and create a release commit when required
- Push to GitHub
- Create and push a Git tag
- Prepare release notes
- Deploy to Render
- Verify deployment fingerprint
- Run production smoke tests
- Produce a release report

### Not Allowed

- New features
- Architecture changes
- Educational Intelligence / Twin / Recommendation redesign
- Unrelated refactors or cosmetic work
- Fixing historical technical debt during the release

---

# 1. Release Philosophy

Disciplined releases protect educational integrity and Internal Alpha trust.

| Principle | Meaning |
|---|---|
| Reproducibility | Same commit, same tag, same deploy target → same verifiable outcome |
| Educational integrity | Curriculum, plans, progress, recommendations, and missions must remain coherent for real study |
| Protect Internal Alpha users | Do not surprise testers with mixed builds, silent schema breaks, or incompatible educational data |
| Verifiability | Every release must prove what is live (fingerprint + smoke), not assume deploy success |

A release is successful only when the expected version is live and verified.

---

# 2. Release Classification

Classify every release before starting. Classification drives verification depth.

| Type | Purpose | Typical scope | Minimum verification |
|---|---|---|---|
| **Hotfix** | Urgent production fix | Narrow bugfix; no schema/curriculum change | Repo + tests + deploy fingerprint + targeted smoke |
| **Feature Release** | Ship completed product capability | App/services/UI; usually no migration | Full pre-release + deploy + smoke for affected journeys |
| **Architecture Release** | Structural platform change | Layering, engines, major service boundaries | Full pre-release + curriculum (if touched) + data compatibility decision + elevated smoke |
| **Migration Release** | Schema or durable data change | Alembic and/or educational data migration | Explicit DB verification **before** deploy + fingerprint + smoke |
| **Internal Alpha Release** | Shared tester baseline | Any of the above plus alpha ops | Classification verification + §10 Internal Alpha requirements |
| **External Alpha Release** | Broader closed testers | Stable slice; limited reset options | Full verification + compatibility decision; prefer no reset |
| **Production Release** | Public or production-grade ship | Tagged milestone | Full verification + risk classification + rollback plan recorded |

A single ship may carry more than one type (e.g. Migration + Internal Alpha). Apply the **union** of minimum verification.

---

# 3. Pre-Release Verification

## Repository

- [ ] Correct branch (normally `main` for production ships)
- [ ] Working tree clean (or one intentional release commit created, then clean)
- [ ] Commits reviewed; no secrets (`.env`, credentials, private keys)

```
git status
git log -5 --oneline
```

If uncommitted release-required files exist: stage only those files, create **one** release commit, re-verify clean tree.

## Architecture governance artefacts

Version 2 architecture documents are **release artefacts**. Confirm they are present and current for Architecture / Production ships (and any release that touches `src/` educational boundaries):

| Artefact | Path |
|---|---|
| Architecture Constitution | `docs/ARCHITECTURE_CONSTITUTION.md` |
| Architecture Overview | `docs/ARCHITECTURE_OVERVIEW.md` |
| System Context | `docs/SYSTEM_CONTEXT.md` |
| Dependency Rules | `docs/DEPENDENCY_RULES.md` |
| ADRs ADR-001 … ADR-010 | `docs/adr/` |
| Version file | `VERSION` |
| Version 2 release notes | `RELEASE_NOTES_V2.md` |
| Version 3 roadmap | `ROADMAP_V3.md` |
| V2 release checklist | `docs/release/V2_RELEASE_CHECKLIST.md` |

- [ ] Architecture governance documents present (APP-003 set)
- [ ] Architecture ADR index current (`docs/adr/README.md`)
- [ ] Production readiness artefacts present (APP-004 set)
## Tests

```
python3 -m pytest tests/architecture/ -v
python3 -m pytest
```

- [ ] Architecture governance gates pass (`tests/architecture/` — mandatory CI gate)
- [ ] pytest passes

Ruff: run on modules modified in this release. Do not treat historical repository-wide Ruff debt as a blocker unless explicitly instructed.

- [ ] Ruff clean on release-touched modules

If tests fail: **STOP**. Report failures, root cause, recommended fix. Do not continue.

## Configuration

- [ ] Required environment variables present for the target environment
- [ ] Secrets not committed; production `SECRET_KEY` and DB credentials verified out-of-band
- [ ] Admin bootstrap env present when startup admin is expected (`ADMIN_EMAIL` / `ADMIN_PASSWORD` as applicable)

---

# 4. Database Verification

**Trigger:** schema changed, new Alembic revision, or migration release.

If migrations exist, require **explicit verification before deployment**.

## Checklist

- [ ] Alembic head matches expected revision
- [ ] Migration applies cleanly on a representative database
- [ ] New tables present (if any)
- [ ] Altered columns present and typed as expected (if any)
- [ ] Application startup succeeds after migrate
- [ ] No destructive surprise (drops / data loss) unless deliberately approved for Internal Alpha reset

## Record

| Item | Value |
|---|---|
| Previous head | |
| New head | |
| Applied on | local / staging / production |
| Result | PASS / FAIL |

If migration fails: **STOP**.

---

# 5. Curriculum Verification

**Trigger:** curriculum JSON, discovery, import path, or subject packaging changed.

Verify **every modified curriculum**. No subject-specific assumptions — treat CS1, CB2, CM1, and future papers the same.

For each modified curriculum id:

| Check | Pass? |
|---|---|
| Discovery finds the curriculum | |
| Import succeeds (idempotent re-import safe) | |
| Study Plan can be created / self-healed against it | |
| TopicProgress aligns with imported topics | |
| Recommendation path runs without curriculum errors | |
| Mission path resolves topics / objectives correctly | |

Record curriculum ids verified (examples: `CS1`, `CB2`, `CM1`, …).

If any modified curriculum fails: **STOP**.

---

# 6. Educational Data Compatibility

For **every** release, record one decision about existing user educational data (plans, progress, twin, missions, calibration state).

| Decision | Meaning |
|---|---|
| **Compatible** | Existing data works as-is with the new version |
| **Self-healing** | Startup or service paths repair plans/progress safely; no manual reset |
| **Requires migration** | Explicit data/schema migration must run before users continue |
| **Requires Internal Alpha reset** | Controlled wipe/rebaseline of educational data for shared testing |

### Decision record (required)

| Field | Value |
|---|---|
| Decision | Compatible / Self-healing / Requires migration / Requires Internal Alpha reset |
| Why | |
| Affected data | plans / TopicProgress / Twin / missions / other |
| Operator action | none / migrate / reset / notify testers |

Do not deploy an Internal Alpha shared round with an undecided compatibility outcome.

---

# 7. Deployment

Operational sequence:

```
GitHub (push main)
        ↓
Tag (semantic, immutable)
        ↓
Release Notes
        ↓
Render (deploy / wait for auto-deploy)
        ↓
Health
        ↓
Smoke Tests
```

## GitHub

```
git push origin main
```

- [ ] Push succeeded
- [ ] Record commit hash

## Tag

- Inspect existing tags; choose next semantic version
- Never overwrite an existing tag

```
git tag vX.Y.Z
git push origin vX.Y.Z
```

- [ ] Tag created and pushed
- [ ] Version recorded

## Release Notes

- Concise notes for completed work only
- Do not invent features
- Store under `docs/release/` when producing a formal notes file

## Render

- Deploy the tagged commit (manual deploy or confirm auto-deploy of the intended commit)
- Account for **Render auto-deploy timing**: push ≠ live; wait until the build for the expected commit finishes
- [ ] Build successful
- [ ] Migrations successful (if any)
- [ ] Startup successful
- [ ] Logs free of startup exceptions

If deployment fails: **STOP**.

## Health

- [ ] `/health` returns OK
- [ ] Database connected (as reported by health / logs)

---

# 8. Deployment Fingerprint

Prove the **expected** version is actually live. Do not trust “deploy finished” alone.

| Signal | How to verify |
|---|---|
| Git commit | Render deploy commit matches release commit |
| Release tag | Tag points at that commit; notes reference same tag |
| Application version | Product/version surface matches release (when exposed) |
| Health endpoint | `/health` OK after the new deploy |
| Build fingerprint | Render build id / deploy timestamp matches this ship |

### Fingerprint record

| Field | Expected | Observed |
|---|---|---|
| Commit | | |
| Tag | | |
| App version | | |
| Health | OK | |
| Build / deploy id | | |

Mismatch → **STOP**. Do not begin smoke tests on the wrong build.

---

# 9. Smoke Tests

Concise production checklist. Prefer journeys affected by this release; for Architecture / Migration / Internal Alpha / Production ships, run the full list.

## Core

- [ ] Login
- [ ] Dashboard
- [ ] Study Plan
- [ ] Calibration (when in scope)
- [ ] Recommendation
- [ ] Mission
- [ ] Progress
- [ ] Theme
- [ ] Settings
- [ ] Logout
- [ ] Health endpoint

## Curriculum-specific (when curriculum or multi-subject touched)

For each modified curriculum under test:

- [ ] Curriculum visible / selectable as designed
- [ ] Plan + recommendation + mission coherent for that subject

## Pass rule

Any failure on an in-scope check → **STOP** and report. Do not mark the release successful.

---

# 10. Internal Alpha Releases

Additional requirements when the audience is Internal Alpha testers.

- [ ] Notify testers of the release window and version under test
- [ ] Reset educational data **if** §6 decided “Requires Internal Alpha reset”
- [ ] Confirm everyone starts from the **same baseline** (same tag, same data policy)
- [ ] Document the release version under test (tag + commit) in the alpha journal / playbook notes as appropriate
- [ ] **Do not mix builds** during the same alpha round — one tagged baseline until the round is closed or explicitly rebaselined

Internal Alpha releases still follow §§3–9. Classification alone does not skip fingerprint or smoke.

---

# 11. Release Report

Produce the same report structure for every release.

### 1. Executive Summary

What shipped and why it is safe (or why it stopped).

### 2. Commit

Full hash.

### 3. Tag

`vX.Y.Z` or N/A if stopped before tag.

### 4. Tests

pytest outcome.

### 5. Ruff

Scope and outcome.

### 6. Deployment

Render result + fingerprint summary.

### 7. Smoke Tests

Pass/fail list (brief).

### 8. Known Issues

Blockers deferred or accepted limitations.

### 9. Verdict

**RELEASED** / **STOPPED** / **RELEASED WITH KNOWN ISSUES**

Also record when relevant:

- Release classification (§2)
- Educational data compatibility decision (§6)
- Risk class (§12)

---

# 12. Release Risk

Classify every release before deploy.

| Risk | Typical drivers | Required verification |
|---|---|---|
| **Low** | Hotfix or narrow feature; no schema/curriculum/data change | Pre-release + fingerprint + targeted smoke |
| **Medium** | Feature or multi-subject touch; self-healing data; routine migration | Full pre-release + DB/curriculum as triggered + full core smoke |
| **High** | Architecture, durable Twin/persistence change, non-trivial migration, Internal Alpha reset, multi-curriculum behaviour change | Union of all triggered sections + explicit rollback notes + tester notification if alpha |

### Risk record

| Field | Value |
|---|---|
| Risk | Low / Medium / High |
| Why | |
| Affected components | |
| Rollback complexity | Low / Medium / High |
| Required verification | (checklist refs) |

---

# 13. Rollback

Choose strategy from what actually changed.

| Strategy | When | Notes |
|---|---|---|
| **Application-only rollback** | No schema/data migration; bad app build | Redeploy previous known-good commit/tag; re-verify fingerprint |
| **Migration rollback** | Alembic revision is safely downgradable | Downgrade only with tested `downgrade()`; prefer forward-fix if downgrade is unsafe |
| **Feature flag / config rollback** | Behaviour gated by config | Revert flag/env; no code redeploy if sufficient |
| **Inappropriate to roll back** | Irreversible data reset, destructive migration, or mixed alpha baselines | Stop further deploys; restore from backup or rebaseline explicitly; communicate to testers |

Always re-run health + fingerprint + critical smoke after any rollback.

---

# 14. Versioning

Semantic expectations for Kwalitec:

| Band | Meaning |
|---|---|
| `v0.x.y` | Internal Alpha / pre-public era |
| `v1.0.0` | First public / production-grade release bar |
| `vX.Y.Z` | Patch/hotfix (`Z`), minor feature (`Y`), major breaking platform (`X`) when that bar applies |

### Tag naming

- Prefer `vMAJOR.MINOR.PATCH` (e.g. `v0.9.0`)
- Tags are immutable; never move a published tag
- Hotfixes increment patch on the current minor line unless a new minor is intentional

### Cadence (default expectations)

| Cadence | Expectation |
|---|---|
| Weekly release | Prefer a tagged weekly baseline during active Internal Alpha when there is shippable completed work |
| Hotfix cadence | As needed; still tagged and fingerprinted; do not skip §8–§9 |

Cadence is a planning default, not a requirement to ship empty releases.

---

# STOP CONDITIONS

Stop immediately if:

- Tests fail
- Required DB / curriculum verification fails
- Educational data compatibility is undecided for an Internal Alpha shared round
- Deployment fails
- Migration fails on the target environment
- Deployment fingerprint mismatches
- Production / alpha smoke test fails
- Health endpoint fails

Do not implement new functionality during a release. Report the blocker.

---

# SUCCESS CRITERIA

A successful release means:

- [ ] Classification and risk recorded
- [ ] Pre-release verification passed
- [ ] Triggered DB / curriculum / compatibility checks passed
- [ ] Code pushed and tagged as planned
- [ ] Render deploy matches fingerprint
- [ ] Smoke tests passed for in-scope journeys
- [ ] Internal Alpha extras completed when applicable
- [ ] Release report produced with verdict

Nothing else is required for the release operation itself.
