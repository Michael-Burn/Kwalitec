# Typography System

**Programme:** DX-001  
**Status:** Binding  
**Font family:** Inter (sole UI family) — see Brand Guidelines for wordmark exceptions  

---

## Philosophy

Large typography is **rare**.

Body text should dominate. Headings create structure; they do not decorate.

Oversized page titles as default chrome are a known Alpha defect. DX-001 corrects that policy for all future redesigns.

---

## Scale

| Role | Token name | Size | Weight | Line height | Tracking | Use |
|---|---|---|---:|---|---|---|
| **Display** | `type-display` | 32px / 2rem | 600 | 1.2 | −0.02em | Marketing, rare product moments (welcome, empty product shell). **At most one per major surface.** |
| **Page Heading** | `type-page` | 24px / 1.5rem | 600 | 1.25 | −0.015em | Screen title. One per page. |
| **Section Heading** | `type-section` | 18px / 1.125rem | 600 | 1.3 | −0.01em | Group label within a page. |
| **Body** | `type-body` | 16px / 1rem | 400 | 1.5 | 0 | Default reading and most UI copy. |
| **Supporting Text** | `type-support` | 14px / 0.875rem | 400 | 1.45 | 0 | Secondary labels, metadata, helper that survived content review. |
| **Caption** | `type-caption` | 12px / 0.75rem | 500 | 1.4 | 0.01em | Timestamps, table footnotes, legal microcopy. |

Monospace (`type-mono`) is reserved for codes, IDs, hashes, and technical identifiers — never for general UI.

---

## Hierarchy rules

1. **One Page Heading per screen.** Do not stack shell title + hero title saying the same thing.  
2. **Body dominates.** Most words on a screen are Body or Supporting Text.  
3. **Display is exceptional.** If every page uses Display, none feel premium.  
4. **Do not inflate weight to fake importance.** Prefer position and space over Bold everywhere.  
5. **Never use decorative heading sizes** (e.g. 40px page titles as default). Legacy UX-001 40 / 28 / 20 scale is **superseded** for redesigns.  
6. **Links and actions** inherit Body/Supporting size; colour and weight convey interactivity, not size inflation.

---

## Mapping from legacy UX-001 (breaking)

| UX-001 | DX-001 |
|---|---|
| Page title 40px | Page Heading **24px** (Display 32px only when justified) |
| Section title 28px | Section Heading **18px** |
| Card title 20px | Prefer Section Heading or Body **semibold**; avoid a fourth “card title” tier |
| Body 16px | Body **16px** (unchanged) |
| Caption 14px | Supporting Text **14px**; Caption **12px** for true micro |

---

## Colour of type

| Role | Default colour token |
|---|---|
| Page / Section / Display | Neutral primary text |
| Body | Neutral primary text |
| Supporting | Neutral secondary text |
| Caption | Neutral muted text |
| Destructive label | Danger |
| Success confirmation | Success |

Do not use brand gold for body or headings. Gold remains brand/achievement only (`BRAND_GUIDELINES.md`).

---

## Accessibility

- Body and Supporting Text: contrast ≥ WCAG AA against surface.  
- Do not rely on size alone for hierarchy when colour contrast fails.  
- Minimum interactive text: Supporting Text (14px); prefer Body for primary controls.
