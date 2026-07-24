# Kwalitec Release Playbook

**Version:** 1.0  
**Status:** Active  
**Audience:** Release operator  
**Complements:** `docs/process/RELEASE_PROTOCOL.md` (canonical detailed procedure)  
**Related:** `knowledge/QUALITY_MANUAL.md`, `docs/ga/RELEASE_CHECKLIST.md`, `.cursor/RELEASE_CHECKLIST.md`

This playbook is the post-consolidation **operator summary**.  
For step-by-step commands and classification tables, follow the Release Protocol.

---

## 1. Release philosophy

Answer one question:

> Can this version be safely released?

Protect educational integrity and beta trust. Prefer STOP over silent unrelated fixes.

Vision alignment: shipping must not introduce unexplained recommendations, dual educational truths, or activity-theatre metrics as “success”.

---

## 2. Release process (summary)

1. **Classify** — hotfixes / feature / architecture / migration / alpha / production (Protocol §2).
2. **Pre-verify** — clean tree, architecture artefacts present, tests, ruff, config, DB, curriculum as required.
3. **Governance artefacts** — Vision, Blueprint, ADR index, Engineering Standards, Quality Manual current for the change type.
4. **Stage** — one intentional release commit if needed; no secrets.
5. **Tag / push** — per Protocol; never force-push `main`.
6. **Deploy** — Render (or host) per `docs/production/DEPLOYMENT.md`.
7. **Fingerprint** — prove the expected version is live.
8. **Smoke** — Protocol + GA release checklist + production smoke as applicable.
9. **Communicate** — release notes (private beta policy if beta cohort).
10. **Report** — release report; update Version 1 Readiness if status changes.

---

## 3. Rollback

| Situation | Action |
|---|---|
| Bad deploy fingerprint | Redeploy last known good tag |
| Critical functional break | Rollback release; hotfix branch from last good |
| Educational integrity incident | STOP cohort use if needed; do not “patch algorithms” casually — Document → Recommend |
| Migration failure | Follow Protocol migration rollback / restore from backup (`docs/production/BACKUP_AND_RECOVERY.md`) |

Record rollback in the release report. Do not destroy evidence needed for postmortem.

---

## 4. Validation

Minimum before declaring success:

- [ ] Expected `VERSION` / app version live
- [ ] Health live + ready
- [ ] Auth login path works
- [ ] Canonical student home reachable under sole runtime
- [ ] No new dual-brain regressions on smoke paths

Architecture / Production ships: architecture pytest suite green.

---

## 5. Smoke tests

- Protocol production smoke section
- `docs/release/PRODUCTION_SMOKE_TESTS_v0.4.0.md` (update paths if superseded)
- `docs/ga/RELEASE_CHECKLIST.md` / `tests/ga/` as required for GA-class ships
- Private beta: verify Today's Session start, Journey, History redirect from legacy `/analytics` if applicable

---

## 6. Performance verification

- CI soft budgets green (`docs/ga/PERFORMANCE_BASELINE.md`)
- For cohort expansion: staging sampling with `PROFILE_SQL` as in Performance Baseline
- Regressions → fix or explicit debt entry

---

## 7. Security verification

- Quality Manual security checklist
- `docs/ga/SECURITY_REVIEW.md` residuals acknowledged
- `pip-audit` reviewed for tag
- No `.env` or credentials in tag

---

## 8. Communication

| Audience | Message |
|---|---|
| Private beta | Release notes per `knowledge/product/private_beta/RELEASE_NOTES_POLICY.md` |
| Internal | Tag, fingerprint, known issues |
| Public | **Not applicable** until commercial readiness Complete |

Never overclaim pass guarantees.

---

## 9. Versioning

- Follow `docs/production/VERSIONING_POLICY.md`
- Tag matches `VERSION` / release notes
- Conventional Commits on `main` integration

---

## 10. Post-consolidation constraints

- EOS is canonical runtime
- Do not use a release window to redesign Twin, EducationalStateService, or educational algorithms
- Legacy redirect shells may remain; removing them requires Technical Debt Register proof of safety

---

**Canonical detail:** always defer to `docs/process/RELEASE_PROTOCOL.md` when this playbook and the Protocol differ in operational steps.
