# Section Justification

**Programme:** DX-005A  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Rule:** Every retained section must justify its existence against the primary question.

---

## Primary question

> What should I study next?

Test for every section:

1. Does it help **Decision**?  
2. Does it enable **Action**?  
3. Does it provide **Feedback** (or orientation that prevents wrong action)?  

If none — remove.

---

## Retained sections

### Page title — Home

| Criterion | Answer |
|---|---|
| Decision | Establishes surface identity (recognition beat) |
| Action | No — correctly; title is not a CTA |
| Feedback | No |
| Why keep | DX-001 / DX-003 reading flow requires one page heading |
| Why not expand | No subtitle, greeting, Sensei narrator, or version eyebrow |

---

### L0 — Current Mission

| Criterion | Answer |
|---|---|
| Decision | **Yes** — names subject, objective, status, why now |
| Action | **Yes** — hosts the single Primary |
| Feedback | Indirect — status + after-completion confirm continuity |
| Why keep | Without L0 the page cannot answer the one question in three seconds |
| What would fail without it | Student must scan Journey, History, or invent a next step |
| Authorities | DX-001 Dashboard Philosophy; DX-002 Home type; DX-003 Decision Architecture; DX-005A Mission Model |

---

### L0 — Primary button (exactly one)

| Criterion | Answer |
|---|---|
| Decision | Resolves the decision |
| Action | **The** Action |
| Feedback | Leads to Session / Assessment / Findings Feedback |
| Why keep | Non-negotiable DX-001 button rule + DX-005A Primary Action mandate |
| Alternatives rejected | Quick Actions cluster; Start + Tutor + Defer + Journey peers |

---

### L0 — Why now (one line)

| Criterion | Answer |
|---|---|
| Decision | Strengthens Decision without a second choice |
| Action | No competing CTA |
| Feedback | No |
| Why keep | Mission Model requires operational “why now”; prevents opaque recommendations |
| Why not MES stack | DX-002/003 density failure; explainability lives deeper off Home |
| Bound | ≤1 sentence; operational only |

---

### L0 — After completion (one line)

| Criterion | Answer |
|---|---|
| Decision | Reduces fear of “what then?” without opening a panel |
| Action | No |
| Feedback | Anticipates Feedback after Session |
| Why keep | Mission Model question 3; operational continuity |
| Bound | One line; omit on mobile only if space-critical (DTO still required) |

---

### L1 — Learning Queue

| Criterion | Answer |
|---|---|
| Decision | Supports Decision when L0 is empty or student selects among attention items **after** seeing Primary |
| Action | Row open = secondary path (not Primary) |
| Feedback | Attention status labels only |
| Why keep | Students often have resume + assessment + revision concurrent; queue is honest without KPI cards |
| Why not Journey map | Journey answers a different question (syllabus position) |
| Bound | Attention-only; max 5; no informational rows |
| Authorities | DX-002 Queue affordance nested in Home; DX-003 status system |

---

### L2 — Recent Progress

| Criterion | Answer |
|---|---|
| Decision | Weak — orientation only (“what did I just do?”) |
| Action | Quiet open to History detail only |
| Feedback | Confirms recent Session/Assessment outcomes without celebration |
| Why keep | Prevents “did I already finish X?” cognitive reload; max 5; omit if empty |
| Why not larger | History owns reflection; Home is not an archive |
| Risk if overbuilt | Becomes vanity feed / streak theatre — then **remove** |
| Authorities | DX-001 L2 secondary; DX-005A explicit L2 |

---

### L3 — Shell navigation

| Criterion | Answer |
|---|---|
| Decision | Escape hatch when next work is discovery / settings / help |
| Action | Destinations elsewhere — not page Primaries |
| Feedback | N/A |
| Why keep | Student shell requires one primary nav (DX-002); Home is not a browser |
| Why not on-page Quick Actions | Duplicates nav; fails One Primary |

---

## Explicitly rejected sections (and why)

| Rejected | Decision | Action | Feedback | Verdict |
|---|---|---|---|---|
| Greeting / welcome | No | No | No | Delete |
| Study Sensei hero narrator | Weak | No | No | Delete from Home |
| Multi-why / benefit / coherence stack | Overload | Delays | No | Delete / relocate |
| Mission Intelligence disclosure wall | Overload | Delays | Partial | Relocate off Home |
| Today’s journey timeline | Process | No | Partial | Delete from Home |
| Readiness % card | Analytics | Competing next | No | Relocate |
| Countdown card | Anxiety theatre | Competing | No | Relocate / omit |
| Journey story panel | Narrative | No | Weak | Relocate to Journey |
| Guidance / Coach panel | Duplicate Decision | Tutor CTA | No | Delete from Home |
| Educational experience panel | Meta | No | No | Delete from Home |
| This week feedback stats | Report | No | Weak | Relocate to Journey/History |
| Upcoming milestones | Future inventory | No | No | Delete from Home |
| Quick Actions | Multi-Decision | Multi-Action | No | Delete |
| Welcome modal | Interrupt | Competes | No | Delete |
| Day-complete congratulations | Celebration | No | Noise | Delete |
| Progress rings / streaks / badges | Gamification | No | False Feedback | Delete |
| Defer “Not today” as peer CTA | Second Decision | Competes | No | Omit from Home (Session policy if needed) |
| Tutor explain as peer CTA | Second Decision | Competes | No | Relocate to Session |

---

## Decision reduction claim

| Surface moment | Legacy | Target |
|---|---|---|
| Independent decisions before Primary | 4–7 | **1** |
| Visible Primaries | 2–5 | **1** |
| Explanation layers above CTA | 6–10 | **≤2** (objective context + why-now) |

Estimated reduction in decisions on Home: **~75–85%**.

---

## Retention rule (ongoing)

If a future feature cannot pass Decision / Action / Feedback for **What should I study next?**, it does not ship on Student Home — regardless of educational merit elsewhere.
