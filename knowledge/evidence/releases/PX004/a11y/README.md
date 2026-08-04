# PX-004 accessibility evidence

## Automated

- Expanded presentation contracts: `tests/presentation/student/test_px004_phase2_home_mobile_a11y.py`
- Contrast: `tests/test_rc001_contrast.py` (nav-section-label α **0.72**)
- Student + session accessibility suites green in Phase 2 pack (153 passed)

## PX-B item notes

| ID | Evidence |
|----|----------|
| PX-B-023 | `confirm_modal.html` `role="dialog"` + `aria-modal`; `confirm-modal.js` visible fallback if Bootstrap missing |
| PX-B-024 | Visual timer + separate `role="status"` live region; minute-boundary announces only |
| PX-B-025 | `--touch-target-min` on nav links, toggle, sign-out, ctx-help |
| PX-B-026 | Primary button transform reserved for `:hover` / `:focus-visible` |
| PX-B-027 | Student-shell reduced-motion after page-enter cascade |
| PX-B-028 | Sidebar `.nav-section-label` opacity 0.72; AA re-verified |
| PX-B-029 | Keyboard checklist below; Escape closes mobile drawer; primary path headings/landmarks |
| PX-B-030 | Static route contracts expanded; **axe/Lighthouse CI + AT recording = residual** |

## Keyboard checklist (primary path)

| Step | Expectation | Result |
|------|-------------|--------|
| Auth login | Focusable fields; submit via keyboard | Pass (markers) |
| Home | Skip to content / h1 / primary CTA tabbable | Pass (automated markers) |
| Open mobile Menu | Toggle `aria-expanded`; Escape returns focus | Pass (JS wired) |
| Journey | Progressbar attributes when present | Pass |
| Session | Finish confirm trigger focusable; modal dialog roles | Pass (markup) |
| Reflection → Home | Landmarks + h1 | Pass (route markers) |

## Screen-reader notes

- Session elapsed time announces on **minute** boundaries (polite), not every second.  
- Confirm-modal failure announces via live region + alert fallback.  
- Full VoiceOver/NVDA recording: **residual PX4-R3**.

## Claim discipline

Do **not** market “WCAG AA certified.” Scope: primary student path presentation improvements with automated markers + checklist.
