# Educational Release Gate

**Framework ID:** EVF-004  
**Programme:** Programme V — Educational Validation Framework  
**Classification:** Official educational approval authority  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Effective:** July 2026  

---

## 1. Purpose

The Educational Release Gate (Layer 4) determines whether the current release candidate satisfies educational requirements.

It is the **official educational approval authority** for Kwalitec versions.

No educational implementation, private-beta expansion under educational claims, or version marketing of educational quality may bypass this Gate.

---

## 2. Gate inputs

The Gate evaluates four evidence families:

| Input | Primary sources |
|---|---|
| **Capability Validation** | `capability_reviews/` reports for required EC-IDs |
| **Blind Comparative Review** | Comparative records + Blind Review corpus mapped per `BLIND_COMPARATIVE_REVIEW.md` |
| **Educational Dimensions** | Dimension matrices in capability reviews / `reports/` |
| **Supporting Educational Evidence** | Baselines, limitations, EGI-003 outcome, evidence register |

Optional but recommended:

- Benchmark reviews under `benchmark_reviews/`  
- Meta-analysis / research synthesis (as secondary evidence only)  

---

## 3. Prerequisites (must be true before Gate scoring)

| Prerequisite | Authority |
|---|---|
| Educational Constitution compliance for in-scope claims | EGI-001 |
| Educational Governance Review outcome **APPROVED** (conditions cleared for release class) | EGI-003 |
| Blind Review subsystem left intact (no protocol mutation for this gate) | EVF Constitution Art. II |
| Candidate version and baseline identified | Version Approval Workflow |
| Version Approval Report draft started from template | `RELEASE_DECISION_TEMPLATE.md` |

If prerequisites fail → Gate outcome is **REJECTED** (or halt: do not score quality until integrity prerequisites clear).

---

## 4. Scoring procedure

### 4.1 Capability Trust Index (weight 40%)

For each required capability:

| Trust band | Score |
|---|---:|
| Trusted | 100 |
| Conditionally Trusted | 70 |
| Not Trusted | 0 |
| Insufficient Evidence | 0 (and flag blocker) |

Capability Trust Index = mean of required capability scores.

Version 1.0 required set: EC-01, EC-02, EC-03, EC-04, EC-05, EC-06.

### 4.2 Comparative Preference Index (weight 25%)

From Blind Comparative Review tasks registered for the version:

| Result pattern | Score guidance |
|---|---:|
| Kwalitec preferred with educational reasoning on ≥60% of primary tasks | 85–100 |
| Mixed preference; Kwalitec competitive on core nightly/planning tasks | 60–84 |
| Human Tutor or Alternative Strategy clearly preferred on core tasks | 0–59 |
| Comparative evidence missing or non-blind | 0 + blocker |

Exact task set and computation worksheet live in the Version Approval Report. Scores must cite task IDs.

### 4.3 Dimension Quality Index (weight 25%)

Convert each applicable dimension rating to a 0–100 score (see `EDUCATIONAL_DIMENSIONS.md`), then mean across required capabilities’ applicable dimensions.

Version 1.0 expects explicit evaluation of at least:

- Educational Soundness  
- Exam Readiness  
- Practicality  
- Personalisation  
- Explainability  
- Motivation  
- Consistency  
- Confidence  

### 4.4 Supporting Evidence Integrity (weight 10%)

| Check | Pass contribution |
|---|---:|
| All required artefacts present and path-cited | 40 |
| Baseline frozen / declared | 20 |
| Conflicts between evidence families disclosed | 20 |
| Limitations and outstanding risks listed | 20 |

Missing artefacts → score 0 and Gate blocker.

### 4.5 Overall Educational Trust

```
Overall Educational Trust =
  0.40 × Capability Trust Index
+ 0.25 × Comparative Preference Index
+ 0.25 × Dimension Quality Index
+ 0.10 × Supporting Evidence Integrity
```

Round to nearest whole percent for publication. Show unrounded worksheet in the report appendix if needed.

---

## 5. Outcomes

| Outcome | Criteria (Version 1.0) |
|---|---|
| **APPROVED** | Overall Educational Trust ≥ 80%; no required capability Not Trusted; no active blockers; prerequisites met |
| **CONDITIONAL APPROVAL** | Overall Educational Trust ≥ 70% **and** < 80%, **or** one Conditionally Trusted required capability with explicit holds; no dual-truth integrity failure; student-facing claim freeze documented |
| **REJECTED** | Overall Educational Trust < 70%, **or** any required capability Not Trusted without approved exception path, **or** prerequisite failure, **or** comparative/evidence blockers |

### CONDITIONAL APPROVAL holds (mandatory fields)

Each hold must state:

1. Capability / claim affected  
2. Why release may still proceed for limited use  
3. Student-facing honesty requirement  
4. Expiry or re-validation trigger  
5. Owner  

Expired holds without re-validation → treat as REJECTED for subsequent expansion.

---

## 6. Bypass prohibition

The following are **not** valid substitutes for Gate APPROVED / CONDITIONAL APPROVAL:

- Green CI / pytest / ruff  
- GA operational certification alone  
- Architecture review alone  
- EGI-003 APPROVED alone  
- Founder preference  
- Feature completeness checklists  
- Silent reuse of an older Version Approval Report for a changed baseline  

---

## 7. Official artefact

The Gate produces a Version Approval Report filed under:

`knowledge/educational_validation/release_reports/`

using `RELEASE_DECISION_TEMPLATE.md`.

That report is the **official educational approval artefact** for the version.

---

## 8. Operator checklist

- [ ] Prerequisites verified  
- [ ] Layer 1 reports present for all required EC-IDs  
- [ ] Layer 2 comparative evidence mapped and cited  
- [ ] Layer 3 dimension matrices complete  
- [ ] Component scores computed and explained  
- [ ] Overall Educational Trust calculated  
- [ ] Outcome selected per §5  
- [ ] Strengths, weaknesses, risks, recommendation recorded  
- [ ] Report filed in `release_reports/`  
- [ ] Release Playbook informed of educational outcome  

---

## 9. Cross references

- `EDUCATIONAL_VALIDATION_CONSTITUTION.md`  
- `EDUCATIONAL_RELEASE_STANDARD.md`  
- `VERSION_APPROVAL_WORKFLOW.md`  
- `RELEASE_DECISION_TEMPLATE.md`  
- `knowledge/RELEASE_PLAYBOOK.md`  
- `knowledge/educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md`  
