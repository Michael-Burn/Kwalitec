# Release Decision Process

**Programme:** P-003.7 — Product Board Charter  
**Version:** 1.0  
**Status:** Active — Board procedure  
**Effective:** 2026-07-26  
**Companion:** [`PRODUCT_BOARD_CHARTER.md`](PRODUCT_BOARD_CHARTER.md)  
**Gate law (unchanged):** `../p002_1_version_1_release_framework/`  
**Dossier (unchanged):** `../p003_1_version1_release_dossier/`  
**Does not:** Amend G1–G12 criteria; flip DR-041; declare Version 1  

---

## 1. Purpose

Define how the Product Board forms a **Version 1 production-ready** recommendation:

> GO · CONDITIONAL GO · NO GO · DEFER

### Binding rule

> **Only the Product Board may recommend GO or NO GO** on Version 1 production-ready declaration.

Engineering gate packs, EVF outcomes, and operational deploys are **inputs**. They are not substitutes for a Board recommendation.

---

## 2. Inputs (required package)

Before a Release review that might change recommendation class, assemble:

| # | Input | Source |
|---|---|---|
| 1 | Gate scores G1–G12 (PASS / FAIL / HOLD / …) | P-002.1 scoring + dossier `Release_Gates.md` |
| 2 | Evidence package index with immutable paths | P-002.1 Evidence Requirements |
| 3 | Validated KSI board (not estimates) | EP-005.* / EP-006.* / EP-007.* chain |
| 4 | Educational effectiveness / G1.9 posture | EP-007.3 (or successor) |
| 5 | EVF educational outcome for claim class | Educational Validation Framework |
| 6 | Decision Register posture (esp. freezes, flags) | P-003.2 |
| 7 | Active material risks | P-003.3 |
| 8 | Material unvalidated / rejected assumptions | P-003.4 |
| 9 | Claim freezes / Evidence Hierarchy posture | P-003.5 |
| 10 | Release Dossier synthesis | P-003.1 |
| 11 | Maturity heatmap (context only; not a gate) | P-003.6 |

Incomplete hard-gate evidence → overall package **incomplete** → recommendation at best **DEFER** (or **NO GO** if hard-gate FAIL already proven).

---

## 3. Decision sequence

Aligns with P-002.1 §5; Board owns steps 5–7 interpretation and recommendation.

```
1. Confirm claim window and audience (C-V1 / public vs Board-only)
2. Verify evidence package completeness
3. Score / confirm G1–G12
4. Confirm EVF outcome (feeds G2.4)
5. Product Governance Lead drafts recommendation
6. Sign-off Board (roles per P-002.1 §5.3 + this Charter quorum)
7. Record recommendation + update readiness tracker alignment
8. Only on GO: allow “Version 1 production-ready” claim language (still subject to C-COM tree)
```

---

## 4. Outcome rules (summary)

| Outcome | When |
|---|---|
| **GO** | All hard gates PASS; HOLDs absent or explicitly cleared for claim class; EVF not REJECTED; signed Board record; evidence package complete |
| **CONDITIONAL GO** | No hard-gate FAIL; one or more HOLD with **named claim restrictions**; Board signs conditions |
| **NO GO** | Any hard-gate FAIL; EVF REJECTED; unresolved honesty P1; validated KSI &lt; 80; K8 &lt; 70; any category &lt; 50; or Board refuses optimism override |
| **DEFER** | Evidence package incomplete or KSI confidence Low without FAIL yet proven |

Full criteria: `VERSION_1_GO_NO_GO_GUIDE.md` under P-002.1.

**Hard rule:** Any hard-gate FAIL → overall **NO-GO**. Opinion cannot override.

---

## 5. Interaction with registers and hierarchy

| Artefact | Role in release decision |
|---|---|
| **Release Gates (P-002.1)** | Law — what must PASS |
| **Evidence Hierarchy (P-003.5)** | What claims the package may support; C-V1 / C-REC / C-COM |
| **Decision Register (P-003.2)** | Standing freezes and posture (e.g. DR-041) |
| **Risk Register (P-003.3)** | Whether residual risks are Accepted / Controlled under operating mode |
| **Assumption Register (P-003.4)** | Whether declaration rests on Rejected or Hypothesis assumptions (blocker honesty) |
| **Exit criteria / readiness tracker** | `VERSION_1_READINESS.md` must not contradict signed recommendation |
| **Dossier (P-003.1)** | Board-readable synthesis — does not amend gates |

---

## 6. Who signs what

| Role | Signs / affirms |
|---|---|
| **Product Governance Lead** | G1 honesty, claim language, drafted overall recommendation |
| **Educational Representative** | G2.3–G2.4, G3–G4 educational honesty; EVF interpretation |
| **Architecture Representative** | G2.5–G2.6, G2.8 |
| **Engineering Representative** | G5–G9, G11–G12 technical packs |
| **Security Representative** | G10 |
| **Evidence Lead** | Classification of package evidence; freshness |
| **Chair** | Quorum; publication of Board recommendation record |
| **Release Operator** | Deploy fingerprint / smoke / rollback readiness — **advisor**; does not alone declare Version 1 |

Detail: [`BOARD_ROLES_AND_RESPONSIBILITIES.md`](BOARD_ROLES_AND_RESPONSIBILITIES.md) and P-002.1 §5.3.

---

## 7. Recording the recommendation

Minimum fields in the Go / No-Go record:

| Field | Example |
|---|---|
| Date | 2026-07-26 |
| Claim window | W-PROD |
| Recommendation | NO GO |
| Blocking gates | G1.1, G1.9; package incomplete; G1.7 HOLD |
| Evidence index path | … |
| Signatures (roles) | … |
| Linked DR posture | DR-041 |
| Next review trigger | New validated KSI ≥ 80 **and** effectiveness not NO-GO **and** complete package |

After record:

1. Align `VERSION_1_READINESS.md` statuses to evidence (do not invent PASS).  
2. Update Decision Lifecycle posture if recommendation class changes.  
3. Refresh dossier Executive Summary / recommendation banner when synthesis programme runs.

---

## 8. Separable verdicts (mandatory reminder)

| Verdict | Meaning |
|---|---|
| Programme / milestone GO | Workstream complete for its scope |
| Educational effectiveness GO | Outcome evidence supports learning-benefit claims |
| Version 1 production-ready GO | Full P-002.1 Board recommendation |

Confusing these is a **process failure**. Current Version 1 dossier recommendation remains **NO GO** as of 2026-07-26.

---

## 9. Private beta vs production-ready

| Mode | Board stance |
|---|---|
| Invite-only / Stage 0 private beta under EP-004 conditions | May continue under controls; **does not** clear C-V1 |
| Operational GA / deploy success | Necessary at most; **insufficient** for Version 1 declaration |
| Public “Version 1 ready” marketing | Requires GO record + Claim Decision Tree Steps D–E |

---

## 10. Exit criteria checklist (Board-facing)

Use as a pre-meeting gate (not a replacement for P-002.1 checklists):

- [ ] Evidence package index linked for every hard gate  
- [ ] Validated KSI ≥ 80 with Medium/High confidence and freshness  
- [ ] G1.9 effectiveness not NO-GO  
- [ ] G1.7 independent re-score filed or dispute resolved  
- [ ] EVF outcome acceptable for claim class  
- [ ] No open educational honesty P1  
- [ ] Flag matrix / G12 honest for student-visible authority  
- [ ] Material Red risks Accepted or Closed with proof  
- [ ] No Rejected assumptions underpinning the GO narrative  
- [ ] Quorum roles present  
- [ ] Draft recommendation and claim language reviewed  

Any unchecked hard item → do not vote GO.

---

## 11. Success check

A new Board member can explain, from this document alone:

- who may recommend GO / NO GO,  
- what package is required,  
- why hard-gate FAIL forces NO GO,  
- how dossier / registers / hierarchy interact,  
- why private beta ≠ production-ready —

and correctly restate the current **NO GO** posture without reading application code.

---

**End of Release Decision Process**
