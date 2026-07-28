# Product Constitution

**Programme:** OA-001 — Operational Architecture & Product Lifecycle Framework  
**Version:** 1.0  
**Status:** Active — enduring operational principles  
**Effective:** 2026-07-28  
**Authority:** Vision 2030 · DG-001 · RR-002 · ER-002 · `knowledge/GOVERNANCE.md`  
**Constraint:** Principles only — does not change application behaviour.

---

## 1. Purpose and relationship

This Product Constitution defines **enduring operating principles** for how Kwalitec is evolved, claimed, reviewed, and certified.

It is **complementary** to Vision 2030 (`knowledge/product/vision/PRODUCT_VISION_2030.md`), which remains the executive product-philosophy apex (why, north star, never-build, Final Test).

| Document | Owns |
|----------|------|
| **Vision 2030** | Product philosophy; educational purpose; never-build list; Final Test |
| **This Constitution** | Operating principles for trust, evidence, lifecycle discipline, and claim honesty |
| **Educational Constitution (EGI-001)** | Educational meaning and integrity |
| **Educational Governance Constitution (DG-001.4)** | Educational governance procedure |
| **Architecture Constitution** | Structural architectural law |

**Conflict rule:** Vision 2030 and EGI-001 win on philosophy and educational meaning. This Constitution wins on *how the organisation must operate* when evolving the product — unless a higher authority is amended first.

Historical references to “Product Constitution” that mean Vision 2030 remain valid for philosophy. For **lifecycle and claim discipline**, cite this document (`knowledge/operations/oa001/PRODUCT_CONSTITUTION.md`).

---

## 2. Preamble

Kwalitec exists to help candidates for demanding professional examinations study with clarity, honesty, and continuity.

Governance programmes (DG-001, RR-002) and engineering recertification (ER-002) established that **trust is earned through evidence and separation of concerns**, not through feature volume or optimistic marketing.

This Constitution freezes the operating principles that future programmes must obey so excellence does not depend on who happens to remember the rules.

---

## 3. Constitutional principles

These principles are permanent. Amendment requires a Governance-class change under `CHANGE_MANAGEMENT_STANDARD.md` with Founder Review.

| ID | Principle | Meaning |
|----|-----------|---------|
| **PC-01** | Student trust outweighs feature count | Features that increase surface area while eroding honesty, agency, or explainability must not ship. Prefer fewer, trustworthy capabilities. |
| **PC-02** | Educational governance and engineering readiness are independently assessed | Educational GO/NO-GO and Engineering GO/HOLD/NO GO are separate boards of evidence. Neither implies the other. |
| **PC-03** | Marketing claims shall never exceed verified evidence | Claim language is bounded by filed evidence packs, gate outcomes, HOLDs, and Contained disclosures. Aspiration is not evidence. |
| **PC-04** | Every production claim requires traceable evidence | Any statement about production behaviour, readiness, performance, security, or educational quality must cite artefact paths and dates. |
| **PC-05** | Every major engineering concern has one authoritative source | Debt, risks, flags, version, dependency policy, and claim-class certifications each have a single canonical register or document. Forks are forbidden. |
| **PC-06** | Architecture decisions are documented before implementation | Structural, boundary, authority, or dual-runtime changes require an accepted ADR (or explicit amendment) before implementation merge. |
| **PC-07** | Every significant feature follows Blueprint → Implementation → Independent Review | Significant features may not skip design freeze or independent review. Thin paths exist only for classified exceptions (hotfix, pure docs, pure chore). |
| **PC-08** | Technical debt must have an explicit owner or remediation plan | Unowned debt is not acceptable. Register entries require owner capacity and target or accepted-residual rationale. |
| **PC-09** | Deterministic educational cores remain non-negotiable | Planning, readiness, and recommendations stay reproducible from the same inputs; no opaque LLM authority in the core learning path. |
| **PC-10** | Curriculum and educational truth precede presentation convenience | UI and growth tactics must not invent educational truth. Sole-runtime presentation (RR-002) is the student path; legacy remains Contained until retired lawfully. |
| **PC-11** | Advice remains advisory; student agency is preserved | Guidance must not coerce, score reflection for ranking, or present estimates as validated certainty without disclosure. |
| **PC-12** | Prefer STOP over silent expansion of claim class | When evidence is thin, stop claim expansion; do not soft-amend constitutions mid-delivery. |

---

## 4. Final Test (inherited)

From Vision 2030, mandatory for features:

> Does this help students become better professionals?

If no → do not build.

OA-001 adds the **Operating Test**:

> Can we explain, evidence, and independently review this change without relying on institutional memory?

If no → do not start until the operating artefacts exist.

---

## 5. Claim honesty rules

1. **Invite-only / Alpha claims** must respect ER-002 conditions (G7 HOLD, Contained architecture disclosure, no unqualified V1 engineering GO).
2. **Version 1 production-ready** requires P-002.1 gates G1–G12 and Product Board recommendation — not estimated ΔKSI alone.
3. **Educational trust claims** require EVF Educational Release Gate outcomes.
4. **Feature-flag OFF** capabilities must not be marketed as live (G12).
5. **Conditional** outcomes must be stated as Conditional; they do not age into Pass.

---

## 6. Separation of assessments (normative)

| Assessment | Answers | Authoritative frameworks |
|------------|---------|--------------------------|
| Educational governance readiness | Is educational law coherent and complied with? | DG-001 · EGI · Educational Constitution |
| Educational release quality | Is educational quality sufficient to release to students? | EVF |
| Engineering readiness | Is the system safe and operable for the claimed class? | P-002.1 G7–G12 · ER programmes · Engineering Standards |
| Product Version 1 declaration | May we declare production-ready? | P-002.1 full board · P-003.1 dossier |

Mixing these questions in a single unchecked narrative is a constitutional violation (PC-02, PC-03).

---

## 7. Duties of programmes

Every material programme must:

1. State its change class and domain ownership.
2. Cite higher authorities and confirm non-contradiction.
3. Produce the evidence artefacts required by its class.
4. Record residuals, debt, and claim-language impact.
5. Update `PROGRAMME_DASHBOARD.md` at start and completion.

Docs-only / audit-only programmes may record ΔKSI = 0 and N/A for student-facing checklists with rationale — they must still obey PC-03–PC-05.

---

## 8. Amendment

1. Propose change with rationale and impact on PC-01…PC-12.
2. Founder Review (Product Owner capacity) with Educational and Engineering lenses as needed.
3. Update this file’s version and effective date.
4. Note amendment on the Programme Dashboard.
5. Do not amend Vision 2030, EGI-001, or Architecture Constitution through this process — use their own amendment paths.

---

**End of Product Constitution**
