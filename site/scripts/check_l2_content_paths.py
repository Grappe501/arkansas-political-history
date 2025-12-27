#!/usr/bin/env python3
r"""
Check Level 2 content path parity for Stand Up Arkansas dashboard.

What it checks:
  1) Expected content exists in:  content/{locale}/l2/{section}/{topic}.md
  2) Warns if markdown exists under src/content (common misplacement)
  3) Warns if static topic routes still exist and override /[section]/[topic]
  4) Optional --fix: creates missing placeholder markdown files

Run:
  cd C:\Users\User\Desktop\Arkansas_Political_History\site
  py scripts\check_l2_content_paths.py
  py scripts\check_l2_content_paths.py --fix
"""

from __future__ import annotations
from pathlib import Path
from datetime import date
import argparse
import sys

TODAY = date.today().isoformat()

# Keep this in sync with scaffold_l2.py
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

def md_placeholder(locale: str, section: str, topic: str) -> str:
    title = f"{section.title()} — {topic.title()}"
    description = f"Level 2 topic: {section}/{topic}."
    tags = [section, topic] if section != "about" else [topic]
    tags_yaml = "[" + ", ".join([f'"{t}"' for t in tags]) + "]"
    status = "ready" if locale == "en" else "translating"
    lead = "**ENGLISH PLACEHOLDER (authoritative for now).**" if locale == "en" else "**ESPAÑOL: En traducción.**"

    return f"""---
title: "{title}"
description: "{description}"
section: "{section}"
topic: "{topic}"
tags: {tags_yaml}
status: "{status}"
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

def find_markdown_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(root.rglob("*.md"))

def check_static_topic_routes(routes_root: Path) -> list[Path]:
    """
    Detects static routes like:
      src/routes/[locale]/l2/power/institutions/+page.svelte
    which override the dynamic:
      src/routes/[locale]/l2/[section]/[topic]/+page.svelte
    """
    if not routes_root.exists():
        return []
    offenders: list[Path] = []
    # any +page.svelte under l2/<section>/<topic>/ where <section> is not [section] and <topic> is not [topic]
    l2 = routes_root / "[locale]" / "l2"
    if not l2.exists():
        return []
    for section_dir in l2.iterdir():
        if not section_dir.is_dir():
            continue
        if section_dir.name.startswith("["):  # [section] dynamic
            continue
        for maybe_topic_dir in section_dir.iterdir():
            if not maybe_topic_dir.is_dir():
                continue
            if maybe_topic_dir.name.startswith("["):  # [topic] dynamic
                continue
            page = maybe_topic_dir / "+page.svelte"
            if page.exists():
                offenders.append(page)
    return offenders

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=".",
        help="Path to the SvelteKit app root (default: current directory).",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Create missing markdown placeholders in content/{locale}/l2/... for expected slugs.",
    )
    args = parser.parse_args()

    ROOT = Path(args.root).resolve()
    content_root = ROOT / "content"
    src_content_root = ROOT / "src" / "content"
    routes_root = ROOT / "src" / "routes"

    print(f"\n=== L2 Content Path Check ===")
    print(f"App root: {ROOT}")

    # 1) Basic structure checks
    if not (ROOT / "src").exists() or not routes_root.exists():
        print("ERROR: This does not look like a SvelteKit root (missing src/routes).")
        return 2

    if not content_root.exists():
        print(f"\nWARN: {content_root} does not exist yet.")
        if args.fix:
            content_root.mkdir(parents=True, exist_ok=True)
            print("  Created root content/ folder.")
        else:
            print("  Create it or run with --fix.")
    else:
        print(f"\nOK: Found content folder: {content_root}")

    # 2) Warn if src/content is being used accidentally
    src_md = find_markdown_files(src_content_root)
    if src_md:
        print(f"\nWARN: Found markdown under src/content ({len(src_md)} files).")
        print("  Your dynamic loader expects /content/... at project root, not /src/content/.\n"
              "  If these are meant for Level 2, move them to: content/{locale}/l2/{section}/{topic}.md")
        # show up to 10 examples
        for p in src_md[:10]:
            print(f"  - {p.relative_to(ROOT)}")
        if len(src_md) > 10:
            print(f"  ... +{len(src_md) - 10} more")
    else:
        if src_content_root.exists():
            print("\nOK: src/content exists but contains no .md files (fine).")
        else:
            print("\nOK: No src/content folder detected (also fine).")

    # 3) Check expected L2 files
    missing: list[Path] = []
    present: list[Path] = []

    for locale in LOCALES:
        for section, topics in LEVEL2_SECTIONS.items():
            for topic in topics:
                p = content_root / locale / "l2" / section / f"{topic}.md"
                if p.exists():
                    present.append(p)
                else:
                    missing.append(p)

    print(f"\nExpected L2 markdown files: {len(present) + len(missing)}")
    print(f"Present: {len(present)}")
    print(f"Missing: {len(missing)}")

    if missing:
        print("\nMissing files (first 20):")
        for p in missing[:20]:
            print(f"  - {p.relative_to(ROOT)}")
        if len(missing) > 20:
            print(f"  ... +{len(missing) - 20} more")

        if args.fix:
            print("\n--fix enabled: creating placeholders for missing files...")
            for p in missing:
                p.parent.mkdir(parents=True, exist_ok=True)
                locale = p.parts[p.parts.index("content") + 1]  # crude but reliable in this structure
                section = p.parts[p.parts.index("l2") + 1]
                topic = p.stem
                p.write_text(md_placeholder(locale, section, topic), encoding="utf-8")
            print("✅ Placeholders created.")
    else:
        print("\n✅ All expected L2 markdown paths exist.")

    # 4) Check for static topic routes that override dynamic [section]/[topic]
    offenders = check_static_topic_routes(routes_root)
    if offenders:
        print(f"\nWARN: Found static topic route pages that will override your dynamic route:")
        print("  You should delete these folders: src/routes/[locale]/l2/<section>/<topic>/")
        print("  Keep section landing pages: src/routes/[locale]/l2/<section>/+page.svelte")
        for p in offenders[:20]:
            print(f"  - {p.relative_to(ROOT)}")
        if len(offenders) > 20:
            print(f"  ... +{len(offenders) - 20} more")
    else:
        print("\nOK: No overriding static topic pages detected under src/routes/[locale]/l2/<section>/<topic>/")

    print("\n=== Done ===\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
