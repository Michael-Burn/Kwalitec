# Assumption Review Process

**Programme:** P-003.4 — Product Assumption Register  
**Date:** 2026-07-26  
**Status:** Active process for maintaining the Product Assumption Register  
**Does not:** Amend Vision, PSF, P-002.1 gates, Educational Constitution, Decision Register, Risk Register, or runtime

---

## 1. Purpose

Version 1 product assumptions must remain:

1. **Discoverable** — Product Board can find what is known vs believed vs disproved without reading every programme folder.  
2. **Traceable** — every assumption cites programme + evidence + related DR/PR.  
3. **Honest** — status updates when evidence changes; Validated is not used for wishful thinking.  
4. **Stable** — Assumption IDs (`PA-NNN`) do not change meaning; Rejected/Superseded create history.

This process governs the **register**, not educational algorithms, gate definitions, decisions, or risk ratings.

---

## 2. Assumption classes

| Class | Status | Meaning | Change frequency |
|---|---|---|---|
| **Known** | Validated | Evidence-bound for claim window | Updates when methodology/board/invariant changes |
| **Believed (evidenced)** | Supported | Credible support; not outcome-validated | Updates after Tier B / structural programmes |
| **Believed (untested)** | Hypothesis | Design intent or untested causal link | Updates after Stage 1 / dedicated measurement |
| **Disproved** | Rejected | Must not drive claims | Rare; archive unless methodology changes |
| **Retired** | Superseded | Replaced by later PA/DR | On explicit supersession |

---

## 3. Lifecycle stages

```
Propose → Evidence → Register → Review → (Confirm | Promote | Demote | Reject | Supersede)
```

### 3.1 Propose

A candidate assumption may arise from:

- Completion reports / SIAs stating “assumes …”  
- Validation unsupported-claims logs  
- Decision Register Risks / Rationale fields  
- Risk Register exposures that rest on unstated beliefs  
- Blind-review hypotheses (SV personas)  
- Release dossier claim language  

**Required before registration:**

- Title + category + draft statement  
- Origin programme / doc path  
- At least one supporting **or** contradicting evidence path  
- Draft status with justification  
- Related DR/PR if known  

**Forbidden:** Inventing market assumptions without repository evidence; renaming Rejected claims as Supported without new evidence; treating estimated ΔKSI as validation.

### 3.2 Evidence

Minimum evidence by status:

| Target status | Minimum evidence |
|---|---|
| Hypothesis | Design doc or SIA statement + explicit “untested” |
| Supported | Tier B pack, Universal/Near-Universal blind theme, or structural implementation + residual gap stated |
| Validated | Gate/invariant law **or** Universal root-cause + remediation accepted **or** methodology certified for claim class |
| Rejected | Explicit unsupported/falsified log, methodology ban, or constitutional prohibition |
| Superseded | Newer PA/DR that replaces the statement |

If evidence is missing → **do not** create `PA-NNN` as Supported or Validated.

### 3.3 Register

1. Allocate next free `PA-NNN` (never reuse IDs).  
2. Add full card to `PRODUCT_ASSUMPTION_REGISTER.md`.  
3. Add row to the appropriate status index.  
4. Add rows to `ASSUMPTION_TRACEABILITY.md` (decisions, risks, programmes).  
5. Do **not** amend Decision or Risk register bodies from this process alone (cross-link only).

P-003.4 packages existing assumptions; future programmes that change evidence should update this register in the same change set (docs-only OK).

### 3.4 Review

| Cadence | What to review |
|---|---|
| Every board declaration / Go-No-Go | PA-021, PA-025, PA-026, PA-027, PA-039 |
| Every educational flag ON proposal | PA-011, PA-012, PA-033, PA-030 |
| Every Stage 1 ops milestone | PA-014, PA-026, PA-039, PA-017 |
| Every validated KSI board publish | PA-021, PA-023, PA-036 |
| Every Tier B perception pack | PA-001, PA-007, PA-017, PA-025 (must stay Rejected) |
| Quarterly hygiene | Superseded accuracy; orphan PAs without evidence |

### 3.5 Confirm / Promote / Demote / Reject / Supersede

| Action | When | How |
|---|---|---|
| **Confirm** | Evidence unchanged | Note in board minutes; no card churn required |
| **Promote** | Hypothesis→Supported or Supported→Validated with evidence | Edit Status + Confidence + Evidence fields; move indexes |
| **Demote** | Regression or overclaim discovered | Lower status; cite new contradicting evidence |
| **Reject** | Falsified / unsupported as claim | Status Rejected; add to Rejected index |
| **Supersede** | Replaced by clearer statement | Status Superseded; point to new PA/DR; keep history |

---

## 4. Confidence rules

1. Confidence rates the **status claim**, not student success.  
2. Prefer-lower when uncertain (aligns with DR-027).  
3. External N = 0 caps behavioural outcome claims at Hypothesis (or Supported perception only).  
4. Law/invariant Validated cards may be High confidence while related outcome PAs remain Hypothesis.  
5. Never promote to Validated because a risk is uncomfortable or a deadline approaches.

---

## 5. Relationship to other registers

| Artefact | Role vs this register |
|---|---|
| P-003.2 Decision Register | Decisions encode *choices*; assumptions encode *beliefs underlying choices* |
| P-003.3 Risk Register | Risks encode *what could go wrong if assumptions fail or remain open* |
| P-002.1 Release Framework | Defines gates; this register tracks epistemic status of claims feeding gates |
| P-003.1 Release Dossier | Synthesis; does not replace assumption cards |
| Validation / Go-No-Go reports | Primary evidence sources for status changes |

**Authority:** This register does **not** outrank P-002.1 gates, Educational Constitution, Decision Register, or Risk Register. It indexes epistemic status under existing law.

---

## 6. Ownership

| Role | Responsibility |
|---|---|
| Product Board | Validated/Rejected discipline at declaration reviews |
| Product | Hypothesis portfolio; Stage 1 validation triggers |
| Validation owner | Tier B / KSI board updates affecting PA status |
| Engineering / Architecture | Invariant assumptions (determinism, Runtime A, flags, curriculum) |

---

## 7. Anti-patterns

- Promoting PA-039 because MES/journey Tier B Passed  
- Closing PA-021’s *bar* because someone wishes KSI were 80 (score ≠ bar)  
- Inventing assumptions to fill category quotas  
- Treating Supported as Validated in marketing  
- Creating parallel assumption ID schemes in dossiers  
- Amending DR/PR cards “to match” without evidence programmes  

---

## 8. Exit test for this process

A Product Board member can determine:

1. what is known ([`VALIDATED_ASSUMPTIONS.md`](VALIDATED_ASSUMPTIONS.md)),  
2. what is believed ([`UNVALIDATED_ASSUMPTIONS.md`](UNVALIDATED_ASSUMPTIONS.md)),  
3. what has been disproved ([`REJECTED_ASSUMPTIONS.md`](REJECTED_ASSUMPTIONS.md)),  
4. what still requires evidence (Hypothesis Validation Triggers + Supported gaps).

---

**End of Assumption Review Process**
