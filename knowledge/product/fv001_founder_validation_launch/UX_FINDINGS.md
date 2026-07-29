# FV-001A — UX Findings

**Date:** 2026-07-28  
**Severity:** Critical · Major · Minor · Observation  
**Source:** Blind walkthrough only — no architecture justification.

---

## Critical

| ID | Finding | Evidence |
|---|---|---|
| UX-C01 | No self-serve registration; journey stops without coordinator credentials | Login invite-only copy; `/register` → 404 |
| UX-C02 | Uploaded curriculum PDFs show Failed; founder cannot trust extraction | Workspace document STATUS Failed; Preview 0 nodes |
| UX-C03 | Zero-setup publish journey cannot complete | Publish flash refuses incomplete/unapproved curriculum |
| UX-C04 | Mission/Session do not name a recognisable CS1 topic | “this topic”, “your topic”, “today's topic”, “Core methods” |
| UX-C05 | No Coach ask surface for Phase 15 | `/coach` 404; Help is orientation/tickets |
| UX-C06 | Console Home does not orient “prepare CS1” in ten seconds | Ops metrics / Platform Health 0% dominate |

---

## Major

| ID | Finding | Evidence |
|---|---|---|
| UX-M01 | Create Subject does not auto-open a workspace | “No workspaces yet” after successful create |
| UX-M02 | Advanced Studio tabs visible before any valid curriculum | PIPELINE, KNOWLEDGE GRAPH, EVIDENCE EXPLORER, ENTITY DETAILS |
| UX-M03 | First upload slot is CMP — syllabus easily misplaced | Slot order on Content Sources |
| UX-M04 | Session activities feel like hollow free-text prompts | “explain one key idea from Core methods”; vague supporting material |
| UX-M05 | Dual Console vs Student identity without clear mode for dogfooding founders | Post-login Console; Student via separate nav/URL |
| UX-M06 | Study Sensei branding implies mentor chat that does not exist | Home + Help vs no ask UI |
| UX-M07 | Estimated Knowledge on readiness card | Home readiness copy |
| UX-M08 | In-progress session not clearly resumable from Home | Left activity; Home still “Start Session” |

---

## Minor

| ID | Finding | Evidence |
|---|---|---|
| UX-m01 | Double period in readiness sentence | “next useful study step..” |
| UX-m02 | Document “UPLOADED BY 1” | Workspace document meta |
| UX-m03 | Wizard option cards awkward to select | Click interception / hesitation |
| UX-m04 | Trailing slash 404 on some student URLs | `/student/revision/` 404 vs `/student/revision` OK |
| UX-m05 | Help essay length before any Q&A | `/alpha/help` |

---

## Observations (no action required now)

| ID | Note |
|---|---|
| UX-O01 | Invite-only messaging is honest for Internal Alpha |
| UX-O02 | Publish refusal copy correctly protects students |
| UX-O03 | Revision empty state is disciplined and clear |
| UX-O04 | IFoA/CS1 support labels on Study Plan wizard are transparent |
| UX-O05 | Session step rail (Overview→Activity→Reflection→Summary) sets structure well |

---

## Cross-cutting themes

1. **Two products in one login** — Console operations vs Student study OS.  
2. **Setup honesty vs setup completion** — Studio explains blockers well but does not complete the founder’s job with uploaded files.  
3. **Action clarity vs content clarity** — Start Session is obvious; *what* you study is not.  
4. **Mentor metaphor without mentor surface** — Study Sensei / Coach gap.

---

**End of UX Findings**
