# PX-001 — Product Language Audit

**Programme:** PX-001 Product Experience Elevation  
**Date:** 2026-07-31

---

## Rules applied

Short. Confident. Helpful. Never verbose, academic, technical, or repetitive.  
Every sentence must help the user make a decision.

---

## Rewrites shipped

| Surface | Before (character) | After |
|---------|--------------------|-------|
| Home empty | Explains Study Plan unlock + “Home answers…” | “Choose an exam” · “Pick your exam to unlock today’s Session.” |
| Revision support | “What deserves my attention?” + Mission primacy essay | “Strengthen what you practised.” |
| History support | Long accomplishment essay + memory bridge | “Your practice record.” |
| Learning Journey | “What kind of learner…” + anti-dashboard essay | “How your learning has developed.” |
| Forecast framing | Disclaimer essay | “Where practice is taking you.” |
| Settings intro | “How Kwalitec works for you” + History lecture | “Settings” · preferences line |
| Footer | Philosophy slogan | “Study with focus.” |
| Journal / Timeline intros | Multi-sentence memory model | One guiding line each |
| Founder Students | “Participants” + Alpha-loop essay | “Students” · activity line |
| Feedback | Hub implementation essay | “Review student feedback across sources.” |
| Product Check-in | Cross-hub explanation | “Triage Product Check-in submissions.” |
| Console Settings | “Operator configuration…” | “Account, version, and Console destinations.” |
| Studio index | “advance curriculum publication” | “Open a workspace to publish.” |

---

## Language still reserved for Help

Help remains the place that may teach Decision Journal, Educational Timeline, and Sensei reflection vocabulary (RR-001.3C). Primary study surfaces no longer restate that model.

Canonical constants in `app/presentation/product_language.py` remain for coherence tests; UI usage is reduced.

---

## Banned on primary surfaces (enforcement list)

- Runtime A / Runtime C / dual-run / RIS
- “Operator,” “epistemology,” “implementation,” “aggregation”
- Milestone IDs (PB-001, DX-004, …)
- “Feedback Loop” as a student-facing product label
- “Why this is empty”
- Screens explaining their own IA (“This page answers one question…”)

---

## Residual

Founder secondary pages (Runtime Health, Evidence Gates, Platform Intelligence) still contain engineering language. They stay nested under Settings until Founder Validation prioritises a deeper Console language pass.
