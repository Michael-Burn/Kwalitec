# Content Audit

**Programme:** DX-002  
**Release Candidate:** `RC-2026.07.29-01`  
**Classification:** Essential · Supporting · Redundant · Remove  
**Assumption:** Professional users. Do not explain obvious interactions.

---

## Policy (from DX-001)

- Labels over paragraphs  
- Empty states = why + next action only  
- No tutorial essays on operational screens  
- Educational explainability stays — but one layer, not six paraphrases  

---

## High-impact content findings

### Remove (priority)

| Location | Content | Why |
|---|---|---|
| History | “What History shows” epistemology paragraph + repeated Journal/Timeline pushes | Compensates for bad IA; redundant |
| Studio hubs | 7-step “Curriculum workflow” essay on every hub | Tutorial; repeated |
| Workspace | “Upload the official curriculum PDFs… never need to manage internal file IDs” | Explains non-problem to professionals |
| Workspace CIP | “Extracted curriculum ready for Founder review.” | Empty filler |
| Workspace Documents tab | Points user to Content Sources above | Meta-navigation as content |
| Help | Full journey ontology + memory model essays | Belongs in IA, not Help homepage |
| Login | Six feature bullets | Redundant with one value proposition |
| Console Home | “Operational pulse — what needs attention today · timestamp · timezone” | Mixes mission with L3 |
| Onboarding / Welcome modal | “Welcome to Kwalitec” | Forbidden welcome pattern |
| Review (C4) | Long sections for defaulted fields user never chose | Surprise content |

### Redundant (collapse)

| Location | Content | Action |
|---|---|---|
| Student Home | Greeting + Study Sensei + eyebrow + title | Keep title + optional one narrator line |
| Student Home | why_recommended + why_it_matters + benefit + coherence | One why; disclose rest |
| Revision | “Revision supports today's Mission — it is not a second Mission” | Supporting once; not repeated in Help |
| History empty | Explains Journal again | Point once |
| Console | Attention section title + Open Attention Center + attention CTA | One path |

### Supporting (keep, demote visually)

| Location | Content |
|---|---|
| Choose Exam | Ready / Coming Soon labels |
| Workspace | Next step label + text |
| Validation findings | why_it_matters + recovery_action (decision-critical) |
| Session | Learning objective / Focus line |
| Subject support gate | Blocking reason |

### Essential (keep as L0/L1)

| Location | Content |
|---|---|
| All screens | Page heading stating task |
| Student Home | Mission title + Primary CTA label |
| Choose Exam | Subject titles |
| Workspace | Subject title + stage Primary control labels |
| Login | Sign in + field labels |
| Errors | Short recovery instruction |

### Badges / status

| Badge | Classification | Note |
|---|---|---|
| Ready / Coming Soon | Essential | Catalogue |
| Blocking | Essential | Validation |
| Internal Alpha | Supporting | Once per shell, not repeated in every header + hero |
| Documents Uploaded / Replace | Supporting | Prefer button state over badge theatre |
| Trust / coherence badges on Home | Remove or L2 | Implementation of trust framework as chrome |
| Priority on Revision | Supporting | OK if quiet |

### Tooltips / helper text

| Pattern | Verdict |
|---|---|
| Wizard helper under H1 | Supporting if one line; Remove if restates H1 |
| Evidence search placeholder examples | Supporting |
| Settings diagnostic disclosure | L3 — hide by default |
| Help search hint | Supporting |

---

## Heading audit (patterns)

| Pattern | Occurrences | Verdict |
|---|---|---|
| Oversized page titles (legacy 40px intent) | Console/Studio section-title pattern | DX-001: 24px Page Heading — fix in visual DX |
| Multiple H2 before Primary CTA | Student Home, History, Help | Reduce |
| Section titles that restate nav | “Curriculum workflow”, “What History shows” | Remove |

---

## Content principles for DX-003

1. If Help must explain two screens’ difference, merge the screens.  
2. If copy says “you never need to…”, delete the feature anxiety and the sentence.  
3. One narrator voice line maximum in L0.  
4. Status messages: change in state only — not permanent decoration.  
5. Defaults on Review: one line “Applied defaults” — not full fake-choice sections.
