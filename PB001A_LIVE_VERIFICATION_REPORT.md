# PB-001A — LIVE Verification Report (Sprint D)

**Programme:** PB-001A LIVE Educational Trust Verification (post Sprint C1 deploy)  
**Authority:** EF-001 · EC-001 PASS · RC2 Sprint C1 PASS · Sprint D deploy  
**Classification:** PI-S1  
**Host:** https://kwalitec.onrender.com  
**LIVE commit:** `94e02f57669831ff6af4e6f6bf87a727ca0cfe38` (fingerprint **PASS**)  
**Deploy:** `dep-d9ms5o6417fc73c3v1h0`  
**Date:** 2026-08-01  
**Nature:** Verification only — educational content and Runtime intentionally unmodified  

**Evidence:** `knowledge/evidence/releases/RC2_SPRINT_D/`  
**Prior FAIL baseline:** `PB001A_LIVE_EDUCATIONAL_DELIVERY_REPORT.md` (tip `0d3fc721`)

---

## Verdict

# **PASS — EC-001 certified packages reach LIVE students on published topics**

| Gate | Result |
|------|--------|
| LIVE fingerprint matches Sprint C1 tip | **PASS** |
| LIVE approved package inventory = 9 | **PASS** |
| Published-topic Reading = certified Guided Reading (not fallback) | **PASS** |
| CMP partnership checklist (purpose / focus / ignore / stop / next) | **PASS** |
| Control topic 4.1 remains fallback | **PASS** |
| PB-001 F1 / F2 closable | **Yes** |

---

## Scope reminder

This programme does **not** author content, redesign Runtime, or review Educational Framework law. It proves whether certified packages are the exact Reading a LIVE student receives after Sprint C1 publication activation is deployed.

---

## LIVE published inventory

EA-006 live loader scans `app/curriculum/data/educational_packages/**/*.json` with status `publication_approved` / `approved` / `certified`.

Asserted on LIVE via Render job `job-d9ms9qu417fc73c487p0` (**succeeded**):

| Package ID | topic_code | Student-reachable |
|------------|------------|-------------------|
| `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` | 1.1 | **Yes** |
| `CS1-EP001-PKG-1.2-EDA-SUMMARIES` | 1.2 | **Yes** (first-match) |
| `CS1-EP001-PKG-1.2-EDA-ASSOCIATION` | 1.2 | On disk; KI-H4 not selected on bare `1.2` |
| `CS1-CS1002-PKG-1.2-PCA` | 1.2 | On disk; KI-H4 not selected on bare `1.2` |
| `CS1-CS1002-PKG-2.1-DISCRETE` | 2.1 | **Yes** (first-match) |
| `CS1-CS1002-PKG-2.1-CONTINUOUS` | 2.1 | On disk; KI-H4 not selected on bare `2.1` |
| `CS1-EA005-PKG-4.2-GLM-STRUCTURE` | 4.2 | **Yes** (EC-001 body) |
| `CS1-EP001-PKG-REV-PURPOSE-EDA` | CA-R1 | Loader **Yes**; campaign day (not Baseline leaf) |
| `CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS` | CB-R1 | Loader **Yes**; campaign day (not Baseline leaf) |

**Count of LIVE published CS1 packages: 9.**

---

## Per-topic LIVE delivery results

### 1. `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` — **PASS**

| Field | Detail |
|-------|--------|
| Student | Fresh Internal Alpha (`rc2d.study11c.*`) |
| Path | Natural Choose Exam → Baseline start → Study **1.1** → Reading (no ops seed) |
| HTML | `knowledge/evidence/releases/RC2_SPRINT_D/html/study11_reading.html` |
| Delivery channel | **publication_approved package** (not fallback) |
| EC-001 certified strings | **Yes** — purpose lead, CMP open, focus, ignore, stop, Worked-example → Knowledge Checks |
| Fallback shell? | **No** |
| Verdict | **PASS** |

Confirming capture (`rc2d.study11b.*` after `seed_declared_position(1.1)`): same certified body — `html/study11_seeded_reading.html`.

### 2. `CS1-EP001-PKG-1.2-EDA-SUMMARIES` — **PASS** (KI-H4 first-match)

| Field | Detail |
|-------|--------|
| Student | `rc2d.study12.*` |
| Path | Enrol → `seed_declared_position(1.2)` → Reading |
| HTML | `html/study12_reading.html` |
| Delivery channel | publication_approved package |
| Fallback shell? | **No** |
| Verdict | **PASS** |

### 3. `CS1-CS1002-PKG-2.1-DISCRETE` — **PASS** (KI-H4 first-match)

| Field | Detail |
|-------|--------|
| Student | `rc2d.study21.*` |
| Path | Enrol → `seed_declared_position(2.1)` → Reading |
| HTML | `html/study21_reading.html` |
| Delivery channel | publication_approved package |
| Fallback shell? | **No** |
| Verdict | **PASS** |

### 4. `CS1-EA005-PKG-4.2-GLM-STRUCTURE` — **PASS** (EC-001 remediated)

| Field | Detail |
|-------|--------|
| Student | `rc2d.study42.*` |
| Path | Enrol → `seed_declared_position(4.2)` → Reading |
| HTML | `html/study42_reading.html` |
| Delivery channel | publication_approved package with EC-001 purpose / next-activity framing |
| Fallback shell? | **No** |
| Verdict | **PASS** |

### 5–6. Revision packs CA-R1 / CB-R1 — **PASS** (loader)

Baseline `seed_declared_position` does not accept campaign day codes (ops jobs failed as expected). LIVE loader inventory assert confirms both packages resolve. Student Reading path requires campaign progression (out of Baseline leaf API).

### Control: topic 4.1 — fallback confirmed — **PASS**

| Field | Detail |
|-------|--------|
| Student | `rc2d.study41.*` |
| HTML | `html/study41_reading_fallback.html` |
| Delivery channel | Fallback LO shell |
| Verdict | **PASS** (correct absence of package) |

---

## Reading checklist (published student paths)

For each of 1.1 / 1.2 / 2.1 / 4.2:

| Check | Result |
|-------|--------|
| CMP reference present | ✓ |
| Educational purpose clear | ✓ |
| Reading focus clear | ✓ |
| Ignore guidance present | ✓ |
| Stop condition explicit | ✓ |
| Immediate next activity named | ✓ |

---

## Comparison to prior PB-001A FAIL

| Prior observation (tip `0d3fc721`) | Sprint D LIVE (`94e02f5`) |
|------------------------------------|---------------------------|
| Only 4.2 live-published; pre-EC-001 body | 9 packs; 4.2 carries EC-001 remediation |
| Study 1.1 → fallback LO shell | Study 1.1 → certified Guided Reading |
| Catalogue packs not in live loader | Campaign packs jointly `publication_approved` |
| F1/F2 open | **Closable** |

---

## Commit fingerprint

```text
GET /health → commit=94e02f57669831ff6af4e6f6bf87a727ca0cfe38
GET /health/ready → ready=true; migrations current=head=202607310002
```

---

## Screenshots

Playwright/Chrome unavailable on the operator workstation. HTML under `knowledge/evidence/releases/RC2_SPRINT_D/html/` is authoritative. Notes in `screenshots/`.

---

## Success criteria assessment

| Criterion | Met? |
|-----------|------|
| LIVE student receives the EC-001 certified educational package on published topics | **Yes** |
| No fallback Reading shell on paths that should carry certified packs | **Yes** |
| Every published Reading demonstrates CMP partnership authored in EC-001 | **Yes** (spine paths + loader for revisions) |

**PB-001 F1 and F2 can close.** Full cohort adversarial PB-001 rerun is authorised on this tip.

---

## Completion report sections

### Summary
Post-deploy LIVE walks prove EC-001 certified Guided Reading reaches students on published topics 1.1, 1.2, 2.1, and 4.2; control 4.1 remains fallback; inventory asserts nine live packages. F1/F2 closable.

### Files Created
- `PB001A_LIVE_VERIFICATION_REPORT.md`
- `knowledge/evidence/releases/RC2_SPRINT_D/**`

### Files Modified
None (application / curriculum on LIVE tip untouched by this verification).

### Tests Executed
LIVE black-box enrolment + Reading capture (not pytest). Fingerprint + inventory assert.

### Migration Impact
None.

### Architecture Compliance
Observed delivery matches EA-006 loader contract. V1/V2 curriculum engine not altered.

### Technical Debt
None introduced. Residual KI-H4 day-key selection; revision campaign days not Baseline-seedable.

### Known Limitations
- Leaf topics beyond section picker used existing `seed_declared_position` ops API (same as prior PB-001A).  
- Screenshot PNGs not generated.  
- Application code and educational content not modified (mandate).

### Student Impact Assessment
- **Student problem (prior):** Empty / non-partnership Reading on LIVE.  
- **Student benefit:** Certified CMP partnership packet now delivered on published LIVE topics.  
- **Learning benefit:** Official CMP use is instructed, not improvised.  
- **Success metrics:** Checklist PASS on published Reading; F1/F2 closed; PB-001 rerun authorised.  
- **Risks:** KI-H4 sibling-day surprise; campaign revision path not exercised end-to-end in this sprint.  
- **Assumptions:** CS1 CMP remains authoritative external text.

### Estimated KSI contribution
ΔKSI = 0 (verification evidence only).

### Evidence collected
`knowledge/evidence/releases/RC2_SPRINT_D/` (`results.json`, `html/`, `audits/`, health snapshots).

### Lessons learned for student value
Deployed publication registration converts EC-001 certification into student-visible Guided Reading. Fingerprint-matched LIVE HTML is the trust evidence.

### Explainability Review
N/A — no intelligence change.

### Recommendation Quality Review
N/A — no ranking change.

### Version 1 readiness residual
Educational delivery LIVE gate cleared for F1/F2; full PB-001 claim re-test remains.

### CRI domains / ΔCRI
ΔCRI = 0 (verification; board update deferred to PB-001 rerun).

---

## Stop

PB-001A LIVE verification (Sprint D) complete. Do not modify educational content or Runtime under this mission ID.
