# Risk Review Process

**Programme:** P-003.3 — Product Risk Register  
**Date:** 2026-07-26  
**Status:** Active process for maintaining the Product Risk Register  
**Does not:** Amend Vision, PSF, P-002.1 gates, Educational Constitution, Decision Register law, or runtime

---

## 1. Purpose

Version 1 release risks must remain:

1. **Discoverable** — Product Board can find open risks without reading every programme folder.  
2. **Traceable** — every risk cites programme + evidence.  
3. **Honest** — ratings update when evidence changes; controls are not invented.  
4. **Stable** — Risk IDs (`PR-NNN`) do not change meaning; closure creates history in [`CLOSED_RISKS.md`](CLOSED_RISKS.md).

This process governs the **register**, not educational algorithms or gate definitions.

---

## 2. Risk classes

| Class | Meaning | Examples | Change frequency |
|---|---|---|---|
| **Blocker** | Prevents honest Version 1 declaration | PR-001, PR-002, PR-003, PR-006 | Updates when evidence programmes complete |
| **Controlled** | Open but residual held by enforced controls | PR-004, PR-011, PR-016 | Review when controls erode or flags flip |
| **Watch** | Mitigated; re-open if triggers fire | PR-018, PR-022, PR-025 | Trigger-driven |
| **Accepted** | Conscious residual under invite-only / OFF flags | PR-015, PR-026 | Revisit on public launch or flag ON |
| **Closed** | Fixed or programme-exit mitigated | CR-001…CR-005 | Re-open only on regression evidence |

---

## 3. Lifecycle stages

```
Propose → Evidence → Register → Active → Review → (Confirm | Retarget | Close | Re-open)
```

### 3.1 Propose

A candidate risk may arise from:

- Release dossier / gate status change  
- Private-beta Go/No-Go or Privacy Review update  
- Validation / KSI board update  
- Feedback register / RCA / readiness residual  
- Decision Register Risks fields becoming material  

**Required before registration:**

- Title + category  
- Description of Version 1 release impact  
- Existing evidence path(s)  
- Programme ID(s)  
- Draft Likelihood / Impact with justification  

**Forbidden:** Speculative market risks, engineering bugs without release impact, Version 2 strategy items without validation evidence, or renaming HOLD preconditions as “failures” without evidence.

### 3.2 Evidence

Minimum evidence by class:

| Class | Minimum evidence |
|---|---|
| Blocker | Gate FAIL/HOLD artefact, Go/No-Go, or validated board number |
| Controlled | Control decision (DR) + residual exposure statement |
| Watch | Mitigated RISK_ASSESSMENT or feedback Watch item + reopen trigger |
| Accepted | Explicit acceptance under operating mode (invite-only / flag OFF) |
| Closed | Fix/RCA/programme exit certification with proof |

If evidence is missing → **do not** create `PR-NNN` as ACTIVE.

### 3.3 Register

1. Allocate next free `PR-NNN` (never reuse IDs).  
2. Add full card to `PRODUCT_RISK_REGISTER.md`.  
3. Add row to `ACTIVE_RISKS.md` (or `CLOSED_RISKS.md` if already closed).  
4. Add rows to `RISK_TRACEABILITY.md` (decisions, programmes, gates).  
5. If closing, move summary to `CLOSED_RISKS.md` as `CR-NNN` and mark PR status CLOSED (or keep PR CLOSED with pointer — prefer CR for fixed incidents, PR CLOSED status for retired open cards).

P-003.3 packages existing risks; future programmes that change evidence should update this register in the same change set (docs-only OK).

### 3.4 Review

| Cadence | What to review |
|---|---|
| Every board declaration / Go-No-Go discussion | All **Red** risks + PR-004/PR-019 |
| Every educational flag ON proposal | PR-012, PR-016, PR-025, PR-026 |
| Every Stage 1 ops milestone | PR-003, PR-006, PR-007, PR-017 |
| Every validated KSI board publish | PR-002, PR-008, PR-009 |
| Quarterly hygiene | PR-021, PR-022, ACCEPTED residuals |

### 3.5 Confirm / Retarget / Close / Re-open

| Action | When | How |
|---|---|---|
| **Confirm** | Evidence unchanged | Update “Last reviewed” in board minutes; no card churn required |
| **Retarget** | Likelihood/Impact/controls change | Edit card fields; adjust Overall; update ACTIVE index |
| **Close** | Closure Criteria met with evidence | Status CLOSED; add CR entry if incident/fix; update traceability |
| **Re-open** | Regression evidence | Restore ACTIVE; cite new evidence; never silently delete history |

---

## 4. Rating rules

1. Use the matrix in [`PRODUCT_RISK_REGISTER.md`](PRODUCT_RISK_REGISTER.md).  
2. Justify Likelihood/Impact from evidence (quotes/paths), not optimism.  
3. Prefer-lower when uncertain (aligns with DR-027).  
4. Control adjustment: at most **one band** downward; document as `ACTIVE (controlled)`.  
5. Critical impact + High/Very High likelihood **cannot** be Green via controls alone.

---

## 5. Relationship to other registers

| Artefact | Role vs this register |
|---|---|
| P-003.1 Risk_Summary | Upstream synthesis; R IDs map to PR IDs |
| P-003.2 Decision Register | Controls and Related Decisions; does not replace risk ratings |
| P-002.1 Release Framework | Defines gates; this register tracks risks of failing them |
| Feedback / RCA | Sources of new risks; not automatic closures |

**Authority:** This register does **not** outrank P-002.1 gates or Educational Constitution. It indexes release risk exposure under existing law.

---

## 6. Ownership

| Role | Responsibility |
|---|---|
| Product Board | Red blockers; declaration reviews; G1.7 staffing |
| Product | KSI/effectiveness claim language; beta ops chain; experience residuals |
| Engineering | G7/G8/G10/G12 technical packaging; durability |
| Privacy / data-protection owner | Privacy Review signatures (PR-003) |

---

## 7. Anti-patterns

- Inventing risks to fill category quotas  
- Closing PR-001 because Tier B perception improved  
- Counting staff N as external cohort without documentation  
- Treating a git tag ship as PR-004 closure  
- Marketing OFF flags as live (opens PR-016)  
- Creating parallel risk ID schemes in dossiers (feeds PR-021)

---

## 8. Exit test for this process

A Product Board member can determine:

1. what risks remain (`ACTIVE_RISKS.md`),  
2. why they exist (Description + Evidence on cards),  
3. how serious they are (Overall Rating),  
4. what evidence supports them (paths),  
5. what must happen before they close (Closure Criteria).
