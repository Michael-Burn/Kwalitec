# Product Communication Standard

**Capability ID:** PTP-003  
**Programme:** Product Trust Programme  
**Title:** Honest Product Communication  
**Priority:** P0  
**Status:** Implemented — awaiting Architecture Review  
**Date:** 2026-07-15  
**Nature:** Product trust — honest labelling of educational claims without redesigning educational cores  

---

## Executive Summary

Blind Internal Alpha Review v2 identified hesitation around self-reported
practice, estimated metrics, empty analytics, and unexplained educational
values. Educational truth is already governed by the Educational Constitution
and Educational Integrity Programme. This standard governs how those truths
are **spoken** to the student.

The goal is not more information. The goal is **removing uncertainty**.

PTP-003 introduces a fixed communication taxonomy and mandatory honesty
phrases for estimated, unavailable, self-reported, empty, and unsupported
claims on Version 1 student surfaces. It does **not** redesign Evidence
Authority, Digital Twin, Educational Intelligence, readiness maths,
recommendation algorithms, or the Learning Experience workflow.

---

## Authority

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md` — educational truth  
2. `EDUCATIONAL_LOGIC_REGISTRY.md` — operational educational behaviour  
3. Educational Integrity Programme (EIP) — meaning, evidence, explainability  
4. Learning Experience Programme Sprint 1 (LXP) — daily loop honesty  
5. `PRODUCT_TRUST_PROGRAMME.md` (PTP-000) — product trust roadmap  
6. PTP-001 Supported Subject Integrity — unsupported examination speech  
7. PTP-002 Single Source of Truth — workflow authority (affects CTAs only)  

Implementation owner for shared phrases: `ProductCommunicationService`.

---

## 1. Communication taxonomy

Every student-facing educational claim must be classifiable as exactly one of:

| Category | Student meaning | Example |
|----------|-----------------|---------|
| **Observed Fact** | Something the student (or product) recorded as it happened | “You attempted 7 questions today.” |
| **Derived Fact** | A calculation from Observed Facts with no judgement of understanding | Syllabus coverage % from completed-studying topics |
| **Estimated Value** | A provisional judgement of understanding or preparation | Estimated Knowledge %; Estimated readiness % |
| **Unavailable** | A value that could exist later but cannot be shown yet | Readiness before enough practice; empty accuracy chart |
| **Coming Soon** | A feature or paper that is announced but not ready | PTP-001 Coming Soon papers |
| **Not Supported** | Outside Version 1 capability | Unsupported examinations (PTP-001) |

### Vocabulary glossary (Version 1)

| Term | Category | Honest meaning |
|------|----------|----------------|
| **Practice Results** | Observed Fact (self-reported) | Counts the student recorded after a Study Session |
| **Study Progress** | Observed Fact / Derived Fact | Topics marked or earned as completed studying |
| **Syllabus coverage** | Derived Fact | Weighted share of syllabus completed studying |
| **Accuracy** | Derived Fact (from self-report) | Correct ÷ attempted from recorded Practice Results |
| **Estimated Knowledge** | Estimated Value | Provisional understanding signal from recorded practice |
| **Estimated readiness** | Estimated Value | Provisional preparation judgement — not an exam outcome |
| **Today's Recommendation** | Educational Advice (not a fact category above) | Guidance; must not replace Mission authority |

Internal engineering terms (“mastery score”, “digital twin”, “evidence warrant”)
must not appear as student-facing labels.

---

## 2. Product Communication Audit (Version 1)

Surfaces reviewed: Dashboard, Mission, Study Session / Practice Outcome /
Feedback, Analytics, Study Plan roadmap, Recommendations, subject-support
gates, login marketing.

### 2.1 Classification summary

| Claim | Primary surfaces | Classification | Misunderstand risk (pre-PTP-003) | Minimum honesty required |
|-------|------------------|----------------|----------------------------------|--------------------------|
| Estimated Knowledge % / `% est.` badges | Dashboard, Analytics, Study Plan | Estimated Value | Yes — reads as “I know X%” | Label as Estimated; basis: recorded practice outcomes |
| Estimated Knowledge empty lists | Dashboard, Analytics | Unavailable | Low if empty text present | Explain practice is required; SP ≠ understanding |
| Syllabus coverage | Dashboard Progress through Study Plan, Mission | Derived Fact | Mild — can feel like readiness | Explain SP-derived; not Estimated Knowledge; single Dashboard progress % (PTP-004) |
| Estimated readiness | Dashboard, Analytics | Estimated Value | Yes — looks like exam readiness | “Estimated”; provisional; evidence basis |
| Readiness unavailable / empty | Dashboard, Analytics | Unavailable | Yes if blank | Why unavailable + what unlocks it |
| Practice Results form | Mission Practice Outcome Capture | Observed Fact (self-reported) | Mild without “you recorded” | State results are self-recorded after today’s session; not mastery |
| Session feedback conclusions | Study Session Feedback | Observed / Unavailable | Low (already strong) | Preserve LXP-004 honesty |
| Accuracy trend / weekly accuracy | Analytics | Derived Fact (self-reported inputs) | Yes — “Accuracy” ≈ grade | State calculated from recorded practice |
| Syllabus coverage (single progress story) | Dashboard Progress through Study Plan | Derived Fact | Mild — can feel like readiness | One authoritative % only (PTP-004 removed sibling Curriculum/Weighted Coverage from Dashboard) |
| Today's Recommendation | Dashboard | Advice + Estimates | Mild | EIP-003 explainability block |
| Learning Outcomes placeholder `—` | Study Plan roadmap | Unavailable / Coming Soon | Mild | Explicit “not available yet” |
| Unsupported / Coming Soon papers | Study Plan wizard | Coming Soon / Not Supported | No when gated | PTP-001 (unchanged) |
| Login “Exam Readiness Analytics” | Marketing | Overclaim risk | Yes | Soften to Estimated readiness language |

### 2.2 Audit verdict

Educational cores already produce lawful meaning (EIP/LXP). Remaining product
trust debt was **uneven honesty labelling**: Estimated Knowledge often relied
on hover titles; legacy readiness fallbacks lacked basis text; Practice
Results and Accuracy did not always state self-report; empty analytics
sometimes under-explained; marketing overclaimed “Exam Readiness”.

---

## 3. Communication rules

### R-1 — Estimated values must be labelled and based

Every Estimated Value must:

1. Use the word **Estimated** (or an approved estimate label such as `% est.`
   with an accessible basis).  
2. State its **basis** in a tooltip, caption, or adjacent sentence.  
3. Never imply certified mastery, exam outcome, or verified in-app scoring.

**Canonical Estimated Knowledge basis**

> Based on your recorded practice outcomes.

**Canonical Estimated readiness unavailable**

> We need more recorded practice before this estimate becomes available.

### R-2 — Unavailable values must explain the gap

An Unavailable claim must never render as a silent blank that could be read as
“zero” or “failed.” Show `—` or empty-state copy that answers:

1. What is missing, and  
2. What the student can do next (without inventing a second workflow).

### R-3 — Self-reported inputs must be named as recorded

Practice Results, Accuracy, and any downstream estimate whose warrant is
self-report must make clear that values reflect **what the student recorded**,
not independently verified exam performance.

**Canonical Practice Results basis**

> These results reflect the answers you recorded after today's study session.

Inventing verification, question banks, or proctoring is out of scope.

### R-4 — Empty states must explain emptiness

Charts, topic lists, and metric cards without data must say why they are empty
and what unlocks them. Prefer short sentences over disclaimer essays.

### R-5 — Unsupported features use PTP-001 vocabulary

Coming Soon and Not Supported examination speech remains owned by PTP-001 /
`SubjectSupportService`. This standard does not invent alternate support copy.

### R-6 — Tooltips carry basis; panels carry narrative

| Device | Use for |
|--------|---------|
| **Tooltip / `title` / `aria-label`** | Compact basis on compact metrics (`% est.` badges) |
| **Caption / microcopy under a number** | One-line basis when the metric is hero-sized |
| **Information panel / explainability block** | EIP-003 Observed / Estimates / Advice / Next structure |
| **Empty-state paragraph** | Unavailable explanation |

Do not duplicate full Constitution lectures on every surface (Blind Review v2
disclaimer fatigue). One honest sentence is preferred when the claim type is
already labelled.

### R-7 — Microcopy must reduce uncertainty, not add theatre

Forbidden student-facing phrasing patterns:

- Presenting estimates as facts (“You know 72% of this topic”)  
- Exam-outcome guarantees from Estimated readiness  
- “Mastered” as a student label (use “Strong estimated knowledge”)  
- Engineering jargon leaks  
- Silent empty cells for educational metrics  

Allowed strength language in recommendations must remain **advice**, with
explainability where EIP-003 already applies. Coverage hyperbole that implies
understanding (“no blind spots” as knowledge guarantee) is discouraged;
PTP-004/005 may harden recommendation copy further.

### R-8 — Marketing must not overclaim product claims

Login and public marketing surfaces must not promise “Exam Readiness” as a
certainty product. Prefer **Estimated readiness** / study insights language
aligned with in-app labels.

---

## 4. Implementation summary

| Area | Change |
|------|--------|
| Shared phrases | `app/services/product_communication_service.py` |
| Estimated Knowledge badges | Tooltip/title → recorded practice outcomes basis |
| Study Plan roadmap EK | Visible basis under the metric |
| Practice Outcome Capture | Self-recorded results sentence |
| Session feedback (practice recorded) | Observed facts acknowledge self-recording |
| Readiness unavailable | Standard “more recorded practice” sentence when thin |
| Dashboard legacy readiness fallback | Basis microcopy when narrative absent |
| Dashboard / Analytics EK empty states | Preserve honest empty copy; align with basis |
| Analytics Coverage label | “Syllabus coverage” (not bare “Coverage”) |
| Analytics Accuracy | Self-report basis caption / empty-state clarity |
| Login marketing | Soften “Exam Readiness Analytics” |
| Learning Outcomes `—` | “Not available yet” |
| Unsupported papers | Unchanged — PTP-001 |

No changes to readiness scoring, recommendation selection, Evidence Authority
ranks, Mission selection, or Study Session workflow steps.

---

## 5. Examples

### Estimated Knowledge

```
72% est.
title / caption: Based on your recorded practice outcomes.
```

### Readiness unavailable

```
Estimated readiness
We need more recorded practice before this estimate becomes available.
```

### Practice Results

```
How did practice go?
These results reflect the answers you recorded after today's study session.
This is not a knowledge or mastery rating.
```

### Unsupported papers

Governed by PTP-001 (Coming Soon / Not Supported gate panels). Unchanged.

### Empty analytics accuracy

```
Accuracy Trend
Accuracy appears after you record practice results in Study Sessions.
Accuracy is calculated from practice results you recorded — not a verified exam score.
```

---

## 6. Testing expectations

Regression tests (`tests/test_ptp003_honest_product_communication.py`) verify:

1. Every shared Estimated Value phrase is labelled and based.  
2. Unavailable readiness speech explains the gap.  
3. Practice Results and Accuracy self-report honesty is present on student templates.  
4. No unsupported educational claim patterns from this standard’s forbidden set.  
5. Empty educational metric states are not unexplained blanks.  
6. PTP-001 support speech remains the authority for Coming Soon / Not Supported.

---

## 7. Known limitations

1. **PTP-004** still owns consolidating multiple coverage percentages into one
   Dashboard narrative. This standard clarifies labels/basis only.  
2. **PTP-005** still owns broader terminology/version polish and disclaimer
   fatigue reduction across all surfaces.  
3. Self-report transparency does **not** create verified practice evidence.  
4. Legacy recommendation strings with strong coverage language may remain until
   a later capability trims them; EIP-003 explainability remains the primary
   honesty layer for recommendation cards.  
5. Chart series names in JavaScript may still shorten labels; surrounding titles
   and captions carry the honesty requirement.

---

## Cross references

| Document | Role |
|----------|------|
| `PRODUCT_TRUST_PROGRAMME.md` | Programme capability PTP-003 |
| `PTP-001_SUPPORTED_SUBJECT_INTEGRITY.md` | Unsupported / Coming Soon speech |
| `PTP-002_SINGLE_SOURCE_OF_TRUTH.md` | Single daily workflow / CTA authority |
| `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` | EIP-003 narrative structure |
| `EDUCATIONAL_EVIDENCE_AUTHORITY.md` | Evidence limits disclosed, not rewritten |
| `BLIND_INTERNAL_ALPHA_REVIEW_V2.md` | Product evidence for trust hesitation |

---

**End of Product Communication Standard (PTP-003).**  
**Stop. Return for Architecture Review.**
