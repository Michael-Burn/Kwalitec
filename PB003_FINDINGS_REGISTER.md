# PB-003 — Findings Register

**Programme:** PB-003 Progressive Educational Confidence Certification  
**Authority:** EF-001 Operational Review Template  
**Date:** 2026-08-01  
**Rule:** Never recommend engineering changes before EF-001 classification.  
**Evidence:** `knowledge/evidence/releases/PB003/`  

---

## Register summary

| Class | Count on LIVE-certified path | Blocks progressive PASS? |
|-------|------------------------------|--------------------------|
| S1 educational | **0** | — |
| S2 educational | **0** | — |
| S3 educational | **0** | — |
| Ops / harness only | Recorded below | **No** |

**Progressive confidence claim:** not blocked.  
**EF-001 unfreeze:** not indicated.

---

## Educational findings (LIVE-certified inventory)

None.

All 40 certified day-observations (8 personas × CG-D1…CG-R1) scored **PASS** on all nine PB-003 dimensions after tomorrow-chrome text was read from the visible Finish block (RO1-R1 `data-tomorrow-preview="true"` attribute carries a boolean, not the copy).

---

## Ops / harness observations (not student educational defects)

### PB003-OPS-01 — Transient LIVE connection resets

1. **Observation:** Occasional `Connection reset by peer` / curl rc=28 during Render job poll or Baseline POST.  
2. **Classification:** PI (ops connectivity) — not educational content.  
3. **Severity:** S3 for programme execution; **N/A** for student LIVE-certified trust once session completes.  
4. **Evidence:** `/tmp/pb003/remaining2.log` weak_math first attempt; provision curl retries.  
5. **Smallest Effective Intervention:** Retry with backoff (executed in harness).  
6. **EF-001 Check:** **YES** — no Educational Framework change.

### PB003-OPS-02 — Invalid harness session-minute radio

1. **Observation:** Posting `preferred_session_minutes=75` yields wizard flash “Not a valid choice.” Allowed radios: 30 / 45 / 60 / 90 / 120.  
2. **Classification:** PI (harness input) — student UI uses fixed radios.  
3. **Severity:** S3 ops; **N/A** for certified educational trust.  
4. **Evidence:** `/tmp/pb003/html/weak_math_diligent/wizard3.html` (first failed enrol).  
5. **SEI:** Coerce harness values to allowed radio set (executed).  
6. **EF-001 Check:** **YES**.

### PB003-OPS-03 — Tomorrow chrome attribute vs visible text

1. **Observation:** Finish HTML sets `data-tomorrow-preview="true"`; approved tomorrow wording appears in the visible Tomorrow block and matches package `student_facing`.  
2. **Classification:** PI (presentation attribute shape) — educational honesty **PASS** after reading visible text.  
3. **Severity:** S3 for automation parsers; student-visible honesty **PASS** (RO1-R1).  
4. **Evidence:** Finish HTML under `/tmp/pb003/html/*/day*_finish.html`; rescored persona JSON.  
5. **SEI:** Auditors/harnesses should match visible tomorrow copy (or package id), not assume attribute holds the sentence. Optional future: put text in a dedicated data attribute — only if product wants parser convenience.  
6. **EF-001 Check:** **YES** — do not reopen Educational Framework; RO1-R1 already closed chrome honesty.

---

## Explicit non-findings (scope)

| Topic | Status |
|-------|--------|
| Reflection 500 (PB-001 F6) | **Not reproduced** on certified days |
| Fallback Reading without CMP (PB-001 F7) | **Absent** on CG-D1…CG-R1 |
| Tomorrow chrome first-match residual (RO1-R1) | **Closed** — matches package text |
| Unpublished exam-path continuity | **Out of scope** — not evaluated |
| Wave 0 Approver honesty gap | **Pre-existing governance** — not a PB-003 certified-day defect |

---

## EF-001 check (programme-level)

> Can progressive educational confidence on the LIVE-certified inventory be affirmed without modifying the frozen Educational Framework?

**YES.**

---

Signed: PB-003 Findings Register · 2026-08-01 · **0 educational S1/S2 on certified path**
