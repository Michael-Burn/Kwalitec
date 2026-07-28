# Narrative Generation

**Programme:** ILE-003 — Educational Timeline  

---

## Arc structure

Each narrative moment follows:

```
Observation
    ↓
Pattern
    ↓
Educational meaning
    ↓
Reflection question
```

| Layer | Intent |
|---|---|
| Observation | What the journal recorded (evidence-facing) |
| Pattern | What appears across one or more entries (hedged) |
| Educational meaning | Why that pattern matters for learning (not judgement) |
| Reflection question | An open prompt for the learner to think |

---

## Certainty bands

| Band | When | Speech |
|---|---|---|
| Insufficient | Fewer than 2 journal entries | Tentative; avoid absolute claims |
| Suggestive | 2–3 entries | “May”, “appears”, “possible” |
| Supported | 4+ entries | Clearer pattern language still without proof theatre |

Overall certainty is shown as a calm status line on the Timeline page.

---

## Pattern sources (journal-only)

| Section | Emerges from |
|---|---|
| Learning Journey | Chronological sample of journal entries |
| Turning Points | First reliable/high accepted guidance; recovery acceptance; milestones; repeated uncertainty |
| Recoveries | `recovery_recommendation` (and recovery-language acceptances) |
| Consistency | Streaks of accepted entries within a short day gap |
| Uncertainty | Thin confidence bands or explicit uncertainty text |
| Mission Milestones | Mission recommendations that reached accepted / reflected / outcome |
| Reflection Highlights | Reflected entries / reflection notes |
| Decision Milestones | Accept / defer / dismiss with later lifecycle progress |
| Learning Momentum | Qualitative comparison of recent vs earlier accepted guidance |

No independent telemetry stream feeds these sections.

---

## Implementation

- Domain: `app/domain/educational_timeline/narrative.py` (`build_educational_narrative`)  
- Service: `app/services/educational_timeline_service.py` (loads journal, validates humility)  
- Application: `app/application/educational_timeline/` (student snapshots)

Humility checks (`assert_narrative_humble`) reject overclaim phrases and forbidden engineering terms before presentation.
