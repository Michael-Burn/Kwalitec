# Version Approval Workflow

**Framework ID:** EVF-040  
**Programme:** Programme V — Educational Validation Framework  
**Classification:** Operator workflow  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Effective:** July 2026  

---

## 1. Purpose

This workflow is the permanent end-to-end process for educational version approval under EVF.

It turns Layers 1–4 into an operable sequence that release operators and educational reviewers can follow for every future Kwalitec version.

---

## 2. Actors

| Role | Responsibility |
|---|---|
| **Release Operator** | Starts workflow; freezes baseline; files final report; informs Release Playbook |
| **Educational Validator** | Executes Layer 1 capability reviews and Layer 3 dimension scoring |
| **Comparative Facilitator** | Prepares sealed packs / mapping notes; preserves blindness; unblinds after filing |
| **Comparative Reviewer** | Records preference + educational reasoning under Layer 2 |
| **Educational Gate Owner** | Confirms prerequisites; computes Overall Educational Trust; issues outcome |
| **Architecture / Educational Governance** | Confirms EGI-003 prerequisite; resolves constitutional conflicts |

Blind Review executors remain governed by the Blind Review framework rule and protocol. They are **not** redefined by this workflow.

---

## 3. Workflow stages

```text
0. Intake
1. Prerequisite integrity check (EGI)
2. Baseline freeze
3. Layer 1 — Capability validation
4. Layer 2 — Blind comparative review (or mapping note)
5. Layer 3 — Dimension consolidation
6. Layer 4 — Educational Release Gate
7. File Version Approval Report
8. Release Playbook hand-off
9. Archive / re-validation triggers
```

### Stage 0 — Intake

- Identify version / candidate ID  
- List required capabilities (default EC-01–EC-06 for Version 1.0)  
- List known product changes since last educational approval  
- Open draft from `RELEASE_DECISION_TEMPLATE.md`

### Stage 1 — Prerequisite integrity check

- Confirm EGI-001 compliance for claimed educational meanings  
- Confirm EGI-003 Educational Governance Review **APPROVED** for in-scope surfaces  
- If not → **STOP** (Gate cannot APPROVE quality over unlawful education)

### Stage 2 — Baseline freeze

- Record app version / commit / review package baseline  
- Prohibit Gate-day educational copy changes except documented hotfixes that restart validation for touched capabilities  

### Stage 3 — Layer 1

- Produce or refresh capability reports in `capability_reviews/`  
- Each required EC-ID receives a trust verdict  

### Stage 4 — Layer 2

- Prefer sealed blind packs (`BLIND_COMPARATIVE_REVIEW.md`)  
- Else file Comparative Mapping Note from Blind Review corpus with conservative scoring  
- Store under `reports/` and/or `benchmark_reviews/`

### Stage 5 — Layer 3

- Ensure dimension tables exist on every required capability report  
- Compute Dimension Quality Index inputs for the Gate  

### Stage 6 — Layer 4

- Run `EDUCATIONAL_RELEASE_GATE.md` scoring  
- Select APPROVED / CONDITIONAL APPROVAL / REJECTED  
- Document holds if conditional  

### Stage 7 — File official report

- Complete Version Approval Report  
- Store under `release_reports/`  
- This file is the official educational approval artefact  

### Stage 8 — Release Playbook hand-off

- Communicate educational outcome to release operators  
- Engineering/architecture gates remain separately required  
- Educational claims freeze until APPROVED / allowed conditional claims  

### Stage 9 — Archive / re-validation

Re-validate when any of the following occur:

- Material change to a required capability’s student-visible behaviour  
- Hold expiry  
- New educational claim class (e.g. exam-mark improvement)  
- Major version boundary  

---

## 4. Decision rights

| Decision | Authority |
|---|---|
| Capability trust verdict | Educational Validator (challenged by Gate Owner if evidence thin) |
| Comparative preference filing | Comparative Reviewer |
| Unblinding | Comparative Facilitator after filings complete |
| Gate outcome | Educational Gate Owner |
| Bypass request | **None** — Constitutionally forbidden |

---

## 5. Parallelism

Allowed in parallel after Stage 2:

- Layer 1 capability reviews (different EC-IDs)  
- Benchmark artefact authoring for Layer 2  

Not allowed before Stage 1 clears:

- Publishing educational APPROVED outcomes  
- Marketing educational trust percentages  

---

## 6. Minimal path (documentation-only candidates)

If the candidate changes **no** student-visible educational behaviour:

1. Stages 0–2  
2. Reuse prior Layer 1–3 artefacts with explicit “unchanged behaviour” attestation  
3. Stage 6–8 with abbreviated report citing reuse  

If behaviour changed for even one required capability, full Layer 1 for that capability is mandatory.

---

## 7. Cross references

- `EDUCATIONAL_RELEASE_GATE.md`  
- `RELEASE_DECISION_TEMPLATE.md`  
- `REVIEWER_GUIDELINES.md`  
- `knowledge/RELEASE_PLAYBOOK.md`  
- `docs/process/RELEASE_PROTOCOL.md`  
