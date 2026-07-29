# Content Style Guide

**Programme:** DX-003  
**Status:** Binding for redesign programmes  
**Release Candidate:** `RC-2026.07.29-01`  
**Supersedes (tone density):** ARP-004 “encouraging” default where it conflicts with quiet professionalism  
**Aligns nouns with:** `TERMINOLOGY_DICTIONARY.md`

---

## Philosophy

Professional. Quiet. Confident. Respectful. Precise.

The product explains only what cannot be inferred from labels, hierarchy, and state.

---

## Voice

| Do | Do not |
|---|---|
| Imperative for actions (“Publish”, “Continue”) | Cheerleading (“Great job!”, “You’re crushing it”) |
| Shortest accurate string | Tutorial paragraphs under controls |
| Direct, adult address | Childish, playful, sales language |
| Specific object names (“CS1 published”) | Vague (“Your content is live!”) |
| Silence when state is obvious | Narrating every idle status |

### Forbidden tones

- Playful  
- Childish  
- Over-encouraging  
- Over-explanatory  
- Sales / marketing  
- Fake urgency  
- Apology humour (“Oops”)  

---

## Design principles (content)

### 1. Decision before description

Replace explanations with decisions.

| Bad | Good |
|---|---|
| “Upload your syllabus so the platform can begin analysing…” | Upload Syllabus |
| “This section lets you review findings before approval…” | Review findings |

### 2. Labels before paragraphs

If a paragraph exists only to explain controls, redesign the controls — do not keep the paragraph.

### 3. Silence is acceptable

Whitespace beats unnecessary words. Empty space is not a defect.

### 4. Every screen has one sentence

See `DECISION_ARCHITECTURE.md`. One line. No wrapping.

---

## Grammar & form

| Element | Rule |
|---|---|
| Buttons | Title Case, verb-led, outcome-matched |
| Page titles | Noun or short imperative stating the job |
| Supporting text | Max one line in L0; risk/legal only by default |
| Lists | Prefer labels + values over prose |
| Truncation | Prefer shorter copy over ellipsis theatre |

---

## Helper text policy

Every helper paragraph must justify itself.

| Allowed | Not allowed |
|---|---|
| Legal / privacy | UI tutorials |
| Compliance | Obvious instructions |
| Risk / irreversible consequence | Marketing copy |
| Critical educational explanation (one layer) | Repeated explanations of the same concept |

Educational explainability remains mandatory where product standards require it — as **one concise why**, not six paraphrases.

---

## Forbidden content (product UI)

Remove:

- Welcome messages  
- Congratulations banners  
- Tutorial paragraphs  
- Repeated headings  
- Duplicate statuses  
- Decorative quotes  
- Generic motivational text  
- Excessive tooltips  
- Multiple explanations of the same concept  
- Implementation terminology in L0 (`workspace_id`, ms timings, retrieval profiles, pipeline enums)  

---

## Attribution

| Audience | Naming |
|---|---|
| Student | Study Sensei named once in Home hero chrome; Guidance elsewhere without re-attribution |
| Founder | No mentor voice; operational labels only |

---

## Relationship to prior guides

| Source | Role after DX-003 |
|---|---|
| DX-001 `CONTENT_GUIDELINES.md` | Visual-system content principles; still binding |
| `PRODUCT_LANGUAGE_GUIDE.md` | Historical noun table — superseded where DX-003 dictionary / tone is stricter |
| `product_language.py` | Implementation constants — update in DX-004+ to match dictionary |

---

## Checklist before shipping copy

1. Can the control label carry the meaning alone?  
2. Does the screen still have exactly one Decision?  
3. Is Feedback ≤ one short sentence (success) or three beats (error)?  
4. Is every status actionable or removable?  
5. Would a senior professional find any sentence condescending or tutorial-like? If yes, delete.
