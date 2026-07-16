# Independent Product Validation Commission

**Capability ID:** IPV-001  
**Programme:** Version 1 Release Programme  
**Title:** Independent Product Validation Commission  
**Priority:** P0  
**Status:** APPROVED  
**Date:** 2026-07-16  
**Nature:** Commissioning document only — no application code, no implementation, no validation execution under this capability  

---

## Authority

| Authority | Role |
|-----------|------|
| V1R-001 | Version 1 Release Certification — `KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` |
| V1S-003 | Release Candidate Preparation — `VERSION1_RELEASE_CANDIDATE.md` |
| V1S-004 | Release Candidate Validation Plan — `RELEASE_CANDIDATE_VALIDATION_PLAN.md` |
| V1S-005 | Internal Alpha Release Validation — `INTERNAL_ALPHA_RELEASE_VALIDATION.md` |
| Release Protocol | Internal Alpha release class — `docs/process/RELEASE_PROTOCOL.md` |

**Prerequisite posture**

| Programme gate | Status |
|----------------|--------|
| Educational Integrity Programme | COMPLETE |
| Learning Experience Programme | COMPLETE |
| Product Trust Programme | COMPLETE |
| Research Intelligence Programme | COMPLETE |
| Release Candidate | PREPARED |

**Release Candidate under validation:** `VERSION1-RC1` (or successor RC identifier named at commissioning time)

**Decision question (Executive):** Is this Release Candidate trustworthy enough to enter Internal Alpha as the Version 1 baseline?

This document commissions the **final independent product review** before Internal Alpha. It is not another architecture review, educational review, or engineering review. It judges only what a first-time student experiences in the running application.

---

## Posture

| This is | This is not |
|---------|-------------|
| Independent product validation as a skeptical first-time student | Architecture, educational, or engineering review |
| Evidence for REJECT / CONDITIONAL GO / GO before Internal Alpha | Feature discovery or Version 2 roadmaping |
| Reproducible blind review of the running product | Code inspection, documentation archaeology, or admin forensics |
| Judgment of daily dependence over three months | Adversarial bug hunting or checklist theatre |

---

# 1. Objective

Commission one completely independent review of Kwalitec Version 1 Release Candidate **exactly as a first-time student would experience it**, before Internal Alpha begins.

The reviewer must know **absolutely nothing** about Kwalitec before beginning. The review must be **completely reproducible**. Another independent reviewer following this commission should reasonably reach similar conclusions.

No application code may be modified under this capability.

---

# 2. Mission

The reviewer has one mission.

Answer this question:

> **If my professional examinations began tomorrow, would I genuinely depend on Kwalitec every day for the next three months?**

Everything in the review must support answering that question. Secondary curiosity about architecture, roadmap, or implementation is out of scope.

---

# 3. Reviewer Persona

The reviewer must become **a skeptical student**.

### Characteristics

| Trait | Behaviour |
|-------|-----------|
| Serious about passing | Treats study time as scarce and expensive |
| Busy | Has limited patience for friction, repetition, or dead ends |
| Paying for expensive professional examinations | Expects honesty; will not forgive over-promising |
| No prior knowledge of Kwalitec | Starts cold — no documentation, no insider context |
| No loyalty to the product | Will abandon products that waste time |
| Wants one trustworthy daily companion | Seeks a single place to return each study day |

The reviewer must behave **naturally**. Explore the product as a real student would — not as a tester executing a script. No forced checklist order. Follow curiosity, confusion, and daily study instinct.

### Suggested context (assign at commissioning)

| Field | Example |
|-------|---------|
| Age / life stage | Late twenties, full-time job |
| Exam proximity | Professional examinations begin in ~90 days |
| Study pattern | Before work and after work; 45–90 minutes per session |
| Prior attempt | Optional: has failed the paper once — raises stakes |
| External materials | Uses own study notes and question banks (e.g. ActEd) — does not expect Kwalitec to replace them unless the product visibly provides content |

Record assigned context in the review output. Do not change persona mid-review.

---

# 4. Independence Requirements

The reviewer **MUST NOT**:

| Prohibited | Reason |
|------------|--------|
| Read architecture documentation | Judges product, not structure |
| Read release documentation | Avoids preconditioned expectations |
| Read previous Blind Reviews | Preserves independence |
| Read the Constitution | Not a governance review |
| Read the Logic Registry | Not an educational-system review |
| Inspect the source code | Not an engineering review |
| Inspect the database | Hidden state is not student-visible |
| Inspect hidden routes | Not student-accessible |
| Inspect admin pages | Not part of the student journey |
| Discuss findings with other reviewers before submission | Preserves independent judgment |

The reviewer **MUST**:

| Required | Reason |
|----------|--------|
| Judge only what the running application reveals | Product honesty standard |
| Record evidence for every major claim | Reproducibility |
| Verify every visible claim before crediting it | No assumed capability |
| Treat undemonstrable features as unavailable | No speculation |
| Use only student-accessible URLs and flows | Realistic experience |

### Permitted inputs

| Input | Use |
|-------|-----|
| Running application (staged RC build) | Primary evidence |
| Student credentials issued at commissioning | Access only |
| This commissioning document | Method and output structure |
| Personal study materials the persona would already own | Realistic external study context |

### Build access

Record at review start:

```
RC identifier: _______________________
Build URL: _______________________
Credentials issued: _______________________
Review start date: _______________________
Review end date: _______________________
```

---

# 5. Product Surfaces

The reviewer should **naturally explore** the following surfaces. No mandatory order. Touch each area at least once across the review window unless a dead end prevents it (record that).

| Surface | What to observe |
|---------|-----------------|
| Landing page | First impression, promises, version identity |
| Registration | If exposed; otherwise note absence |
| Onboarding | Plan creation, calibration, welcome flows |
| Calibration | Educational history, declarations, skip/abandon paths |
| Study Plan | Create, view, edit, switch; syllabus structure; pacing |
| Dashboard | Today's story; alignment with plan and mission |
| Today's Study Session | Mission → session → finish path |
| Practice Outcome Capture | Self-reported practice; validation; honest limits |
| Study Session Feedback | What happened / observed / concluded / next |
| Recommendations | Plan-bound suggestions; explainability |
| Analytics | Progress and estimates; consistency with dashboard |
| Settings | Changes reflected where expected |
| Research Check-in | If discoverable in normal navigation |
| General navigation | Sidebar, breadcrumbs, back paths, dead ends |
| Version identity | Strings, labels, build markers across surfaces |
| Overall consistency | One coherent product or competing stories |

**Minimum review window:** 3–5 calendar days with at least **3 distinct study sessions** of realistic length (45–90 minutes each, or persona-appropriate).

**Minimum journey:** First impression → onboarding (or returning-user equivalent) → active plan → daily study session (complete the loop) → return on a subsequent day → spot-check dashboard, recommendations, analytics or settings.

---

# 6. Review Dimensions

Evaluate the product across these dimensions. Each dimension informs category scores (§7).

| Dimension | Core question |
|-----------|---------------|
| **First Impression** | Within minutes, do I understand what this is and why I would use it? |
| **Onboarding Experience** | Can I reach a trustworthy active plan without excessive friction or repetition? |
| **Daily Study Workflow** | Can I complete a realistic study day and know what to do tomorrow? |
| **Educational Trust** | Do progress, estimates, guidance, and recommendations feel honest and non-contradictory? |
| **Product Trust** | Do dashboard, mission, plans, analytics, and settings tell one coherent story? |
| **Consistency** | Do labels, versions, messaging, and behaviour agree across surfaces? |
| **Clarity** | Is language student-centred? Are next actions obvious? |
| **Usability** | Can I study without workarounds, refresh rituals, or re-configuration? |
| **Motivation** | Does the product make me want to return tomorrow? |
| **Long-term Daily Use** | Would I still open this every day at week 4? Week 8? Week 12? |

### Educational Trust — specific probes

- Study Progress, Estimated Knowledge, and Educational Guidance remain distinguishable.
- Nothing claims mastery or exam readiness without evidence the product itself respects.
- Recommendations and missions match the active study plan and subject.
- Explainability does not invent unsupported claims.
- Self-reported practice limits are stated and honoured.

### Product Trust — specific probes

- Dashboard and Today's Mission agree after plan switch or next-day return.
- Analytics and dashboard do not disagree about what I have done.
- Unsupported or incomplete subjects are gated honestly — no "beautiful empty shell."
- Settings changes (where applicable) appear where students expect.

### Daily Workflow — specific probes

- Onboarding → plan → mission → session → practice capture → feedback closes cleanly.
- No competing "how did it go?" paths.
- Dead ends, broken buttons, and silent failures are recorded with evidence.
- Returning the next day does not require rebuilding context.

---

# 7. Scoring Framework

Use a **100-point scale**. Category scores sum to 100. Round final score to nearest whole number.

| Category | Weight | Score range | What it measures |
|----------|--------|-------------|------------------|
| First Impression | 10 | 0–10 | Landing, sign-in, initial promise vs early reality |
| Onboarding | 15 | 0–15 | Plan creation, calibration, time-to-trustworthy plan |
| Daily Workflow | 20 | 0–20 | Mission → session → capture → feedback → return |
| Educational Trust | 20 | 0–20 | Honesty of progress, estimates, guidance, recommendations |
| Product Trust | 15 | 0–15 | Cross-surface coherence; promise delivery |
| Consistency | 10 | 0–10 | Version strings, labels, messaging, behaviour alignment |
| Daily Dependence | 10 | 0–10 | Would I genuinely depend on this every day for three months? |

### Scoring guidance

| Band | Meaning |
|------|---------|
| 9–10 (or proportional) | Exceptional — would actively recommend |
| 7–8 | Strong — minor friction only |
| 5–6 | Adequate — usable with reservations |
| 3–4 | Weak — trust erosion; would hesitate |
| 0–2 | Failing — would abandon or not adopt |

**Overall Score** = sum of category scores.

Record a one-line justification per category. Do not adjust weights.

### Reference thresholds (non-binding)

| Overall Score | Typical posture |
|---------------|-----------------|
| ≥ 75 | Strong candidate for GO |
| 60–74 | CONDITIONAL GO territory — strengths real, dependence question unsettled |
| 45–59 | Significant trust or workflow gaps — likely CONDITIONAL GO or REJECT |
| < 45 | REJECT territory — would not adopt for exam preparation |

Thresholds inform judgment; they do not override evidence. A single Critical Finding may justify REJECT regardless of score.

---

# 8. Product Honesty

### Verify every claim

| Rule | Application |
|------|-------------|
| Never assume hidden capability | If not visible in the student UI, it does not exist |
| If a feature cannot be demonstrated, treat it as unavailable | Record "promised but not observed" |
| Do not speculate about Version 2 | Future intent is irrelevant |
| Do not reward good code | Engineering quality is invisible to students |
| Do not infer architecture | Behaviour is evidence; implementation is not |

### Landing page and marketing copy

Treat every bullet on the landing page and in-product headline as a **claim to verify**. Examples to check if present:

- Adaptive learning
- Intelligent study planning
- Daily missions
- Readiness or knowledge estimates
- Burnout monitoring
- Analytics depth

For each claim: **demonstrated**, **partially demonstrated**, or **not demonstrated**. Evidence required.

---

# 9. Release Discipline

Judge **only Version 1**.

| Do not penalise | Do penalise |
|-----------------|-------------|
| Intentionally deferred Version 2 functionality | Broken promises |
| Absence of future modules if not advertised | Confusing wording |
| Roadmap items not promised in the student UI | Contradictory behaviour |
| External study content not claimed to be in-app | Dead ends |
| | Untrustworthy communication |
| | Version or label mismatches |
| | Features advertised but absent |

### Version 2 Ideas section

Record Version 2 ideas **separately** in the output (§10). They must **not** reduce the Version 1 score. They inform future planning only.

---

# 10. Required Output

The reviewer submits **one self-contained report**. Copy the template below. Every major claim requires evidence: screen, quote, journey step, or observed behaviour.

```
==============================================================================
IPV-001 — INDEPENDENT PRODUCT VALIDATION REPORT
==============================================================================
Review ID: IPV-001-_______
Reviewer (identifier only): _______________________
Persona context: _______________________
RC identifier: _______________________
Build URL: _______________________
Review dates: _______________________
Sessions completed: _______
Total realistic study time: _______ minutes

------------------------------------------------------------------------------
EXECUTIVE SUMMARY
------------------------------------------------------------------------------
(3–6 paragraphs. Answer the mission question directly. No jargon.)

------------------------------------------------------------------------------
OVERALL SCORE: ___ / 100
------------------------------------------------------------------------------

------------------------------------------------------------------------------
CATEGORY SCORES
------------------------------------------------------------------------------
First Impression:     ___ / 10   — justification:
Onboarding:           ___ / 15   — justification:
Daily Workflow:       ___ / 20   — justification:
Educational Trust:    ___ / 20   — justification:
Product Trust:        ___ / 15   — justification:
Consistency:          ___ / 10   — justification:
Daily Dependence:     ___ / 10   — justification:

------------------------------------------------------------------------------
TOP STRENGTHS (3–5)
------------------------------------------------------------------------------
1.
2.
3.

------------------------------------------------------------------------------
TOP WEAKNESSES (3–5)
------------------------------------------------------------------------------
1.
2.
3.

------------------------------------------------------------------------------
EVIDENCE LOG
------------------------------------------------------------------------------
(Major claims only. Format: Claim → Evidence → Impact on trust)

------------------------------------------------------------------------------
WOULD I USE THIS EVERY DAY?
------------------------------------------------------------------------------
Yes / Hesitant / No — with reasoning tied to the three-month horizon.

------------------------------------------------------------------------------
WOULD I RECOMMEND IT?
------------------------------------------------------------------------------
Yes / Hesitant / No — to whom, and with what caveats.

------------------------------------------------------------------------------
RELEASE RECOMMENDATION
------------------------------------------------------------------------------
[ ] GO
[ ] CONDITIONAL GO
[ ] REJECT

One paragraph: what would need to change for the next band (if not GO).

------------------------------------------------------------------------------
FINDINGS
------------------------------------------------------------------------------

CRITICAL (release blockers — broken journeys, trust collapse, false claims)
-
-

HIGH (serious friction or contradiction — likely to cause abandonment)
-
-

MEDIUM (noticeable issues — survivable but damaging)
-
-

LOW (polish, minor confusion, nice-to-have)
-
-

------------------------------------------------------------------------------
VERSION 2 IDEAS (do not affect score)
------------------------------------------------------------------------------
-
-

------------------------------------------------------------------------------
ONE-SENTENCE VERDICT (suitable for the website)
------------------------------------------------------------------------------
(Student voice. Honest. No marketing fluff.)

------------------------------------------------------------------------------
METHODOLOGY ATTESTATION
------------------------------------------------------------------------------
[ ] I did not read architecture, release, or blind-review documentation
[ ] I did not read the Constitution or Logic Registry
[ ] I did not inspect source code, database, or admin pages
[ ] I judged only the running application as a student
[ ] I recorded evidence for major claims
[ ] I treated undemonstrable features as unavailable
```

---

# 11. Release Decision

Executive Review records one outcome based on the submitted report and this commission.

| Decision | Meaning |
|----------|---------|
| **GO** | Release Candidate is trustworthy enough to enter Internal Alpha as the Version 1 baseline. Daily dependence question is sufficiently answered. No unresolved Critical Findings. |
| **CONDITIONAL GO** | Enter Internal Alpha with named conditions tracked. Usable for real study but material trust, workflow, or communication gaps require explicit follow-up before Version 1.0 promotion. |
| **REJECT** | Not trustworthy enough for Internal Alpha. Critical journeys broken, trust collapse, or mission question answered "No" with evidence. Return to stabilisation. |

### Decision inputs

| Input | Weight |
|-------|--------|
| Overall Score | Strong signal, not sole determinant |
| Daily Dependence category | Primary mission alignment |
| Critical / High Findings | May override score |
| Evidence quality | Must support reproducibility |
| Methodology attestation | Must be complete |

### Relationship to other validation

| Capability | Relationship |
|------------|--------------|
| V1S-005 Internal Alpha Release Validation | Runs **after** IPV-001 GO or CONDITIONAL GO; cohort feedback during Internal Alpha |
| V1R-001 Release Certification | Composite certification; IPV-001 is the product-trust input before Internal Alpha |
| Blind Internal Alpha Reviews | Historical persona reviews; IPV-001 supersedes as formal pre-Internal-Alpha gate |

---

# 12. Success Criteria

The review is successful when:

1. A skeptical first-time student persona is maintained throughout.
2. Independence requirements (§4) are attested and credible.
3. Every major claim in the report has observable evidence.
4. The mission question is answered directly — not deferred.
5. Category scores sum to the Overall Score with per-category justification.
6. Findings are classified CRITICAL / HIGH / MEDIUM / LOW with proportionate evidence.
7. Version 2 ideas are separated and do not contaminate Version 1 scoring.
8. Another independent reviewer could repeat the exercise and reasonably reach similar conclusions.

---

# 13. Known Constraints

| Constraint | Implication |
|------------|-------------|
| Reviewer must not invent functionality | Report only observed behaviour |
| Reviewer must not infer architecture | "It probably works because…" is out of scope |
| Reviewer must not reward good code | Invisible engineering does not score |
| Reviewer must judge only the product | Documentation quality is irrelevant |
| No application code changes under IPV-001 | Findings feed stabilisation backlog; not fixed in this capability |
| Single reviewer default | Executive may commission a second reviewer for corroboration; not required by this document |
| Registration may not be publicly exposed | Note absence; do not penalise if not advertised |

---

# 14. Reproducibility Protocol

To allow a second reviewer to repeat the exercise:

### Before starting

1. Executive issues RC build URL and student credentials.
2. Reviewer confirms no prior Kwalitec exposure.
3. Reviewer reads **only** this document.
4. Reviewer records persona context and dates.

### During review

1. Complete at least 3 realistic study sessions over 3–5 days.
2. Log confusion, surprise, and trust movement as they occur.
3. Screenshot or quote key claims where possible.
4. Complete the full daily loop at least twice.
5. Return on a subsequent day without re-onboarding.

### After review

1. Complete the output template (§10) in full.
2. Attest methodology compliance.
3. Submit to Executive Review. Do not discuss with other reviewers before submission.

---

# 15. Completion Report (IPV-001 Commissioning)

*This section records delivery of the commissioning document. Validation execution is a separate activity.*

## Executive Summary

IPV-001 commissions the final independent product validation of Kwalitec Version 1 Release Candidate before Internal Alpha. The reviewer acts as a skeptical first-time student and answers whether they would genuinely depend on Kwalitec every day for three months if professional examinations began tomorrow. The commission is blind, reproducible, and product-only — not architecture, educational, or engineering review.

## Purpose

Provide a single authoritative commissioning document that:

- Defines reviewer persona, independence constraints, and product surfaces
- Establishes a 100-point scoring framework aligned to daily dependence
- Requires evidence-based output with REJECT / CONDITIONAL GO / GO recommendation
- Gates Internal Alpha entry on credible product trust

## Reviewer Constraints

- No documentation archaeology (architecture, release, blind reviews, Constitution, Logic Registry)
- No code, database, hidden route, or admin inspection
- Judge only the running application as a student
- Verify every claim; treat undemonstrable features as unavailable
- Natural exploration — no forced checklist order

## Scoring Framework

| Category | Weight |
|----------|--------|
| First Impression | 10 |
| Onboarding | 15 |
| Daily Workflow | 20 |
| Educational Trust | 20 |
| Product Trust | 15 |
| Consistency | 10 |
| Daily Dependence | 10 |
| **Total** | **100** |

## Files Created

- `knowledge/release/IPV-001_INDEPENDENT_PRODUCT_VALIDATION.md`

## Files Modified

- None

## Tests Executed

- None (documentation-only)

## Migration Impact

- None

## Architecture Compliance

- No application code modified.
- No layering, curriculum, or schema changes.
- Commission respects product-only validation posture; services and routes are not in scope for the reviewer.
- Curriculum V1/V2 invariants: N/A — reviewer does not inspect curriculum engine or JSON.

## Known Limitations

- This document commissions the review; it does not execute it.
- Single-reviewer default — corroboration is Executive discretion.
- Scoring thresholds are guidance, not automatic decision rules.
- Findings from IPV-001 feed stabilisation and V1S-005; remediation is out of scope here.
- Registration exposure depends on deployment posture; reviewer records what is visible.

---

**Status:** SUBMITTED — awaiting Executive Review  
**Stop.** Return for Executive Review.
