# Implementation Plan

**Programme:** DX-004B  
**Status:** Plan for subsequent UI execution (not executed in DX-004B)  
**Release Candidate:** `RC-2026.07.29-01`  
**Depends on:** This corpus + DX-001 / DX-002 / DX-003 / DX-004A  

---

## Scope boundary

| DX-004B (this programme) | Later execution |
|---|---|
| Architecture, wireframe, object model, specs, scorecard | Template + CSS + view-model + routes |
| Documentation only | Hub collapse in nav |
| No application code | Subjects catalogue UI |

DX-004B does **not** ship UI. The following is the ordered plan for the implementation milestone that consumes these artefacts.

---

## Phase 0 — Preconditions

1. Treat `SUBJECTS_ARCHITECTURE.md` + `CATALOGUE_WIREFRAME.md` as binding.  
2. Confirm Home (DX-004A) “View all in Subjects” / Create Subject targets remain valid.  
3. Inventory routes: Subjects hub + Review / Publishing / Versions / Quality hubs — mark for collapse.  
4. Confirm DTO can supply identity fields in `OBJECT_MODEL.md`.  
5. Do not start Workspace visual redesign (DX-004C) until Subjects catalogue contract is clear (design already is; UI may parallelise carefully).

---

## Phase 1 — Single catalogue structure

1. Replace Subjects body with L0 table/list + L1 search/filter + header Create Subject.  
2. Delete tutorial essays, dual Primary cards, “Open Curriculum Studio” CTA, KPI/activity chrome.  
3. Wire row Open → workspace (no intermediate landing).  
4. Empty state: Reason + Create Subject per `EMPTY_STATE_SPEC.md`.  

**Exit:** One question; one Primary; table catalogue.

---

## Phase 2 — Search, filter, sort

1. Implement search over name/code with <200ms cached target.  
2. Status / activity filters per `SEARCH_FILTER_SPEC.md`.  
3. Default sort: most recently active; expose alphabetical / recently published / recently created.  
4. Optional URL presets for Ready to publish (Home deep-links).  

**Exit:** Search-first path works without hub switching.

---

## Phase 3 — Hub collapse & navigation

1. Remove Review Queue / Publishing / Versions / Quality as peer nav destinations.  
2. Map intents to filters or workspace stages (`NAVIGATION_BOUNDARIES.md`).  
3. Ensure Curriculum Studio is not a second Subjects catalogue.  
4. Align shell ≤6 items with DX-004A nav plan.  

**Exit:** Subjects is the only curriculum catalogue in nav.

---

## Phase 4 — Object permanence

1. Shared Subject name/stage helpers for Home, Subjects, Workspace headers.  
2. Row fields match `ROW_SPECIFICATION.md` / `OBJECT_MODEL.md`.  
3. More (…) for rare ops only.  

**Exit:** Same subject reads as one object across surfaces.

---

## Phase 5 — Visual system & a11y

1. DX-001 type/spacing; no card walls.  
2. Keyboard: search, row navigate, Enter opens.  
3. Responsive stack per wireframe.  
4. Re-run `PREMIUM_SCORECARD.md`; all ≥9.  

**Exit:** Scorecard PASS on live UI.

---

## Phase 6 — Performance

1. Client or server search index for catalogue scale.  
2. Virtualise/paginate when row count demands — same layout.  
3. Spot-check time-to-Open <5s for known subject.  

**Exit:** Performance goals met or documented residual.

---

## Non-goals (implementation)

- Student Ready catalogue redesign  
- Workspace stage UI redesign (DX-004C)  
- Home UI (separate DX-004A plan) unless coupling nav labels  
- Curriculum engine / V1–V2 changes  

---

## Suggested file touchpoints (indicative)

Exact paths follow live codebase at execution time. Likely:

- Founder / console Subjects templates and routes  
- Nav config (`nav.py` / sidebar)  
- View-models for subject list DTO  
- Hub templates currently duplicating catalogues  

Do not CSS-hide legacy hubs — remove routes/nav entries and redirect presets to Subjects filters where needed.

---

## Sequencing with DX-004A / DX-004C

| Order | Work |
|---|---|
| Design | DX-004A ✓ · DX-004B ✓ · DX-004C next |
| UI | Home and Subjects may ship in one Founder Experience slice if nav stays coherent |
| UI | Workspace (DX-004C) after catalogue Open contract is stable |

---

## Definition of done (UI milestone)

- [ ] Subjects is the only catalogue in product nav  
- [ ] Exactly one Primary: Create Subject  
- [ ] Search-first; filters/sort per spec  
- [ ] Open → workspace one click  
- [ ] Empty state compliant  
- [ ] Premium scorecard ≥9 live  
- [ ] No curriculum V1/V2 breakage (N/A expected)  
