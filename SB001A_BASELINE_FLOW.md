# SB-001A — Baseline Flow

**Programme:** SB-001A Baseline Integration & Runtime Bridge  
**Date:** 2026-07-31

---

## Student-visible flow

```text
Choose Exam → Exam Date → Study Availability
        ↓
Baseline (one question per screen)
  1 Experience
  2 Curriculum position (+ topic picker if continue)
  3 Exam history (+ optional mark)
  4 Objective
  5 Confidence
  6 Confirm
        ↓
Twin birth (existing Builder)
        ↓
Runtime A Study Plan  OR  Runtime C enrol
        ↓
Home / Today's Mission
```

## Returning student

If a complete Baseline exists for the subject:

- Do **not** re-ask questions
- Show current position, study phase, objective
- Offer **Restart Baseline** (history preserved)

## Progressive disclosure

- One decision per screen
- Progress indicator (`Baseline N of 6`)
- Back returns to previous step (or availability from step 1)
- Autosave after each POST
- Confirm summarises before finalize

## Educational reasoning

Baseline is a tutor intake conversation: meet the student where they are, then plan. Declarations are self-assessed priors (`self_declared` / `thin`), never Estimated Knowledge or mastery.
