# Navigation Boundaries

**Programme:** DX-004B  
**Status:** Binding for Founder Operating System ownership  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-002, DX-004A, this programme  

---

## 1. Ownership map

| Surface | Owns | One question |
|---|---|---|
| **Home** | Continuation | What should I work on next? |
| **Subjects** | Discovery | Which subject do I want to work on? |
| **Workspace** | Execution | How do I advance this curriculum? |
| **Review** | Verification | Is this ready? |
| **Publish** | Release | Can this release? |

Responsibilities must **never** overlap.

---

## 2. Subjects owns discovery

Subjects is the **only** catalogue for curriculum objects.

| Allowed on Subjects | Forbidden on Subjects |
|---|---|
| Browse / search / filter subjects | Publication queue as Home-style L0 |
| Create Subject (sole Primary) | Ops Attention / Support inbox |
| Open → Workspace | Platform statistics |
| Quiet metadata | Second catalogue pages for the same objects |

No other page may become a competing catalogue.

---

## 3. Home owns continuation

Per DX-004A:

- Home presents **Current Work** + attention queue + recent publications  
- Home Primary resumes publication work  
- Home may link **View all in Subjects** (text) — does not re-implement the catalogue  

Subjects must not replicate Home’s “what next” Current Work hero.

---

## 4. Workspace owns execution

- Pipeline stages, uploads, validation, approval actions live in Workspace  
- Open from Subjects is a **transition**, not a summary stop  
- DX-004C redesigns Workspace; DX-004B only requires immediate entry  

Subjects rows must not host execution Primaries (Validate / Publish buttons).

---

## 5. Review owns verification

| Form | Allowed |
|---|---|
| Review as **workspace stage** | Yes |
| Review as **filter** on Subjects or Studio list | Yes (preset) |
| Review as **peer catalogue page** of all subjects | **No** — competing catalogue |

---

## 6. Publish owns release

| Form | Allowed |
|---|---|
| Publish as **workspace stage** | Yes |
| **Ready to publish** filter on Subjects | Yes |
| Publish hub as second catalogue | **No** |

---

## 7. Curriculum Studio boundary

| Studio role | Boundary |
|---|---|
| Workspace list / tooling entry | May list workspaces with filters |
| Subject catalogue of record | **Subjects** — Studio must not become the primary subject browser |
| “Open Curriculum Studio” as Subjects Primary | **Forbidden** |

If Studio shows workspaces, it is an execution index — not a second Subjects with Create + tutorial hubs.

---

## 8. Legacy hub collapse

| Remove as nav destinations | Replace with |
|---|---|
| Review Queue hub page | Filter / workspace stage |
| Publishing hub page | Ready to publish filter / Publish stage |
| Versions hub page | Subject More → History / versions |
| Quality hub page | Workspace findings / Support |

Shell nav stays ≤6 primary items (DX-002 / DX-004A).

```
Home
Subjects
Curriculum Studio
Students
Support
Settings
```

---

## 9. Cross-links (allowed)

| From | To | Affordance |
|---|---|---|
| Home | Subjects | Text “View all in Subjects” |
| Home empty | Subjects Create | Primary Create Subject |
| Subjects | Workspace | Open (row) |
| Workspace | Subjects | Shell nav only (no duplicate local “back to hub” chrome required beyond standard back) |
| Subjects | Home | Shell nav |

No in-page Subjects local nav duplicating the shell.

---

## 10. Success test

Ask: “Where do I find a subject?” → **Subjects** only.  
Ask: “Where do I continue today’s publish?” → **Home**.  
Ask: “Where do I validate?” → **Workspace** (Review).  
If answers point at five hubs, boundaries failed.
