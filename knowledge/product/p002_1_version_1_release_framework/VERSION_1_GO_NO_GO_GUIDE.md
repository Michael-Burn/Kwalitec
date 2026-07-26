# Version 1 Go / No-Go Guide

**Programme:** P-002.1 — Version 1 Release Framework  
**Version:** 1.0  
**Status:** Active — decision guide for Version 1 production-ready declaration  
**Effective:** 2026-07-26  
**Companion:** [`VERSION_1_RELEASE_FRAMEWORK.md`](VERSION_1_RELEASE_FRAMEWORK.md)  
**Does not:** Change runtime behaviour, Twin algorithms, UI, or APIs  

---

## 1. Purpose

Define **how** Product and peer authorities turn gate results into a Version 1 declaration decision — including holds, claim language, and revocation.

This guide complements (does not replace):

- EVF Educational Release Gate outcomes  
- EP-003 / EP-004 cohort Go / No-Go decisions  
- Release Playbook deploy/rollback execution  

---

## 2. Decision outcomes

| Outcome | Meaning | Allowed claim language |
|---|---|---|
| **GO** | Version 1 is production-ready for the claim window | “Kwalitec Version 1 is production-ready” (with cohort/scope if limited) |
| **GO WITH CONDITIONS** | Production-ready only under stated holds | Must list holds; must not claim unconditional V1 readiness |
| **NO-GO** | Version 1 may not be declared | Forbid V1 production-ready claims; may continue private-beta / gated work under other decisions |
| **DEFER** | Evidence incomplete or KSI confidence Low | No new claim; complete package and re-board |

---

## 3. Hard rules (non-negotiable)

1. **Any hard-gate FAIL → NO-GO.**  
2. **Validated KSI < 80 → NO-GO** (estimated programme ΔKSI boards are insufficient).  
3. **Any category < 50 → NO-GO.**  
4. **K8 < 70 → NO-GO.**  
5. **EVF REJECTED → NO-GO.**  
6. **Unresolved educational honesty incident → NO-GO.**  
7. **Security critical open without Security HOLD acceptance → NO-GO.**  
8. **Vision Final Test Fail for the claim set → NO-GO.**  
9. **HOLDs never waive educational honesty, dual-truth bans, or Never-Build violations.**  
10. **If this guide conflicts with Vision 2030 → STOP;** amend Product Constitution first.

---

## 4. Mapping gate results → outcome

| Gate pattern | Outcome |
|---|---|
| All G1–G12 PASS; EVF APPROVED (or CONDITIONAL holds cleared) | **GO** |
| All educational honesty + G1 + G2.1–G2.5 + G10 criticals PASS; only G7/G8/G9 (and similar operational) HOLDs remain with claim restrictions | **GO WITH CONDITIONS** |
| Any FAIL on G1–G6, G10, G11 hard criteria, or G12 claim/flag honesty | **NO-GO** |
| Evidence package incomplete; KSI confidence Low; sign-offs missing | **DEFER** |

**GO WITH CONDITIONS** requires:

- Written HOLD list (gate ID, residual, owner, expiry or re-review date)  
- Explicit **forbidden claims** (e.g. “no high-traffic marketing until G7.2 production load sample”)  
- Product + owning authority + Release operator acknowledgement  

---

## 5. Relationship to other Go / No-Go boards

| Board | Question it answers | If that board is NO-GO |
|---|---|---|
| **This guide** | May we declare Version 1 production-ready? | V1 declaration forbidden |
| **EVF Educational Release Gate** | Is educational quality trusted enough to release under educational claims? | G2.4 fails → this board NO-GO |
| **EP-003 Educational Go / No-Go** | Are effectiveness / educational review claims supported for the cohort window? | G1.9 fails if EP-003 is NO-GO for the same claim window |
| **EP-004 Private Beta Go / No-Go** | May private-beta stages proceed under stated conditions? | May be GO WITH CONDITIONS for beta while this board remains NO-GO for Version 1 declaration |

**Rule:** Private-beta **GO WITH CONDITIONS** does **not** imply Version 1 **GO**.

---

## 6. Claim language examples

### Allowed on GO

- “Version 1 is production-ready under the P-002.1 evidence package dated [date].”  
- “Validated KSI = [n] (≥ 80) for the claim window; this is educational usefulness, not exam pass-rate proof.”

### Allowed on GO WITH CONDITIONS

- “Version 1 is production-ready with holds: [list]. We do not claim [forbidden].”

### Forbidden until GO

- “Version 1 launched” / “V1 production-ready” without a filed decision record  
- “Students who use Kwalitec pass more exams” without approved pass-rate methodology  
- “Recommendations are proven effective” while EP-001 / EP-003 marketing freeze applies  
- “Exam Ready” without readiness gates

---

## 7. Decision record template

File as `VERSION_1_GO_NO_GO_DECISION.md` inside the evidence package (or link an equivalent signed record).

```markdown
# Version 1 Go / No-Go Decision

| Field | Value |
|---|---|
| Candidate version / tag | |
| Claim window | |
| Decision date | |
| Outcome | GO / GO WITH CONDITIONS / NO-GO / DEFER |
| Validated KSI | |
| EVF outcome | |
| Acceptance checklist path | |

## Gate summary

| Gate | Result | Notes |
|---|---|---|
| G1 Validated KSI | | |
| G2 Constitutional compliance | | |
| G3 Explainability coverage | | |
| G4 Recommendation Quality | | |
| G5 Planning Quality | | |
| G6 Readiness Quality | | |
| G7 Performance | | |
| G8 Reliability | | |
| G9 Production telemetry | | |
| G10 Security / data integrity | | |
| G11 Test coverage | | |
| G12 Feature-flag readiness | | |

## Holds (if any)

| Gate | Residual | Forbidden claim | Owner | Re-review date |
|---|---|---|---|---|

## Claim language approved

>

## Founder Review (sign-offs)

| Founder Review | Reviewer | Date | Capacity | Decision | Notes |
|---|---|---|---|---|---|
| Overall usefulness / claim language | | | Product Owner | | |
| EVF / educational honesty | | | Educational Gate Owner | | |
| Architecture invariants | | | Engineering Owner (architecture lens) | | |
| Engineering verification packs | | | Engineering Owner | | |
| Security / data integrity | | | Privacy Owner (security lens) | | |
| Deploy / smoke / rollback ack | | | Operations Owner (release lens) | | |
| Board recommendation record | | | Product Board Chair | | |
```

**GP-001 note:** Sign-offs are capacity Founder Reviews (same person may hold multiple capacities). Evidence requirements are unchanged. Authority: `../gp001_founder_governance_model/UPDATED_APPROVAL_MATRIX.md`.

---

## 8. Post-decision obligations

| Outcome | Required actions |
|---|---|
| GO | Update `knowledge/VERSION_1_READINESS.md`; retain evidence package; permit approved claim language |
| GO WITH CONDITIONS | Same as GO **plus** track HOLD expiry; auto-downgrade to NO-GO if HOLD expires unmet |
| NO-GO | Publish blockers; forbid V1 claim language; open remediation programmes by expected ΔKSI / gate |
| DEFER | List missing artefacts; do not treat silence as GO |

### Revocation

Automatic claim freeze → treat as **NO-GO** until re-boarded when:

- Sev-1 educational honesty or security incident  
- Validated KSI re-score drops below 80 or breaches G1.4 / G1.5  
- Production flag matrix silently diverges from the declared G12 matrix  
- EVF outcome withdrawn / REJECTED for the claim class  

---

## 9. Board meeting checklist (lightweight)

1. Confirm claim window and candidate tag.  
2. Walk Acceptance Checklist gate results (do not re-argue closed PASS without new evidence).  
3. Confirm EVF outcome and EP-003/EP-004 status for the window.  
4. Read proposed claim language aloud; apply Final Test.  
5. Record outcome; update readiness tracker the same day.  

---

**End of VERSION_1_GO_NO_GO_GUIDE**
