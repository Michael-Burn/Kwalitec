# Implementation Plan

**Programme:** DX-004A  
**Status:** Plan for subsequent UI execution (not executed in DX-004A)  
**Release Candidate:** `RC-2026.07.29-01`  
**Depends on:** This corpus + DX-001 / DX-002 / DX-003  

---

## Scope boundary

| DX-004A (this programme) | Later execution |
|---|---|
| Architecture, wireframe, removal register, scorecard | Template + CSS + view-model |
| Documentation only | Routes/nav label updates |
| No application code | `overview.html` → Home |

DX-004A does **not** ship UI. The following is the ordered plan for the implementation milestone that consumes these artefacts (Founder Experience Redesign / DX-004 Home slice).

---

## Phase 0 — Preconditions

1. Treat `FOUNDER_HOME_ARCHITECTURE.md` + `FOUNDER_HOME_WIREFRAME.md` as binding.  
2. Update `TERMINOLOGY_DICTIONARY.md`: Console decision surface **Home** (was Overview).  
3. Confirm publication pipeline can supply: current workspace, attention queue by stage, recent published (≤5).  
4. Do not start Subjects (DX-004B) until Home exit criteria are met in UI.

---

## Phase 1 — Content & structure (no token remap first)

Per DX-003 cognitive-load plan: content and IA before chrome polish.

1. Replace `overview.html` body with L0 / L1 / L2 structure only.  
2. Delete Platform Summary, Quick Actions, Operational detail, Attention KPI grid, pulse essay, version eyebrow from Home template.  
3. Single Primary in L0; queue/recent as lists.  
4. Empty state: Reason + Create Subject.  
5. Wire Primary → Curriculum Workspace (or Subjects create).

**Exit:** One question answerable without scroll; one Primary.

---

## Phase 2 — View-model

1. Build Home DTO:  
   - `current_work`: subject, stage, primary_label, href  
   - `queue[]`: subject, status, href (attention-only)  
   - `recent_publications[]`: subject, published_at, href (max 5)  
2. Selection algorithm per Architecture §5.  
3. Stop feeding Home with participant/check-in/health aggregates.  
4. Preserve those aggregates on Operations / Research routes only.

**Exit:** Home renders without legacy overview metrics fields.

---

## Phase 3 — Navigation chrome

1. Rename nav label Overview / Console Home → **Home**.  
2. Remove in-page duplicates (already deleted in Phase 1).  
3. Align sidebar to ≤6 primary items per `NAVIGATION_SIMPLIFICATION.md` (may span DX-004 nav slice).  
4. Ensure Attention / Operations are not Home Primaries.

**Exit:** Nav audit FP for Home Quick Actions closed.

---

## Phase 4 — Visual system compliance

1. Apply DX-001 type scale (24 / 18 / 16 / 14).  
2. Apply spacing scale only.  
3. Semantic status colour; no gold chrome.  
4. Focus states, keyboard order, responsive column.  
5. Re-run `PREMIUM_SCORECARD.md`; all ≥9.

**Exit:** Scorecard PASS on live UI.

---

## Phase 5 — Verification

| Test | Expect |
|---|---|
| Dogfood 3-second test | “I should Resume X” |
| No KPI tiles in DOM on Home | 0 |
| Primary count | 1 |
| A11y smoke | Focus, contrast, labels |
| Regression | Support / Operations still reachable via nav |
| Curriculum V1/V2 | Untouched (Home is Console chrome only) |

---

## Out of scope for Home implementation

- Subjects catalogue redesign → **DX-004B**  
- Curriculum Workspace stage UI → later DX-004 slice  
- Student Home  
- Algorithm / curriculum engine changes  
- New dependencies  

---

## Risk register

| Risk | Mitigation |
|---|---|
| Ops-only Founders miss health on Home | Nest health under Settings; Alpha process uses Operations |
| Empty queue but unfinished drafts hidden | Selection algorithm prefers last-active workspace in L0 |
| Data model lacks “recent published” | Derive from publication bridge / subject Ready events |
| Scope creep into Subjects | Hard stop — DX-004B |

---

## Recommended ownership order

1. Design (done — DX-004A)  
2. Console template + service DTO  
3. Nav label / dictionary  
4. Premium re-score  
5. DX-004B Subjects
