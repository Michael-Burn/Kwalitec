# Content Inventory

**Programme:** DX-003  
**Status:** Binding content map  
**Release Candidate:** `RC-2026.07.29-01`  
**Classification:** Keep · Rewrite · Merge · Delete · Unknown  
**Sources:** Live templates + DX-002 `CONTENT_AUDIT.md` + `product_language.py` constants  

Nothing survives because it has “always been there.”

---

## Legend

| Class | Meaning |
|---|---|
| **Keep** | Necessary for Decision / Action / Feedback or legal/risk/education |
| **Rewrite** | Keep intent; shorten or relabel to DX-003 style |
| **Merge** | Combine with another element; one survivor |
| **Delete** | Remove; silence or control redesign replaces it |
| **Unknown** | Needs product owner call in DX-004 (flagged; default lean toward Delete) |

---

## P0 — Curriculum Workspace (`workspace.html` + guidance)

| Content | Class | Rationale |
|---|---|---|
| Subject title | Keep | Recognition |
| Next step label + one line | Rewrite | Keep; cut essay length |
| Stage Primary CTAs (Upload, Validate, Preview, Approve, Publish…) | Rewrite | Align verbs to dictionary; one Primary visible |
| “Upload the official curriculum PDFs… never need to manage internal file IDs” | Delete | Anxiety tutorial |
| “Extracted curriculum ready for Founder review.” | Delete | Filler |
| Documents tab pointing to Content Sources above | Delete | Meta-navigation |
| Workflow card / full stage essay | Delete | Stage chrome + Primary suffice |
| Readiness KPI triad (validation/preview/checklist essays) | Merge | One compact readiness row or stage gate only |
| Blocking findings + why_it_matters + recovery_action | Rewrite | Keep decision-critical; shorten why to one line |
| Pipeline jobs with ms timings | Delete (from L0) | Advanced only |
| Entity id / embedding / retrieval profiles | Delete (from L0) | Implementation |
| CIP 9 tabs always visible | Merge | ≤3 stage panels |
| Actions grid (many buttons) | Merge | One Primary + overflow |
| Version assign control | Keep | When stage requires |
| Flash success essays | Rewrite | Per success guide |
| `recover_flash` long forms | Rewrite | Problem → Reason → Action |

---

## P0 — Console Overview

| Content | Class | Rationale |
|---|---|---|
| Page title Overview | Keep | |
| “Operational pulse — what needs attention… timestamp · timezone” | Delete | Mission + L3 mashup |
| Version / build in L0 eyebrow | Delete | L3 |
| Attention KPI cards (4) | Merge | Attention list |
| Platform Summary KPI cards (4) | Delete | Non-decision |
| Quick Actions multi-Primary | Merge | One Primary to top item |
| Attention list rows | Keep | Decision fodder |
| Operational detail cards | Delete / Merge | Into Operations report |
| Curriculum shortcuts | Rewrite | Quiet L2 links |

---

## P0 — Studio hubs (`hub.html` × Subjects + duplicates)

| Content | Class | Rationale |
|---|---|---|
| “Curriculum workflow” 7-step essay | Delete | Repeated tutorial |
| Create Subject form | Keep | Decision |
| Open Workspace control | Keep | Decision |
| “Open Curriculum Studio” CTA on Subjects | Delete | Wrong job / nav duplicate |
| Hub pages Review / Publishing / Versions / Quality | Merge | Filters inside Studio |
| Subject / workspace lists | Keep | Catalogue |
| Ready / status chips on rows | Rewrite | Per status system |

---

## P0 — Student Home

| Content | Class | Rationale |
|---|---|---|
| Mission title | Keep | Decision object |
| Start / Continue Primary | Keep | Action |
| Greeting / welcome line | Delete | Forbidden welcome |
| Study Sensei eyebrow + hero narrator | Merge | Name Sensei once; one narrator line max |
| Duration | Keep | L1 context |
| why_recommended | Keep (one) | Educational explainability |
| why_it_matters / benefit / coherence stack | Merge | Single “Why this?” disclosure |
| Trust / coherence badges | Delete | L0 chrome |
| Readiness / countdown cards | Delete / Merge | Journey |
| Secondary CTAs (tutor, defer, mark complete) | Merge | Overflow / menu |
| Day-complete congratulations | Delete | Quiet state |
| `HOME_SENSEI_NAMING_POLICY` | Keep (policy) | Enforce in UI |
| `REVISION_MISSION_PRIMACY` on Home | Delete | Belongs once on Revision |

---

## P1 — History / Journal / Timeline / Help

| Content | Class | Rationale |
|---|---|---|
| `HISTORY_EPISTEMOLOGY_BRIDGE` paragraph | Delete | Compensates bad IA |
| History KPI cards | Delete | Non-decision |
| Dual Open Journal / Timeline CTAs | Merge | One Progress entry (DX-002) |
| Session archive list | Keep | |
| `EDUCATIONAL_MEMORY_MODEL_SENTENCE` on Help | Delete | IA, not Help homepage |
| `REFLECTION_FAMILY_MAP_SENTENCE` on Help | Delete / Merge | One-shot orientation max |
| Help search + contact | Keep | Unblock job |
| Welcome modal | Delete | Forbidden |

---

## P1 — Login / Onboarding / Review

| Content | Class | Rationale |
|---|---|---|
| Sign in + fields | Keep | |
| Six feature bullets | Delete / Rewrite | ≤ one value sentence |
| Alpha badge repeats | Merge | Once |
| Onboarding “Welcome to Kwalitec” | Delete | |
| Onboarding Continue | Keep | |
| Skip / Help equal CTAs | Merge | One secondary |
| Review defaulted fields user never chose | Merge | One “Applied defaults” line |
| Begin Learning Primary | Keep | |

---

## Student planning & session (lean)

| Content | Class | Rationale |
|---|---|---|
| Choose Exam subject titles + Ready/Soon | Keep | |
| Wizard helpers restating H1 | Delete | |
| Support gate blocking reason | Rewrite | Problem → Action |
| Session learning objective / focus line | Keep | |
| Session activity controls | Keep | |
| Reflection prompts | Rewrite | Short; no cheerleading |
| Return Home | Keep | |

---

## Product language constants

| Constant | Class | Notes |
|---|---|---|
| `APPROVED_TERMS` | Rewrite | Align with dictionary; drop redundant reflection variants from L0 |
| `STUDENT_PRIMARY_CTAS` | Keep | |
| `FOUNDER_STUDIO_CTAS` | Rewrite | Shorten “Publish Verified Curriculum” → **Publish** |
| `FOUNDER_PRIMARY_NAV_LABELS` | Merge | Drop Review Queue / Publishing / Versions / Quality as peers (DX-002) |
| `REJECTED_SYNONYMS` | Keep | Enforce |
| Long memory / epistemology sentences | Delete from UI surfaces | May remain in docs |

---

## Operator flashes (`FLASH_SUCCESS` / `FLASH_WARNING`)

| Pattern | Class |
|---|---|
| Multi-sentence success with student consequence | Rewrite → outcome label |
| Multi-sentence gate warnings with pedagogy | Rewrite → Problem → Reason → Action |
| Specific field pointing | Keep intent |

---

## Unknown (default Delete unless owner keeps)

| Item | Question |
|---|---|
| Product Check-in thank-you prose | Celebrate or quiet “Submitted.”? |
| Vision Journal copy | In Alpha nav at all? |
| Calibration instructional paragraphs | Required for validity of prior-coverage? |
| Evidence Gates page titles vs nested labels | Rename only? |

---

## Inventory counts (approximate)

| Class | Items tagged (primary surfaces) |
|---|---|
| Keep | ~95 |
| Rewrite | ~70 |
| Merge | ~45 |
| Delete | ~85 |
| Unknown | ~8 |

**Delete + Merge dominate P0** — consistent with ~50% word reduction target.
