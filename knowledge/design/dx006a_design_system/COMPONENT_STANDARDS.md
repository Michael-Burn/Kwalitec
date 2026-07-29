# Component Standards

**Programme:** DX-006A  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  

---

## 1. Purpose

Define the **documentation and engineering contract** every catalogue component must satisfy before it may enter the foundation or be used in DX-006B migrations.

---

## 2. Mandatory documentation fields

Every component entry in `COMPONENT_CATALOGUE.md` must include:

| Field | Meaning |
|---|---|
| **Purpose** | Why it exists — one sentence job |
| **When to use** | Conditions that justify inclusion |
| **When NOT to use** | Forbidden or better-alternative cases |
| **Inputs** | Props / attributes / slots |
| **Outputs** | Events / navigation / side effects (UI only) |
| **States** | Default, interactive, disabled, loading, error, empty as applicable |
| **Accessibility** | Roles, names, ARIA, contrast notes |
| **Keyboard behaviour** | Keys and focus rules |
| **Responsive behaviour** | Mobile / tablet / desktop expectations |
| **Examples** | Real product usages |
| **Anti-patterns** | Known misuse |

Incomplete entries are not shippable.

---

## 3. Existence test

Before adding a component:

1. Does an existing catalogue entry already cover this job? → **Reuse**.  
2. Is the job decorative or KPI theatre? → **Reject**.  
3. Is the job page-specific and unlikely to recur? → **Keep on page**; do not promote.  
4. Does it contradict DX-001–005? → **Reject**.  
5. Clear purpose + ≥2 intended call sites → **Propose** for catalogue + Guardian review.

---

## 4. API conventions

- **Naming:** PascalCase component names; semantic prop names (`tone`, not `color`).  
- **Variants:** Closed enums only (e.g. Button `primary | secondary | ghost | text | danger`).  
- **Tokens:** Props accept token names or map internally to tokens — never raw hex/px from callers.  
- **Composition:** Children / slots for content; do not fork components per page.  
- **No domain logic:** No mastery math, recommendation ranking, or curriculum rules inside components.

---

## 5. Visual rules

- Exactly one Primary **button variant** usage per page.  
- Cards only when DX-001 grouping test passes.  
- Icons: Lucide only; functional meaning; adjacent text or accessible name.  
- Elevation: prefer border; shadows rare.  
- Motion: token durations only; respect reduced motion.

---

## 6. State completeness

Interactive components ship with:

| State | Required |
|---|---|
| Focus visible | Always |
| Disabled + reason path for blocked Primary | When applicable |
| Loading on async submit | When applicable |
| Error association for fields | Forms |
| Empty for collections | Lists/tables/queues |

---

## 7. Testing expectations (implementation phases)

| Check | Minimum |
|---|---|
| Token integrity | No raw colour/spacing in component styles |
| A11y | Keyboard path + name + focus |
| Responsive | Smoke at mobile / tablet / desktop widths |
| Hierarchy | Component level L1–L3 respected in imports |

---

## 8. Deprecation

Rejected or superseded components:

1. Mark **Rejected** in catalogue.  
2. Remove from public foundation `__init__` exports used by new work.  
3. Leave shim only if unmigrated pages require it — with expiry in DX-006B.  
4. Never document Rejected items as recommended.

---

## 9. Anti-patterns (standards level)

- “Utility” components that only wrap a div with a hard-coded colour  
- Forking `ButtonPrimaryStudent` / `ButtonPrimaryFounder`  
- Embedding copy essays inside primitives  
- Shipping without When NOT to use  

---

*Release Candidate: RC-2026.07.29-01*
