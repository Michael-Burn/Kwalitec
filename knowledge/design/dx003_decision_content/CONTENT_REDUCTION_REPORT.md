# Content Reduction Report

**Programme:** DX-003  
**Release Candidate:** `RC-2026.07.29-01`  
**Method:** Template word samples + inventory classification + DX-002 density findings  
**Note:** Estimates for architecture planning — not a runtime string counter.

---

## Information density (selected screens)

| Screen | Headings | Paragraphs (est.) | Cards | Badges | Buttons | Status indicators | Nav choices | Current density | Target density | Expected reduction |
|---|---|---|---|---|---|---|---|---|---|---|
| Curriculum Workspace | 12–18 | 15–25 | 8–12 | 6–10 | 15–25 | 12–18 | 9 tabs + shell | **Very High** | Moderate | **~55–65%** elements |
| Console Overview | 8–12 | 6–10 | 10–14 | 4–8 | 8–12 | 8–12 | Shell + Quick Actions | **Very High** | Low–Mod | **~60–70%** |
| Studio hub (each) | 4–6 | 8–12 | 3–5 | 2–4 | 4–6 | 2–4 | Peer hubs | **High** | Low | **~50%** + hub collapse |
| Student Home | 6–10 | 10–18 | 5–8 | 4–8 | 5–9 | 6–10 | Shell | **High** | Low–Mod | **~45–55%** |
| History | 5–8 | 8–12 | 4–6 | 2–4 | 4–6 | 3–5 | Shell + Journal/Timeline | **High** | Low | **~50%** |
| Help | 8–12 | 20–40 | 2–4 | 1–2 | 3–5 | 1–2 | Shell | **High** | Low | **~60%** words |
| Login | 2–3 | 6–8 bullets | 1–2 | 1–2 | 1–2 | 1 | Auth | **Moderate** | Low | **~40%** |
| Choose Exam | 2–3 | 2–4 | 3–6 | 2 | 2 | 2 | Wizard | **Low–Mod** | Low | **~10–15%** |
| Session activity | 2–4 | 2–4 | 1–2 | 0–2 | 2–3 | 1–2 | Session | **Low–Mod** | Low | **~10%** |
| Begin Learning review | 5–8 | 6–10 | 3–5 | 0–2 | 2 | 1–2 | Wizard | **Moderate** | Low | **~35%** |

Density = competing visible content units in the first 1–2 viewports, not educational question difficulty.

---

## Word reduction (P0 path estimate)

| Surface | Current words (template sample incl. chrome text) | Target words | Δ |
|---|---|---|---|
| Student Home | ~3,290 (template; much dynamic) → visible ~800–1,200 | ~400–550 | **~50%** |
| Curriculum Workspace | ~1,430 template → visible ~1,000–1,400 | ~450–600 | **~55%** |
| Studio hub | ~386 → visible ~250–350 | ~80–120 | **~65%** |
| Console Overview | (view-model heavy) visible ~600–900 | ~200–300 | **~65%** |
| History | ~539 → visible ~400–500 | ~150–200 | **~55%** |

**P0 aggregate visible-word reduction: ~50–55%.**

Including P1 Help epistemology + Login bullets + Welcome modal + flash shortening: **product primary-path word reduction ~45–55%.**

---

## Highest-impact copy removals

1. **Curriculum Workspace** upload “never manage file IDs” + extracted-curriculum filler + Documents meta-tab + always-on readiness essays.  
2. **Studio hubs** repeated “Curriculum workflow” seven-step tutorial (×5 pages).  
3. **History** `HISTORY_EPISTEMOLOGY_BRIDGE` and Journal/Timeline teaching CTAs.  
4. **Student Home** multi-why stack + trust badges + greeting/welcome patterns.  
5. **Console Overview** Platform Summary + pulse timestamp essay + multi-Primary Quick Actions labels.  
6. **Help** memory-model and reflection-family ontology essays.  
7. **Operator `recover_flash`** pedagogical justifications (keep recovery; cut sermons).  
8. **Welcome modal** entire surface.  
9. **Login** six feature bullets.  
10. **CTA** “Publish Verified Curriculum” → **Publish**.

---

## Decision reduction (summary)

See `DECISION_DENSITY_AUDIT.md`.

| Path | Decisions now | Target | Δ |
|---|---|---|---|
| Publish subject (Workspace) | 6–9 | 1 per visit | **~70%** |
| Founder morning (Overview) | 4–6 | 1 | **~75%** |
| Student start study (Home) | 4–7 | 1 | **~70%** |

---

## Status message reduction

See `STATUS_SYSTEM.md`.

| Scope | Δ |
|---|---|
| Redundant status messages on primary paths | **~40–50%** |

---

## What not to cut

| Keep | Why |
|---|---|
| One why for Mission | Explainability standard |
| Blocking findings + recovery | Publication safety |
| Ready / Coming Soon | Catalogue decision |
| Support gate reason | Prevents unsafe enrolment |
| Confirm modal specificity | Destructive risk |
| Session focus line | Task clarity |

---

## Execution dependency

Word/decision reductions require **copy edits + IA consolidations** from DX-002 (hub merge, Overview decision surface, Home density). DX-003 specifies the content targets; DX-004 executes Founder surfaces first without claiming full student reduction until a student DX programme.
