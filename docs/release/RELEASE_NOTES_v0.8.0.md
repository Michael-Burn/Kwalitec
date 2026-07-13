# Kwalitec v0.8.0

## Discovery-Driven Multi-Paper Curriculum Binding

Version:

v0.8.0

Status:

Production

---

## Overview

Version 0.8.0 removes hardcoded per-paper curriculum version maps from the Study Plan wizard. Every on-disk V2 syllabus under `app/curriculum/data/` is discovered automatically and can bind into study plans, topic progress, missions, and recommendations.

This fixes CB2 (and any future paper) being created without curriculum linkage while CS1/CM1 remained wired.

---

## Highlights

### Curriculum version discovery

Study Plan wizard versions are resolved via `CurriculumEngineService.list_supported_versions` — not a hardcoded `(IFoA, paper) → version` map.

### Syllabus-anchored mission and recommendation copy

Missions and coverage recommendations lead with official topic codes and titles (e.g. `4.2 Generalised Linear Models`) when a curriculum topic is selected.

### Curriculum parity tests

Discovery-driven parity coverage for every on-disk syllabus (import → study plan → topic selection → recommendation → mission → roadmap), so new papers inherit checks without per-paper test edits.

### Theme contrast polish

Bootstrap `data-bs-theme` follows appearance mode; card and topic text use primary/secondary theme colours for readability.

---

## Looking Ahead

Continue Internal / External Alpha feedback loops on multi-paper study journeys and mission copy quality.

---

Thank you to everyone contributing to Kwalitec.
