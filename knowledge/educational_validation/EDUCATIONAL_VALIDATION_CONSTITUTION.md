# Educational Validation Constitution

**Framework ID:** EVF-001  
**Programme:** Programme V — Educational Validation Framework  
**Classification:** Highest educational *quality* authority for release decisions  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Effective:** July 2026  

---

## Authority

This Constitution defines the permanent principles of Kwalitec’s Educational Validation Framework (EVF).

It governs **whether educational quality is sufficient to release**.  
It does **not** redefine educational meaning (that remains `KWALITEC_EDUCATIONAL_CONSTITUTION.md`, EGI-001).  
It does **not** replace Educational Governance Review (EGI-003).  
It does **not** replace or alter Blind Review.

Where this Constitution conflicts with a proposed release practice, **this Constitution prevails** for educational quality approval. Where it would conflict with Educational Constitution (EGI-001) meaning, **EGI-001 prevails** and EVF must not certify unlawful educational claims.

---

## Preamble

Kwalitec ships software to students who trust it with scarce study time and fragile confidence.

Engineering excellence can prove that a build works.  
Educational governance can prove that a build tells educational truth.  
Neither alone proves that students should **trust** the educational product enough to rely on it.

Therefore Kwalitec binds itself to a permanent Educational Validation Framework: evidence before opinion, capabilities before marketing claims, and an explicit Educational Release Gate before every version that reaches students.

Educational trust is earned. It is never assumed from shipping velocity, feature count, or architectural elegance.

---

## Article I — Purpose

### Section 1. The Central Question

EVF exists to answer:

> Has Kwalitec demonstrated sufficient educational quality to justify releasing this version to students?

### Section 2. The Version 1 Standard

Version 1.0 requires independent educational validation that Study Plans, Daily Missions, Recovery Plans, Revision Strategy, Readiness Assessment, and educational explanations are trusted — with overall educational trust at or above the agreed threshold (see Educational Release Standard).

### Section 3. Completeness Rule

No feature may be considered complete until it satisfies the Educational Release Gate applicable to its version and capability scope.

---

## Article II — Independence

### Section 1. Independence from Runtime A

EVF shall remain independent of Runtime A. Validation artefacts may inspect student-visible behaviour and recorded evidence; they shall not execute inside the educational decision path.

### Section 2. Independence from Recommendation Generation

EVF shall never generate, select, rank, or mutate recommendations, missions, plans, or readiness scores.

### Section 3. Evaluation Only

EVF evaluates educational decisions and experiences. It does not become a second educational brain.

### Section 4. Blind Review Integrity

Blind Review is a mature research subsystem. EVF shall:

1. Preserve Blind Review exactly as implemented;
2. Consume Blind Review outputs as evidence;
3. Never rewrite Blind Review protocol, personas, scoring rules, or independence constraints as part of validation convenience.

---

## Article III — Constitutional Principles

These principles are binding for all EVF work:

1. **Educational quality before feature count.**  
   Shipping more surfaces does not increase educational trust.

2. **Student learning before algorithm complexity.**  
   Sophistication that students cannot use or believe does not count as quality.

3. **Explainability before sophistication.**  
   Opaque “intelligence” fails validation even when outputs appear clever.

4. **Educational evidence before opinion.**  
   Release decisions cite artefacts: capability reviews, comparative reviews, dimension scores, benchmarks, and supporting educational evidence.

5. **Capabilities are approved independently.**  
   Strength in one capability does not waive weakness in another required for the version bar.

6. **No release without educational validation.**  
   Engineering GO and architecture GO are necessary but not sufficient.

7. **No release based solely on engineering success.**  
   Green CI, GA certification, and deployability do not constitute educational approval.

8. **Educational trust is earned, never assumed.**  
   Prior release approval does not auto-approve a subsequent version; evidence must be current for the candidate under review.

9. **Honesty over theatre.**  
   Empty educational claims, dual homes for the same decision, and certainty without inspectability are validation failures — not UX polish issues alone.

10. **Explainable decisions.**  
    Every APPROVED, CONDITIONAL APPROVAL, or REJECTED outcome must state the evidence path that produced it.

---

## Article IV — Levels of Validation

EVF permanently recognises four layers:

| Layer | Name | Obligation |
|---:|---|---|
| 1 | Educational Capability Validation | Each Version capability is reviewed independently |
| 2 | Blind Comparative Review | Independent preference and reasoning vs human and alternative strategies |
| 3 | Educational Quality Assessment | Each capability is scored on permanent educational dimensions |
| 4 | Educational Release Gate | Official educational approval authority for the version |

Layers 1–3 produce evidence. Layer 4 alone may issue a release decision.

---

## Article V — Evidence Hierarchy

When evidence conflicts, prefer in this order unless the Release Gate explicitly documents a justified exception:

1. Direct student-visible behaviour under a frozen baseline  
2. Blind Review transcripts and registered comparative reviews  
3. Capability validation reports filed under EVF  
4. Dimension and benchmark summaries that cite (1)–(3)  
5. Secondary synthesis (meta-analysis, strategy bridges)  
6. Founder or stakeholder opinion

Opinion may inform interpretation. It may never alone produce APPROVED.

---

## Article VI — Release Outcomes

The Educational Release Gate shall produce exactly one of:

| Outcome | Meaning |
|---|---|
| **APPROVED** | Educational quality meets the version standard; educational release may proceed subject to engineering/architecture gates |
| **CONDITIONAL APPROVAL** | Educational release may proceed only with named, time-bounded holds and explicit student-facing honesty about limited claims |
| **REJECTED** | Educational quality is insufficient; the version must not be released to students under educational claims for the rejected scope |

No implementation, marketing statement, or beta expansion may bypass this Gate for educational quality claims.

---

## Article VII — Scope Boundaries

### In scope

- Educational quality of student-facing capabilities  
- Trust, practicality, exam readiness contribution, explainability, personalisation, motivation, consistency, and confidence as defined in Educational Dimensions  
- Comparative educational preference against registered benchmarks  
- Version Approval Reports as official educational approval artefacts  

### Out of scope

- Software architecture correctness (Architecture Constitution / ADRs)  
- Security, performance, and operational GA certification  
- Rewriting Educational Constitution meaning  
- Changing Blind Review methodology  
- Runtime A integration or recommendation mutation  

---

## Article VIII — Amendment

1. Amendments require an explicit Architecture / Educational governance decision recorded under `knowledge/educational_validation/`.  
2. Amendments must not silently weaken Version thresholds without updating the Educational Release Standard and notifying release operators.  
3. Dimension and benchmark catalogues may evolve additively under their own documents without amending this Constitution, provided Articles II–VI remain intact.  
4. Deprecating a constitutional principle requires a new Constitution version and a migration note in the next Version Approval Report.

---

## Article IX — Cross References

| Document | Role |
|---|---|
| `EDUCATIONAL_RELEASE_STANDARD.md` | Version bars and trust threshold |
| `EDUCATIONAL_RELEASE_GATE.md` | Gate procedure |
| `CAPABILITY_VALIDATION_GUIDE.md` | Layer 1 |
| `BLIND_COMPARATIVE_REVIEW.md` | Layer 2 |
| `EDUCATIONAL_DIMENSIONS.md` | Layer 3 |
| `EDUCATIONAL_BENCHMARKS.md` | Benchmark registry |
| `VERSION_APPROVAL_WORKFLOW.md` | Operator workflow |
| `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Educational law |
| `knowledge/educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` | Integrity review |
| `knowledge/architecture/BLIND_REVIEW_CURRENT_STATE.md` | Blind Review as-built boundary |
| `knowledge/product/ep004_private_beta/reviewer_framework/` | Blind Review execution |

---

**Status:** Governing  
**Next review:** After first Version 1.0 Educational Release Gate execution, or end of next major release — whichever is sooner
