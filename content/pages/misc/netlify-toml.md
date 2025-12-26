---
title: "Netlify.toml"
description: "\\# Stand Up Arkansas \u00e2\u20ac\u201d The People\u00e2\u20ac\u2122s Political History"
tags:
  - migration:uncategorized
---

\# netlify.toml

\# Stand Up Arkansas â€” The Peopleâ€™s Political History

\# SvelteKit + adapter-netlify

\[build\]

base = "site"

command = "npm run build:indexes && npm run build"

publish = "build"

\# If you use environment variables (API keys, etc.), set them in Netlify UI.

\[build.environment\]

NODE_VERSION = "20"

\# Optional: keep builds deterministic and avoid noisy caching issues early on

\[context.production.environment\]

NODE_ENV = "production"

\# Optional: Security headers (safe defaults; adjust CSP later once assets are known)

\[\[headers\]\]

for = "/\*"

\[headers.values\]

X-Frame-Options = "DENY"

X-Content-Type-Options = "nosniff"

Referrer-Policy = "strict-origin-when-cross-origin"

Permissions-Policy = "geolocation=(), microphone=(), camera=()"

\# Optional: redirect examples (add more as you create forever slugs)

\# \[\[redirects\]\]

\# from = "/constitution/006-constitution-1874"

\# to = "/constitution/1874"

\# status = 301

\# force = true
