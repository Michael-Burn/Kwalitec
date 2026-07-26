# Capability Validation Guide

**Framework ID:** EVF-010  
**Programme:** Programme V — Educational Validation Framework  
**Classification:** Layer 1 — Educational Capability Validation  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Effective:** July 2026  

---

## 1. Purpose

Layer 1 evaluates each educational capability **independently**.

A version may be engineering-complete and still fail educationally if any required capability is not trusted.

Capability validation produces a dedicated report under `capability_reviews/`. Strength in one capability does not waive weakness in another.

---

## 2. Version 1 capability register

| ID | Capability | Validates trust in | Primary student surfaces (illustrative) |
|---|---|---|---|
| **EC-01** | Master Planner | Study Plans | Study Plan, syllabus sequencing, plan continuity |
| **EC-02** | Daily Coach | Daily Missions | Today’s Mission / Session, nightly checklist |
| **EC-03** | Learning Coach | Educational explanations | Coach guidance, What/Why/Next narratives |
| **EC-04** | Recovery Coach | Recovery Plans | Restart after missed days / failure recovery |
| **EC-05** | Revision Coach | Revision Strategy | Revision mode / late-stage planning |
| **EC-06** | Exam Coach | Readiness Assessment | Readiness, exam preparation honesty |

Future capabilities receive new EC-IDs in this register before they may enter a Release Gate.

---

## 3. Independence rules

1. One capability per report (EC-ID in filename).  
2. Reviewers judge the capability as experienced by students — not by reading Runtime A code.  
3. Do not score architecture elegance, test coverage, or Twin internals.  
4. Do not mutate product behaviour during validation.  
5. Cite Blind Review evidence where relevant; do not re-run Blind Review inside a capability report unless executing a scheduled research cycle.  
6. If evidence is insufficient, rate **Insufficient Evidence** — do not invent trust.

---

## 4. Validation method

For each capability:

1. **Scope** — what educational job this capability claims to do.  
2. **Baseline** — product/version/baseline identifier under review.  
3. **Evidence pack** — student-visible behaviour, Blind Review citations, prior capability reports if reused.  
4. **Dimension assessment** — per `EDUCATIONAL_DIMENSIONS.md`.  
5. **Trust verdict** — Trusted / Conditionally Trusted / Not Trusted / Insufficient Evidence.  
6. **Risks & holds** — outstanding educational risks.  
7. **Gate implication** — how this result should weight Layer 4.

### Trust verdict definitions

| Verdict | Meaning |
|---|---|
| **Trusted** | Capability meets Version educational quality for its claimed job |
| **Conditionally Trusted** | Usable with named holds and claim limits |
| **Not Trusted** | Students should not rely on this capability for the claimed job |
| **Insufficient Evidence** | Cannot validate; Gate blocker until evidence exists |

---

## 5. Capability-specific focus prompts

These prompts guide evidence collection. They are not Blind Review personas.

### EC-01 Master Planner

- Is the Study Plan educationally coherent with syllabus order?  
- Can the student trust near-term sequencing without calendar theatre?  
- Are plan changes explainable and continuous after interruption?

### EC-02 Daily Coach

- Does tonight’s Mission answer “what should I do now?” without dithering?  
- Is duration/workload practical for a weeknight?  
- Is completion distinguished from understanding?

### EC-03 Learning Coach

- Are explanations inspectable (What / Why / Next)?  
- Are certainty and evidence strength honest?  
- Does coaching language avoid Twin/engineering jargon?

### EC-04 Recovery Coach

- After missed days or failure, is recovery actionable and non-shaming?  
- Does recovery restore productive study without false mastery repair claims?

### EC-05 Revision Coach

- Is revision strategy realistic for remaining time?  
- Does it prioritise exam-relevant work without pretending full re-teaching?

### EC-06 Exam Coach

- Is Readiness Assessment calibrated and bounded?  
- Does it refuse unsupported exam-mark promises?  
- Does it connect preparation actions to readiness claims honestly?

---

## 6. Report location and naming

```
knowledge/educational_validation/capability_reviews/
  EC-01_master_planner_<version>_<YYYYMMDD>.md
  EC-02_daily_coach_<version>_<YYYYMMDD>.md
  …
```

Use the template in §8.

---

## 7. Relationship to Blind Review

| Blind Review | Capability Validation |
|---|---|
| Persona-bound hypotheses (SV-001…SV-020) | Capability-bound trust verdicts (EC-01…EC-06) |
| First-person research transcripts | Structured educational quality reports |
| Must remain intact | Consumes Blind Review as evidence |

Map Blind Review findings thematically (planning, mission, recovery, revision, readiness, explainability) into the relevant EC report’s evidence section. Do not “fix” Blind Review scores inside capability math.

---

## 8. Capability validation report template

```markdown
# Capability Validation Report — EC-XX <Name>

- Framework: EVF Layer 1
- Capability ID:
- Version / candidate:
- Baseline ID:
- Review date:
- Reviewer(s):
- EVF documents version: 1.0

## 1. Capability scope
- Claimed educational job:
- In scope surfaces:
- Explicit non-goals:

## 2. Evidence pack
- Student-visible observations:
- Blind Review citations (IDs / paths):
- Other educational evidence:
- Evidence gaps:

## 3. Dimension assessment
| Dimension | Applicability | Rating | Evidence |
|---|---|---|---|
| ED-01 Educational Soundness | | | |
| ED-02 Exam Readiness | | | |
| ED-03 Practicality | | | |
| ED-04 Personalisation | | | |
| ED-05 Explainability | | | |
| ED-06 Motivation | | | |
| ED-07 Consistency | | | |
| ED-08 Confidence | | | |

## 4. Educational strengths
-

## 5. Educational weaknesses
-

## 6. Trust verdict
- Trusted | Conditionally Trusted | Not Trusted | Insufficient Evidence
- Rationale:

## 7. Holds / claim limits
-

## 8. Outstanding risks
-

## 9. Gate implication
- Suggested contribution to Capability Trust Index:
```

---

## 9. Cross references

- `EDUCATIONAL_DIMENSIONS.md`  
- `EDUCATIONAL_RELEASE_GATE.md`  
- `BLIND_COMPARATIVE_REVIEW.md`  
- `REVIEWER_GUIDELINES.md`  
- `capability_reviews/README.md`  
