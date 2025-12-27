#!/usr/bin/env python3
"""
Fix nav href links across Svelte files.

Usage:
  python fix_nav_links.py --root site/src --dry-run
  python fix_nav_links.py --root site/src
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple


# Add / remove mappings as needed.
# Keys are "wrong" hrefs, values are "correct" hrefs.
DEFAULT_HREF_MAP: Dict[str, str] = {
    # Start Here (common wrong variants)
    "/start-here": "/p/start-here",
    "/Start-Here": "/p/start-here",
    "/start_here": "/p/start-here",
    "/startHere": "/p/start-here",
    "/p/start_here": "/p/start-here",
    "/p/startHere": "/p/start-here",
    "/pages/start-here": "/p/start-here",
    "/page/start-here": "/p/start-here",
    "/content/pages/start-here": "/p/start-here",
    "/content/pages/start-here.md": "/p/start-here",

    # If you ever had this older pattern:
    "/p/start-here.md": "/p/start-here",

    # Keep these canonical (only rewrites if they’re wrong)
    "/Timeline": "/timeline",
    "/Power": "/power",
    "/Search": "/search",
}

# Also normalize any accidental double slashes like //p/start-here
DOUBLE_SLASH_RE = re.compile(r"^//+")

# Very targeted href matcher (won’t touch JS strings not in href="")
HREF_ATTR_RE = re.compile(
    r'''href\s*=\s*(?P<quote>["'])(?P<href>[^"']+)(?P=quote)''',
    re.IGNORECASE
)


def normalize_href(href: str) -> str:
    href = DOUBLE_SLASH_RE.sub("/", href)
    return href


def rewrite_hrefs(text: str, href_map: Dict[str, str]) -> Tuple[str, List[Tuple[str, str]]]:
    """
    Returns: (new_text, changes)
    changes is list of (old, new)
    """
    changes: List[Tuple[str, str]] = []

    def _sub(m: re.Match) -> str:
        q = m.group("quote")
        old_href = m.group("href")
        old_norm = normalize_href(old_href)

        new_href = None

        # direct mapping match
        if old_norm in href_map:
            new_href = href_map[old_norm]
        else:
            # extra: if someone wrote /p/start-here/ (trailing slash)
            if old_norm.rstrip("/") in href_map:
                new_href = href_map[old_norm.rstrip("/")]

        if new_href and new_href != old_href:
            changes.append((old_href, new_href))
            return f'href={q}{new_href}{q}'

        return m.group(0)

    new_text = HREF_ATTR_RE.sub(_sub, text)
    return new_text, changes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="site/src", help="Root folder to scan (default: site/src)")
    ap.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    ap.add_argument("--no-backup", action="store_true", help="Do not create .bak backups")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"[ERROR] Root not found: {root}")
        return 1

    href_map = dict(DEFAULT_HREF_MAP)

    svelte_files = sorted(root.rglob("*.svelte"))
    if not svelte_files:
        print(f"[WARN] No .svelte files found under: {root}")
        return 0

    touched = 0
    total_changes = 0

    for fp in svelte_files:
        original = fp.read_text(encoding="utf-8", errors="replace")
        updated, changes = rewrite_hrefs(original, href_map)

        if changes:
            touched += 1
            total_changes += len(changes)

            print(f"\n[FILE] {fp}")
            for old, new in changes:
                print(f"  - {old}  ->  {new}")

            if not args.dry_run:
                if not args.no_backup:
                    bak = fp.with_suffix(fp.suffix + ".bak")
                    bak.write_text(original, encoding="utf-8")
                fp.write_text(updated, encoding="utf-8")

    print("\n---")
    print(f"Scanned: {len(svelte_files)} files")
    print(f"Modified: {touched} files")
    print(f"Total href rewrites: {total_changes}")
    if args.dry_run:
        print("(dry-run: no files written)")
    else:
        print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
