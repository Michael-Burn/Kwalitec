# Educational Release Standard

**Framework ID:** EVF-002  
**Programme:** Programme V — Educational Validation Framework  
**Classification:** Mandatory educational release bar  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Effective:** July 2026  

---

## 1. Purpose

This Standard defines **what “good enough to release” means** educationally for each Kwalitec version.

It is subordinate to the Educational Validation Constitution (EVF-001).  
It is complementary to Educational Governance Review (EGI-003), which certifies educational *truth/integrity*.  
This Standard certifies educational *quality and trust* for student release.

---

## 2. Governing question

For the candidate version under review:

> Has independent educational validation demonstrated sufficient educational quality to justify releasing this version to students?

---

## 3. Version 1.0 Release Standard

### 3.1 Capability trust requirements

Version 1.0 is educationally approvable only if independent validation demonstrates that each required capability is trusted:

| Capability ID | Capability | Must be trusted |
|---|---|---|
| EC-01 | Master Planner | Study Plans |
| EC-02 | Daily Coach | Daily Missions |
| EC-04 | Recovery Coach | Recovery Plans |
| EC-05 | Revision Coach | Revision Strategy |
| EC-06 | Exam Coach | Readiness Assessment |
| EC-03 | Learning Coach | Educational explanations |

“Trusted” means: under Layer 1–3 evidence, reviewers judge the capability educationally usable, honest, and preferable enough that a careful IFoA candidate could rely on it within its stated bounds — without requiring belief in unsupported claims.

### 3.2 Overall educational trust threshold

| Metric | Version 1.0 bar |
|---|---|
| **Overall Educational Trust** | **≥ 80%** |

Overall Educational Trust is computed by the Educational Release Gate from capability results, comparative preference, dimension scores, and supporting evidence (see §5 and `EDUCATIONAL_RELEASE_GATE.md`). It is **not** a Runtime A metric and **not** an automated Twin score.

### 3.3 Mandatory evidence families for Version 1.0

| Evidence family | Required |
|---|---|
| Layer 1 capability validation reports for EC-01–EC-06 | Yes |
| Layer 2 Blind Comparative Review (or valid Blind Review corpus mapped per EVF comparative protocol) | Yes |
| Layer 3 dimension assessment per capability | Yes |
| Educational Governance Review outcome APPROVED (EGI-003) for the educational surfaces in scope | Yes (prerequisite) |
| Supporting educational evidence register (links to reviews, baselines, limitations) | Yes |

### 3.4 Non-waivable Version 1.0 failures

Any of the following blocks APPROVED (CONDITIONAL APPROVAL only if explicitly allowed by the Gate for that failure class):

1. Overall Educational Trust below 80%  
2. Any required capability rated **Not Trusted** without an approved hold  
3. Systematic preference for Human Tutor **and** Alternative Planning Strategy over Kwalitec on the primary planning/mission tasks, without compensating educational strengths documented in the Version Approval Report  
4. Persistent dual-truth or certainty-without-inspectability findings that EGI-003 would also reject  
5. Missing Version Approval Report  

---

## 4. Standards for later versions

Future versions (1.x, 2.0, …) inherit this Standard and may raise thresholds or add capabilities by amending this document.

| Rule | Requirement |
|---|---|
| Additive capabilities | New EC-IDs registered in Capability Validation Guide before gate |
| Threshold changes | Explicit amendment; never silent |
| Evidence reuse | Prior reports may be reused only if baseline and product behaviour are declared unchanged for the reused scope |
| Regression | A previously trusted capability that falls below trust in a new candidate must be treated as a new failure |

Default posture for Version 2.0 planning: raise the bar; do not lower Version 1.0’s 80% trust floor without constitutional amendment.

---

## 5. How Overall Educational Trust is expressed

Overall Educational Trust is a **governed percentage** published in the Version Approval Report.

### 5.1 Composition (Version 1.0)

| Component | Weight | Source |
|---|---:|---|
| Capability Trust Index | 40% | Layer 1 — mean of trusted capability scores |
| Comparative Preference Index | 25% | Layer 2 — preference for Kwalitec vs benchmarks on registered tasks |
| Dimension Quality Index | 25% | Layer 3 — mean applicable dimension scores across capabilities |
| Supporting Evidence Integrity | 10% | Completeness, currency, and conflict-handling of the evidence pack |

Each component is scored 0–100 before weighting. The Gate document defines scoring bands and conversion rules so results remain explainable.

### 5.2 Explainability requirement

The Version Approval Report must show:

- the four component scores;
- the weighted total;
- the decisive strengths and weaknesses;
- why the outcome is APPROVED, CONDITIONAL APPROVAL, or REJECTED.

Opaque single-number dashboards without this breakdown are non-compliant.

---

## 6. Relationship to other release bars

| Bar | Owns | Does not replace |
|---|---|---|
| Educational Release Standard (this document) | Educational quality / trust | Architecture, security, GA |
| EGI-003 Educational Governance Review | Educational truth / integrity | Student preference research |
| GA / Release Protocol | Operational ship readiness | Educational trust |
| EP-003 Go/No-Go (historical) | Early effectiveness programme framing | EVF Layer 4 authority |

For student-facing educational claims on a version, **EVF Layer 4 is authoritative**.

---

## 7. Claim freeze

Until a version is APPROVED (or CONDITIONAL APPROVAL with explicit allowed claims):

- Do not market recommendation effectiveness as proven;
- Do not claim exam-mark improvement;
- Do not claim mastery or readiness beyond what validated capabilities support;
- Do not treat engineering certification as educational certification.

---

## 8. Cross references

- `EDUCATIONAL_VALIDATION_CONSTITUTION.md`  
- `EDUCATIONAL_RELEASE_GATE.md`  
- `CAPABILITY_VALIDATION_GUIDE.md`  
- `BLIND_COMPARATIVE_REVIEW.md`  
- `EDUCATIONAL_DIMENSIONS.md`  
- `RELEASE_DECISION_TEMPLATE.md`  
