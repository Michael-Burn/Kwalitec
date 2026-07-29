# DX-004B Completion Report

**Programme:** DX-004B — Subjects Experience Redesign (Catalogue First)  
**Status:** Complete  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01` (Alpha Candidate 1)  
**Implementation:** None (documentation-only; no CSS, layouts, components, or routes)

---

## Summary

DX-004B designs Subjects from first principles as the **canonical curriculum catalogue** under **Catalogue First**. The page answers one question — **Which subject do I want to work on?** — with exactly one Primary (**Create Subject**) and an L0–L3 hierarchy (Catalogue → Search/Filters → Quick Metadata → shell navigation). Search is primary; browsing secondary. Object permanence is specified across Catalogue, Workspace, Publication, Review, and History. Competing Studio hubs are retired as catalogues. Premium scorecard target **≥9/10** is met for the architecture. No UI was implemented.

---

## Elements removed

(From legacy Subjects / multi-hub pattern — Zero Legacy; register for implementation removal)

- KPI cards, analytics, charts, progress rings  
- Platform statistics on catalogue  
- Tutorial / workflow essays on hub pages  
- Feature promotion and welcome chrome  
- Recent activity feeds and operational summaries  
- Duplicate quick actions and multi-Primary clusters  
- Decorative icons as default row chrome  
- Peer catalogue pages: Review Queue, Publishing, Versions, Quality hubs  
- “Open Curriculum Studio” as Subjects Primary  
- Side-by-side Create / Open Workspace marketing cards  
- Intermediate subject landing / summary between catalogue and workspace  
- Technical sort orders exposed in UI  

---

## Elements retained

| Element | Reason |
|---|---|
| **Page title — Subjects** | Recognition; DX-001 page heading |
| **L0 catalogue table/list** | System of record; one row = one subject |
| **Primary — Create Subject** | Sole origin action for curriculum objects |
| **Search** | Primary find path; scales to hundreds |
| **Minimal filters** | Status / recently updated / ready to publish / in progress / archived |
| **Sort controls** | Recently active (default), alphabetical, recently published, created |
| **Quiet metadata** | Stage, updated, publication status — decision support only |
| **Open + More (…)** | Continue vs rare ops; no action overload |
| **L3 shell navigation** | Escape without duplicate local nav |
| **Empty: Reason → Create Subject** | DX-003 empty-state law |

Every retained element is justified by recognition, create, or open — not decoration.

---

## Catalogue scalability assessment

| Scale | Design response |
|---|---|
| 0 | Empty state only |
| Tens | Browse + search |
| Hundreds | Search-first + same table; virtualisation/pagination allowed |
| Layout redesign at N | **None** — thresholds must not spawn dashboards |

Performance targets: cached search **<200ms**; Open **one click**; time-to-action **<5s** for a known subject. Architecture supports these; live verification is an implementation gate.

---

## Estimated reduction in navigation complexity

| Metric | Legacy | Target | Δ |
|---|---|---|---|
| Curriculum catalogue destinations | 5 hubs | **1** (Subjects) | **−80%** |
| Decisions to “find a subject” | Hub pick + scan/tutorial | Search or scan one list | **~60–75%** fewer nav choices |
| Primaries on Subjects entry | 2–4 | **1** | **~70%** |
| Hops Open known subject | Often 2–4 | **1** (search → open) | **~50–75%** |

Home retains continuation; Subjects no longer competes as a second “what next” dashboard.

---

## Expected improvement in discovery

- Recognition-first rows (name → stage → open) vs recall of which hub.  
- Search-first path removes dependence on remembering pipeline location.  
- Object permanence reduces “is this the same curriculum?” friction across surfaces.  
- Former hub intents become filters — discovery stays on one URL.  

*(Estimates are architectural; not instrumented UX timings.)*

---

## Implementation notes

1. Do not CSS-hide legacy hubs — collapse nav/routes; redirect presets to Subjects filters (`IMPLEMENTATION_PLAN.md`).  
2. Catalogue DTO: identity fields from `OBJECT_MODEL.md`; no KPI aggregates.  
3. Open must enter workspace immediately — no summary interstitial.  
4. Coordinate with DX-004A Home links (“View all in Subjects”, Create Subject).  
5. Re-score live UI with `PREMIUM_SCORECARD.md`; any dimension ≤8 → redesign before ship.  
6. Update UI Guardian to enforce Subjects-only catalogue + one Primary + no hub peers.  
7. No curriculum engine / V1–V2 changes.

---

## Known limitations

- Architecture only — live product may still show multi-hub catalogues until implementation.  
- Workspace visual redesign deferred to **DX-004C**; only the Open transition is bound here.  
- Student Subject Catalogue (Ready / Coming Soon) is out of scope — noun shared, surface separate.  
- Search <200ms depends on client index or API design at implementation.  
- Owner column optional; multi-operator rules may need Alpha policy later.  
- No Figma file; ASCII wireframe is the layout authority.  
- Premium scores are **design-target** scores, not validated on rendered UI.

---

## Recommendations for DX-004C

**DX-004C — Publication Workspace Redesign** should:

1. Honour **object permanence** — same Subject name/stage language as Subjects / Home.  
2. Own **execution** only — no embedded second catalogue or Home-style “what next” hero.  
3. Receive Open from Subjects as the default entry — no intermediate landing.  
4. Host Validate / Approve / Publish actions that were forbidden on catalogue rows.  
5. Keep Review / Publish as **stages** (or clear stage chrome), not resurrected hub pages.  
6. Apply DX-001–003 density: one Primary per stage decision; no KPI theatre.  
7. Preserve keyboard/focus continuity from catalogue row activation into workspace.  
8. Update Guardian rules for Workspace L0–L3 once defined.  
9. Sequence UI: stable Subjects Open contract before or tightly coupled with Workspace chrome.

---

## Premium review

See `PREMIUM_SCORECARD.md`.

| Dimension | Score |
|---|---:|
| Catalogue Clarity | 10 |
| Recognition Speed | 10 |
| Search Experience | 10 |
| Information Density | 9 |
| Object Consistency | 10 |
| Minimalism | 10 |
| Professional Tone | 10 |
| Navigation Clarity | 10 |
| Scalability | 9 |
| Overall Premium Feel | 10 |

**Mandatory checks: PASS. Verdict: SHIP (design).**

---

## Files Created

- `knowledge/design/dx004b_subjects/DX004B_EXECUTIVE_SUMMARY.md`  
- `knowledge/design/dx004b_subjects/SUBJECTS_ARCHITECTURE.md`  
- `knowledge/design/dx004b_subjects/CATALOGUE_WIREFRAME.md`  
- `knowledge/design/dx004b_subjects/OBJECT_MODEL.md`  
- `knowledge/design/dx004b_subjects/ROW_SPECIFICATION.md`  
- `knowledge/design/dx004b_subjects/SEARCH_FILTER_SPEC.md`  
- `knowledge/design/dx004b_subjects/EMPTY_STATE_SPEC.md`  
- `knowledge/design/dx004b_subjects/NAVIGATION_BOUNDARIES.md`  
- `knowledge/design/dx004b_subjects/PREMIUM_SCORECARD.md`  
- `knowledge/design/dx004b_subjects/IMPLEMENTATION_PLAN.md`  
- `knowledge/design/dx004b_subjects/DX004B_COMPLETION_REPORT.md`  

## Files Modified

- `.cursor/rules/99-CURRENT_MILESTONE.md` (milestone pointer → DX-004B complete)

## Tests Executed

None (documentation-only).

## Migration Impact

None.

## Architecture Compliance

N/A for curriculum V1/V2 traversal. No application layering or engine changes. Design architecture is additive under `knowledge/design/`. Console remains the operator shell (DX-002); Subjects is the Console Catalogue-type surface; Home remains continuation (DX-004A).

## Technical Debt

- Live Subjects / hub templates still violate DX-001–004B until implementation.  
- Nav may still expose Review / Publishing / Versions / Quality until Phase 3 of the implementation plan.  
- Terminology dictionary may need Subjects catalogue vs student catalogue clarification at implementation.

## CRI / KSI / Student Impact

N/A — design documentation for Founder Console surface; no student-facing Runtime A / recommendation / KSI claims. ΔKSI = 0. ΔCRI = 0 (provisional; no board update). Student Ready catalogue unchanged.

## Explainability Review

N/A — no student-facing intelligence changes.

## Recommendation Quality Review

N/A — no recommendation ranking changes.

## Version 1 readiness residual

N/A — does not claim V1 production-ready progress; clears a design gate for Founder Console UX.

---

## Exit criteria

| Criterion | Status |
|---|---|
| Subjects is the only catalogue | ✓ Architecture + navigation boundaries |
| Exactly one Primary action | ✓ Create Subject |
| Object permanence documented | ✓ `OBJECT_MODEL.md` |
| Search-first architecture established | ✓ `SEARCH_FILTER_SPEC.md` |
| Navigation boundaries defined | ✓ `NAVIGATION_BOUNDARIES.md` |
| Premium score ≥9/10 | ✓ Scorecard (all ≥9) |

**DX-004B is complete.** The project may proceed to **DX-004C — Publication Workspace Redesign** (design) and/or Subjects UI implementation per `IMPLEMENTATION_PLAN.md`.
