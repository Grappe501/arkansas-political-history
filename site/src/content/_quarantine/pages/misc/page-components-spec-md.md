---
title: "PAGE_COMPONENTS_SPEC.md"
description: "Stand Up Arkansas \u00e2\u20ac\u201d The People\u00e2\u20ac\u2122s Political History"
tags:
  - migration:uncategorized
---
\# Page Components Spec

Stand Up Arkansas â€" The Peopleâ€™s Political History

\## Purpose

Defines standard UI components to keep the site consistent and fast to build.

---

\## 1) MetadataBar (required on all pages)

Shows:

\- Status (Template/Draft/Active)

\- Last updated (date)

\- Section + Type (small)

\- Sourcing status (Sources pending / Partially sourced / Fully sourced)

Inputs:

\- frontmatter fields + computed updated_at

---

\## 2) TagRow (recommended)

Displays clickable chips for:

\- Era

\- Power channels

\- Power mechanisms

\- Policy areas

\- Places

Rules:

\- Only show categories that exist on the page

\- Each chip routes to a tag hub listing page

---

\## 3) RelatedLinks (required for Events, recommended elsewhere)

Displays curated links grouped by:

\- Constitutions

\- Eras

\- Events

\- Power frameworks

\- Community pages

---

\## 4) ProvenanceBox (Phase 1 optional, Phase 2 required for data)

Displays:

\- Source name

\- Vintage

\- Retrieved date

\- Notes/limitations

\- Link to Sources page or provenance record

---

\## 5) SectionSidebar (required)

Context-aware:

\- Constitution: show constitutional arc

\- Timeline: show eras/events

\- Power: show channels

\- Tags: show categories

---

\## 6) Callout Blocks (optional, restrained)

Allowed types:

\- Note

\- Context

\- Definition

\- Caution (used sparingly)

No icons by default.
