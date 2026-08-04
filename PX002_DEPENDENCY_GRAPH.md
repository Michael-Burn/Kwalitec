# PX-002 — Premium Experience Dependency Graph

**Programme:** PX-002 — Premium Experience Workstream Planning  
**Status:** Planning complete — **implementation not authorised**  
**Effective:** 2026-08-04  
**Authority:** `PX002_WORKSTREAMS.md` · `PX001_PREMIUM_BACKLOG.md` · `PX001_EXECUTION_PLAN.md` · EF-001 · Educational Content Freeze  

---

## 1. Purpose

Show prerequisite work, blocking relationships, parallelisable tracks, release sequencing, **Critical Path**, and **Quick Wins** for Version 1 Premium Experience implementation.

---

## 2. Legend

| Symbol | Meaning |
|--------|---------|
| → | Hard prerequisite (must finish or decide before) |
| ⇢ | Soft preference (safer / cleaner if done first) |
| ‖ | Parallelisable (no hard block) |
| ★ | Critical Path node |
| QW | Quick Win (small effort, independent or lightly dependent) |

---

## 3. Founder / Product decision gates (block engineering)

| Gate | Blocks | Nature |
|------|--------|--------|
| **D-DURATION** | PX-B-035 (WS-01) | Authoritative duration source for presentation unify |
| **D-SESSION-PATH** | PX-B-014 (WS-02) | Authoritative student completion path (`session/*` vs `mission/*`) |
| **D-EOS** | PX-B-038 (WS-07) | Keep / retire “Education Operating System” framing |
| **D-IDENTITY** | PX-B-039, part of PX-B-022 (WS-07 / WS-10) | Student-grade Version 1 identity vs Internal Alpha chrome |
| **D-COMPLETE-STEP** | PX-B-015 (WS-02) | Show crafted complete screen **or** drop phantom step |
| **D-FINISH-CONFIRM** | PX-B-016 (WS-02) | Confirm modal vs documented low-stakes Finish |
| **D-COACH** | PX-B-050 (WS-04, Future) | Distinct Coach contract or hide |

Decisions may be recorded as waivers with owner if deferred — they still block claim of Closed for those IDs.

---

## 4. Workstream dependency graph

```text
                    ┌─────────────────────────────────────┐
                    │  Founder gates D-* (as needed)      │
                    └──────────────┬──────────────────────┘
                                   │
         ★ WS-01 Trust & Navigation (001,002,035,054,034; 003 later OK)
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
   ★ WS-03 Revision        WS-07 Microcopy      WS-02 Session
     (005,007,004)         & Identity           Workflow
              │              (038–045)            (015,016 early;
              │                    │               014,017,033 later)
              │                    │
              └────────┬───────────┘
                       │
         ┌─────────────┼──────────────┐
         ▼             ▼              ▼
   WS-04 Home     WS-06 A11y     WS-05 Mobile
   Experience     (023–030)      (037 then 036)
         │             │              │
         │             └──────┬───────┘
         ▼                    ▼
   WS-09 Performance    WS-08 Reliability
   (031,032)            (006,008,009)
         │                    │
         └─────────┬──────────┘
                   ▼
         WS-10 Premium Moments
         (019,020 early; 022 with identity;
          018 after 027; 046–049 later)
                   │
                   ▼
         ★ WS-11 Founder Dogfooding (052)
                   │
                   ▼
         ★ WS-12 Premium Certification (053)
```

---

## 5. Item-level prerequisites (blocking)

| Item | Requires before / with |
|------|-------------------------|
| PX-B-002 | Soft-depends on PX-B-001 pattern (same chrome identity programme) |
| PX-B-003 | Prefer after student chrome honesty (001/002) so ops isolation is clear |
| PX-B-005 | Continuity regenerate boundary; related to PX-B-007 |
| PX-B-007 | Re-verify with / after PX-B-005 |
| PX-B-004 | Independent of regenerate; may ship with WS-03 or early identity wave |
| PX-B-034 | Terminology matrix; coordinate with WS-07 identity |
| PX-B-035 | **D-DURATION** |
| PX-B-039 | **D-IDENTITY**; coordinate relocating research chrome with PX-B-022 |
| PX-B-022 | **D-IDENTITY** / pilot feedback strategy |
| PX-B-018 | PX-B-027 (reduced-motion) must cover student shell |
| PX-B-019 | Prefer with / after PX-B-025 touch targets |
| PX-B-032 | Soft-depends on PX-B-009 (shared perceived-latency story) |
| PX-B-036 | Soft-depends on PX-B-037 evidence + PX-B-025 |
| PX-B-014 | **D-SESSION-PATH** |
| PX-B-015 | **D-COMPLETE-STEP** |
| PX-B-016 | **D-FINISH-CONFIRM** + shared confirm modal |
| PX-B-050 | **D-COACH** — Future only |
| PX-B-052 | Prefer after trust + home craft baseline |
| PX-B-053 | Requires High Impact / Foundation closures or Board waiver |

---

## 6. Parallelisable work

| Track A | Track B | Track C | Notes |
|---------|---------|---------|-------|
| WS-01 chrome (001, 002) | WS-07 QW microcopy (040, 041, 043) | WS-06 micro a11y (024, 026, 027) | After Founder authorises implementation |
| WS-03 Q6 (004) | WS-02 finish/complete (015, 016) | WS-10 error/icon QW (019, 020) | Low cross-talk |
| WS-04 Analytics QW (011, 012) | WS-07 EOS/identity (038, 039) once decided | WS-09 measurement spike (031) | Measure before heavy trim |
| WS-05 device study (037) | WS-08 Continue Session (008) | WS-06 contrast/touch (025, 028) | Device study unblocks nav decision |
| WS-10 Nice to Have (046–049) | WS-04 Journey (013) | WS-02 recovery posture (017) | Late waves; not Critical Path |

**Do not parallelise:** PX-B-005/007 with unrelated Continuity experiments; PX-B-053 with unfinished S1 trust items.

---

## 7. Release sequencing (workstream order)

| Seq | Workstream | Release rationale |
|----:|------------|-------------------|
| 1 | WS-01 (core: 001, 002, 035, 054, 034) | Trust is the Version 1 premium floor |
| 2 | WS-03 | Terminal Revision / tip-complete S1 |
| 3 | WS-07 (identity + QW) ‖ early WS-02 QW ‖ early WS-06 QW | Student voice + interaction honesty |
| 4 | WS-05 evidence → pattern ‖ WS-06 Foundation | Mobile + a11y blockers |
| 5 | WS-04 Home craft ‖ WS-09 skeletons | One composition + loading |
| 6 | WS-08 ‖ WS-09 trim ‖ late WS-02 | Reliability / performance / path unify |
| 7 | WS-10 remaining ‖ WS-04 Nice ‖ WS-01 ops (003) | Polish + ops isolation |
| 8 | WS-11 | Multi-week evidence |
| 9 | WS-12 | Certification exit |

Wave mapping: see `PX002_IMPLEMENTATION_PLAN.md`.

---

## 8. Critical Path

The Critical Path is the minimum sequence that unlocks honest Premium Certification without leaving S1 trust open.

```text
★ D-DURATION (if open)
    → ★ PX-B-001 / PX-B-002 (chrome honesty)
    → ★ PX-B-035 / PX-B-054 (duration + profile exam trust)
    → ★ PX-B-005 / PX-B-007 (terminal R1 / tip-complete)
    → ★ PX-B-039 (student identity — D-IDENTITY)
    → ★ PX-B-037 → PX-B-036 / PX-B-025 / PX-B-028 (mobile + tap/contrast)
    → ★ PX-B-010 / PX-B-032 (Home composition + loading)
    → ★ PX-B-008 (Continue Session dignity)
    → ★ PX-B-052 (multi-week dogfood)
    → ★ PX-B-053 (Premium Certification)
```

**Critical Path properties**

- Dominated by S1 and High Impact Foundation items.  
- Nice to Have / Future items are **off** Critical Path.  
- Quick Wins may ship on side tracks without extending Critical Path length if they do not steal Continuity / chrome capacity.  
- Progressive Confidence regression on chrome/regenerate → **pause PX** per `PX001_EXECUTION_PLAN.md` §9.

---

## 9. Quick Wins

Items tagged Quick Win in `PX001_PREMIUM_BACKLOG.md`, mapped to workstreams:

| ID | Workstream | Why quick | Parallel note |
|----|------------|-----------|---------------|
| PX-B-004 | WS-03 | Presentation variant | ‖ with identity wave |
| PX-B-011 | WS-04 | Analytics density | ‖ early |
| PX-B-012 | WS-04 | Day-zero framing | ‖ early |
| PX-B-015 | WS-02 | Needs **D-COMPLETE-STEP** | After decision = S |
| PX-B-016 | WS-02 | Needs **D-FINISH-CONFIRM** | After decision = S |
| PX-B-019 | WS-10 | Icon stroke/size | Prefer with 025 |
| PX-B-020 | WS-10 | Error ID colour/copy | ‖ early |
| PX-B-024 | WS-06 | Timer live region | ‖ early |
| PX-B-026 | WS-06 | Focus-visible | ‖ early |
| PX-B-027 | WS-06 | Reduced-motion | Before 018 |
| PX-B-038 | WS-07 | Needs **D-EOS** | After decision = S |
| PX-B-040 | WS-07 | Session terminology | Coordinate tests |
| PX-B-041 | WS-07 | Reflection framing | Re-verify craft |
| PX-B-043 | WS-07 | Diagnostic disclosure | Re-verify |

**Quick Win release rule:** Bundle into the earliest independently releasable wave that already touches the same surface — do not open a separate “QW-only” programme that bypasses trust exits.

---

## 10. Blocking work summary

| Blocker class | Examples | Effect |
|---------------|----------|--------|
| Founder decisions | D-* gates | Hold Closed status for dependent IDs |
| S1 chrome / regenerate | 001, 002, 005, 007, 035, 054 | Block premium claim and Critical Path |
| Live mobile evidence | 037 | Blocks honest mobile nav certification (036) |
| CI / AT capacity | 030 | Blocks accessibility readiness claim |
| Hosting / Render | 008, 009 | Limits reliability Target under load |
| Educational Freezes | Content / EF / recommendations | Absolute — never unblock via PX |

---

## 11. Prerequisite work (already done — do not redo)

| Prerequisite | Evidence |
|--------------|----------|
| PB-017 PASS / 72/72 / Progressive Confidence 9.00/9 | `PB017_RELEASE_DECISION.md` |
| Educational Content Freeze | Charter G-PX-D |
| PX-001 backlog + execution plan | `PX001_PREMIUM_BACKLOG.md` · `PX001_EXECUTION_PLAN.md` |
| RO1-R1 class-1 closed | Residual mapping — extend pattern, do not reopen |
| Reflection persistence promise closed | Do not regress |

---

## 12. Claim posture vs graph

| Milestone | May claim when | Must not claim |
|-----------|----------------|----------------|
| After Critical Path through 005/007 | Trust/chrome/regenerate progress | Full premium PASS |
| After mobile + a11y Foundation | Mobile/a11y progress | WCAG conformance without audit |
| After WS-12 PASS | Premium Experience PASS (scorecard) | Until-exam trust; V1 production-ready from UX alone |

Signed: Product Experience · PX-002 Dependency Graph · 2026-08-04
