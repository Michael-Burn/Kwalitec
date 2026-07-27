# Troubleshooting Guide — Founder Operations

**Programme:** PR-001A  

Use this guide when a Studio action fails. Each row: symptom → cause → recovery.

---

## Access

| Symptom | Likely cause | Recovery |
|---|---|---|
| Cannot open Curriculum Studio | Account not founder-authorised | Sign in with authorised email; ask platform admin to add `FOUNDER_EMAILS` |
| Login fails | Wrong password / inactive user | Reset via admin process; do not share credentials |

## Subject & workspace

| Symptom | Likely cause | Recovery |
|---|---|---|
| “Couldn't create this subject… already exists” | Duplicate subject code | Open existing workspace or choose a new code |
| “Couldn't open this workspace” | Unknown subject / form error | Create subject first; check code spelling |
| “Workspace could not be found” | Bad URL / deleted workspace | Return to Studio dashboard; open a listed workspace |

## Upload & parsing

| Symptom | Likely cause | Recovery |
|---|---|---|
| “Couldn't upload sources” | Empty refs or missing version | Assign version; provide CMP and/or syllabus reference; retry |
| Ingestion / parsing findings after upload | Bad reference or structure | Correct references; re-upload; validate |
| Port / service unavailable | Temporary Management/Ingestion outage | Wait, refresh workspace, retry; contact support if persistent |

## Validation

| Symptom | Likely cause | Recovery |
|---|---|---|
| Validation needs attention + missing CMP/syllabus | Sources not uploaded | Upload both references; validate again |
| “No version is assigned” | Version gate | Assign version label; retry validate |
| Blocking findings remain | Structural/source issues | Follow each finding’s **What to do**; re-validate |

## Preview / approve / publish

| Symptom | Likely cause | Recovery |
|---|---|---|
| Couldn't build preview | Not validated | Validate first |
| Couldn't approve | Missing version/preview | Assign version; build preview; retry |
| Couldn't publish | Checklist incomplete | Complete approval + version; fix checklist; retry |

## Version conflicts

| Symptom | Likely cause | Recovery |
|---|---|---|
| Version label already exists | Duplicate label/id | Choose a new label (e.g. `2027.2`); retry |

## Still stuck?

1. Capture the exact flash message and finding codes.
2. Note subject code, workspace id, and version label.
3. Contact platform support with those details — do **not** ask engineering to bypass validation gates.
