# SOURCE_CERTIFICATION.md

**Programme:** RC-001  
**Release Candidate ID:** `RC-2026.07.29-01`  
**Recorded at (UTC):** `2026-07-28T23:03:37Z`

---

## Recorded values

| Field | Value | Evidence |
|---|---|---|
| Git commit SHA | `f17058862baf9aa8c6f416c6fa7bd26739812fb8` | `git rev-parse HEAD` → `_evidence/source/source_snapshot.txt` |
| Active branch | `feature/ap-002-assessment-engine` | `git branch --show-current` |
| Repository status | **modified** (not clean) | `git status --porcelain` → **86** dirty/untracked paths |
| Build timestamp | `2026-07-28T23:03:37Z` | Worktree freeze timestamp |
| Build identifier | `5e8e92256cbd1e728e5ddb8f8ec40b1f9f26ccf1ac84ddb0addd36d02593915e` | SHA-256 of `_evidence/source/worktree_manifest_sha256.txt` (63 application-affecting file hashes) |

### HEAD commit metadata

| Field | Value |
|---|---|
| Subject | `docs(fv-001): record completion report commit hashes` |
| Committer date | `2026-07-28 22:20:04 +0200` |

### Worktree freeze

The intended validation code image is **HEAD plus local modifications** (post–PI-002R / Curriculum Studio publication pipeline work). Commit SHA alone does **not** identify the loaded image.

Frozen evidence:

- `_evidence/source/worktree_paths.txt` — paths included in the freeze
- `_evidence/source/worktree_manifest_sha256.txt` — per-file SHA-256
- Aggregate build identifier above

Any change to a frozen path changes the build identifier and **invalidates** this Release Candidate.

---

## Verification

| Check | Result | Notes |
|---|---|---|
| Working tree clean | **FAIL** | 86 modified/untracked paths at certification time |
| Intended commit checked out | **PASS (with freeze)** | HEAD `f1705886…` checked out; intended *image* is HEAD + frozen dirty tree |

---

## Condition (carried to certificate)

Source certification substitutes a **frozen worktree digest** for a clean tree. Subsequent programmes must recompute the digest from `_evidence/source/worktree_manifest_sha256.txt` inputs and confirm it still equals:

`5e8e92256cbd1e728e5ddb8f8ec40b1f9f26ccf1ac84ddb0addd36d02593915e`

If it differs → Release Candidate invalidated → new RC-001 required.
