#!/usr/bin/env python3
r"""
Stand Up Arkansas — Level 2 Dashboard Scaffold (Deliverable A/B)

Run:
  cd C:\Users\User\Desktop\Arkansas_Political_History\site
  py scripts\scaffold_l2.py
"""

from __future__ import annotations
from pathlib import Path
from datetime import date

# =========================
# CONFIG
# =========================
ROOT = Path(r"C:\Users\User\Desktop\Arkansas_Political_History\site")  # <- your SvelteKit app root

# TEMP: set True to regenerate existing scaffold files with new layout/page shell
OVERWRITE = False

TODAY = date.today().isoformat()

LOCALES = ["en", "es"]

LEVEL2_SECTIONS: dict[str, list[str]] = {
    "foundations": ["intro", "framework"],
    "power": ["institutions", "chokepoints"],
    "money": ["donors", "contracts"],
    "process": ["committees", "floor"],
    "people": ["roles", "networks"],
    "cases": ["atlarge", "directdem"],
    "toolkit": ["foia", "meetings"],
    "sources": ["provenance", "standards"],
    "trackers": ["bills", "votes"],
    "about": ["mission", "governance"],
}

ARTICULATE_PLACEHOLDER = "https://articulate.placeholder.tld"
LEVEL3_GATE_EMAIL = "standuparkansas@gmail.com"

# =========================
# HELPERS
# =========================
def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def write_file(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    if path.exists() and not OVERWRITE:
        return
    path.write_text(content, encoding="utf-8")

def svelte_page(title: str, body: str) -> str:
    # NOTE: Layout provides shell/topbar/main.
    # Pages should render inside a .prose card for consistent styling.
    return f"""<script lang="ts">
  import {{ siteConfig }} from '$lib/siteConfig';
</script>

<svelte:head>
  <title>{title} • {{siteConfig.siteName}}</title>
</svelte:head>

<section class="prose">
  <header class="page-header">
    <h1>{title}</h1>
  </header>

{body}
</section>

<style>
  .page-header {{
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.75rem;
    margin-bottom: 1rem;
  }}
  .page-header h1 {{
    margin: 0;
  }}
</style>
"""

def md_placeholder(
    locale: str,
    section: str,
    topic: str,
    title: str,
    description: str,
    tags=None,
    status=None,
    lesson_slug=None
) -> str:
    tags = tags or []
    status = status or ("ready" if locale == "en" else "translating")
    lesson_line = f'lesson_slug: "{lesson_slug}"\n' if lesson_slug else ""
    tags_yaml = "[" + ", ".join([f'"{t}"' for t in tags]) + "]"
    lead = "**ENGLISH PLACEHOLDER (authoritative for now).**" if locale == "en" else "**ESPAÑOL: En traducción.**"

    return f"""---
title: "{title}"
description: "{description}"
section: "{section}"
topic: "{topic}"
tags: {tags_yaml}
{lesson_line}status: "{status}"
updated: "{TODAY}"
provenance: []
---

{lead}

## What this page will teach

- Replace this with doctorate-level civic instruction.
- Keep it practical: what a person can do *today*.

## Key terms

- Term 1 — definition
- Term 2 — definition

## Sources

- Add primary documents and provenance IDs here.
"""

# =========================
# PATHS
# =========================
SRC = ROOT / "src"
ROUTES = SRC / "routes"
LIB = SRC / "lib"
CONTENT = ROOT / "content"
DOCS = ROOT / "docs"

def route_file(*parts: str) -> Path:
    return ROUTES.joinpath(*parts)

def content_file(locale: str, *parts: str) -> Path:
    return CONTENT.joinpath(locale, *parts)

# =========================
# GENERATORS
# =========================
def create_lib() -> None:
    ensure_dir(LIB)

    write_file(
        LIB / "siteConfig.ts",
        f"""export const siteConfig = {{
  siteName: "Stand Up Arkansas",
  articulateBaseUrl: "{ARTICULATE_PLACEHOLDER}",
  level3GateEmail: "{LEVEL3_GATE_EMAIL}",
  level3Enabled: (import.meta.env.PUBLIC_LEVEL3_ENABLED ?? "false") === "true"
}};
"""
    )

    write_file(
        LIB / "nav.ts",
        """export const level2Sections = [
  { slug: "foundations", label: "Foundations" },
  { slug: "power", label: "Power Map" },
  { slug: "money", label: "Money & Influence" },
  { slug: "process", label: "Rules & Process" },
  { slug: "people", label: "People & Networks" },
  { slug: "cases", label: "Case Files" },
  { slug: "toolkit", label: "Civic Toolkit" },
  { slug: "sources", label: "Sources & Provenance" },
  { slug: "trackers", label: "Trackers" },
  { slug: "about", label: "About & Governance" }
];
"""
    )

def create_locale_layout() -> None:
    # This layout matches your app.css: .shell .topbar .topbar-inner .main .prose
    # Includes language toggle + theme toggle.
    write_file(
        route_file("[locale]", "+layout.svelte"),
        f"""<script lang="ts">
  import {{ page }} from '$app/stores';
  import {{ browser }} from '$app/environment';
  import {{ siteConfig }} from '$lib/siteConfig';
  import {{ getTheme, setTheme, type Theme }} from '$lib/theme';

  $: locale = $page.params.locale ?? 'en';
  $: otherLocale = locale === 'en' ? 'es' : 'en';
  $: pathRemainder = $page.url.pathname.replace(/^\\/(en|es)/, '');
  $: switchHref = `/${{otherLocale}}${{pathRemainder}}${{$page.url.search}}`;

  let theme: Theme = 'system';
  if (browser) theme = getTheme();

  function toggleTheme() {{
    const next: Theme =
      theme === 'light' ? 'dark'
      : theme === 'dark' ? 'system'
      : 'light';

    theme = next;
    setTheme(next);
  }}
</script>

<div class="shell">
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="/{{$page.params.locale}}/l2">
        {{siteConfig.siteName}}
        <small>Arkansas Political History • Level 2</small>
      </a>

      <nav class="nav">
        <a href="/{{$page.params.locale}}/l2">Level 2</a>
        <a href="/{{$page.params.locale}}/ideas">Ideas</a>
        <a href="/{{$page.params.locale}}/search">Search</a>
        <a href="/{{$page.params.locale}}/l3">Level 3</a>
      </nav>

      <div class="controls">
        <a class="pill" href={{switchHref}} aria-label="Switch language">
          {{locale === 'en' ? 'ES' : 'EN'}}
        </a>

        <button class="pill" type="button" on:click={{toggleTheme}} aria-label="Toggle theme">
          {{theme === 'light' ? '☀️' : theme === 'dark' ? '🌙' : '🖥️'}}
        </button>
      </div>
    </div>
  </header>

  <main class="main">
    <slot />
  </main>
</div>

<style>
  .nav {{
    margin-left: auto;
    display: flex;
    gap: 1rem;
    align-items: center;
    flex-wrap: wrap;
  }}

  .nav a {{
    text-decoration: none;
    color: var(--text);
    opacity: 0.92;
  }}
  .nav a:hover {{
    text-decoration: underline;
    opacity: 1;
  }}

  .controls {{
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin-left: 0.75rem;
  }}

  .pill {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 44px;
    height: 36px;
    padding: 0 0.75rem;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--panel);
    color: var(--text);
    text-decoration: none;
    cursor: pointer;
    line-height: 1;
  }}
  button.pill {{
    font: inherit;
  }}

  @media (max-width: 760px) {{
    .topbar-inner {{
      align-items: flex-start;
      flex-direction: column;
      gap: 0.75rem;
    }}
    .nav {{
      margin-left: 0;
    }}
    .controls {{
      margin-left: 0;
    }}
  }}
</style>
"""
    )

def create_level2_routes() -> None:
    write_file(
        route_file("[locale]", "l2", "+page.svelte"),
        svelte_page(
            "Level 2 Dashboard",
            """<p><strong>Purpose:</strong> doctorate-level civic power literacy for Arkansas — practical, source-backed, community-centered.</p>

<div class="grid">
  <a class="card" href="/{$page.params.locale}/l2/foundations">Foundations</a>
  <a class="card" href="/{$page.params.locale}/l2/power">Power Map</a>
  <a class="card" href="/{$page.params.locale}/l2/money">Money & Influence</a>
  <a class="card" href="/{$page.params.locale}/l2/process">Rules & Process</a>
  <a class="card" href="/{$page.params.locale}/l2/people">People & Networks</a>
  <a class="card" href="/{$page.params.locale}/l2/cases">Case Files</a>
  <a class="card" href="/{$page.params.locale}/l2/toolkit">Civic Toolkit</a>
  <a class="card" href="/{$page.params.locale}/l2/sources">Sources & Provenance</a>
  <a class="card" href="/{$page.params.locale}/l2/trackers">Trackers</a>
  <a class="card" href="/{$page.params.locale}/l2/about">About & Governance</a>
</div>

<style>
  .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.8rem; }
  .card {
    display:block; padding: 1rem; border: 1px solid var(--border);
    border-radius: 14px; text-decoration:none;
    background: rgba(0,0,0,0.02);
  }
  :global(:root[data-resolved-theme="dark"]) .card { background: rgba(255,255,255,0.03); }
  .card:hover { text-decoration: underline; }
</style>
"""
        ),
    )

    for section, topics in LEVEL2_SECTIONS.items():
        write_file(
            route_file("[locale]", "l2", section, "+page.svelte"),
            svelte_page(
                f"Level 2 • {section}",
                "<p>This section is scaffolded. Topic pages are linked below.</p>\n"
                + "<ul>\n"
                + "\n".join([f'  <li><a href="/{{$page.params.locale}}/l2/{section}/{t}">{t}</a></li>' for t in topics])
                + "\n</ul>\n",
            ),
        )

        for topic in topics:
            write_file(
                route_file("[locale]", "l2", section, topic, "+page.svelte"),
                svelte_page(
                    f"{section}/{topic}",
                    f"""<p><em>Placeholder topic page.</em></p>
<p>Planned content source: <code>content/{{$page.params.locale}}/l2/{section}/{topic}.md</code></p>

<p>
  <a href="/{{$page.params.locale}}/ideas/submit">Submit an idea</a> for improving this page.
</p>

<p>
  Lesson (Articulate placeholder):<br />
  <a href="{{siteConfig.articulateBaseUrl}}/{{$page.params.locale}}/l2/{section}/{topic}" rel="noopener">
    {{siteConfig.articulateBaseUrl}}/{{$page.params.locale}}/l2/{section}/{topic}
  </a>
</p>
""",
                ),
            )

def create_search_tag_l3_routes() -> None:
    write_file(
        route_file("[locale]", "search", "+page.svelte"),
        svelte_page(
            "Search",
            "<p>Search UI scaffold. Separate EN/ES indexes will be generated later.</p>\n"
            "<p><code>/static/search-en.json</code> and <code>/static/search-es.json</code> (planned)</p>\n",
        ),
    )

    write_file(
        route_file("[locale]", "t", "[tag]", "+page.svelte"),
        svelte_page(
            "Tag",
            "<p>Tag hub scaffold.</p>\n"
            "<p>Tag: <strong>{$page.params.tag}</strong></p>\n",
        ),
    )

    write_file(
        route_file("[locale]", "l3", "+page.svelte"),
        svelte_page(
            "Level 3 • Action (Gated)",
            f"""{{#if siteConfig.level3Enabled}}
  <p><strong>Level 3 is enabled.</strong> (Wire the action dashboard routes next.)</p>
{{:else}}
  <p><strong>Level 3 is gated.</strong> To request access, email <a href="mailto:{LEVEL3_GATE_EMAIL}">{LEVEL3_GATE_EMAIL}</a>.</p>
  <p>Include:</p>
  <ul>
    <li>Your full name</li>
    <li>Your phone number</li>
    <li>Your county/city</li>
    <li>How you want to help (organizing, research, outreach, etc.)</li>
  </ul>
  <p>We’ll verify identity and respond with next steps.</p>
{{/if}}
""",
        ),
    )

def create_ideas_routes() -> None:
    write_file(
        route_file("[locale]", "ideas", "+page.svelte"),
        svelte_page(
            "Public Ideas (Pending Approval)",
            """<p>
  This is a public intake space. Submissions are <strong>reviewed and approved</strong> before appearing in the dashboard.
</p>
<p><a href="/{$page.params.locale}/ideas/submit">Submit an idea</a></p>

<hr />

<p><em>Approved ideas list will render here later.</em></p>
<p>Approval workflow: see <code>/docs/IDEAS_WORKFLOW.md</code></p>
""",
        ),
    )

    form_body = f"""<p>
  Submit an idea to improve the Arkansas Political History dashboard. We require an email to verify identity.
</p>

<form name="ideas" method="POST" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="ideas" />

  <p style="display:none;">
    <label>Don’t fill this out: <input name="bot-field" /></label>
  </p>

  <label>
    Full name<br />
    <input name="name" required />
  </label>
  <br /><br />

  <label>
    Email (required for identity verification)<br />
    <input name="email" type="email" required />
  </label>
  <br /><br />

  <label>
    County / City<br />
    <input name="location" />
  </label>
  <br /><br />

  <label>
    Idea title<br />
    <input name="title" required />
  </label>
  <br /><br />

  <label>
    Your idea (details)<br />
    <textarea name="details" rows="8" required></textarea>
  </label>
  <br /><br />

  <label>
    Links / sources (optional)<br />
    <textarea name="sources" rows="4"></textarea>
  </label>
  <br /><br />

  <button type="submit">Submit idea</button>
</form>

<p style="margin-top:1rem;">
  <strong>Note:</strong> Before Level 3 access, request a password by emailing
  <a href="mailto:{LEVEL3_GATE_EMAIL}">{LEVEL3_GATE_EMAIL}</a>.
</p>
"""
    write_file(
        route_file("[locale]", "ideas", "submit", "+page.svelte"),
        svelte_page("Submit an Idea", form_body),
    )

def create_content_placeholders() -> None:
    for locale in LOCALES:
        for section, topics in LEVEL2_SECTIONS.items():
            for topic in topics:
                title = f"{section.title()} — {topic.title()}"
                desc = f"Level 2 topic: {section}/{topic}."
                tags = [section, topic] if section != "about" else [topic]
                write_file(
                    content_file(locale, "l2", section, f"{topic}.md"),
                    md_placeholder(locale, section, topic, title, desc, tags=tags),
                )

def create_docs() -> None:
    ensure_dir(DOCS)
    write_file(
        DOCS / "IDEAS_WORKFLOW.md",
        """# Ideas Workflow (Public → Pending → Approved)

## Goal
Allow the public to submit ideas while keeping the dashboard **curated, accurate, and safe**.
All ideas are treated as **pending** until reviewed.

## Intake
- Public submit form route:
  - /en/ideas/submit
  - /es/ideas/submit
- Form is configured for **Netlify Forms** (no backend required).
- Required: **name + email** (identity verification).

## Review
1. Review submissions in Netlify dashboard (Forms).
2. Verify identity:
   - If necessary, reply requesting confirmation details.
3. Classify:
   - Content improvement
   - New case file request
   - Source submission
   - Bug/UI issue
   - Other

## Approval + Publishing
- Approved ideas should be manually added to an approved list (future):
  - content/{locale}/ideas/approved/*.md (recommended)
- For now, approval is tracked via Netlify + internal notes.

## Level 3 Gate
- Level 3 remains gated until identity verification.
- Access request email: standuparkansas@gmail.com
""",
    )

    write_file(
        DOCS / "LEVEL3_GATE.md",
        f"""# Level 3 Access Gate

## Rule
Before accessing Level 3, a user must request a password by emailing:
{LEVEL3_GATE_EMAIL}

## Verification Required
- Full name
- Phone number
- County/city
- How they want to help

## Implementation Notes
- Current implementation is informational (static).
- Future implementation can use Netlify Identity or a custom auth service.
""",
    )

def main() -> None:
    if not ROOT.exists():
        raise SystemExit(
            f"ERROR: Root path not found: {ROOT}\n"
            "Edit ROOT in scripts/scaffold_l2.py to match your local path."
        )

    create_lib()
    create_locale_layout()
    create_level2_routes()
    create_search_tag_l3_routes()
    create_ideas_routes()
    create_content_placeholders()
    create_docs()

    print("✅ Scaffold updated (Layout + .prose page shell).")
    print(f"Root: {ROOT}")
    print("Key routes:")
    print("  /en/l2  |  /es/l2")
    print("  /en/ideas  |  /en/ideas/submit")
    print("  /en/l3 (gated placeholder)")
    print("")
    print("NOTE: OVERWRITE=True in this run. Set it back to False after confirming.")

if __name__ == "__main__":
    main()
