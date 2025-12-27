---
title: "1) Guiding rules for data in this archive"
description: "traceable (source + query + date pulled)"
tags:
  - migration:uncategorized
---
## 1) Guiding rules for data in this archive
Data must be:
traceable (source + query + date pulled)
repeatable (same request yields same output for that vintage)
joinable (links to Place, Era, Policy Area, and Events)
explainable (plain-language labels, not just codes)
This matches your Sources/Provenance framework.
Census API is explicitly designed for retrieving official datasets via API calls and keys.
BLS offers an API with v2 requiring registration for expanded access/optional params.
Arkansas election results are available through the Secretary of State's election results research pages, and OpenElections provides Arkansas CSVs converted from official PDFs.

## 2) Data domains and what they unlock
### A) Census (Demographics + socioeconomics)
Use cases
show community change over time (race/ethnicity, age, household composition)
tie political structures to population shifts (e.g., at-large dilution, annexation impacts)
power analysis grounding ("who lived here when the rules were written?")
Primary feeds
ACS 5-year for consistent county/city tract-level indicators (annual-ish, smoother)
Decennial Census for long-term anchors (every 10 years)
Optional: SAIPE (poverty estimates) if needed later
### B) BLS (Jobs, wages, unemployment, industry)
Use cases
connect policy eras to labor outcomes (Delta decline, manufacturing shifts)
build "Community Health" panels: unemployment trend, wage trend, industry mix
support "impact" narratives with measurable outcomes
Primary feeds
LAUS (Local Area Unemployment Statistics) for counties/MSAs
QCEW (Quarterly Census of Employment and Wages) for industry detail

 BLS API v2 supports optional parameters and requires a registration key for expanded access.
### C) Elections (Results + administration)
Use cases
representation outcomes over time (who wins, margins, turnout proxies)
detect structural patterns (runoffs, at-large, district changes)
build local "representation history" pages
Primary feeds
Arkansas SOS election results repository (official publications)
OpenElections Arkansas (CSV normalization layer for many years)
Optional governance/admin dataset: EAC Election Administration and Voting Survey (state-by-state administration metrics).

## 3) The integration plan (phased, realistic, scalable)
### Phase 1 - "Data-ready prototype" (no SQL required yet)
Goal: get data panels working as generated JSON that the site reads.
Deliverables
A /data/ folder with versioned JSON:
/data/census/
/data/bls/
/data/elections/
A /data/provenance/ log that records:
source system
endpoint or file
query parameters
pull timestamp
transformations performed
A "Community Snapshot" component that can render:
demographics (Census)
unemployment trend (BLS)
election results list (SOS/OpenElections)
Why this first: it makes the site feel alive immediately, without a DB.
### Phase 2 - "Normalized SQL backbone" (Postgres)
Goal: support real querying, cross-linking, and pattern discovery.
Core tables (minimum)
place (state/county/city/tract, plus GIS IDs like FIPS)
indicator (what metric is this)
indicator_value (place_id, indicator_id, date, value, source_id)
election (date, election_type, jurisdiction)
race (office, district, party rules, etc.)
result (race_id, candidate_id, votes, pct)
source + source_pull (provenance)
page_entity_link (connect data to your Markdown "entities")
### Phase 3 - "Pattern layer"
Goal: make "Find Patterns" real:
maps of change (demographic + economic)
structural flags (at-large, runoff, preemption)
correlations across eras (not causal claims-just patterns to investigate)

## 4) Your canonical join keys (do this right and everything works)
### Places
Standardize on:
State FIPS
County FIPS
Optional later: Census tract/block group GEOIDs
This lets Census + BLS + elections all attach to "place."
### Time
Use:
year for long series
date for election events
vintage where datasets are vintage-based (Census/ACS)
### Election jurisdictions
You'll need a "jurisdiction registry":
statewide
county
city
district (state house/senate, congressional)

## 5) What to pull first (high impact, low complexity)
### First 10 Census indicators (suggested)
For each county (and later city/tract):
total population
race/ethnicity breakdown
median household income
poverty rate
educational attainment (HS+, BA+)
housing tenure (owner/renter)
age brackets (youth, working age, seniors)
### First 5 BLS indicators
For each county:
unemployment rate
labor force
employed
unemployed
(optional) industry employment mix via QCEW later
### First elections dataset slice
Start with General elections (cleanest), statewide & federal:
Governor
U.S. Senate
U.S. House

 Then expand into:
state legislative
local municipal systems (at-large/ward)
SOS has structured election results archives by year and election type, and OpenElections provides processed CSVs for Arkansas.

## 6) Provenance rules (so nobody can ever call it "made up")
Every dataset you import must carry:
source_name
source_url (or reference)
retrieved_at
query_params (or file name + checksum)
transform_steps (e.g., "PDF→CSV normalized by OpenElections")
This is especially important for elections, because official records are often PDFs and aggregations vary; OpenElections explicitly notes its Arkansas repo converts official PDFs into CSV.

## 7) How it shows up on the site (first-class UX)
For each Community page, add a section:
### "Community Snapshot"
Demographics (Census)
Economy (BLS)
Representation (Elections)
Each metric shows:
value
year/date
small "Source" link
"Pulled on" date
For each Era page, add:
"Era Indicators" (statewide trends)
"Counties most changed" (later)
"Key elections" (links)
For Policy Area pages, add:
"Indicators that reflect this policy area" (e.g., education attainment, poverty, turnout proxies)
