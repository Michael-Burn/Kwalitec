# Forbidden Patterns Register

**Programme:** DX-002  
**Release Candidate:** `RC-2026.07.29-01`  
**Rule:** Each occurrence recorded. Patterns from DX-002 brief + DX-001.

---

## Register

| ID | Pattern | Location(s) | Evidence | Severity |
|---|---|---|---|---|
| FP-01 | Oversized headings | Console/Studio `section-title` / legacy 40px culture | Studio & Console headers dominate vs DX-001 24px Page Heading | High |
| FP-02 | Card overload | Console Overview; Workspace; History; Profile; hubs | Metric tiles + command-cards as default container | Critical |
| FP-03 | Multiple primary buttons | Console Quick Actions (primary + peers); Workspace Actions grid; Onboarding Continue/Skip/Help | Multiple `btn-primary` / primary-weight CTAs | Critical |
| FP-04 | Duplicate navigation | Studio hubs ↔ sidebar; Attention ↔ Overview; Search topbar+secondary; Curriculum Studio repeated CTAs | `nav.py` + hub template + overview.html | Critical |
| FP-05 | Repeated status indicators | Internal Alpha badge (sidebar/topnav/login/onboarding); Documents Uploaded badge + CTA; trust/coherence on Home | Multiple chrome locations | High |
| FP-06 | Tutorial paragraphs | History epistemology; Hub workflow list; Workspace upload essay; Help journey map | Templates cited in Content Audit | Critical |
| FP-07 | Decorative KPIs | Platform Summary grid; History readiness trend; CIP Documents/Topics; embedding vector counts | KPI Audit | Critical |
| FP-08 | Decorative illustrations | Login `landing-illustration` shapes | `auth/login.html` | Medium |
| FP-09 | Excessive colour usage | Attention card severity mosaics; multi-badge status rows | Console + Studio | Medium |
| FP-10 | Repeated explanations | Home why/benefit/coherence; History→Journal CTAs twice; Revision “not a second Mission” echoed in Help | Student templates | High |
| FP-11 | Welcome messages | Onboarding H1; Welcome modal; post-calibration | `alpha/onboarding.html`, `welcome_modal.html` | High |
| FP-12 | Implementation terminology | Workspace Entity id `ent-…`; retrieval profiles (Mission Engine, Tutor); duration_ms; build number; timezone_policy in hero; “CIP”, “embeddings” | `workspace.html`, overview eyebrow | Critical |
| FP-13 | Analytics above action | Console Platform Summary before/alongside work | `overview.html` | High |
| FP-14 | Dashboard theatre | Console Home as reporting wall; Studio “dashboard” label | overview + dashboard.html | High |
| FP-15 | Equal-weight peer archives | History / Decision Journal / Educational Timeline | Student nav + Help ontology | High |
| FP-16 | Meta-tabs | CIP Documents tab pointing to Content Sources above | workspace.html | Medium |
| FP-17 | Orphan UX surface | Unused wizard_step_2/4/6/7 templates | Disk inventory | Low (cleanup) |
| FP-18 | Label collisions | Participants vs Students; Settings vs Profile; Analytics vs History | Nav vs H1 | Medium |

---

## Counts by severity

| Severity | Count |
|---|---|
| Critical | 7 |
| High | 8 |
| Medium | 4 |
| Low | 1 |

---

## Pattern frequency (approx. product-wide)

| Pattern | Est. distinct surfaces affected |
|---|---|
| Card overload | ≥12 |
| Tutorial paragraphs | ≥8 |
| Decorative KPIs | ≥6 |
| Multiple primaries | ≥5 |
| Implementation terminology | ≥4 |
| Welcome messages | 3 |

---

## Clearance rule for redesign programmes

A screen may not claim DX-001 Premium Checklist pass while any **Critical** FP remains on that screen.
