# CQ-003 — Daily Habit Audit

**Programme:** CQ-003 — Daily Habit Fit  
**Date:** 2026-07-28  
**Path audited:** Production sole-runtime (`KWALITEC_V2_SOLE_RUNTIME=1`) founder study evening  
**Method:** Code + template inspection; CQ-002 residual inventory; journey before / during / after

---

## 1. Study-evening journey map

```
Before (open delay)
  Login → (onboarding/plan gates) → Student Home
  Friction: hero density; Start wording when already mid-session;
            commitment chrome before return

During (leave mid-session)
  Activity / Reflection / Summary
  Friction: brand Home exit; Quick Check fork; multi-step advance

After interruption (fail to return)
  Home again with in_progress session
  Friction: “Start” label; POST re-commitment; no deep link (without UJ)

After completion (return tomorrow)
  day_complete messaging; next mission
  Continuity copy OK; no streak (by policy — keep)
```

---

## 2. Friction inventory (habit lens)

| ID | Moment | Friction | Severity | V1 fix? |
|---|---|---|---|---|
| H01 | Return mid-session | CTA still “Start Session” without Unified Journey | **Critical** | Yes |
| H02 | Return mid-session | Resume via POST start re-records commitment | **Critical** | Yes |
| H03 | Return mid-session | Full start-time MES stack (Why / Why now / Next / commit) | **Major** | Yes (suppress on resume) |
| H04 | Revision entry | Lands on Overview; Home path auto-begins Activity | **Major** | Yes |
| H05 | Quick actions | “Resume” href = `/student/` not session URL | **Minor** | Yes |
| H06 | Evening open (fresh) | Hero density 10–14 blocks (CQ-002 F08) | **Med** | Partial — resume path only |
| H07 | Mid-session leave | Brand link to Home (no confirm) | **Med** | Deferred |
| H08 | Mid-session | Quick Check parallel path | **Med** | Deferred (V2/optional) |
| H09 | Next-day return | No streak on Home | Policy | **No** (anti-shame) |
| H10 | Scarce time | `preferred_session_minutes` not echoed at entry | **Med** | Deferred (needs prefs wiring) |

---

## 3. Delay / leave / abandon reasons (founder)

| Reason class | Examples from audit | Addressed in CQ-003? |
|---|---|---|
| Delay opening | Dense Home before CTA; unclear whether session already open | Partial (resume clarity) |
| Leave during session | Accidental Home nav; cognitive fork (Quick Check) | No (deferred) |
| Fail to return after interrupt | “Start” implies restart; re-commitment friction | **Yes** |
| Abandon for ops reasons | Extra Overview click on Revision; empty/dead paths | Revision yes; empty closed in CQ-002 |

---

## 4. What already works (habit enablers)

- Session `resume_redirect_if_needed` restores active surface on any session GET.
- CQ-002 Home auto-begin → Activity (one commitment click).
- Duration single-source; day_complete and continuity reflection copy.
- Honest “Not today” without streak shame.

---

## 5. Audit verdict

**CR2 remains Weak** primarily because **interrupt recovery on default Home** still feels like starting over. Closing Continue labelling, deep-link resume, resume-hero lightness, and Revision auto-begin should move CR2 within Emerging without Version 2 habit mechanics.

---

**End of Daily Habit Audit**
