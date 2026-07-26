# Feedback Register

**Programme:** EP-004 — Workstream 5  
**Updated:** 2026-07-24  
**Channels:** In-product founder feedback, check-ins, structured interviews (protocol week 4+)  
**Governing:** [`../private_beta/FEEDBACK_SYSTEM.md`](../private_beta/FEEDBACK_SYSTEM.md)  
**Rule:** Code every item to a category **and** preferably to M1–M9 / O1–O9 / educational surface. Decline Never-Build requests with Vision citation.

---

## Categories

| Code | Category | Use |
|---|---|---|
| BUG | Bug | Defect; wrong behaviour; data error |
| UX | UX | Navigation, clarity, overwhelm, copy |
| EDU | Educational | Honesty, guidance trust, Session/Reflection/Journey/Coach/Twin usefulness |
| OPS | Operational | Access, invites, support, analytics/privacy ops |
| FPRD | Future PRD | Requires approved PRD before behaviour change |

Severity: `blocker` | `confusing` | `suggestion`

---

## Collection themes (required interview / check-in coverage)

| Theme | Maps to |
|---|---|
| Usability | UX |
| Trust | EDU / Q3 |
| Navigation | UX |
| Coach usefulness | EDU (Coach surface) |
| Mission / Session usefulness | EDU / M2 / M4 |
| Reflection usefulness | EDU / M3 |
| Journey usefulness | EDU / M5 |
| Confusion points | UX / EDU |
| Feature requests | Triage → FPRD or decline |

---

## Register

| ID | Date | Source | Participant | Theme | Category | Severity | Summary | Metric / surface | Disposition |
|---|---|---|---|---|---|---|---|---|---|
| FB-001 | 2026-07-24 | Educational review baseline | Stage 0 composite | Trust / naming | EDU | confusing | Coach vs Mission/Session naming cohesion remains a trust risk | Coach / Session; Q2–Q3 | **Open** — copy governance; no algorithm change |
| FB-002 | 2026-07-24 | Educational review baseline | Stage 0 composite | Journey | EDU | suggestion | Journey quantitative claims provisional until production emit | M5; Journey; ADR-026 | **Open** — FPRD / ADR-026 programme; label provisional in scorecards |
| FB-003 | 2026-07-24 | Educational review baseline | Stage 0 composite | Twin | EDU | confusing | Twin existence ≠ perceived usefulness; risk of “made up” readiness | Twin; M8; Q3 | **Watch** — interview in Stage 1+; forbid marketing claim |
| FB-004 | 2026-07-24 | Protocol / product policy | N/A | Feature request | FPRD | suggestion | Recommendation-effectiveness claims / experiments | O8 excluded | **Declined for EP-004** — future PRD only |
| FB-005 | 2026-07-24 | Ops | N/A | Privacy | OPS | blocker (gate) | Expanded cohort blocked on Privacy Review signatures | Privacy / Stage 1 | **Open** — sign-off required |
| FB-006 | 2026-07-24 | Stage 0 dogfood | BETA-INT-001 | Session usefulness | EDU | suggestion | Today's Session remains the right primary learning object for validation | Mission/Session; M2/M4 | **Accepted** — measure; no redesign |
| FB-007 | 2026-07-24 | Stage 0 dogfood | BETA-INT-002 | Reflection | EDU | suggestion | Reflection completion measurable; body text must stay out of analytics | M3; privacy | **Accepted** — preserve privacy invariant |
| FB-008 | 2026-07-24 | Stage 0 dogfood | BETA-INT-003 | Navigation | UX | confusing | Orientation still needed for Journey vs History vs Revision | UX / onboarding | **Open** — reinforce onboarding checklist; no IA redesign in EP-004 |
| FB-009 | — | Reserved | — | Usability | UX | — | *Fill from Week 1 check-in* | — | Reserved |
| FB-010 | — | Reserved | — | Interview Final Test | EDU | — | “Did this help you study like a professional?” | Satisfaction / Q1 | Reserved (≥8 interviews target) |

---

## Category tallies (Stage 0 seed)

| Category | Count | Notes |
|---|---|---|
| BUG | 0 | No Stage 0 P0/P1 filed under EP-004 |
| UX | 1 (+ reserved) | Navigation orientation |
| EDU | 5 | Naming, Journey provisional, Twin trust, Session/Reflection fit |
| OPS | 1 | Privacy gate |
| FPRD | 1 | Recommendations excluded |

---

## Triage rules (recap)

1. Educational honesty / wrong next action → High (educational governance) — **no silent algorithm fix under EP-004**.  
2. Lost / unclear navigation → High experience priority; prefer onboarding/copy over new features.  
3. Polish → Medium/Low weekly batch.  
4. Vanity engagement / opaque AI / public launch → **Decline** (Vision Never-Build).

---

## Exit criteria (WS5)

| Criterion | Status |
|---|---|
| Themes cover usability → feature requests | COMPLETE |
| Categories Bug/UX/Educational/Operational/Future PRD | COMPLETE |
| Stage 0 items coded | COMPLETE |
| Interview sample ≥8 or 25% active | OPEN — Stage 1+ |
