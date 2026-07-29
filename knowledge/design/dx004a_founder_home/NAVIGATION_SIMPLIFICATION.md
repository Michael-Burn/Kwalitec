# Navigation Simplification

**Programme:** DX-004A  
**Status:** Binding for Founder Home chrome interaction  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-002 `NAVIGATION_AUDIT.md`, `PRODUCT_ARCHITECTURE.md`; DX-003 terminology  

---

## Principle

Founder Home is **not** a place to browse.

| Job | Surface |
|---|---|
| Continue work | **Home** |
| Browse / create | **Subjects** |
| Open workspaces | **Curriculum Studio** |
| Reporting | **Reports** (under Settings) |
| Configuration | **Settings** |

In-page navigation that duplicates the sidebar is forbidden on Home.

---

## Target Console primary nav (≤6)

Per DX-002 Console tree, applied at Home:

```
Home
Subjects
Curriculum Studio
Students
Support
Settings
```

| Item | Role |
|---|---|
| Home | Decision surface (this programme) |
| Subjects | Catalogue |
| Curriculum Studio | Workspace list |
| Students | Participants catalogue |
| Support | Feedback queue |
| Settings | Config + nested ops/reports/search |

---

## Demote from Home and from equal-weight chrome

| Destination | Action |
|---|---|
| Attention Center | Nest under Support or Settings; link from Support — **not** Home Primary |
| Operations / Operational Health | Settings → Operations |
| Platform Intelligence / Alpha Observability | Settings → Intelligence |
| Findings | Support or Settings nested |
| Research / Analytics | Settings → Research |
| Vision Journal | Settings nested |
| Runtime Health / Evidence Gates / Releases / Internal Alpha | Settings → Operations |
| Search | Settings or shell utility — not Home Quick Action |
| Review Queue / Publishing / Versions / Quality hubs | Fold into Studio filters (DX-004B / Studio work) |

---

## Home-specific nav rules

1. **No Quick Actions section.**  
2. **No “Open X” buttons** that mirror sidebar labels.  
3. **No second Home** (legacy dashboard routes remain redirects only).  
4. **One Primary** — always publication Current Work (or Create Subject empty state).  
5. **Queue / Recent rows** are object links, not nav destinations to peer dashboards.  
6. **“View all in Subjects”** (if used) is text-weight only.

---

## Label changes on this surface

| Before | After |
|---|---|
| Console Home / Overview / Dashboard | **Home** |
| Manage content | *(removed — use Subjects / Studio)* |
| Review attention queue | *(removed as Home Primary)* |
| Participants (if linked) | **Students** |

---

## Cross-shell

- No student Education OS links as peer chrome on Home.  
- Account → student settings remains quiet (existing DX-002 rule).

---

## Success test

From Home, the Founder can Resume without opening a nav menu.

If they must use Quick Actions or Attention Center to start publishing, navigation simplification has failed.
