# Kwalitec Release Protocol

## OBJECTIVE

Release the latest completed work to GitHub and Render.

This task is strictly a release operation.

Do NOT implement features.

Do NOT refactor code.

Do NOT redesign architecture.

Do NOT fix unrelated issues discovered during the release unless they directly prevent deployment.

=========================================================
## RELEASE BOUNDARIES
=========================================================

### Allowed

✓ Verify repository state

✓ Run verification tests

✓ Stage files

✓ Create release commit (if required)

✓ Push to GitHub

✓ Create and push Git tag

✓ Prepare release notes

✓ Deploy to Render

✓ Verify deployment

✓ Run production smoke tests

✓ Produce release report

### Not Allowed

✗ New features

✗ Architecture changes

✗ Educational Intelligence changes

✗ Digital Twin redesign

✗ Recommendation changes

✗ Evidence Loop work

✗ Refactoring unrelated modules

✗ Cosmetic improvements outside release fixes

✗ Fixing historical technical debt

If release blockers are found:

STOP

Report them.

Do not silently fix unrelated issues.

=========================================================
## STEP 1 — VERIFY REPOSITORY
=========================================================

Run:

```
git status
```

Verify:

• Branch is main

• Working tree is clean

If uncommitted files exist:

Stage them.

Create ONE release commit.

Use an appropriate commit message describing only the completed work.

Verify working tree is clean.

=========================================================
## STEP 2 — VERIFY QUALITY
=========================================================

Run:

```
python3 -m pytest
```

Expected:

All tests pass.

Run Ruff only on modules modified during this release.

Do NOT treat historical repository-wide Ruff debt as a release blocker unless explicitly instructed.

If tests fail:

STOP.

Provide:

• failing tests

• root cause

• recommended fix

Do not continue.

=========================================================
## STEP 3 — PUSH TO GITHUB
=========================================================

Push:

```
git push origin main
```

Verify push succeeded.

Record deployed commit hash.

=========================================================
## STEP 4 — CREATE RELEASE TAG
=========================================================

Inspect existing tags.

Create the next available semantic version.

Never overwrite an existing tag.

Push the tag.

Record the version.

=========================================================
## STEP 5 — RELEASE NOTES
=========================================================

Generate concise release notes.

Include only completed work.

Do not invent features.

=========================================================
## STEP 6 — DEPLOY
=========================================================

Deploy the latest commit to Render.

Wait for deployment to finish.

If deployment fails:

STOP.

Report failure.

=========================================================
## STEP 7 — VERIFY PRODUCTION
=========================================================

Confirm:

✓ Application starts

✓ Health endpoint returns OK

✓ Database connected

✓ Migrations successful

✓ No startup exceptions

=========================================================
## STEP 8 — SMOKE TEST
=========================================================

Verify the user journey affected by this release.

Examples

Authentication

Dashboard

Study Plan

Calibration

Recommendation

Mission

Progress

Theme

Settings

Curriculum

Only test features relevant to this release.

=========================================================
## STEP 9 — RELEASE REPORT
=========================================================

Provide:

1. Commit hash

2. Release tag

3. Test summary

4. Ruff summary

5. Deployment summary

6. Smoke test summary

7. Known issues

8. Overall verdict

=========================================================
## STOP CONDITIONS
=========================================================

Immediately stop if:

• Tests fail

• Deployment fails

• Migration fails

• Production smoke test fails

• Health endpoint fails

Do not implement new functionality during a release.

Only report the blocker.

=========================================================
## SUCCESS CRITERIA
=========================================================

A successful release means:

• Code is committed

• Code is pushed

• Tag is created

• Render deployment succeeds

• Production passes smoke tests

• A release report is produced

Nothing else.
