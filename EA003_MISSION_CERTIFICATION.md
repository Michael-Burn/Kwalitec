# EA-003 — Mission Certification

**Programme:** Educational Excellence Programme EA-003  
**Status:** Binding — Mission lifecycle review and certification  
**Effective:** 2026-08-01  
**Parent:** `EA003_MISSION_BLUEPRINT.md` · `EA003_MISSION_SCHEMA.md` · `EA003_MISSION_SCORING_RUBRIC.md`  
**Related:** Gate MG · `EA002_CERTIFICATION_WORKFLOW.md` · `EA002_PUBLICATION_WORKFLOW.md` · `EA001_QUALITY_GATES.md`  
**Nature:** Process law — not educational content, not application code  

---

## 1. Purpose

Define how a Mission moves from inputs to retirement — and the measurable quality gates that reject unfit briefs before students see them.

EA-001 defines Gate MG (what PASS means).  
EA-002 defines multi-stage certification for all artefact classes.  
**EA-003 specialises the Mission lifecycle and Mission-only reject criteria** so Mission quality can be objectively reviewed.

> **A single failed stage blocks publication.**

---

## 2. Mission lifecycle

```text
INPUTS
  → AUTHORING
    → EDUCATIONAL REVIEW
      → TUTOR REVIEW
        → CERTIFICATION (Gate MG + Rubric threshold)
          → PUBLICATION
            → MAINTENANCE
              → RETIREMENT
```

| Stage | Owner | Output |
|-------|-------|--------|
| **Inputs** | Author / curriculum lead | Lawful topic, CMP locus, prior context, mode |
| **Authoring** | Educational author | Complete Mission pack (`EA003_MISSION_SCHEMA.md`) |
| **Educational Review** | Educational Reviewer (≠ sole Author for commercial packs) | PASS / FAIL / HOLD on educational coherence |
| **Tutor Review** | Tutor Voice reviewer (human) | PASS / FAIL / HOLD on Tutor Intent + voice |
| **Certification** | Quality Gate Owner | Gate MG + Rubric ≥ threshold; evidence recorded |
| **Publication** | Publication Approver | Student exposure authorised for package version |
| **Maintenance** | Author + Board | Recertify on CMP/syllabus/defect triggers |
| **Retirement** | Publication Approver | Removed from student-reachable inventory |

Curriculum Review (EA-002 stage) still applies for topic lawfulness and package consistency when certifying subject packages. Mission-specific flow above nests inside EA-002’s full pipeline.

---

## 3. Stage definitions

### 3.1 Inputs

**Enter when:** Topic identity resolves; CMP edition known; mode known.

**Required artefacts:**

- Syllabus node (code + title)  
- Prior Mission/topic or cold-start context  
- CMP edition pin  
- Mode (Learning / Revision)  
- Draft Session intent (structure names)

**Exit criteria:** No contaminant nodes; no unresolved placeholders in identity.

**Fail →** Do not author.

---

### 3.2 Authoring

**Enter when:** Inputs complete.

**Required artefacts:** Full pack per Schema §4–5; Authoring Guide sequence followed; P1–P12 self-denial.

**Exit criteria:** Schema-complete; `tutor_intent` present and Mission-unique; Continuity Bundle complete; Session/Episodes draft-linked.

**Fail →** Remain `draft`; do not submit review.

---

### 3.3 Educational Review

**Reviewer:** Educational Reviewer (Academic Board designate).

**Checks (all required):**

| ID | Criterion |
|----|-----------|
| ER-M01 | Mission Purpose and Educational Intent are educationally coherent |
| ER-M02 | Learning Objective distinct from syllabus heading and display title |
| ER-M03 | Concept Focus concrete; Common Misconceptions usable |
| ER-M04 | CMP Reading Scope precise (open / stop / out-of-scope) |
| ER-M05 | Syllabus Coverage honest; mode correct |
| ER-M06 | Prerequisites stated; safe for claimed entry point |
| ER-M07 | Success Criteria assessable; Reflection Goal topic-specific |
| ER-M08 | Continuity Bundle complete (prior + tomorrow or honest absence) |
| ER-M09 | Study Strategy matches deliberate study (not passive “read”) |
| ER-M10 | Load and time mutually consistent with scope |
| ER-M11 | Revision Signals present or lawfully noted |
| ER-M12 | No reject class from §5 triggered |
| ER-M13 | Universal preconditions U1–U7 respected |

**Exit:** PASS / FAIL / HOLD with notes. FAIL returns to Authoring.

---

### 3.4 Tutor Review

**Reviewer:** Human Tutor Voice reviewer (Version 1: automation may not PASS this stage alone).

**Checks (all required):**

| ID | Criterion |
|----|-----------|
| TR-M01 | **Tutor Intent mandatory** — present, specific, non-interchangeable |
| TR-M02 | Night-before IFoA tutor brief test passes |
| TR-M03 | Voice conforms to `EA002_TUTOR_VOICE_GUIDE.md` |
| TR-M04 | Style conforms to `EA002_EDUCATIONAL_STYLE_GUIDE.md` |
| TR-M05 | Why-now / explainability specific — not TB-004 boilerplate |
| TR-M06 | No platform meta on hero-destined fields |
| TR-M07 | Continuity language feels remembered (EP-02), not stamped |
| TR-M08 | Student confidence: brief reduces anxiety without false mastery |

**Exit:** PASS / FAIL / HOLD. FAIL returns to Authoring (voice/intent rewrite).

---

### 3.5 Certification

**Owner:** Quality Gate Owner.

**Required:**

1. Educational Review PASS  
2. Tutor Review PASS  
3. Gate MG checklist PASS (`EA001_QUALITY_GATES.md` §4) including M1–M12 / MG-01–MG-10  
4. Mission Scoring Rubric overall ≥ publication threshold (`EA003_MISSION_SCORING_RUBRIC.md`)  
5. Joint rule: linked Session/Episodes PASS Gate SS/LE **or** honest `unavailable_state`  
6. Dependencies block complete; package version pinned  
7. EV-001 regression denials recorded for TB-002, TB-004, TB-005, TB-009/010 as applicable  

**Exit:** `certification_status` = pass | fail | hold. Evidence URI recorded in pack.

---

### 3.6 Publication

Follow `EA002_PUBLICATION_WORKFLOW.md`.

**Mission-specific rules:**

- Publish only as **Mission bundle** (Mission + Session + Episodes + Reflection + Tomorrow) unless unavailable-state Mission.  
- Orphan Mission briefs forbidden.  
- Publication Approval human-signed for Version 1.  
- `status` → `published` only after approval record complete.

---

### 3.7 Maintenance

**Triggers requiring re-review (at least Tutor Review + affected Gate MG items):**

| Trigger | Action |
|---------|--------|
| CMP edition change affecting locus | Update scope; recertify |
| Syllabus node retitle / restructure | Update identity/coverage; recertify |
| Defect discovery (student/Board) | HOLD or retire; fix; recertify |
| Session/Episode redesign changing stages | Update strategy/dependencies; recertify |
| Contaminant / truth-split discovered | Immediate HOLD; cross-surface audit |
| Rubric dimension regression on spot-check | Remediate pack |

Maintenance is educational duty — silent rot forbidden (EA-002 lesson).

---

### 3.8 Retirement

**Enter when:** Topic removed, package superseded, irreparable defect, or Board decision.

**Requirements:**

- `status=retired`  
- Removed from student-reachable inventory  
- History/Twin evidence for past study preserved (do not erase rightful history)  
- Replacement Mission (if any) certified independently  
- Retirement reason recorded in publication metadata  

Retired ≠ deleted educational memory.

---

## 4. Gate MG integration (Mission checklist restated)

All of the following remain mandatory (EA-001):

| ID | Criterion |
|----|-----------|
| MG-01 | M1–M12 present (via EA-003 field mapping) |
| MG-02 | Objective ≠ syllabus heading |
| MG-03 | Bridge from prior (or cold-start) |
| MG-04 | Why-now specific |
| MG-05 | Concept focus concrete |
| MG-06 | Success criterion countable |
| MG-07 | Material locus named |
| MG-08 | Session intent matches certified/existing episodes |
| MG-09 | P1–P12 absent |
| MG-10 | IFoA-tutor brief test |

**EA-003 additions (Mission Certification Gate MX):**

| ID | Criterion |
|----|-----------|
| MX-01 | Tutor Intent present and Mission-unique |
| MX-02 | Continuity Bundle complete |
| MX-03 | Common Misconceptions 1–3 (or Board HOLD) |
| MX-04 | Reflection Goal topic-specific |
| MX-05 | Cognitive load + study time consistent |
| MX-06 | Revision Signals present or lawful note |
| MX-07 | Dependencies complete for publish |
| MX-08 | Rubric overall ≥ publication threshold |
| MX-09 | No §5 reject class |

**Mission Certification PASS** = Gate MG PASS **and** MX-01–MX-09 PASS **and** Educational Review PASS **and** Tutor Review PASS.

---

## 5. Mission quality gates — reject classes (measurable)

Reject (automatic FAIL) if the Mission is any of the following.

### 5.1 Generic

| Measure | Fail when |
|---------|-----------|
| Topic-swap test | Replacing topic code/title leaves Tutor Intent, why-now, Concept Focus, and Reflection Goal still plausible without rewrite |
| Specificity count | Fewer than 2 concrete topic/skill/CMP references in student-facing brief fields |

### 5.2 Template driven

| Measure | Fail when |
|---------|-----------|
| Boilerplate | `why_now` or `explainability` matches another Mission in package verbatim or near-verbatim |
| Stamp fields | Display title / objective / narrative collapse to same string pattern with only code changed |
| Mechanical concatenation | Authoring notes or prose show fragment assembly without tutor rewrite |

### 5.3 CMP paraphrases

| Measure | Fail when |
|---------|-----------|
| Body paste | Mission narrative restates CMP paragraphs rather than guiding into CMP |
| Locus absent | `cmp_reading_scope.open_point` missing while long explanatory body present |

### 5.4 Syllabus restatements

| Measure | Fail when |
|---------|-----------|
| Equality | `learning_objective` == syllabus heading **or** == `display_title` with no distinct educational verb |
| Triple collapse | Title = objective = purpose = heading |

### 5.5 Disconnected

| Measure | Fail when |
|---------|-----------|
| Prior | `prior_bridge` missing or empty cold-start without enrolment/chapter purpose |
| Tomorrow | `tomorrow_bridge` missing both known continuity and honest absence |
| Session | No linked Session/Episodes and no honest unavailable state at certification |

### 5.6 Educationally purposeless

| Measure | Fail when |
|---------|-----------|
| Intent | `educational_intent` missing or equals “complete the Mission / cover the topic” |
| Success | No assessable success criteria |
| Benefit | Expected benefit is readiness ±N% alone |

### 5.7 Lacking continuity

| Measure | Fail when |
|---------|-----------|
| Bundle | Any Continuity Bundle element failed (Schema CI-01–CI-05) |
| Arc voice | No yesterday→today educational story when history exists |

### 5.8 Lacking Tutor Intent

| Measure | Fail when |
|---------|-----------|
| Missing | `tutor_intent` empty |
| Interchangeable | Intent could apply unchanged to ≥3 other topics in package |
| Too thin | Fails SV-05 length or Tutor Review TR-M01 |

---

## 6. Certification evidence package (Mission)

Minimum evidence for a Mission PASS:

| Item | Required |
|------|----------|
| Mission pack snapshot (schema fields) | Yes |
| Educational Review record | Yes |
| Tutor Review record | Yes |
| Gate MG checklist outcomes | Yes |
| MX checklist outcomes | Yes |
| Rubric scores by dimension + overall | Yes |
| Joint Session/Episode gate refs or unavailable-state | Yes |
| Prohibited-pattern / TB denial list | Yes |
| Reviewer IDs + dates | Yes |
| HOLD waivers + expiry (if any) | Conditional |

Store evidence URI in `certification_evidence`.

---

## 7. Relationship to EA-002 stages

| EA-002 stage | Mission handling |
|--------------|------------------|
| Educational Review | §3.3 ER-M* |
| Tutor Review | §3.4 TR-M* |
| Curriculum Review | Topic lawfulness, package consistency, contaminant scan |
| Quality Gate | Gate MG + MX + Rubric |
| Publication Approval | §3.6 + EA-002 Publication Workflow |

Do not skip EA-002 stages. EA-003 deepens Mission criteria inside them.

---

## 8. Results model

| Result | Meaning |
|--------|---------|
| **PASS** | May proceed to Publication Approval for scoped package version |
| **FAIL** | Must not reach students; defects listed with ER/TR/MG/MX/reject IDs |
| **HOLD** | Temporary block with expiry and honesty constraints — not a silent PASS |

---

## 9. Closing

> Objective review means: every reject class has a measure, Tutor Intent is mandatory, continuity is checked, and Gate MG still stands.

No shortcuts. No “fix voice later.” No orphan briefs.

If it cannot pass Mission Certification, it is not a Kwalitec Mission.
