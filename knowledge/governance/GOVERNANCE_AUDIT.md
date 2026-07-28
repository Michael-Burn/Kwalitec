# Governance Audit — Existing Strategic Documents

**Audit date:** 2026-07-28  
**Scope:** Read-only inventory of governance, philosophy, constitution, strategy, and release authority  
**Constraint:** Audit only — no new principles, constitutions, architecture, or product strategy changes  
**Companion artefacts:** `GOVERNANCE_HIERARCHY.md`, `GOVERNANCE_OVERLAP_MATRIX.md`, `GOVERNANCE_GAP_ANALYSIS.md`, `GOVERNANCE_RECOMMENDATIONS.md`, `GOVERNANCE_AUDIT_COMPLETION_REPORT.md`  
**Baseline meta-authority:** `knowledge/GOVERNANCE.md` (v1.0, Active, July 2026)

---

## 1. Executive summary

Kwalitec already has a **dense, ranked governance corpus**. The permanent hierarchy is defined in `knowledge/GOVERNANCE.md` (ranks 1–10) and is substantially populated:

| Layer | Authority exists? | Completeness |
|---|---|---|
| Vision / north star / never-build | Yes — Vision 2030 | Complete |
| Product strategy / Blueprint | Yes | Complete (ILE strategy docs elaborate) |
| Educational law (EGI) | Yes — Educational Constitution + Registry + Review Standard | Complete |
| Educational release quality (EVF) | Yes — Programme V | Complete |
| Architecture law | Yes — Architecture Constitution + ADRs + Design Principles | Complete |
| Measurement (KSI) | Yes — P-001.1 | Complete |
| Explainability / recommendation product gates | Yes — P-001.2 / P-001.3 | Complete |
| Version 1 production-ready gates | Yes — P-002.1 (G1–G12) | Complete |
| Product Board / registers / evidence claims | Yes — P-003.x + GP-001 | Complete |
| Study Sensei / Student Decision philosophy | Yes — ILE-010 / ILE-011 | Complete |
| Engineering / quality / ship procedure | Yes | Complete (multi-layer release stack) |
| AI enrichment boundary | Yes — ADR-008 | Complete |
| Brand | Yes — Brand Guidelines | Adequate |
| Standalone ethics / AI ethics charter | Partial — embedded in Vision, Twin Philosophy, ADR-008 | See gap analysis |

**Verdict:** Additional governance *constitutions* or a second hierarchy are **not required**. Future governance work should **extend, cross-link, or clarify** existing authority. Any proposal labelled GP-001 (or similar) must reference this audit first — noting that **GP-001 Founder Governance Model already exists** under `knowledge/product/gp001_founder_governance_model/`.

**Current Version 1 posture (governance state, not this audit’s decision):** Validated KSI **64** (target ≥ 80); Gate G1 **FAIL**; Product Board dossier recommendation **NO GO** (as of 2026-07-26 evidence freeze cited in GOVERNANCE.md).

---

## 2. Catalogue method

1. Seeded from `knowledge/GOVERNANCE.md` ranked table and §1a / §7 programme index.  
2. Expanded via repository search under `knowledge/`, `docs/`, repo root, `.cursor/rules/`.  
3. Classified each artefact as: **Constitutional / Strategic / Framework / Operational / Procedural / Supporting / Historical**.  
4. Programme completion reports and constitutional lifecycle *leaf* models are **clustered** (not individually catalogued as law) unless they define permanent authority.  
5. Authority status: **Active** unless document status or supersession evidence indicates otherwise.

**Authority levels used in this audit**

| Level | Meaning |
|---|---|
| Constitutional | Highest law in a domain; amend before contradicting |
| Strategic | Permanent product/engineering philosophy or strategy |
| Framework | Binding measurement, quality, release, or educational operational law |
| Operational | How work is executed / tracked |
| Procedural | Who decides / approval steps |
| Supporting | Index, alias, language, orientation |
| Historical | Point-in-time evidence or superseded practice |

---

## 3. Document inventory (authority records)

Fields: **Path · Title · Purpose · Primary owner · Authority level · Dependencies · Superseded by · Potential overlaps · Referenced by · Referenced documents · Still authoritative**

### 3.1 Meta-governance

| Field | Value |
|---|---|
| Path | `knowledge/GOVERNANCE.md` |
| Title | Kwalitec Governance |
| Purpose | Permanent post-consolidation document & decision hierarchy; review/PRD/EP completion rules; founder capacity note |
| Primary owner | Unstated (Product / Architecture Office implied); Founder capacities per GP-001 |
| Authority level | Constitutional (meta) |
| Dependencies | All ranked documents it indexes |
| Superseded by | None |
| Potential overlaps | `.cursor/rules/00-engineering.mdc`, `07-reporting.mdc` (agent enforcement of same rules) |
| Referenced by | Vision 2030, Blueprint, knowledge README, P-001/P-002/P-003 programmes, GP-001 |
| Referenced documents | Vision 2030, Blueprint, KSI, P-001.2/1.3, P-002.1, P-003.1, Educational Constitution, EVF, Architecture Constitution, ADRs, Engineering Standards, Quality Manual, PRDs, Release Playbook/Protocol, Version 1 Readiness, GP-001 |
| Still authoritative | **Yes — Active** |

### 3.2 Vision, mission, constitution (product apex)

| Field | Value |
|---|---|
| Path | `knowledge/product/vision/PRODUCT_VISION_2030.md` |
| Title | KWALITEC PRODUCT VISION 2030 |
| Purpose | Permanent product constitution: why Kwalitec exists, north star, philosophies, never-build, Final Test |
| Primary owner | Founder — Product Owner capacity |
| Authority level | Constitutional (product) — GOVERNANCE Rank 1 |
| Dependencies | None (apex product philosophy) |
| Superseded by | None |
| Potential overlaps | Blueprint (strategy only); `NON_GOALS.md` (expands never-build); Study Sensei / Product Principles (filters) |
| Referenced by | GOVERNANCE, Blueprint, ILE philosophy docs, P-001.x, P-002.1, Product Board Charter |
| Referenced documents | Blueprint, Educational Constitution, GOVERNANCE, GP-001 |
| Still authoritative | **Yes — Active** |

| Field | Value |
|---|---|
| Path | `PRODUCT_BLUEPRINT.md` (repo root) |
| Title | Kwalitec Product Blueprint |
| Purpose | How the product operates: audiences, model, Twin role, roadmap, promise |
| Primary owner | Founder — Product Owner capacity |
| Authority level | Strategic — Rank 2 |
| Dependencies | Vision 2030 |
| Superseded by | None (canonical path; do not duplicate under `knowledge/`) |
| Potential overlaps | `PRODUCT_STRATEGY.md`, `PRODUCT_ROADMAP.md`, `VERSION2_PRODUCT_STRATEGY.md` |
| Referenced by | GOVERNANCE, Vision, knowledge README |
| Referenced documents | Vision 2030, Educational Constitution, Product Language Guide, ARCHITECTURE.md, SYSTEM_ARCHITECTURE |
| Still authoritative | **Yes — Active** |

### 3.3 Educational constitution & integrity

| Field | Value |
|---|---|
| Path | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` |
| Title | Kwalitec Educational Constitution |
| Purpose | Highest educational authority (EGI-001): philosophy, truth, governance, terminology, integrity |
| Primary owner | Founder — Educational Gate Owner capacity |
| Authority level | Constitutional (educational) — Rank 3 |
| Dependencies | None (apex educational) |
| Superseded by | None |
| Potential overlaps | `EDUCATIONAL_CONSTITUTION.md` (alias); product `EDUCATIONAL_PHILOSOPHY.md`; V2 Educational Principles |
| Referenced by | GOVERNANCE, Blueprint, EVF, EIP/EGI suite, ILE docs, Architecture Constitution process |
| Referenced documents | Article X amendment rules; companion EGI/EIP docs |
| Still authoritative | **Yes — APPROVED governing** |

| Field | Value |
|---|---|
| Path | `knowledge/educational/EDUCATIONAL_CONSTITUTION.md` |
| Title | Educational Constitution |
| Purpose | Alias pointer to `KWALITEC_EDUCATIONAL_CONSTITUTION.md` |
| Primary owner | Same as EGI-001 |
| Authority level | Supporting |
| Dependencies | KWALITEC Educational Constitution |
| Superseded by | N/A (alias) |
| Potential overlaps | Name similarity with EVF Validation Constitution |
| Referenced by | Various historical links |
| Referenced documents | KWALITEC Educational Constitution |
| Still authoritative | **Yes — as alias only** |

| Field | Value |
|---|---|
| Path | `knowledge/educational/EDUCATIONAL_LOGIC_REGISTRY.md` |
| Title | Educational Logic Registry |
| Purpose | EGI-002 operational description of educational decisions (HOW) |
| Primary owner | Unstated (Educational Gate Owner) |
| Authority level | Framework |
| Dependencies | EGI-001 |
| Superseded by | None |
| Potential overlaps | Programme VI domain models; orchestration authority |
| Referenced by | EGI-003, EIP programme |
| Referenced documents | Educational Constitution |
| Still authoritative | **Yes** |

| Field | Value |
|---|---|
| Path | `knowledge/educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` |
| Title | Educational Governance Review Standard |
| Purpose | EGI-003 mandatory review before educational implementation approval |
| Primary owner | Educational Gate Owner |
| Authority level | Framework |
| Dependencies | EGI-001, EGI-002 |
| Superseded by | None |
| Potential overlaps | EVF capability validation; P-001.2/1.3 review checklists |
| Referenced by | GOVERNANCE §3.1 |
| Referenced documents | EGI-001/002 |
| Still authoritative | **Yes** |

| Field | Value |
|---|---|
| Path | `knowledge/educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md` |
| Title | Educational Explainability Standard |
| Purpose | EIP-003 educational speech contract (facts / estimates / advice) |
| Primary owner | Unstated |
| Authority level | Framework |
| Dependencies | EGI-001/002/003; EIP suite |
| Superseded by | None |
| Potential overlaps | **P-001.2 Explainability Standard** (product specialisation — intentional) |
| Referenced by | GOVERNANCE explainability note; P-001.2 |
| Referenced documents | EGI / EIP suite |
| Still authoritative | **Yes** |

| Field | Value |
|---|---|
| Path | `knowledge/educational/EDUCATIONAL_INTEGRITY_PROGRAMME_BLUEPRINT.md` |
| Title | Educational Integrity Programme Blueprint |
| Purpose | EIP-000 master roadmap for educational integrity capabilities to V1 |
| Primary owner | Unstated |
| Authority level | Strategic (programme map) |
| Dependencies | EGI-001/002/003 |
| Superseded by | None |
| Potential overlaps | Orchestration Programme VII; Product Trust Programme |
| Referenced by | EIP capability docs |
| Referenced documents | EGI suite |
| Still authoritative | **Yes — programme map, not law** |

**EGI/EIP specialised standards (cluster — Active Framework):** include Educational State Authority Matrix, Educational Evidence Model, Continuity Standard, Knowledge & Mastery Model, Educational Governance Certification V1, and Programme VI domain folders under `knowledge/educational/*/` (planning, scheduling, coach, recovery, revision, student_profile, etc.). All subordinate to EGI-001.

### 3.4 Educational Validation Framework (EVF — Rank 4)

| Path | Title | Purpose | Owner | Level | Authoritative |
|---|---|---|---|---|---|
| `knowledge/educational_validation/README.md` | EVF index | Official educational release governance index | Educational Gate Owner | Supporting | Yes |
| `…/EDUCATIONAL_VALIDATION_CONSTITUTION.md` | Educational Validation Constitution | EVF-001 principles for release-quality sufficiency | Educational Gate Owner | Constitutional (quality domain) | Yes |
| `…/EDUCATIONAL_RELEASE_STANDARD.md` | Educational Release Standard | Per-version educational release bar (V1 ≥80% trust) | Educational Gate Owner | Framework | Yes |
| `…/EDUCATIONAL_RELEASE_GATE.md` | Educational Release Gate | Layer-4 approval authority | Educational Gate Owner | Framework | Yes |
| `…/CAPABILITY_VALIDATION_GUIDE.md` | Capability Validation Guide | Layer 1 independent capability reviews | Educational Gate Owner | Framework | Yes |
| `…/BLIND_COMPARATIVE_REVIEW.md` | Blind Comparative Review | Layer 2 blind comparison protocol | Educational Gate Owner | Framework | Yes |
| `…/EDUCATIONAL_DIMENSIONS.md` | Educational Dimensions | Layer 3 permanent quality dimensions | Educational Gate Owner | Framework | Yes |
| `…/EDUCATIONAL_BENCHMARKS.md` | Educational Benchmarks | Benchmark registration | Educational Gate Owner | Framework | Yes |
| `…/VERSION_APPROVAL_WORKFLOW.md` | Version Approval Workflow | Approval workflow | Educational Gate Owner | Procedural | Yes |
| `…/RELEASE_DECISION_TEMPLATE.md` | Release Decision Template | Gate output template | Educational Gate Owner | Procedural | Yes |

**Dependencies:** EGI-001, EGI-003, Blind Review research framework.  
**Superseded by:** None.  
**Critical name overlap:** `knowledge/product/ep001_product_validation/EDUCATIONAL_VALIDATION_FRAMEWORK.md` answers a **different** question (effectiveness metrics / instrumentation), not release-gate authority.

### 3.5 Product frameworks (Ranks 2a–2e)

| Path | Title | Purpose | Owner | Level | Authoritative |
|---|---|---|---|---|---|
| `knowledge/product/p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md` | Product Success Framework | KSI law; V1 usefulness ≥ 80; K1–K8 | Product Owner | Framework | Yes |
| `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md` | Explainability Standard | Product explainability levels, schema, review gate | Product + Educational Gate | Framework | Yes |
| `knowledge/product/p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_STANDARD.md` | Recommendation Quality Standard | Recommendation quality principles, scorecard, review gate | Product + Educational Gate | Framework | Yes |
| `…/RECOMMENDATION_DECISION_FRAMEWORK.md` | Recommendation Decision Framework | Prioritisation of competing lawful tips | Unstated | Framework | Yes |
| `…/RECOMMENDATION_QUALITY_SCORECARD.md` | Recommendation Quality Scorecard | Scorecard metrics | Unstated | Framework | Yes |
| `knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md` | Version 1 Release Framework | Production-ready gates G1–G12; evidence; go/no-go | Product Board Chair | Framework | Yes |
| `…/VERSION_1_ACCEPTANCE_CHECKLIST.md` | Version 1 Acceptance Checklist | Gate checklist | Product Board | Framework | Yes |
| `…/VERSION_1_GO_NO_GO_GUIDE.md` | Version 1 Go / No-Go Guide | Decision procedure | Product Board | Procedural | Yes |
| `…/VERSION_1_EVIDENCE_REQUIREMENTS.md` | Version 1 Evidence Requirements | Evidence package law | Product Board | Framework | Yes |
| `knowledge/product/p003_1_version1_release_dossier/Version_1_RELEASE_DOSSIER.md` | Version 1 Release Dossier | Board evidence synthesis; **NO GO** | Product Board | Framework (synthesis, not gate law) | Yes (snapshot) |

### 3.6 Architecture & design law (Rank 5–6)

| Path | Title | Purpose | Owner | Level | Authoritative |
|---|---|---|---|---|---|
| `docs/ARCHITECTURE_CONSTITUTION.md` | Kwalitec Architecture Constitution | EOS structural law: determinism, layering, Twin, one runtime | Engineering Owner | Constitutional | Yes |
| `ARCHITECTURE.md` | Kwalitec — Architecture | Structural map (blueprints/services/engine/EOS) | Unstated | Framework | Yes |
| `docs/architecture/SYSTEM_ARCHITECTURE.md` | SYSTEM_ARCHITECTURE | Binding post-consolidation runtime map | Unstated | Framework | Yes |
| `docs/architecture/DIGITAL_TWIN_CONSTITUTION.md` | Constitution of the Kwalitec Digital Twin | Non-negotiable Twin implementation law | Unstated | Constitutional (sub-domain) | Yes |
| `DIGITAL_TWIN_PHILOSOPHY.md` | DIGITAL_TWIN_PHILOSOPHY | Why Twin exists; ethics; non-responsibilities | Unstated | Strategic | Yes |
| `knowledge/version2/DIGITAL_TWIN_PHILOSOPHY.md` | (V2 Twin philosophy) | V2 canonical Twin philosophy copy | Unstated | Strategic | Yes (prefer with V2 work) |
| `knowledge/architecture/DESIGN_PRINCIPLES.md` | Kwalitec Design Principles | Enduring design principles (ARCH-001) | Unstated | Framework | Yes |
| `docs/architecture/EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md` | Educational Intelligence Architecture | Epic 2 EI architecture (Twin, decisions, recommendations) | Unstated | Framework | Yes |
| `docs/DEPENDENCY_RULES.md` | Kwalitec Dependency Rules | Allowed EOS dependency directions | Unstated | Framework | Yes |
| `docs/adr/README.md` | ADR Index | EOS ADR index (primary) | Engineering Owner | Framework | Yes |
| `docs/adr/ADR-008-ai-enrichment-boundary.md` | ADR-008 — AI Enrichment Boundary | AI only as enrichment; forbidden as educational brain | Engineering Owner | Framework | Yes |
| `knowledge/version2/V2_DESIGN_MANIFESTO.md` | Version 2 Design Manifesto | V2 conscience: outcomes over engagement | Unstated | Strategic | Yes |
| `knowledge/version2/EDUCATIONAL_PRINCIPLES.md` | Version 2 Educational Principles | Binding V2 Learning Journey rules | Unstated | Framework | Yes |
| `knowledge/version2/education/INSTRUCTIONAL_PRINCIPLES.md` | Instructional Principles | Teaching-strategy selection principles | Unstated | Framework | Yes |

### 3.7 Study Sensei, product principles, decision philosophy (ILE)

| Path | Title | Purpose | Owner | Level | Authoritative |
|---|---|---|---|---|---|
| `knowledge/product/STUDY_SENSEI_PHILOSOPHY.md` | Study Sensei Philosophy | Trusted-guide identity vs content/AI tutor (ILE-010) | Unstated | Strategic | Yes |
| `knowledge/product/PRODUCT_PRINCIPLES.md` | Kwalitec Product Principles | Eight ILE-000 decision filters | Unstated | Framework | Yes |
| `knowledge/product/EDUCATIONAL_PHILOSOPHY.md` | Educational Philosophy | Product-level learning beliefs (ILE) | Unstated | Strategic | Yes |
| `knowledge/product/USER_EXPERIENCE_PHILOSOPHY.md` | User Experience Philosophy | Desired student feelings / design questions | Unstated | Strategic | Yes |
| `knowledge/product/DECISION_MAKING_PRINCIPLES.md` | Decision-Making Principles | When to suggest / wait / challenge / reassure | Unstated | Strategic | Yes |
| `knowledge/product/STUDENT_DECISION_FRAMEWORK.md` | Student Decision Framework | Student vs platform agency model (ILE-011) | Unstated | Framework | Yes |
| `knowledge/product/DECISION_CATALOGUE.md` | Decision Catalogue | Major learner decisions | Unstated | Supporting | Yes |
| `knowledge/product/GUIDANCE_RESPONSIBILITY_MATRIX.md` | Guidance Responsibility Matrix | Who decides vs recommends | Unstated | Framework | Yes |
| `knowledge/product/DECISION_CONFIDENCE_MODEL.md` | Decision Confidence Model | Evidence levels before guidance | Unstated | Framework | Yes |
| `knowledge/product/SILENCE_PRINCIPLE.md` | Silence Principle | When to stay quiet | Unstated | Strategic | Yes |
| `knowledge/product/DECISION_LIFECYCLE.md` | Decision Lifecycle | Observe→guide→act→reflect | Unstated | Framework | Yes |
| `knowledge/product/GUIDANCE_OVER_CONTENT.md` | Guidance Over Content | Amplify external resources | Unstated | Strategic | Yes |
| `knowledge/product/STUDENT_RELATIONSHIP_MODEL.md` | Student Relationship Model | Long-term learner relationship | Unstated | Strategic | Yes |
| `knowledge/product/NON_GOALS.md` | Non-Goals | Explicit product non-goals | Unstated | Strategic | Yes |

### 3.8 Strategy, roadmaps, trust, monetisation

| Path | Title | Purpose | Owner | Level | Authoritative |
|---|---|---|---|---|---|
| `knowledge/product/PRODUCT_STRATEGY.md` | Kwalitec Product Strategy | Post-platform ILE strategic direction | Unstated | Strategic | Yes |
| `knowledge/product/PRODUCT_ROADMAP.md` | Product Roadmap — Intelligent Learning Experience | ILE programme sequencing | Product Board may reorder | Strategic | Yes |
| `knowledge/product/roadmap/VERSION2_PRODUCT_STRATEGY.md` | VERSION2_PRODUCT_STRATEGY | Post-RC2 V2 evidence-driven strategy | Unstated | Strategic | Yes |
| `knowledge/product/PRODUCT_TRUST_PROGRAMME.md` | Product Trust Programme Blueprint | Master trust roadmap (PTP-000) | Unstated | Strategic | Yes (partially absorbed by P-001.x / EP-008) |
| `knowledge/product/MONETISATION_STRATEGY.md` | Monetisation Strategy | Commercial model strategy | Unstated | Strategic | Yes |

### 3.9 Product Board, founder ops, registers (P-003.x / GP-001)

| Path | Title | Purpose | Owner | Level | Authoritative |
|---|---|---|---|---|---|
| `knowledge/product/gp001_founder_governance_model/FOUNDER_GOVERNANCE_MODEL.md` | Founder Governance Model | Founder-operated multi-capacity model | Founder | Procedural | Yes |
| `…/ROLE_MAPPING.md` | Role Mapping | Capacity → role mapping | Founder | Supporting | Yes |
| `…/UPDATED_APPROVAL_MATRIX.md` | Updated Approval Matrix | Material approval matrix | Founder | Procedural | Yes |
| `knowledge/product/p003_7_product_board_charter/PRODUCT_BOARD_CHARTER.md` | Product Board Charter | Board mission; V1 GO/NO GO recommendation authority | Product Board / Founder Chair | Procedural | Yes |
| `…/DECISION_PROCESS.md` | Decision Process | Board decision procedure | Product Board | Procedural | Yes |
| `…/RELEASE_DECISION_PROCESS.md` | Release Decision Process | Release-specific board process | Product Board | Procedural | Yes |
| `…/EVIDENCE_REVIEW_PROCESS.md` | Evidence Review Process | Board evidence review | Product Board | Procedural | Yes |
| `…/CHANGE_CONTROL.md` | Change Control | Board change control | Product Board | Procedural | Yes |
| `…/MEETING_CADENCE.md` | Meeting Cadence | Cadence | Product Board | Procedural | Yes |
| `…/BOARD_ROLES_AND_RESPONSIBILITIES.md` | Board Roles | Roles (capacities under GP-001) | Product Board | Procedural | Yes |
| `knowledge/product/p003_2_product_decision_register/PRODUCT_DECISION_REGISTER.md` | Product Decision Register | Canonical DR-NNN cards | Product Board | Framework | Yes |
| `knowledge/product/p003_3_product_risk_register/PRODUCT_RISK_REGISTER.md` | Product Risk Register | PR risks | Product Board | Framework | Yes |
| `knowledge/product/p003_4_product_assumption_register/PRODUCT_ASSUMPTION_REGISTER.md` | Product Assumption Register | Assumptions | Product Board | Framework | Yes |
| `knowledge/product/p003_5_evidence_hierarchy/EVIDENCE_HIERARCHY.md` | Evidence Hierarchy | E1–E5 claim evidence levels | Product Board | Framework | Yes |
| `knowledge/product/p003_6_product_maturity_model/PRODUCT_MATURITY_MODEL.md` | Product Maturity Model | Organisational capability maturity | Product Board | Framework | Yes |
| `knowledge/product/p003_8_version1_exit_criteria/VERSION1_EXIT_CRITERIA.md` | Version 1 Exit Criteria | Board synthesis of exit readiness | Product Board | Framework (synthesis) | Yes |

### 3.10 Engineering, quality, release, readiness (Ranks 7–10)

| Path | Title | Purpose | Owner | Level | Authoritative |
|---|---|---|---|---|---|
| `knowledge/ENGINEERING_STANDARDS.md` | Kwalitec Engineering Standards | Permanent PR bar / DoD themes | Engineering Owner | Framework | Yes |
| `docs/ENGINEERING_CHARTER.md` | Kwalitec Engineering Charter | Engineering philosophy / mission | Engineering Owner | Strategic | Yes |
| `knowledge/QUALITY_MANUAL.md` | Kwalitec Quality Manual | a11y, perf, security, release quality policy | Engineering Owner | Framework | Yes |
| `knowledge/RELEASE_PLAYBOOK.md` | Kwalitec Release Playbook | Operator release summary; mandates EVF + P-002.1 | Operations Owner | Operational | Yes |
| `docs/process/RELEASE_PROTOCOL.md` | Kwalitec Release Protocol | Canonical detailed release procedure | Operations Owner | Operational | Yes |
| `knowledge/engineering/RELEASE_PROTOCOL.md` | Release Protocol | Engineering release *contract* / gates | Engineering Owner | Framework | Yes |
| `knowledge/VERSION_1_READINESS.md` | Version 1.0 Readiness | Tracker reflecting P-002.1 evidence | Product Board | Operational | Yes |
| `docs/production/VERSIONING_POLICY.md` | Versioning Policy | Semver policy | Unstated | Procedural | Yes |
| `docs/production/RELEASE_PROCESS.md` | Release Process | Production release process | Unstated | Operational | Yes |
| `docs/ga/RELEASE_CHECKLIST.md` | GA Release Checklist | GA operational checklist | Unstated | Operational | Yes |
| `docs/release/V2_RELEASE_CHECKLIST.md` | Version 2 Release Checklist | V2.0.0 verification | Unstated | Operational / Historical | Contextual |
| `knowledge/release/RELEASE_CHECKLIST.md` | Release Checklist | V1 programme trail checklist | Unstated | Operational | Contextual |
| `knowledge/release/KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` | Version 1 Release Certification | Formal V1R-001 certification (2026-07-15) | Unstated | Historical | **Historical** — superseded in *practice* by P-002.1 + dossier for production-ready claims |
| `CONTRIBUTING.md` | Contributing to Kwalitec | Git/PR/milestone workflow | Unstated | Procedural | Yes |

### 3.11 Brand, language, orientation

| Path | Title | Purpose | Owner | Level | Authoritative |
|---|---|---|---|---|---|
| `knowledge/design/BRAND_GUIDELINES.md` | Kwalitec Brand Guidelines | Brand mission, visual identity | Unstated | Strategic (brand) | Yes |
| `knowledge/design/UI_UX_IMPLEMENTATION_STANDARD.md` | UI/UX Implementation Standard | UI implementation law | Unstated | Framework | Yes |
| `PROJECT_CONTEXT.md` | Kwalitec — Project Context | Primary orientation for developers/agents | Unstated | Supporting | Yes |
| `knowledge/README.md` | Knowledge Base index | Knowledge organisation | Unstated | Supporting | Yes |
| `UBIQUITOUS_LANGUAGE.md` | Ubiquitous Language | Canonical domain terms | Unstated | Framework | Yes |
| `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` | Product Language Guide | Learner-facing terminology | Unstated | Framework | Yes |
| `knowledge/prd/PRD_TEMPLATE.md` | PRD Template | Feature proposal template | Unstated | Procedural | Yes |

### 3.12 Orchestration (Programme VII) — cluster

**Index:** `knowledge/orchestration/README.md`

| Cluster | Representative authority | Purpose | Level | Authoritative |
|---|---|---|---|---|
| Workflows | `workflows/EDUCATIONAL_WORKFLOW_MODEL.md` | How educational decisions flow | Framework | Yes |
| Authority | `authority/AUTHORITY_PRINCIPLES.md`, `EDUCATIONAL_AUTHORITY_MODEL.md` | Who owns which educational decisions | Framework | Yes |
| Conflict | `conflict_resolution/CONFLICT_RESOLUTION_FRAMEWORK.md` | Conflict resolution | Framework | Yes |
| Recommendations | `recommendations/RECOMMENDATION_STRUCTURE.md` (+ assembly/explainability) | Lawful recommendation structure | Framework | Yes |
| State | `state/EDUCATIONAL_STATE_MODEL.md` | Constitutional educational context | Framework | Yes |

All subordinate to EGI-001 and Programme VI. Overlaps intentionally with P-001.3 (product quality) and Student Decision Framework (agency philosophy).

### 3.13 Constitutional meta-corpora (Programmes VIII–X) — cluster

Large Model → Lifecycle → Completion trees under `knowledge/integration/`, `conformance/`, `verification/`, `compliance/`, `certification/`, `evolution/`, `audit/`, `decision/`, `execution/`, `execution_engine/`, `explainability/`, `runtime/`.

| Field | Value |
|---|---|
| Purpose | Constitutional integrity, conformance, verification, compliance, certification, evolution, execution architecture |
| Authority level | Framework (meta-constitutional documentation) |
| Dependencies | EGI-001; Architecture Constitution |
| Still authoritative | **Yes — governing documentation**; not student-facing product law and not a substitute for Vision / Educational Constitution / P-002.1 |
| Potential overlaps | Fragmentation risk — many leaves; hard for newcomers to locate Rank 1–10 authorities |

### 3.14 Agent enforcement (`.cursor/rules/`)

| Path | Role | Maps to | Authoritative |
|---|---|---|---|
| `00-engineering.mdc` | Engineering philosophy | ENGINEERING_STANDARDS, PROJECT_CONTEXT | Yes (agent) |
| `00-CONSTITUTION.md` | Architecture constitution digest | ARCHITECTURE_CONSTITUTION | Yes (agent) |
| `01-architecture.mdc` | Layering invariants | GOVERNANCE / ARCHITECTURE | Yes (agent) |
| `10-security.mdc` | Security rules | Quality / security policy | Yes (agent) |
| `06-git.mdc` | Git workflow | CONTRIBUTING | Yes (agent) |
| `07-reporting.mdc` | Completion report sections | GOVERNANCE §4 | Yes (agent) |
| `blind-review-framework.mdc` | Blind review execution | reviewer_framework | Yes (agent) |

### 3.15 Misnamed / dual-purpose documents

| Path | Title | Purpose | Level | Authoritative | Note |
|---|---|---|---|---|---|
| `knowledge/product/ep001_product_validation/EDUCATIONAL_VALIDATION_FRAMEWORK.md` | Educational Validation Framework | Learning-outcome metrics / instrumentation (EP-001) | Framework (metrics) | Yes for metrics | **Not** Programme V EVF; name collision |
| `knowledge/product/ep001_product_validation/V1_EXIT_CRITERIA.md` | V1 Exit Criteria (EP-001) | Pre-board exit criteria | Historical | No for current board law | Superseded by P-003.8 + P-002.1 |

### 3.16 Evidence programmes (not law)

Validated KSI / perception / trust programmes under `knowledge/product/ep005_*` … `ep008_*`, Blind Review under `ep004_private_beta/reviewer_framework/`, and ~79 `COMPLETION_REPORT.md` files are **evidence and delivery records**. They feed P-002.1 / Product Board claims; they do not redefine Rank 1–10 law unless a framework explicitly elevates them.

---

## 4. Release governance review (summary)

See also § Release in `GOVERNANCE_HIERARCHY.md` and completeness table in `GOVERNANCE_RECOMMENDATIONS.md`.

| Topic | Existing authority | Completeness |
|---|---|---|
| Release philosophy | Vision Final Test + Blueprint promise + EVF question + P-002.1 purpose | **Covered** |
| Release gates (educational) | EVF Educational Release Gate + Standard | **Covered** |
| Release gates (Version 1 production-ready) | P-002.1 G1–G12 | **Covered** |
| Student trust gates | EVF 80% trust target; KSI K categories; Evidence Hierarchy claim levels | **Covered** (multiple lenses — intentional) |
| Quality gates | Quality Manual + Engineering Standards + P-001.2/1.3 reviews | **Covered** |
| Version definitions / versioning | VERSIONING_POLICY + Blueprint / V2 strategy | **Covered** |
| Production readiness | P-002.1 + Playbook + Protocol + Readiness tracker + Dossier | **Covered** |
| Version 1 framework | P-002.1 + companions + P-003.1 dossier + P-003.8 exit criteria | **Complete as law**; declaration blocked on evidence (G1 FAIL) |

---

## 5. How to use this audit

1. Before proposing a new governance programme (GP-*, constitution, release framework, philosophy pack), search this catalogue and `GOVERNANCE_OVERLAP_MATRIX.md`.  
2. Prefer amending or cross-linking an existing Rank 1–10 document over creating a peer authority.  
3. Treat constitutional meta-corpora (Programmes VIII–X) as specialised integrity law — not as replacements for Vision / Educational Constitution / P-002.1.  
4. Treat completion reports as evidence, not hierarchy amendments.

---

**End of inventory.** Companions: hierarchy, overlap matrix, gap analysis, recommendations, completion report.
