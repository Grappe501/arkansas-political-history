---
title: "Place Registry"
description: "Stand Up Arkansas \u2014 The People\u2019s Political History"
tags:
  - migration:uncategorized
---

# Place Registry
Stand Up Arkansas — The People’s Political History

## Purpose
This document defines how geographic places are identified, named, and joined across datasets.

Consistency here determines whether data integration succeeds or fails.

---

## Canonical Place Types

1. State
2. County
3. City / Municipality
4. Census Tract (future)
5. School District (future)
6. Legislative District (future)

---

## Canonical Identifiers

### State
- State FIPS code
- Example: Arkansas = 05

### County
- County FIPS (state + county)
- Example: Phillips County = 05107

### City / Municipality
- Census Place GEOID
- Plus human-readable name
- Example: Little Rock (place GEOID)

---

## Naming Rules

- Use official Census names for identifiers.
- Display names may use common names.
- Avoid abbreviations unless standardized (e.g., “St.”).

---

## Place Table (Conceptual)

| field | description |
|------|------------|
| place_id | internal unique ID |
| name | display name |
| type | state / county / city |
| fips | FIPS or GEOID |
| parent_place_id | hierarchical parent |
| valid_from | start year |
| valid_to | end year (if applicable) |

---

## Boundary Changes

When boundaries change:
- Preserve historical records.
- Do not overwrite past data.
- Use `valid_from` / `valid_to` to track changes.

Boundary changes are political events and must remain visible.

---

## Why This Matters

Place is the primary join key across:
- Census
- BLS
- Elections
- Community impact pages

If place breaks, analysis breaks.
