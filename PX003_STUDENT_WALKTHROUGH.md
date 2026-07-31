# PX-003 — Student Walkthrough

**Programme:** Product Experience Programme PX-003 — Workflow Transparency & Confidence  
**Date:** 2026-07-31  
**Method:** Manual code-backed walkthrough of implemented Student study flow only.

---

## Walkthrough — Entry → Home → Overview → Session → Completion → History

| Step | Purpose | Confidence before | Confidence after PX-003 | Next action |
|------|---------|-------------------|-------------------------|-------------|
| Entry / Login | Land on study OS | Greeting only | Unchanged entry; Home carries next cue | Open Home |
| Home | What should I do now? | Strong CTA; weak “what after?” | “After this · …” on mission hero (why stays on Overview per UX-001) | Start / Continue Session |
| Session Overview | Am I ready to begin? | Briefing collapsed; no step map; Timer showed estimate | Briefing open; Step strip; Estimated time label | Begin Session |
| Study Session | Complete practice | Silent answer submit; no journey chrome; broken timer hook | Answer flash; stage indicator; `data-ux=study-session` timer | Continue → Reflection |
| Reflection → Summary | Close honestly | Silent continue | Reflection saved flash | Finish review |
| Completion | What just happened? | Information wall | Headline + studied + up next + History link first; details disclosed | Return Home / History |
| History | Practice record | Thin support line | Support: sessions are saved here | Return Home |

### Confidence drops closed

1. Invisible session journey → `ds_stage_indicator` from existing `shell.steps`.
2. Overview did not preview at a glance → briefing `open`.
3. Timer JS selector mismatch → fixed.
4. Silent mid-session transitions → flashes.
5. Completion cognitive overload → progressive disclosure.
6. History not framed as the archive of the session just finished.

### UX-001 boundary respected

- Home remains decision-first.
- Educational “why today” stays on Session Overview, not restored as Home MES stack.

### Remaining Student experience debt

1. Pause can still appear twice in chrome (exit strip + show_pause).
2. History cards still use generic “Session complete” outcome labels.
3. No highlight of the just-finished session when arriving from Complete.
