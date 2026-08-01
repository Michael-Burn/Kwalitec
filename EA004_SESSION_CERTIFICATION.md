# EA-004 — Session Certification

**Programme:** Educational Excellence Programme EA-004  
**Status:** Binding — Study Session lifecycle review and certification  
**Effective:** 2026-08-01  
**Parent:** `EA004_SESSION_BLUEPRINT.md` · `EA004_STUDY_SESSION_FLOW.md` · `EA004_READING_GUIDANCE_ARCHITECTURE.md` · `EA004_SESSION_SCORING_RUBRIC.md`  
**Related:** Gate SS · Gate LE · `EA002_CERTIFICATION_WORKFLOW.md` · `EA002_PUBLICATION_WORKFLOW.md` · `EA001_QUALITY_GATES.md` · EA-003 Mission Certification (joint)  
**Nature:** Process law — not educational content, not application code  

---

## 1. Purpose

Define how a Study Session moves from inputs to retirement — and the measurable quality gates that reject unfit Sessions before students see them.

EA-001 defines Gate SS / Gate LE (what PASS means).  
EA-002 defines multi-stage certification for all artefact classes (AF-SS).  
EA-003 requires joint Mission + Session certification.  
**EA-004 specialises the Session lifecycle and Session-only reject criteria** so Session quality can be objectively reviewed.

> **A single failed stage blocks publication.**

---

## 2. Session lifecycle

```text
INPUTS
  → AUTHORING
    → EDUCATIONAL REVIEW
      → TUTOR REVIEW
        → CERTIFICATION (Gate SS + Gate LE + Rubric threshold + SX)
          → PUBLICATION (Mission bundle)
            → MAINTENANCE
              → RETIREMENT
```

| Stage | Owner | Output |
|-------|-------|--------|
| **Inputs** | Author / curriculum lead | Parent Mission pack (or co-draft), CMP edition, stage plan, mode |
| **Authoring** | Educational author | Complete Session pack per Blueprint §5 + Episodes |
| **Educational Review** | Educational Reviewer (≠ sole Author for commercial packs) | PASS / FAIL / HOLD on flow, reading guidance, checks, reflection |
| **Tutor Review** | Tutor Voice reviewer (human) | PASS / FAIL / HOLD on Tutor Purpose + rhythm feel |
| **Certification** | Quality Gate Owner | Gate SS/LE + SX + Rubric ≥ threshold; evidence recorded |
| **Publication** | Publication Approver | Student exposure authorised as Mission bundle |
| **Maintenance** | Author + Board | Recertify on CMP/syllabus/defect/Mission redesign triggers |
| **Retirement** | Publication Approver | Removed from student-reachable inventory |

Curriculum Review (EA-002) still applies for topic lawfulness and package consistency. Session-specific flow nests inside EA-002’s full pipeline.

---

## 3. Stage definitions

### 3.1 Inputs

**Enter when:** Parent Mission topic identity resolves (or Mission co-authored in same bundle); CMP edition known; mode known.

**Required artefacts:**

- Parent Mission ID / pack (Purpose, Tutor Intent, CMP Reading Scope, Reflection Goal, Continuity Bundle, Success Criteria, Revision Signals)  
- Syllabus node (code + title)  
- CMP edition pin  
- Mode (Learning / Revision)  
- Draft stage plan matching Blueprint §4  
- Interruption budget draft  

**Exit criteria:** No contaminant nodes; no unresolved placeholders in identity; Mission fields available for Session implementation.

**Fail →** Do not author Session as student-reachable.

---

### 3.2 Authoring

**Enter when:** Inputs complete.

**Required artefacts:**

- All Blueprint §5 components  
- Stage plan with Episode types  
- Reading Guidance packet (objectives, misconceptions use, attention directives, exit, re-entry, pause points)  
- Knowledge Check design (≥1 Active Recall / Practice / Checkpoint)  
- Reflection + Confidence designs  
- Wrap-up + Tomorrow Preparation aligned to Mission Tomorrow Bridge  
- Linked Episode drafts for Gate LE  

**Exit criteria:** Blueprint-complete; Tutor Purpose Session-specific; rhythm laws RF-01–RF-08 respected in design; P/RG forbidden patterns self-denied.

**Fail →** Remain `draft`; do not submit review.

---

### 3.3 Educational Review

**Reviewer:** Educational Reviewer (Academic Board designate).

**Checks (all required):**

| ID | Criterion |
|----|-----------|
| ER-S01 | Educational Purpose and Tutor Purpose coherent with parent Mission |
| ER-S02 | Stage arc complete (Entry → … → Completion); advertised N of M reachable |
| ER-S03 | Reading Preparation creates selective attention (focus questions + locus + stop) |
| ER-S04 | Reading Guidance deliberate per `EA004_READING_GUIDANCE_ARCHITECTURE.md` |
| ER-S05 | Interruption budget respected; pauses sparse and justified |
| ER-S06 | Knowledge Checks demand retrieval/performance after reading (SS-03) |
| ER-S07 | Reflection topic-specific and student-authored path (SS-04) |
| ER-S08 | Confidence Assessment soft-only; no mastery conflation |
| ER-S09 | Wrap-up truthful; Tomorrow Preparation lawful or honest absence |
| ER-S10 | Duration / load consistent with depth and Mission time |
| ER-S11 | Success / Reflection / Revision / Continuity evidence paths present |
| ER-S12 | No §5 reject class triggered |
| ER-S13 | Universal preconditions U1–U7 respected |
| ER-S14 | CMP vs Kwalitec roles correct — no CMP dump |

**Exit:** PASS / FAIL / HOLD with notes. FAIL returns to Authoring.

---

### 3.4 Tutor Review

**Reviewer:** Human Tutor Voice reviewer (Version 1: automation may not PASS this stage alone).

**Checks (all required):**

| ID | Criterion |
|----|-----------|
| TR-S01 | **Tutor Purpose mandatory** — present, Session-specific, non-interchangeable |
| TR-S02 | Primary-block IFoA tutor test: reviewer would assign this Session for the hour |
| TR-S03 | Voice conforms to `EA002_TUTOR_VOICE_GUIDE.md` |
| TR-S04 | Style conforms to `EA002_EDUCATIONAL_STYLE_GUIDE.md` |
| TR-S05 | Rhythm feels like a tutor (guide → yield → return → reflect → tomorrow) — not software nagging |
| TR-S06 | Mission information not excessively restacked |
| TR-S07 | No platform meta on hero Session surfaces |
| TR-S08 | Silence during reading is designed, not accidental emptiness |
| TR-S09 | Student confidence: Session reduces anxiety without false mastery |

**Exit:** PASS / FAIL / HOLD. FAIL returns to Authoring (voice/rhythm rewrite).

---

### 3.5 Certification

**Owner:** Quality Gate Owner.

**Required:**

1. Educational Review PASS  
2. Tutor Review PASS  
3. Gate SS checklist PASS (`EA001_QUALITY_GATES.md` §6) SS-01–SS-10  
4. All constituent Learning Episodes PASS Gate LE  
5. Parent Mission PASS Gate MG + EA-003 MX **or** co-certifying in same bundle with joint rule  
6. Session Scoring Rubric overall ≥ publication threshold (`EA004_SESSION_SCORING_RUBRIC.md`)  
7. Session Certification Gate SX-01–SX-10 PASS  
8. No §5 reject class  
9. Dependencies / publication metadata complete  
10. EV-001 regression denials recorded for TB-001, TB-007, TB-008, TB-009 as applicable  

**Exit:** `certification_status` = pass | fail | hold. Evidence recorded in pack.

**Session Certification PASS** = Gate SS PASS **and** all Gate LE PASS **and** SX-01–SX-10 PASS **and** Educational Review PASS **and** Tutor Review PASS **and** Rubric threshold met **and** joint Mission rule satisfied.

---

### 3.6 Publication

Follow `EA002_PUBLICATION_WORKFLOW.md`.

**Session-specific rules:**

- Publish only as **Mission bundle** (Mission + Session + Episodes + Reflection + Tomorrow) unless Mission unavailable-state.  
- Orphan Sessions forbidden.  
- Publication Approval human-signed for Version 1.  
- `status` → `published` only after approval record complete.

---

### 3.7 Maintenance

**Triggers requiring re-review (at least Tutor Review + affected Gate SS/LE items):**

| Trigger | Action |
|---------|--------|
| CMP edition change affecting locus | Update Reading Guidance; recertify |
| Syllabus node retitle / restructure | Update identity; recertify |
| Mission redesign changing scope/strategy | Align Session; recertify jointly |
| Defect discovery (student/Board) | HOLD or retire; fix; recertify |
| Episode redesign changing N of M | Update stage plan; recertify |
| Interruption / flow defect found in dogfood | Remediate; recertify |
| Contaminant / truth-split discovered | Immediate HOLD; cross-surface audit |
| Rubric dimension regression on spot-check | Remediate pack |

Maintenance is educational duty — silent rot forbidden.

---

### 3.8 Retirement

**Enter when:** Topic removed, package superseded, irreparable defect, or Board decision.

**Requirements:**

- `status=retired`  
- Removed from student-reachable inventory  
- History/Twin evidence for past study preserved  
- Replacement Session (if any) certified independently / jointly with Mission  
- Retirement reason recorded in publication metadata  

Retired ≠ deleted educational memory.

---

## 4. Gate SS integration + Session Certification Gate SX

### 4.1 Gate SS (restated — still mandatory)

| ID | Criterion |
|----|-----------|
| SS-01 | Overview answers “Am I ready to begin?” with real topic data |
| SS-02 | Before / During / After Reading responsibilities satisfied |
| SS-03 | At least one Active Recall or Practice demand after reading |
| SS-04 | Reflection present, topic-specific, student-authored path |
| SS-05 | Stage advance and feedback paths complete |
| SS-06 | Duration honesty vs depth |
| SS-07 | Summary does not invent completion/mastery beyond warrant |
| SS-08 | Premium fitness test pass (Session Philosophy §12 + Blueprint §8) |
| SS-09 | All constituent Learning Episodes PASS Gate LE |
| SS-10 | Parent Mission PASS Gate MG (or Session not offered) |

### 4.2 Session Certification Gate SX (EA-004 additions)

| ID | Criterion |
|----|-----------|
| SX-01 | Tutor Purpose present and Session-unique (extends Mission Tutor Intent) |
| SX-02 | Educational rhythm engineered per `EA004_STUDY_SESSION_FLOW.md` (RF-01–RF-08) |
| SX-03 | Reading Guidance Architecture satisfied (exit packet + re-entry + RG-X denials) |
| SX-04 | Interruption budget stated and respected |
| SX-05 | Mission information not excessively repeated across stages |
| SX-06 | Confidence Assessment present and non-mastery |
| SX-07 | Tomorrow Preparation + Continuity Evidence complete or honest absence |
| SX-08 | Success / Reflection / Revision evidence fields complete |
| SX-09 | Rubric overall ≥ publication threshold; no dimension below floor |
| SX-10 | No §5 reject class |

---

## 5. Session quality gates — reject classes (measurable)

Reject (automatic FAIL) if the Session is any of the following. Rubric scoring does not override an automatic reject.

### 5.1 Interrupts excessively

| Measure | Fail when |
|---------|-----------|
| Pause count | Designed Reading Pause Points > interruption_budget, or > 3 without Board HOLD |
| Continuous prompt test | Reading phase requires Kwalitec speech more often than at authored pause boundaries |
| Feel test | Tutor Reviewer judges the Session “nags during reading” (TR-S05 FAIL) |

**Link:** RF-03 · Reading Guidance §7 · EP-04

---

### 5.2 Repeats Mission information

| Measure | Fail when |
|---------|-----------|
| Restack test | Same multi-sentence why-now / Mission narrative appears verbatim in ≥3 distinct stages |
| Progressive disclosure test | Orientation + Preparation + Wrap-up each re-brief the full Mission without new educational job |

**Link:** SB-09 · Flow RF-07 · Flow §6

---

### 5.3 Duplicates CMP

| Measure | Fail when |
|---------|-----------|
| Paste test | Session/Episode body contains CMP paragraph-length exposition presented as Kwalitec content |
| Parallel course test | Student can complete “reading” without opening CMP because Kwalitec replaced it |

**Link:** EP-01 · EP-04 · Guidance Over Content · V1 E1 · RG-X03

---

### 5.4 Contains educational filler

| Measure | Fail when |
|---------|-----------|
| Filler test | Stages exist without cognitive demand (empty cheer, platform essays, generic tips unrelated to concept focus) |
| Template fragment test | Mechanically concatenated boilerplate detectable as non-specific to topic |
| Hero meta test | Platform/engineering jargon on primary study surfaces (U4) |

**Link:** EP-09 · EA-002 Style · TB-012

---

### 5.5 Breaks educational flow

| Measure | Fail when |
|---------|-----------|
| Arc test | Missing mandatory stage job (e.g. no Knowledge Checks; no Reflection; no return after reading) |
| Advance test | Advertised stages unreachable or Continue dead-ends (TB-008) |
| Rhythm test | No designed exit into CMP or no designed re-entry |
| Order test | Tomorrow heavy teaching before Reflection; Reflection used instead of Knowledge Checks |

**Link:** Flow §2–4 · SS-02 · SS-05 · RF-01–RF-06

---

### 5.6 Lacks deliberate reading guidance

| Measure | Fail when |
|---------|-----------|
| Locus test | No named CMP open point |
| Focus test | No 2–4 focus questions / reading objectives |
| Stop test | No stop condition / return cue |
| Empty shell test | Reading stage is free-text only (TB-007; Gate LE special rule) |
| Exit packet test | Exit packet incomplete (Reading Guidance §7.2) |

**Link:** EP-04 · Reading Guidance Architecture · SS-02

---

### 5.7 Lacks meaningful reflection

| Measure | Fail when |
|---------|-----------|
| Specificity test | Prompts reusable across unrelated topics without substitution (“Today’s topic”) |
| Authorship test | System-written reflection attributed to student; or Reflection skippable while Session completes |
| Goal test | Does not implement Mission Reflection Goal (clearer / uncertain / carry forward absent) |

**Link:** EP-07 · SS-04 · Blueprint §5.7

---

### 5.8 Additional automatic rejects

| Class | Fail when |
|-------|-----------|
| Placeholders | “Today’s topic”, TODO, TBD, unfilled tokens (U2; TB-001) |
| Failed bind | Session openable when topic/locus unresolved |
| Mastery theatre | Completion or confidence language claims mastery / Topic Complete improperly |
| Joint orphan | Session certified without Mission PASS / co-cert path |
| Duration lie | Claimed minutes contradict Episode depth or Home duration authority (TB-009) |
| Truth split | Designed contradiction with History / Home / Journey for same facts (EP-10) |

---

## 6. Evidence record (required at Certification PASS)

| Field | Content |
|-------|---------|
| Reviewer IDs | Educational Reviewer + Tutor Reviewer + Quality Gate Owner |
| Dates | Review and certification timestamps |
| Gate SS / LE | Checklist outcomes per Episode |
| SX-01–SX-10 | Outcomes |
| Reject class scan | Explicit denial of §5.1–§5.8 |
| Rubric | Dimension scores + overall |
| Joint Mission | Mission ID + MG/MX status |
| Package | Subject/version + CMP edition |
| EV-001 denials | TB-001 / TB-007 / TB-008 / TB-009 as applicable |

---

## 7. Explicit non-goals

EA-004 Session Certification does **not**:

- Certify live CS1 Sessions in this programme  
- Replace Gate SS / LE  
- Allow automation-only Tutor Review PASS in Version 1  
- Amend EA-001 / EA-002 / EA-003 certification texts  

---

## 8. Stop

Certification law is complete. Successor programmes submit Session packs through this lifecycle inside `EA002_CERTIFICATION_WORKFLOW.md`, then joint publication via `EA002_PUBLICATION_WORKFLOW.md`.
