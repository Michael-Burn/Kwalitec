# Design System Architecture

**Programme:** DX-006A  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-001 · DX-002 · DX-003 · DX-004 · DX-005 · Brand Guidelines  

---

## 1. Purpose

Define how the Kwalitec Design System is structured so that:

1. **Pages compose components** — never invent local UI primitives.  
2. **Components compose tokens** — never hard-code colour, space, type, radius, or motion.  
3. **Tokens define the visual language** — single source of truth.  
4. **Guardian enforces** hierarchy and primary rules.

DX-006A is the foundation. DX-006B migrates Founder and Student surfaces onto it.

---

## 2. Layering model

```
┌─────────────────────────────────────────────────────────┐
│  Pages (DX-006B)                                        │
│  Founder Home · Subjects · Workspace · Student Home · … │
├─────────────────────────────────────────────────────────┤
│  L3 Operational Components                              │
│  Mission Card · Stage Indicator · Blocking Findings · … │
├─────────────────────────────────────────────────────────┤
│  L2 Layout Components                                   │
│  Page · Section · Container · Grid · Stack · Table · …  │
├─────────────────────────────────────────────────────────┤
│  L1 Primitive Components                                │
│  Button · Input · Dialog · Toast · Empty State · …      │
├─────────────────────────────────────────────────────────┤
│  L0 Design Tokens                                       │
│  Colour · Type · Space · Elevation · Radius · Motion ·… │
└─────────────────────────────────────────────────────────┘
```

| Level | May depend on | Must not depend on |
|---|---|---|
| **L0 Tokens** | Brand HEX | Components, pages, domain logic |
| **L1 Primitives** | L0 only | Layout shells, operational concepts, routes |
| **L2 Layout** | L0 + L1 | Product OS concepts (Mission, Stage) |
| **L3 Operational** | L0 + L1 + L2 | Page routes, educational decision math |
| **Pages** | All levels | Inventing new L0–L3 without catalogue entry |

Educational / planning logic stays in services. Presentation components receive view-model props only.

---

## 3. Component philosophy

Every component must answer:

> **Why does this exist?**

| Answer quality | Outcome |
|---|---|
| Clear product job (e.g. “sole next action control”) | Keep |
| Vague (“looks nice”, “dashboard feel”) | Reject |
| Duplicate of an existing pattern | Merge or reject |
| Page-specific one-off | Keep on the page until promoted with justification |

No orphan components in the foundation. If nothing consumes a component after DX-006B, remove it.

---

## 4. Dual runtime surfaces (compatibility)

Kwalitec currently has two presentation paths. DX-006A unifies **contracts**; migration unifies **usage**.

| Runtime | Path | Role under DX-006A |
|---|---|---|
| **CSS tokens** | `app/static/css/tokens.css` (+ brand) | Canonical CSS custom properties for Flask/Jinja shells |
| **Python DS** | `src/presentation/design_system/` | Framework-independent token + component contracts |
| **Templates / JS** | `app/templates/`, `app/static/js/` | Compose L1–L3; no hard-coded values |

Both runtimes must expose the **same semantic token names** after Phase 1 remap. Components document one API; adapters render HTML/CSS or Python dataclasses.

---

## 5. Authority resolution

| Conflict | Winner |
|---|---|
| Token values vs UX-001 legacy scale | **DX-001** (via this programme) |
| Component exists in V3 but contradicts DX-001 KPI/card policy | **Reject / replace** (see catalogue) |
| Founder Home structure | **DX-004A** |
| Subjects catalogue | **DX-004B** |
| Workspace stages | **DX-004C** |
| Student Home / Mission | **DX-005A** |
| Choose Exam | **DX-005B** |
| Study Session | **DX-005C** |
| Copy tone / empty states | **DX-003** |
| Surface type / nav tree | **DX-002** |
| Brand HEX / mark | **Brand Guidelines** |

---

## 6. Primary composition rules

1. **One Primary** per page (viewport / primary task context).  
2. **One H1** per page.  
3. **L0 operational strip** (Persistent Context / Current Work / Mission) may host the Primary; secondary actions stay Ghost/Text.  
4. **Cards** only when DX-001 grouping justification holds.  
5. **Tables / lists** for collections; never KPI card grids.  
6. **Icons** (Lucide only) for function, never decoration.  
7. **No duplicate navigation** — shell owns nav; pages do not re-implement peer trees.

---

## 7. State model (all interactive components)

Every interactive L1+ component documents:

| State | Required |
|---|---|
| Default | Yes |
| Hover | Pointer devices |
| Focus | Always — visible ring from tokens |
| Active / Pressed | Interactive controls |
| Disabled | With adjacent reason when Primary is blocked |
| Loading | Async actions |
| Error | Forms and blocking failures |
| Empty | Collections and missions |

Empty / Loading / Error **states** are first-class L1 patterns — not page invents.

---

## 8. Accessibility & responsiveness

- WCAG **AA** minimum — see `ACCESSIBILITY_STANDARD.md`.  
- Desktop / Tablet / Mobile — one component, responsive behaviour — see `RESPONSIVE_STANDARD.md`.  
- No separate “mobile variants” unless catalogue records a justified exception.

---

## 9. Performance constraints

- Minimal DOM; no decorative wrapper stacks.  
- Lazy render for off-screen L2 disclosures and heavy tables where justified.  
- Shared CSS classes from tokens — no duplicated per-page style sheets for the same primitive.  
- Prefer CSS variables over inline style attributes.

---

## 10. Guardian boundary

`UI_GUARDIAN.md` + `GUARDIAN_RULES.md` enforce:

- One Primary · One H1 · Token-only values · No hard-coded colours · No duplicate spacing scales · No KPI theatre · No decorative cards · L0–L3 hierarchy respected  

Implementation that fails Guardian is not shippable.

---

## 11. What DX-006A does not own

- Page layouts for Founder/Student (DX-006B)  
- Curriculum / mastery / recommendation algorithms  
- New brand colours or fonts  

---

*Release Candidate: RC-2026.07.29-01*
