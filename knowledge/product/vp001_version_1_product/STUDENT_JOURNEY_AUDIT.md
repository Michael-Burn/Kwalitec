# VP-001 — Student Journey Audit

**Programme:** VP-001 — Version 1 Product Completion  
**Date:** 2026-07-28  
**Status:** Complete (audit artefact)

---

## 1. Purpose

Map the complete Version 1 learner journey and every interaction with the
Educational Intelligence Platform (EI-004…EI-007 → EX-001 → RI-001 → LP-001).

---

## 2. Preferred authority chain

```
Published Curriculum (CKG)
  → SCI (EI-004) via LP-001 onboard
  → Evidence (EI-005) via LP-001 process_evidence
  → Twin Beliefs (EI-006)
  → Educational Decisions (EI-007)
  → Experience Models (EX-001)
  → Runtime Integration (RI-001)
  → Surface adapters → Student UI
```

No educational reasoning may live in presentation. Runtime A remains Temporary
compatibility when SCI + decisions are absent.

---

## 3. Journey map

| Stage | Canonical path | EI Platform interaction | Authority |
|-------|----------------|-------------------------|-----------|
| **Account creation** | Admin / `flask create-admin` / StartupService (no public registration) | None | N/A (security law) |
| **Login** | `auth.login` → Alpha onboarding gate or canonical home | None | Presentation only |
| **Product onboarding** | `alpha.onboarding` | None (presentation gate) | Presentation |
| **Study plan wizard** | `study_plan.wizard` → `review_post` | **LP-001 `onboard_after_enrolment`** when published CKG edition exists | Write path → EI |
| **Published enrolment** | `FounderStudentEnrolmentBridge.enrol` (Runtime A or C) | **LP-001 onboard** after successful enrol | Write path → EI |
| **Calibration** | `calibration.start` | Legacy Twin birth (Runtime A); SCI already created by LP when edition exists | Temporary / additive |
| **Home / Dashboard** | `/student/` (legacy `/dashboard` redirects under sole runtime) | **RIS** via RecommendationAdapter + `has_educational_intelligence` fork | Preferred Authority when SCI+decisions |
| **Daily Mission** | Home mission chrome; legacy `/missions` redirects | **RIS** `DAILY_MISSION` framing (legacy dual-run); Home via recommendation bridge | Preferred Authority |
| **First / ongoing study** | `/session/<id>/…` | **RIS** `STUDY_SESSION` briefing on overview; **LP-001 evidence** on answer + complete | Preferred Authority + write refresh |
| **Coach** | Home chrome + `tutor/explain-mission` | **RIS** `COACH` metadata on IntelligentTutorService | Preferred Authority metadata |
| **Revision** | `/student/revision` | **RIS** `REVISION_PLANNER` via RevisionService (Adaptive fallback) | Preferred Authority |
| **Progress / Journey / History** | `/student/journey`, `/student/history` | Readiness / journey read models (not recommendation authority) | Read models (RI-001 unchanged) |
| **Notifications** | Profile `notifications_enabled` only | No delivery surface in V1 | Out of HTTP scope |

---

## 4. Surface × EI interaction matrix

| Surface | Read (RIS / EX) | Write (LP) | Notes |
|---------|-----------------|------------|-------|
| Dashboard / Home | Yes | Via enrolment | Recommendation bridge |
| Daily Mission | Yes (framing) | Persistence still PlanningService | Temporary compatibility for ORM |
| Study Session | Yes (briefing) | Evidence on answer/complete | Fail-open evidence hook |
| Revision Planner | Yes | — | Adaptive Temporary compatibility |
| Coach | Yes (metadata) | — | Does not replace AP-002 pipeline |
| Progress | Read models only | — | Not ranking authority |
| Notifications | — | — | No V1 delivery UI |

---

## 5. Gaps closed by VP-001

| Gap (pre-VP-001) | Resolution |
|------------------|------------|
| LP-001 not HTTP-wired | Enrolment hooks on wizard + bridge |
| Session never recorded LEE / refreshed EI | Evidence hook on answer + complete |
| Revision Planner unused RIS adapter | RevisionService RIS-first |
| Study Session unused RIS adapter | Session overview briefing overlay |

---

## 6. Remaining Temporary compatibility

- Runtime A recommendation / planning when no published CKG edition / SCI
- Mission ORM create/complete on PlanningService / MissionService
- Coach primary speech still AP-002 / Twin context with RIS metadata attached
- Notifications product surface deferred
- Public registration remains intentionally closed

---

**End of Student Journey Audit**
