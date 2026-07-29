# Implementation Guard

**Programme:** DX-006B  
**Status:** Binding — stop-ship rules for all migration work  
**Release Candidate:** `RC-2026.07.29-01`  

---

## 1. Purpose

Prevent architectural drift while Founder and Student surfaces are migrated onto the DX-006A design system.

If a proposed change violates this Guard, **do not merge**. Fix or discard.

---

## 2. Authority stack (read before coding)

Mandatory pre-read for any DX-006B UI change:

1. `knowledge/design/BRAND_GUIDELINES.md`  
2. `knowledge/design/dx006a_design_system/DESIGN_SYSTEM_ARCHITECTURE.md`  
3. `knowledge/design/dx006a_design_system/DESIGN_TOKEN_SPEC.md`  
4. `knowledge/design/dx006a_design_system/COMPONENT_CATALOGUE.md` (relevant entries)  
5. Surface authority (DX-004A / 004B / 004C / 005A / 005B / 005C)  
6. `knowledge/design/dx006a_design_system/GUARDIAN_RULES.md` + `UI_GUARDIAN.md`  
7. This file + `MIGRATION_SEQUENCE.md`  

---

## 3. Engineering Law

```text
Architecture is the authority.
Code conforms to architecture.
Architecture does not conform to code.
```

Forbidden remediation patterns:

- Editing DX-001…006A docs to legalise a shortcut  
- “Temporary” second Primary  
- New tokens defined in page CSS  
- Page-local widgets promoted as shared without catalogue Purpose  

---

## 4. Migration Philosophy (enforceable)

| ID | Rule | Fail if |
|---|---|---|
| **M-1** | **Replace** | New UI layered on top of unchanged legacy body |
| **M-2** | **Never layer** | Dual trees (new + old) both reachable for same job |
| **M-3** | **Never CSS-hide** | Legacy KPI / Quick Action / Sensei blocks only `display:none` / `visibility:hidden` / off-canvas |
| **M-4** | **Never preserve legacy chrome** | Platform Summary, readiness tiles, coach walls, hub peers remain in template |

---

## 5. Forbidden during DX-006B

| ID | Forbidden | Why |
|---|---|---|
| **F-1** | New dashboards | DX-001 / DX-002 Home ≠ dashboard |
| **F-2** | New KPI cards / StatisticTile | G-6; DX-001 vanity ban |
| **F-3** | Extra Primaries | G-1; one Primary law |
| **F-4** | Page redesign | Architecture frozen; fidelity programme |
| **F-5** | New IA / nav trees | DX-002 / DX-004 / DX-005 own structure |
| **F-6** | Component duplication | Catalogue only (G-11) |
| **F-7** | Token duplication | Single token law (G-3, G-5) |
| **F-8** | Hard-coded colours | G-4 |
| **F-9** | Architecture document changes | Drift legalisation |
| **F-10** | Skipping phase order | `MIGRATION_SEQUENCE.md` |

---

## 6. Required composition pattern

```text
Page
  └── L2 Layout (Page / Section / Stack / …)
        └── L3 Operational (Mission / Current Work / …)
              └── L1 Primitives (Button / Badge / …)
                    └── L0 Tokens
```

- Pages **compose**; they do not invent primitives.  
- L3 must not import routes or Flask request globals.  
- Rejected catalogue components (StatisticTile, ProgressRing chrome, etc.) must not appear on migrated surfaces (G-12).

---

## 7. Phase start checklist

Before writing Phase *N* code:

- [ ] Phase *N−1* marked **CERTIFIED** in `PHASE_TRACKER.md` (or Foundation Gate for Phase 1)  
- [ ] Surface authority corpus read  
- [ ] Shared components to reuse listed (no duplicates planned)  
- [ ] Legacy removal list from authority IMPLEMENTATION_PLAN / CONTENT_REMOVAL_REGISTER identified  
- [ ] No architecture edits proposed  

---

## 8. Phase ship checklist

Before marking Phase *N* CERTIFIED:

- [ ] Legacy chrome removed (not hidden)  
- [ ] One H1 · One Primary  
- [ ] Guardian G-1…G-12 PASS  
- [ ] Accessibility Standard PASS  
- [ ] Performance audit PASS (no KPI DOM; L2–L3 lazy where specified)  
- [ ] Regression PASS  
- [ ] Architectural Fidelity ≥95%  
- [ ] Premium all dimensions ≥9/10  
- [ ] Phase report fields filled in `PHASE_TRACKER.md`  

---

## 9. Escalation

| Situation | Action |
|---|---|
| Spec ambiguity between DX docs | Prefer more specific surface authority; record in phase Known issues; do not invent IA |
| Missing L3 component | Add to catalogue first (DX-006A process) — do not page-orphan |
| Backend cannot supply DTO field | Honest empty / blocking state per DX-003; do not fake KPI |
| Pressure to “ship and polish later” | Refuse certification; keep phase In Progress |

---

## 10. After programme exit

Only when all six phases CERTIFIED may work proceed to **CQ-008**.  
Until then, do not claim Premium Product Certification.

---

*Release Candidate: RC-2026.07.29-01*
