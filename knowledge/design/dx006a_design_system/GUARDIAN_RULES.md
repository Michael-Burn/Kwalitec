# Guardian Rules — DX-006A

**Programme:** DX-006A  
**Status:** Binding — update applied to `knowledge/design/UI_GUARDIAN.md`  
**Release Candidate:** `RC-2026.07.29-01`  

---

## 1. Purpose

Extend UI Guardian so every UI change is checked against the Design System foundation (L0–L3), DX-001–005 authorities, and the primary product rules.

---

## 2. Mandatory pre-read (implementation workflow)

Before writing or modifying UI, Cursor MUST read:

1. `knowledge/design/BRAND_GUIDELINES.md`  
2. `knowledge/design/dx006a_design_system/DESIGN_SYSTEM_ARCHITECTURE.md`  
3. `knowledge/design/dx006a_design_system/DESIGN_TOKEN_SPEC.md`  
4. `knowledge/design/dx006a_design_system/COMPONENT_CATALOGUE.md` (relevant entries)  
5. Surface authority as applicable: DX-004A/B/C or DX-005A/B/C  
6. This file + `UI_GUARDIAN.md`  

UX-001 / legacy type-40 scale is **superseded** for redesigns by DX-001 / DX-006A.

---

## 3. Enforceable checks (PASS required)

| ID | Check | Fail if |
|---|---|---|
| **G-1** | **One Primary** | More than one Primary-variant button/CTA in the primary task viewport |
| **G-2** | **One H1** | Multiple `h1` or duplicate shell+hero titles |
| **G-3** | **Token usage only** | New colour, spacing, type, radius, shadow, or motion values not in token spec |
| **G-4** | **No hard-coded colours** | Raw hex/rgb in component or page CSS/templates (except token definition files) |
| **G-5** | **No duplicate spacing scales** | Parallel space systems (e.g. inventing 12/96 alongside DX-001 4–64) in new work |
| **G-6** | **No dashboard KPI patterns** | Statistic tiles, vanity counts, progress rings as chrome |
| **G-7** | **No decorative cards** | Cards without DX-001 grouping justification; card grids for KPIs |
| **G-8** | **L0–L3 hierarchy** | Page invents primitives; L3 depends on routes; tokens defined inside components |
| **G-9** | **No decorative icons** | Icons without function or accessible name |
| **G-10** | **No duplicate navigation** | In-page nav competing with shell / OS boundaries |
| **G-11** | **Catalogue only** | Component not in catalogue (unless page-local and not promoted) |
| **G-12** | **Rejected list** | Use of Rejected components (`StatisticTile`, etc.) in new/migrated UI |

---

## 4. Authority checks (surface-aware)

| Surface | Extra Guardian focus |
|---|---|
| Founder Home | Current Work L0; no Platform Summary KPIs (DX-004A) |
| Subjects | Catalogue only; one Primary (DX-004B) |
| Workspace | Stage model; Review/Publish as stages (DX-004C) |
| Student Home | Mission L0; no gamification (DX-005A) |
| Choose Exam | Discovery; Begin Learning → Home (DX-005B) |
| Study Session | Practice First; educational feedback; no cheer (DX-005C) |

---

## 5. Never implement (DX-006A additions)

- Hard-coded colours or spacing in pages/components  
- Second Primary “for mobile”  
- KPI / StatisticTile / ProgressRing chrome  
- Decorative Card wrappers  
- New foundation components without Purpose + catalogue entry  
- Page-specific widgets exported as shared foundation without justification  
- Gold as button/link/focus colour  

---

## 6. Design review checklist (DX-006A)

Before approving UI:

- [ ] G-1 … G-12 PASS  
- [ ] Brand + DX-001 premium mandatory checks  
- [ ] Accessibility Standard  
- [ ] Responsive Standard  
- [ ] Empty / Loading / Error covered  
- [ ] Copy follows DX-003 (calm, professional, no cheer)  
- [ ] Self-review: Would Apple remove / Linear simplify / Notion clarify?  

---

## 7. Release rule

UI is **not complete** until Brand, DX-006A tokens/components, UI Guardian (including G-1–G-12), accessibility, responsive, and performance checks pass.

---

*Release Candidate: RC-2026.07.29-01*
