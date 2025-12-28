---
title: "Interactive County Map Spec — Archetype Filters"
description: "Specification for an interactive Arkansas county map that filters by county archetype (Impact, Enforcement, Decision, Legitimacy), supports search and comparisons, and deep-links into county overlay pages and related throughlines."
tags:
  - section:pages
  - maps
  - counties
  - archetypes
  - spec
  - ui
  - build
contentType: "spec"
section: "Pages"
type: "Specification"
status: "Published"
slug: "/pages/specs/interactive-county-map-archetype-filters"
crosslinks:
  hub:
    - "/community/counties/archetypes"
    - "/community/counties/archetype-table"
  related:
    - "/community-impact/counties/faith-politics"
    - "/enforcement/statewide-geography"
    - "/frameworks/index"
---

# Interactive County Map Spec  
## Filters by Archetype + Deep Links Into the System

---

## Purpose

Build an interactive Arkansas county map that lets users:
- **see** the four county archetypes spatially,
- **filter** by archetype and overlays,
- **click** into each county’s pages,
- and **compare** counties side-by-side.

This map is not decoration.  
It is a navigation and comprehension engine.

---

## Primary Use Cases

### Use Case A — “Show me the system”
A user toggles archetypes to see how:
- Impact counties dominate the state,
- Decision power concentrates in a few places,
- Enforcement is geographically isolated,
- Legitimacy clusters around growth corridors.

### Use Case B — “I live here”
A user searches their county and sees:
- county archetype(s),
- key overlay links (faith/politics, county timeline),
- state-level crosslinks (courts, legislature, direct democracy).

### Use Case C — “Why did my reform fail?”
A user selects:
- the county where organizing happened,
- the county where the case was decided (often Pulaski),
- and the county where enforcement occurs (prisons / boards / sheriffs).

Map helps the user trace the path.

### Use Case D — “Compare two counties”
User selects two counties and gets a comparison card:
- archetype,
- institutional pathways,
- dominant frameworks,
- crosslinks.

---

## Data Model

Each county must have a stable record in a JSON registry used by the map.

### Canonical source file
`/content/data/counties/counties.registry.json`

### Required fields per county
```json
{
  "county": "Pulaski",
  "slug": "pulaski",
  "fips": "05119",
  "seat": "Little Rock",
  "region": ["Central"],
  "archetypePrimary": "Decision",
  "archetypeSecondary": ["Legitimacy"],
  "overlays": {
    "faithPolitics": "/community-impact/counties/pulaski/faith-politics",
    "countyTimeline": "/community-impact/counties/pulaski/timeline",
    "countyOverview": "/community-impact/counties/pulaski"
  },
  "crosslinks": {
    "enforcementGeography": "/enforcement/statewide-geography",
    "countyArchetypes": "/community/counties/archetypes",
    "archetypeTable": "/community/counties/archetype-table"
  },
  "frameworks": [
    "procedural-supremacy",
    "institutional-memory-as-power",
    "legitimacy-laundering"
  ],
  "notes": "Courts, agencies, capital hub."
}
