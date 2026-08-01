# PUBLICATION_ACTIVATION_REPORT.md

**Programme:** VERSION1-RC2 — Sprint C1 — Educational Publication Activation  
**Authority:** EF-001 · EC-001 PASS (inventory) · PB-001A PI-S1 blocker · EA-006 live loader  
**Date:** 2026-08-01  
**Nature:** Publication pipeline only — Runtime, pedagogy, and Educational Framework unmodified  

---

## Verdict

# **PASS — EC-001 certified packages are registered `publication_approved` under the EA-006 live loader**

Catalogue packages that were stranded as `campaign_member_certified` under `educational_campaigns/` are now jointly registered as live educational packages. Student Reading for published topics resolves via `find_educational_package()` / `EducationalSubstancePlanner` to certified package substance (not the fallback LO shell), subject to the documented shared-`topic_code` first-match residual (KI-H4).

---

## Why packages remained `campaign_member_certified`

| Cause | Detail |
|-------|--------|
| Catalogue gate | EP-001 / CS1-002 deliberately set status `campaign_member_certified` so EA-006 would **not** auto-load orphans before Approver + activation (EA-R1-04 / EA-R2-06). |
| Loader root | Live loader scans **only** `app/curriculum/data/educational_packages/**/*.json`. |
| Status enum | Live admission requires `publication_approved` / `approved` / `certified` — not `campaign_member_certified`. |
| Path class | Campaign JSON under `educational_campaigns/` is inventory, not the live publication path. |

**Not causes:** Missing EC-001 reading body (authored); Runtime defects; Educational Framework gaps.

---

## Publication inventory activated (joint)

All nine EC-001 inventory packages are LIVE-eligible after this sprint:

| # | Package | Old Status | New Status | Reason | LIVE eligible |
|---|---------|------------|------------|--------|---------------|
| 1 | `CS1-EA005-PKG-4.2-GLM-STRUCTURE` | `publication_approved` (pre-EC-001 tip copy) | `publication_approved` (EC-001 remediated body) | Already on live path; commit EC-001 `reading_guidance` so LIVE can receive certified partnership text | **Yes** |
| 2 | `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` | `campaign_member_certified` | `publication_approved` | Registered under `educational_packages/cs1/1.1-purpose-function-ep001.json` | **Yes** |
| 3 | `CS1-EP001-PKG-1.2-EDA-SUMMARIES` | `campaign_member_certified` | `publication_approved` | Registered as `1.2.1-eda-summaries-ep001.json` (first-match for topic `1.2`) | **Yes** (selected for `1.2`) |
| 4 | `CS1-EP001-PKG-1.2-EDA-ASSOCIATION` | `campaign_member_certified` | `publication_approved` | Registered as `1.2.2-eda-association-ep001.json` (joint inventory; not first-match on `1.2`) | **Yes** (on disk; deferred selection — KI-H4) |
| 5 | `CS1-EP001-PKG-REV-PURPOSE-EDA` | `campaign_member_certified` | `publication_approved` | Registered as `revision-purpose-eda-ep001.json` (`CA-R1`) | **Yes** (revision code) |
| 6 | `CS1-CS1002-PKG-1.2-PCA` | `campaign_member_certified` | `publication_approved` | Registered as `1.2.3-pca-cs1002.json` (joint inventory; not first-match on `1.2`) | **Yes** (on disk; deferred selection — KI-H4) |
| 7 | `CS1-CS1002-PKG-2.1-DISCRETE` | `campaign_member_certified` | `publication_approved` | Registered as `2.1.1-discrete-cs1002.json` (first-match for topic `2.1`) | **Yes** (selected for `2.1`) |
| 8 | `CS1-CS1002-PKG-2.1-CONTINUOUS` | `campaign_member_certified` | `publication_approved` | Registered as `2.1.2-continuous-cs1002.json` (joint inventory; not first-match on `2.1`) | **Yes** (on disk; deferred selection — KI-H4) |
| 9 | `CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS` | `campaign_member_certified` | `publication_approved` | Registered as `revision-pca-distributions-cs1002.json` (`CB-R1`) | **Yes** (revision code) |

**Catalogue originals** under `educational_campaigns/` remain `campaign_member_certified` (membership / audit trail). Live student delivery uses the `educational_packages/` copies only.

---

## Activation method (publication pipeline)

1. Copy EC-001-certified package JSON into `app/curriculum/data/educational_packages/cs1/`.  
2. Set `status` = `publication_approved`, `published_at` = `2026-08-01`, and live `publication_version` (`ep001-live-1.0.0` / `cs1002-live-1.0.0`).  
3. Name shared-`topic_code` files so sorted first-match prefers Campaign day order (`1.2.1` → `1.2.2` → `1.2.3`; `2.1.1` → `2.1.2`) without Runtime changes.  
4. Do **not** modify loaders, substance planner, templates, recommendations, or readiness.

---

## Loader verification

| Check | Result |
|-------|--------|
| `EducationalPackageLoader().all_approved()` count | **9** |
| `find_educational_package(topic_code="1.1")` | `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` |
| `find_educational_package(topic_code="1.2")` | `CS1-EP001-PKG-1.2-EDA-SUMMARIES` (day-order first-match) |
| `find_educational_package(topic_code="2.1")` | `CS1-CS1002-PKG-2.1-DISCRETE` (day-order first-match) |
| `find_educational_package(topic_code="4.2")` | `CS1-EA005-PKG-4.2-GLM-STRUCTURE` (EC-001 body) |
| `find_educational_package(topic_code="4.1")` | `None` (control — fallback still correct) |
| `discover_curricula()` | Still syllabi only (`IFOA` CB2/CM1/CS1); **excludes** `educational_packages` / `educational_campaigns` (RC2 hygiene preserved) |

Note: Sprint brief item “verify `discover_curricula()` loads the intended packages” is satisfied as **negative control** — inventory must not register as exams — plus positive control via `EducationalPackageLoader.all_approved()` / `find_educational_package()`.

---

## Residual (honest)

| Residual | Severity | Notes |
|----------|----------|--------|
| KI-H4 shared `topic_code` first-match | Medium | Topics `1.2` and `2.1` deliver the first Campaign-day package only; sibling day packs are jointly published on disk but not selected until day-key / multi-package Runtime support (out of C1 scope). |
| Volume `released` | Ops | Package live-load ≠ Volume EO-001 `released` marketing claim; deploy is next sprint. |
| Deployment | Next sprint | Local tip activation only; LIVE host unchanged until deploy. |

---

## Stop

Publication activation complete for Sprint C1. Deployment belongs to the next sprint.
