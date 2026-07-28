# RP-001.1 — Capability Matrix

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.1  
**Date:** 2026-07-28  
**Authority:** `ALPHA_PRODUCT_INVENTORY.md`

---

## Legend

| Maturity | Meaning |
|----------|---------|
| Prototype | Code stubs / flags without student routes |
| Implemented | Built; may be flag-off or partial |
| Integrated | Wired into EOS / Alpha paths |
| Certified | Programme or control plane certified |
| Alpha Candidate | Intended primary Alpha student use |

| Release | Meaning |
|---------|---------|
| Ready | Include in Alpha without further product work |
| Ready with Conditions | Include only with disclosed conditions |
| Not Ready | Exclude from Alpha default / do not claim |

| Prod | Production (`render.yaml`) student exposure |
|------|---------------------------------------------|
| ON | Reachable in production Alpha posture |
| OFF | Flag-off, redirected, or not implemented |
| COND | Depends on Twin / recommendation presence / eligibility |

---

## Matrix

| ID | Capability | Owner | Maturity | Flag (default) | Student Visible | Prod | Nav Entry | Release |
|----|------------|-------|----------|----------------|-----------------|------|-----------|---------|
| CAP-01 | Authentication | auth | Alpha Candidate | — | Yes | ON | `/auth/login` | Ready |
| CAP-02 | Onboarding | ALPHA-001 | Integrated | — | Yes | ON | `/alpha/onboarding` | Ready with Conditions |
| CAP-03 | Student Home | EP-007 / EP-008 / ILE-004 | Alpha Candidate | Sole runtime ON | Yes | ON | `/student/` | Ready |
| CAP-04 | Daily Mission Intelligence | ILE-004 | Alpha Candidate | — | COND | ON | Home embed | Ready |
| CAP-05 | Journey | Student Experience | Integrated | Journey bridge optional | Yes | ON | `/student/journey` | Ready |
| CAP-06 | Revision | Student Experience | Implemented | Adaptive auth OFF | Yes | ON* | `/student/revision` | Ready with Conditions |
| CAP-07 | History | Student Experience | Integrated | History bridge optional | Yes | ON | `/student/history` | Ready |
| CAP-08 | Decision Journal | ILE-002 | Alpha Candidate | — | Yes | ON | `/student/decision-journal` | Ready |
| CAP-09 | Educational Timeline | ILE-003 | Alpha Candidate | — | Yes | ON | `/student/educational-timeline` | Ready |
| CAP-10 | Educational Feedback Loop | ILE-005 | Alpha Candidate | — | COND | ON | Journal reflect | Ready |
| CAP-11 | Mission Commitment | EP-008.3 | Alpha Candidate | — | Yes | ON | Home POSTs | Ready |
| CAP-12 | Session Experience | V2-019 | Alpha Candidate | Durable ON | Yes | ON | `/session/<id>/…` | Ready |
| CAP-13 | Quick Check | ILE-001B/C | Implemented | Adaptive+QC OFF | COND | OFF | Quick-check routes | Ready with Conditions |
| CAP-14 | Contextual Framing | ILE-001C | Implemented | Framing OFF | COND | OFF | Within Quick Check | Ready with Conditions |
| CAP-15 | Learning Check `/assessment` | Assessment Delivery | Implemented | — | Orphan | ON | `/assessment/` | Ready with Conditions |
| CAP-16 | Study Plan | V1 Study Plan | Alpha Candidate | Discovery OFF | Yes | ON | `/study-plan/` | Ready with Conditions |
| CAP-17 | Calibration | Calibration / EP-001.1 | Integrated | EI internal alpha ON | Yes | ON | `/calibration/…` | Ready |
| CAP-18 | Student Profile | Student Experience | Integrated | — | Yes | ON | `/student/profile` | Ready with Conditions |
| CAP-19 | Settings Subpages | V1 settings | Integrated | — | Yes | ON | `/settings/*` | Ready with Conditions |
| CAP-20 | Help & Alpha Feedback | ALPHA-001 | Integrated | — | Yes | ON | `/alpha/help` | Ready |
| CAP-21 | Product Check-in | RIP-001 | Integrated | — | Yes | ON | `/research/checkin` | Ready with Conditions |
| CAP-22 | Welcome / Revision Ack | PX-003 | Integrated | — | COND | ON | Home modal | Ready |
| CAP-23 | Tutor Explain Mission | TUTOR-001 | Implemented | Twin not in Render | COND | COND | Home POST | Ready with Conditions |
| CAP-24 | Navigation (EOS) | DEP-003 | Alpha Candidate | Unified Journey OFF | Yes | ON | Global chrome | Ready |
| CAP-25 | Accessibility | PX / ILE-001A+ | Integrated | — | Yes | ON | Cross-cutting | Ready with Conditions |
| CAP-26 | Feature Flags | V2 / EI / Adaptive | Certified | Meta | Indirect | ON | Ops/env | Ready |
| CAP-27 | Unified Journey Chrome | P2-MS001–004 | Implemented | Unified OFF | COND | OFF | Nav replace | Not Ready |
| CAP-28 | Experience Feedback Home | P2-MS008 | Implemented | Feedback OFF | COND | OFF | Home section | Not Ready |
| CAP-29 | Runtime C Panel | PX-001 / PI-002A | Implemented | Runtime C OFF | COND | OFF | Home/Journey embed | Not Ready |
| CAP-30 | Legacy Dashboard/Missions/Analytics | V1 Runtime A | Integrated (rollback) | Sole redirects | Dual-run | OFF† | Redirected | Not Ready |
| CAP-31 | Notifications | — | Prototype | — | No | OFF | — | Not Ready |
| CAP-32 | Progress Surfaces (composite) | Cross-cutting | Integrated | Bridges vary | Yes | ON | Distributed | Ready |

\* Page ON; revision **content** quality conditional on adaptive port.  
† Routes registered; production sole runtime redirects to EOS.

---

## Counts

| Release recommendation | Count |
|------------------------|------:|
| Ready | 16 |
| Ready with Conditions | 11 |
| Not Ready | 5 |
| **Total** | **32** |

---

## Alpha include set (default production posture)

**In Alpha (Ready):** CAP-01, 03–05, 07–12, 17, 20, 22, 24, 26, 32  

**In Alpha with disclosed conditions:** CAP-02, 06, 13–16, 18–19, 21, 23, 25  

**Excluded from Alpha default claims:** CAP-27–31 (and CAP-13/14 as *activated* experiences until flags ON)

---

## Navigation map (production feature mode)

```
Home (/student/)
  ├─ Daily Mission Intelligence (embed)
  ├─ Commitment / Defer / Reflection ack
  ├─ Welcome modal (conditional)
  └─ Tutor explain (conditional)
Journey (/student/journey)
Revision (/student/revision)
History (/student/history)
  ├─ Decision Journal
  └─ Educational Timeline (+ optional reflection)
Settings → Profile (/student/profile) → /settings/*
Study Plan (/study-plan/)
Help (/alpha/help) → feedback
```

Session and Quick Check (if enabled) are entered from Home/Session, not primary nav.
