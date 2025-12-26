---
title: "Provenance Schema"
description: "Stand Up Arkansas \u2014 The People\u2019s Political History"
tags:
  - migration:uncategorized
---

# Provenance Schema
Stand Up Arkansas — The People’s Political History

## Purpose
This document defines how data sources are tracked, audited, and referenced.

Every number must be explainable.

---

## Core Provenance Fields (Required)

### source_name
Plain-language name of source system
Example: "U.S. Census Bureau — ACS 5-Year"

---

### source_type
Primary / Secondary / Tertiary / Derived

---

### source_url
Landing page or API documentation URL
(Do not embed raw API keys.)

---

### retrieval_date
Date data was retrieved (ISO 8601)

---

### query_parameters
- API endpoint
- variables requested
- geographic scope
- filters applied

If file-based:
- file name
- originating URL
- checksum (if available)

---

### data_vintage
The reference period of the data
Example: "ACS 2019–2023"

---

### transformation_steps
Plain-language description of any processing:
- aggregation
- normalization
- suppression handling
- format conversion

---

### limitations
Known caveats, suppression, sampling error, or missing data.

---

## Provenance Table (Conceptual)

| field | description |
|------|------------|
| provenance_id | unique ID |
| source_name | source system |
| retrieval_date | when pulled |
| data_vintage | reference period |
| query_parameters | how retrieved |
| transformation_steps | what was done |
| limitations | known issues |

---

## Display Rules (Public-Facing)

For every data point shown publicly:
- Show source name
- Show data vintage
- Show retrieval date (or “last updated”)
- Link to source documentation

---

## Why This Matters

Provenance protects the archive from:
- accusations of fabrication,
- unintentional misuse,
- and loss of institutional memory.

Transparency is non-negotiable.
