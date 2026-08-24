# PB009-AUDIT — Confidence Score Root Cause Analysis

**Programme:** PB-009 Progressive Educational Confidence (Campaign Iota)  
**Mission:** Determine exactly why the cohort mean was **8.14 / 9** instead of **9.00 / 9**  
**Authority:** PB-009 PASS · EF-001 Frozen Educational Law · RO-007 PASS WITH RESIDUAL  
**Date:** 2026-08-02  
**Scope:** Reconstruct scoring events only — **no remediation · Wave 8 not started**

---

## Verdict (exit criterion)

# A. The entire 8.14 score is fully explained by existing residuals.

Arithmetic identity:

\[
\frac{12 \times 8 + 2 \times 9}{14} = \frac{114}{14} = 8.142857\ldots \approx \mathbf{8.14}
\]

Every point below 9.00 is produced by **exactly 12** dimension FAILs — all of them `tomorrow_confidence` on Learning days **CI-D1…CI-D6** × **2 personas**. Those FAILs are the same Finish/Home tomorrow-chrome fragment miss already registered as **RO7-R3 / PB9-R2**.

No other dimension failed. No previously unknown issue is required to explain the mean.

---

## Evidence corpus

| Artefact | Role |
|----------|------|
| `knowledge/evidence/releases/PB009/results.json` | Authoritative PB-009 dimension matrix (14 certified sittings) |
| `knowledge/evidence/releases/PB009/personas/first_time.json` | Persona 1 trajectory |
| `knowledge/evidence/releases/PB009/personas/repeat.json` | Persona 2 trajectory |
| `PB009_PROGRESSIVE_CONFIDENCE_REPORT.md` | Residual soft-pass policy; residual register PB9-R1…R3 |
| `knowledge/evidence/releases/RO007/results.json` | Supporting LIVE verify chrome / Q6 residuals |
| `knowledge/evidence/releases/RO007/audits/day41{2–8}_CI-*.json` | Per-day chrome / Q6 observations |
| `RO007_LIVE_VERIFICATION_REPORT.md` / `RO007_RELEASE_DECISION.md` | RO7-R1…R3 definitions |
| `app/curriculum/data/educational_campaigns/cs1/campaign-iota-cs1009/packages/*.json` | Approved package `tomorrow_preview` text (expected chrome) |

PB-009 evidence stores **scores only** (no HTML). Observation quotes for deductions are taken from the RO-007 package-path LIVE verify that PB-009 cites as supporting evidence and that defines RO7-R3.

---

## Scoring law used by PB-009

Nine educational-confidence dimensions (PASS = 1 point toward `/9`):

1. `mission_clarity`  
2. `cmp_partnership`  
3. `educational_confidence`  
4. `session_completion`  
5. `reflection_quality`  
6. `transition_quality`  
7. `tomorrow_confidence`  
8. `trust_retention`  
9. `educational_consistency`  

Residual soft-pass policy (same class as RO-007 / prior PB programmes):

| Residual | Effect on **progressive PASS gate** | Effect on **numeric `/9` score** |
|----------|--------------------------------------|----------------------------------|
| RO7-R3 / PB9-R2 chrome miss on Learning days | Soft-pass (does not fail progressive claim) | **Recorded as FAIL** on `tomorrow_confidence` → **8/9** |
| RO7-R3 chrome miss on CI-R1 | Soft-pass | Soft-passed into **PASS** on `tomorrow_confidence` → contributes to **9/9** |
| RO7-R2 / PB9-R1 revision Q6 on CI-R1 | Soft-pass | No dimension FAIL (revision audit-rubric class) |
| RO7-R1 / PB9-R3 Continuity Front ops label desync | Observed on transit; claim scores only true Iota substance | **Not scored** on CI-D1…CI-R1 matrix |

This matches PB-009’s own statement: Learning days **8/9 typical**; CI-R1 **9/9**; fail-dimension events on educational path after residual policy = **0**.

---

## 1. Reconstructed scoring events

### Persona 1 — First-time candidate (`first_time`)

Email: `pb009.iota.first_time.1785660489@example.com`  
Persona mean: **8.142857 / 9** · trajectory: stable HIGH

| Day | Score | Failing dimension(s) |
|-----|------:|----------------------|
| CI-D1 | 8 | `tomorrow_confidence` |
| CI-D2 | 8 | `tomorrow_confidence` |
| CI-D3 | 8 | `tomorrow_confidence` |
| CI-D4 | 8 | `tomorrow_confidence` |
| CI-D5 | 8 | `tomorrow_confidence` |
| CI-D6 | 8 | `tomorrow_confidence` |
| CI-R1 | 9 | — |

### Persona 2 — Repeat sitting (`repeat`)

Email: `pb009.iota.repeat.1785662601@example.com`  
Persona mean: **8.142857 / 9** · trajectory: stable HIGH

| Day | Score | Failing dimension(s) |
|-----|------:|----------------------|
| CI-D1 | 8 | `tomorrow_confidence` |
| CI-D2 | 8 | `tomorrow_confidence` |
| CI-D3 | 8 | `tomorrow_confidence` |
| CI-D4 | 8 | `tomorrow_confidence` |
| CI-D5 | 8 | `tomorrow_confidence` |
| CI-D6 | 8 | `tomorrow_confidence` |
| CI-R1 | 9 | — |

Identical matrices — no persona-specific divergence.

---

## 2. Full dimension matrix (14 × 9)

Legend: **P** = PASS (1) · **F** = FAIL (0)  
Evidence refs: `PB009/results.json` persona trajectory; chrome observations from RO-007 audits as noted.

### CI-D1

| Dimension | Persona 1 | Persona 2 | Evidence |
|-----------|:---------:|:---------:|----------|
| mission_clarity | P | P | Guided Reading purpose/focus present (`PB009`; RO-007 reading body Syllabus 2.6.1) |
| cmp_partnership | P | P | CMP open / ignore / stop framing; no fallback |
| educational_confidence | P | P | Reading + reflection + finish held |
| session_completion | P | P | Sitting finished |
| reflection_quality | P | P | Reflection loaded / continued |
| transition_quality | P | P | Chain advanced toward CI-D2 |
| tomorrow_confidence | **F** | **F** | RO7-R3 chrome miss — see Deduction D01 |
| trust_retention | P | P | No educational trust drop |
| educational_consistency | P | P | Body matches HR-007 / LIVE inventory |

### CI-D2

| Dimension | P1 | P2 | Evidence |
|-----------|:--:|:--:|----------|
| mission_clarity … educational_consistency (exc. tomorrow) | P | P | Same PASS pattern as CI-D1; body Syllabus 2.6.2 |
| tomorrow_confidence | **F** | **F** | Deduction D02 · RO7-R3 |

### CI-D3

| Dimension | P1 | P2 | Evidence |
|-----------|:--:|:--:|----------|
| (8 non-tomorrow dimensions) | P | P | Body Syllabus 2.6.3 |
| tomorrow_confidence | **F** | **F** | Deduction D03 · RO7-R3 |

### CI-D4

| Dimension | P1 | P2 | Evidence |
|-----------|:--:|:--:|----------|
| (8 non-tomorrow dimensions) | P | P | Body Syllabus 2.6.4 |
| tomorrow_confidence | **F** | **F** | Deduction D04 · RO7-R3 |

### CI-D5

| Dimension | P1 | P2 | Evidence |
|-----------|:--:|:--:|----------|
| (8 non-tomorrow dimensions) | P | P | Body Syllabus 2.6.5 (`day416_CI-D5_reading.html` / audit) |
| tomorrow_confidence | **F** | **F** | Deduction D05 · RO7-R3 (`day416_CI-D5_audit.json`: `chrome_residual: true`) |

### CI-D6

| Dimension | P1 | P2 | Evidence |
|-----------|:--:|:--:|----------|
| (8 non-tomorrow dimensions) | P | P | Body Syllabus 2.6.6 |
| tomorrow_confidence | **F** | **F** | Deduction D06 · RO7-R3 |

### CI-R1

| Dimension | P1 | P2 | Evidence |
|-----------|:--:|:--:|----------|
| mission_clarity | P | P | Revision CMP retrieval clear |
| cmp_partnership | P | P | Targeted CMP reopen framing; no fallback |
| educational_confidence | P | P | Revision + reflection + finish held |
| session_completion | P | P | Sitting finished |
| reflection_quality | P | P | Reflection OK |
| transition_quality | P | P | Certified Iota arc completed |
| tomorrow_confidence | **P** | **P** | Soft-pass of RO7-R3 on revision day (numeric PASS; residual still open) |
| trust_retention | P | P | No mid-sequence educational trust drop |
| educational_consistency | P | P | Matches `…-REV-SAMPLING-DISTRIBUTIONS` |

**Note:** CI-R1 also carries **RO7-R2** (Q6 Learning-oriented checklist). Soft-pass → no dimension FAIL → does not reduce the `/9` score.

---

## 3. Deduction register (all 12 FAILs)

Shared observation class (RO-007 Finish/Home after true Iota sittings):

> Finish/Home tomorrow chrome did **not** match approved package `tomorrow_preview` fragments.  
> Fragment checks: `next_topic_code=false`, `continuity_fragment=false`, `student_facing_fragment=false`, `chrome_matches_package_continuity=false`, `tomorrow_chrome_matches_approved=false`, `chrome_residual=true`.

Representative Home chrome (post-sitting), quoted from RO-007 certified-day records (e.g. CI-D1 / CI-D5 / CI-R1 audits):

> “Today's Mission Relate sample-mean and sample-variance moments to the population … Study 3.1 — Construct estimators and discuss their properties After this · Study Progress for sample-mean/variance moments — not 2.6.4.”

Approved package tomorrow text that chrome failed to surface (examples):

| Day | Approved `student_facing` (catalogue) |
|-----|----------------------------------------|
| CI-D1 | “Tomorrow: sampling distribution of a statistic (2.6.2). Optional light prep: skim 2.6.2 headings — titles only tonight.” |
| CI-D2 | “Tomorrow: mean/variance of sample mean and mean of sample variance (2.6.3). …” |
| CI-D3 | “Tomorrow: basic Normal sampling distributions for mean and variance (2.6.4). …” |
| CI-D4 | “Tomorrow: t-statistic for random samples from a Normal (2.6.5). …” |
| CI-D5 | “Tomorrow: F distribution for the ratio of two sample variances (2.6.6). …” |
| CI-D6 | “Tomorrow: Campaign Iota Revision (retrieve 2.6.1–2.6.6). …” |

| ID | Day | Persona | Dimension | Observation (exact class) | EF-001 class | Residual coverage |
|----|-----|---------|-----------|---------------------------|--------------|-------------------|
| D01a | CI-D1 | Persona 1 | tomorrow_confidence | Chrome fragment miss vs approved 2.6.2 tomorrow text; Home after-finish misaligned | **PI** | **RO7-R3** / PB9-R2 |
| D01b | CI-D1 | Persona 2 | tomorrow_confidence | Same | **PI** | **RO7-R3** / PB9-R2 |
| D02a | CI-D2 | Persona 1 | tomorrow_confidence | Same class | **PI** | **RO7-R3** / PB9-R2 |
| D02b | CI-D2 | Persona 2 | tomorrow_confidence | Same class | **PI** | **RO7-R3** / PB9-R2 |
| D03a | CI-D3 | Persona 1 | tomorrow_confidence | Same class | **PI** | **RO7-R3** / PB9-R2 |
| D03b | CI-D3 | Persona 2 | tomorrow_confidence | Same class | **PI** | **RO7-R3** / PB9-R2 |
| D04a | CI-D4 | Persona 1 | tomorrow_confidence | Same class | **PI** | **RO7-R3** / PB9-R2 |
| D04b | CI-D4 | Persona 2 | tomorrow_confidence | Same class | **PI** | **RO7-R3** / PB9-R2 |
| D05a | CI-D5 | Persona 1 | tomorrow_confidence | Same class (`day416_CI-D5_audit.json` `chrome_residual: true`) | **PI** | **RO7-R3** / PB9-R2 |
| D05b | CI-D5 | Persona 2 | tomorrow_confidence | Same class | **PI** | **RO7-R3** / PB9-R2 |
| D06a | CI-D6 | Persona 1 | tomorrow_confidence | Same class | **PI** | **RO7-R3** / PB9-R2 |
| D06b | CI-D6 | Persona 2 | tomorrow_confidence | Same class | **PI** | **RO7-R3** / PB9-R2 |

**Count:** 12 / 12 deductions → **RO7-R3**.  
**NEW findings:** **0**.

### Soft-passed residuals that did **not** create numeric deductions

| Residual | Observation | EF-001 | Why not in 8.14 gap |
|----------|-------------|--------|---------------------|
| **RO7-R2** / PB9-R1 | CI-R1 checklist Q6 Learning-oriented (`Q6_next: false`; `revision_q6_residual: true`) | **PI** (presentation / audit rubric) | Soft-pass; CI-R1 scored 9/9 |
| **RO7-R3** on CI-R1 | Chrome miss also recorded on CI-R1 in RO-007 | **PI** | Soft-pass into `tomorrow_confidence` PASS on revision day |
| **RO7-R1** / PB9-R3 | Continuity Front ops label desync on transit | **PI** | Progressive claim scores only true Iota substance days; no CI-* dimension FAIL attributed to R1 |

EF-001 check: all observations resolve as **PI** (product implementation / chrome / presentation). None require **EC / AW / RB / EF**. None require unfreezing Educational Law.

---

## 4. Aggregates

### Per-dimension averages (PASS rate across 14 sittings)

| Dimension | PASS count | Average |
|-----------|----------:|--------:|
| mission_clarity | 14 / 14 | **1.000** |
| cmp_partnership | 14 / 14 | **1.000** |
| educational_confidence | 14 / 14 | **1.000** |
| session_completion | 14 / 14 | **1.000** |
| reflection_quality | 14 / 14 | **1.000** |
| transition_quality | 14 / 14 | **1.000** |
| tomorrow_confidence | 2 / 14 | **0.143** |
| trust_retention | 14 / 14 | **1.000** |
| educational_consistency | 14 / 14 | **1.000** |

Only `tomorrow_confidence` is below 1.0. Its 12 FAILs are the entire mean gap.

### Per-persona averages

| Persona | Certified days | Mean `/9` |
|---------|---------------:|----------:|
| Persona 1 (`first_time`) | 7 | **8.142857** |
| Persona 2 (`repeat`) | 7 | **8.142857** |
| Cohort | 14 | **8.142857 ≈ 8.14** |

### Per-day averages (both personas)

| Day | Sittings | Scores | Mean `/9` | Driver |
|-----|---------:|--------|----------:|--------|
| CI-D1 | 2 | 8, 8 | **8.00** | RO7-R3 → tomorrow FAIL |
| CI-D2 | 2 | 8, 8 | **8.00** | RO7-R3 |
| CI-D3 | 2 | 8, 8 | **8.00** | RO7-R3 |
| CI-D4 | 2 | 8, 8 | **8.00** | RO7-R3 |
| CI-D5 | 2 | 8, 8 | **8.00** | RO7-R3 |
| CI-D6 | 2 | 8, 8 | **8.00** | RO7-R3 |
| CI-R1 | 2 | 9, 9 | **9.00** | Soft-pass R2/R3 |

---

## 5. Root cause summary

1. **What failed numerically:** only `tomorrow_confidence` on Learning days CI-D1…CI-D6 (12 events).  
2. **What that failure is:** Finish/Home chrome does not bind approved package `tomorrow_preview` text after Iota sittings (fragment miss + misaligned After-this / next-mission chrome).  
3. **Prior registration:** RO-007 residual **RO7-R3** (“Tomorrow chrome fragment miss on some Iota days (incl. CI-R1)”), mirrored as **PB9-R2**.  
4. **Why not 9.00:** PB-009 records Learning-day chrome miss as a hard FAIL on the numeric dimension while soft-passing it for the progressive claim gate — producing stable HIGH at **8/9** on six Learning days and **9/9** on CI-R1.  
5. **What did not move the mean:** RO7-R2 (Q6) and RO7-R1 (ops label desync) — present as residuals, soft-passed / out of Iota substance scoring, **zero** numeric FAILs attributed to them.  
6. **EF-001:** classification **PI**; Smallest Effective Intervention would be chrome/presentation binding under existing Educational Law — **out of scope for this audit**.

### Residual coverage check

| Residual | Explains any of the 12 FAILs? | Notes |
|----------|-------------------------------|-------|
| RO7-R1 | No | Transit / selection presentation; not the scored Iota dimension fails |
| RO7-R2 | No | CI-R1 only; soft-passed; CI-R1 = 9/9 |
| RO7-R3 | **Yes — all 12** | Learning-day chrome miss = entire 8.14 gap |
| NEW | **None** | — |

---

## 6. Exit conclusion

> **The entire 8.14 score is fully explained by existing residuals.**

Specifically: **RO7-R3 / PB9-R2** (tomorrow chrome fragment miss on Learning days CI-D1…CI-D6), under PB-009’s numeric scoring of that residual as `tomorrow_confidence` FAIL.

No previously unknown issue has been identified.  
No remediation implemented.  
Wave 8 not started.

---

Signed: PB009-AUDIT · Confidence Score Root Cause Analysis · 2026-08-02  
**Conclusion: A**
