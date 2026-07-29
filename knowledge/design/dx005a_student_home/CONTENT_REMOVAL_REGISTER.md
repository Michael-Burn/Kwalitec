# Content Removal Register

**Programme:** DX-005A  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Source of legacy inventory:** `app/templates/student/home.html` + DX-002/DX-003 Student Home audits  
**Rule:** Zero Legacy — do not rearrange; remove and replace with L0–L3 only.

---

## Method

Each legacy element is classified:

| Class | Meaning |
|---|---|
| **Delete** | Never on Student Home |
| **Relocate** | Belongs on another surface |
| **Replace** | Intent survives as L0/L1/L2 structure |
| **Keep** | Survives with rewrite (rare) |

---

## Legacy → target map

| # | Legacy element | Class | Destination / replacement | Authority |
|---|---|---|---|---|
| 1 | Greeting (`student-hero-greeting`) | **Delete** | — | DX-001/003 forbidden welcome |
| 2 | “Study Sensei” narrator line | **Delete** from Home | Session may name Sensei once if required | DX-003 inventory; HOME_SENSEI policy relocate |
| 3 | Hero eyebrow (Today’s Focus / Guided Session / Reflection) | **Replace** | Section label **Current Mission** | DX-005A L0 |
| 4 | Hero title (mission / recommendation / reflection headline) | **Replace** | Subject + objective in L0 | Mission Model |
| 5 | Mission / session status stack | **Replace** | One operational status line | DX-003 status |
| 6 | Duration label | **Keep** (optional L0) | Only if aids Action | DX-003 |
| 7 | Purpose / Why / Why now / Benefit / Coherence / Next stack | **Replace** | **One** why-now + optional after line | DX-002 density; DX-005A |
| 8 | Readiness bridge line | **Delete** from Home | Journey / readiness surface | KPI / density |
| 9 | Confidence / honest refusal chrome on Home | **Relocate** | Session disclosure | Trust without L0 theatre |
| 10 | Commitment reflection “Got it” block on Home | **Relocate** | Session complete / reflection surface | Home ≠ reflection host |
| 11 | Commitment committed/deferred chrome | **Delete** from Home | Continuity implied by Mission status | Density |
| 12 | “Starting means you’re doing this next” | **Delete** | — | Tutorial chrome |
| 13 | Defer “Not today” details peer to Primary | **Delete** from Home | Optional Session/policy elsewhere — not Home peer CTA | One Primary |
| 14 | Expected outcome / mission summary duplicates | **Merge/Delete** | Covered by objective + after | — |
| 15 | Guided Reflection preview prompts on Home | **Relocate** | Session reflection | Home ≠ execution |
| 16 | Primary Start / Continue / Resume CTA | **Replace** | L0 single Primary | Keep intent |
| 17 | Mark mission complete (Runtime C) on Home | **Relocate** | Session / mission completion flow | Home continues, Session completes |
| 18 | Day-complete congratulations / unlocks essay | **Replace** | Quiet complete state (one line) | Explicit forbid |
| 19 | Empty state “insights will appear” + Study Plan dual links | **Replace** | Reason + **Choose Exam** Primary | DX-003 empty |
| 20 | Explanation card / MES disclosure under hero | **Relocate** | Session overview disclosure | Explainability off Home L0 |
| 21 | Mission Intelligence disclosure (full aside) | **Relocate** | Session / Help deep why | DX-002 B-004 |
| 22 | Today’s journey timeline nav | **Delete** from Home | Session chrome if needed | Process ≠ Decision |
| 23 | “Your Journey / This week” feedback stats | **Relocate** | Journey / History | Report type |
| 24 | Educational experience panel on Home | **Delete** from Home | Not a Home job | Meta |
| 25 | Readiness panel + % metric + drivers | **Relocate** | Journey | KPI Audit |
| 26 | Countdown panel content (via readiness) | **Relocate** / **Delete** | Profile or Journey — not Home | Anxiety theatre |
| 27 | Journey story panel | **Relocate** | Journey | Narrative |
| 28 | Guidance / Coach panel + tutor forms | **Delete** from Home | Session tutor if product requires | Duplicate Decision |
| 29 | Recommendation alternatives on Home | **Relocate** | Session disclosure | Density |
| 30 | Upcoming milestones list | **Delete** from Home | Journey | Future inventory |
| 31 | Quick Actions nav panel | **Delete** | Shell nav | FP-03; One Primary |
| 32 | Tertiary “More” disclosure wrapping milestones/QA | **Delete** | — | Compensates bad IA |
| 33 | Welcome modal include | **Delete** | — | Forbidden interrupt |
| 34 | Syllabus revision acknowledgement section | **Replace** | L0 Mission Primary **Continue** when ack required | Continuity |
| 35 | Multiple Primary-weight buttons | **Delete** | Exactly one Primary | DX-001 |
| 36 | Progress rings / streaks / badges / gamification | **Delete** | — | Explicit forbid (even if absent, stay off) |
| 37 | Feature promotion / marketing empty copy | **Delete** | — | Explicit forbid |
| 38 | Decorative card mosaic (secondary panels) | **Delete** | Lists L0–L2 | DX-001 cards policy |

---

## Explicit forbid list (DX-005A) — confirmation

| Forbidden content | Present in legacy? | Status |
|---|---|---|
| Large welcome messages | Yes (greeting + empty insights + modal) | Removed |
| Congratulations banners | Yes (day-complete / reflection cheer adjacent) | Removed |
| Motivational quotes | Soft (coach / educational tone) | Removed |
| Learning statistics | Yes (readiness %, this week facts) | Removed |
| Study streaks | No (keep off) | Stay off |
| Achievement badges | No (keep off) | Stay off |
| Progress rings | No (keep off) | Stay off |
| Gamification | Soft commitment theatre | Removed |
| Feature promotion | Yes (insights empty; Quick Actions) | Removed |
| Long explanations | Yes (MES / Mission Intelligence / panels) | Removed / relocated |
| Multiple primary buttons | Yes | One Primary |

---

## Estimated visual / decision reduction

| Measure | Legacy Student Home | Target Student Home | Δ |
|---|---|---|---|
| Distinct content sections | Hero + feedback + edu + 3 secondary + tertiary | 3 page sections (L0–L2) + shell | **~60%** fewer sections |
| Explanation layers above CTA | 6–10 | ≤2 | **~70–80%** |
| Metric / readiness tiles | 1–3 | 0 | **−100%** Home metrics |
| Primary-weight buttons | 2–5 competing | **1** | **~80%** |
| Card / panel containers | ~8–12 | 0–1 (optional L0 group) | **~90%** |
| Independent decisions (DX-003) | 4–7 | **1** | **~75–85%** |

---

## What is *not* removed from the product

Removal from **Student Home** is not deletion from Kwalitec.

| Capability | Lives at |
|---|---|
| Deep why / evidence / alternatives | Session disclosure / Insights policy surfaces |
| Readiness estimate | Journey (or dedicated progress) |
| Syllabus position story | Journey |
| Tutor explain | Session |
| Reflection / journal | Session complete + History / Journal |
| Weekly experience facts | Journey / Research (founder) — not Home |
| Defer / commitment policy | Session start policy if retained — not Home peer CTA |
| Choose Exam / Study Plan | Choose Exam (DX-005B) |
| History archive | History |
| Sensei naming | Once in Session if required by product language |

---

## Implementation caution

Do not CSS-hide legacy Home sections. Replace the template body and slim the Home view-model so unused MES/readiness/coach payloads are not required for first paint of Primary.
