# Technical Debt Governance

**Programme:** OA-001 — Operational Architecture & Product Lifecycle Framework  
**Version:** 1.0  
**Status:** Active  
**Effective:** 2026-07-28  
**Authority:** Product Constitution PC-05 · PC-08 · `docs/TECHNICAL_DEBT_REGISTER.md`  
**Constraint:** Governance only — does not invent or close debt entries by itself.

---

## 1. Purpose

Technical debt is an **intentional engineering compromise**. This standard defines how debt is recorded, owned, prioritised, reviewed, and retired so it cannot hide in institutional memory.

**Laws:**

- **PC-08** — Technical debt must have an explicit owner or remediation plan.
- **PC-05** — One authoritative source: `docs/TECHNICAL_DEBT_REGISTER.md`.

Defects (unintended incorrect behaviour) are tracked separately (issues / incident / fix programmes). Do not launder defects as “debt” to avoid fixing correctness.

---

## 2. Authoritative register

| Field | Value |
|-------|-------|
| **Canonical register** | `docs/TECHNICAL_DEBT_REGISTER.md` |
| **Owner capacity** | Founder — Engineering Owner |
| **Secondary citations** | Programme completion reports, ER non-compliance registers, Contained inventories |

Secondary documents may **reference** debt IDs. They must not maintain a conflicting parallel “real” list. When ER / RR programmes catalogue residuals, either:

1. Add/update a TD entry in the canonical register, or  
2. Explicitly mark the residual as **Accepted Contained / claim-class HOLD** with a cross-link and review date — still requiring an owner.

---

## 3. Required fields per debt item

Every active item must include:

| Field | Requirement |
|-------|-------------|
| **ID** | Stable `TD-NNN` (never reuse) |
| **Priority** | Critical · High · Medium · Low (register definitions) |
| **Category** | e.g. Framework · Architecture · Dual-stack · Security · Test · Docs |
| **Description** | What the compromise is |
| **Impact** | Engineering / student / claim-class effect |
| **Justification** | Why accepted now |
| **Owner** | Named capacity (default Engineering Owner; may be Product/Ops) |
| **Remediation plan** | Concrete next action **or** explicit Accepted Residual with conditions |
| **Target** | Epic / programme / release window, or `Accepted — review by YYYY-MM-DD` |
| **Status** | Open · In progress · Accepted residual · Closed |

**Forbidden:** Entries with neither owner nor remediation plan; “TBD forever”; priority Critical without a target before expansion claims.

---

## 4. Lifecycle

```
Identify → Record → Accept (with owner) → Schedule / Hold → Remediate → Verify → Close
```

1. **Identify** — during design, PR review, audit (ER), or Epic close.  
2. **Record** — add TD entry before merging intentional compromise when feasible; otherwise within the same programme’s completion window.  
3. **Accept** — Engineering Owner acknowledges; Product consulted if claim language or student impact.  
4. **Schedule / Hold** — link to programme or mark Accepted Residual with review date.  
5. **Remediate** — dedicated chore/fix/feature programme; prefer root cause.  
6. **Verify** — tests / architecture checks / audit evidence.  
7. **Close** — mark Closed with date and verifying artefact; retain history in register.

---

## 5. Priority and claim-class coupling

| Priority | Operating rule |
|----------|----------------|
| **Critical** | Blocks major production expansion / higher claim class until remediated or formally HOLD-documented with forbidden claims listed |
| **High** | Must appear on Programme Dashboard; target within next 1–2 Epics |
| **Medium** | Review every Epic; may slip with rationale |
| **Low** | Opportunistic; still owned |

Engineering Conditional GO (ER-002) and Contained dual-stack residuals illustrate lawful **Accepted Residuals**: disclosed, owned, claim-restricted — not invisible.

---

## 6. Review cadence

| When | Action |
|------|--------|
| End of every Epic / material programme | Review open High/Critical items; update targets |
| Before claim-class expansion | Confirm no Critical debt contradicts the new claims |
| Quarterly board | Summarise debt trend on Programme Dashboard |
| After architecture ADR that defers work | Create TD entries for deferred consequences |

---

## 7. Relationship to risks and non-compliance

| Register | Use for |
|----------|---------|
| Technical Debt Register | Intentional engineering compromises |
| Product Risk Register (P-003.3) | Risks to Version 1 / student trust / release success |
| ER non-compliance registers | Audit findings vs gates (may spawn TD or risk entries) |

A single underlying issue may appear in more than one register **with cross-links**; ratings and owners must not contradict without explanation.

---

## 8. Closure criteria

Debt may be Closed only when:

1. Remediation merged (or scope explicitly withdrawn with Product agreement).  
2. Verification evidence cited.  
3. Related claim language updated if the debt previously constrained claims.  
4. Register status set to Closed (history retained).

---

**End of Technical Debt Governance**
