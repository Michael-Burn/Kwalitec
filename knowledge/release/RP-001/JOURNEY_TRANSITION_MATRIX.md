# RP-001.2 — Journey Transition Matrix

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.2  
**Date:** 2026-07-28  
**Scope:** Every audited transition on the Alpha student journey (default production flags) plus conditional flag branches  
**Companion:** `END_TO_END_JOURNEY_CERTIFICATION.md`

---

## Legend

| Column | Meaning |
|--------|---------|
| **ID** | Transition identifier |
| **From → To** | Surfaces / routes |
| **Trigger** | User or system action |
| **Conditions** | Flags / data gates |
| **Next clarity** | Does the student know what to do next? (Clear / Conditional / Unclear) |
| **Cert** | Pass / Conditional Pass / Fail |

---

## A. Default Alpha path (production flags)

### A1. Authentication and first entry

| ID | From → To | Trigger | Conditions | Next clarity | Cert |
|----|-----------|---------|------------|--------------|------|
| T-01 | Unauthenticated → `/auth/login` | `@login_required` or direct | Always | Clear | Pass |
| T-02 | Login fail → Login | Invalid credentials | Always | Clear (retry) | Pass |
| T-03 | Login success → `/alpha/onboarding` | POST login | `AlphaOnboardingService.should_show` | Clear | Pass |
| T-04 | Login success → `/study-plan/wizard/1` | POST login | Onboarding done; no active plan; no Runtime C enrolment | Clear | Pass |
| T-05 | Login success → `/student/` | POST login | Onboarding done; active plan (or Runtime C) | Clear | Pass |
| T-06 | Login success → Founder Console | POST login | Founder user | Clear (non-student) | Pass (N/A student) |
| T-07 | Login (already auth) → canonical home | GET login | Authenticated | Clear | Pass |
| T-08 | Any → Login | POST logout | Always | Clear | Pass |
| T-09 | Login `?next=` unsafe → ignored | Open redirect attempt | Absolute / protocol-relative / encoded bypass | Clear (safe fallback) | Pass |

### A2. Product onboarding

| ID | From → To | Trigger | Conditions | Next clarity | Cert |
|----|-----------|---------|------------|--------------|------|
| T-10 | Onboarding → canonical home | POST complete | Always | Conditional (may then hit wizard) | Conditional Pass |
| T-11 | Onboarding → canonical home | POST skip | Always | Conditional (under-oriented) | Conditional Pass |
| T-12 | Onboarding → Help | Link | Always | Clear | Pass |
| T-13 | `/student/` → Onboarding | GET home | `should_show` | Clear | Pass |

### A3. Study plan wizard

| ID | From → To | Trigger | Conditions | Next clarity | Cert |
|----|-----------|---------|------------|--------------|------|
| T-14 | Wizard step *n* → *n+1* | POST valid | Steps 1–6 | Clear | Pass |
| T-15 | Wizard 7 → Review | POST valid | Step 7 | Clear | Pass |
| T-16 | Review → `/calibration/after-plan/<id>` | POST confirm | Runtime A plan created (default) | Clear | Pass |
| T-17 | Review → canonical home | POST confirm | Runtime C enrolment path (flag ON only) | Conditional | N/A default |
| T-18 | Wizard error → same / step 1–2 | Validation / missing curriculum | Error cases | Clear (flash) | Pass |
| T-19 | `/study-plan/` → wizard 1 or view plan | GET index | No plan vs active plan | Clear | Pass |

### A4. Calibration

| ID | From → To | Trigger | Conditions | Next clarity | Cert |
|----|-----------|---------|------------|--------------|------|
| T-20 | Calibration → `/student/?welcome=1` | Submit declarations | Valid plan | Clear | Pass |
| T-21 | Calibration → `/student/?welcome=1` | Beginner skip | POST skip | Clear | Pass |
| T-22 | Calibration → `/student/?welcome=1` | Persist failure | Soft-fail | Conditional (warning) | Conditional Pass |
| T-23 | Calibration → canonical home | Abandon | POST abandon | Conditional (no Twin) | Conditional Pass |
| T-24 | Calibration → home | Twin already exists | GET/POST | Clear | Pass |
| T-25 | Calibration → study plan index | Plan not found | Missing plan | Clear | Pass |
| T-26 | `/calibration/resume` → start or wizard | GET resume | Plan present or not | Clear | Pass |

### A5. Home, welcome, mission intelligence

| ID | From → To | Trigger | Conditions | Next clarity | Cert |
|----|-----------|---------|------------|--------------|------|
| T-27 | Calibration/entry → Home + welcome modal | Welcome eligible + `should_show` | After calibration paths | Clear | Pass |
| T-28 | Welcome dismiss → next or home | POST `/dashboard/welcome/dismiss` | Modal shown | Clear | Pass |
| T-29 | Welcome CTA → Home (not session) | “Start Today's Session” | Sole runtime: `canonical_session_entry_url` = home | Conditional (extra click) | Conditional Pass |
| T-30 | Home empty → stay / nav | No recommendation | Early / fail-open | Conditional | Conditional Pass |
| T-31 | Home day_complete → stay | Day finished | Commitment / experience state | Clear (“Return tomorrow”) | Pass |
| T-32 | Home → Mission Intelligence visible | Recommendation exists | ILE-004 compose | Clear | Pass |
| T-33 | Legacy `/dashboard/` → Home | GET | Sole runtime ON | Clear | Pass |
| T-34 | Legacy `/missions/` → Home | GET | Sole runtime ON | Clear | Pass |
| T-35 | Legacy `/settings/` → Profile | GET | Sole runtime ON | Clear | Pass |
| T-36 | Legacy `/analytics/` → History | GET | Sole runtime ON | Conditional (no charts) | Conditional Pass |

### A6. Commitment and session

| ID | From → To | Trigger | Conditions | Next clarity | Cert |
|----|-----------|---------|------------|--------------|------|
| T-37 | Home → `/session/<id>/overview` | POST `start_session` | CTA enabled; ports OK | Clear | Pass |
| T-38 | Home → Home (deferred) | POST `defer_commitment` | Defer reason | Clear | Pass |
| T-39 | Overview → Activity | POST `begin` | Session owned | Clear | Pass |
| T-40 | Activity → Activity | POST answer / advance | More items | Clear | Pass |
| T-41 | Activity → Reflection | POST advance (end) | No next item | Clear | Pass |
| T-42 | Reflection → Summary | POST continue | — | Clear | Pass |
| T-43 | Summary → Complete | Navigate | — | Clear | Pass |
| T-44 | Complete → Home | POST `finish` | Session owned | Clear | Pass |
| T-45 | Mid-session deep link → active surface | Resume redirect | Wrong surface URL | Clear (flash) | Pass |
| T-46 | Session error → Home | Missing/forbidden | Ownership | Clear | Pass |
| T-47 | Session finish → Home **without** commitment `mark_completed` | POST finish | V2 session path | **Unclear** for reflection chrome | **Fail** (continuity) |
| T-48 | Legacy mission complete → commitment completed | Legacy `/missions/` path | Sole runtime redirects away | N/A default | Fail-as-unreachable |
| T-49 | Home reflection ack → Home | POST `acknowledge_reflection` | `show_reflection` true | Clear | Pass (when shown) |
| T-50 | Revision begin → Session overview | POST `begin_revision` | Revision CTA | Clear | Pass |

### A7. Quick Check (default OFF)

| ID | From → To | Trigger | Conditions | Next clarity | Cert |
|----|-----------|---------|------------|--------------|------|
| T-51 | Session → Quick Check embed | Render overview/activity | Flags OFF → embed None | N/A | Pass (excluded) |
| T-52 | *(If ON)* Embed → QC start → … → return mission | QC flow | Flags ON | Clear | Requires delta cert |

### A8. Reflection, journal, timeline, history

| ID | From → To | Trigger | Conditions | Next clarity | Cert |
|----|-----------|---------|------------|--------------|------|
| T-53 | History → Decision Journal | Link | Always | Clear | Pass |
| T-54 | History → Educational Timeline | Link | Always | Clear | Pass |
| T-55 | Journal empty → Home | CTA | No entries | Clear | Pass |
| T-56 | Journal → Journal (reflect) | POST reflect | `can_reflect` + invite available | Clear | Pass |
| T-57 | Timeline empty → Journal | CTA | No beats | Clear | Pass |
| T-58 | Timeline ↔ Journal | Nav links | Always | Clear | Pass |
| T-59 | Home preview “Done reflecting” / “Skip” | Click spans | UJ presentation chrome; **non-functional** | **Unclear** | **Fail** (false affordance) |
| T-60 | Research check-in (optional) | Eligibility | RIP-001 separate from ILE-005 | Conditional | Conditional Pass |

### A9. Return next day and lifecycle

| ID | From → To | Trigger | Conditions | Next clarity | Cert |
|----|-----------|---------|------------|--------------|------|
| T-61 | Next-day login → Home | POST login | Plan + onboarding done | Clear | Pass |
| T-62 | Home deferred chrome retained | GET home | Prior defer | Clear | Pass |
| T-63 | Open session resume | Start/resume CTA or deep link | Mid-session | Clear | Pass |
| T-64 | Syllabus complete → revision ack UI | Lifecycle `show_completion_acknowledgement` | UI only on **legacy dashboard** | **Unclear / missing** | **Fail** |
| T-65 | Revision ack POST → Home | POST `/dashboard/revision/acknowledge` | If UI reachable | Clear | Pass (unreachable under sole) |

---

## B. Sole-runtime redirect matrix

| Legacy URL | Sole ON | Sole OFF (rollback) |
|------------|---------|---------------------|
| `/dashboard/` | → `student.home` | Dashboard home (+ revision ack UI) |
| `/missions/` | → `student.home` | Mission list / start |
| `/analytics/` | → `student.history` | Analytics charts |
| `/settings/` | → `student.profile` | Settings landing |

---

## C. Conditional journeys (flags OFF in production)

### C1. Quick Check + Adaptive Assessment (+ optional Contextual Framing)

```
session.overview|activity
  → [embed entry card]
  → POST /adaptive-assessment/quick-check/start
  → introduction → begin → question (+ hint/pause/resume)
  → reflection → completion → return_to_mission
  → session.overview|activity
```

| Gate | Default | If enabled |
|------|---------|------------|
| Student sees QC | No | Yes (subject/cohort allow-lists apply) |
| Sensei framing card | No | If `KWALITEC_CONTEXTUAL_FRAMING=1` |
| Alpha claim allowed | Must not claim | Only after delta certification |

### C2. Unified Journey (`KWALITEC_UNIFIED_JOURNEY`)

| Aspect | OFF (prod) | ON |
|--------|------------|-----|
| Nav labels | Home · Journey · Revision · History · Settings | Today · Planning · Exam Readiness · Revision · Archive · Help |
| Home chrome | Today's Mission | Journey stage / timeline attributes |
| Guided reflection controls | Non-functional preview spans | Journey-stage presentation (still verify interactivity before claiming) |
| Re-certify | — | Required (nav a11y + terminology) |

### C3. Experience Feedback (`KWALITEC_EXPERIENCE_FEEDBACK`)

Requires Unified Journey ON. Adds Home “Your Journey” factual section. Default OFF.

### C4. Runtime C (`KWALITEC_RUNTIME_C_ENROLMENT` + published subject discovery)

| Aspect | OFF (prod) | ON (pilot) |
|--------|------------|------------|
| Post-wizard | Calibration → Home | May enrol Runtime C → Home (skip calibration) |
| Home CTA | `start_session` | May `complete_runtime_mission` |
| Fail-open | — | Errors fall back to Runtime A composition |

---

## D. Transition certainty summary

| Clarity | Count (default path material transitions) |
|---------|------------------------------------------:|
| Clear | Majority (T-01–T-46, T-49–T-58, T-61–T-63, etc.) |
| Conditional | Welcome CTA, empty Home, skip/abandon, analytics→history, dual chrome exits |
| Unclear / Fail | **T-47** commitment completion on V2 finish; **T-59** fake reflection controls; **T-64** revision ack unreachable |

---

## E. “What am I supposed to do now?” hotspot list

1. Empty Home without recommendation (T-30)  
2. Welcome CTA lands on Home, not session (T-29)  
3. Non-interactive reflection preview (T-59)  
4. Missing Home post-session commitment reflection after V2 finish (T-47)  
5. Syllabus-complete with no acknowledgement UI (T-64)  
6. Dual chrome after Help/Settings/Wizard returns to EOS  
7. Thin Revision page when adaptive authority OFF  

---

## Document control

Documentation only. Flag enablement requires matrix delta, not silent scope expansion.
