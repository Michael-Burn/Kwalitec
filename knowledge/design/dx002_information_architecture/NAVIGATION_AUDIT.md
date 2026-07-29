# Navigation Audit

**Programme:** DX-002  
**Release Candidate:** `RC-2026.07.29-01`

---

## 1. Shells in play

| Shell | Primary nav | Secondary | Status |
|---|---|---|---|
| Student EOS | Horizontal top nav | Mobile Menu toggle; Sign out | Canonical student |
| Console | Left sidebar (10) | Topbar search; Account; Sign out; footer Search | Canonical founder |
| Legacy workspace | Left sidebar (7) | Topnav email + appearance | Dual-run only — exclude from product IA |
| Session | Minimal chrome | — | Correct for focus |
| Auth | None | Appearance | Correct |
| Wizard | Step indicator | Back / Next | Correct pattern |

---

## 2. Student navigation

### Feature mode (default)

Home · Journey · Revision · History · Settings · Study Plan · Help  

**Count:** 7 destinations.

### Unified journey mode (`ENABLE_UNIFIED_JOURNEY`)

Today · Planning · Exam Readiness · Revision · Archive · Onboarding · Help  

**Count:** 7 destinations with different labels mapping to overlapping surfaces.

### Findings

| Question | Answer |
|---|---|
| Duplicated? | History ↔ Journal ↔ Timeline (Journal/Timeline not always in primary nav but repeatedly linked from History/Help) |
| Removable destinations? | Onboarding as permanent nav (unified mode) — should be one-shot; Help can stay |
| Implementation details? | Labels mostly product language; “Archive” is clearer than History for practice logs |
| Mirrors user goals? | Partially — Home/Journey/Revision good; memory triad does not |

### Target student nav

```
Home
Journey
Revision
Progress      ← History + Journal + Timeline (internal views)
Study Plan
Settings
```

Help: account menu or footer — not equal peer if nav budget is tight. Max **6** primary items.

---

## 3. Console navigation

### Primary (`COMMAND_CENTRE_NAV`)

Overview · Subjects · Curriculum Studio · Review Queue · Publishing · Versions · Quality · Students · Settings · Support  

**Count:** 10.

### Secondary (`COMMAND_CENTRE_SECONDARY_NAV`)

Operations · Learning · Assessments · Analytics · Platform · Attention · Runtime Health · Findings · Internal Alpha · System Operations · Releases · Vision Journal · Search  

**Count:** 13.

### Findings

| Question | Answer |
|---|---|
| Duplicated? | **Yes.** Review/Publishing/Versions/Quality ≈ filtered Studio; Attention ≈ Overview cards; Findings ≈ Support path; Search in topbar **and** secondary list; Operations vs System Operations naming collision |
| Removable destinations? | Review Queue, Publishing, Versions, Quality as top-level; most secondary reports from primary product path |
| Implementation details? | Runtime Health, Evidence Gates, Alpha Observability, System Operations expose engineering ontology |
| Mirrors user goals? | Curriculum path is close; ops sprawl is not |

### Target Console nav

```
Overview
Subjects
Curriculum Studio
Students
Support
Settings          ← nests: Search, Operations, Intelligence, Releases, Vision
```

**Max 6 primary.** Attention merges into Overview. Findings under Support.

### Context navigation (Workspace)

- Breadcrumbs: Overview → … → workspace — keep as Supporting Text (not hero).  
- CIP tabs (9): **collapse** to stage-relevant set (e.g. Structure · Review · Evidence).  
- Do not duplicate hub destinations inside workspace tabs with equal weight to sidebar.

---

## 4. Breadcrumbs, tabs, menus

| Pattern | Where | Verdict |
|---|---|---|
| Breadcrumbs | Studio hubs + workspace | Keep; quieter type |
| CIP tab bar | Workspace | Overload — reduce |
| Wizard steps | Study Plan | Keep 4; remove orphan step templates from product mindshare |
| Settings section nav | `/settings` | Keep local |
| Appearance switcher | Topnav / auth | Keep; not primary nav |
| Account link (Console → settings) | Topbar | Keep quiet |

---

## 5. Duplicate CTA map (navigation smell)

| Destination | Appears in |
|---|---|
| Curriculum Studio | Sidebar, Console Quick Actions, every hub “Open Curriculum Studio” |
| Support / Feedback | Sidebar, Overview attention card, Quick Actions, recent support |
| Attention | Overview CTA, attention cards, secondary nav |
| Search | Topbar form, secondary nav, sidebar foot |

**Rule:** A destination may appear once in primary nav; deep links from content lists are fine; repeating as Primary buttons is not.

---

## 6. Cross-shell leakage

| Link | Risk |
|---|---|
| Console Account → student settings | Acceptable if labelled Account |
| Student never sees Console | Correct |
| Legacy sidebar still in codebase | Confuses agents/docs — document as non-product |

---

## 7. Global Search & Notifications

| Capability | Present | IA decision |
|---|---|---|
| Console Search | Yes | Keep operator-only topbar |
| Student global search | No | Do not add for Alpha |
| Help topic search | Yes | Keep local |
| Notification centre | No | Do not add; use flash |

---

## 8. Recommendations (ordered)

1. Collapse Curriculum hubs to Studio filters — remove 4 primary nav items.  
2. Cap Console primary at 6; nest reports under Settings.  
3. Unify student Progress surfaces under one nav item.  
4. Eliminate Quick Actions Primary button cluster on Console Home.  
5. Reduce Workspace tabs to ≤3 stage-relevant views.  
6. Treat legacy sidebar as non-existent for redesign programmes.
