# DEP-002 — Recommended Remediation

**Programme:** DEP-002 (investigation) → proposed **DEP-003** (implementation)  
**Constraint from DEP-002:** no fixes in this programme.

---

## Do not do first

1. Do **not** unset `KWALITEC_V2_SOLE_RUNTIME` — that restores full dual-home, worsening the symptom.  
2. Do **not** mass-delete legacy blueprints without a chrome migration for Study Plan / Help / Onboarding / Settings.  
3. Do **not** treat this as a Render redeploy problem — commit and flag are already correct.

---

## DEP-003 — Presentation unification under sole runtime

**Goal:** One student-visible application chrome when `SOLE_RUNTIME=1`, without deleting educational engines.

### Workstreams (suggested order)

1. **Chrome contract**  
   Define the single shell for sole runtime (extend `student/base.html` or a shared EOS layout). Document which endpoints must never render `layouts/base.html` under sole.

2. **Login entry**  
   Keep study-plan requirement, but render wizard **inside EOS chrome** (or redirect to `student.home` with an in-EOS plan CTA). Eliminate first-paint legacy shell for new users.

3. **EOS nav destinations**  
   Re-home or wrap `study_plan.*` and `alpha.help_centre` (and onboarding) so nav clicks do not cross into V1 sidebar.

4. **Settings**  
   Finish settings consolidation: subpages either redirect into `student.profile` sections or inherit EOS shell (index already redirects).

5. **Hard-coded V1 CTAs**  
   Sweep remaining `url_for('dashboard.index')` / mission CTAs in templates still reachable under sole.

6. **Only then — physical retirement**  
   After soak: delete or quarantine dashboard/mission/analytics templates; optionally stop registering redirect-only blueprints behind a second flag. Keep Runtime A / Mission Engine / curriculum untouched.

### Acceptance criteria (for DEP-003)

- With production flag matrix, a student session never renders `app-sidebar` / `layouts/base.html` for student-facing flows.  
- Login → Home or EOS-wrapped plan setup only.  
- `/dashboard/`, `/missions/`, `/analytics/` remain redirect-only or gone.  
- Founder dogfood: no perceptible “second app” when opening Study Plan or Help.  
- Rollback path documented (restore V1 shell via flag or release).

### Out of scope for DEP-003 (unless explicitly expanded)

- Twin / Adaptive authority cutovers  
- Deleting `src/web` EOS composition root  
- Database schema changes  
- Public registration

---

## Evidence package handoff

DEP-003 implementers should start from:

- `ROOT_CAUSE_ANALYSIS.md` (primary cause H)  
- `NAVIGATION_AUDIT.md` + `TEMPLATE_AUDIT.md` (shell mix)  
- `LEGACY_RUNTIME_INVENTORY.md` (what is safe to remove later)  
- `DEPLOYMENT_AUDIT.md` (prove env/commit before changing behaviour)
