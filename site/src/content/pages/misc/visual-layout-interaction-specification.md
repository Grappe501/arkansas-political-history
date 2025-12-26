---
title: "Visual Layout & Interaction Specification"
description: "Stand Up Arkansas \u2014 The People\u2019s Political History"
tags:
  - migration:uncategorized
---

# Visual Layout & Interaction Specification
Stand Up Arkansas — The People’s Political History

## 1) Design Philosophy (Non-Negotiable)
### Core feeling
A public archive you trust the moment you land on it.
The site should feel like:
a court record
a museum exhibit
a living ledger
Not:
a nonprofit landing page
a blog
a campaign site
### Emotional goals
Calm
Serious
Grounded
Slow (in a good way)
Credible to judges, journalists, and everyday Arkansans alike

## 2) Visual Identity System
### Color Palette (Elevated Stand Up Arkansas)
Primary
Charcoal / near-black → authority, gravity
Warm off-white / parchment → history, readability
Accent (use sparingly)
Deep Arkansas red or muted slate blue

 (never both on the same page)
Rules
No gradients
No bright primaries
No color-coded ideology
Contrast must pass accessibility
Color is supporting, not leading.

### Typography (this matters more than anything)
Primary type (long-form content)
Serif
High readability
Feels judicial / archival
Used for:
Constitutions
Analysis
Community impact narratives
Secondary type (UI + navigation)
Clean sans-serif
Neutral
Modern but restrained
Used for:
Menus
Metadata
Tags
Buttons
Rules
Never mix more than 2 families
Headings are understated
White space does the work

## 3) Page Layout System (Universal)
### Global layout structure
┌────────────────────────────────────┐
│ Header (Brand + Section Nav)        │
├───────────┬────────────────────────┤
│ Sidebar   │ Main Content            │
│ (Context) │                         │
│           │                         │
├───────────┴────────────────────────┤
│ Footer (Provenance + Status)        │
└────────────────────────────────────┘
### Header (persistent)
Stand Up Arkansas wordmark
Section navigation:
Constitution
Timeline
Power
Community
Legislature
Sources
No hero images.
No carousels.

### Sidebar (this is the secret weapon)
The sidebar is contextual, not global.
Examples:
On a Constitution page → shows the constitutional arc
On a Timeline page → shows eras
On a Power page → shows power channels
This teaches structure without explanation.

## 4) Homepage Interaction Spec
### Above the fold
Headline (no animation)
Subhead
3 primary entry actions
No scrolling gimmicks.
### Below the fold
Constitution Arc (horizontal or vertical spine)
Latest Additions (date-stamped)
How to Use This Archive (short, restrained)
Everything reinforces permanence.

## 5) Constitution Pages (Flagship Experience)
### Visual hierarchy
Title + date range
Context block (subtle shaded background)
Sectioned analysis
Long-term impact
Sources (collapsed by default)
### Interaction rules
No pop-ups
No tooltips
Footnote-style source links
Expand/collapse for deep dives
Constitution pages should feel weighty.

## 6) Timeline Pages
### Era index
Vertical list
Clear date ranges
One-sentence summaries
No images
### Event pages
Minimalist
Strong section separation
Cross-links to:
Constitution
Power channels
Community impact
Time is the organizing force.

## 7) Power Framework Pages
### Interaction goal
Teach how to see, not what to believe.
### Design choices
Short sections
Strong headings
Pull-quotes (used sparingly)
Cross-links embedded inline
No charts yet.
No icons.

## 8) Community Impact Pages
### Tone shift (subtle, not emotional)
Same structure
Slightly warmer spacing
Emphasis on patterns over anecdotes
### Future-ready blocks
Leave space (visually) for:
Census indicators
Trend lines
Comparative tables
But do not clutter now.

## 9) Metadata & Provenance (Visible Everywhere)
Every page includes, at the bottom:
Status: Draft / Active / Version #
Last updated
Source status:
Sources pending
Partially sourced
Fully sourced
This builds trust instantly.

## 10) Interaction Principles (Hard Rules)
### Never do this
Infinite scroll
Auto-playing anything
Gamification
“Engagement” tricks
Emotional imagery
### Always do this
Make structure visible
Show dates
Show evolution
Respect the reader’s intelligence

## 11) Accessibility & Ethics
Keyboard navigable
Screen-reader friendly
Plain language without simplification
No dark patterns
No data extraction without notice
This is a public good, not a product funnel.

## 12) How this scales to SQL later
Because:
pages already map to entities
sidebars map to relationships
metadata maps to tables
sources map to provenance records
The UI does not change when the backend does.
That’s intentional.

## 13) What this gives Stand Up Arkansas
This design:
signals seriousness instantly
earns institutional trust
supports organizing without campaigning
becomes a reference point for the state
It looks like something Arkansas should have had decades ago.
