# Governance Overlap Matrix

**Audit date:** 2026-07-28  
**Purpose:** Identify duplicate concepts, near-duplicates, contradictions, missing cross-links, fragmentation, and obsolete posture — without deleting documents.

Legend: **D** duplicate concept · **N** near-duplicate · **C** complementary (intentional) · **X** contradictory risk · **F** fragmented · **H** historical / superseded practice · **L** needs stronger cross-link

---

## 1. Concept matrix (high-signal)

| Concept | Primary authority | Secondary / specialised | Relation | Notes |
|---|---|---|---|---|
| Why / north star / never-build | Vision 2030 | Blueprint (strategy); NON_GOALS; Study Sensei | C | Vision wins on philosophy conflict |
| Product strategy / audiences / roadmap | Blueprint | PRODUCT_STRATEGY; PRODUCT_ROADMAP; VERSION2_PRODUCT_STRATEGY | N / C | Blueprint remains Rank 2; ILE/V2 docs elaborate horizons |
| Educational meaning / mastery / truth | Educational Constitution (EGI-001) | EIP suite; Programme VI; V2 Educational Principles | C | V2 principles specialise, must not contradict |
| Educational philosophy (product prose) | Educational Constitution Art. II | `EDUCATIONAL_PHILOSOPHY.md` (ILE) | N / L | Product doc should explicitly defer to Constitution articles |
| Educational release quality / trust | EVF Programme V | Blind Review; KSI (usefulness index) | C | Different questions: trust-to-release vs KSI usefulness |
| “Educational Validation Framework” name | `knowledge/educational_validation/` | `ep001…/EDUCATIONAL_VALIDATION_FRAMEWORK.md` | D (name) | **Different purposes** — metrics vs release gate |
| Explainability | EIP-003 Educational Explainability Standard | P-001.2 Explainability Standard; orchestration explainability; constitutional explainability architecture | C / F | GOVERNANCE notes intentional specialisation; many leaves |
| Recommendations | Programme VII recommendation models | P-001.3 Quality Standard + Decision Framework; EP-008 trust programmes | C / F | Structure vs quality vs delivery evidence |
| Decision / agency / silence | Student Decision Framework (ILE-011) | Decision-Making Principles; Orchestration authority / conflict; Recommendation Decision Framework | C / N | Three “decision” vocabularies — agency vs tip priority vs educational ownership |
| Version 1 production-ready | P-002.1 G1–G12 | P-003.1 Dossier; P-003.8 Exit Criteria; VERSION_1_READINESS | C | Tracker / synthesis must not amend gates |
| Pre-P-002.1 V1 certification | — | `KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` | H | Historical SUBMITTED record; not current declaration law |
| EP-001 V1 exit criteria | — | `ep001…/V1_EXIT_CRITERIA.md` | H | Superseded by P-003.8 + P-002.1 |
| Release procedure | `docs/process/RELEASE_PROTOCOL.md` | RELEASE_PLAYBOOK; `engineering/RELEASE_PROTOCOL.md`; production RELEASE_PROCESS; multiple checklists | C / F / L | Three-layer stack intentional; checklist locations proliferate |
| Architecture law | Architecture Constitution | DESIGN_PRINCIPLES; ARCHITECTURE.md; SYSTEM_ARCHITECTURE; 00-CONSTITUTION.md | C | Digest vs law vs map — clear if Constitution cited first |
| Twin philosophy | Twin Constitution + Philosophy | Root + `knowledge/version2/` copies | N / L | Prefer one canonical pointer for readers |
| AI boundary / ethics | ADR-008; Vision never-build; Twin Philosophy | ENGINEERING_STANDARDS § AI; agent rules | C | No single “AI Ethics Charter” — covered across docs |
| Student trust | EVF trust bar; Evidence Hierarchy; Product Trust Programme; EP-008 | Brand / UX philosophy | C / F | Multiple programmes; PTP partially absorbed |
| Engineering principles | ENGINEERING_CHARTER | ENGINEERING_STANDARDS; 00-engineering.mdc | C / N | Charter = philosophy; Standards = PR bar |
| Product Board vs Founder | P-003.7 Charter | GP-001 Founder model | C | Capacities concentrated; evidence unchanged (DR-054 / PR-027) |
| Capability definitions | Capability Validation Guide; EI Architecture; docs/architecture CAPABILITY_* | Educational Logic Registry | F | Capability IDs span educational validation and engineering docs |
| Brand principles | Brand Guidelines | UI/UX Implementation Standard; PX branding reports | C | Adequate |
| Monetisation | MONETISATION_STRATEGY | Blueprint commercial notes | C | No conflict found in audit scope |
| Constitutional meta-law | EGI-001 / Architecture Constitution | Programmes VIII–X integration/conformance/… trees | F / L | Authoritative but hard to navigate; risk of treating leaf models as product apex |

---

## 2. Duplicate concepts (same question answered twice)

| ID | Duplicate | Documents | Severity | Audit note |
|---|---|---|---|---|
| DUP-01 | Name “Educational Validation Framework” | Programme V folder vs EP-001 metrics doc | High (confusion) | Purposes differ; naming collides |
| DUP-02 | Title “Release Protocol” | `docs/process/` vs `knowledge/engineering/` | Medium | Intentional split (procedure vs gate contract) — needs explicit “see also” if missing |
| DUP-03 | Twin philosophy presence | Repo root + `knowledge/version2/` | Medium | Near copies; canonical for V2 work should be version2 path |
| DUP-04 | Educational Constitution filename | `KWALITEC_…` + alias `EDUCATIONAL_CONSTITUTION.md` | Low | Alias intentional |
| DUP-05 | V1 exit / readiness synthesis | P-003.8, P-003.1, VERSION_1_READINESS, historical EP-001 exit | Medium | Active trio is intentional; EP-001 exit is historical |

**Do not delete** these without a dedicated supersession programme. Prefer rename/cross-link for DUP-01.

---

## 3. Near-duplicates (related filters)

| ID | Topic | Documents | Guidance |
|---|---|---|---|
| ND-01 | Never-build vs non-goals | Vision 2030 § never-build; `NON_GOALS.md` | Vision is higher; NON_GOALS expands for roadmap |
| ND-02 | Product strategy horizon docs | Blueprint; PRODUCT_STRATEGY; PRODUCT_ROADMAP; VERSION2_PRODUCT_STRATEGY | Blueprint owns Rank 2; others are horizon elaborations |
| ND-03 | Sensei vs Vision mission prose | Vision; Study Sensei; Guidance Over Content | Complementary identity layer |
| ND-04 | Decision frameworks | Student Decision Framework; Recommendation Decision Framework; Orchestration authority/conflict; planning_engine DECISION_* | Different scopes — keep; strengthen “which decision doc?” map |
| ND-05 | Explainability corpora | EIP-003; P-001.2; orchestration / constitutional explainability trees | Keep specialisation; avoid new explainability constitutions |
| ND-06 | Engineering philosophy | ENGINEERING_CHARTER; ENGINEERING_STANDARDS; cursor rules | Keep; Charter should remain philosophy-only |

---

## 4. Contradictory guidance (observed / residual risk)

| ID | Topic | Observation | Severity |
|---|---|---|---|
| CX-01 | Version 1 “released” language | Historical V1R-001 certification SUBMITTED (2026-07-15) vs current P-002.1 board **NO GO** / G1 FAIL | Medium — readers may confuse certification trail with production-ready declaration |
| CX-02 | Role language vs GP-001 | Multi-person role names in older docs vs founder capacity model | Low if GOVERNANCE §1a / GP-001 cited; residual PR-027 |
| CX-03 | Estimated ΔKSI vs validated KSI | Some programme reports cite estimated contribution; P-002.1 G1 requires validated KSI | Controlled by GOVERNANCE notes — residual risk if ignored |
| CX-04 | EVF 80% trust vs KSI ≥ 80 | Same numeric “80” for different indices | Medium confusion risk — not a logical contradiction if labelled correctly |

No hard conflict found between Vision 2030 and Educational Constitution in this audit. Hierarchy STOP rule is the resolution mechanism.

---

## 5. Documents that should reference each other (missing or weak links)

| From | To | Why |
|---|---|---|
| EP-001 `EDUCATIONAL_VALIDATION_FRAMEWORK.md` | `knowledge/educational_validation/README.md` | Disambiguate name and purpose |
| `NON_GOALS.md` | Vision 2030 never-build section | Explicit subordination |
| `EDUCATIONAL_PHILOSOPHY.md` | Educational Constitution Article II | Avoid parallel philosophy apex |
| Twin philosophy (root) | `knowledge/version2/DIGITAL_TWIN_PHILOSOPHY.md` + Twin Constitution | Canonical pointer |
| Multiple release checklists | RELEASE_PLAYBOOK + P-002.1 + EVF Gate | Single “start here” for ship decisions |
| Constitutional meta README trees | GOVERNANCE.md Rank table | Prevent treating leaf models as Rank 1 |
| ILE-011 Student Decision Framework | P-001.3 Recommendation Decision Framework | Clarify agency vs tip prioritisation |
| PRODUCT_TRUST_PROGRAMME | P-001.2 / P-001.3 / EP-008 / EVF | Show absorption / remaining scope |

(Exact presence of links may vary; this list flags **audit-priority** relationships.)

---

## 6. Obsolete / historical posture

| Document / cluster | Status | Recommendation class |
|---|---|---|
| `knowledge/release/KWALITEC_VERSION1_RELEASE_CERTIFICATION.md` | Historical SUBMITTED | Retain as trail; label readers toward P-002.1 for declaration |
| `ep001…/V1_EXIT_CRITERIA.md` | Superseded by P-003.8 + P-002.1 | Retain; mark superseded in future docs work (out of this audit’s modify scope) |
| RC / V2_023 release candidate anchors | Historical | Keep as SYSTEM_ARCHITECTURE provenance |
| Programme completion reports | Evidence | Never treat as hierarchy law |
| PRODUCT_TRUST_PROGRAMME | Active programme map; partially absorbed | Do not delete; clarify residual vs delivered standards |

**Deletion:** Not recommended by this audit except where a future programme proves a document is pure duplicate *and* already superseded with redirects.

---

## 7. Fragmentation patterns

| Area | Symptom | Effect |
|---|---|---|
| Constitutional meta-corpora (VIII–X) | Hundreds of Model/Lifecycle/Completion leaves | Discovery cost; false “missing constitution” perception |
| Explainability | Educational + product + orchestration + constitutional trees | Newcomers propose yet another standard |
| Release checklists | `docs/ga`, `docs/release`, `knowledge/release`, Playbook, Protocol | Unclear which checklist binds which claim |
| ILE philosophy pack | Many short permanent filters (Sensei, silence, confidence, …) | Strong coverage; needs index under GOVERNANCE or product README |
| Capability docs | Validation guide vs architecture CAPABILITY_* specs | “Capability” overloaded |

Fragmentation ≠ absence of authority. Hierarchy is defined; **navigation** is the weakness.

---

## 8. Overlap with GP-001 / future GP programmes

| Finding | Implication |
|---|---|
| GP-001 Founder Governance Model **already exists** and is indexed in GOVERNANCE.md §1a / §7 | A new programme also named GP-001 would be a **duplicate ID** |
| Approval matrix, role mapping, capacity model already defined | Do not recreate founder operating model |
| Product Board Charter (P-003.7) already defines board procedure | Do not recreate board constitution |
| Any future GP-* must cite this audit and either amend GP-001 / GOVERNANCE.md or use a new ID with a non-overlapping purpose | Success criterion of this audit |

---

## 9. Summary counts (qualitative)

| Category | Assessment |
|---|---|
| True missing apex authorities | **None identified** |
| High-severity naming collisions | **1** (EVF vs EP-001) |
| Intentional complementary stacks | **Many** (explainability, recommendations, release layers) |
| Historical supersession risks | **Several** (V1 certification / EP-001 exit) |
| Fragmentation hotspots | Meta-constitutional trees; release checklists; explainability |
