# Internal Alpha Release Candidate Validation

**Capability ID:** V1S-005  
**Sprint:** Version 1 Sprint 2  
**Title:** Internal Alpha Release Candidate Validation  
**Status:** SUBMITTED — awaiting Executive Review  
**Date:** 2026-07-15  
**Nature:** Validation pack only — no application code, no implementation, no UI changes, no educational changes, no validation execution under this capability  

---

## Authority

| Authority | Role |
|-----------|------|
| V1S-004 | Release Candidate Validation Plan — `RELEASE_CANDIDATE_VALIDATION_PLAN.md` (**APPROVED**) |
| V1S-003 | Release Candidate Preparation — `VERSION1_RELEASE_CANDIDATE.md` |
| V1R-001 | Version 1 Release Certification — `KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` |
| EIP-007 | Educational Governance APPROVED / Educationally Ready |
| V1S-001 / V1S-002 | Engineering Stabilisation complete |
| Release Protocol | Internal Alpha release class — `docs/process/RELEASE_PROTOCOL.md` |
| EGI-003 §7 | Engineering + Architecture + Educational Governance triad |

**Prerequisite posture**

| Programme gate | Status |
|----------------|--------|
| Educational Integrity Programme | COMPLETE |
| Engineering Stabilisation | COMPLETE |
| Release Candidate Preparation | COMPLETE |
| Validation Plan (V1S-004) | APPROVED |

**Release Candidate under validation:** `VERSION1-RC1`  
**Decision question:** Does this Release Candidate deserve promotion toward Version 1.0 (continued Internal Alpha as the Version 1 baseline)?

This document is the **operational validation pack** for Internal Alpha. It does not redesign the product. It does not discover Features. It does not execute validation — it equip Executives, triage, and testers to do so cleanly.

---

## Posture

| This is | This is not |
|---------|-------------|
| Release Candidate validation | Feature discovery |
| Trust · clarity · usability confirmation | Product redesign |
| Evidence for ACCEPT / CONDITIONAL ACCEPT / REJECT / INCOMPLETE | Version 2 roadmaping |
| Natural daily study use | Adversarial bug hunting |

---

# 1. Release Validation Guide

## 1.1 Purpose

Determine whether `VERSION1-RC1` is trustworthy enough for continued Internal Alpha use as the Version 1 baseline — and whether it deserves promotion toward Version 1.0.

Internal Alpha testers evaluate the **Release Candidate as a whole product**, not individual capabilities or open backlogs.

Validation answers one executive question:

> Can students rely on this build for real study without educational contradiction, workflow collapse, or loss of daily trust?

## 1.2 Tester role

| The tester is | The tester is not |
|---------------|-------------------|
| A realistic IFoA student using Kwalitec for study | A QA engineer hunting edge cases |
| An independent observer of trust, clarity, and usability | A product designer proposing Redesign |
| A recorder of genuine session experience | A group debating findings before submission |

Testers:

1. Use the product naturally across study sessions.
2. Complete the Release Candidate Feedback Form (§2) after each meaningful session (or at the end of the validation window, if session cadence requires).
3. Submit feedback independently.
4. Do not discuss findings with other testers until all submissions for the window are complete.

Triage (Product / Architecture) later classifies submissions (§3) and assigns severity (§5). Testers report honestly; they do not need to assign executive outcomes.

## 1.3 Validation process

```
RC available to Internal Alpha
        │
        ▼
Testers use Kwalitec as daily study companion (§7)
        │
        ▼
Each tester submits independent Feedback Form(s) (§2)
        │
        ▼
Triage classifies each item (§3) and assigns severity (§5)
        │
        ▼
Coverage and hard/soft gates checked against V1S-004
        │
        ▼
Decision Matrix applied (§4)
        │
        ▼
Executive Summary completed (§6)
        │
        ▼
Executive Review records ACCEPT / CONDITIONAL ACCEPT / REJECT / INCOMPLETE
```

**Mandatory product areas** (from V1S-004; at least once across the cohort):

| Area | Notes |
|------|--------|
| Onboarding | Covered by ≥1 tester who creates or regenerates plan context |
| Study Plans | Create / view / edit / switch as used |
| Daily Mission | Start → study → return |
| Dashboard | “Today” story aligned with plan and mission |
| Recommendations | Plan-bound and explainable |
| Analytics **or** Settings | At least one of these plus closing confidence judgment |
| Overall educational confidence | Required on every form |

**Coverage minimums** (fail → **INCOMPLETE**, not ACCEPT/REJECT):

| Requirement | Minimum |
|-------------|---------|
| Testers | Prefer ≥ 2; single-tester requires explicit Executive acceptance of limitation |
| Sessions | Prefer ≥ 3 study sessions total across testers |
| Feedback | Each participating tester submits ≥ 1 completed form |
| Areas | All mandatory areas evaluated at least once across the cohort |

**Window (default):** 3–5 study days once the RC build is available. Exact calendar dates follow Executive scheduling.

## 1.4 Expected mindset

- **Trust over novelty.** Prefer “Did it stay honest?” over “What should we add?”
- **Natural use over obscure bugs.** Study as you would for an exam week. Do not invent exotic reproduction scripts unless something breaks during real use.
- **One coherent story.** Watch whether Progress, Estimated Knowledge, Guidance, Mission, Recommendation, Dashboard, and Plans agree.
- **Park Version 2.** Future modules, Adaptive Twin evolution, public registration, syllabus redesign — record as Version 2 if they arise; they do not fail the RC by themselves.
- **Independence.** No sharing findings until submissions are in. Group consensus after the window is Executive/triage work, not tester work.
- **Honesty over politeness.** Partial trust and “would not use tomorrow” are valid and valuable outcomes.

---

# 2. Release Candidate Feedback Form

Copy from the separator downward for tester distribution. Focus on **trust**, **clarity**, and **usability**. This is not a Feature request form.

```
==============================================================================
KWALITEC — RELEASE CANDIDATE FEEDBACK FORM
Internal Alpha | VERSION1-RC1 | Trust · Clarity · Usability
==============================================================================

RC identifier: VERSION1-RC1 (or successor): _______________________
Commit / tag / build fingerprint (if known): _______________________
Date: _______________________
Tester: _______________________
Exam / subject context (e.g. CM1): _______________________
Study plans used: _______________________
Session number in RC window: _______ of _______
Planned study duration (minutes): _______
Actual study duration (minutes): _______

------------------------------------------------------------------------------
A. SESSION CONTEXT
------------------------------------------------------------------------------

Areas used today (tick all that apply)

[ ] Onboarding
[ ] Study Plans
[ ] Daily Mission
[ ] Dashboard
[ ] Recommendations
[ ] Analytics
[ ] Settings

Briefly: what did you intend to do in this session?


------------------------------------------------------------------------------
B. EDUCATIONAL TRUST
------------------------------------------------------------------------------

1. Did Study Progress, Estimated Knowledge, and Educational Guidance feel
   honest, distinguishable, and non-contradictory?
   [ ] Yes   [ ] Mostly   [ ] No

2. Did anything feel misleading, overstated, or educationally contradictory?
   [ ] No   [ ] Yes — describe what was shown vs what felt true:


3. Did the recommendation and/or mission match the active plan and subject?
   [ ] Yes   [ ] No — describe:


------------------------------------------------------------------------------
C. PRODUCT TRUST
------------------------------------------------------------------------------

4. Did Dashboard, Daily Mission, Analytics (if used), and the active Study Plan
   tell one coherent story?
   [ ] Yes   [ ] Mostly   [ ] No — describe disagreements:


5. After plan switch or next-day return (if applicable), did state stay coherent?
   [ ] Yes   [ ] N/A   [ ] No — describe:


------------------------------------------------------------------------------
D. WORKFLOW COMPLETENESS
------------------------------------------------------------------------------

6. Could you complete your intended study journey without a dead end?
   [ ] Yes   [ ] No — where did it stop?


7. Did you need workarounds (refresh, re-login, recreate plan, admin tricks)?
   [ ] No   [ ] Yes — describe:


------------------------------------------------------------------------------
E. USER EXPERIENCE
------------------------------------------------------------------------------

8. Was it clear what to do next?
   [ ] Yes   [ ] Mostly   [ ] No

9. What was clearest today?


10. What was most confusing today?


------------------------------------------------------------------------------
F. DAILY USABILITY
------------------------------------------------------------------------------

11. Could you use this build as part of real daily study without re-configuring
    everything?
    [ ] Yes   [ ] Mostly   [ ] No — describe:


12. Would you open this build again for real study tomorrow?
    [ ] Yes   [ ] Hesitant   [ ] No
    Why?


------------------------------------------------------------------------------
G. OVERALL CONFIDENCE
------------------------------------------------------------------------------

13. Overall educational confidence in this Release Candidate:
    [ ] Trust   [ ] Partial trust   [ ] Do not trust

14. Overall product confidence (surfaces agree; journeys close):
    [ ] Trust   [ ] Partial trust   [ ] Do not trust

15. One sentence: what most affects your confidence right now?


------------------------------------------------------------------------------
H. FINAL RECOMMENDATION (tester view — not the executive decision)
------------------------------------------------------------------------------

16. As a student using this RC for continued Internal Alpha study, I would:
    [ ] Recommend ACCEPT (ready to keep using as Version 1 baseline)
    [ ] Recommend CONDITIONAL ACCEPT (usable, but named issues must be tracked)
    [ ] Recommend REJECT (not trustworthy enough yet)
    [ ] Insufficient personal coverage to recommend

17. Issues or observations to file (one block per item; add sheets if needed):

    Item #: _______
    What happened (observed):
    Steps (if reproducible):
    Expected:
    Actual:
    My draft type (optional): Observed Fact / Reproducible Defect / Suggestion /
                              Preference / Version 2


------------------------------------------------------------------------------
I. OPTIONAL NOTES
------------------------------------------------------------------------------

18. Anything else about trust, clarity, or usability?


N.B. Park Feature ideas that are not about broken trust or unclear behaviour.
Prefer describing what went wrong or felt unclear over proposing Version 2.

==============================================================================
END OF FORM
==============================================================================
```

---

# 3. Feedback Classification Standard

Every submission item is classified into **exactly one** type before severity is applied. Classification describes the **epistemic nature** of the feedback; severity (§5) describes **release impact**.

| Classification | Definition | Triage treatment |
|----------------|------------|------------------|
| **Observed Fact** | A verifiable statement of what the product showed or did in a real session, without requiring a bug claim | Record as evidence; may support trust metrics or escalate if it reveals contradiction |
| **Reproducible Defect** | Broken or incorrect behaviour with enough steps that another person can reproduce (or Engineering confirms) | Enter finding inventory; assign severity; counts toward gates |
| **Suggestion** | Constructive improvement within Version 1 scope that is not a claim of broken behaviour | Track as Enhancement unless it exposes a latent defect |
| **Preference** | Personal taste (wording tone, layout preference, pacing preference) without evidence of harm to trust or completion | Do not treat as defect; may inform polish backlog as Low/Enhancement |
| **Version 2** | Out-of-scope capability, redesign, or future educational evolution | Park explicitly; never use alone to REJECT the RC |

### Classification rules

1. Prefer **Observed Fact** when the tester only reports what appeared (e.g. “Guidance said X while Analytics showed Y”) until triage confirms defect vs intended design.
2. Promote to **Reproducible Defect** when steps reproduce wrong educational meaning, dead ends, crashes, data loss, or inconsistent surfaces.
3. “I wish it did X” after a successful study session is **Suggestion** or **Preference**, not a defect.
4. New modules, Twin evolution, public registration, syllabus redesign → **Version 2**.
5. Duplicates of the same root cause count as **one** finding for blocking thresholds once triage merges them.
6. Week_001-style trust collapses (wrong subject, stale plan sync marketed as reliability) start as **Observed Fact** / **Reproducible Defect** and escalate in severity — never Preference.

### Relationship to severity

| Classification | Typical severity path |
|----------------|------------------------|
| Observed Fact | May remain unsevered evidence, or map to Critical–Low after triage |
| Reproducible Defect | Always receives a severity (§5) |
| Suggestion | Enhancement (default) or Low |
| Preference | Preference stays non-blocking; optional Low/Enhancement |
| Version 2 | Version 2 (non-blocking for RC acceptance) |

---

# 4. Release Decision Matrix

After coverage check, triage, and severity assignment, select **exactly one** outcome.

| Outcome | Meaning | Objective criteria (all must hold for that row) |
|---------|---------|--------------------------------------------------|
| **ACCEPT** | RC cleared for continued Internal Alpha as Version 1 baseline | Coverage minimums met (§1.3); **zero** open Critical; **zero** open High without written Executive waiver; **no** open educational contradictions; **no** open Critical/High workflow dead ends on primary paths; **no** open Critical/High stability failures (crash, data loss, persistent 500 on primary paths); majority of testers report positive educational confidence (Trust or would continue); soft gates largely passed (Medium volume preferably ≤ 5 distinct open findings; no widespread primary-nav confusion pattern; continuity / multi-day return demonstrated or explicitly waived) |
| **CONDITIONAL ACCEPT** | Continue Internal Alpha with an explicit remediation backlog | Coverage minimums met; **all hard gates same as ACCEPT** (no open Critical; no unresolved High without waiver; no educational contradiction hard-gate failure); **soft gates missed** and/or Medium backlog heavy; backlog ordered with owner; Enhancements/Version 2 alone never force REJECT |
| **REJECT** | Not promoted; return to Engineering / Educational Integrity remediation before another RC validation cycle | Coverage minimums met **and** any hard gate failed: open Critical; open High without waiver; educational contradiction as presented facts; Critical/High dead-end on onboarding → plan → mission → return; Critical/High stability failure on primary paths; **or** majority educational confidence is negative (**Do not trust** / would not continue) such that hard educational-confidence gate fails |
| **INCOMPLETE** | Do not score ACCEPT/REJECT yet | Coverage minimums unmet (testers, sessions, forms, or mandatory areas); validation window not finished; fingerprint under test unclear |

### Decision order (apply in sequence)

1. Coverage unmet → **INCOMPLETE**.
2. Open **Critical** → **REJECT**.
3. Open **High** without Executive waiver → **REJECT**.
4. Educational contradiction or workflow dead-end hard gate fails → **REJECT**.
5. Hard gates pass and soft gates pass → **ACCEPT**.
6. Hard gates pass, soft gates fail or Medium backlog heavy → **CONDITIONAL ACCEPT**.
7. **Enhancement** and **Version 2** items never alone flip ACCEPT → REJECT.
8. Reappearance of week_001 trust-collapse themes on this RC counts as new findings if reproduced.

### Decision record (required when validation closes)

Record in this file’s Executive Summary (§6) or a dated companion under `knowledge/release/`:

- RC identifier and commit/tag fingerprint
- Tester list and session dates
- Finding inventory by classification and severity
- Outcome label and rationale
- Any waivers (owner, time-box, fix commitment)

---

# 5. Issue Severity Matrix

Severity measures **release impact**. Assign after classification (§3).

| Severity | Definition | Examples | Blocks RC ACCEPT? |
|----------|------------|----------|-------------------|
| **Critical** | Breaks trust, corrupts educational meaning, or prevents core study | Wrong-subject mission; Progress vs Estimate contradictory as facts; data loss; unable to start studying on primary path | **Yes** — hard gate |
| **High** | Severe friction or inconsistency that repeatedly undermines daily use | Plan switch requires forced refresh every time; recommendation regularly mismatches plan; primary CTA dead-ends | **Yes** — default hard gate (waiver only with written time-box + owner) |
| **Medium** | Meaningful defect or clarity issue; workaround exists | Occasional confusing copy; secondary flow awkward; analytics label unclear but not false | **No** — volume informs CONDITIONAL ACCEPT |
| **Low** | Minor polish or rare edge annoyance | Typo; visual inconsistency; rare empty-state wording | **No** |
| **Enhancement** | Improvement within Version 1 scope, not a defect | Better defaults; clearer empty states; scheduling cues | **No** |
| **Version 2** | Out-of-scope future work | New Adaptive Twin behaviour; public registration; syllabus redesign; new modules | **No** — park |

### Blocking rule (summary)

| Blocks promotion / ACCEPT | Does not block |
|---------------------------|----------------|
| Critical (any open) | Medium |
| High (any open without written Executive waiver) | Low |
| Educational contradiction hard-gate failure | Enhancement |
| Critical/High dead-end or stability failure on primary paths | Version 2 |

### Severity assignment rules

1. Prefer the **highest truthful severity**.
2. Educational-trust impact: false claims escalate toward **Critical**.
3. Feature requests without broken trust are **Enhancement** or **Version 2**, never Critical.
4. Confirmed duplicates count once for thresholds.
5. Preference never becomes Critical solely because the tester feels strongly.

---

# 6. Executive Summary Template

Complete **after** the Internal Alpha validation window and triage — not before.

```
==============================================================================
KWALITEC — INTERNAL ALPHA RC VALIDATION — EXECUTIVE SUMMARY
==============================================================================

Capability: V1S-005
RC identifier: VERSION1-RC1 (or successor): _______________________
Fingerprint (commit / tag / deploy): _______________________
Validation window: _______________ → _______________
Status of this summary: DRAFT / FINAL
Prepared by: _______________________
Date: _______________________

------------------------------------------------------------------------------
COVERAGE
------------------------------------------------------------------------------

Number of testers: _______
Sessions completed (total): _______
Forms submitted: _______
Mandatory areas covered: [ ] Yes  [ ] No — gaps:


------------------------------------------------------------------------------
FINDINGS (after triage)
------------------------------------------------------------------------------

Critical issues (open): _______
High issues (open): _______
High waivers (if any): _______
Medium (open, distinct): _______
Low: _______
Enhancement: _______
Version 2 (parked): _______

Educational contradictions (open, as presented facts): _______
  Describe if any:


Workflow dead ends (Critical/High, primary paths): _______
Stability failures (Critical/High, primary paths): _______

Educational confidence tally:
  Trust: _______   Partial trust: _______   Do not trust: _______

Tester recommendation tally (optional):
  ACCEPT: _______   CONDITIONAL: _______   REJECT: _______   Insufficient: _______


------------------------------------------------------------------------------
HARD / SOFT GATES
------------------------------------------------------------------------------

Hard gates: [ ] PASS  [ ] FAIL — which:


Soft gates: [ ] PASS  [ ] MISS — which:


------------------------------------------------------------------------------
RECOMMENDATION
------------------------------------------------------------------------------

Outcome: [ ] ACCEPT  [ ] CONDITIONAL ACCEPT  [ ] REJECT  [ ] INCOMPLETE

Rationale (short):


Remediation backlog (required for CONDITIONAL ACCEPT):


Waivers (owner / time-box / commitment):


------------------------------------------------------------------------------
NEXT STEP
------------------------------------------------------------------------------

[ ] Executive Review confirm outcome
[ ] If REJECT — return to remediation; schedule new RC cycle
[ ] If ACCEPT / CONDITIONAL ACCEPT — proceed under Release Protocol / V1R-001
[ ] If INCOMPLETE — extend window / add testers; do not promote

==============================================================================
END OF EXECUTIVE SUMMARY
==============================================================================
```

**Validation execution status under V1S-005:** Not started. Section 6 remains a blank template until Internal Alpha runs against the released RC fingerprint.

---

# 7. Tester Instructions

Distribute these instructions with the Feedback Form (§2).

### Do

1. **Use Kwalitec naturally** as your daily study companion for real (or realistically planned) IFoA study.
2. Work through normal paths: plan → mission → dashboard → recommendations; include analytics or settings when useful.
3. **Treat the application as your study companion**, not as a demo to break.
4. **Record genuine observations** — what you saw, what you trusted, what confused you, whether you would return tomorrow.
5. **Submit feedback independently** using the Feedback Form.
6. Cover enough sessions to speak honestly about daily usability (prefer more than one study day if the window allows).

### Do not

1. **Do not search for obscure bugs** or invent adversarial edge cases unrelated to study.
2. **Do not** turn the window into Feature discovery or redesign workshops.
3. **Do not discuss findings** with other testers until all submissions for the window are complete.
4. **Do not** inflate failures with Version 2 wishes; park those explicitly on the form.
5. **Do not** skip the Overall Confidence and Final Recommendation sections — they matter as much as defect lists.

### Mindset reminder

This is Release Candidate validation for `VERSION1-RC1`.  
The product has already completed Educational Integrity, Engineering Stabilisation, and RC preparation.  
Your job is to confirm — or honestly deny — that the repaired whole is fit for Version 1 baseline trust.

---

# 8. Explicit Non-Goals (V1S-005)

- No application code changes  
- No implementation  
- No UI changes  
- No educational logic or Constitution changes  
- No ACCEPT / REJECT decision under this capability alone (pack creation only; decision follows real validation + Executive Review)  
- No commit / tag / deploy under this capability  

---

# 9. Status and Next Step

| Field | Value |
|-------|-------|
| V1S-005 deliverable | This validation pack |
| Validation execution | **Not started** |
| Forms ready for distribution | Yes (§2, §7) |
| Decision Matrix ready | Yes (§4) |
| Classification + severity ready | Yes (§3, §5) |
| Executive Summary | Template only (§6) — complete after validation |
| Required next action | **Executive Review** of this pack; then schedule Internal Alpha RC window |

**Stop.** Return for Executive Review. Do not begin scoring ACCEPT / REJECT until testers have submitted against the RC fingerprint and §6 is completed with evidence.
