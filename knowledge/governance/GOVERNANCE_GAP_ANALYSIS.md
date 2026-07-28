# Governance Gap Analysis

**Audit date:** 2026-07-28  
**Rule:** Report a gap only if no equivalent authority exists and no higher-level document already covers it.  
**Bias:** Prefer “already covered” over inventing documents that similar products might have.

---

## 1. Verdict

**No missing apex governance documents** were found for Vision, Educational Constitution, Architecture Constitution, Product Blueprint, Version 1 Release Framework, EVF, KSI, Explainability/Recommendation product standards, Product Board, Founder operating model, Engineering Standards, or Release Playbook/Protocol.

Remaining items are **navigation, naming, and consolidation gaps** — not absence of law.

---

## 2. Gaps that are *not* gaps (already covered)

| Apparent need | Already covered by | Why not a gap |
|---|---|---|
| Company mission / vision | Vision 2030 + Blueprint purpose | Apex exists |
| Educational constitution | `KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Apex exists |
| Product constitution | Vision 2030 (executive product constitution) | Apex exists |
| Release philosophy | Vision Final Test + EVF purpose + P-002.1 purpose + Playbook | Covered across ranks |
| Release / quality / trust gates | EVF Gate; P-002.1 G1–G12; Quality Manual; P-001.2/1.3 | Covered |
| Version 1 definition & readiness declaration | P-002.1 + dossier + exit criteria + readiness tracker | Covered |
| AI governance / ethics | ADR-008; Vision never-build; Twin Philosophy; Engineering Standards | Covered without a separate charter |
| Student trust | EVF trust target; Evidence Hierarchy; Product Trust Programme; EP-008 | Covered |
| Recommendation principles | Programme VII + P-001.3 + ILE decision pack | Covered |
| Study Sensei philosophy | ILE-010 | Covered |
| Student decision framework | ILE-011 | Covered |
| Product Board | P-003.7 | Covered |
| Decision registers | P-003.2 (+ risks/assumptions) | Covered |
| Founder / operating governance | GP-001 + GOVERNANCE.md | Covered |
| Brand principles | Brand Guidelines | Covered |
| Non-goals | Vision never-build + NON_GOALS.md | Covered |
| Engineering / architecture principles | Architecture Constitution; Design Principles; Engineering Charter/Standards | Covered |
| Capability validation | EVF Capability Validation Guide + EI Architecture | Covered |

Creating peer documents for the rows above would **duplicate** existing authority.

---

## 3. Genuine gaps (authority or clarity)

### G-01 — Canonical index for ILE philosophy pack (navigation)

| Field | Value |
|---|---|
| Gap type | Navigation / discoverability |
| Missing | A single index (under GOVERNANCE or `knowledge/product/`) listing Sensei, Student Decision Framework, Principles, Non-Goals, Silence, etc., and their relation to Ranks 1–3 |
| Why genuine | Documents exist and are Active, but GOVERNANCE.md Rank table does not list them; newcomers may invent parallel philosophy docs |
| Equivalent authority? | Content exists; **index authority** is weak |
| Higher doc cover? | Partially via Vision/Blueprint links inside each file |
| Recommended response class | Cross-link / index only — **not** a new constitution |

### G-02 — Disambiguation of “Educational Validation Framework” (naming)

| Field | Value |
|---|---|
| Gap type | Naming collision |
| Missing | Explicit subordination / rename of EP-001 metrics document relative to Programme V EVF |
| Why genuine | Two Active documents share the framework name for different questions |
| Equivalent authority? | Both exist; clarity does not |
| Higher doc cover? | GOVERNANCE asserts Programme V for release gates |
| Recommended response class | Cross-link / optional rename in a future docs programme — **not** a new EVF |

### G-03 — Single “start here” for ship / release claims (navigation)

| Field | Value |
|---|---|
| Gap type | Navigation across intentional multi-layer release stack |
| Missing | One short map from claim type → required gate (EVF vs P-002.1 vs GA checklist vs operator Protocol) |
| Why genuine | Law is complete; operators may pick the wrong checklist |
| Equivalent authority? | Pieces exist in Playbook / P-002.1 / EVF README |
| Higher doc cover? | Partially |
| Recommended response class | Add map to RELEASE_PLAYBOOK or GOVERNANCE — **not** a new release framework |

### G-04 — Historical V1 certification vs production-ready declaration (clarity)

| Field | Value |
|---|---|
| Gap type | Status clarity |
| Missing | Persistent reader warning that V1R-001 / early certification trails do not satisfy P-002.1 declaration |
| Why genuine | Numeric/date proximity creates false “already released” reading |
| Equivalent authority? | P-002.1 is clear; historical doc status may be under-signalled |
| Recommended response class | Status banner / cross-link in a future docs pass — **not** new gates |

### G-05 — Constitutional meta-corpus entry map (navigation)

| Field | Value |
|---|---|
| Gap type | Fragmentation / discoverability |
| Missing | A short “these trees are *below* Educational + Architecture Constitutions” map for Programmes VIII–X |
| Why genuine | Volume creates illusion of missing product governance or competing apexes |
| Equivalent authority? | Trees are authoritative specialised law |
| Recommended response class | Index under knowledge README / GOVERNANCE supporting indexes — **not** a new apex constitution |

### G-06 — Standalone company ethics / AI ethics charter (optional consolidation only)

| Field | Value |
|---|---|
| Gap type | Optional consolidation — **not required** |
| Missing | Single ethics charter document |
| Why listed | External readers may expect one file |
| Equivalent authority? | **Yes** — Vision, Twin Philosophy, ADR-008, Educational Constitution integrity articles |
| Higher doc cover? | **Yes** |
| Recommended response class | **Do not create** unless a Product Board programme explicitly wants a reader-facing digest that only *points* to existing law |

### G-07 — Mission statement as separate corporate artefact

| Field | Value |
|---|---|
| Gap type | Not a gap |
| Note | Mission prose lives inside Vision 2030; Blueprint clarifies “Mission” domain term vs company purpose |
| Recommended response class | None |

### G-08 — Independent second-assessor organisational model

| Field | Value |
|---|---|
| Gap type | Known organisational residual (PR-027 / DR-054) — not document absence |
| Missing | Multi-person separation of duties at scale |
| Why not a docs gap | GP-001 explicitly defers independent separation until organisational scale; evidence requirements unchanged |
| Recommended response class | Do not invent paper independence; follow existing risk/decision registers |

---

## 4. Gaps explicitly rejected by this audit

The following were considered and **rejected** as reasons to create new governance programmes:

- Second Product Vision or “Company Constitution”  
- Second Educational Constitution or “Learning Ethics Constitution”  
- Second Version 1 Release Framework or “Production Readiness Constitution”  
- Second Product Board Charter  
- Second Founder Governance Model (or a new GP-001 with overlapping purpose)  
- Standalone Recommendation Constitution (P-001.3 + Programme VII suffice)  
- Standalone Student Trust Constitution (EVF + Evidence Hierarchy + PTP suffice)  
- New Decision Framework replacing ILE-011  
- New Architecture Principles replacing Architecture Constitution / Design Principles  

---

## 5. Release governance completeness (gap lens)

| Topic | Gap? | Notes |
|---|---|---|
| Release philosophy | No | Multi-doc but complete |
| Release gates | No | EVF + P-002.1 |
| Version definitions | No | Versioning policy + frameworks |
| Student trust gates | No | EVF + claim hierarchy |
| Quality gates | No | Quality Manual + engineering + P-001.x |
| Production readiness | No | P-002.1 complete as law; evidence incomplete (G1 FAIL) — **evidence gap, not governance gap** |
| Version 1 framework | No | P-002.1 complete |

**Important distinction:** Open Version 1 **gates** (e.g. G1 FAIL) are product/evidence deficits. They are not missing governance documents.

---

## 6. Priority for future work (non-implementation)

| Priority | Gap ID | Action class |
|---|---|---|
| P1 | G-02 | Naming / cross-link EVF vs EP-001 |
| P1 | G-04 | Historical vs P-002.1 declaration clarity |
| P2 | G-03 | Ship-claim start-here map |
| P2 | G-01 | ILE philosophy index |
| P3 | G-05 | Meta-constitutional navigation map |
| Reject | G-06 / G-07 | No new charter / mission doc |

Any future GP-* programme must: (1) cite this audit, (2) state which gap ID it closes, (3) prove no existing Rank 0–10 document already owns the question.
