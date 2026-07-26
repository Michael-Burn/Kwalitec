# Claim Standard

**Programme:** P-003.5 — Evidence Hierarchy & Claim Standard  
**Version:** 1.0  
**Status:** Active — board claim law for public and release language  
**Effective:** 2026-07-26  
**Companions:** [`EVIDENCE_HIERARCHY.md`](EVIDENCE_HIERARCHY.md), [`CLAIM_DECISION_TREE.md`](CLAIM_DECISION_TREE.md)  
**Does not:** Change runtime, governance law, decisions, risks, assumptions, or release gates  

---

## 1. Purpose

Answer the Product Board question permanently:

> What claims are we allowed to make?

Every claim has a **minimum evidence level**, an **audience scope**, and an explicit **prohibition** when evidence is insufficient.

---

## 2. Claim codes

| Code | Claim family | Plain meaning |
|---|---|---|
| **C-IMP** | Implementation complete | Change is built, tested, and shipped (or gated) as described |
| **C-STR** | Structural / quality verified | Quality contracts / checklists Pass; honesty paths exist |
| **C-VAL-I** | Validated internal improvement | Post-change internal/persona validation supports a bounded lift |
| **C-VAL-E** | Validated external perception | External students corroborate perception / acceptance |
| **C-EDU** | Educational effectiveness | Product improves learning / study outcomes on defined metrics |
| **C-BEN** | Student benefit (outcome) | Students are better professionals / helped in Final Test sense with outcome evidence |
| **C-REL** | Release readiness (ops) | Deployable / reliable / secure enough for a named release class |
| **C-V1** | Version 1 production-ready | All P-002.1 hard gates PASS with evidence package; board GO |
| **C-COM** | Commercial / marketing claim | Public website, sales, press, or paid acquisition language |
| **C-REC** | Board Version 1 recommendation | Explicit Product Board recommend / do-not-recommend for V1 declaration |

---

## 3. Audience scopes

| Scope | Meaning | Default bar |
|---|---|---|
| **Internal eng** | Engineering / architecture notes | E1–E2 often enough for C-IMP / C-STR |
| **Board** | Product Board / governance | Cite level; prefer under-claim |
| **Cohort** | Private-beta participants | No overclaim vs freezes |
| **Public** | Website, social, press, sales | Requires C-COM rules (§6) |

**Rule:** Public scope never inherits Board optimism. Public requires the claim family **and** C-COM clearance.

---

## 4. Minimum evidence matrix

| Claim code | Minimum evidence | Also required | Forbidden substitutes |
|---|---|---|---|
| **C-IMP** | **E2** for the shipped surface | Flag state disclosed if gated | E1 design docs alone |
| **C-STR** | **E2** checklist/contract Pass | Defect register clear of P1 honesty items for claim | Perception packs alone |
| **C-VAL-I** | **E3** post-change pack or validated board | Prefer-lower; limitations; claim window | Pre-change corpus; estimates |
| **C-VAL-E** | **E4** external floors met | Method + N disclosed | Internal Tier B alone |
| **C-EDU** | **E5** + educational Go not NO-GO | Q1–Q5 Yes with paths; sample floors | Perception; KSI alone; GA |
| **C-BEN** | **E5** for learning-benefit claims; **E4** minimum for “students find X helpful” public phrasing | Final Test alignment; no honesty P1 | Activity vanity metrics alone |
| **C-REL** | **E2** ops pack for named class (G7–G11 class evidence) | Does **not** imply C-EDU or C-V1 | “It deployed” anecdote |
| **C-V1** | Full P-002.1 package; G1–G12 hard gates PASS | Validated KSI ≥ 80; G1.9 not NO-GO; signed go/no-go | Estimated ΔKSI; dossier alone |
| **C-COM** | Meet the underlying claim’s minimum **and** §6 freezes | Board ack for educational claims | Engineering pride; roadmap |
| **C-REC** | Board synthesis citing gates + evidence summary | Explicit GO / NO GO / DEFER | Silent assumption of GO |

---

## 5. Permitted language by evidence level

### With E1 only

| Permitted | Prohibited |
|---|---|
| “We designed / decided / assumed …” | “Students benefit …” |
| “Estimated ΔKSI for planning …” | “Validated improvement …” |
| “Framework / gate / standard defines …” | “Version 1 ready …” |
| “Architecture requires …” | “Educationally effective …” |
| Cite DR / PA / PR status | Public commercial educational claims |

### With E2 (and not higher)

| Permitted | Prohibited |
|---|---|
| C-IMP for tested surfaces | C-VAL-I / C-VAL-E / C-EDU / C-BEN outcome |
| C-STR (“quality contract Pass”) | “Students understand / trust …” as proven |
| C-REL for ops gates with pack | C-V1; Exam Ready; pass-rate lift |
| “Structural eligibility for usefulness” | Strong-band KSI claims from contracts alone |

### With E3 (plus needed E2)

| Permitted | Prohibited |
|---|---|
| C-VAL-I with disclosed Medium confidence / N | C-EDU; C-VAL-E |
| Bounded category language (“K8 70 on Tier B N=9”) | “External students confirm …” |
| Board under-claim of validated KSI | KSI ≥ 80; G1 PASS; C-V1 |
| “Perceived explainability / readiness / journey improved (internal validation)” | Recommendation-effectiveness marketing |

### With E4 (plus needed E2/E3)

| Permitted | Prohibited |
|---|---|
| C-VAL-E | C-EDU until E5 + Go |
| High confidence path on perception categories if floors + agreement rules met | Pass-rate / professional outcome claims |
| Stronger public “students report …” (still needs C-COM) | C-V1 without full gate package |

### With E5 (plus freezes clear)

| Permitted | Prohibited |
|---|---|
| C-EDU / C-BEN outcome language per scorecard | Claims beyond measured metrics |
| Lifting educational effectiveness freeze **only** if EP-001 O8 / PRD process also clears recommendation claims | Exam Ready without G6.3 / Never-Build compliance |
| Input to G1.9 / educational GO | Silent C-V1 (still need G2–G12) |

---

## 6. Standing freezes (C-COM hard stops)

These remain **prohibited in public** until their governing artefacts lift them — regardless of E2/E3 wins:

| Freeze | Authority | Public claim status |
|---|---|---|
| Recommendation-effectiveness marketing | DR-036; EP-001 / EP-003 G9; G4.5 | **Frozen** |
| Exam Ready / false readiness marketing | DR-035; G6.3; Vision Never-Build | **Banned** |
| Educational effectiveness | EP-003/004/007.3; DR-021/022/033 | **NO-GO / PENDING** |
| Personalisation usefulness under W-PROD while flags OFF | DR-039; PA-011 | **Δ = 0; do not market** |
| Version 1 production-ready | DR-041; P-002.1; dossier | **NO GO** |
| Twin / cutover as production-default student authority | DR-009; DR-010 | **OFF; no default claim** |
| Pass-rate lift | Vision / methodology gap (PR-024) | **Unavailable** |
| Estimated KSI as validated | DR-026; PA-023 Rejected | **Forbidden** |
| Perception as effectiveness | DR-033; PA-025 Rejected | **Forbidden** |
| Operational GA as educational ready | DR-032; PA-027 Rejected | **Forbidden** |

---

## 7. Version 1 posture card (2026-07-26)

Use this as the default Board answer until evidence programmes update it.

| Claim code | Allowed now? | Evidence basis |
|---|---|---|
| C-IMP | **Yes** (named surfaces with E2) | EP-003.* contracts; EP-006.2; EP-007.1 etc. |
| C-STR | **Yes** (bounded) | Checklist Pass + tests |
| C-VAL-I | **Yes** (bounded, Medium) | Tier B packs; KSI 62 |
| C-VAL-E | **No** | N_external = 0 |
| C-EDU | **No** | E5 unavailable; G1.9 FAIL |
| C-BEN (outcome) | **No** | E5 unavailable |
| C-BEN (internal perceived) | **Board-only under-claim** via C-VAL-I | Not public C-COM |
| C-REL | **Partial** — ops claims only with pack; ≠ educational | G7–G11 incomplete for V1 package |
| C-V1 | **No** | G1 FAIL; package incomplete |
| C-COM educational | **No** (freezes) | §6 |
| C-REC | **Yes — NO GO** | DR-041; P-003.1 |

**Board one-liner:**

> We may say what is implemented and structurally verified, and — internally — what Tier B validated under Medium confidence. We may **not** say we are educationally effective, externally validated, commercially proven, or Version 1 production-ready.

---

## 8. Claim drafting rules

1. **One claim, one code** — do not smuggle C-EDU inside a C-IMP sentence.  
2. **Disclose window** — W-PROD vs W-GATED.  
3. **Disclose N and confidence** for C-VAL-I / C-VAL-E.  
4. **Link paths** — unlinked claims are invalid.  
5. **Prefer lower** on conflict.  
6. **Public = C-COM** — if unsure, do not publish; walk `CLAIM_DECISION_TREE.md`.  
7. **Separable verdicts** — programme GO ≠ effectiveness GO ≠ C-V1.

---

## 9. Escalation

| Situation | Action |
|---|---|
| Wanted claim exceeds evidence | Downgrade language or DEFER; open evidence programme |
| Conflict between E2 and E3 | Prefer lower claim; document |
| Honesty incident | Freeze affected C-VAL / C-EDU / C-COM; G1.10 path |
| Marketing draft without matrix check | Reject until worksheet filed (`EVIDENCE_CLASSIFICATION.md` §6) |

---

## 10. References

- [`EVIDENCE_HIERARCHY.md`](EVIDENCE_HIERARCHY.md)  
- [`CLAIM_DECISION_TREE.md`](CLAIM_DECISION_TREE.md)  
- [`CLAIM_TRACEABILITY.md`](CLAIM_TRACEABILITY.md)  
- P-001.1 PSF; P-002.1 Release Framework; P-003.1 Dossier; DR-021…DR-041  

---

**End of CLAIM_STANDARD**
