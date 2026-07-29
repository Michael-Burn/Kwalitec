# Architectural Fidelity Checklist

**Programme:** DX-006B  
**Status:** Binding scoring instrument for every migrated surface  
**Release Candidate:** `RC-2026.07.29-01`  
**Pass threshold:** **≥95 / 100**  

---

## 1. How to score

1. Copy the scorecard below into the phase block in `PHASE_TRACKER.md`.  
2. Award points per category using the rubrics (partial credit allowed only where the rubric says so).  
3. Sum weighted points.  
4. **&lt;95 = FAIL** — phase may not certify; remediate and re-score.  
5. Do not average away a failing Guardian or One Primary violation — those cap related categories (see §3).

---

## 2. Weight table

| Category | Weight | Max points |
|---|---:|---:|
| Matches DX Architecture | 30 | 30 |
| Shared Components | 20 | 20 |
| Token Compliance | 15 | 15 |
| Guardian Compliance | 15 | 15 |
| Accessibility | 10 | 10 |
| Performance | 10 | 10 |
| **Total** | **100** | **100** |

---

## 3. Hard caps (automatic)

| Condition | Effect |
|---|---|
| More than one Primary in primary task viewport | Guardian ≤7; Matches DX Architecture ≤20; **overall FAIL** regardless of other scores |
| KPI / StatisticTile / vanity progress rings present | Guardian ≤7; Matches DX Architecture ≤18; **FAIL** |
| Hard-coded colours in page/component CSS (non-token files) | Token Compliance ≤7; Guardian ≤10; **FAIL** if any new hex introduced in this phase |
| Legacy chrome CSS-hidden rather than removed | Matches DX Architecture ≤15; Shared Components ≤10; **FAIL** |
| Phase started before prior CERTIFIED | **Invalid score** — do not record PASS |

---

## 4. Rubrics

### 4.1 Matches DX Architecture (30)

Score against the phase authority (DX-004A/B/C or DX-005A/B/C):

| Points | Criteria |
|---:|---|
| 28–30 | Hierarchy L0→L3 exact; one question answerable; removals complete; hand-offs match authority |
| 24–27 | Structure correct; minor copy/label drift; no structural extras |
| 18–23 | Missing section or extra panel that competes with L0 |
| 0–17 | Redesign drift, dashboard mashup, or wrong surface type |

**Checks:**

- [ ] Screen answers the authority’s one question  
- [ ] L0 / L1 / L2 / L3 match architecture (or justified omit of empty L2)  
- [ ] Explicit removals from authority CONTENT_REMOVAL / IMPLEMENTATION_PLAN gone  
- [ ] No new IA invented  

### 4.2 Shared Components (20)

| Points | Criteria |
|---:|---|
| 18–20 | All jobs use catalogue L1–L3; no page-orphan duplicates |
| 14–17 | One justified page-local fragment; not promoted as shared |
| 8–13 | Parallel widgets for Mission / Queue / Context / Findings |
| 0–7 | Rebuilt primitives locally; Rejected components used |

**Checks:**

- [ ] L3 operational components from catalogue used where applicable  
- [ ] No duplicate Current Work / Mission / Queue implementations  
- [ ] Rejected list unused (G-12)  

### 4.3 Token Compliance (15)

| Points | Criteria |
|---:|---|
| 14–15 | Type 32/24/18/16/14/12; spacing 4–64; semantic colour only |
| 11–13 | Minor alias debt documented; no new raw values |
| 6–10 | Mixed UX-001 and DX-001 scales on migrated surface |
| 0–5 | Hard-coded colours/spacing/type in templates or page CSS |

**Checks:**

- [ ] No raw hex/rgb outside token definition files  
- [ ] No parallel spacing scale  
- [ ] Inter only; Lucide only  

### 4.4 Guardian Compliance (15)

| Points | Criteria |
|---:|---|
| 14–15 | G-1…G-12 all PASS + surface extras |
| 11–13 | All G PASS; one soft warning documented |
| 6–10 | Any G fail |
| 0–5 | Multiple G fails or Rejected components |

**Checks:** G-1 One Primary · G-2 One H1 · G-3 Token only · G-4 No hard-coded colours · G-5 No duplicate spacing · G-6 No KPI · G-7 No decorative cards · G-8 L0–L3 hierarchy · G-9 No decorative icons · G-10 No duplicate nav · G-11 Catalogue only · G-12 Rejected unused  

### 4.5 Accessibility (10)

| Points | Criteria |
|---:|---|
| 9–10 | DX-006A Accessibility Standard met; keyboard path; focus; labels; contrast |
| 7–8 | Minor SR gap with ticket; critical path keyboard OK |
| 4–6 | Icon-only critical action or missing focus |
| 0–3 | Keyboard trap / inaccessible Primary |

### 4.6 Performance (10)

| Points | Criteria |
|---:|---|
| 9–10 | Minimal DOM; no KPI grids; L2–L3 lazy/collapsed per spec; no heavy unused assets |
| 7–8 | Acceptable; one unnecessary nested wrapper documented |
| 4–6 | Large hidden legacy DOM retained |
| 0–3 | Dual trees / dashboard chrome still loading |

---

## 5. Scorecard template (copy per surface)

```text
Surface: ____________________
Phase: ______________________
Authority: __________________
Reviewer: ___________________
Date: _______________________
Release Candidate: RC-2026.07.29-01

Matches DX Architecture:   __ / 30
Shared Components:         __ / 20
Token Compliance:          __ / 15
Guardian Compliance:       __ / 15
Accessibility:             __ / 10
Performance:               __ / 10
─────────────────────────────────
TOTAL:                     __ / 100

Hard caps triggered?  Yes / No
If Yes, list: _______________

Verdict:  PASS (≥95)  /  FAIL
```

---

## 6. Phase mapping

| Phase | Surface | Authority corpus |
|---|---|---|
| 1 | Founder Home | `knowledge/design/dx004a_founder_home/` |
| 2 | Founder Subjects | `knowledge/design/dx004b_subjects/` |
| 3 | Founder Workspace | `knowledge/design/dx004c_workspace/` |
| 4 | Student Home | `knowledge/design/dx005a_student_home/` |
| 5 | Choose Exam | `knowledge/design/dx005b_choose_exam/` |
| 6 | Study Session | `knowledge/design/dx005c_study_session/` |

---

*Release Candidate: RC-2026.07.29-01*
