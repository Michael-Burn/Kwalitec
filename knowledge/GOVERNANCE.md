# Kwalitec Governance

**Version:** 1.0  
**Status:** Active  
**Effective:** July 2026  
**Programme:** Post-Consolidation Product Governance  

This document defines permanent governance for product, architecture, and engineering decisions after Architecture Consolidation.

It does **not** redesign the application or change educational algorithms.

---

## 1. Document hierarchy

Authority flows **downward**. Lower documents must not contradict higher ones. When conflict appears: **STOP**, document, recommend amendment of the higher authority first.

| Rank | Document | Canonical path | Owns |
|---:|---|---|---|
| 1 | Product Vision 2030 | `knowledge/product/vision/PRODUCT_VISION_2030.md` | Why; north star; philosophies; never-build; Final Test |
| 2 | Product Blueprint | `PRODUCT_BLUEPRINT.md` (repo root) | Strategy; audiences; model; roadmap; promise |
| 3 | Educational Constitution | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Educational law and truth |
| 4 | Architecture Constitution + System Architecture | `docs/ARCHITECTURE_CONSTITUTION.md`, `docs/architecture/SYSTEM_ARCHITECTURE.md`, `ARCHITECTURE.md` | Structural law; one runtime; layering |
| 5 | ADRs | `docs/adr/` (primary EOS); historical trees indexed there | Accepted architectural decisions |
| 6 | Engineering Standards + Quality Manual | `knowledge/ENGINEERING_STANDARDS.md`, `knowledge/QUALITY_MANUAL.md` | How we build and verify |
| 7 | PRDs | `knowledge/prd/` | Feature proposals |
| 8 | Release Playbook + Release Protocol | `knowledge/RELEASE_PLAYBOOK.md`, `docs/process/RELEASE_PROTOCOL.md` | How we ship |
| 9 | Version 1 Readiness | `knowledge/VERSION_1_READINESS.md` | Readiness tracking |

### Path note (resolved)

The post-consolidation directive referenced `knowledge/PRODUCT_BLUEPRINT.md`. The authoritative Blueprint remains at **repository root** `PRODUCT_BLUEPRINT.md` to avoid duplication. Do not create a second Blueprint under `knowledge/`.

### Supporting indexes

| Index | Path |
|---|---|
| Vision folder | `knowledge/product/vision/README.md` |
| Knowledge base | `knowledge/README.md` |
| ADR index (EOS) | `docs/adr/README.md` |
| Ubiquitous language | `UBIQUITOUS_LANGUAGE.md` |
| Product language (UI) | `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` |

---

## 2. Decision hierarchy

| Decision type | Primary authorities | Approver (default) |
|---|---|---|
| Product philosophy / never-build | Vision 2030 | Product owner |
| Roadmap / audience / promise | Blueprint | Product owner |
| Educational meaning / mastery / evidence | Educational Constitution | Educational governance |
| Runtime, layering, Twin boundaries | Architecture Constitution + ADRs | Architecture |
| Feature scope | PRD → Vision + Blueprint alignment | Product + Architecture as needed |
| Implementation pattern | Engineering Standards + ADRs | Engineering |
| Ship / rollback | Release Playbook + Protocol | Release operator |

**Final Test (mandatory for features):**

> Does this help students become better professionals?

If no → do not build.

---

## 3. Review process

### 3.1 Document review

| Trigger | Action |
|---|---|
| End of major release | Review Vision (philosophy drift), Blueprint (roadmap), Readiness tracker |
| End of Epic | Review Technical Debt Register, ADR currency, Quality Manual budgets |
| Educational capability change | Educational Governance Review Standard (EGI-003) |
| Architecture boundary change | New or amended ADR before merge |

### 3.2 Pull Request review

Every PR must satisfy (see Engineering Standards):

- Tests
- Documentation
- Accessibility (if UI)
- Security
- Performance (budgets / no regress without justification)
- Architecture (layering, no duplicate educational logic)

### 3.3 When uncertain

1. **STOP**
2. **Document** the uncertainty
3. **Recommend** options with Vision / Blueprint / Educational Constitution citations
4. **Never guess** into educational algorithms, Twin, or EducationalStateService

---

## 4. Feature proposal process

1. Author a PRD using `knowledge/prd/PRD_TEMPLATE.md`.
2. Complete Vision Alignment and Architecture Impact sections honestly.
3. Product reviews student/educational benefit and Final Test.
4. Architecture reviews Educational State / Twin / runtime impact.
5. If educational law may be affected → Educational Governance review before implementation.
6. Implementation follows Engineering Standards; PR uses Definition of Done.
7. Completion report per project reporting rules when required by milestone.

**No PRD → no significant feature work.**

Exceptions (still require review notes): hotfixes, pure docs, pure chore with no behaviour change.

---

## 5. Architecture proposal process

1. Confirm Vision / Blueprint / Educational Constitution do not forbid the change.
2. Write or amend an ADR under the correct tree (`docs/adr/` for EOS boundaries).
3. ADR must reference Vision 2030, Blueprint, and Educational Principles (Constitution).
4. Update `docs/adr/README.md` (and secondary indexes if historical trees change).
5. Prefer additive changes with compatibility shims over breaking rewrites.
6. Document migration impact and V1/V2 curriculum effects.
7. Do not bypass StartupService safety or introduce a second educational brain.

**Forbidden without explicit programme authority:**

- Redesigning the Student Digital Twin
- Changing EducationalStateService contracts casually
- Changing educational algorithms under “governance” or “docs” cover
- Introducing duplicate educational logic

---

## 6. Post-consolidation posture

Architecture Consolidation is **COMPLETE**. The Education Operating System is the canonical runtime.

Development focus: product excellence, governance, quality, documentation, engineering maturity, release readiness — not parallel educational architectures.

---

## 7. Related programmes

| Programme | Artefact |
|---|---|
| Engineering governance | `knowledge/ENGINEERING_STANDARDS.md` |
| Quality platform | `knowledge/QUALITY_MANUAL.md` |
| Product requirements | `knowledge/prd/` |
| Product analytics (design only) | `knowledge/product/analytics/PRODUCT_ANALYTICS_ARCHITECTURE.md` |
| Private beta prep | `knowledge/product/private_beta/README.md` |
| Technical debt | `docs/TECHNICAL_DEBT_REGISTER.md` |
| Release management | `knowledge/RELEASE_PLAYBOOK.md` |
| V1 readiness | `knowledge/VERSION_1_READINESS.md` |

---

**Status:** Active  
**Next review:** End of next major release
