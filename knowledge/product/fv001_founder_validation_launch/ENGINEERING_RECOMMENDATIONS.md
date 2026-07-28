# FV-001 — Engineering Recommendations

**Programme:** FV-001 — Founder Validation & Dogfooding  
**As of:** 2026-07-28  
**Gate:** Critical or Major blockers from real sessions only ([`VALIDATION_PROTOCOL.md`](VALIDATION_PROTOCOL.md) §6)

---

## Current recommendation

# **No product engineering authorised**

| Check | Result |
|---|---|
| Critical blockers from sessions | **0** |
| Major blockers from sessions | **0** |
| Speculative / hypothetical issues | **Forbidden — none filed** |
| CQ-007 Minor residuals (B-01…B-07) | Watch only — not promoted |
| FV-001 instrumentation / workflows | **Authorised** (programme scope) |

**Rationale:** Observational instrumentation and validation workflows are authorised under FV-001 programme scope. Product/architecture fixes remain blocked until Critical or Major blockers appear in real sessions. Authorising educational or UX redesign without session evidence would reintroduce assumption-driven engineering, which FV-001 exists to prevent.

---

## Authorised under programme scope (not product fixes)

| ID | Summary | Status |
|---|---|---|
| FV-INST-01 | Founder validation metrics service + `flask fv-metrics` | Done |
| FV-INST-02 | Hook telemetry on enrolment / evidence paths | Done |
| FV-INST-03 | Version 1 journey workflow catalogue | Done |
| FV-DOCS-01 | Issue log, journal, metrics, explainability, UX, acceptance artefacts | Done |

---

## Authorised product backlog (when justified)

| ID | Severity | Summary | Session evidence | Domains | Recommended action | Status |
|---|---|---|---|---|---|---|
| — | — | _None_ | — | — | — | — |

---

## Explicitly not recommended

- Polish passes against unobserved Minor residuals  
- Redesign, educational engine expansion, recommendation / Twin / AI changes  
- Item banks or Version 2 content work under the guise of “validation fixes”  
- Inflating Engineering CRI or creating `cri-*` tags from this document  

---

## Update rule

When a Critical or Major row appears in [`REAL_WORLD_BLOCKER_REGISTER.md`](REAL_WORLD_BLOCKER_REGISTER.md):

1. Add a row above with session citation.  
2. Set **Status** to Proposed → Authorised (Founder Review) → In progress → Done.  
3. Note Engineering CRI impact only after the fix ships with evidence.  

---

**End of Engineering Recommendations**
