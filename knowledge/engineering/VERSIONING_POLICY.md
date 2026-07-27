# Versioning Policy

**Document ID:** ENG-STD-008  
**Pack:** Engineering Standards Pack  
**Status:** Canonical  
**Audience:** Engineers and release operators  
**Related:** [`RELEASE_PROTOCOL.md`](RELEASE_PROTOCOL.md), [`GIT_WORKFLOW.md`](GIT_WORKFLOW.md), [`docs/production/VERSIONING_POLICY.md`](../../docs/production/VERSIONING_POLICY.md), `VERSION`, `pyproject.toml`, `app/version.py`

---

## Purpose

Kwalitec uses Semantic Versioning for product releases. This policy defines how Major, Minor, and Patch numbers change, how tags and releases are named, and how milestones are named relative to versions.

---

## Source of truth

For a shipped release, these must agree:

| Source | Role |
|---|---|
| `VERSION` | Repository semver file |
| `pyproject.toml` `[project].version` | Packaging version |
| `app.version.APP_VERSION` | Runtime / health identity for the app |

Do not ship with divergent version identity.

---

## Semantic versioning

Format:

```
MAJOR.MINOR.PATCH
```

Optional pre-release suffix when publishing candidates:

```
MAJOR.MINOR.PATCH-<label>
```

Examples: `2.0.0`, `2.1.0`, `2.1.1`, `1.0.0-rc.2`

### Major

Bump **MAJOR** when the release includes breaking change that requires coordinated cutover, for example:

- Breaking public/student API or durable contract break
- Schema or educational-data change that is not backward compatible
- Removal or incompatible replacement of a production educational authority contract

Major releases must call out migration and compatibility impact in the changelog and release notes.

### Minor

Bump **MINOR** when the release adds backward-compatible capability, for example:

- New educational capability that preserves existing contracts
- New operator surfaces that do not break student journeys
- Backward-compatible API additions

Reset PATCH to `0` when MINOR increments.

### Patch

Bump **PATCH** when the release is backward-compatible hardening without new learner-facing capability, for example:

- Bug fixes
- Security hardening
- Documentation-only governance packs (if a version ship is required)
- Operational fixes that do not change educational contracts

---

## Tag naming

Git tags for releases:

```
vMAJOR.MINOR.PATCH
```

Examples: `v2.0.0`, `v2.1.0`

Pre-release tags:

```
vMAJOR.MINOR.PATCH-<label>
```

Example: `v1.0.0-rc.2`

Rules:

- Always prefix with `v`
- Tags are immutable; fix-forward with a new tag
- Every production deploy is tagged
- Health JSON `version` must match the tagged release

---

## Release naming

| Artefact | Naming |
|---|---|
| GitHub Release title | Prefer `vX.Y.Z` or `vX.Y.Z — <short theme>` |
| Changelog heading | `[X.Y.Z] - YYYY-MM-DD — <theme>` |
| Release notes files | `docs/release/RELEASE_NOTES_vX.Y.Z.md` (or programme-agreed path) |

Release notes describe user/operator impact; they do not replace architecture ADRs.

---

## Milestone naming

Milestones identify work packages; they are **not** product versions.

| Form | Example |
|---|---|
| Programme-milestone | `ENG-001`, `SDT-003`, `TUTOR-001` |
| Branch | `milestone/eng-001-engineering-standards` |
| Folder | `knowledge/engineering/` or programme-specific path |

Rules:

- Milestone IDs stay stable even if the eventual release version changes
- Multiple milestones may land in one MINOR/MAJOR release
- A single milestone must not claim a version bump unless the brief is a release milestone
- Do not overload milestone IDs as SemVer (use `ENG-001`, not `v1.1.0`, for work tracking)

---

## When not to bump

- Merging to `main` alone does not require a version bump
- Internal WIP commits do not bump version
- Documentation merged without a ship may leave version unchanged until the next release

---

## Alignment with existing production policy

Operational notes in `docs/production/VERSIONING_POLICY.md` remain valid for deploy identity. If a conflict appears, resolve via ADR and update both documents in the same change — do not leave contradictory bump rules.
