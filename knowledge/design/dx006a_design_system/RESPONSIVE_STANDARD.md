# Responsive Standard

**Programme:** DX-006A  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  

---

## 1. Principle

One component definition. Responsive **behaviour**, not separate component variants — unless the catalogue records a justified exception.

---

## 2. Breakpoints

| Band | Width | Default columns |
|---|---|---|
| Mobile | &lt; 768px | 4 |
| Tablet | 768–1023px | 8 |
| Desktop | ≥ 1024px | 12 |

Tokens: `DESIGN_TOKEN_SPEC.md` § Breakpoints.

---

## 3. Layout rules

| Rule | Detail |
|---|---|
| Mobile-first | Base styles = mobile; enhance upward |
| No horizontal scroll | Except intentional code/table overflow with accessible scroll |
| Stack by default | Stack / Section vertical rhythm; Grid only when columns earn space |
| Primary survives | Primary Action remains visible without hunting; may go full-width on mobile |
| Persistent context | May compress to two lines; must not disappear |
| Tables | Horizontal scroll region OK; prefer priority columns on mobile |
| Shell | Sidebar collapses to overlay/drawer on mobile; no duplicate in-page nav |

---

## 4. Containers

| Surface type | Preferred container |
|---|---|
| Reading / Session content | `narrow` or `content` |
| Catalogues / tables | `wide` or `content` |
| Shell | `full` for chrome; content inset by container |

---

## 5. Typography & spacing

- Type roles do not shrink below Caption for UI labels.  
- Page Heading may remain 24px; do not invent a mobile-only display size.  
- Section gaps may step down one token on mobile (e.g. `space.6` → `space.5`) without inventing new values.

---

## 6. Touch & pointer

- Touch targets ≥ `shell.touch-target-min`.  
- Hover styles are additive; functionality must not depend on hover (tooltips need focus/labels on mobile).

---

## 7. Component variant policy

| Allowed | Not allowed |
|---|---|
| Responsive CSS on one Button | `ButtonMobile` / `ButtonDesktop` forks |
| Table → priority column hide | Separate MobileCardGrid for same data as vanity |
| Sidebar → drawer | Second nav tree on the page |

Exceptions require catalogue note + Guardian approval.

---

## 8. Verification

- [ ] 320px / 375px / 768px / 1024px / 1280px smoke  
- [ ] Primary reachable without zoom  
- [ ] No overlapping sticky header + Primary  
- [ ] Empty / Error states readable on narrow  

---

*Release Candidate: RC-2026.07.29-01*
