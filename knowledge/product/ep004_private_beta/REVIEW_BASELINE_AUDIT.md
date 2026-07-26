# Review Baseline Audit — SV-001 through SV-020

**Programme:** EP-004 private beta / V1 blind educational reviews  
**Audit date:** 2026-07-24  
**Purpose:** Pre-analysis validation — confirm whether all twenty reviews reflect one consistent application baseline before any meta-analysis.

---

## 1. Current Git commit hash

```
e2622fe9329c2c4a20e85c3b35ce871ad7b60499
```

**Subject:** `docs(ep003): define educational effectiveness validation framework`  
**Committed:** 2026-07-24 07:05:23 +0200

**Note:** The student-visible P0 fix for Home → Start Session (see §6) is present in the **working tree** and is **not** included in this commit. Affected paths remain uncommitted:

- `app/infrastructure/adapters/mission/experience_adapter.py`
- `app/infrastructure/engines/opaque_bridges.py`
- related regression tests under `tests/`

Product label observed by reviewers (footer / package): **Kwalitec v2.0.0 · Internal Alpha · Founding Cohort · Build RC2**.

---

## 2. Current branch

```
feature/educational-architecture-consolidation
```

Tracks `origin/feature/educational-architecture-consolidation`.

---

## 3. How the application was reviewed

| Mode | Used? | Evidence |
|---|---|---|
| Local source (code-only reading) | No | Reviewers judged student-visible behaviour, not engineering docs |
| **Local running server** | **Yes — primary** | Review package capture: “Local running app”; RCA verification on local `:5055` with V2 inject-engines on; reviewers signed in with coordinator credentials and walked live Session / Home / Dashboard paths |
| Deployed Render version | No | No Render host / deploy fingerprint referenced in package or SV reviews |
| Screenshots only | No | Package screens were a companion; README instructs live exploration as preferred; SV narratives describe interactive sign-in, clicks, and outcomes |

**Companion package:** `knowledge/reviews/V1_REVIEW_PACKAGE/` (overview, journeys, walkthrough, known limitations, beta expectations, screens).

**Verdict:** Reviews were performed against a **local running server**, assisted by the V1 review package (docs + screenshots). Not Render. Not screenshots-only.

---

## 4. Date the review package was last regenerated

**Last regeneration (post-fix refresh):** **2026-07-24, approximately 14:55–14:58** (local filesystem timestamps)

| Artefact | Approximate mtime |
|---|---|
| Working Session Overview / fix screens (`35-session-overview.png`, `fix-*.png`, core student screens) | 2026-07-24 14:55 |
| `KNOWN_LIMITATIONS.md`, `CLICK_PATHS.md`, `USER_JOURNEYS.md`, `APPLICATION_WALKTHROUGH.md`, `REVIEW_PACKAGE_REPORT.md` | 2026-07-24 14:55–14:56 |
| `BETA_EXPECTATIONS.md` | 2026-07-24 14:56 |
| `SCREEN_INVENTORY.md` | 2026-07-24 14:58 |

**Earlier same-day generation:** morning capture ~07:35–08:03, including historical failure screens:

- `screens/58-error-500-raw.png` (2026-07-24 07:39)
- `screens/35-session-overview-error.png` (2026-07-24 07:39)

Those error captures are retained and labelled in `SCREEN_INVENTORY.md` as **historical / superseded** (“path works in current app”).

---

## 5. Whether any reviewer used an outdated package

**Yes.**

| Review | Package / app state relative to final package | Evidence |
|---|---|---|
| **SV-001** | Outdated vs final regenerated package | File completed ~14:43 — before 14:55 package refresh. Reports raw **Internal Server Error** on Home → Start Session. |
| **SV-002** | Outdated vs final regenerated package | File completed ~14:49 — before 14:55 package refresh. Reports raw **Internal Server Error** on Home → Start Session. |
| SV-003 … SV-020 | Aligned with final regenerated package | Completed from ~14:58 onward. Where Home → Start Session was tried, outcome is **working thin Session Overview** (e.g. “Core methods”, “No activities listed”), not HTTP 500. Package confirmations cite the same Build RC2 student package. |

No reviewer cites a different product version string. The outdatedness is **behavioural baseline** (pre- vs post-P0 Session start fix), not a mismatched version label.

---

## 6. Application changes during the review programme

Programme day for these reviews: **2026-07-24**.

### Change A — P0: Home → Start Session HTTP 500

| Field | Detail |
|---|---|
| What | `ExperienceMissionAdapter.start_session` raised `KeyError: 'experience_session_id'` when Mission opaque engine returned a start dict without that key → raw Flask **HTTP 500** on `POST /student/session/start` |
| Fix | Normalize / merge opaque start results so Experience identity keys are never dropped; emit `experience_session_id` from `MissionOpaqueBridge.start_opaque` |
| Files | `experience_adapter.py`, `opaque_bridges.py` (+ regression tests) |
| Educational behaviour | Unchanged (no Twin / Educational State / recommendation algorithm change) |
| Record | `ROOT_CAUSE_ANALYSIS.md` — status **FIXED** |
| Git | Uncommitted on top of `e2622fe…` at audit time |

| Affected reviews | Should review be considered valid? | Should review be repeated? |
|---|---|---|
| **SV-001**, **SV-002** | **No** as members of a single post-fix baseline. Observations of Dashboard → Session, dual homes, duration mismatch, Coach vagueness, etc. remain informative, but Home → Start Session crash findings describe a **superseded** defect. | **Yes — repeat** (or exclude from consistent-baseline meta-analysis until repeated). |
| **SV-003 … SV-020** | **Yes** for the post-fix student surface (Home → Start Session opens thin Overview; Dashboard Session path unchanged). | **No** (for this change). |

### Change B — Review package regeneration (not application code)

| Field | Detail |
|---|---|
| What | Afternoon re-capture of Session Overview / fix screens; docs updated so Home → Start Session is documented as **working** (thin Overview), with morning 500 screens marked historical |
| Application code | None beyond Change A |
| Affected reviews | Same split as Change A (SV-001 / SV-002 pre-refresh; SV-003–SV-020 post-refresh) |
| Valid / repeat | Same as Change A |

### Other application changes during SV-001…SV-020 writing window

**None found.** Working-tree application diffs for the programme day are limited to Change A (+ its tests). EP-003/EP-004 knowledge and readiness docs changed in parallel; they are not student-facing application changes.

---

## 7. Do all 20 reviews represent ONE consistent baseline?

### Conclusion

**NO**

### Why

Two sequential student-visible baselines existed on the same review day:

1. **Pre-fix (morning / early afternoon):** Home → Start Session → raw Internal Server Error (HTTP 500). Dashboard → Session still worked.
2. **Post-fix (from ~14:55 package refresh onward):** Home → Start Session → Session Overview (thinner briefing; known limitation). Dashboard → Session unchanged.

SV-001 and SV-002 are on baseline (1). SV-003 through SV-020 are on baseline (2).

Shared version chrome (**v2.0.0 · Build RC2**) does **not** erase that behavioural split.

### Reviews to discard or repeat

| Review | Action |
|---|---|
| **SV-001** | **Repeat** (or discard from consistent-baseline set until repeated on post-fix app + current package) |
| **SV-002** | **Repeat** (or discard from consistent-baseline set until repeated on post-fix app + current package) |
| SV-003 | Keep |
| SV-004 | Keep |
| SV-005 | Keep |
| SV-006 | Keep |
| SV-007 | Keep |
| SV-008 | Keep |
| SV-009 | Keep |
| SV-010 | Keep |
| SV-011 | Keep |
| SV-012 | Keep |
| SV-013 | Keep |
| SV-014 | Keep |
| SV-015 | Keep |
| SV-016 | Keep |
| SV-017 | Keep |
| SV-018 | Keep |
| SV-019 | Keep |
| SV-020 | Keep |

**Consistent-baseline set for meta-analysis (until repeats land):** **SV-003 through SV-020 (18 reviews).**

**Do not treat crash severity scores or “Home Start Session reliability” themes from SV-001 / SV-002 as describing the current fixed application.**

---

## Audit gate

Meta-analysis of the twenty reviews must **not** proceed as if all SV-001…SV-020 share one application baseline.

Proceed only after either:

1. SV-001 and SV-002 are repeated on the post-fix local baseline and current package, **or**
2. Meta-analysis is explicitly scoped to **SV-003–SV-020** and states that SV-001 / SV-002 are excluded for baseline inconsistency.

---

## Evidence index

| Source | Role |
|---|---|
| `git rev-parse HEAD` / `git branch --show-current` | Commit + branch |
| `git status` / `git diff` (app + tests) | Uncommitted P0 fix |
| `knowledge/reviews/V1_REVIEW_PACKAGE/REVIEW_PACKAGE_REPORT.md` | Local capture environment |
| `knowledge/reviews/V1_REVIEW_PACKAGE/SCREEN_INVENTORY.md` | Working vs historical 500 screens |
| `knowledge/product/ep004_private_beta/ROOT_CAUSE_ANALYSIS.md` | Defect, fix, local `:5055` verification |
| `knowledge/product/ep004_private_beta/blind_reviews/SV-001.md` … `SV-020.md` | Per-review outcomes + timestamps |
| Filesystem mtimes on package screens/docs and blind review files | Regeneration vs review ordering |
