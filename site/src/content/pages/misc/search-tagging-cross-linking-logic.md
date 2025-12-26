---
title: "Search, Tagging & Cross-Linking Logic"
description: "Stand Up Arkansas \u2014 The People\u2019s Political History"
tags:
  - migration:uncategorized
---
# Search, Tagging & Cross-Linking Logic
Stand Up Arkansas - The People's Political History

## 1) Core principle
Readers shouldn't have to know where something lives to find it.
Search and linking must let someone start from:
a person ("Brooks-Baxter War")
a concept ("preemption")
a place ("Phillips County")
a document ("Constitution of 1874")

 ...and still arrive at the right material fast.

## 2) Entity types (the things we can search and link)
These are the canonical "nodes" of the system (even before the database):
Constitution (1836, 1861, 1864, 1868, 1874, Amendment Era)
Era
Event
Power Channel (Rules, Gatekeepers, Money, Courts, Geography, Narrative)
Power Mechanism (preemption, disenfranchisement, etc.)
Community (place-based or group-based)
Institution (General Assembly, courts, agencies-prototype stubs)
Source (documents, archives)
Claim (later: atomic assertions, source-linked)
For the prototype, we'll implement 1-6 as first-class, and leave 7-9 as stubs that still tag and link.

## 3) Required frontmatter (minimal but powerful)
Every Markdown page gets frontmatter so the site can auto-index it.
### Standard fields (all pages)
---
title: ""
section: ""         # Constitution | Timeline | Power | Community | Legislature | Sources
type: ""            # constitution | era | event | framework | community | policy | explainer | source
status: ""          # template | draft | active
date: ""            # YYYY or YYYY-MM-DD or range (if event)
date_range: ""      # YYYY-YYYY (if era or long-form scope)
---
### Optional but strongly recommended
tags:
- ""
era:
- ""              # one or more era identifiers
power_channels:
- ""              # Rules, Gatekeepers, Money, Courts, Geography, Narrative
power_mechanisms:
- ""              # preemption, procedural_supremacy, disenfranchisement, etc.
places:
- ""              # county/city/region
institutions:
- ""              # General Assembly, courts, governor, etc.
people:
- ""              # names (later: ids)
related:
- ""              # internal slugs or URLs
---
Rule: If a page makes a big claim about power, it must include either a power_channels or power_mechanisms tag.

## 4) Tag taxonomy (controlled vocabulary)
To avoid chaos, tags are not freeform. We use controlled lists.
### A) Power channels (fixed list)
Rules
Gatekeepers
Money
Courts
Geography
Narrative
### B) Power mechanisms (growing list, curated)
Start with these (foundational):
procedural_supremacy
preemption
disenfranchisement
dilution_at_large
runoff_turnout_suppression
executive_weakening
executive_enforcement
judicial_delay
appointment_capture
funding_withdrawal
privatization
deregulation
carveout_exemptions
criminalization_of_participation
information_asymmetry
intimidation_violence
narrative_legitimation
### C) Policy areas (curated)
elections_representation
education
labor_economy
agriculture_land
health
environment_water
criminal_justice
local_government
taxation_budget
civil_rights
### D) Place tags (standardized)
county:Phillips
city:Little_Rock
region:Delta
district:HD_XX (later)
This makes search predictable.

## 5) Cross-linking rules (how pages connect)
### Minimum cross-links per page
Constitution page: must link to relevant era(s) + at least 2 events
Era page: must link to relevant constitution(s) + 3-10 events
Event page: must link to era + constitution (if relevant) + at least one power channel
Power mechanism page (future): must link to at least 3 examples (events or policies)
Community page: must link to at least 1 era + 1 power mechanism + 1 policy area
This creates a web, not a tree.
### "Related Pages" block (standardized)
Every page ends with:
Related Pages (links)
Tags (visible, clickable)
Status + last updated
Sources section (even if "pending")

## 6) Search modes (what users can do)
### Mode 1: Quick Search (global)
search bar in header
searches titles + summaries + tags
instant results grouped by type:
Constitutions
Eras
Events
Power Frameworks
Communities
### Mode 2: Filter Search (browse)
A dedicated search page with filters:
section/type
era
date range
power channel
power mechanism
policy area
place
### Mode 3: "Find Patterns" (future)
Once SQL is in place:
show clusters: "most common power mechanisms in the Amendment Era"
network view: "events connecting to preemption and local control"
"bill genealogy" style linking for repeated language (later)

## 7) Ranking logic (how results are ordered)
Even in a static prototype, we can rank.
Priority order:
Exact title match
Tag match (power_mechanisms, policy areas, places)
Section match (user filters)
Recency (for "Updates" and modern topics)
"Hub score" (pages with more inbound links rank higher)
Later, in SQL:
full-text ranking (tsvector)
popularity (clicks) if you choose, but not required

## 8) Auto-generated navigation pages (critical)
To feel "first-class," the site should generate:
### Tag index pages
/tags/power_mechanisms/preemption
/tags/policy_areas/education
/tags/places/county/Phillips
Each tag page shows:
definition (short)
linked pages grouped by type
timeline view of linked events
### Era dashboards
Each era shows:
top power mechanisms in that era
key constitutions
key communities
event list
These can be static now, dynamic later.

## 9) The "Cross-link engine" (how we do it now vs later)
### Now (Markdown prototype)
we store frontmatter tags
build-time index compiles JSON of pages and their metadata
search reads the index
### Later (SQL/Postgres)
entities become tables
tags become join tables
search becomes:
Postgres full-text
optional vector search
relationship traversal queries
Important: The UI stays the same.

## 10) "Definition-first tags" (adds moral clarity without editorializing)
For every power mechanism and policy area, we create a short definition page.
Example:
power/mechanisms/procedural_supremacy.md
definition
why it matters
Arkansas examples (linked)
sources / further reading (later)
This prevents the tag system from becoming jargon.
