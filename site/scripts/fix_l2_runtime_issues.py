#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re
import argparse
import shutil

def patch_locale_links(file_path: Path, dry_run: bool) -> bool:
    txt = file_path.read_text(encoding="utf-8")

    # If already fixed (uses locale variable), skip
    if "href={`/${locale}/" in txt or "href={\`/${locale}/" in txt:
        return False

    changed = False

    # Ensure we have locale reactive var
    if "import { page } from '$app/stores';" in txt and "locale =" not in txt:
        # insert $: locale = $page.params.locale;
        txt2 = re.sub(
            r"(import\s+\{\s*page\s*\}\s+from\s+'\$app/stores';\s*)",
            r"\1\n  $: locale = $page.params.locale;\n",
            txt,
            count=1,
        )
        if txt2 != txt:
            txt = txt2
            changed = True

    # Replace href="/{$page.params.locale}/..."
    def repl(m):
        rest = m.group(1)
        return f'href={{`/${{locale}}/{rest}`}}'

    txt2 = re.sub(r'href="/\{\$page\.params\.locale\}/([^"]+)"', repl, txt)
    if txt2 != txt:
        txt = txt2
        changed = True

    if changed and not dry_run:
        file_path.write_text(txt, encoding="utf-8")

    return changed

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="site root (default: current directory)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ROOT = Path(args.root).resolve()
    routes = ROOT / "src" / "routes" / "[locale]" / "l2"

    if not routes.exists():
        print(f"ERROR: cannot find {routes}")
        return 2

    # 1) Fix $page usage in markup for L2 home + section pages
    targets = [routes / "+page.svelte"]
    for p in routes.glob("*"):
        if p.is_dir() and not p.name.startswith("["):
            f = p / "+page.svelte"
            if f.exists():
                targets.append(f)

    print(f"Scanning {len(targets)} L2 pages for old $page href patterns...")

    changed_files = []
    for f in targets:
        if f.exists():
            if patch_locale_links(f, args.dry_run):
                changed_files.append(f)

    if changed_files:
        print("\nPatched files:")
        for f in changed_files:
            print(f"  - {f.relative_to(ROOT)}")
        if args.dry_run:
            print("\nDRY RUN: no files written.")
        else:
            print("\n✅ Changes written.")
    else:
        print("✅ No href patches needed.")

    # 2) Remove +page.server.ts if present
    bad_server = ROOT / "src" / "routes" / "[locale]" / "l2" / "[section]" / "[topic]" / "+page.server.ts"
    if bad_server.exists():
        print(f"\nFound non-serializable loader file: {bad_server.relative_to(ROOT)}")
        if args.dry_run:
            print("DRY RUN: would delete it.")
        else:
            bad_server.unlink()
            print("✅ Deleted +page.server.ts (required).")
    else:
        print("\nOK: no +page.server.ts in topic route.")

    # 3) Warn if nested site/site/src/content exists
    nested = ROOT / "site" / "src" / "content"
    if nested.exists():
        print(f"\nWARN: nested folder exists: {nested.relative_to(ROOT)}")
        print("  Your sync-content.mjs is likely copying into site/site/src/content (wrong).")
        print("  Fix scripts/sync-content.mjs destination to ROOT/src/content.")
    else:
        print("\nOK: no nested site/site/src/content detected.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
