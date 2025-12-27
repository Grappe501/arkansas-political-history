#!/usr/bin/env python3
r"""
Remove scaffolded static topic route pages that override the dynamic route:

Deletes:
  src/routes/[locale]/l2/<section>/<topic>/

Keeps:
  src/routes/[locale]/l2/+page.svelte
  src/routes/[locale]/l2/<section>/+page.svelte

Run:
  cd C:\Users\User\Desktop\Arkansas_Political_History\site
  py scripts\remove_static_l2_topics.py --dry-run
  py scripts\remove_static_l2_topics.py --apply
"""

from __future__ import annotations
from pathlib import Path
import argparse
import shutil

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

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="SvelteKit app root (default: current dir).")
    ap.add_argument("--dry-run", action="store_true", help="Print what would be removed.")
    ap.add_argument("--apply", action="store_true", help="Actually delete folders.")
    args = ap.parse_args()

    if not args.dry_run and not args.apply:
        print("Choose one: --dry-run or --apply")
        return 2

    ROOT = Path(args.root).resolve()
    routes = ROOT / "src" / "routes" / "[locale]" / "l2"
    if not routes.exists():
        print(f"ERROR: missing {routes}")
        return 2

    targets: list[Path] = []
    for section, topics in LEVEL2_SECTIONS.items():
        for topic in topics:
            p = routes / section / topic
            if p.exists() and p.is_dir():
                # Only delete if it contains +page.svelte (real route folder)
                if (p / "+page.svelte").exists():
                    targets.append(p)

    if not targets:
        print("✅ No static topic route folders found. Nothing to remove.")
        return 0

    print(f"Found {len(targets)} static topic route folders that override /[section]/[topic]:\n")
    for t in targets:
        print(f"  - {t.relative_to(ROOT)}")

    if args.dry_run:
        print("\nDRY RUN: nothing removed.")
        return 0

    # Apply
    print("\nRemoving folders...")
    for t in targets:
        shutil.rmtree(t)
    print("✅ Removed static topic folders. Dynamic route can now take over.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
