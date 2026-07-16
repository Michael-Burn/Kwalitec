# Release Candidate Validation Plan

**Capability ID:** V1S-004  
**Sprint:** Version 1 Sprint 2  
**Title:** Release Candidate Validation Planning  
**Status:** SUBMITTED — awaiting Executive Review  
**Date:** 2026-07-15  
**Nature:** Planning only — no application code, no product redesign, no educational redesign, no validation execution  

---

## Authority

| Authority | Role |
|-----------|------|
| V1S-003 | Release Candidate Preparation — `VERSION1_RELEASE_CANDIDATE.md` |
| V1R-001 | Version 1 Release Certification — `KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` |
| EIP-007 | Educational Governance APPROVED / Educationally Ready |
| V1S-001 / V1S-002 | Engineering Stabilisation complete |
| Release Protocol | Internal Alpha release class + verification — `docs/process/RELEASE_PROTOCOL.md` |
| EGI-003 §7 | Engineering + Architecture + Educational Governance triad |
| Internal Alpha programme | Prior feedback patterns — `research/internal_alpha/`, `knowledge/product/internal_alpha/` |

**Prerequisite posture (assumed entering validation)**

| Programme gate | Status |
|----------------|--------|
| Educational Integrity Programme | COMPLETE |
| Engineering Stabilisation | COMPLETE |
| Release Candidate preparation | COMPLETE |

Internal Alpha now validates the **Release Candidate as a product**, not individual features or open capabilities.

---

## 1. Purpose

Define how Internal Alpha testers evaluate the Version 1 Release Candidate (`VERSION1-RC1` or successor RC identifier) so Executive Review can decide:

> Is this Release Candidate trustworthy enough for continued Internal Alpha use as the Version 1 baseline?

This plan covers:

- Validation objectives
- Validation areas and evaluation criteria
- Feedback severity categories (including release blockers)
- Objective acceptance thresholds
- Release recommendation rules
- A Release Candidate Feedback Template focused on **trust**, **clarity**, and **usability**

This plan does **not**:

- Execute validation
- Redesign product or education
- Change application code
- Create commits, tags, or deploys
- Expand scope into Version 2 feature work

---

## 2. Validation Posture

### What changed from earlier Internal Alpha weeks

| Earlier Internal Alpha | Release Candidate Validation |
|------------------------|------------------------------|
| Find and stabilize discrete defects (IA-001…IA-004) | Confirm the repaired whole product holds together |
| Feature-centric feedback (“this mission is wrong”) | Trust-centric feedback (“I can rely on what Kwalitec tells me”) |
| Capability delivery is the goal | Release Candidate acceptance is the goal |
| Engineering health may be recovering | Engineering Stabilisation is treated as COMPLETE before validation starts |

### What testers are asked to do

Use Kwalitec as they would for real IFoA study across several sessions (minimum posture defined in §6). Focus judgment on whether the product feels educationally honest, operationally complete, and stable enough for daily study — **not** on requesting new Features or Version 2 concepts.

---

## 3. Validation Objectives

Testers and reviewers assess six objectives. Each objective has a plain-language question and pass intent.

| Objective | Core question | Pass intent |
|-----------|---------------|-------------|
| **Educational Trust** | Do progress, estimates, guidance, and recommendations feel honest and consistent? | No educational contradictions; claims match observed behaviour |
| **Product Trust** | Do dashboard, mission, plans, and analytics agree with each other? | Surfaces tell one coherent story for the active plan |
| **Workflow Completeness** | Can a student complete core study journeys without dead ends? | Onboarding → plan → mission → progress update closes cleanly |
| **User Experience** | Is navigation and language clear enough for undisturbed study? | Friction does not require workarounds or repeated refresh rituals |
| **Stability** | Does the app behave reliably across sessions? | No crashes, data loss, or broken primary actions in normal use |
| **Daily Usability** | Can a student use Kwalitec as part of real daily study? | Realistic session length; recommendations and plans support continued return |

### Objective detail

#### 3.1 Educational Trust

- Study Progress, Estimated Knowledge, and Educational Guidance remain distinguishable and non-contradictory (EIP-006 / IA-004 posture).
- Recommendations and missions match the active study plan and intended subject.
- Explainability (What / Why / Next) does not invent unsupported claims.
- Nothing tells the student they “know” or have “mastered” content without evidence the product itself respects.

#### 3.2 Product Trust

- Dashboard, Daily Mission, and launch pathways stay synchronized with the active plan (IA-001 / IA-002 lineage).
- Switching plans updates today‘s mission without stale subject bleed.
- Analytics and dashboard do not disagree about what the student has done.
- Settings changes that affect study (where applicable) are reflected where students expect.

#### 3.3 Workflow Completeness

- New or returning tester can create/select a plan and reach a meaningful mission.
- Completing or updating study does not strand the student on a dead-end screen.
- Delete / switch / resume plan flows leave a clear next action.
- No required journey depends on undocumented admin or refresh tricks.

#### 3.4 User Experience

- Labels and messaging stay student-centred (IA-003).
- Primary actions are findable within one session without hunting.
- Errors, empty states, and guidance are understandable.
- Premium feel is judged by calm clarity, not feature volume.

#### 3.5 Stability

- Pages load; forms submit; auth session holds for a study block.
- No reproducible crash, 500, or data wipe during normal journeys.
- State after refresh matches state before refresh for completed actions.

#### 3.6 Daily Usability

- Student can open the app, get a sensible next action, and study without re-configuring every day.
- Workload and recommendation pace feel usable for planned study duration.
- Returning the next day preserves continuity of intent (same plan, coherent next step).

---

## 4. Validation Areas

Students evaluate the following product areas against the six objectives. Area coverage is **mandatory** for Release Candidate acceptance unless Executive Review documents an exception.

| Area | Primary objectives | What “good” looks like |
|------|--------------------|------------------------|
| **Onboarding** | Workflow Completeness, UX, Educational Trust | Clear path into an active plan and first mission without confusion |
| **Study Plans** | Product Trust, Workflow Completeness, Daily Usability | Create, view, edit, switch, and (if used) delete without stale state |
| **Daily Mission** | Educational Trust, Product Trust, Stability | Mission matches active plan; start → study → return is coherent |
| **Dashboard** | Product Trust, Educational Trust, Daily Usability | One trustworthy “today” story aligned with mission and plan |
| **Recommendations** | Educational Trust, Product Trust | Appropriate, plan-bound, explainable; not contradictory |
| **Analytics** | Educational Trust, Product Trust | Progress presentation honest; no false mastery narrative |
| **Settings** | Workflow Completeness, Stability, UX | Account/study preferences behave as labeled; no silent breakage |
| **Overall educational confidence** | All six | Student would trust Kwalitec for continued Internal Alpha study |

Area checklist for each tester (minimum): at least one real session touching **Study Plans, Daily Mission, Dashboard, Recommendations**, plus either **Analytics** or **Settings**, and a closing judgment on **Overall educational confidence**. Onboarding must be covered by at least one tester who creates or regenerates plan context during the RC window.

---

## 5. Feedback Categories

Every Internal Alpha finding from RC validation is classified into exactly one category.

| Category | Definition | Examples | Blocks RC acceptance? |
|----------|------------|----------|------------------------|
| **Critical** | Breaks trust, corrupts educational meaning, or prevents core study | Wrong-subject mission; contradictory Progress vs Estimate as facts; data loss; unable to start studying on primary path | **Yes** |
| **High** | Severe friction or inconsistency that repeatedly undermines daily use | Plan switch requires forced refresh every time; recommendation regularly mismatches plan; primary CTA dead-ends | **Yes** (unless formally waived with remediation plan and time-box — default is block) |
| **Medium** | Meaningful defect or clarity issue; workaround exists | Occasional confusing copy; secondary flow awkward; analytics label unclear but not false | **No** (tracked for post-RC fix; volume may inform conditional pass — see §6) |
| **Low** | Minor polish or rare edge annoyance | Typo; visual inconsistency; rare empty-state wording | **No** |
| **Enhancement** | Improvement request within Version 1 product scope, not a defect | Better defaults; clearer empty states; nicer scheduling cues | **No** (does not block; not treated as “bugs”) |
| **Version 2** | Out-of-scope capability, redesign, or future educational evolution | New Adaptive Twin behaviour; public registration; syllabus redesign; new product modules | **No** (explicitly park; do not inflate RC failure) |

### Classification rules

1. Prefer the **highest truthful severity**. If unsure between High and Critical, use educational-trust impact: false educational claims escalate toward Critical.
2. A Feature request without evidence of broken trust is **Enhancement** or **Version 2**, never Critical.
3. “I wish it did X” after a successful study session is not a release blocker.
4. Duplicates of the same root cause count as **one finding** for blocking thresholds once confirmed by triage.
5. Week_001-style trust collapses (wrong subject, stale plan sync marketed as reliability) are treated as **Critical** or **High**, not Enhancement.

### Triage ownership

| Role | Responsibility |
|------|----------------|
| Tester | Report observed behaviour using the Feedback Template (§8) |
| Product / Architecture triage | Assign category; merge duplicates; mark blocker vs non-blocker |
| Engineering | Confirm reproducibility for Critical / High only as needed for decision |
| Executive Review | Apply §6–§7 for accept / conditional / reject |

---

## 6. Acceptance Criteria

Release Candidate Validation **passes** only when all of the following are true after the planned Internal Alpha RC window.

### 6.1 Hard gates (must all pass)

| Gate | Threshold |
|------|-----------|
| **No Critical issues** | Zero open Critical findings after triage |
| **No unresolved High blockers** | Zero open High findings that still block daily study, unless Executive Review issues a written, time-boxed waiver with owner and fix commitment |
| **No educational contradictions** | No open finding where Progress, Estimated Knowledge, Guidance, Mission, and Recommendation mutually contradict as presented facts |
| **No workflow dead ends** | Every mandatory area path in §4 has a documented successful traverse by ≥1 tester; no open Critical/High dead-end on onboarding → plan → mission → return |
| **Stable daily use** | Across the RC window, no open Critical/High stability finding (crash, data loss, persistent 500 on primary paths) |
| **Educational confidence** | Majority of participating testers answer overall educational confidence as positive (trust / would continue) — see §6.3 |

### 6.2 Soft gates (should pass; inform Conditional Accept)

| Gate | Threshold |
|------|-----------|
| Medium finding volume | Prefer ≤ 5 distinct Medium findings open at decision time; above this → prefer Conditional Accept with prioritized backlog |
| UX clarity | No widespread pattern (≥2 independent testers) that primary navigation requires explanation outside the product |
| Continuity | Plan switch and next-day return do not regenerate week_001 stale-mission pattern for any tester |
| Daily Usability | At least one multi-day return demonstrated (same tester, ≥2 study days) without re-onboarding |

### 6.3 Coverage minimums

| Requirement | Minimum |
|-------------|---------|
| Tester count | Prefer ≥ 2 Internal Alpha testers; if only 1, Executive Review must explicitly accept single-tester limitation |
| Sessions | Prefer ≥ 3 study sessions total across testers in the RC window |
| Area coverage | All areas in §4 evaluated at least once (via tester checklist) |
| Feedback form | Each participating tester submits ≥1 completed RC Feedback Template (§8) |

### 6.4 Outcome labels

| Outcome | Meaning |
|---------|---------|
| **ACCEPT** | Hard gates passed; soft gates largely passed; RC cleared for continued Internal Alpha as Version 1 baseline |
| **CONDITIONAL ACCEPT** | Hard gates passed; soft gates missed or Medium volume high; continue Internal Alpha with explicit remediation backlog (no Critical/High open) |
| **REJECT** | Any hard gate failed; return to Engineering / Educational Integrity remediation before another RC validation cycle |
| **INCOMPLETE** | Coverage minimums not met; do not score ACCEPT/REJECT until evidence exists |

Engineering suite green and RC fingerprint cleanliness remain **preconditions** governed by V1S-003 / Release Protocol. This plan assumes those are already satisfied when validation **starts**. Failures discovered during validation that reveal engineering breakage are classified under §5 and can still force REJECT.

---

## 7. Release Recommendation Rules

After triage and coverage check, recommend one outcome using these rules **in order**.

1. If coverage minimums (§6.3) are unmet → **INCOMPLETE**. Do not accept.
2. If any open **Critical** finding remains → **REJECT**.
3. If any open **High** finding remains without Executive waiver → **REJECT**.
4. If educational contradiction or workflow dead-end hard gates fail → **REJECT**.
5. If hard gates pass and soft gates pass → **ACCEPT**.
6. If hard gates pass but soft gates fail or Medium backlog is heavy → **CONDITIONAL ACCEPT** with:
   - Ordered Medium/Low backlog
   - Owner
   - Whether fixes are required before public/External Alpha (not required for Internal Alpha continue-use unless specified)
7. **Enhancement** and **Version 2** items never flip ACCEPT → REJECT by themselves.
8. Prior week_001 defect *themes* that reappear on the RC count as new findings if reproduced; historical closure alone does not grant ACCEPT.

### Decision record (required before closing V1S-004 validation later)

When validation is eventually executed (outside this planning capability), record:

- RC identifier and commit/tag fingerprint under test
- Tester list and session dates
- Finding inventory by category
- Outcome label and rationale
- Any waivers

Location for that future decision artefact: `knowledge/release/` (execution report — **not created by this plan**).

---

## 8. Release Candidate Feedback Template

Use this template for Internal Alpha RC validation. Focus on **trust**, **clarity**, and **usability**. Do not treat this as a feature request form.

Copy from the separator downward for tester distribution.

```
==============================================================================
KWALITEC — RELEASE CANDIDATE FEEDBACK
Internal Alpha | Trust · Clarity · Usability
==============================================================================

RC identifier (if known): _______________________
Date: _______________________
Tester: _______________________
Exam / subject context (e.g. CM1): _______________________
Study plans used today: _______________________
Planned study duration (minutes): _______
Actual study duration (minutes): _______

------------------------------------------------------------------------------
A. SESSION CONTEXT
------------------------------------------------------------------------------

Which areas did you use today? (tick all that apply)

[ ] Onboarding
[ ] Study Plans
[ ] Daily Mission
[ ] Dashboard
[ ] Recommendations
[ ] Analytics
[ ] Settings

------------------------------------------------------------------------------
B. EDUCATIONAL TRUST
------------------------------------------------------------------------------

1. Did Progress, Estimated Knowledge, and Guidance feel honest and consistent?
   [ ] Yes   [ ] Mostly   [ ] No

2. Did anything feel misleading, contradictory, or overstated?
   [ ] No   [ ] Yes — describe:

3. Did the recommendation / mission match the plan and subject you intended?
   [ ] Yes   [ ] No — describe:

------------------------------------------------------------------------------
C. PRODUCT TRUST & WORKFLOWS
------------------------------------------------------------------------------

4. Did Dashboard, Daily Mission, and your active Study Plan agree with each other?
   [ ] Yes   [ ] No — describe:

5. Could you complete your intended study journey without a dead end?
   [ ] Yes   [ ] No — where did it stop?

6. Did you need workarounds (refresh, re-login, recreate plan, etc.)?
   [ ] No   [ ] Yes — describe:

------------------------------------------------------------------------------
D. CLARITY & DAILY USABILITY
------------------------------------------------------------------------------

7. Was it clear what to do next?
   [ ] Yes   [ ] Mostly   [ ] No

8. What was clearest today?


9. What was most confusing today?


10. Would you use this build again for real study tomorrow?
    [ ] Yes   [ ] Hesitant   [ ] No
    Why?

------------------------------------------------------------------------------
E. STABILITY
------------------------------------------------------------------------------

11. Any crashes, errors, lost progress, or broken buttons?
    [ ] No   [ ] Yes — describe (what you did, what you saw):

------------------------------------------------------------------------------
F. OVERALL EDUCATIONAL CONFIDENCE
------------------------------------------------------------------------------

12. Overall: Do you trust Kwalitec’s educational guidance in this Release Candidate?
    [ ] Trust   [ ] Partial trust   [ ] Do not trust

13. One sentence: what most affects your confidence right now?


------------------------------------------------------------------------------
G. OPTIONAL NOTES (not feature requests)
------------------------------------------------------------------------------

14. Anything else about trust, clarity, or usability?


N.B. Please park “new feature” ideas separately. Prefer describing what
went wrong or felt unclear over proposing Version 2 product ideas here.

==============================================================================
END OF TEMPLATE
==============================================================================
```

### Triage mapping hints (internal only)

| Template signal | Likely category |
|-----------------|-----------------|
| Wrong subject / contradictory educational facts / cannot study | Critical |
| Repeated sync/refresh workaround; primary path broken | High |
| Confusing but completable; occasional mismatch with workaround | Medium |
| Cosmetic / rare | Low |
| “Would be nice if…” with successful study | Enhancement |
| New modules / redesign / Twin / public open registration | Version 2 |

---

## 9. Validation Window (planning defaults)

| Parameter | Default (for Executive approval) |
|-----------|----------------------------------|
| Window length | 3–5 study days once RC build is available to testers |
| Cadence | Daily or end-of-session feedback using §8 template |
| Mid-window triage | At least one triage pass before final decision |
| Stop condition | Any confirmed Critical may pause validation for fix → new RC — Executive call |

Exact calendar dates are **not** set by this document; they follow RC availability after V1S-003 execution and Executive scheduling.

---

## 10. Explicit Non-Goals

- No application code changes under V1S-004  
- No product or educational redesign  
- No commencement of Internal Alpha Validation under this capability  
- No ACCEPT / REJECT decision under this capability (planning only)  
- No commit / tag / deploy  

---

## 11. Status and Next Step

| Field | Value |
|-------|-------|
| V1S-004 deliverable | This plan |
| Validation execution | **Not started** |
| Required next action | **Executive Review** of this plan |

**Stop.** Do not begin Internal Alpha Validation until Executive Review returns with approval (or amendments) of this plan.
