# Empty State Specification

**Programme:** DX-004B  
**Status:** Binding for Subjects empty / zero-result states  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-003 `EMPTY_STATE_STANDARDS.md`, DX-001  

---

## 1. Law

Every empty state contains **exactly**:

```
Reason
    ↓
Next Action
```

Nothing else.

Forbidden: tips, illustrations with essays, secondary metrics, welcome copy, feature promotion, multiple equal CTAs.

---

## 2. Catalogue empty (zero subjects)

| Beat | Copy |
|---|---|
| **Reason** | No subjects yet. |
| **Next Action** | **Create Subject** |

### Layout

- Page title: Subjects  
- **Canonical Primary placement:** filled **Create Subject** in the empty region (centred or start-aligned in content column)  
- Header must **not** show a second filled Primary at the same time (avoid twin Primaries). Hide header Primary while empty, or use header text-only title with empty-region Primary only.

### Wireframe

See `CATALOGUE_WIREFRAME.md` — empty state.

---

## 3. Search / filter zero results

| Condition | Reason | Next Action |
|---|---|---|
| Query has no matches | No matches. | Clear query |
| Filters exclude all | No subjects match. | Clear filters |

Page Primary **Create Subject** may remain available in header when the catalogue is non-empty overall but the current query/filter set is empty — the **Next Action** for the empty region is Clear query / Clear filters, not Create (unless the Founder explicitly wants to create; Create stays the page Primary, Clear is the empty-region action as Secondary/text or Primary only if Create is not competing — prefer **text/button Secondary: Clear query** while header keeps Create Subject as the sole filled Primary).

**Canonical zero-result:**

```
Reason: No matches.
Next Action: Clear query   ← Secondary / text button
Header: [ Create Subject ] ← sole filled Primary
```

---

## 4. Archived-only / edge

If the Founder filters to Archived and none exist:

| Reason | Next Action |
|---|---|
| No archived subjects. | Clear filters |

---

## 5. Tone

| Do | Do not |
|---|---|
| Factual Reason | “Start your curriculum journey with Kwalitec…” |
| Verb-led Create Subject | “Get started” / “Add your first course” |
| Stop after Next Action | Bullet tutorials under the CTA |

Align DX-003 Subjects pattern: *No subjects yet. → Create Subject*.

---

## 6. Success test

Empty Subjects shows two elements only (Reason + Create Subject). A reviewer cannot find a third content block that is not shell chrome.
