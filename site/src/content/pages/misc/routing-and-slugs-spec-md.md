---
title: "ROUTING_AND_SLUGS_SPEC.md"
description: "Stand Up Arkansas \u2014 The People\u2019s Political History"
tags:
  - migration:uncategorized
---
Stand Up Arkansas - The People's Political History

## 1. Purpose
This spec defines canonical URL routing, slug rules, and redirect behavior for the archive.
Goals:
Stable links for decades
No broken references as content grows
Deterministic mapping from /content/**.md → site routes
Clear rules for renames, moves, and version evolution
Hard rule: once published, a page's canonical URL should never change without a redirect.

## 2. Canonical routing model
### 2.1 Sections map to top-level routes
Each section has a top route:
Home → /
Constitution → /constitution
Timeline → /timeline
Power → /power
Community → /community
Legislature → /legislature
Sources → /sources
Tags → /tags
Governance → /governance
Search → /search
### 2.2 Content directory maps to route base
Each Markdown file lives under:
/content/&lt;routeBase&gt;/...
Example:
/content/constitutions/index.md → /constitution
/content/constitutions/006_constitution_1874.md → /constitution/006-constitution-1874
Route base mapping:
content/constitutions → /constitution
content/timeline → /timeline
content/power → /power
content/community → /community
content/legislature → /legislature
content/sources → /sources
content/tags → /tags
content/governance → /governance
Note: directory names can differ from section label (e.g., constitutions vs Constitution). The mapping above is authoritative.

## 3. Slug generation rules
### 3.1 Default slug is file-based
If no explicit slug is provided in frontmatter, the slug is generated from the filename.
Example:
006_constitution_1874.md → 006-constitution-1874
Reconstruction_era.md → reconstruction-era
### 3.2 Normalization
Slug normalization must:
lowercase
replace _ and spaces with -
remove non-alphanumeric except -
collapse multiple - into one
trim leading/trailing -
### 3.3 Numeric prefixes
If a filename begins with a numeric ordering prefix (001_, 010_), keep the number in the slug.
Why: preserves ordering and avoids collisions.
Example:
001_territorial_governance.md → 001-territorial-governance
### 3.4 Index pages
Any index.md maps to the directory route.
Examples:
/content/constitutions/index.md → /constitution
/content/timeline/index.md → /timeline
/content/timeline/eras/index.md → /timeline/eras

## 4. Optional explicit slugs (recommended for "forever pages")
slug: "constitution/1874"

Rules:
Explicit slugs override file-based slugs.
Must not begin with / (store as relative path).
Must be unique across the site.
If used, create a redirect from the old file-based URL if it was ever deployed.
Recommendation: Use explicit slugs for long-lived "pillar" pages once stable, e.g.:
constitution/1874
power/rules
tags/policy-areas/education

## 5. Route patterns by section
### Constitution
Index: /constitution
Pages: /constitution/&lt;slug&gt;
### Timeline
Index: /timeline
Eras index: /timeline/eras
Era pages: /timeline/eras/&lt;slug&gt;
Events index: /timeline/events
Event pages: /timeline/events/&lt;slug&gt;
### Power
Index: /power
Channel pages: /power/&lt;slug&gt;
Mechanisms (tag definitions): /tags/power_mechanisms/&lt;slug&gt;
### Community
Index: /community
Place pages: /community/places/&lt;slug&gt; (recommended)
Policy impact pages: /community/policy/&lt;slug&gt; (optional later)
### Tags
Index: /tags
Category index: /tags/&lt;category&gt;
Tag definition page: /tags/&lt;category&gt;/&lt;tag&gt;
Category route names should be:
power_mechanisms
policy_areas
(later) places, institutions, people
### Governance
Index: /governance
Pages: /governance/&lt;slug&gt;

## 6. Canonical URL and redirects
### 6.1 Canonical URL
Every page must declare its canonical URL (UI-level meta tag) as the route produced by the rules above.
### 6.2 Redirect requirements
A redirect is required when:
a file is renamed
a file is moved to a different folder
an explicit slug is introduced after deployment
a typo in a slug is corrected
Redirects should be declared in netlify.toml (preferred) or _redirects.
/constitution/006-constitution-1874   /constitution/1874   301

### 6.3 Redirect permanence
All redirects are permanent (301) unless explicitly temporary for testing.

## 7. Collision handling
If two pages resolve to the same slug:
Prefer the one with explicit slug
Otherwise fail build in strict mode
In prototype mode: warn + append -2 to the second slug (not recommended long-term)
Goal: no collisions in production.

## 8. Link conventions inside Markdown
### 8.1 Prefer absolute internal links
Use site-root paths:
/constitution/1874
/timeline/eras/reconstruction
Avoid relative file links like ../constitutions/....
### 8.2 "Related Pages" blocks
Related links should use canonical routes.
If a link target is unknown yet, use placeholder text without fake URLs.

## 9. Deprecation policy
If a page is replaced or merged:
Keep the original URL alive
Add a banner at the top:
"This page has been merged into: [New Page]."
Do not delete public pages without a redirect.

## 10. Implementation checklist
Build scripts must:
compute slugs deterministically
emit slug in search-index.json, nav.json, tags-index.json
detect collisions
emit redirect suggestions to build-manifest.json warnings (optional enhancement)
