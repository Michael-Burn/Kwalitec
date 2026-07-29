# FV-001A — Prioritised Actions

**Date:** 2026-07-28  
**Rule:** Document issues before engineering. These are **recommendations from observed UX evidence**, not an authorisation to build new Educational Intelligence layers. Engineering under FV-001 remains gated by Critical/Major real-use blockers per `VALIDATION_PROTOCOL.md`.

---

## P0 — Must clear before claiming zero-setup founder journey

| # | Action | Clears | Notes |
|---|---|---|---|
| 1 | Decide and surface onboarding model: **invite-only** (with explicit coordinator path) **or** self-serve registration | LB-01 | If invite-only stays, Version 1 success criteria must stop claiming self-serve registration |
| 2 | Make upload → validation → preview produce a **human-readable curriculum tree** (or a plain failure with fix steps) | LB-02, LB-03 | Failed STATUS without explanation is a trust killer |
| 3 | Name the Mission and Session topic with real syllabus labels a CS1 candidate recognises | LB-04 | Home H1 / Mission title / session topic |
| 4 | Either ship a visible Coach/ask surface **or** remove Coach from Version 1 journey claims | LB-05 | Help ≠ Coach |
| 5 | Console empty-state: primary CTA “Create your first subject” / “Open Curriculum Studio” | LB-06 | Reduce ops noise on day one |

---

## P1 — High frustration

| # | Action | Clears |
|---|---|---|
| 6 | Auto-open workspace after Create Subject (or single combined flow) | UX-M01 |
| 7 | Hide PIPELINE / KNOWLEDGE GRAPH / EVIDENCE EXPLORER / ENTITY DETAILS until documents validate | UX-M02, terminology Critical |
| 8 | Clarify CMP vs Syllabus slots; prevent silent wrong-slot upload | UX-M03 |
| 9 | Label scaffolded free-text activities honestly; do not imply CMP exam practice | UX-M04 |
| 10 | Founder dogfood: explicit switch “Study as student” from Console | UX-M05 |
| 11 | Resume in-progress session CTA on Home | UX-M08 |
| 12 | Replace or explain “Estimated Knowledge” in plain language | UX-M07 |

---

## P2 — Polish

| # | Action | Clears |
|---|---|---|
| 13 | Fix readiness double-period typo | UX-m01 |
| 14 | Show uploader display name, not user id `1` | UX-m02 |
| 15 | Enlarge Study Plan wizard option hit targets | UX-m03 |
| 16 | Consistent trailing-slash routing for student pages | UX-m04 |
| 17 | Shorten Help orientation; lead with tasks | UX-m05 |

---

## Explicit non-actions (out of scope for this review)

- Do not redesign Educational Intelligence cores from this document alone.  
- Do not inflate Founder Validated CRI from this blind review — it is an acceptance walkthrough, not a soak journal.  
- Do not treat NO-GO as permission to invent parallel recommendation engines.

---

## Suggested re-review trigger

Re-run FV-001A when P0 items 1–5 have visible product evidence, using the same persona and zero-setup scenario.

---

**End of Prioritised Actions**
