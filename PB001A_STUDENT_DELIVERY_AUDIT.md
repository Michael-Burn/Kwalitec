# PB-001A — Student Delivery Audit

**Programme:** PB-001A Educational Release Verification  
**Authority:** EF-001 · EC-001 · RC2 LIVE  
**Classification:** PI-S1  
**Date:** 2026-08-01  
**Method:** Fresh LIVE students; Reading captured via ordinary session UI; compare to certified packages  

**Evidence root:** `knowledge/evidence/releases/PB001A_RC2/`  
**Machine summary:** `knowledge/evidence/releases/PB001A_RC2/results.json`

---

## Audit rule

For every package in the EC-001 inventory:

- **PASS** only if the LIVE student Reading is the certified package body (EC-001 remediated `reading_guidance`), not the fallback LO shell, and Q1–Q6 hold.  
- **FAIL** otherwise (with HTML path).

Screenshots: operator workstation lacked Chromium/Playwright; **HTML captures are authoritative**. Open files under `html/` for visual review (`screenshots/README.md`).

---

## Environment

| Item | Value |
|------|-------|
| Host | https://kwalitec.onrender.com |
| LIVE commit | `0d3fc72137ba0ea51d1baa522c52aa526cf04438` |
| Fingerprint | **PASS** |
| EC-001 content on LIVE | **No** (local uncommitted only) |

---

## Audit rows

### LIVE published

| # | Package | Student path | Captured HTML | Channel | EC-001 match | Verdict |
|---|---------|--------------|---------------|---------|--------------|---------|
| 1 | `CS1-EA005-PKG-4.2-GLM-STRUCTURE` | Enrol → seed leaf 4.2 (existing Baseline API) → Start Session → Reading | `html/study42_reading.html` | Tip `publication_approved` package | No (pre-EC-001 tip) | **FAIL** |

**Justification (FAIL):** Student receives real package Reading (CMP open/stop/focus/exit; not LO shell). Tip strings match deployed JSON. EC-001 remediated lead/exit/return (purpose + named next activity) absent because EC-001 is not on LIVE tip. Q2 and Q6 fail EC-001 bar. See `audits/study42c_42_reading.json`.

**Supporting surfaces:** `html/study42_home.html`, `html/study42_overview.html`.

---

### Catalogue certified (not live-published)

| # | Package | Student path | Captured HTML | Channel | Verdict |
|---|---------|--------------|---------------|---------|---------|
| 2 | `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` | Natural Study 1.1 | `html/study11_reading.html` | Fallback LO shell | **FAIL** |
| 3 | `CS1-EP001-PKG-1.2-EDA-SUMMARIES` | Not reachable as certified pack | — | Not delivered | **FAIL** |
| 4 | `CS1-EP001-PKG-1.2-EDA-ASSOCIATION` | Not reachable as certified pack | — | Not delivered | **FAIL** |
| 5 | `CS1-EP001-PKG-REV-PURPOSE-EDA` | Not reachable as certified pack | — | Not delivered | **FAIL** |
| 6 | `CS1-CS1002-PKG-1.2-PCA` | Not reachable as certified pack | — | Not delivered | **FAIL** |
| 7 | `CS1-CS1002-PKG-2.1-DISCRETE` | Not reachable as certified pack | — | Not delivered | **FAIL** |
| 8 | `CS1-CS1002-PKG-2.1-CONTINUOUS` | Not reachable as certified pack | — | Not delivered | **FAIL** |
| 9 | `CS1-CS1002-PKG-REV-PCA-DISTRIBUTIONS` | Not reachable as certified pack | — | Not delivered | **FAIL** |

**Justification (row 2 FAIL):** Title `Reading: Read the material for 1.1…`; body is LO list only; support is generic LO connective; zero CMP partnership strings. Confirms certified campaign package is not what LIVE serves. Audit: `audits/study11_audit.json`.

**Justification (rows 3–9 FAIL):** Status remains `campaign_member_certified` outside EA-006 live loader (`educational_campaigns/`). No student Reading can be the certified packet until Approver registration as `publication_approved` under `educational_packages/` (and volume release). Delivery absence = FAIL for this programme’s success criteria.

---

## Control observation (not an inventory package)

| Topic | HTML | Result |
|-------|------|--------|
| 4.1 (section-4 continue) | `html/study41_reading_fallback.html` | Fallback LO shell; no CMP — confirms package match is topic-specific |

---

## Checklist recap (LIVE student-visible)

| Check | 1.1 | 4.2 tip | Required for PASS |
|-------|-----|---------|-------------------|
| CMP guidance present | No | Yes | Yes |
| Q1–Q6 complete (EC-001) | 0/6 | 4/6 | 6/6 |
| Correct CMP references | N/A | Yes (tip) | Yes |
| Reading purpose clear | No | Weak / fail EC-001 | Yes |
| Stop condition clear | No | Yes | Yes |
| Immediate next activity named | No | No | Yes |
| No fallback shell | Fail | Pass | Yes |
| Exact EC-001 certified text | No | No | Yes |

---

## Scoreboard

| Class | PASS | FAIL |
|-------|------|------|
| LIVE published packages (n=1) | 0 | **1** |
| Catalogue EC-001 inventory (n=8) | 0 | **8** |
| **Total inventory (n=9)** | **0** | **9** |

---

## F1 / F2 closure gate

| Gate | Status |
|------|--------|
| LIVE student receives EC-001 certified package on exercised path | **Not met** |
| No fallback Reading on paths that should carry certified packs | **Not met** |
| Every Reading shows EC-001 CMP partnership guidance | **Not met** |
| **Close PB-001 F1 and F2?** | **No** |

---

## EF-001 operational note

Observation remains **PI** (delivery / publication activation), severity **S1** for trust claim. Existing Educational Law sufficient; no framework unfreeze. Smallest effective interventions (outside this verification programme): commit+deploy EC-001 package text; Approver + joint activation of catalogue packs onto the live loader / released pathway.

---

## Stop

Student delivery audit complete. Application educational content and Runtime were not modified under PB-001A.
