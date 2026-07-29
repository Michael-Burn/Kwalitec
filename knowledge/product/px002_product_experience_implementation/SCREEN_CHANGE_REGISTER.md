# PX-002 — Screen Change Register

**Programme:** PX-002  
**Date:** 2026-07-28  
**Quality gates per screen:** Who for? Next action? Implementation detail hidden? Glossary match?

---

| Screen | Audience | Change | Next action | Hidden? | Glossary |
|--------|----------|--------|-------------|---------|----------|
| Alpha Welcome (`/alpha/onboarding`) | Student | Plain study-prep orientation; removed Education OS framing | Continue to Home / Choose Exam path | Yes | Subject, Study Plan, Today's Focus |
| Choose Exam (`/study-plan/wizard/1`) | Student | Subject Catalogue cards (Name, Availability, Version, Updated) | Select Ready subject → Exam Date | Yes — no Studio / upload / KG | Ready, Coming Soon, Subject |
| Exam Date (`/study-plan/wizard/2`) | Student | Relabelled; former sitting step | Enter date → Availability | Yes | Exam Date |
| Study Availability (`/study-plan/wizard/3`) | Student | Relabelled; former availability step | Enter time → Begin Learning | Yes | Study Availability |
| Begin Learning (`/study-plan/review`) | Student | Confirm Study Plan; deferred defaults applied | Begin Learning → LP-001 / bridge | Yes | Study Plan, Verified Curriculum |
| Subject support gate partial | Student | Ready alternatives; Coming Soon preparation copy | Choose Ready subject | Yes | Ready, Coming Soon |
| Student Home | Student | Hero eyebrow / fallback title → Today's Focus; completion labels strengthened | Start / continue session | Yes | Today's Focus |
| Session completion / outcome copy | Student | Completed / why / tomorrow framing | Reflect / return tomorrow | Yes | Session |
| Console sidebar | Founder | Curriculum Authority tagline + primary nav | Subjects → … → Quality | Ops demoted | Founder Studio |
| Subjects hub | Founder | New hub over Studio spine | Create Subject / Open Workspace | Advanced CIP not primary | Subjects |
| Curriculum Studio dashboard | Founder | Remains workspace home | Advance workflow | Yes | Curriculum Studio |
| Review / Publishing / Versions / Quality hubs | Founder | New framing pages | Open Studio workspace | Yes | Review Queue, Publishing, Versions, Quality |
| Publish CTA | Founder | Publish Verified Curriculum | Publish | Yes | Verified Curriculum |

---

## Removed / never introduced on student chrome

- Upload CMP / Syllabus  
- Publish Curriculum  
- Knowledge Graph  
- Extraction / Review Queue  
- Curriculum Studio / Console links  
- “Published Curriculum” category branding  

---

**End of Screen Change Register**
