# Reflection Spec

**Programme:** DX-005C  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-003 Terminology; `PRACTICE_MODEL.md`; `SESSION_ARCHITECTURE.md`  

---

## 1. Law

**Reflection belongs after practice. Not before.**

| Allowed | Forbidden |
|---|---|
| After **Complete Session** | Modal journal before first activity |
| Brief, optional Sensei reflection | Mandatory multi-page reflection essay |
| Return Home as the exit | Reflection as a second Home / dashboard |

---

## 2. Completion flow

```
Practice cycle
    ↓
Complete Session
    ↓
Reflection
    ↓
Return Home
```

Home owns continuation. Reflection must not invent “start next Mission” as a peer Primary theatre — at most one quiet line that Home will show the next step.

---

## 3. Reflection modes

| Mode | When | Primary | Secondary |
|---|---|---|---|
| **Offered** | Product enables post-session reflection | **Save & return Home** | Skip to Home (text) |
| **Optional skip-default** | Reflection optional and empty | **Return Home** | Open reflection (text) |
| **Disabled** | No reflection configured | **Return Home** immediately after Complete | — |

Never two filled Primaries (Save + Skip as peers).

---

## 4. Content rules

| Allowed | Forbidden |
|---|---|
| One short prompt (e.g. What mattered in this practice?) | Multi-why MES stack |
| Single text field or ≤3 short prompts | Survey batteries / NPS mid-flow |
| Quiet save acknowledgement (**Saved.**) | “Proud of you!” / streak theatre |
| Link to Decision Journal / Sensei reflection (DX-003 terms) | “Feedback Loop” student label |

Prompt tone: professional, operational. Not therapeutic. Not motivational.

---

## 5. Terminology (DX-003)

| Concept | Student label |
|---|---|
| Post-session notice | **Session reflection** |
| Optional journal form | **Sensei reflection** |
| Archive of past practice | **History** (not opened as Primary during reflection) |

---

## 6. Timing & interruption

| Event | Behaviour |
|---|---|
| Student completes last activity | Show **Complete Session** (not auto-force reflection mid-feedback) |
| Student confirms Complete | Enter Reflection mode (or Home if disabled) |
| Student exits mid-practice | No reflection — persist practice state only |
| Student abandons reflection | Treat as Skip → Home; do not block |

Reflection is never required to preserve continuity of practice coordinates.

---

## 7. Layout

```
│  Reflection                                                             │
│  What mattered in this practice?                                        │
│  [ text area ]                                                          │
│                                                                         │
│  [ Save & return Home ]                                                 │
│  Skip to Home                                                           │
```

No confetti. No badge unlock. No “session summary dashboard” of KPIs. Optional one-line session fact (subject · steps completed) may appear as quiet orientation — not a stats wall.

---

## 8. Data

| Persist | Do not |
|---|---|
| Reflection text when saved | Block session close on empty optional field |
| Timestamp / session_id linkage | Require re-auth for skip |
| | Store fake “mood scores” without product need |

---

## 9. Boundary with History

History owns browsing past sessions and reflections. Reflection UI at Session end is **capture**, not archive navigation. Do not embed History lists inside Reflection.

---

## 10. Acceptance tests

1. No reflection UI appears before the first practice Primary.  
2. Complete Session precedes Reflection.  
3. Skip / Return Home lands on Home with continuation ownership.  
4. Exactly one filled Primary on the Reflection screen.  
5. No gamification on reflection complete.
