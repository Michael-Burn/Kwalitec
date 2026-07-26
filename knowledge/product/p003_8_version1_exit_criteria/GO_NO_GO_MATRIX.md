# GO / NO GO Matrix

**Programme:** P-003.8 — Version 1 Exit Criteria  
**Version:** 1.0  
**Status:** Active — synthesis of existing Board definitions  
**Effective:** 2026-07-26  
**Sources (unchanged law):**

- `../p002_1_version_1_release_framework/VERSION_1_GO_NO_GO_GUIDE.md`
- `../p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md` §5.5
- `../p003_7_product_board_charter/RELEASE_DECISION_PROCESS.md` §4
- `../p003_7_product_board_charter/PRODUCT_BOARD_CHARTER.md` §7

**Does not:** Invent new outcomes or soften hard-gate FAIL rules.

---

## Naming note

| This pack | P-002.1 wording | Meaning |
|---|---|---|
| **GO** | GO | Unconditional production-ready for claim window |
| **CONDITIONAL GO** | **GO WITH CONDITIONS** | Production-ready only under named HOLDs / claim restrictions |
| **NO GO** | NO-GO | Declaration forbidden |
| **DEFER** | DEFER | Incomplete evidence or Low KSI confidence; no new claim |

Charter / dossier use **CONDITIONAL GO**; P-002.1 uses **GO WITH CONDITIONS**. Treat as the **same outcome class**.

---

## Matrix

| Outcome | When (existing rules only) | Allowed claim language | Forbidden | Typical next action |
|---|---|---|---|---|
| **GO** | All hard gates G1–G12 **PASS**; no material HOLDs (or holds explicitly cleared for claim class); EVF not REJECTED; Evidence Package complete; Board signs XC-REC | “Kwalitec Version 1 is production-ready” for the declared cohort / claim window (with scope if limited); validated KSI stated as usefulness, not pass-rate proof | Pass-rate proof without methodology; dual educational truths; marketing OFF flags as live | Update readiness tracker; retain package; permit approved claims |
| **CONDITIONAL GO** | No hard-gate **FAIL**; educational honesty + G1 + G2.1–G2.5 + G10 criticals PASS; remaining residuals are **HOLD**s with **named claim restrictions**; Board + owning authority + Release operator acknowledge | Must list holds; must not claim unconditional V1 readiness | Claiming unconditional readiness; waiving honesty / dual-truth / Never-Build via HOLD | Track HOLD expiry; auto-downgrade to NO GO if HOLD expires unmet |
| **NO GO** | Any hard-gate **FAIL**; EVF REJECTED; unresolved honesty P1; validated KSI &lt; 80; K8 &lt; 70; any category &lt; 50; or Board refuses optimism override | Forbid V1 production-ready claims; may continue private-beta / gated work under **other** decisions (e.g. DR-040) | “Version 1 launched / production-ready”; effectiveness claims while G1.9 NO-GO; Exam Ready without gates | Publish blockers; remediate by gate / expected evidence; re-board when package ready |
| **DEFER** | Evidence package incomplete **or** KSI confidence **Low**, without treating silence as GO; FAIL not yet proven on every hard gate | No new claim | Treating DEFER as soft GO | List missing artefacts; complete package; re-board |

---

## Hard rules (non-negotiable — from P-002.1 §3)

1. Any hard-gate FAIL → **NO GO**.  
2. Validated KSI &lt; 80 → **NO GO**.  
3. Any category &lt; 50 → **NO GO**.  
4. K8 &lt; 70 → **NO GO**.  
5. EVF REJECTED → **NO GO**.  
6. Unresolved educational honesty incident → **NO GO**.  
7. Security critical open without Security HOLD acceptance → **NO GO**.  
8. Vision Final Test Fail for the claim set → **NO GO**.  
9. HOLDs never waive educational honesty, dual-truth bans, or Never-Build violations.  
10. If guidance conflicts with Vision 2030 → **STOP**; amend Product Constitution first.

---

## Gate-pattern map (P-002.1 §4)

| Gate pattern | Outcome |
|---|---|
| All G1–G12 PASS; EVF APPROVED (or CONDITIONAL holds cleared) | **GO** |
| Educational honesty + G1 + G2.1–G2.5 + G10 criticals PASS; only operational HOLDs (e.g. G7/G8/G9) with claim restrictions | **CONDITIONAL GO** |
| Any FAIL on G1–G6, G10, G11 hard criteria, or G12 claim/flag honesty | **NO GO** |
| Evidence package incomplete; KSI confidence Low; sign-offs missing | **DEFER** |

---

## Separable verdicts (DR-032) — do not collapse

| Verdict | Current (2026-07-26) | Clears Version 1 GO? |
|---|---|---|
| Programme / milestone complete | Many EP/P complete | **No** |
| Private-beta execution | **GO WITH CONDITIONS** (DR-040) | **No** |
| Educational effectiveness | **NO-GO / PENDING EVIDENCE** | Blocks G1.9 |
| Version 1 production-ready | **NO GO** (DR-041) | This matrix’s subject |

---

## Current application

| Field | Value |
|---|---|
| Outcome today | **NO GO** |
| Binding pattern | Hard-gate FAIL on G1 (G1.1, G1.9) + incomplete package |
| Could today be DEFER instead? | **No** — FAIL already proven on G1; DEFER is for incomplete evidence *without* hard FAIL |
| Could today be CONDITIONAL GO? | **No** — CONDITIONAL GO requires no hard-gate FAIL |

---

**End of GO_NO_GO_MATRIX**
