# Operational Architecture

**Programme:** OA-001 — Operational Architecture & Product Lifecycle Framework  
**Version:** 1.0  
**Status:** Active — permanent operating model  
**Effective:** 2026-07-28  
**Authority:** DG-001 · RR-002 · ER-002 · `knowledge/GOVERNANCE.md` · all approved governance and engineering artefacts  
**Constraint:** Framework only — does not change application behaviour, UI, schema, educational algorithms, or release artefacts.

---

## 1. Purpose

This document is the **permanent operating model** for how Kwalitec is governed and evolved after completion of the Governance (DG-001, RR-002) and Engineering (ER-002) programmes.

It answers, for any future team:

1. How is work initiated?
2. Who owns which class of decision?
3. How are features, architecture, governance, engineering, and releases executed and reviewed?
4. When must certification be renewed?
5. Where is the single authoritative source for each concern?

**Success criterion:** A future engineering team can operate Kwalitec without relying on institutional memory.

---

## 2. Relationship to existing authorities

OA-001 does **not** replace higher law. It **orchestrates** how that law is applied in day-to-day product evolution.

| Layer | Authority | Role relative to OA-001 |
|-------|-----------|-------------------------|
| Product philosophy | Vision 2030 (`knowledge/product/vision/PRODUCT_VISION_2030.md`) | Why; north star; never-build; Final Test |
| Operational principles | Product Constitution (this programme) | Enduring operating principles for trust, evidence, and lifecycle |
| Meta-governance | `knowledge/GOVERNANCE.md` | Document & decision hierarchy |
| Educational meaning | Educational Constitution (EGI-001) | What learning / evidence / mastery mean |
| Educational governance | DG-001 Educational Governance Constitution | Vocabulary, authority, reflection procedure |
| Educational release quality | EVF | Whether educational quality justifies release |
| Architecture law | Architecture Constitution + ADRs | Structural invariants |
| Engineering practice | Engineering Standards + Quality Manual | How we build and verify |
| Version 1 declaration | P-002.1 Release Framework | Gates G1–G12; go / no-go |
| Engineering claim class | ER-002 | Engineering Conditional GO (invite-only Alpha) |
| Runtime presentation | RR-002 | Sole-runtime Education OS; Contained legacy |

**Conflict rule:** On conflict between this operating model and a higher authority, **STOP**, document, amend the higher authority first (or amend OA-001 if it overreached). Never silently reinterpret educational meaning or architecture law through process documents.

---

## 3. Responsibility domains

Kwalitec separates four domains. One Founder may hold multiple capacities (GP-001); the **domains remain distinct** in assessment and evidence.

| Domain | Owns | Does not own |
|--------|------|--------------|
| **Governance** | Educational law, vocabulary, authority, reflection, claim honesty, constitution amendment | Implementation code; release deploy commands |
| **Engineering** | Runtime safety, CI, dependencies, performance HOLDs, architecture tests, deploy fingerprint | Educational GO/NO-GO; marketing claim language beyond engineering evidence |
| **Product** | Roadmap, PRDs, KSI prioritisation, student-value programmes, Version 1 board synthesis | Bypassing EVF or P-002.1 gates |
| **Operations** | Release execution, hotfixes, runbooks, incident response, certification renewal triggers, debt review cadence | Inventing educational algorithms under ops cover |

**Independence rule:** Educational governance readiness and engineering readiness are **independently assessed**. Engineering Conditional GO does not imply Product Version 1 GO. Educational APPROVED does not waive engineering HOLDs.

---

## 4. Operating model map

```
                    Vision 2030 + Product Constitution
                                   │
                    knowledge/GOVERNANCE.md (hierarchy)
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
   Governance changes        Product / Features         Engineering changes
   (CHANGE_MANAGEMENT)       (FEATURE_LIFECYCLE)        (CHANGE_MANAGEMENT)
        │                          │                          │
        │                   Architecture ADRs                 │
        │              (ADR_STANDARD · before code)           │
        │                          │                          │
        └──────────────┬───────────┴───────────┬──────────────┘
                       │                       │
                 Independent Review      Risk & Debt reviews
                       │                       │
                       └───────────┬───────────┘
                                   │
                         Release / Hotfix lifecycle
                    (RELEASE_GOVERNANCE_MODEL)
                                   │
                    Certification / audit / renewal
```

Companion standards in this package:

| Concern | Document |
|---------|----------|
| Enduring principles | `PRODUCT_CONSTITUTION.md` |
| Architecture decisions | `ARCHITECTURE_DECISION_RECORD_STANDARD.md` |
| Features | `FEATURE_LIFECYCLE.md` |
| Technical debt | `TECHNICAL_DEBT_GOVERNANCE.md` |
| Releases & hotfixes | `RELEASE_GOVERNANCE_MODEL.md` |
| Change classes | `CHANGE_MANAGEMENT_STANDARD.md` |
| Risk | `RISK_REVIEW_STANDARD.md` |
| Programme status | `PROGRAMME_DASHBOARD.md` |

---

## 5. Product lifecycle (permanent)

| Stage | Meaning | Exit criteria |
|-------|---------|---------------|
| **Conceive** | Problem framed against Vision Final Test + estimated KSI | PRD or programme brief approved |
| **Govern** | Educational / architecture / privacy impact classified | Required reviews scheduled; ADR if structural |
| **Blueprint** | Design, contracts, claim language, evidence plan | Blueprint / ADR / PRD design freeze |
| **Implement** | Code and tests per Engineering Standards | Definition of Done met |
| **Independent Review** | Educational, architecture, engineering, or privacy lens as class requires | Checklist Pass / Conditional / Fail recorded |
| **Certify** | Completion report + gate outcomes | Programme Pass / Conditional Pass / Fail |
| **Release** | Classify → verify → deploy → fingerprint → smoke | Release report filed |
| **Operate** | Observe residuals, debt, risks, flags | Cadence reviews current |
| **Renew / Retire** | Recertify on triggers; deprecate with register | Certification current or explicit sunset |

Stages may be thin for docs-only or hotfix work, but **must not be skipped silently** when the change class requires them (see Change Management Standard).

---

## 6. Cadences

| Cadence | Activity | Owner capacity | Artefacts |
|---------|----------|----------------|-----------|
| **Per PR** | Engineering Standards + DoD | Engineering Owner | PR checklist |
| **Per Epic / programme** | Debt register review; ADR currency; completion report | Product + Engineering | `docs/TECHNICAL_DEBT_REGISTER.md`; programme report |
| **Per student-facing intelligence change** | Explainability + Recommendation reviews as applicable | Product + Educational Gate | P-001.2 / P-001.3 checklists |
| **Per educational capability change** | Educational Governance Review (EGI-003) | Educational Gate Owner | DG-001 / EGI artefacts |
| **Per release** | Release Playbook + Protocol; EVF gate if educational claims | Operations Owner | Release report; gate outcome |
| **Quarterly (or pre-claim expansion)** | Risk review; architectural Contained residuals | Product Board Chair | Risk register; dashboard |
| **On certification trigger** | Engineering and/or educational recertification | Domain owner | Audit / certification report |

Detailed triggers: §9 and `RELEASE_GOVERNANCE_MODEL.md` / `RISK_REVIEW_STANDARD.md`.

---

## 7. Documentation ownership

| Document class | Canonical home | Owner capacity | Update rule |
|----------------|----------------|----------------|-------------|
| Vision / Blueprint | `knowledge/product/vision/`, repo root Blueprint | Product Owner | Amendment process; never silent drift |
| Educational governance | `knowledge/governance/`, `knowledge/educational/` | Educational Gate Owner | DG-001 amendment process |
| Architecture Constitution / ADRs | `docs/`, `docs/adr/`, secondary trees | Engineering Owner (architecture lens) | ADR before structural merge |
| Engineering standards / quality | `knowledge/ENGINEERING_STANDARDS.md`, `QUALITY_MANUAL.md` | Engineering Owner | Versioned updates; cite reason |
| Technical debt register | `docs/TECHNICAL_DEBT_REGISTER.md` | Engineering Owner | Every Epic close; debt governance standard |
| Product risks | `knowledge/product/p003_3_product_risk_register/` | Product Owner | Risk review standard |
| Release procedure | `knowledge/RELEASE_PLAYBOOK.md`, `docs/process/RELEASE_PROTOCOL.md` | Operations Owner | Protocol wins on procedure detail |
| Operational framework (OA-001) | `knowledge/operations/oa001/` | Operations Owner | Amendment via Change Management (Governance class) |
| Programme dashboard | `PROGRAMME_DASHBOARD.md` | Product Owner | Update at programme start/end and board reviews |

**One authoritative source rule:** Every major engineering concern has exactly one primary register or constitution. Secondary docs **link**; they do not fork conflicting truth.

---

## 8. Authoritative source map (engineering & ops)

| Concern | Authoritative source |
|---------|----------------------|
| App version | `app/version.py` |
| Production flags / G12 claims | `docs/production/VERSION_1_FLAG_MATRIX.md` + `render.yaml` |
| G7 performance posture | `docs/production/G7_PERFORMANCE_HOLD.md` |
| Dependency policy | `docs/security/DEPENDENCY_ASSURANCE_POLICY.md` |
| Technical debt | `docs/TECHNICAL_DEBT_REGISTER.md` |
| Product risks | P-003.3 Product Risk Register |
| Educational vocabulary | DG-001.1 Canonical Educational Lexicon |
| Educational speech authority | DG-001.2 Educational Authority Model |
| Student presentation path | RR-002 sole-runtime (`/student`, `/session`) |
| Engineering claim class (post ER-002) | `knowledge/release/ER-002/ER002_RELEASE_RECOMMENDATION.md` |
| Version 1 production-ready gates | P-002.1 Version 1 Release Framework |
| Layering / curriculum V1+V2 | `ARCHITECTURE.md` + Architecture Constitution |

---

## 9. Certification renewal triggers

Recertification is required when any of the following occur. Partial renewal may be domain-scoped (engineering-only or educational-only) when the other domain is unaffected **and** that independence is documented.

| Trigger | Domain | Minimum action |
|---------|--------|----------------|
| Material change to educational algorithms, Twin, or EducationalState contracts | Educational (+ Engineering as needed) | Educational Governance Review + EVF path; architecture ADR if structural |
| Material change to CI integrity, authn/authz, dependency Critical gates, or deploy path | Engineering | Engineering audit / gate re-verify |
| Intent to expand claim class (e.g. invite-only → Stage 1 / high-traffic / V1 production-ready) | Both | Full gate board review (G1–G12 as applicable) |
| Lift or rewrite of a formal HOLD (e.g. G7) | Engineering (+ Product claims) | New evidence pack + claim language update |
| Contained dual-stack / dual-authority consolidation | Architecture + Educational | ADR + educational continuity review |
| Security incident or Critical vulnerability in production path | Engineering + Operations | Incident report; recertify affected gates |
| Marketing or board language that would exceed verified evidence | Product + Governance | STOP; align claims to evidence or gather evidence first |
| 12 months since last engineering claim-class certification without interim audit | Engineering | Lightweight recertification or explicit deferral with rationale |
| Discovery that a prior certification assumed false premises | Owning domain | Invalidate affected claims; re-audit |

**Rule:** Certification does not age into stronger claims. Silence is not renewal.

---

## 10. Forbidden operating patterns

- Shipping significant features without Blueprint → Implementation → Independent Review.
- Treating Engineering GO as Product GO (or the reverse).
- Marketing claims that exceed verified evidence.
- Implementing structural architecture changes before an ADR is accepted.
- Leaving material technical debt without owner or remediation plan.
- Opening educational governance under an “engineering-only” programme cover.
- Relying on institutional memory instead of updating the Programme Dashboard and authoritative registers.

---

## 11. How to start work (quick path)

1. Classify the change (`CHANGE_MANAGEMENT_STANDARD.md`).
2. Confirm Vision Final Test and domain ownership.
3. Follow the matching lifecycle (Feature / Architecture ADR / Governance / Engineering / Release / Hotfix).
4. Record outcomes on the Programme Dashboard and in the required completion / release artefacts.
5. Update debt, risk, and claim language if residuals change.

---

**End of Operational Architecture**
