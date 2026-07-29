# Implementation Plan

**Programme:** DX-005A  
**Status:** Plan for subsequent UI execution (not executed in DX-005A)  
**Release Candidate:** `RC-2026.07.29-01`  
**Depends on:** This corpus + DX-001 / DX-002 / DX-003  

---

## Scope boundary

| DX-005A (this programme) | Later execution |
|---|---|
| Architecture, mission model, wireframe, removal, continuity, nav boundaries, scorecard | Template + CSS + view-model |
| Documentation only | Routes/nav alignment |
| No application code | `student/home.html` → Mastery First Home |

DX-005A does **not** ship UI. The following is the ordered plan for the implementation milestone that consumes these artefacts.

---

## Phase 0 — Preconditions

1. Treat `STUDENT_HOME_ARCHITECTURE.md` + `STUDENT_HOME_WIREFRAME.md` + `MISSION_MODEL.md` as binding.  
2. Confirm continuity services can supply open session / assessment / findings pointers (`SESSION_CONTINUITY_SPEC.md`).  
3. Align product language: Home continues; Choose Exam discovers (DX-005B may still be design-only).  
4. Update `TERMINOLOGY_DICTIONARY.md` at implementation time if any Home labels diverge.  
5. Do not start Choose Exam UI redesign until Home exit criteria are clear in design (this programme) and preferably UI.

---

## Phase 1 — Content & structure

Per DX-003 cognitive-load plan: content and IA before chrome polish.

1. Replace `student/home.html` body with L0 / L1 / L2 structure only.  
2. Delete greeting, Sensei narrator, MES stack, Mission Intelligence, timeline, experience feedback, educational panel, readiness/journey/coach panels, milestones, Quick Actions, welcome modal.  
3. Single Primary in L0; queue/recent as lists.  
4. Empty state: Reason + Choose Exam.  
5. Quiet day-complete state (no congratulations).  
6. Wire Primary → Session / Assessment / Findings / Choose Exam per Mission status.

**Exit:** One question answerable without scroll; one Primary; mission recognition immediate.

---

## Phase 2 — View-model

1. Build Home DTO:  
   - `current_mission`: subject, objective, status, why_now, after_completion, primary_label, primary_target, continuity  
   - `learning_queue[]`: attention_label, subject, focus, href (attention-only, max 5)  
   - `recent_progress[]`: activity_type, title, relative_time, href (max 5)  
2. Selection algorithm per Architecture §5 / Continuity §4.  
3. Stop requiring readiness/coach/milestones/quick_actions for Home first paint.  
4. Preserve those payloads on Journey / Session / History routes only.

**Exit:** Home renders without legacy secondary-panel fields.

---

## Phase 3 — Continuity wiring

1. Ensure Continue Session never requires re-commitment POST.  
2. Restore chapter / question / assessment index / timer per spec.  
3. Findings Ready → Review Findings Primary.  
4. Honest failure states for invalid session ids.  
5. Cross-day: open session still resumes.

**Exit:** One-click resume acceptance tests pass.

---

## Phase 4 — Navigation chrome

1. Remove in-page Quick Actions (already deleted in Phase 1).  
2. Align student shell to Home / Choose Exam / History / Settings / Help (Journey placement per `NAVIGATION_BOUNDARIES.md`).  
3. Ensure Session/Assessment stay out of primary nav.  
4. No duplicate Journey/Revision/History CTAs on Home.

**Exit:** Nav boundaries acceptance tests pass.

---

## Phase 5 — Visual system compliance

1. Apply DX-001 type scale (24 / 18 / 16 / 14).  
2. Apply spacing scale only.  
3. Semantic status colour; no gold chrome; no gamification.  
4. Focus states, keyboard order, responsive column.  
5. Re-run `PREMIUM_SCORECARD.md`; all DX-005A dimensions ≥9.

**Exit:** Scorecard PASS on live UI.

---

## Phase 6 — Performance

1. Primary path independent of secondary data fetches.  
2. Measure time-to-Primary (target <3s perceived).  
3. Mission L0 in first viewport on mobile and desktop.

**Exit:** Performance goals met or documented waiver with fix date.

---

## Explicit non-goals for implementation slice

- Choose Exam redesign (DX-005B)  
- Full Journey / History visual redesign  
- Curriculum engine changes  
- Founder Console changes  
- Adding streaks/badges “temporarily”

---

## Risk register

| Risk | Mitigation |
|---|---|
| MES/explainability regression claims | Relocate disclosure to Session; keep one why-now on Home |
| Continuity gaps in assessment timers | Spec acceptance tests before ship |
| Nav still shows legacy Quick Actions elsewhere | Boundaries doc + shell audit |
| View-model still hydrates coach/readiness | Slim assembler for Home route only |

---

## Suggested commit framing (when UI ships)

```text
feat(student-home): implement DX-005A mastery-first Home

Replace legacy hero/panel Home with L0 Mission, L1 queue, L2 progress.
One Primary; session continuity resume; no KPI or Quick Action theatre.
```

Do not commit until the implementation milestone explicitly requests it.
