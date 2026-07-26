# Board Release Checklist

**Programme:** P-003.8 — Version 1 Exit Criteria  
**Version:** 1.0  
**Status:** Active — meeting aid (synthesis only)  
**Effective:** 2026-07-26  
**Use in:** Product Board Release review  
**Does not:** Replace P-002.1 Acceptance Checklist or invent new gates  

**Authorities restated:**

- P-002.1 `VERSION_1_ACCEPTANCE_CHECKLIST.md` / `VERSION_1_GO_NO_GO_GUIDE.md` §9  
- P-003.7 `RELEASE_DECISION_PROCESS.md` §10  
- P-003.1 dossier recommendation banner  

---

## Pre-meeting (Chair / Product Governance Lead)

- [ ] Claim window and candidate version / tag frozen  
- [ ] Audience confirmed (Board-only vs C-V1 / public claim class) — P-003.5 Claim Decision Tree  
- [ ] Evidence package index linked (XC-PKG) — P-002.1 §5.2  
- [ ] Dossier / Exit Criteria current assessment reviewed (`CURRENT_RELEASE_POSITION.md`)  
- [ ] Quorum / capacity Founder Reviews available (Charter + P-002.1 §5.3 + GP-001)  

---

## Hard educational / usefulness blockers (any FAIL → stop; vote NO GO)

- [ ] **XC-G1 / G1.1** — Validated KSI ≥ 80 (not estimates) — DR-025, DR-026, DR-051  
- [ ] **XC-G1 / G1.2** — Confidence High or Medium  
- [ ] **XC-G1 / G1.3** — Assessment ≤ 90 days  
- [ ] **XC-G1 / G1.4** — No category &lt; 50  
- [ ] **XC-G1 / G1.5** — K8 ≥ 70 — DR-042  
- [ ] **XC-G1 / G1.7** — Independent re-score ±3 filed or dispute resolved — PR-009  
- [ ] **XC-G1 / G1.9** — Educational effectiveness **not** NO-GO for claim window — DR-022, DR-033; EP-007.3  
- [ ] **XC-G1 / G1.10** — No unresolved educational honesty P1  
- [ ] **XC-G2 / G2.4** — EVF outcome APPROVED or CONDITIONAL holds cleared — PR-020  
- [ ] **XC-G2** — Final Test / Never-Build / one-runtime / curriculum V1–V2 / SIA / ADR — G2.1–G2.8  

---

## Quality contracts (G3–G6)

- [ ] **XC-G3** — Explainability pack + G3.4 spot-check — P-001.2  
- [ ] **XC-G4** — Recommendation checklist / scorecard; freeze honesty — P-001.3, DR-036  
- [ ] **XC-G5** — Planning tests + duration smoke pack — EP-003.3 / EP-007.1  
- [ ] **XC-G6** — Readiness tests + honesty path; Exam Ready still gated — DR-035  

---

## Operational / security / flags (G7–G12)

- [ ] **XC-G7** — Perf PASS or HOLD with forbidden high-traffic claims — PR-010  
- [ ] **XC-G8** — Reliability pack (health, smoke, rollback, backup ack) — PR-013  
- [ ] **XC-G9** — Telemetry claim/flag alignment — DR-047, PR-011  
- [ ] **XC-G10** — Security / privacy for claim class — PR-003, PR-023  
- [ ] **XC-G11** — Green release-candidate CI  
- [ ] **XC-G12** — Published flag matrix; OFF flags not marketed — DR-043, PR-012, PR-016  

---

## Registers and claim honesty

- [ ] Material Red risks Accepted or Closed with proof — P-003.3 (esp. PR-001, PR-002, PR-004, PR-019)  
- [ ] No Rejected assumptions underpinning the GO narrative — P-003.4  
- [ ] Claim freezes respected unless Evidence Hierarchy permits lift — DR-021, DR-035, DR-036; P-003.5  
- [ ] Separable verdicts stated aloud: programme GO ≠ effectiveness GO ≠ Version 1 GO — DR-032  
- [ ] Private-beta posture (DR-040) not treated as Version 1 GO  

---

## Recommendation and recording (XC-REC)

- [ ] Draft outcome: **GO** / **CONDITIONAL GO** / **NO GO** / **DEFER** — per [`GO_NO_GO_MATRIX.md`](GO_NO_GO_MATRIX.md)  
- [ ] If CONDITIONAL GO: HOLD list with gate ID, residual, forbidden claims, owner, re-review date  
- [ ] Proposed claim language read aloud; apply Vision Final Test  
- [ ] Founder Reviews captured per capacity (Product Owner, Educational Gate Owner, Engineering Owner / architecture lens, Privacy Owner / security lens, Evidence Lead, Product Board Chair; Operations Owner release ack) — GP-001 `UPDATED_APPROVAL_MATRIX.md`  
- [ ] Record filed; `VERSION_1_READINESS.md` aligned same day  
- [ ] Decision Lifecycle posture updated only if recommendation **class** changes (do not silently mutate DR IDs)  

---

## Freeze-date reminder (2026-07-26)

| Check | Expected today |
|---|---|
| Overall | **NO GO** |
| Why | XC-G1 FAIL (G1.1, G1.9); XC-PKG incomplete; XC-REC remains NO GO |
| Allowed | Stage 0 private beta under DR-040; remediation; claim freezes |
| Forbidden | “Version 1 production-ready”; public launch; effectiveness / pass-rate claims from current evidence |

**Any unchecked hard item → do not vote GO.**

---

**End of BOARD_RELEASE_CHECKLIST**
