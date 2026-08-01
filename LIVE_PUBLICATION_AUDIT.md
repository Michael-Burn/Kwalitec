# LIVE_PUBLICATION_AUDIT.md

**Programme:** VERSION1-RC2 — Sprint C1 — Educational Publication Activation  
**Authority:** EF-001 · EC-001 · PB-001A delivery bar  
**Date:** 2026-08-01  
**Method:** Local tip loader + substance planner resolution after publication registration (pre-deploy)  
**Companion:** `PUBLICATION_ACTIVATION_REPORT.md`

---

## Audit rule

For each published topic that should carry an EC-001 certified package:

| Field | Meaning |
|-------|---------|
| **Expected Reading** | EC-001 certified Guided Reading (`reading_guidance` partnership packet) |
| **Delivered Reading** | What `find_educational_package` / substance planner resolves **on this tip** |
| **Package Source** | On-disk live path under `educational_packages/` |
| **Fallback?** | Yes only if LO shell / no package match |

**PASS** when Delivered Reading is the certified package body (not fallback). Shared-`topic_code` day selection is noted where KI-H4 applies.

---

## Environment

| Item | Value |
|------|-------|
| Scope | Local tip after Sprint C1 registration (not yet redeployed to Render) |
| Loader root | `app/curriculum/data/educational_packages/` |
| Catalogue root (unchanged membership) | `app/curriculum/data/educational_campaigns/` |
| Approved live packages | **9** |

---

## Audit rows — published topics

| Expected Reading | Delivered Reading | Package Source | Fallback? |
|------------------|-------------------|----------------|-----------|
| EC-001 Guided Reading for `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` (Q1–Q6 CMP partnership) | Same package; lead opens with “Purpose of this reading…”; exit/return name Worked-example → Knowledge Checks | `educational_packages/cs1/1.1-purpose-function-ep001.json` | **No** |
| EC-001 Guided Reading for topic **1.2** Campaign day (summaries / association / PCA) | **First-match:** `CS1-EP001-PKG-1.2-EDA-SUMMARIES` (EC-001 body). Association + PCA packs are live-registered but not selected on bare `topic_code=1.2` | `…/1.2.1-eda-summaries-ep001.json` (selected); siblings `1.2.2-…`, `1.2.3-…` on disk | **No** (package, not LO shell) |
| EC-001 Guided Reading for topic **2.1** Campaign day (discrete / continuous) | **First-match:** `CS1-CS1002-PKG-2.1-DISCRETE` (EC-001 body). Continuous pack live-registered but not selected on bare `topic_code=2.1` | `…/2.1.1-discrete-cs1002.json` (selected); sibling `2.1.2-…` on disk | **No** |
| EC-001 Guided Reading for `CS1-EA005-PKG-4.2-GLM-STRUCTURE` | Same package with EC-001 remediated lead/exit/return (purpose + named next activity) | `educational_packages/cs1/4.2-glm-structure-ea006.json` | **No** |
| EC-001 Revision Reading `CS1-EP001-PKG-REV-PURPOSE-EDA` when topic resolves `CA-R1` | Same revision package | `…/revision-purpose-eda-ep001.json` | **No** |
| EC-001 Revision Reading `CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS` when topic resolves `CB-R1` | Same revision package | `…/revision-pca-distributions-cs1002.json` | **No** |

---

## Control — unpublished adjacent topic

| Expected Reading | Delivered Reading | Package Source | Fallback? |
|------------------|-------------------|----------------|-----------|
| No certified package for topic **4.1** | `find_educational_package(topic_code="4.1")` → `None` → Runtime C LO shell path remains | — | **Yes** (correct) |

---

## Per-package delivery matrix

| Package | Expected on student path? | Delivered when? | Fallback? |
|---------|---------------------------|-----------------|-----------|
| `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` | Yes — natural Study **1.1** | Always on `topic_code=1.1` | No |
| `CS1-EP001-PKG-1.2-EDA-SUMMARIES` | Yes — Study **1.2** (day-1 preference) | First-match on `1.2` | No |
| `CS1-EP001-PKG-1.2-EDA-ASSOCIATION` | Joint inventory day | On disk; not selected for bare `1.2` (KI-H4) | N/A (not selected; not fallback) |
| `CS1-CS1002-PKG-1.2-PCA` | Joint inventory day | On disk; not selected for bare `1.2` (KI-H4) | N/A |
| `CS1-CS1002-PKG-2.1-DISCRETE` | Yes — Study **2.1** (day-1 preference) | First-match on `2.1` | No |
| `CS1-CS1002-PKG-2.1-CONTINUOUS` | Joint inventory day | On disk; not selected for bare `2.1` (KI-H4) | N/A |
| `CS1-EA005-PKG-4.2-GLM-STRUCTURE` | Yes — Study **4.2** | Always on `topic_code=4.2` | No |
| `CS1-EP001-PKG-REV-PURPOSE-EDA` | Revision `CA-R1` | When topic code/alias is `CA-R1` | No |
| `CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS` | Revision `CB-R1` | When topic code/alias is `CB-R1` | No |

---

## Comparison to PB-001A LIVE failure class

| PB-001A observation | Post-C1 tip (pre-deploy) |
|---------------------|--------------------------|
| Study **1.1** → fallback LO shell | **Closed on tip** — package Reading |
| Catalogue packs not in live loader | **Closed** — 8 campaign packs registered + 4.2 EC-001 body |
| Study **4.2** tip package without EC-001 strings | **Closed on tip** — EC-001 `reading_guidance` in live JSON |
| Study **4.1** → fallback | **Still correct** — no package |

F1/F2 **LIVE host** closure still requires the next sprint’s deploy + fingerprint re-test.

---

## Scoreboard (tip)

| Class | PASS | Notes |
|-------|------|-------|
| Topics with unique live package (`1.1`, `4.2`, revisions) | **PASS** | Exact certified package |
| Topics with shared `topic_code` (`1.2`, `2.1`) | **PASS vs fallback** | Certified package delivered; day siblings deferred (KI-H4) |
| Control `4.1` | **PASS** | Fallback intentional |

---

## Stop

Live publication audit complete for Sprint C1 tip. No Runtime changes. Deploy deferred.
