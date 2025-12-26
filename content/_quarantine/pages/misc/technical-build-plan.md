---
title: "Technical Build Plan"
description: "Here\u2019s a technical build plan that matches your goals:"
tags:
  - migration:uncategorized
---

Here’s a technical build plan that matches your goals:
Prototype fast (Markdown-driven, “museum-grade” UI)
Deploy on Netlify
Scale indefinitely
Migrate to SQL/Postgres later without redesigning the site
Keep your “Brain” as versioned markdown logs
I’m going to pick the stack and standards so you can just execute.

## Stack decisions
### Frontend + content engine
SvelteKit (excellent for content-heavy sites + fast + clean routing)
mdsvex (Markdown → Svelte components, supports frontmatter)
Static-first (build pages from Markdown at build time)
### Hosting
Netlify (static deploy + optional serverless functions later)
### Future database (Phase 2)
Postgres hosted (recommend: Supabase or Neon)
ORM: Drizzle (simple, type-safe) or Prisma (heavier)
### Search (Phase 1)
Build-time generated search-index.json from Markdown frontmatter + excerpts

 Later: Postgres full-text search (tsvector) / optional vector search.

## Repository structure (first-class, scalable)

standup-arkansas-archive/
site/
src/
routes/
+layout.svelte
+page.svelte                 # homepage
constitution/
+page.svelte               # constitution index
[slug]/+page.svelte        # constitution page renderer
timeline/
power/
community/
legislature/
sources/
tags/
search/
lib/
components/
content/
utils/
styles/
tokens.css
typography.css
layout.css
static/
assets/
scripts/
build-search-index.ts
build-tag-index.ts
build-sitemaps.ts
package.json
svelte.config.js
netlify.toml

content/
index.md
start-here.md

constitutions/
index.md
000_constitution_module_overview.md
001_territorial_governance.md
002_constitution_1836.md
...

timeline/
index.md
eras/
events/

power/
index.md
rules.md
...

community/
index.md
...

sources/
index.md
...

tags/
index.md
power_mechanisms/
policy_areas/

governance/
index.md
...

legislature/
index.md
history.md
process-modern.md
...

data/
DATA_DICTIONARY.md
PLACE_REGISTRY.md
PROVENANCE_SCHEMA.md
census/
bls/
elections/
provenance/

brain/
2025/
2025-04-01.md
2025-04-02.md
decisions/
logs/

README.md

## Content standard (frontmatter + slugs)
Every Markdown page gets:
---
title: ""
section: ""
type: ""
status: "draft"
date: ""
date_range: ""
tags: []
era: []
power_channels: []
power_mechanisms: []
policy_areas: []
places: []
institutions: []
—

Routing rule:
file name becomes slug (e.g., constitution_1874.md → /constitution/constitution_1874)
later we can add an explicit slug: field if you want.

## Build mechanics (how Markdown becomes a “system”)
### 1) Page rendering
SvelteKit route loads Markdown by slug
mdsvex renders it into styled content
### 2) Auto navigation
At build time, generate JSON maps from the filesystem:
nav-constitution.json
nav-timeline.json
nav-power.json

 Sidebars use these maps so navigation is automatic.
### 3) Search index (Phase 1)
A build script scans all Markdown:
extracts frontmatter
generates excerpt
writes static/search-index.json
Search page filters results client-side.
### 4) Tag pages (Phase 1)
Generate:
tag index pages (static markdown you already started)
plus optional auto tag hubs (dynamic pages that list everything tagged “preemption”, “education”, etc.)
Static now: tag definition pages you wrote
Dynamic listing: built from the search index

## Styling plan (museum-grade without bloat)
### CSS tokens
Create tokens.css with:
spacing scale
font sizes
colors (charcoal, parchment, accent)
border + divider styles
### Typography rules
serif for content body
sans for UI and metadata
generous line height
strong whitespace
### Content components (reusable)
Build a few lightweight components:
MetadataBar (status, updated, sourcing status)
TagRow (clickable tags)
RelatedLinks
ProvenanceBox (for data panels later)

## Netlify deployment plan
### 1) Netlify config
Build command: npm run build
Publish directory: site/build (or .svelte-kit/output depending on adapter)
Use SvelteKit Netlify adapter:
@sveltejs/adapter-netlify
### 2) Environment variables (later)
For APIs (Census/BLS) you’ll store keys in Netlify env vars, not in repo.
### 3) Preview deploys
Netlify auto-builds every branch → you get staging URLs to review changes.

## Data integration (Phase 1: JSON panels, no DB)
Create data/provenance/ logs for each pull and write datasets into:
data/census/acs_county_2019_2023.json
data/bls/laus_county_2024.json
data/elections/open_elections_statewide_2000_2024.json
Then build a CommunitySnapshot component that loads relevant JSON by place key (FIPS) and displays:
Census: population, income, poverty
BLS: unemployment trend
Elections: last N races (later)
Each panel must show:
source name
vintage
retrieval date

 (from provenance metadata)

## Phase 2 migration to SQL (without redesign)
When you’re ready:
### Postgres tables (minimum)
place
indicator
indicator_value
election, race, result
source, source_pull
### Hybrid content model
Keep Markdown for:
narrative pages, frameworks, governance, constitutions
Use SQL for:
indicators, results, query-driven dashboards, pattern tools
The UI stays the same; only the data loaders change.

## Developer workflow (how you work from iPad + laptop)
### On iPad (now)
Keep writing Markdown (or txt that is Markdown)
Use consistent frontmatter
Store daily logs under brain/
### On laptop (execution)
Copy files into content/ and brain/
Run scripts to regenerate:
nav maps
search index
tag listings

## Concrete execution checklist (the next build steps)
### Week 1: Stand up the prototype
Initialize repo structure exactly as above
SvelteKit + mdsvex rendering for Markdown pages
Global layout + sidebar system
Constitution pages render + navigation works
Search index builds + basic search UI works
### Week 2: “First class” polish
Typography + spacing system
MetadataBar + tag click-through
Dynamic tag hub pages (list all pages tagged X)
Sitemap + SEO baseline (titles, descriptions)
### Week 3: Data-ready foundation
Add data/ loaders + provenance display
One sample CommunitySnapshot panel (even with placeholder JSON)
