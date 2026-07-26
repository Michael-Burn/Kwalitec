# PX-002B — Microcopy Review

Scope: sentences rewritten or added in this programme, and copy explicitly
reviewed and kept. PX-002A's `COPY_STANDARDIZATION.md` and `COPY_REVIEW.md`
cover the terminology and copy work done in the prior programme; this
document covers only what changed in PX-002B.

## Rewritten

| Location | Before | After | Why |
|---|---|---|---|
| Journey — true empty state | "Your learning path will appear here." | "Your journey will take shape after your first session" / "Once you complete a study session, we'll map your path — current topic, what's done, and what's next." | Original was a flat statement with no encouragement or next step. New copy explains *why* it's empty and *what happens next*, per the brief's empty-state rule. |
| Revision — true empty state | "Revision options will appear when available." | "Revision opens up after your first session" / "Once you've studied a topic, we'll surface the revision that will help you the most." | Same rationale — passive "will appear" replaced with a confident, causal explanation. |
| History — true empty state | "Your educational progress will appear here." | "Your history starts with your first session" / "Study time, readiness trends, and completed topics will appear here as you go." | Same rationale, and previews *what* will show up so the emptiness feels intentional rather than broken. |
| History — no sessions sub-empty | "No completed sessions yet." | "No sessions completed yet" / "Finish a study session and it will show up here, with what you covered and how it went." | The banned "No data."-style phrasing replaced with guidance toward the next action. |
| Study Plan roadmap — time metric label | "Est. Hours" + "0.8h" style value | "Estimated time" + "1 hour 30 min" style value | Removes both the abbreviation and the false decimal precision; matches the duration phrasing used everywhere else in the product (Home, Mission, Session Overview). |

## Reviewed and kept as-is

| Location | Copy | Why it was kept |
|---|---|---|
| `session_practice_outcome.html` eyebrow | "Practice Outcome Capture" | Reads as internal terminology, but it is the formal, test-pinned name of a shipped capability (LXP-003) across three test suites. Rewriting it would require a coordinated rename across engineering + tests, which is outside a copy-only pass. Flagged as a known limitation rather than silently left. |
| "Back to Today's Study Session" link text | Unchanged text, demoted from button to link (see `SCREEN_STANDARDIZATION_REPORT.md`) | The words were already clear and human; the problem was visual weight, not wording. |
| Revision "no revision focus yet" empty message | Service-provided `revision.empty_message`, default "No revision focus is ready yet. Check back after your next session." | Already calm, confident, and precise; already has a CTA. No rewrite needed. |
| Help search no-results copy | "No topics match that search. Try a different word, or use Quick actions below." | Already meets the bar (human, guides next step); only the accessibility wiring around it changed in this pass. |

## Copy principles applied

Every rewrite in this pass followed the same test used in PX-002A:

- **Human** — no "N/A", no system jargon, no passive-voice hedging.
- **Confident** — states what *will* happen, not what *might*.
- **Calm** — no exclamation points, no urgency manufactured where none exists.
- **Precise** — says exactly what will appear and when, not a vague
  reassurance.

No copy was rewritten purely for tone — every change above ties to a
concrete gap (missing CTA context, banned "No data." phrasing, or false
numeric precision) named in `PREMIUM_UI_AUDIT.md` or the PX-002B brief.
