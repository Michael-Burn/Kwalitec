# Alpha Readiness — Founder UX (ARP-002)

**Authority:** Informational (Founder presentation polish)  
**Scope:** Founder-facing interfaces only — no educational logic, domain, routing, or persistence changes.

This note captures the ARP-002 Founder Experience Polish pass: consistency review findings, improvements shipped, and remaining opportunities for Internal Alpha.

---

## Surfaces reviewed

| Surface | Path / entry | Role in Founder journey |
|---------|--------------|-------------------------|
| Founder Dashboard (Overview) | `/founder/` | Operational home |
| Curriculum Studio | `/founder/studio/` | Curriculum readiness hub |
| Workspace | `/founder/studio/workspaces/<id>` | Validate → Preview → Approve → Publish |
| Validation / Preview / Approve / Publish | Workspace actions | Stage-gated Founder actions |
| Version History | Workspace “Version history” | Post-approval labelling |
| Founder Intelligence | `/founder/intelligence` | Advisory journey signals |
| Evidence Gates | `/founder/evidence-gates` | Cutover evidence checklist |

Secondary Command Centre destinations (Attention, Findings, Internal Alpha, etc.) were left structurally unchanged; Studio, Intelligence, and Evidence Gates received the polish focus for Alpha readiness.

---

## Improvements made

### Consistency

- Shared Founder CSS (`founder_dashboard.css`) now loads on Studio, Intelligence, and Evidence Gates.
- Common patterns: breadcrumbs, “Next step” callouts, command cards, primary/secondary buttons, empty-state blocks.
- Workflow stage labels aligned with the product journey (`Content Sources`, `Publish`).
- Primary action on the workspace page follows the current stage so the next step is visually obvious.

### Empty states

- Studio dashboard: guided empty states for **no workspaces** and **no recent activity** (no blank lists).
- Workspace: guided empty state for **no version history**.
- Intelligence: guided empty state for **no signals**.
- Evidence Gates: empty checklist / empty notes fallbacks (never a blank table).

### Messaging

Centralised Founder flash copy in presentation view-models, for example:

- “Validation completed successfully.”
- “Curriculum published successfully.”
- “Publish curriculum” (button) instead of terse or command-like phrasing.

Warnings guide recovery (“check … and try again”) rather than dead-end failures.

### Forms

- Placeholders on subject code, approval note, publication note, and version label.
- Required-field indicators (`*`) with `aria-required` on critical inputs.
- Validation error regions with `role="alert"`.
- Consistent `founder-btn` sizing and focus styles.

### Accessibility

- Breadcrumb `nav` with `aria-current="page"`.
- Focus-visible outlines on Founder inputs, buttons, and workspace links.
- Minimum control height (~2.5rem) for touch / pointer targets.
- Screen-reader hints for active workflow stage and evidence gate readiness.

### Responsive layout

- Action and version forms wrap cleanly below ~768px.
- Workspace list items stack meta under the subject code on small widths.
- Workflow stepper remains a wrapping flex row (no horizontal overflow trap).

### Workflow clarity

Suggested Founder journey is now explicit in UI copy:

```text
Dashboard → Studio → Workspace → Validate → Preview → Approve → Publish → Version History
```

Each workspace stage exposes a **Next step** sentence and highlights one primary CTA.

---

## UX findings

1. **Studio was visually orphaned** from the Command Centre shell (missing Founder CSS) — fixed.
2. **Action buttons were equally weighted**, so the “obvious next action” was unclear — fixed via stage-based primary CTA.
3. **Empty activity was omitted entirely** on the Studio dashboard, which felt unfinished — now always shows a card with guidance.
4. **Intelligence and Evidence Gates** used milestone codes (V2-021 / ADR-007) as eyebrows; Alpha copy now emphasises product language while keeping diagnostic dual-run context.
5. **Harsh / terse flashes** (“Validation complete.”) reduced confidence; success copy now confirms outcomes explicitly.

---

## Future enhancement ideas

- Dedicated per-stage panels (Validate / Preview / Approve / Publish) instead of a single action grid, once Alpha feedback confirms Founders want deeper staging.
- Inline publication checklist checklist UI (item-by-item) rather than a summary sentence.
- Diff / preview iframe surface when Curriculum Preview payloads are ready for Founder review.
- Evidence Gates: Founder attestation toggles (product evidence signed-off) without changing gate computation.
- Keyboard shortcut map for Studio power users (advance / validate / publish).
- Shared Jinja macros package for breadcrumbs / next-step / empty-state to reduce template duplication.

---

## Remaining polish opportunities

| Area | Opportunity | Priority |
|------|-------------|----------|
| Overview empty alerts | Align Overview alert empty copy with Studio empty-state pattern | Medium |
| Feedback / Vision Journal | Apply the same breadcrumb + next-step chrome | Low (out of ARP-002 focus) |
| Live form re-render | Re-show invalid Studio create forms in-place instead of flash + redirect | Medium |
| Colour contrast audit | Formal WCAG AA pass on metric labels under brand themes | Medium |
| Motion | Subtle workflow-step transition when stage advances | Low |
| Internationalisation | Extract Founder strings to a message catalogue | Low |

---

## Tests

Presentation coverage lives under `tests/presentation/curriculum_studio/`:

- View models, forms, templates, empty states, navigation, messaging, accessibility, rendering, volume grid.

Target for ARP-002: **50–100** presentation tests. Collected: **105** passing
cases under `tests/presentation/curriculum_studio/` (parametrized grids included).

---

## Constraints respected

- No educational algorithm changes
- No curriculum / domain behaviour changes
- No persistence or infrastructure changes
- No routing changes (URLs and endpoints unchanged)
- Presentation refinement only

---

## Related documents

- [`CURRICULUM_STUDIO.md`](CURRICULUM_STUDIO.md) — Studio product/architecture
- [`V2_020_RETIREMENT_RUNBOOK.md`](V2_020_RETIREMENT_RUNBOOK.md) — cutover evidence runbook
- [`DESIGN_SYSTEM.md`](DESIGN_SYSTEM.md) — learner UI design system (distinct from Founder shell)
