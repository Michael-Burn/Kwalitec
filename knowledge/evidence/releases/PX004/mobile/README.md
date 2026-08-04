# PX-004 mobile evidence

## Decision (PX-B-036) — provisional Founder ratification

**Canonical pattern:** compact **topbar drawer**

- Desktop / wide: horizontal inline `student-nav-link` row  
- Mobile (max-width 767.98px): `Menu` toggle opens absolute drawer panel (`data-mobile-nav="drawer"`)  
- Sign-out remains in topbar  
- No bottom tab bar; no dual product strategy (PX-X-04 parked)

Markup: `app/templates/student/components/navigation.html`  
CSS: `app/static/css/student/student.css`  
JS: `wireCompactNav()` in `student.js` (Escape + outside click)

## Live device evidence (PX-B-037)

| Capture | Status |
|---------|--------|
| Phone screenshot pack | Protocol in `../screenshots/README.md` — **pending Founder dogfood** |
| Tablet screenshot pack | Same |
| Defects from live capture | None filed yet — close under residual PX4-R1 |

Engineering verified responsive CSS/media queries and automated nav markers. Live-device PASS awaits Founder captures.
