# DOC-001 — Welcome Pack Design Knowledge Pack

**Programme:** DOC-001  
**Nature:** Research & consolidation only — not a Welcome Pack design  
**Audience:** Professional designers / ChatGPT publication design  
**Status:** Single source of truth for Early Access Welcome Pack creative brief inputs  
**Compiled:** 2026-08-04  
**Constraint:** Every statement below is traceable to repository evidence. Where evidence is absent: **Not found in repository.**

---

## How to use this pack

This document is a **creative brief dossier**, not artwork.

| Do | Do not |
|----|--------|
| Treat cited paths as authoritative | Invent colours, fonts, claims, or features |
| Prefer under-claim language from §8 | Declare Version 1 production-ready or pass guarantees |
| Use approved logo masters from §2 / §11 | Trace, redraw, or typeset a competing logo |
| Reuse Early Access copy patterns from §6 / §12 | Treat CMP syllabus PDFs as brand publications |

**Related programmes (ops context, not design assets):** REL-001 · OP-001 · OP-002 · EA-001 · EF-001 · PX-001 / BI-000 · Claim Standard P-003.5.

---

## 1. Brand Philosophy

### 1.1 Mission

| Source | Statement |
|--------|-----------|
| `knowledge/product/vision/PRODUCT_VISION_2030.md` | “Our mission is not to teach students. Our mission is to help students become professionals.” |
| `knowledge/design/BRAND_GUIDELINES.md` | “Kwalitec helps learners build mastery through structured curriculum, clear progress, and quality-first study.” |
| `PROJECT_CONTEXT.md` | Product thesis: **Reduce decisions. Increase learning.** |
| `knowledge/product/COMPETITIVE_POSITIONING.md` | UVP: “Reduce decisions. Increase learning — with curriculum-first structure, deterministic educational intelligence, and explanations you can believe.” |

### 1.2 Vision

From `knowledge/product/vision/PRODUCT_VISION_2030.md`:

> To become the world's most trusted AI-powered learning platform for professional qualifications.  
> Not by replacing teachers. Not by replacing textbooks.  
> But by becoming the intelligent companion every serious student wishes they had.

**Long-term ambition (2030):** become “the operating system for professional learning” — multi-profession, multi-qualification, multi-country — centred on helping people become competent professionals. Same source.

### 1.3 Purpose (four daily questions)

Every student deserves to know (`PRODUCT_VISION_2030.md`):

1. What to study.  
2. Why it matters.  
3. Whether they understand it.  
4. What they should do next.

**North star:** Students who consistently use Kwalitec should have a materially higher probability of passing their examinations than students who do not.  
**Daily design expression of the north star:** “What is the highest-value thing this student should do next?”

### 1.4 Core values / principles (named lists)

A single marketing “core values” poster list was **Not found in repository.**

Use these constitution-level principles instead:

| Cluster | Principles | Path |
|---------|------------|------|
| Product philosophy | Measures learning, not activity | `PRODUCT_VISION_2030.md` |
| AI | Transparent, explainable, evidence-based, educationally defensible | Same |
| Educational behaviours | Consistency, immediate feedback, reflection, intelligent revision, gradual confidence, understand mistakes | Same |
| Experience | Never lost / overwhelmed / judged / confused; always guided / supported / confident / motivated | Same |
| Never-build | Complexity without learning gain; artificial gamification; opaque AI; unhealthy habits; activity-over-mastery metrics | Same |
| Operating constitution | Student trust > feature count; marketing ≤ verified evidence; deterministic educational cores; advice remains advisory | `knowledge/operations/oa001/PRODUCT_CONSTITUTION.md` PC-01…PC-12 |
| Product principles | Evidence before inference; explain every decision; respect uncertainty; quality over quantity; student trust first | `knowledge/product/PRODUCT_PRINCIPLES.md` |
| Brand feel | Simple, modern, premium, minimal, timeless — “at home beside Stripe, Linear, Notion, GitHub, Vercel, and Figma” | `knowledge/design/BRAND_GUIDELINES.md` |

### 1.5 Personality

| Voice | Evidence |
|-------|----------|
| **Study Sensei** — trusted professional guide for learning decisions | `knowledge/product/STUDY_SENSEI_PHILOSOPHY.md`, `EA002_TUTOR_VOICE_GUIDE.md`, `knowledge/product/TONE_OF_VOICE.md` |
| Quiet professional warmth — not cheerleader, drill sergeant, or chatbot | `TONE_OF_VOICE.md` |
| Mentor / Education Operating System, not documentation dump | `PRODUCT_EXPERIENCE_GUIDELINES.md`, `app/static/branding/README.md` (brand hierarchy: Kwalitec → Education Operating System → value prop → supporting copy) |
| Guidance multiplies external content; does not replace CMP / textbooks | `knowledge/product/GUIDANCE_OVER_CONTENT.md`, `EC001_CMP_PARTNERSHIP_AUDIT.md` |

### 1.6 Desired emotional response

Students should **always feel** (`PRODUCT_VISION_2030.md`): guided, supported, confident, motivated.  
Students should **never feel**: lost, overwhelmed, judged, confused.

Early Access trust checkpoints (`OP002_PARTICIPANT_JOURNEY.md`): avoid expectation mismatch, lockout panic, “will this make me pass?” over-trust, guilt from missed days.

### 1.7 How Kwalitec differs from competitors

Authoritative positioning: `knowledge/product/COMPETITIVE_POSITIONING.md`, `knowledge/product/DIFFERENTIATORS.md`, `STUDY_SENSEI_PHILOSOPHY.md`.

| Versus | Kwalitec stance |
|--------|-----------------|
| Question banks | Highest-value next action + syllabus truth, not practice volume |
| Flashcard / SR apps | Spaced revision inside curriculum-bound missions, not decks-as-product |
| Traditional LMS | Student-first decision companion, not institution course shells |
| Generic AI tutors | Deterministic, explainable educational authority — no opaque chat ranking |
| Teachers / tutors | Complements them; never claims to be a person or substitute educator |
| Spreadsheets / Notion | Must beat DIY trackers on daily clarity and honesty |

**Ambition on map:** occupy **high educational honesty × high decision support**.

### 1.8 What we will never build (design implication)

From Vision Never-Build + DX manifesto: no gamification theatre, KPI vanity, opaque AI, unhealthy intensity encouragement, decorative dashboard chrome. Design should feel like a calm professional tool, not an engagement product.

---

## 2. Brand Identity

### 2.1 Official logo — authoritative display mark

| Role | Path | Notes |
|------|------|-------|
| **Live UI / display single source of truth** | `app/static/assets/branding/approved-kwalitec-logo.png` (1418×372) | `app/static/assets/branding/README.md`, `app/static/branding/README.md` — do not recreate in SVG/CSS/HTML for app UI |
| Navy canvas variant | `app/static/assets/branding/approved-kwalitec-logo-on-navy.png` (1774×887) | Same README |
| Final Approved master archive | `app/static/assets/branding/original/Final-Approved-Kwalitec-Logo.png` (1774×887) | Unaltered archive |
| Archive / optimised copies | `original/Approved-Kwalitec-Logo.png`, `original/Approved-Kwalitec-Logo-optimised.png` | Same family |

**UI rules** (`brand.css`, branding READMEs): never stretch; never apply CSS filters/tints; preserve aspect ratio; clear space via padding only.

### 2.2 Logo philosophy (symbol meaning)

From `knowledge/design/BRAND_GUIDELINES.md`:

| Component | Meaning |
|-----------|---------|
| Book (white page + blue left lobe) | Curriculum, knowledge, structured learning |
| Stylised K | Kwalitec identity; open pages / letterform |
| Gold ascending stroke + gold dot | Growth, reach, quality — learner rising |

Gold ascending stroke is the primary motion cue — always upward/forward. Masters are vector-first geometric constructions (BI-000).

### 2.3 Logo variants (BI-000 pack)

Documented in `app/static/assets/branding/ASSET_INVENTORY.md` and `EXPORT_INVENTORY.md`. Full path table: **§11**.

**Important repo tension (do not invent a merge):**

- BI-000 / `BRAND_GUIDELINES.md` describe SVG masters as permanent vector brand pack.  
- PX-001 branding READMEs state SVG under `svg/` is **obsolete for app display**; live UI uses the approved PNG only.  
- For **print / Welcome Pack**, prefer approved PNG + `print/` large assets; use SVG masters only where print conversion notes apply (`print/*-print.svg`).

### 2.4 Clear space & minimum size

From `BRAND_GUIDELINES.md`:

| Rule | Spec |
|------|------|
| Unit **1U** | Diameter of the gold dot |
| Clear space | ≥ **1U** all sides; prefer **1.5U** in marketing |
| Symbol ↔ wordmark gap | ≈ 1U–1.5U |
| Icon minimum | 16px tall (favicon); prefer 24px+ UI |
| Primary lockup minimum | 24px tall; prefer 32px+ |
| Print embroidery icon | ≥ 12 mm tall |
| Print full lockup | ≥ 25 mm tall |

### 2.5 Incorrect usage

Do **not** (`BRAND_GUIDELINES.md` + branding READMEs):

1. Stretch, skew, or rotate non-uniformly  
2. Recolour gold/blue off-palette  
3. Add drop shadows, glows, outlines, or gradients to masters  
4. Crop the gold tip inside a competing shape  
5. Separate gold dot from ascending stroke as a “new” logo  
6. Replace Inter/Manrope with decorative/script fonts in lockup  
7. Trace or embed approved PNG inside SVG/PDF masters  
8. Use the old IAHF-era neural-book mark  
9. Clear space below 1U  
10. Full lockup below 24px height  
11. Apply filters / tint / brightness to display PNG  

### 2.6 Brand marks & favicons

| Need | Path |
|------|------|
| Favicon SVG (pack) | `app/static/assets/branding/icons/favicon.svg` |
| Favicon PNG / ICO | `icons/favicon-{16,32,48}.png`, `favicon.ico` |
| Runtime served favicons | `app/static/branding/favicon.*` |
| Apple touch | `icons/apple-touch-icon.png` (180×180) / runtime copy |
| Android / PWA | `android-192.png`, `android-512.png`, `maskable-icon.png` |
| Windows tile | `mstile-150.png` |
| Manifest | `app/static/branding/manifest.webmanifest` |

### 2.7 Background pairing

| Background | Recommended mark (`BRAND_GUIDELINES.md`) |
|------------|------------------------------------------|
| Midnight / Deep Navy / Primary Dark | `logo-*-dark` (white book + white wordmark) |
| White / light grey | `logo-*-light` |
| Photography / busy | Solid midnight panel, or mono white/black |
| Single-colour print | Mono black or white only |

**Never** place light lockup on midnight.

---

## 3. Colours

### 3.1 Official brand palette (BI-000)

Canonical: `app/static/assets/branding/COLOUR_SPECIFICATION.md` · mirrored in `app/static/css/brand.css`.

| Token | HEX | RGB | CSS variable | Role |
|-------|-----|-----|--------------|------|
| Primary Blue | `#3B4FB8` | 59, 79, 184 | `--brand-primary-blue` / `--brand-blue` | Symbol K / book accents; primary action |
| Primary Blue Hover | `#2F3F96` | — | `--brand-blue-dark` / `--primary-hover` | Primary hover (`brand.css`, DX tokens) |
| Primary Dark | `#0D1B2A` | 13, 27, 42 | `--brand-primary-dark` | Light-surface lockups; chrome |
| Deep Navy | `#0A1628` | 10, 22, 40 | `--brand-deep-navy` / `--brand-navy` | Elevated dark chrome |
| Midnight | `#020D24` | 2, 13, 36 | `--brand-midnight` | Dark canvases, OG, app icons |
| Gold | `#E8B02B` | 232, 176, 43 | `--brand-gold` | Ascending stroke, accent — **not** UI chrome |
| Gold Hover | `#F0C040` | 240, 192, 64 | `--brand-gold-hover` | Interactive gold states (brand, not CTAs) |
| White | `#FFFFFF` | 255, 255, 255 | `--brand-white` | Book page / dark wordmark |
| Text Secondary (on dark) | `#8B93A7` | 139, 147, 167 | `--brand-text-secondary` | Supporting copy on dark |
| Divider (dark) | `#1E2A3D` | 30, 42, 61 | `--brand-divider` | Dark rules |

CMYK approx values: see `COLOUR_SPECIFICATION.md`.

### 3.2 Product semantic colours (DX-006A / tokens)

Canonical law: `knowledge/design/dx006a_design_system/DESIGN_TOKEN_SPEC.md` · CSS: `app/static/css/tokens.css`.

| Role | HEX / value | Notes |
|------|-------------|-------|
| Background (page) | `#F4F6F9` | `--background` / `--surface-alt` |
| Surface | `#FFFFFF` | Panels |
| Border | `#d5dae3` | Default |
| Border subtle | `#e6e9ef` | Soft |
| Text primary | `#1E2430` | Body / headings |
| Text secondary | `#4A5568` / `#3d4654` (tokens.css) | Supporting |
| Text muted | `#5C6570` / `#4a5568` | Metadata |
| Text inverse / on-primary | `#f8fafc` | On dark / primary fill |
| Secondary (quiet) | `#475569` | Secondary chrome |
| Success | `#0f766e` | bg `#e6f7f5` |
| Warning | `#A16207` | bg `rgba(161,98,7,0.12)` |
| Danger | `#c81e1e` | bg `#fef1f1` |
| Info | alias Primary Blue | Not decorative fourth hue |
| Focus ring | `0 0 0 3px rgba(59,79,184,0.28)` | |

**Hard rule:** Gold `#E8B02B` is **logo / achievement / certificates only** — never CTAs, links, focus, or nav (`DESIGN_TOKEN_SPEC.md`, `brand.css`).

Dark theme remaps roles in `tokens.css` `[data-theme="dark"]` — same roles, different bindings.

---

## 4. Typography

### 4.1 Official families

| Priority | Family | Source |
|----------|--------|--------|
| **Production UI** | **Inter** only | `DESIGN_TOKEN_SPEC.md` §3 |
| Brand wordmark recommendation | Inter SemiBold (600) | `BRAND_GUIDELINES.md` |
| Alternates (marketing / lockup experiments) | Manrope, Sora, Space Grotesk | Brand guidelines — use sparingly |
| Fallbacks | `system-ui, sans-serif` (SVG wordmark stack) | `ASSET_INVENTORY.md` |
| Mono | Codes / IDs only | Token spec |

**Special:** Wordmark **i**-tittle is brand gold (`#E8B02B`), matching gold dot (`BRAND_GUIDELINES.md`).

Suggested lockup tracking: approximately `−0.015em` to `−0.02em` at display sizes.

### 4.2 Hierarchy (product)

| Role | Size | Weight | Line height | Tracking |
|------|------|--------|-------------|----------|
| Display | 32px | 600 | 1.2 | −0.02em |
| Page heading (H1) | 24px | 600 | 1.25 | −0.015em |
| Section | 18px | 600 | 1.3 | −0.01em |
| Body | 16px | 400 | 1.5 | 0 |
| Supporting | 14px | 400 | 1.45 | 0 |
| Caption | 12px | 500 | 1.4 | +0.01em |

**One H1 per screen.** No fourth “card title” tier (`DESIGN_TOKEN_SPEC.md`).

### 4.3 Button typography

Not found as a separate Welcome Pack type scale. Product rule: Title Case, verb-led CTAs (`knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md`). Button radius/size follow component catalogue / `radius.md` tokens — see §5.

### 4.4 Spacing scale

8-point system (`DESIGN_TOKEN_SPEC.md`):

| Token | px |
|-------|----|
| space.1 | 4 |
| space.2 | 8 |
| space.3 | 16 |
| space.4 | 24 |
| space.5 | 32 |
| space.6 | 48 |
| space.7 | 64 |

**Retired for new product UI:** 12, 96, 128.

Brand safe-area spacing uses **1U = gold-dot diameter** (logo only) — distinct from UI spacing tokens.

---

## 5. Design Language

### 5.1 Premium / minimalism

Primary authorities:

- `knowledge/design/dx001_design_system/PRODUCT_DESIGN_MANIFESTO.md`  
- `knowledge/design/dx001_design_system/DESIGN_PRINCIPLES.md`  
- `PRODUCT_EXPERIENCE_GUIDELINES.md`  
- `knowledge/design/dx006a_design_system/PREMIUM_CERTIFICATION.md`

**Premium means:** immediate next-action clarity; calm hierarchy; respect for scarce attention; consistency that builds trust — **not** decoration.

Reference *principles* (not copies): Apple, Linear, Notion, Stripe, Raycast.

**Avoid:** colourful enterprise dashboards, card overload, KPI grids, tutorial theatre, gamification, purple-indigo decorative themes, rainbow KPI tiles.

### 5.2 Whitespace philosophy

Pages must feel calm (`PRODUCT_EXPERIENCE_GUIDELINES.md`): clear type hierarchy; consistent spacing; no crowding; no oversized paragraphs; no oversized cards for passive content.  
UX-001 note: empty large whitespace without intent can read as unfinished (`knowledge/product/px001/PREMIUM_UI_AUDIT.md`) — prefer intentional calm over vacant panels.

### 5.3 Motion philosophy

`DESIGN_TOKEN_SPEC.md` §7 · `INTERACTION_PRINCIPLES.md`:

| Token | Duration |
|-------|----------|
| press | 100ms |
| fast | 150ms |
| base | 200ms |
| panel / page | ≤250ms |

Ease-out. Respect `prefers-reduced-motion`. **No** bounce, elastic, confetti, cinematic fades in product OS. Motion clarifies state — never decoration.

### 5.4 Component / card / elevation / radius

| Topic | Rule | Path |
|-------|------|------|
| Cards | Only when they contain interaction / justified grouping | PX guidelines · DX-001 · Component Standards |
| Elevation | Prefer **border + spacing** over shadow stacks | `DESIGN_TOKEN_SPEC.md` |
| Radius | sm 0.5rem · md 0.75rem · lg 1rem · full pills only when functional | Same |
| One Primary action | Exactly one Primary button usage per page | Component Standards / Premium checklist |
| Empty states | Heading · one sentence · one action | Product Experience Guidelines |

### 5.5 Icons

**Lucide only** in product UI (`ICONOGRAPHY.md`, `brand.css` note: stroke 1.75–2, 24×24). Sizes 16 / 20 / 24 / 32. Icons support recognition; never replace labels. Gold not for general UI icons. Brand logo SVGs are separate from Lucide.

### 5.6 Illustration style

**Not found in repository** as a positive illustration system.

Anti-pattern is explicit: **no decorative illustrations** on Session / empty states / discovery (`dx005c` specs, Forbidden Patterns FP-08). Login historically used abstract CSS shapes — flagged as not product imagery (`POP-001` audit).

### 5.7 Photography guidance

**Not found in repository.** Brand guidelines only say: on photography/busy imagery, place logo on solid midnight panel or use mono marks.

---

## 6. Voice

### 6.1 Official writing style

| Layer | Document | Register |
|-------|----------|----------|
| Educational prose | `EA002_TUTOR_VOICE_GUIDE.md` | Calm, specific, professional Study Sensei |
| Tone attributes | `knowledge/product/TONE_OF_VOICE.md` | Professional, calm, warm, respectful, precise, quiet confidence |
| Ops Alpha voice | `knowledge/release/RP-001/VOICE_GUIDE.md` | Observation → meaning → action → benefit → uncertainty |
| Product UI nouns | `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` | Clear, professional, encouraging, concise |
| Experience chrome | `PRODUCT_EXPERIENCE_GUIDELINES.md` | Guide before explaining; short; specific |

**North-star sentence** (`EA002_TUTOR_VOICE_GUIDE.md`):  
> “Today we do this, because of that, so you can demonstrate this skill — then we continue here.”

**Grammar defaults:** British professional education register for IFoA context; second person for instructions; short action sentences; active assessable verbs.

### 6.2 Words / patterns to avoid

| Avoid | Sources |
|-------|---------|
| Crush it / You’ve got this / destiny / guaranteed pass | Tone · Tutor Voice · Claim Standard |
| Fail / weak student / doom | Tone vocabulary |
| Streak unlocked / gamification cheer as rationale | Tutor Voice |
| Twin, warrant, ranking algorithm, Mission Engine, Adaptive Decision Engine, Learning Orchestrator | Voice Guide · Product Language |
| Mastery score as identity; Exam Ready marketing | Claim freezes · Product Language |
| Runtime / milestone IDs / operator / epistemology on student surfaces | PX Experience Guidelines |
| Pop quiz / mock exam on Adaptive Assessment surfaces | Tone · ILE-001 |
| Exclamation campaigns, countdown drama, sticker praise | Tone |

### 6.3 Voice by context

| Context | Voice | Path |
|---------|-------|------|
| Marketing / Early Access ops email | Kwalitec product; claim-disciplined; invite-only honesty | `OP001_COMMUNICATION_TEMPLATES.md` |
| Educational Mission / Session / Reflection | Study Sensei tutor | EA-002 · Tone |
| Support | Calm ops; SLAs; no redesign promises | OP-001 / OP-002 · `SUPPORT_WORKFLOW.md` |
| System status | Neutral “we couldn’t…” — no fake Sensei theatre | RP-001 Voice Guide |

### 6.4 Examples of excellent writing already in-repo

**Early Access invitation (canonical claim-safe marketing):**  
`OP001_COMMUNICATION_TEMPLATES.md` §1 — “study companion… not a question bank, not a gamification app, and not a promise of pass rates.”

**Welcome / orientation:**  
Same file §4; also `knowledge/product/private_beta/STAGE1_INVITE_PACK.md` §2–§4.

**Sensei mission patterns:**  
`knowledge/product/MICROCOPY_LIBRARY.md` — e.g. “Today’s Mission focuses on {topic}.” / “Not enough evidence yet.”

**Tone example:**  
`TONE_OF_VOICE.md` — “Today’s focus is reinforcing Topic X. Recent practice looks fragile, and it blocks the next syllabus step.”

**Preferred student CTAs** (`PRODUCT_LANGUAGE_GUIDE.md`): Start Today's Session · Begin Session · Continue · Submit Answer · Continue to Summary · Return Home.

---

## 7. Student Journey

### 7.1 Terminology (binding for learner-facing copy)

From `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` (and Vision terminology notes):

| Domain / internal | Learner UI |
|-------------------|------------|
| Mission | **Session** / **Today's Session** |
| Progress path | **Journey** |
| Review work | **Revision** |
| Landing | **Home** |
| History of study | **History** |

**Note:** Older Sensei microcopy still says “Mission”; RP-001 documents the Mission/Session noun tension — for Welcome Pack student pages, prefer **Session** / **Today’s Session** per Product Language Guide unless quoting Sensei educational prose standards.

### 7.2 Core loop (product)

Authorities: `MISSION_MODEL.md`, `SESSION_ARCHITECTURE.md`, Educational Philosophy, CMP partnership.

```
Home (what now)
  → Start / Continue Today's Session
    → Overview (ready to begin?)
      → Activities (Reading → practice / checks …)
        → Reflection (after practice)
          → Summary / Return Home
Journey · Revision · History as orientation surfaces
```

**Mission answers three questions only** (`MISSION_MODEL.md`): What am I doing? Why now? What happens after completion?

**Session purpose:** Build mastery through practice — Practice First; reflection after practice (`SESSION_ARCHITECTURE.md`).

### 7.3 Reading & CMP partnership

Kwalitec is an **explicit guide for using the CMP**, not a replacement (`EC001_CMP_PARTNERSHIP_AUDIT.md`, `PB001A_CMP_PARTNERSHIP_VERIFICATION.md`).

A Guided Reading activity must answer Q1–Q6: what to open · purpose · attention · ignore · finished criteria · next in-app activity.

Principle: **Own the decision. Amplify the content.** (`GUIDANCE_OVER_CONTENT.md`)

### 7.4 Activities, Reflection, Revision, Progress, Finish, Continue

| Concept | Evidence |
|---------|----------|
| Activities | Session body practice steps; educational packages |
| Reflection | Soft, optional, non-scoring; after practice (`EA002`, ILE-005 references in Voice Guide) |
| Revision | Highest-value review from evidence — not streak theatre (`EDUCATIONAL_PHILOSOPHY.md`, Product Language) |
| Continue / Finish | CTAs: Continue · Submit · Continue to Summary · Return Home |
| Daily Mission / Today's Session | One primary commitment per day |
| Progress | Journey / History — not vanity dashboards |

### 7.5 Journey & Knowledge Map

| Surface | Path / note |
|---------|-------------|
| **Journey** | Approved nav term; progress through topics toward exam readiness | `PRODUCT_LANGUAGE_GUIDE.md` |
| **Knowledge Map** | Student surface `/student/knowledge_graph` introduced in UX-001 (`knowledge/engineering/ux001_premium_beta/UX001_PREMIUM_BETA_REPORT.md`) | Hierarchy over certified graph |
| **Curriculum Map** naming | Later note: Journey CTA uses **Curriculum Map** (not Knowledge Map) | `V1S001_IMPLEMENTATION_REPORT.md` |

For Welcome Pack: describe **Journey** as the student-facing progress story; mention Knowledge Map / Curriculum Map only if matching current LIVE labels — verify against LIVE UI before printing.

### 7.6 Early Access participant journey (ops)

Canonical map: `OP002_PARTICIPANT_JOURNEY.md`.

Invitation → accept + consent → first login → welcome/orientation → Home → Today’s Session (≥1 productive Session = Activated) → study weeks → optional interview → completion.

Orientation checklist (`BETA_ONBOARDING.md`, welcome email): Home · Session · Reflection · Journey · History · Revision · support.

### 7.7 Learning philosophy (short)

Sequential syllabus study; study ≠ understanding; consistency beats intensity; feedback + reflection close the loop; mistakes as fuel; confidence tracks evidence (`EDUCATIONAL_PHILOSOPHY.md`).

---

## 8. Version 1 Position & Claim Boundaries

### 8.1 Current release posture (as of 2026-08-04)

| Item | Fact | Path |
|------|------|------|
| Application version | `2.0.0-beta.1` | `REL001_RELEASE_NOTES.md` |
| Release programme | **REL-001 — Early Access Baseline Release** | Same · `REL001_DEPLOYMENT_REPORT.md` |
| Tag / commit | `rel-001` / `95a82b04ae50…` | Same |
| Host | https://kwalitec.onrender.com | Same |
| Claim class | Early Access operational baseline (invite-only) — **not** Version 1 production-ready | `REL001_BASELINE_FINGERPRINT.md` |
| Premium Experience | Conditional PASS (PX-007) | Release notes |
| Educational Content Freeze | Held | REL-001 |
| Educational Framework | **FROZEN** (EF-001) | `EF001_EDUCATIONAL_FRAMEWORK_FREEZE.md` |
| Educational effectiveness (KSI-003) | NO-GO / Pending Evidence | Release notes · OP-001 |
| Version 1 production-ready | **NO-GO** (P-002.1 — G1 FAIL, G7 HOLD) | Release notes · Claim Standard |

### 8.2 Private Beta vs Early Access

| Term | Meaning in-repo |
|------|-----------------|
| Private Beta / Stage 1 | Earlier protocol artefacts (`knowledge/product/private_beta/`, EP-008.2) |
| Early Access | Current ops language for invite-only cohort (OP-001 / OP-002 / EA-001 / REL-001) |

Both are **invite-only**, not public launch. Welcome Pack should use **Early Access** consistently with current templates, while privacy/consent text may reuse Stage 1 invite pack.

### 8.3 What MAY be claimed (Welcome Pack safe zone)

Aligned with `CLAIM_STANDARD.md` §5–§7 + OP-001 copy rules + REL-001:

- Invite-only Early Access / closed pilot  
- Study companion for professional exam preparation  
- Helps study with clarity and honesty  
- Curriculum-first / structured daily Session guidance (as product description, not proven effectiveness)  
- Educational packages for this wave are stable / frozen  
- Bugs may occur; honest feedback welcome  
- What is implemented / structurally verified (bounded, non-marketing)  

Board one-liner (`CLAIM_STANDARD.md`):  
> We may say what is implemented and structurally verified… We may **not** say we are educationally effective, externally validated, commercially proven, or Version 1 production-ready.

### 8.4 What MUST NOT be claimed

| Prohibited | Authority |
|------------|-----------|
| Version 1 production-ready / “V1 released” | P-002.1 · C-V1 · OP-001 templates |
| Exam pass-rate promises / pass guarantees | Vision · Claim freezes · OP templates |
| “Exam Ready” / false readiness marketing | DR-035 · G6.3 |
| Educational effectiveness / outcome marketing | C-EDU freeze · KSI-003 NO-GO |
| Recommendation-effectiveness marketing | DR-036 etc. |
| Perception as effectiveness | DR-033 |
| Estimated KSI as validated | DR-026 |
| Public self-registration / commercial launch | OP-001 · Invite packs |
| Guaranteed until-exam trust | OP-001 claim discipline |

### 8.5 Commercial wording restrictions

Public / sales / press = **C-COM** (`CLAIM_STANDARD.md` §3, §6). Standing freezes block educational commercial claims regardless of engineering pride. Prefer OP-001 template language verbatim for participant-facing Welcome Pack copy.

---

## 9. Founder Principles

| Theme | Principle | Path |
|-------|-----------|------|
| Quality / craft | Premium = clarity + restraint; Reference Linear/Stripe calm | DX-001 Manifesto · PX Guidelines |
| Student trust | Trust outweighs feature count; honesty over speed | Product Constitution PC-01 · Product Principles |
| Honesty / claims | Marketing ≤ verified evidence; STOP over silent claim expansion | PC-03, PC-12 · Claim Standard |
| Constitution | Vision 2030 Final Test: “Does this help students become better professionals?” | Vision · Product Constitution |
| Determinism | Planning / readiness / recommendations reproducible; no opaque LLM in core path | Vision · PC-09 · PROJECT_CONTEXT |
| Educational freeze | Produce guidance that helps students use CMP well — do not invent new Educational Framework | EF-001 |
| Design philosophy | One screen, one purpose; guide before explaining; remove before adding | Product Experience Guidelines · DX-001 |
| Product philosophy | Reduce decisions. Increase learning. Own the decision; amplify content | PROJECT_CONTEXT · Guidance Over Content · Study Sensei |
| Agency | Advice advisory; student agency preserved | PC-11 |
| Early Access ops | No product redesign from ops feedback mid-wave; packages frozen | OP-002 Participant Journey |

Founder approval gates invitations (`REL001`, `EA001`, `OP001`) — Welcome Pack must not imply open enrollment.

---

## 10. Images suitable for Welcome Pack inclusion

**Photography / lifestyle stock:** Not found in repository.  
**Decorative illustration library:** Not found (and discouraged).

### 10.1 Brand / social (preferred for cover & chrome)

| Relative path | Purpose | Resolution |
|---------------|---------|------------|
| `app/static/assets/branding/approved-kwalitec-logo.png` | Primary print/PDF logo (transparent) | 1418×372 |
| `app/static/assets/branding/approved-kwalitec-logo-on-navy.png` | Cover / dark hero lockup | 1774×887 |
| `app/static/assets/branding/original/Final-Approved-Kwalitec-Logo.png` | Master archive reference | 1774×887 |
| `app/static/assets/branding/social/og-logo.png` | Wide brand panel / OG style | 1200×630 |
| `app/static/assets/branding/social/twitter-x-logo.png` | Wide brand panel | 1200×600 |
| `app/static/assets/branding/social/linkedin-square.png` | Square brand mark | 400×400 |
| `app/static/assets/branding/social/github-profile.png` | Square brand mark | 500×500 |
| `app/static/branding/social-preview.png` | Runtime social preview | 1200×630 |
| `app/static/assets/branding/print/logo-primary-print.png` | Large print lockup | 2048×2048 |
| `app/static/assets/branding/print/logo-icon-print.png` | Large print icon | 2048×2048 |
| `app/static/assets/branding/print/logo-icon-mono-print.png` | Mono print / embroidery | 2048×2048 |
| `app/static/assets/branding/print/logo-wordmark-print.png` | Large wordmark | 1024×1024 |
| `app/static/assets/branding/png/logo-icon-1024.png` | High-res colour symbol | 1024×1024 |
| `app/static/assets/branding/icons/android-512.png` | App icon on midnight | 512×512 |
| `app/static/assets/branding/icons/apple-touch-icon.png` | Touch icon | 180×180 |

### 10.2 Product UI screenshots (orientation / journey visuals)

Use sparingly; many capture Alpha/legacy dual-runtime eras — **verify against LIVE REL-001** before publication.

| Relative path | Purpose |
|---------------|---------|
| `knowledge/reviews/V1_REVIEW_PACKAGE/screens/01-login.png` | Login |
| `…/04-dashboard-student.png` | Student home (era-dependent) |
| `…/05-journey.png` | Journey |
| `…/06-revision.png` | Revision |
| `…/19-onboarding.png` | Onboarding |
| `…/35-session-overview.png` | Session overview |
| `…/54-welcome-modal.png` | In-app welcome modal |
| `…/fix-home-start-session-overview.png` | Home → Session |
| `…/fix-home-before-start-session.png` | Pre-start Home |
| `…/26-navigation-student.png` | Student nav |

Full set (~60 screens): `knowledge/reviews/V1_REVIEW_PACKAGE/screens/`.  
PX evidence screenshots: `knowledge/evidence/releases/PX004/screenshots/` (README only listed in tree — confirm files before use).  
REL-001 HTML captures (not PNG): `knowledge/evidence/releases/REL001/html/`.

### 10.3 Not suitable without heavy disclaimer

- CMP / syllabus **content** PDFs (copyrighted educational materials — not brand publications)  
- Instance QA keyed SVGs under `instance/bi001d_qa/`  
- Error / raw 500 screenshots  

---

## 11. Logo asset table

| Asset | Relative path | Format | Size / notes |
|-------|---------------|--------|--------------|
| Approved display logo | `app/static/assets/branding/approved-kwalitec-logo.png` | PNG | 1418×372 · **UI SSoT** |
| Approved on navy | `app/static/assets/branding/approved-kwalitec-logo-on-navy.png` | PNG | 1774×887 |
| Final Approved master | `app/static/assets/branding/original/Final-Approved-Kwalitec-Logo.png` | PNG | 1774×887 |
| Approved archive | `app/static/assets/branding/original/Approved-Kwalitec-Logo.png` | PNG | 1774×887 |
| Approved optimised | `app/static/assets/branding/original/Approved-Kwalitec-Logo-optimised.png` | PNG | 1418×372 |
| Primary lockup (dark) | `app/static/assets/branding/svg/logo-primary.svg` | SVG | BI-000 master |
| Primary dark | `…/svg/logo-primary-dark.svg` | SVG | |
| Primary light | `…/svg/logo-primary-light.svg` | SVG | |
| Icon colour | `…/svg/logo-icon.svg` | SVG | |
| Icon dark | `…/svg/logo-icon-dark.svg` | SVG | |
| Icon light | `…/svg/logo-icon-light.svg` | SVG | |
| Mono black lockup | `…/svg/logo-monochrome-black.svg` | SVG | |
| Mono white lockup | `…/svg/logo-monochrome-white.svg` | SVG | |
| Wordmark | `…/svg/logo-wordmark.svg` | SVG | Live Inter + gold i-dot |
| Icon mono black | `…/svg/logo-icon-mono-black.svg` | SVG | |
| Icon mono white | `…/svg/logo-icon-mono-white.svg` | SVG | |
| PNG primary 64–1024 | `…/png/logo-primary-{64,128,256,512,1024}.png` | PNG | + alias `logo-primary.png` (512) |
| PNG icon 64–1024 | `…/png/logo-icon-{64…1024}.png` | PNG | + alias |
| PNG wordmark 64–1024 | `…/png/logo-wordmark-{64…1024}.png` | PNG | + alias |
| Print primary PNG | `…/print/logo-primary-print.png` | PNG | 2048×2048 |
| Print icon PNG | `…/print/logo-icon-print.png` | PNG | 2048×2048 |
| Print icon mono PNG | `…/print/logo-icon-mono-print.png` | PNG | 2048×2048 |
| Print wordmark PNG | `…/print/logo-wordmark-print.png` | PNG | 1024×1024 |
| Print SVGs | `…/print/logo-*-print.svg` | SVG | CMYK notes |
| Favicon set (pack) | `…/icons/favicon*` | SVG/PNG/ICO | 16–48 |
| Apple / Android / maskable / mstile | `…/icons/` | PNG | See EXPORT_INVENTORY |
| Social OG / X / LinkedIn / GitHub | `…/social/` | PNG | See §10 |
| Runtime branding copies | `app/static/branding/*` | PNG/SVG/webmanifest | Served at `/static/branding/` |

Inventories: `ASSET_INVENTORY.md`, `EXPORT_INVENTORY.md`, `COLOUR_SPECIFICATION.md`, `knowledge/design/BRAND_GUIDELINES.md`.

---

## 12. Publication references

### 12.1 Designed marketing / Welcome PDFs

**Not found in repository.** No prior official Early Access Welcome Pack PDF or branded brochure was located.

### 12.2 PDF files present (not Welcome Pack designs)

| Class | Examples | Reuse for Welcome Pack? |
|-------|----------|-------------------------|
| Official CMP / syllabus fixtures | `knowledge/product/fv001b_final/_evidence/official_*.pdf`, `knowledge/release/rc001…`, `instance/curriculum_documents/**` | **No** as brand artwork — third-party educational materials / evidence fixtures |
| Figma exports | — | **Not found in repository** |

### 12.3 Markdown / ops publications to reuse (copy & structure)

| Artefact | Path | Reuse |
|----------|------|-------|
| Communication templates | `OP001_COMMUNICATION_TEMPLATES.md` | Invitation, welcome, expectations, claim-safe wording |
| Stage 1 Invite Pack | `knowledge/product/private_beta/STAGE1_INVITE_PACK.md` | Welcome note, participant sheet, privacy outline |
| Participant journey | `OP002_PARTICIPANT_JOURNEY.md` | Timeline / what is / is not |
| Beta onboarding | `knowledge/product/private_beta/BETA_ONBOARDING.md` | Orientation checklist |
| REL-001 release notes | `REL001_RELEASE_NOTES.md` | Honest limitations box |
| Claim Standard | `knowledge/product/p003_5_evidence_hierarchy/CLAIM_STANDARD.md` | Legal-grade claim boundaries |
| Brand guidelines | `knowledge/design/BRAND_GUIDELINES.md` | Visual system |
| Tutor / Tone | `EA002_TUTOR_VOICE_GUIDE.md`, `TONE_OF_VOICE.md` | Voice if any Sensei excerpts |
| Product Language | `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` | Noun hygiene |
| Educational volumes / HR packs | Root `CS1*_PUBLICATION_*`, `EP001_WAVE1_PUBLICATION_PACK.md` | **Not** Welcome Pack — educational content governance |

### 12.4 What to reuse visually

1. Approved logo PNG + midnight/navy panels  
2. Brand blue / midnight / gold accent (gold sparingly)  
3. Inter typography  
4. Minimal callout boxes (border elevation, not card theatre)  
5. Optional **fresh** LIVE screenshots of Home / Session / Journey only after verification  

---

## 13. Recommended Welcome Pack Structure

Recommendation grounded **only** in: OP-001 welcome email, Stage 1 invite pack, BETA_ONBOARDING checklist, OP-002 journey map, Claim Standard freezes, Brand/DX calm premium rules. No invented marketing chapters.

### 13.1 Page count

**6–8 pages** (or equivalent short PDF / digital booklet).  
Rationale: welcome email + orientation checklist are short; Experience Guidelines forbid philosophy essays on primary surfaces; claim discipline forbids outcome marketing sections.

### 13.2 Sections (information hierarchy)

| # | Section | Content source | Notes |
|---|---------|----------------|-------|
| 1 | **Cover** | Logo on midnight/navy · “Kwalitec” · “Early Access” · Education Operating System descriptor | Brand hierarchy from `app/static/branding/README.md` |
| 2 | **Welcome** | Invite-pack / OP-001 welcome prose | Study companion; clarity & honesty; not Q-bank / gamification / pass promise |
| 3 | **What this is / is not** | OP-002 §4–§5 · Claim freezes | Invite-only; packages frozen; not public launch; not V1 production-ready |
| 4 | **How to start** | Numbered 1–4 from templates | Login → onboarding → Home → Today’s Session |
| 5 | **Your study loop** | Orientation checklist + Product Language nouns | Home · Session · Reflection · Journey · Revision · History · support |
| 6 | **Using your CMP** | EC-001 partnership principle (one short callout) | Kwalitec guides CMP use; does not replace it |
| 7 | **Support & expectations** | OP-001 SLAs · bugs may occur | Security immediate; cannot-study same business day |
| 8 | **Appendix (optional)** | Privacy pointer · consent summary · glossary of product nouns | Link/reference Stage 1 Privacy Notice — do not invent legal text |

### 13.3 Graphics

- Cover: approved logo on midnight (`approved-kwalitec-logo-on-navy.png` or equivalent composition respecting clear space)  
- Optional 2–3 LIVE screenshots: Home (next action), Session overview, Journey — verified against REL-001  
- Simple loop diagram (text-first) matching OP-002 / onboarding flow — no decorative illustration system available  
- **Do not** invent lifestyle photography  

### 13.4 Callout boxes

Use sparingly (border / soft surface tokens):

1. **Claim honesty** — “We do not guarantee exam passes.”  
2. **CMP partnership** — “Open your CMP when Reading asks — we guide; we do not replace.”  
3. **Support** — reply channel + SLA lines  

### 13.5 Timeline

Participant personal clock from `OP002_PARTICIPANT_JOURNEY.md` / `OP002_STUDY_TIMELINE.md` (ops): first Session activation (≤7 days), study weeks, optional ~week-4 interview — present as orientation, not marketing roadmap of product features.

### 13.6 Quotes

Founder/marketing testimonial library: **Not found in repository.**  
Do **not** fabricate quotes. Optional interview quotes require C3 quote consent (`STAGE1_INVITE_PACK.md`) — none are filed for reuse here.

Permitted attributed lines only if quoting Vision / Sensei north-star sentences as **product philosophy**, clearly labelled — not student testimonials.

### 13.7 Appendices

- Product noun glossary (Session, Journey, Revision, Home, History)  
- Pointer to Privacy Notice / consent (do not paste stale legal without operator update)  
- Honest limitations from `REL001_RELEASE_NOTES.md` (optional founder-facing insert; consider omitting from student PDF if redundant with §3)

---

## 14. Designer checklist (pre-flight)

- [ ] Logo from approved PNG masters; clear space ≥1U  
- [ ] Palette from COLOUR_SPECIFICATION + tokens; gold not used as CTA colour  
- [ ] Inter as primary type  
- [ ] Copy claim-checked against §8  
- [ ] Student nouns from Product Language Guide  
- [ ] No decorative illustration / gamification chrome  
- [ ] No Version 1 / pass-rate / Exam Ready language  
- [ ] Screenshots verified against LIVE if used  
- [ ] CMP partnership stated without implying Kwalitec replaces CMP  

---

## 15. Gaps explicitly recorded

| Topic | Status |
|-------|--------|
| Named “core values” marketing list | Not found — use constitution principles |
| Photography / art direction guide | Not found |
| Illustration system | Not found (decorative illustrations forbidden) |
| Prior Welcome Pack PDF | Not found |
| Figma source files | Not found |
| Student testimonials for print | Not found |
| Separate Welcome Pack button type scale | Not found — use product type roles |
| Resolved Mission vs Session noun for all surfaces | Documented tension — prefer Session for learner UI |
| Knowledge Map vs Curriculum Map vs Journey label | Multiple historical names — verify LIVE |

---

## 16. Authority index (quick paths)

| Need | Path |
|------|------|
| Vision / north star | `knowledge/product/vision/PRODUCT_VISION_2030.md` |
| Brand guidelines | `knowledge/design/BRAND_GUIDELINES.md` |
| Colours | `app/static/assets/branding/COLOUR_SPECIFICATION.md` |
| Tokens | `knowledge/design/dx006a_design_system/DESIGN_TOKEN_SPEC.md` · `app/static/css/tokens.css` · `brand.css` |
| Experience feel | `PRODUCT_EXPERIENCE_GUIDELINES.md` · DX-001 manifesto |
| Voice | `EA002_TUTOR_VOICE_GUIDE.md` · `TONE_OF_VOICE.md` · `OP001_COMMUNICATION_TEMPLATES.md` |
| Claims | `knowledge/product/p003_5_evidence_hierarchy/CLAIM_STANDARD.md` |
| Early Access ops | `OP001_EARLY_ACCESS_PLAN.md` · `OP002_PARTICIPANT_JOURNEY.md` · `REL001_RELEASE_NOTES.md` |
| EF freeze | `EF001_EDUCATIONAL_FRAMEWORK_FREEZE.md` |
| CMP partnership | `EC001_CMP_PARTNERSHIP_AUDIT.md` |
| Positioning | `COMPETITIVE_POSITIONING.md` · `DIFFERENTIATORS.md` · `STUDY_SENSEI_PHILOSOPHY.md` |

---

**End of DOC-001.**  
Do not treat this file as the Welcome Pack itself. Design work begins only after Founder authorises use of this pack as the brief.
