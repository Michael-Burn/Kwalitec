# DX-002 Executive Summary

**Programme:** DX-002 — Product Information Architecture Review  
**Status:** Complete  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01` (Alpha Candidate 1)  
**Implementation:** None (architecture documentation only)

---

## Verdict

Kwalitec’s product surfaces mostly know their missions — Student Home answers “what should I study next?”, Choose Exam answers “what can I begin studying?”, Session answers “what do I practice now?” — but **information architecture currently undermines those missions** through card/KPI theatre, duplicate navigation, tutorial copy, and screens that answer more than one primary question.

DX-001 set the design law. DX-002 finds that **no primary surface yet meets that law as shipped**. The highest leverage work before Beta is not new colour tokens — it is collapsing overloaded workspaces, cutting decorative metrics, and making every screen answer exactly one question.

---

## What was reviewed

| Domain | Screens / shells audited |
|---|---|
| Founder Console | Home, Search, Attention, Support, Findings, Students, Settings, secondary ops/analytics surfaces, Vision Journal |
| Curriculum Authority | Studio dashboard, Subjects / Review / Publishing / Versions / Quality hubs, Workspace |
| Student EOS | Home, Journey, Revision, History, Decision Journal, Educational Timeline, Profile |
| Planning | Choose Exam wizard (4 steps), Review / Begin Learning, Study Plan view/list/edit |
| Learning loop | Session overview → activity → reflection → summary → complete; Assessment / Quick Check embeds |
| Entry & system | Login, Alpha onboarding, Help, Settings sections, Calibration, errors, modals |
| Navigation | Console primary + secondary, Student feature + unified-journey modes, legacy sidebar, breadcrumbs, CIP tabs |

**Global search:** Console only. **Notifications centre:** Absent (flash + preferences only).

---

## Critical findings

1. **Curriculum Studio Workspace fails one-purpose** — Next step, full workflow stepper, three readiness KPI cards, upload cards, 7-stage processing timeline, **nine review tabs** (including entity IDs and embedding metrics), and a multi-button Actions grid compete in one scroll. Premium score: **2/10**.
2. **Console Home is an analytics dashboard**, not a decision surface — dual KPI grids (“Attention Required” + “Platform Summary”), multiple Primary-weight buttons, build stamps and timezone policy in the hero. Premium score: **3/10**.
3. **Curriculum hubs duplicate each other** — Subjects, Review Queue, Publishing, Versions, Quality are filtered tables of the same workspace list with repeated workflow essays and an “Open Curriculum Studio” CTA that does not match the hub’s claimed job.
4. **Student Home has the right question but too much answer** — Greeting, Study Sensei narrator, eyebrow, title, status, duration, why, benefit, coherence, alternatives, readiness/countdown cards, and defer affordances stack above the single Start CTA.
5. **History / Decision Journal / Educational Timeline** require Help essays to explain their differences — IA failure deferred to content.
6. **Console navigation is oversized** — 10 primary + 13 secondary destinations; several expose engineering concerns (Runtime Health, Evidence Gates, System Operations) as peer product destinations.
7. **Forbidden patterns are systemic** — card overload, decorative KPIs, tutorial paragraphs, welcome messages, implementation terminology (`ent-…`, retrieval profiles, ms timings), multiple primary buttons.

---

## Target architecture (summary)

Two products, two shells, one mission each:

| Shell | Product job | Home question |
|---|---|---|
| **Student** | Learn for an exam | What should I study next? |
| **Console** | Publish curriculum & run Alpha | What should I publish or fix next? |

Everything else is a **workspace**, **wizard**, **catalogue**, **report**, or **settings** surface — not a “dashboard” unless monitoring is the sole purpose.

---

## Priority for redesign programmes

| Priority | Focus |
|---|---|
| **P0** | Console Home · Curriculum Studio Workspace · Curriculum hub consolidation · Student Home density |
| **P1** | History/Journal/Timeline merge or clarification · Console nav collapse · Login landing · Help · Study Plan review |
| **P2** | Secondary Console reports · Settings · Onboarding · Assessment chrome |
| **P3** | Session activity core · Auth form · Confirm modal (already focused) |

---

## Estimated complexity reduction

If DX-003–DX-005 execute the backlog:

| Lever | Estimated reduction |
|---|---|
| Visible primary nav destinations (Console) | ~10 + 13 → ~6 primary + ops under Settings |
| Curriculum hub pages | 6 → 2 (Catalogue + Studio) |
| Workspace L0 chrome | ~60% fewer competing blocks above the stage action |
| Student Home L0 copy blocks | ~40–50% fewer simultaneous explanation layers |
| KPI cards product-wide | Default none; keep only decision-changing counts |

**Overall UI complexity (cognitive competing elements on primary paths): ~35–45% reduction** without removing educational capabilities — by relocating detail behind progressive disclosure.

---

## What DX-002 does not do

- No CSS, tokens, or component implementation  
- No route deletion in code  
- No copy rewrite in templates (that is DX-003)  
- No visual redesign (later DX programmes)

---

## Proceed to

**DX-003 — Content Strategy & Information Density Reduction**, using this IA as binding input: one question per screen, L0–L3 maps, and the redesign backlog.
