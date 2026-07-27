# Release Protocol

**Document ID:** ENG-STD-003  
**Pack:** Engineering Standards Pack  
**Status:** Canonical engineering gate  
**Audience:** Release operators and engineers preparing a ship  
**Related:** [`VERSIONING_POLICY.md`](VERSIONING_POLICY.md), [`TESTING_STANDARD.md`](TESTING_STANDARD.md), [`docs/process/RELEASE_PROTOCOL.md`](../../docs/process/RELEASE_PROTOCOL.md) (detailed operational procedure), [`.cursor/RELEASE_CHECKLIST.md`](../../.cursor/RELEASE_CHECKLIST.md)

---

## Purpose

This protocol defines the **engineering release contract**: what must be true before a version ships. Detailed operator steps (deploy, smoke, Internal Alpha) live in `docs/process/RELEASE_PROTOCOL.md`. This document owns the mandatory pre-release gates and must not contradict that procedure.

---

## Release philosophy

| Principle | Meaning |
|---|---|
| Reproducibility | Same commit + tag + target → same verifiable outcome |
| Educational integrity | Curriculum, Twin, missions, and recommendations remain coherent |
| Verifiability | Prove what is live; do not assume deploy success |
| No drive-by fixes | Do not silently redesign architecture during a release |

If a blocker is found: **STOP**, report it, and do not expand scope.

---

## Before every release verify

Complete all items below unless an explicit written waiver exists.

### 1. pytest

```bash
python -m pytest tests/ -v
```

Full suite green (or documented, reviewed exclusions only). Architecture suite green when structural change is included:

```bash
python -m pytest tests/architecture/ -v
```

### 2. Ruff

```bash
ruff check app/ src/ tests/
```

Lint clean for shipped paths per CI policy.

### 3. Alembic head

```bash
flask db heads    # expect a single head
flask db current  # staging/production target at expected revision
```

Migration releases must verify upgrade on a backup/staging database before production.

### 4. Architecture unchanged (or intentionally changed)

- No accidental layer violations (`Application` must not import `Infrastructure`).
- Educational Intelligence authorities preserved ([`ARCHITECTURE_INVARIANTS.md`](ARCHITECTURE_INVARIANTS.md)).
- Curriculum V1 and V2 remain loadable and traversable.
- If architecture **did** change: ADR or programme docs updated; architecture tests pass.

### 5. Changelog updated

Update `CHANGELOG.md` for the release with user-relevant Added / Changed / Fixed / Removed notes. Keep fingerprint fields aligned with the version being shipped.

### 6. Version tag created

Align version sources, then tag:

```bash
# ensure VERSION, pyproject.toml, and app.version.APP_VERSION agree
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

Tag naming follows [`VERSIONING_POLICY.md`](VERSIONING_POLICY.md). Tags are immutable; fix-forward with a new tag.

### 7. GitHub Release created

```bash
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file CHANGELOG.md
# or paste release notes derived from CHANGELOG / docs/release/
```

Attach or link release notes; record deploy fingerprint after production cutover per the detailed process doc.

---

## Release checklist (summary)

| # | Gate | Evidence |
|---|---|---|
| 1 | pytest green | Command output / CI |
| 2 | Ruff green | Command output / CI |
| 3 | Alembic single head + applied | `flask db heads` / `current` |
| 4 | Architecture invariants hold | Architecture tests + review |
| 5 | Changelog updated | `CHANGELOG.md` diff |
| 6 | Version tag created | `vX.Y.Z` on remote |
| 7 | GitHub Release created | Release URL |

Additional operator gates (health endpoints, smoke tests, GA checklists) remain mandatory when shipping to shared environments — see `docs/process/RELEASE_PROTOCOL.md`.

---

## Classification note

Hotfix, feature, architecture, migration, and alpha releases may require **additional** verification depth. Apply the union of requirements from the detailed protocol. This pack’s seven gates always apply.

---

## Stop conditions

**STOP** the release if:

- pytest or architecture tests fail
- Ruff fails on shipped paths under CI policy
- Multiple Alembic heads or untested migrations
- Architecture invariants or educational authority boundaries broken
- Changelog or version identity inconsistent
- Secrets detected in the release commit
