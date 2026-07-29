# Navigation Boundaries

**Programme:** DX-005A  
**Status:** Binding for Student Operating System navigation ownership  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-002 product architecture; DX-003 terminology; DX-005A Home mandate  

---

## 1. Law

Each student surface owns exactly one job. Responsibilities **never overlap**.

| Surface | Owns | Does not own |
|---|---|---|
| **Home** | Continuation — what to study next | Discovery, execution UI, evaluation UI, archive browsing |
| **Choose Exam** | Discovery — what to begin studying | Daily continuation, session practice |
| **Study Session** | Execution — practice steps now | Choosing next mission as a second Home |
| **Assessment** | Evaluation | Syllabus browsing, celebration Home |
| **History** | Reflection / archive | Starting today’s mission as Primary theatre |

---

## 2. One-question map (student OS)

| Surface | One question | Primary action family |
|---|---|---|
| Home | What should I study next? | Continue / Resume / Start Assessment / Review Findings / Choose Exam (empty) |
| Choose Exam | What can I begin studying? | Select subject → continue wizard / Begin Learning |
| Study Session | What do I practice now? | Submit / Advance / Finish |
| Assessment | How do I complete this evaluation? | Answer / Submit |
| Findings (review) | What do these results mean for next study? | Acknowledge → return Home |
| History | What have I practiced? | Open detail |
| Journey | Where am I in the syllabus? | Return Home / continue from context |
| Revision | What should I revise for today’s focus? | Begin revision |
| Settings | How do I configure my account? | Save |
| Help | How do I get unblocked? | Search / contact |

---

## 3. Home ownership (detail)

Home **may**:

- Display Current Mission  
- Offer exactly one Primary into Session / Assessment / Findings / Choose Exam  
- List attention-only Learning Queue  
- Show ≤5 Recent Progress orientation rows  
- Rely on shell nav for escape  

Home **must not**:

- Embed Session activity controls  
- Host assessment questions  
- Host full Journey map or readiness KPI wall  
- Host Choose Exam catalogue  
- Host Quick Actions duplicating shell  
- Become Insights / Coach home  

---

## 4. Choose Exam ownership (boundary for DX-005B)

Choose Exam **may**:

- Catalogue Ready / Soon subjects  
- Capture exam date and availability  
- Begin Learning into the study plan  

Choose Exam **must not**:

- Show “today’s mission” as a competing Home  
- Become daily resume surface  

When Home empty state Primary is **Choose Exam**, it hands off discovery — it does not import catalogue UI onto Home.

---

## 5. Study Session ownership

Session **may**:

- Execute chapter / question flow  
- Show learning objective for the active session  
- Host reflection at session end  
- Offer Return Home  

Session **must not**:

- Redesign itself as a dashboard of all missions  
- Replace Home as the place you decide “what’s next today” after return (post-complete may suggest next, but daily entry remains Home)

---

## 6. Assessment ownership

Assessment **may**:

- Run evaluation items and timers  
- Persist progress for continuity  

Assessment **must not**:

- Own daily continuation messaging (Home shows Assessment Ready / Findings Ready)

---

## 7. History ownership

History **may**:

- Archive sessions, journal, timeline disclosure  

History **must not**:

- Present Start Mission as page Primary competing with Home  
- Duplicate Learning Queue as a second attention Home  

Home L2 may deep-link into History quietly.

---

## 8. Journey & Revision (non-primary)

Per DX-002, Journey and Revision remain in the student tree but are **not** peer Homes.

| Surface | Relationship to Home |
|---|---|
| Journey | Syllabus position report — link from shell secondary or Session; not Home L0 |
| Revision | Supporting practice — may appear as L1 **Revision Due**; execution on Revision/Session |

Do not reintroduce Journey / Revision / History as Quick Actions on Home.

---

## 9. Shell nav target (Student)

Primary destinations (≤6):

1. Home  
2. Choose Exam  
3. History  
4. Settings  
5. Help  

Optional sixth: Journey **or** fold Journey under History/Progress disclosure — product choice in implementation; must not create two Homes.

Session and Assessment stay out of primary nav (enter via Home Primary / deep links).

---

## 10. Cross-links (quiet)

Allowed quiet links:

| From | To | When |
|---|---|---|
| Home empty | Choose Exam | No plan |
| Home L2 row | History detail | Orientation |
| Session complete | Home | Default return |
| Findings ack | Home | Continue learning |
| Choose Exam complete | Home | First mission ready |

Forbidden: equal-weight CTA rows on Home to Journey + Revision + History + Tutor + Plan.

---

## 11. Founder vs Student (no mashup)

Student Home ≠ Founder Home ≠ Console Overview.

No platform health, publication queue, or support inbox on Student Home.

---

## 12. Acceptance tests

1. From Home, next study is reachable without visiting Choose Exam (when plan exists).  
2. From Choose Exam, user is not asked to “continue today’s mission” as the page purpose.  
3. Session does not re-present full Home mission stack.  
4. History has no competing daily Primary.  
5. No in-page Quick Actions on Home.
