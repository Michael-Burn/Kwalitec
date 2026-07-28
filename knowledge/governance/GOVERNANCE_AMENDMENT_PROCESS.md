# Governance Amendment Process

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.4 — Educational Governance Constitution  
**Version:** 1.0  
**Status:** Active — Board amendment procedure for educational governance  
**Effective:** 2026-07-28  
**Authority:** Subordinate to `EDUCATIONAL_GOVERNANCE_CONSTITUTION.md`  
**Scope:** Amendments to the Educational Governance Constitution and DG-001.1–3 instruments (and their companions)

---

## 1. Purpose

Define how educational governance law changes — so features, copy programmes, and local READMEs cannot silently redefine Mission, Study Sensei, reflection, or constitutional principles.

**Implementation never amends the Constitution.  
The Constitution is amended first; then implementation follows.**

---

## 2. What this process covers

| In scope | Out of scope (use other processes) |
|----------|-------------------------------------|
| Educational Governance Constitution (DG-001.4) | Vision 2030 amendments (product philosophy process) |
| Lexicon + map + deprecation + style (DG-001.1) | EGI-001 Educational Constitution Article X |
| Authority model + transitions + matrix + conflicts (DG-001.2) | Architecture Constitution / ADRs |
| Reflection architecture + lifecycle + matrix + RG rules (DG-001.3) | EVF / P-002.1 / Release Playbook |
| Constitutional principles CP-01–CP-10 and invariants CI-* | Engineering Standards |

If a proposed change would contradict **E1 Educational Constitution** or **Vision 2030**, stop and use those documents’ amendment paths first. This process alone cannot override them.

---

## 3. Who may propose amendments

| Role / capacity | May propose? | Notes |
|-----------------|--------------|-------|
| Founder — Educational Gate Owner | Yes | Primary proposers |
| Founder — Product Owner | Yes | Especially vocabulary / authority / student impact |
| Founder — Engineering Owner | Yes | Especially reflection storage / residual consolidation |
| Product Board (Chair capacity) | Yes | May mandate amendment from certification residuals |
| Implementation programme leads (EP / ILE / RP / DG) | Yes | Via written proposal citing evidence |
| External contributors | No direct | Route through Founder capacities |

Under GP-001, capacities may be founder-held; proposals still require written records.

---

## 4. Required evidence

Every amendment proposal must include:

1. **Problem statement** — what ambiguity, conflict, or student harm exists.  
2. **Evidence** — at least one of: RP / ED residual ID, blind review, dogfood, certification finding, production defect, Board decision gap, or explicit OQ-* closure rationale.  
3. **Affected documents** — exact paths and sections.  
4. **Affected principles** — CP-01–CP-10 / CI-* / RG-* / D* decisions touched.  
5. **Proposed text** — concrete replacement or addition (not “clarify later”).  
6. **Student impact** — does student-facing meaning change? If yes, state risk to trust.  
7. **Migration / supersession plan** — what prior decisions or deprecations change.  
8. **Non-claims** — what the amendment does *not* authorise (e.g. no template rewrite in the same package if governance-only).

**Insufficient evidence:** preference, marketing convenience, or engagement metric alone.

---

## 5. Review process

```
Proposal drafted
    ↓
Educational governance review (checklist)
    ↓
Conflict check against E0–E6 hierarchy
    ↓
Founder Review record(s) — Educational (+ Product / Engineering as needed)
    ↓
Approval / Conditional / Reject / Hold
    ↓
If approved: version bump + supersession notice + Decision Log entry
    ↓
Notify dependent programmes (copy, Help, PX, Alpha residuals)
```

### 5.1 Review questions (mandatory)

| # | Question |
|---|----------|
| 1 | Does this preserve CP-06–CP-08 (trust, honesty, evidence)? |
| 2 | Does this preserve CP-10 (sole Study Sensei mentor)? |
| 3 | Does this keep one concept → one definition (CP-03)? |
| 4 | Does this keep one primary authority per interaction (CP-04)? |
| 5 | If reflection-related: does this preserve one coherent system (CP-05) and Journal memory singularity (CI-02)? |
| 6 | Does this invent a peer apex or bypass EGI-001? |
| 7 | Are outstanding OQ-* items closed, deferred with rationale, or newly created? |

### 5.2 Reviewers

| Amendment type | Minimum review capacities |
|----------------|---------------------------|
| Constitutional principles / hierarchy | Educational Gate Owner + Product Owner (Board Chair informed) |
| Lexicon / deprecation | Educational Gate Owner |
| Authority model | Educational Gate Owner + Product Owner |
| Reflection architecture / RG rules | Educational Gate Owner + Engineering Owner (storage implications) |
| Compliance checklist only | Educational Gate Owner |

---

## 6. Approval process

| Decision | Meaning | Next step |
|----------|---------|-----------|
| **Approve** | Law changes | Publish version; update Decision Log; supersede prior text |
| **Conditional Approve** | Law changes with named residual | Publish; residual must appear in completion report / OQ register |
| **Reject** | No change | Record rationale; proposer may revise |
| **Hold** | Evidence insufficient | Do not treat draft as law |

**Approval authority:** Founder — Educational Gate Owner capacity for DG-001 instruments; Product Board Chair capacity when the amendment affects certification claims or constitutional principles CP-01–CP-10.

Material approvals use **Founder Review** records: Reviewer · Date · Decision · Notes (per GP-001).

---

## 7. Versioning

| Document class | Versioning rule |
|----------------|-----------------|
| Educational Governance Constitution | Semantic: MAJOR = principle/hierarchy change; MINOR = clarification; PATCH = typo/link |
| DG-001.1–3 primary instruments | Same semantic scheme |
| Companions (maps, matrices, registers) | May share parent package version or date stamp; must cite parent version |
| Completion reports | Immutable once committed; corrections via addendum report |

**Header requirements after amendment:**

- Version number  
- Status (Active / Superseded)  
- Effective date  
- Amended date + short change summary  
- Pointer to prior version or git commit when practical  

---

## 8. Supersession rules

1. **Explicit supersession** — the amending document must name what it replaces (section, decision ID, or prior version).  
2. **No silent overwrite** — deprecated terms/decisions move to a register (e.g. Term Deprecation Register) or Decision Log with status *Superseded*.  
3. **Downstream notice** — programmes citing the old text must update citations in their next touching change; they must not keep shipping against superseded law.  
4. **Evidence trail** — RP / Alpha residual IDs that motivated the amendment remain cited.  
5. **Code does not supersede law** — if production behaviour differs from law, that is a **defect or residual**, not an amendment.  
6. **Higher law first** — if EGI-001 or Vision must change, complete that amendment before claiming DG-001 alignment to the new meaning.

---

## 9. Emergency / interim guidance

If a live defect harms student trust (false mastery claim, dual mentor, Check-in presented as Sensei memory):

1. **Contain** via existing operational means (flag, copy hotfix under Engineering/Operations) if needed for safety.  
2. **Do not** treat the hotfix as constitutional amendment.  
3. Open a formal amendment or remediation programme within a defined Board window.  
4. Record the interim exception with expiry in the compliance statement.

---

## 10. Proposal template (minimum)

```markdown
# Educational Governance Amendment Proposal

**ID:** DG-001-AMD-XXX
**Date:**
**Proposer capacity:**
**Target document(s):**
**Type:** MAJOR / MINOR / PATCH

## Problem
## Evidence
## Affected principles / decisions
## Proposed change (exact text)
## Student impact
## Supersession plan
## Non-claims
## Review outcome (filled after review)
```

---

## 11. Relationship to other change control

| Process | Interaction |
|---------|-------------|
| P-003.7 Product Board / Change Control | Board may mandate DG-001 amendments; this process executes educational governance text change |
| GP-001 Founder Reviews | Approval recording mechanism |
| EGI-003 Educational Governance Review | Still required for educational *implementation* meaning; amendment of DG-001 law uses *this* process |
| Git commit | Documentation commit is publication; commit message is not approval |

---

**End of GOVERNANCE_AMENDMENT_PROCESS**
