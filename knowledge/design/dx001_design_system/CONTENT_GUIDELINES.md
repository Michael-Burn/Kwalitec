# Content Guidelines

**Programme:** DX-001  
**Status:** Binding  
**Related:** `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` (product vocabulary)  

---

## Philosophy

Assume users understand software.

Replace paragraphs with:

- Good labels  
- Good hierarchy  
- Good naming  

If a sentence merely explains how to use the interface, **redesign the interface**.

---

## Voice

| Quality | Expectation |
|---|---|
| Tone | Calm, precise, professional |
| Person | Direct; prefer imperative for actions (“Continue”, “Publish”) |
| Intelligence | Respect expertise; no condescension |
| Length | Shortest accurate string |

Avoid: cheerleading, tutorial voice, fake urgency, enterprise jargon without meaning.

---

## Labels over paragraphs

| Prefer | Avoid |
|---|---|
| “Blocking errors: 3” | “Here you can see how many validation errors are currently blocking…” |
| “Study next” | “Your personalized recommendation for what you should study next today is…” |
| “Awaiting approval” | “This curriculum is waiting for an approver to review and approve…” |

One line of Supporting Text is allowed when risk or irreversibility requires it — not as default chrome.

---

## Naming

- Use product language consistently (Student Home, Mission, Curriculum Studio, Publish).  
- Do not expose implementation names (`workspace_id`, pipeline stage enums) in primary UI.  
- Match button label to outcome (“Publish”, not “Submit form”).  

---

## Explanatory text policy

| Keep | Cut |
|---|---|
| Consequence of a destructive action | How to click |
| Why empty (factual) | Marketing filler on empty states |
| Why this recommendation (educational explainability — concise) | Repeated coach paraphrases of the same fact |
| Legal / privacy required copy | Soft onboarding essays on every screen |

Educational explainability remains mandatory where product standards require it — but as **structured, concise explanation**, not tutorial walls. See Explainability Standard for student-facing intelligence; DX-001 constrains *presentation density*.

---

## Empty states

Exactly three beats:

1. **State** — what is empty  
2. **Why** — one short reason  
3. **Action** — one Primary (or clear Secondary if Primary is elsewhere)  

No tips carousel. No secondary metrics.

---

## Errors

- Say what failed  
- Say what to do next  
- Point to the field or object when possible  

Avoid blame and humour.

---

## Anti-patterns

- Double titles restating the same concept  
- Helper text under every field by default  
- “Welcome to your dashboard!” heroes  
- Tooltip novels  
- Status essays that belong in a detail panel  
