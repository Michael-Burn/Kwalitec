# PB-001A — CMP Partnership Verification

**Programme:** PB-001A Educational Release Verification  
**Authority:** EF-001 · EC-001 partnership standard (Q1–Q6) · RC2 LIVE  
**Date:** 2026-08-01  
**Unit of check:** What the LIVE student actually sees on the Reading activity  

Companion reports: `PB001A_LIVE_EDUCATIONAL_DELIVERY_REPORT.md`, `PB001A_STUDENT_DELIVERY_AUDIT.md`.

---

## Partnership bar (from EC-001)

A diligent student on Guided Reading must know:

| ID | Question |
|----|----------|
| Q1 | Exactly what CMP material to open |
| Q2 | Educational purpose of this reading / revision |
| Q3 | What to pay attention to |
| Q4 | What to ignore (if applicable) |
| Q5 | How to know they are finished |
| Q6 | What in-app activity follows immediately |

---

## Method

1. Enrol fresh LIVE students on RC2 tip `0d3fc721…`.  
2. Reach Reading via Start Session (natural UI).  
3. Capture HTML.  
4. Score Q1–Q6 against the **EC-001** bar (not merely “any CMP mention”).  
5. Separately note whether the body is the tip package, EC-001 certified text, or fallback shell.

---

## Results

### A. Study 1.1 (natural path) — **FAIL**

**HTML:** `knowledge/evidence/releases/PB001A_RC2/html/study11_reading.html`  
**Channel:** Fallback LO shell (certified 1.1 package not live-loaded)

| Q | Verdict | LIVE evidence |
|---|---------|---------------|
| Q1 | **FAIL** | No “Open your CMP” / edition+locus instruction |
| Q2 | **FAIL** | No purpose-of-reading framing; generic “Read the material…” |
| Q3 | **FAIL** | No focus questions / misconception watch / annotation |
| Q4 | **FAIL** | No ignore / out-of-scope list |
| Q5 | **FAIL** | No stop condition / finished criteria |
| Q6 | **FAIL** | No named next activity |

**CMP guidance present?** **No.**  
**Overall:** **FAIL**

This is the same LIVE failure class as PB-001 F1/F2.

---

### B. Study 4.2 (sole LIVE `publication_approved` package) — **FAIL** vs EC-001 bar

**HTML:** `knowledge/evidence/releases/PB001A_RC2/html/study42_reading.html`  
**Channel:** Tip `publication_approved` package (not fallback)  
**Matches EC-001 certified strings?** **No** (EC-001 uncommitted / not deployed)  
**Matches LIVE tip package strings?** **Yes**

| Q | Verdict | LIVE evidence |
|---|---------|---------------|
| Q1 | **PASS** | Support: “Open your CMP at the GLM setup for Syllabus 4.2…”; body `Open: CMP · Syllabus 4.2 GLM setup (4.2.1–4.2.3 centre)` |
| Q2 | **FAIL** | Tip lead lacks EC-001 “Purpose of this reading:…” framing |
| Q3 | **PASS** | Focus questions + misconception watch present in body |
| Q4 | **PASS** | Out-of-scope / ignore list present |
| Q5 | **PASS** | Stop condition + return cue present (tip wording) |
| Q6 | **FAIL** | Tip exit/return does not name Worked-example re-entry → Knowledge Checks |

**CMP guidance present?** **Yes** (open CMP + locus).  
**Correct CMP references?** **Yes** for tip copy (Syllabus 4.2 / 4.2.1–4.2.3).  
**Reading purpose clear (EC-001 bar)?** **No.**  
**Stop condition clear?** **Yes** (tip).  
**Immediate next activity named (EC-001 bar)?** **No.**  

**Overall vs EC-001:** **FAIL**  
**Overall vs “any package Reading”:** Tip package **is** delivered (important activation fact; still insufficient for F1/F2 close).

---

### C. Catalogue packages (1.2… / CS1-002) — **FAIL** (not delivered)

No LIVE student Reading was obtained from certified campaign packages because they are not in the live loader. Partnership verification on a non-delivered packet is **FAIL** by delivery absence.

Desk EC-001 content PASS (inventory) remains valid for **authored JSON**, not for LIVE student surface.

---

### D. Control — Study 4.1 — **FAIL** (fallback)

**HTML:** `knowledge/evidence/releases/PB001A_RC2/html/study41_reading_fallback.html`  
Confirms adjacent topic without `publication_approved` package → LO shell, zero CMP partnership strings.

---

## Summary table

| Surface | CMP present | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Verdict |
|---------|-------------|----|----|----|----|----|----|---------|
| LIVE 1.1 Reading | No | F | F | F | F | F | F | **FAIL** |
| LIVE 4.2 Reading (tip) | Yes | P | F | P | P | P | F | **FAIL** |
| LIVE 4.1 Reading | No | F | F | F | F | F | F | **FAIL** |
| Catalogue EC-001 packs on LIVE | — | — | — | — | — | — | — | **FAIL** (not delivered) |

---

## Implication for PB-001 F1 / F2

| Finding | Still open? |
|---------|-------------|
| F1 — No CMP direction on early spine | **Yes** (1.1) |
| F2 — Empty Reading shell | **Yes** (1.1; also 4.1) |
| 4.2 tip shows CMP can appear when a live package matches | Observed — does **not** close F1/F2 for the student-default path |

F1/F2 may close only after: (1) EC-001 content is committed and deployed, and (2) early-spine packages are live-published / activated so natural enrolment no longer hits the fallback shell.

---

## Stop

CMP partnership verification complete for PB-001A. No content or Runtime changes.
