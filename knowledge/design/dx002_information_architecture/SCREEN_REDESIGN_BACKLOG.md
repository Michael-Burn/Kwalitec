# Screen Redesign Backlog

**Programme:** DX-002  
**Release Candidate:** `RC-2026.07.29-01`  
**Nature:** Architecture backlog for later DX programmes — **no implementation in DX-002**.

Items are ordered within priority. Each item states outcome, not visual style.

---

## P0 — Before Beta

### B-001 · Console Overview → decision surface
- **Screen:** G1 Console Home  
- **Outcome:** Answers “What should I publish or fix next?” with one Primary and a short work list.  
- **Remove:** Platform Summary KPI grid; build/timezone in hero; multi-primary Quick Actions.  
- **Depends on:** KPI + Nav audits  
- **DX follow-on:** Visual shell polish after IA

### B-002 · Curriculum Workspace → stage workspace
- **Screen:** H7  
- **Outcome:** Next step + one stage Primary + blockers + stage-needed content only.  
- **Remove:** Always-on readiness KPI triad; 9-tab default; entity id entry; embedding KPIs; ms timings; Actions button grid.  
- **Introduce:** ≤3 stage panels; Advanced disclosure for diagnostics.  
- **Depends on:** Publication pipeline stages already in product

### B-003 · Collapse Curriculum hubs
- **Screens:** H1–H6  
- **Outcome:** Subjects catalogue + Studio workspace list with filters (Review / Publishing / Versions / Quality as filters, not pages).  
- **Remove:** Duplicate workflow essays; “Open Curriculum Studio” CTA from every hub.  
- **Nav:** Drop Review Queue, Publishing, Versions, Quality from primary sidebar.

### B-004 · Student Home density cut
- **Screen:** D1  
- **Outcome:** Title + one why + duration + one Primary (+ resume/reflection states).  
- **Remove/relocate:** Readiness/countdown cards; trust chrome; stacked paraphrases; competing secondary CTAs.  
- **Keep:** Educational explainability at L1 once.

---

## P1 — During Alpha

### B-010 · Unify Progress / Memory
- **Screens:** D4, D5, D6  
- **Outcome:** One nav item with Archive / Journal / Timeline views.  
- **Remove:** History epistemology essay; KPI cards; duplicate CTAs.

### B-011 · Console nav collapse
- **Chrome:** `COMMAND_CENTRE_NAV` / secondary  
- **Outcome:** ≤6 primary destinations; reports under Settings.  
- **Align labels:** Students (not Participants).

### B-012 · Login landing restraint
- **Screen:** A1  
- **Outcome:** Brand + one value sentence + Sign in.  
- **Remove:** Six bullets; decorative shapes; repeated alpha theatre.

### B-013 · Help becomes unblock tool
- **Screen:** B2  
- **Outcome:** Search + quick actions + short topics.  
- **Remove:** Journey ontology essays after B-010.

### B-014 · Kill welcome modal
- **Screen:** J2  
- **Outcome:** No modal competing with Home.  
- **Remove:** Welcome modal trigger path.

### B-015 · Study Plan review honesty
- **Screen:** C4  
- **Outcome:** Confirm only user-set fields; defaults one quiet line.  

### B-016 · Journey / Revision calm
- **Screens:** D2, D3  
- **Outcome:** No second Home personality; lists over card mosaics.

### B-017 · Attention / Support as queues
- **Screens:** G3, G4  
- **Outcome:** List-first queues; metrics only as row counts.  
- **Link from:** Overview (B-001), not duplicate KPI cards.

---

## P2 — Improve later

### B-020 · Profile / Settings card demotion
### B-021 · Onboarding single Primary
### B-022 · Session overview / reflection copy trim
### B-023 · Assessment chrome consistency
### B-024 · Nest Console report pages under Settings IA
### B-025 · Choose Exam list alternative to radio cards
### B-026 · Delete orphan wizard templates from product inventory
### B-027 · Calibration copy restraint
### B-028 · Subject support gate: blocker only

---

## P3 — Already near DX-001 intent

### B-030 · Session activity — preserve focus; minor card chrome only
### B-031 · Session complete — single exit
### B-032 · Confirm modal — keep
### B-033 · Vision Journal — low product priority; leave until ops IA settles
### B-034 · Error pages — keep minimal

---

## Guardian / process backlog (non-screen)

### B-040 · Update `UI_GUARDIAN.md` to require DX-001 corpus + Premium Checklist + this IA one-question table before UI changes  
*(Recommended in DX-001; owned as process follow-on — may land with DX-003)*

### B-041 · Document legacy sidebar as non-product for agents

---

## Suggested programme sequencing

```
DX-002 (this)     IA law
    ↓
DX-003            Content strategy & density (copy + hierarchy cuts)
    ↓
DX-004            Navigation & shell restructure (nav trees)
    ↓
DX-005+           Visual token remap & component execution per P0 screens
```

Exact programme IDs may vary; **do not restyle CSS before B-001–B-004 structural decisions are accepted.**
