# PX-007 — Founder dogfood findings (WS-11)

**Date:** 2026-08-04  
**Method:** Structured code-backed end-to-end audit of sole-runtime student surfaces + aggregate regression (157 passed) + targeted defect correction.  
**Authority:** PX-B-052 · Educational Content Freeze · EF-001  

## Classification rule

| Class | Meaning |
|-------|---------|
| Critical | Blocks primary path trust or safety |
| Major | Material premium / identity / honesty break on default student paths |
| Minor | Friction or incompleteness; does not block certification if owned |
| Cosmetic | Non-student or comment-level only |
| Idea | Not a bug → Version 1.1 backlog |

## Finding counts (post-correction)

| Severity | Count |
|----------|------:|
| Critical | 0 |
| Major | 0 |
| Minor | 6 |
| Cosmetic | 2 |

## Closed this programme

| ID | Was | Surface | Fix |
|----|-----|---------|-----|
| PX7-001 | Major | Feedback | Student-visible “Internal Alpha” → Private Beta / Kwalitec microcopy |
| PX7-002 | Major | Feedback | “Closed Beta” eyebrow → `student_release_label` / Private Beta |

## Open Minor / Cosmetic (owned)

| ID | Severity | Surface | Description | Disposition |
|----|----------|---------|-------------|-------------|
| PX7-003 | Minor | Settings | Dual chrome: premium `student.profile` hub vs legacy `/settings/*` subpages | V1.1 backlog |
| PX7-004 | Minor | Settings | Session-scoped study-goal honesty less visible on premium hub | V1.1 / carry PX6-R3 |
| PX7-005 | Minor | Settings | “Not set” for study days / session length when prefs unset (exam label OK) | Accept when unset |
| PX7-006 | Minor | Study plan | Plan skeleton macro visually-hidden on empty list | Accept / transition covered by nav skeleton |
| PX7-007 | Minor | Session | Focus mode disabled until JS enables | V1.1 hide-until-ready |
| PX7-008 | Minor | Mobile | Founder-only Curriculum Health footer link on dual-role accounts | Expected RBAC |
| PX7-009 | Cosmetic | Nav module | Docstring still says “Education Operating System” | Comment-only |
| PX7-010 | Cosmetic | Settings URL | `/settings/internal-alpha` slug retained | V1.1 optional alias |

## Ideas → Version 1.1 backlog (not bugs)

- Account-durable daily study goal (`PX6-R3`)  
- Full icon library migration (`PX-B-051`)  
- Self-service password reset backend (`PX3-R5`)  
- Unify settings subpages into premium hub  
- axe/Lighthouse CI gate (`PX4-R2`)  
- Recorded VoiceOver/NVDA pass (`PX4-R3`)  
- LIVE Core Web Vitals field measure (`PX6-R2`)  
- Coach panel contract if Coach returns (`PX4-R5`)  

## Chrome growth / fatigue (PX-B-052)

- Home secondary `<details>` accumulate for established density — calm defaults; monitor multi-week noise.  
- Session complete demotes heavy report behind disclosure — correct proportion.  
- Help Centre is long-form before actions — thorough; mobile scroll fatigue possible.  
- Footer carries version + Private Beta + Report issue (+ Switch Experience for dual-role).  
- No S1 chrome-growth reopen observed on primary path after Phases 1–4.

## Dogfood rubric (experience confidence — provisional)

| Dimension | Score (1–5) | Notes |
|-----------|------------:|-------|
| Chrome trust | 4 | Package-path chrome contracts held in regression |
| Next-action clarity | 5 | Single primary CTA on Home |
| Emotional tone | 4 | Gap/exam calm; no pass promises in celebration |
| Help usefulness | 4 | FAQ + support; feedback identity closed |
| Celebration honesty | 5 | Research demoted; no pass promises |
| **Mean** | **4.4** | Meets M10 ≥ 4.0 provisional |

## Educational honesty

No educational package body changes. No selection/Twin/Runtime redesign. Celebration and diligence copy forbid pass promises.
