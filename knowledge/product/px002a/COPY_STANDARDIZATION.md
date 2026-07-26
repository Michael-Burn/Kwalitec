# PX-002A — Copy Standardization

**Programme:** PX-002A — Trust & Friction Resolution
**Input:** `knowledge/product/px001/COPY_REVIEW.md`, backlog items T1-3, T2-5, T2-6, plus copy touched incidentally while implementing T2-1/T2-2/T2-3/T2-8.
**Principle applied:** clarity, brevity, confidence — never explain the obvious, never repeat the same fact in more than one place on a screen.

---

## 1. Reflection — value framing added, not just moved (T1-3)

**Before:** `session/components/reflection_card.html` asked for reflection with no explanation of why it exists or what happens to it. The only explanatory sentence in the product lived in Onboarding step 4, days before a student would ever reach Reflection again.

**After:** the reflection card itself now states, at the moment it matters, why the reflection is collected and what it feeds into — reusing the tone already proven in Onboarding ("It helps Kwalitec understand how the session felt and keeps tomorrow's guidance honest") rather than inventing new phrasing.

**Why this length, not shorter:** PR-001's thematic finding was "Reflection is appreciated in principle, skipped in practice" — the gap was trust in *purpose*, not verbosity. Adding one sentence of purpose is a copy addition that directly targets the finding; cutting it shorter would have re-created the original problem.

## 2. Sign-in — remove redundant branding, not remove information (T2-5)

**Before:** `auth/login.html` showed the logo lockup, then a separate "Kwalitec" headline directly beneath it, then two independent mentions of "Kwalitec coordinator" in the onboarding note.

**After:** the duplicate "Kwalitec" headline is removed (the lockup already carries the brand); "Kwalitec coordinator" is stated once.

**Copy fix during implementation:** the onboarding note was reworded to open with "Kwalitec is invite-only..." — tightening three separate ideas (invite-only access, coordinator invitation, how to get one) into one flow without dropping any of them.

## 3. Study Plan roadmap — one note instead of fourteen (T2-6)

**Before:** every one of 14 topic cards on `study_plan/view.html` individually repeated "Learning Outcomes: Not available yet."

**After:** one top-level note above the roadmap: "Learning Outcomes **Not available yet** for topics below." Same fact, stated once. Repetition at this scale reads as broken content, not as an honest disclaimer — removing the other 13 copies is a legibility fix, not a loss of information (the fact that outcomes aren't available yet is still stated, clearly, exactly once).

## 4. Numeric false precision (T2-6)

**Before:** the Dashboard "Time Status" card showed `remaining_hours` and hours surplus/deficit to two decimal places (e.g. "199.98 hours").

**After:** rounded to whole numbers for display. A study-hours estimate accurate to the minute reads as manufactured precision it does not actually have; rounding does not change the underlying computation (Runtime A untouched), only how many digits are shown to a student who cannot act on the second decimal place anyway.

## 5. Error pages — added guidance, not just recoloured (T2-7)

**Before:** `errors/404.html`, `403.html`, `500.html` showed a Reference ID in an off-brand colour with no explanation of what it is for.

**After:** restyled with a neutral/muted token, plus one added sentence telling the student what to do with the reference ID (quote it to support if they need help). The colour fix alone would have left the underlying copy gap PX-001 also implicitly flagged (a raw identifier with no stated purpose reads as a debug artefact, which is exactly the kind of implementation leakage this programme targets — see T2-1 and the Trust section of `FRICTION_RESOLUTION_MATRIX.md`).

## 6. Settings / Help — reframed as disclosure, not deleted (T2-1, T2-2)

Build date, environment, build number, commit hash, and raw user ID in Settings, and the release-info table in Help, were not deleted (a student who is asked for this by support still needs to find it) — they were moved behind a single collapsed "Diagnostic information" disclosure in both places, using the same pattern so a student who learns it once recognises it the second time. This is a copy-and-structure decision, not a data-removal decision: nothing that was previously visible is now unreachable, it is simply no longer the first thing a student sees on a routine visit.

## 7. Help — replaced a release table with topic guidance (T2-2)

**Before:** `alpha/help.html`'s primary content was a release-info table and four feedback buttons — no answer existed for an actual "how do I..." question.

**After:** a small, real set of popular-topic entries in the student's own language ("How is my study plan built," "What does readiness mean," "How do I change my exam"), each expandable rather than dumped as a wall of text, plus a search box to jump to a topic directly. Copy for each topic answers the question in the fewest sentences that remain honest — no filler paragraphs added to make the page look fuller.

## 8. Analytics — softened framing for a zero-history week (T2-3)

**Before:** a brand-new account with no study history still saw per-metric "needs improvement" copy ("Only studied 0 days — try for at least 5 days," etc.) under a warning-triangle icon — a list of failures on day one.

**After:** for a zero-history week, all per-metric copy is suppressed in favour of a single line ("No study activity recorded this week yet." / "Set up a study plan and begin your first mission to start tracking progress.") under a neutral icon. Once a student has any history, the original per-metric copy still applies unchanged — this is not a permanent softening of honest feedback, only a fix for the specific case where "feedback" would otherwise be manufactured from zero data.

## 9. Coach panel — remove duplication, not remove Coach (T2-8)

**Before:** Coach always rendered its own Why / Why now / Next / Benefit list even when the Mission card directly above it, on the same page, was already showing the same four fields from the same underlying data. Six of 20 PR-001 reviewers independently called this out as paraphrase rather than new information.

**After:** Coach's structured list only renders when the Mission card is *not* already showing it (guided-session and reflection states, where the Mission card's own explanation is not visible). Whenever the Mission card is visible with its explanation, Coach instead shows commitment status if there is any, or a one-line pointer back to the Mission card — never a second copy of the same four fields.

---

## Copy items reviewed and explicitly left unchanged

- **Empty-state copy on `student/home.html`** was touched only to fix a `REJECTED_SYNONYMS` violation ("study session" → reworded) and to keep the required "learning insights" phrase — the surrounding structure and tone were already compliant with `PRODUCT_LANGUAGE_GUIDE.md` §5's empty-state pattern (name what's missing + give the next step) and were not rewritten further.
- **`readiness_quality.py` / `recommendation_quality.py` `review_point` messages** were edited only to remove a "study session" synonym violation, not restructured — their underlying advice content is Runtime A output and out of this programme's scope.
