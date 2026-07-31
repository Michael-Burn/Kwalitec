# Version 1 Release Criteria

**Programme:** V1S-001 / V1S-002 / V1S-003 / V1S-004 / V1S-005 / V1S-006 / V1S-007 — Version 1 Stabilisation  
**Status:** Active — dogfooding gate checklist  
**Effective:** 2026-07-31  
**Authority:** V1S-001 · V1S-002 · V1S-003 · V1S-004 · V1S-005 · V1S-006 · V1S-007 · `PRODUCT_BLUEPRINT.md` · P-002.1 Version 1 Release Framework  
**Does not:** Declare production-ready by itself. Production-ready still requires P-002.1 gates G1–G12.

Every requirement below is **checkable**. Mark **PASS** / **FAIL** / **HOLD** with evidence path.

---

## How to use

1. Run internal dogfooding against Adaptive Study Workspace (Home).
2. For each criterion, record PASS / FAIL / HOLD and a one-line evidence note.
3. Dogfooding **GO** requires all **Educational**, **Product**, and **Architecture** hard criteria PASS or approved HOLD.
4. **Commercial launch** additionally requires P-002.1 G1–G12 and this document’s Commercial + Launch sections.

---

## 1. Educational

| ID | Requirement | Check | Hard? |
|---|---|---|---|
| E1 | Learning Episodes never paste raw CMP / syllabus dump language | Spot-check 10 authored episodes across CS1/CB2/CM1; `looks_like_cmp_dump` + human review | Yes |
| E2 | Each Learning Episode has one clear learning objective | Episode DTO `learning_objective` non-empty and ≤160 chars; not topic-title-only concatenation | Yes |
| E3 | Educational context explains why today matters | Context references foundation / successor / recent work when graph data exists | Yes |
| E4 | Success criteria are meaningful and countable | 2–4 criteria; actionable verbs (explain / solve / complete) | Yes |
| E5 | Natural transitions within mission arc | Morning Brief → Learning Episode → Checkpoint → Reflection → Tomorrow Preview order on Home | Yes |
| E6 | Tomorrow continuity is present when next topic known | Tomorrow Preview shows topic + continuity line when available | Yes |
| E7 | Extra Study offered only when spare capacity remains | Extra Study section absent when duration fills available minutes | Yes |
| E8 | No dual educational truths on one student path | Same enrolment never mixes JSON Runtime A mastery theatre with Runtime C evidence claims | Yes |
| E9 | Authorities consumed, not reimplemented, in presentation | Presentation uses `get_*_engine()` / composer; no inline strategy/diagnostic math | Yes |

---

## 2. Product

| ID | Requirement | Check | Hard? |
|---|---|---|---|
| P1 | One student product language | Copy uses Product Language Guide terms; no rejected synonyms on certified Home | Yes |
| P2 | Home answers “where you are, what to do today, where heading” | Adaptive Workspace sections present when data available | Yes |
| P3 | Consistent terminology across surfaces | Tomorrow Preview, Extra Study, Curriculum Map, Readiness Forecast, My Learning Journey labels match | Yes |
| P4 | Primary CTA hierarchy clear | One primary Mission/Session action; secondary links ghost/secondary | Yes |
| P5 | Empty / quiet / complete states are educational | Quiet and day-complete states use calm operational copy (no lorem/TODO) | Yes |
| P6 | Journey surfaces distinguishable | Syllabus **Journey** ≠ narrative **My Learning Journey**; Home teaser labelled accordingly | Yes |
| P7 | Study Sensei naming density respected | Sensei named once in Home hero chrome per product language policy | Hold OK |
| P8 | No developer / engine nouns in student copy | No “Strategy, Diagnostics, Difficulty, Effectiveness”, “coverage signal”, “runtime-c” labels | Yes |

---

## 3. Architecture

| ID | Requirement | Check | Hard? |
|---|---|---|---|
| A1 | Bundled JSON loader singularity | Only `CurriculumRepository.load_auto` detects V1/V2; delegates do not re-branch (`tests/test_curriculum_load_auto.py`) | Yes |
| A2 | On-disk curricula are V2 hierarchical | `app/curriculum/data/**/*.json` all V2; no shipped V1 JSON | Yes |
| A3 | Exactly one student curriculum authority | **PASS for dogfood cohort** when Runtime C enrolment is on and an active published package exists for CS1/CB2/CM1 (V1S-002 dogfood cutover). JSON_BUNDLED remains substrate/fallback only. Evidence: `effective_runtime_c_allowlist`, routing reason `dogfood_curriculum_cutover` | Yes* |
| A4 | Each educational authority has one owner | Authority Ownership Matrix in `runtime_ownership.py` / V1S-002 report — CLEAN or documented DEBT | Yes |
| A5 | No parallel Mission student spine | Production Home uses ERE + CertifiedMissionEngine + StudentRuntimeCoordinator (or documented sole Runtime A path) | Yes |
| A6 | Progress writes converge on ProgressEngine | Runtime C path uses ProgressEngine; legacy mastery paths flagged HOLD | Hold OK |
| A7 | Adaptive Workspace is presentation-only | `compose_adaptive_workspace` does not write Evidence/Progress/Twin | Yes |
| A8 | Educational Authoring owns composition only | Authoring never selects/reschedules missions | Yes |
| A9 | Educational Runtime Singularity | Every Runtime C student educational interaction executes through one Educational Runtime; SCI missing → ensure or readiness message — never Runtime A fallback (`ensure_active_sci`, V1S-007) | Yes |

\*A3 dogfood cohort cutover landed in V1S-002. Commercial launch still requires published packages for every claimed cohort subject (L2) and RI-002 before Runtime A hard removal.

---

## 4. Technical

| ID | Requirement | Check | Hard? |
|---|---|---|---|
| T1 | No student-visible TODO / Lorem / placeholder labels | Grep templates + VM output | Yes |
| T2 | Forbidden-term scrub on Adaptive Workspace guidance | `_scrub` / product language reject list active | Yes |
| T3 | Dead presentation components catalogued or removed | Latent cards listed in debt register with remove-or-wire decision | Hold OK |
| T4 | Opaque demo bridges not on dogfood path | Session composition uses real `LearningSessionRuntimeEngine` | Yes |
| T5 | Deprecate public V1-only `load_curriculum` for new callers | Docstring + no new production callers | Hold OK |
| T6 | MissionEngineV2 unwired from production | No non-test `app/` consumer of MissionEngineV2 on student spine; package marked ARCHIVE (V1S-002) | Yes |
| T7 | Tests green for touched surfaces | pytest on V1S affected modules + ruff | Yes |
| T8 | Duplicate mission packages owned or archived | MissionEngine DEPRECATED; MissionAdapter ARCHIVE; ownership in `runtime_ownership.py` | Yes |
| T9 | Every application package has a lifecycle owner | `package_lifecycle.py` registers all `app/application/*` dirs; Founder V1 Readiness shows Package Lifecycle | Yes |
| T10 | Engineering standards published | `docs/engineering/` Repository / Naming / Module / Dependency / Lifecycle policy present | Yes |
| T11 | No new `src.*` imports into `app/` product path | Static guard in `tests/test_v1s003_repository_health.py` | Yes |

---

## 5. Performance

| ID | Requirement | Check | Hard? |
|---|---|---|---|
| F1 | Home composition avoids duplicate engine evaluate when cached inputs identical | Code review Adaptive Workspace / Home service | Hold OK |
| F2 | Curriculum Map does not rebuild full CKG when certified package graph available | Knowledge graph presentation uses certified learner graph | Yes |
| F3 | Educational Authoring evaluate is O(topics in sitting), not full syllabus scan | Authoring engine scoped to mission context | Yes |
| F4 | Founder Version 1 Readiness page is static snapshot (no heavy DB fan-out) | `build_v1_readiness_snapshot` has no per-request curriculum load | Yes |
| F5 | G7 operator sample documented or HOLD | Per P-002.1 G7 | Hold OK |

---

## 6. Commercial

| ID | Requirement | Check | Hard? |
|---|---|---|---|
| C1 | Product feels one commercial identity | Dogfooders report no “prototype / transitional” language on Home | Yes |
| C2 | No public registration / open pricing claims | Auth remains invite-only | Yes |
| C3 | CRI board updated when material | `COMMERCIAL_READINESS_BOARD.md` note for V1S-001 | Hold OK |
| C4 | Validated KSI ≥ 80 for production-ready claim | P-002.1 G1 — **not required for dogfood GO** | No (launch) |
| C5 | Explainability + Recommendation checklists Pass for launch | P-001.2 / P-001.3 | No (launch) |

---

## 7. Launch (production-ready)

| ID | Requirement | Check | Hard? |
|---|---|---|---|
| L1 | P-002.1 gates G1–G12 PASS or approved HOLD | VERSION_1_READINESS + evidence package | Yes |
| L2 | Curriculum authority singularity complete for claimed cohort | A3 PASS without HOLD | Yes |
| L3 | Signed go / no-go under GP-001 | Board / founder record | Yes |
| L4 | Release Playbook executed | Tag + deploy protocol | Yes |
| L5 | Support path staffed for claimed cohort | Private beta support workflow | Yes |

---

## Dogfooding go / no-go (V1S-001)

| Outcome | When |
|---|---|
| **DOGFOOD GO** | E1–E9, P1–P6, P8, A1–A2, A4–A5, A7–A8, T1–T2, T4, T6–T7, F2–F4 PASS; A3/A6/F1/F5 HOLD documented; single authority per dogfood subject |
| **DOGFOOD HOLD** | Any Educational or Product hard FAIL; dual curriculum on same subject; student-visible engine nouns |
| **PRODUCTION NO-GO** | Default until L1–L5 and C4–C5 PASS |

**Current provisional status (2026-07-31):** **G1 FAIL — exclusive week incomplete** — see `G1_FOUNDER_EDUCATIONAL_VALIDATION_REPORT.md`. Integrity prerequisites PASS (`V1S008_EDUCATIONAL_INTEGRITY_VALIDATION_REPORT.md` · `V1S007_EDUCATIONAL_RUNTIME_SINGULARITY_REPORT.md`): DF-013/016 and DF-014/015 closed; open P0 educational defects: **none**. G1 consecutive live week not executed after remediation — do **not** proceed to G2 Closed Beta Readiness. Private beta **NO-GO** until 5–7 consecutive live days complete without undocumented workarounds.

Dogfooding GO additionally expects T9–T11 PASS (package lifecycle + engineering standards) once V1S-003 lands.

V1S-004 added a **founder dogfood validation** bar. V1S-005 remediates P0/P1 friction (published package readiness gate, silent episode quiet state, ProgressEngine isolation, Syllabus nav, CTA honesty). V1S-006 begins exclusive live evidence collection. See `app/services/dogfood_validation.py`.

---

## Related artefacts

| Artefact | Path |
|---|---|
| G1 Founder Educational Validation | `G1_FOUNDER_EDUCATIONAL_VALIDATION_REPORT.md` |
| Live week report | `V1S006_DOGFOOD_WEEK_REPORT.md` |
| Dogfood remediation report | `V1S005_IMPLEMENTATION_REPORT.md` |
| Dogfood validation report | `V1S004_DOGFOOD_REPORT.md` |
| Dogfood validation registry | `app/services/dogfood_validation.py` |
| Implementation report (engineering) | `V1S003_IMPLEMENTATION_REPORT.md` |
| Implementation report (cutover) | `V1S002_IMPLEMENTATION_REPORT.md` |
| Implementation report (polish) | `V1S001_IMPLEMENTATION_REPORT.md` |
| Package lifecycle registry | `app/services/package_lifecycle.py` |
| Runtime ownership registry | `app/services/runtime_ownership.py` |
| Engineering standards | `docs/engineering/` |
| Founder dashboard | `/founder/v1-readiness` |
| Release framework | `knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md` |
| Readiness tracker | `knowledge/VERSION_1_READINESS.md` |
| Product language | `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` |
| Blueprint | `PRODUCT_BLUEPRINT.md` |
