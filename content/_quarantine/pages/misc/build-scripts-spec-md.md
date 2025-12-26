---
title: "1. Purpose"
description: "This document specifies the build-time scripts that turn Markdown content into a navigable, searchable, first-class civic archive."
tags:
  - migration:uncategorized
---

## 1. Purpose
This document specifies the build-time scripts that turn Markdown content into a navigable, searchable, first-class civic archive.
Scripts must:
run locally during development and in Netlify builds,
be deterministic and repeatable,
generate stable JSON artifacts used by the UI,
preserve provenance for generated artifacts where relevant.
This spec is designed for a static-first build and scales cleanly to a future SQL-backed build.

## 2. Inputs
### 2.1 Content directory (primary input)
/content/**.md
All Markdown pages with YAML frontmatter per CONTENT_STANDARDS.md.
### 2.2 Data directory (optional input)
/data/**
Used later for building data panels and cross-linking.
### 2.3 Controlled vocabularies
/content/tags/** definition pages (power mechanisms, policy areas, etc.)
Optional (recommended later): /content/_taxonomies/*.json for canonical lists

## 3. Outputs (Build Artifacts)
All build artifacts are written to:
site/static/_index/
So they can be fetched client-side and cached.
### Required output files
nav.json
search-index.json
tags-index.json
sitemap.json
build-manifest.json

## 4. Canonical Page Record Shape
All scripts must produce normalized page records with this minimal schema:
{
"id": "content/constitutions/006_constitution_1874.md",
"slug": "/constitution/006_constitution_1874",
"title": "Arkansas Constitution of 1874",
"section": "Constitution",
"type": "constitution",
"status": "active",
"date": "1874",
"date_range": "1874–Present",
"era": ["Redemption & Jim Crow Consolidation (1874–1940s)"],
"tags": ["constitution", "arkansas"],
"power_channels": ["Rules"],
"power_mechanisms": ["executive_weakening"],
"policy_areas": ["elections_representation"],
"places": ["state:AR"],
"institutions": ["General Assembly"],
"excerpt": "The Arkansas Constitution of 1874 was adopted after the collapse of Reconstruction...",
"headings": ["Context", "Conditions of Adoption", "Core Structural Changes", "Power Analysis"],
"updated_at": "2025-04-01T00:00:00.000Z"
}

### Rules
slug must be stable across builds.
excerpt must be deterministic (same input → same excerpt).
updated_at should come from git last modified time if available; otherwise file mtime.

## 5. Script 1 — Navigation Builder
### Name
build-nav.ts
### Goal
Generate a complete navigation structure for:
global top nav,
section sidebars,
and next/previous ordering within sections.
### Inputs
all content pages with section and type
### Outputs
nav.json with:
topNav: ordered list of primary sections
sidebars: per-section ordered lists
ordering: explicit ordering arrays
Example structure

{
"topNav": [
{"label": "Constitution", "href": "/constitution"},
{"label": "Timeline", "href": "/timeline"},
{"label": "Power", "href": "/power"},
{"label": "Community", "href": "/community"},
{"label": "Legislature", "href": "/legislature"},
{"label": "Sources", "href": "/sources"},
{"label": "Tags", "href": "/tags"}
],
"sidebars": {
"Constitution": [
{"title": "Overview", "slug": "/constitution"},
{"title": "Territorial Governance", "slug": "/constitution/001_territorial_governance"},
{"title": "Constitution of 1836", "slug": "/constitution/002_constitution_1836"}
],
"Timeline": [
{"title": "Timeline", "slug": "/timeline"},
{"title": "Eras", "slug": "/timeline/eras"},
{"title": "Events", "slug": "/timeline/events"}
]
},
"nextPrev": {
"/constitution/002_constitution_1836": {
"prev": "/constitution/001_territorial_governance",
"next": "/constitution/003_constitution_1861"
}
}
}

### Ordering rules
If filename begins with numeric prefix (001_, 002_), sort numerically.
Otherwise sort by date (if present), then title.
index.md is always first within its folder.
Preserve curated “arc” ordering for constitutions.

## 6. Script 2 — Search Index Builder
### Name
build-search-index.ts
### Goal
Generate a client-searchable index that supports:
keyword search (title + excerpt + tags),
filtering by section/type/era/date/tags.
### Outputs
search-index.json with array of normalized page records.
### Excerpt generation
Use the first non-empty paragraph after the first H1, stripped of markdown.
Cap at 240 characters (word boundary).
Must be deterministic.
### Tokenization (for lightweight search)
Include a tokens field for client search (optional but recommended):
"tokens": ["arkansas", "constitution", "1874", "executive", "weakening"]

Rules:
lowercase
strip punctuation
split on whitespace
include frontmatter tags as tokens

## 7. Script 3 — Tags Index Builder
### Name
build-tags-index.ts
### Goal
Create a complete mapping of:
tag → pages
tag category → tag list
tag definition pages (if they exist)
### Outputs
tags-index.json
Example structure

{
"categories": {
"power_mechanisms": ["procedural_supremacy", "preemption", "disenfranchisement"],
"policy_areas": ["education", "elections_representation"]
},
"definitions": {
"power_mechanisms/procedural_supremacy": "/tags/power_mechanisms/procedural_supremacy",
"policy_areas/education": "/tags/policy_areas/education"
},
"tagToPages": {
"power_mechanisms:preemption": [
"/tags/power_mechanisms/preemption",
"/power/geography",
"/timeline/events/example_preemption_event"
],
"policy_areas:education": [
"/tags/policy_areas/education",
"/constitution/005_constitution_1868"
]
}
}

### Rules
Treat frontmatter arrays as authoritative tag assignments.
Tag key format: {category}:{value}
Include tag definition pages as first results when present.

## 8. Script 4 — Sitemap Builder
### Name
build-sitemap.ts
### Goal
Generate a machine-readable sitemap for internal use and SEO.
### Outputs
sitemap.json
Structure:
{
"generated_at": "2026-01-01T12:00:00Z",
"urls": [
{"slug": "/", "section": "Home"},
{"slug": "/constitution", "section": "Constitution"},
{"slug": "/constitution/006_constitution_1874", "section": "Constitution"}
]
}

Optional: also write site/static/sitemap.xml if desired.

## 9. Script 5 — Build Manifest
### Name
build-manifest.ts
### Goal
Record build metadata for debugging and transparency.
### Outputs
build-manifest.json
Fields:
{
"build_time": "2026-01-01T12:00:00Z",
"content_pages_indexed": 142,
"nav_version": "1",
"search_index_version": "1",
"tags_index_version": "1",
"git_commit": "abc123 (if available)",
"warnings": [
"Missing status in content/community/foo.md",
"Unknown power_mechanism tag: 'foo_bar'"
]
}

## 10. Validation & Warnings (Required)
All build scripts must validate:
### Required frontmatter fields
title
section
type
status
### Controlled vocabulary checks
power_channels must be one of: Rules, Gatekeepers, Money, Courts, Geography, Narrative
power_mechanisms must exist in /content/tags/power_mechanisms/ (or approved list)
policy_areas must exist in /content/tags/policy_areas/ (or approved list)
### Output behavior
Build should not fail on validation warnings in early prototype phase.
It should log warnings to build-manifest.json.
Later, warnings can be promoted to failures.

## 11. Netlify Integration
Netlify build pipeline should run in this order:
npm run build:indexes
runs nav/search/tags/sitemap/manifest scripts
npm run build
SvelteKit build consumes generated artifacts in site/static/_index/
{
"scripts": {
"build:indexes": "ts-node scripts/build-nav.ts && ts-node scripts/build-search-index.ts && ts-node scripts/build-tags-index.ts && ts-node scripts/build-sitemap.ts && ts-node scripts/build-manifest.ts",
"build": "svelte-kit build"
}
}
## 12. Future SQL Migration Notes
When SQL is introduced:
search-index.json becomes optional (or fallback).
tags-index.json becomes dynamic from join tables.
nav.json may remain build-time (content-driven) or move to DB if desired.
Slugs remain stable (critical).
The UI should not need redesign—only loaders change.

## 13. Definition of Done
This spec is considered implemented when:
Navigation sidebars populate automatically from content.
Search returns results with filters by:
type, era, power mechanism, policy area, place.
Tag pages show all linked pages reliably.
Build manifest reports warnings and counts.
Builds are deterministic (same content → same outputs).
