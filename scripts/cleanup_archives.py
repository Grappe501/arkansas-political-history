#!/usr/bin/env python3
"""
cleanup_archives.py

Deletes archive files (zip/7z/rar) that are not needed to run the project.
Designed for "repo hygiene" before sharing with developers.

Defaults:
- Recursively scans from repo root (current working directory)
- Deletes *.zip, *.7z, *.rar
- Skips protected directories (e.g., .git, node_modules, site/.svelte-kit)
- Supports dry-run (default) and apply mode

Usage:
  python scripts/cleanup_archives.py --dry-run
  python scripts/cleanup_archives.py --apply

Optional:
  python scripts/cleanup_archives.py --apply --extensions .zip
  python scripts/cleanup_archives.py --apply --protect releases backups
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

DEFAULT_EXTS = [".zip", ".7z", ".rar"]

DEFAULT_PROTECT_DIRS = {
    ".git",
    "node_modules",
    ".svelte-kit",
    "dist",
    "build",
    ".netlify",
}

def is_under_dir(path: Path, dirname: str) -> bool:
    parts = {p.lower() for p in path.parts}
    return dirname.lower() in parts

def main() -> int:
    parser = argparse.ArgumentParser(description="Delete archive files from the repo (zip/7z/rar).")
    parser.add_argument("--apply", action="store_true", help="Actually delete files.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be deleted (default).")
    parser.add_argument(
        "--extensions",
        nargs="*",
        default=DEFAULT_EXTS,
        help=f"Extensions to delete (default: {DEFAULT_EXTS})",
    )
    parser.add_argument(
        "--protect",
        nargs="*",
        default=[],
        help="Extra directory names to protect/skip (e.g., releases backups).",
    )

    args = parser.parse_args()

    repo_root = Path.cwd().resolve()
    exts = {e.lower() if e.startswith(".") else f".{e.lower()}" for e in args.extensions}
    protect_dirs = set(DEFAULT_PROTECT_DIRS) | {p.strip() for p in args.protect if p.strip()}

    # default behavior: dry-run unless --apply
    do_apply = bool(args.apply)
    if not args.apply and not args.dry_run:
        # if neither specified, default to dry-run
        pass

    candidates: list[Path] = []

    for p in repo_root.rglob("*"):
        if not p.is_file():
            continue

        # skip protected dirs anywhere in the path
        if any(is_under_dir(p, d) for d in protect_dirs):
            continue

        if p.suffix.lower() in exts:
            candidates.append(p)

    if not candidates:
        print(f"No archives found with extensions {sorted(exts)} under {repo_root}")
        return 0

    print(f"Found {len(candidates)} archive(s):")
    for f in candidates:
        rel = f.relative_to(repo_root)
        size = f.stat().st_size
        print(f"  - {rel} ({size} bytes)")

    if not do_apply:
        print("\nDry run only. Re-run with --apply to delete.")
        return 0

    print("\nDeleting...")
    deleted = 0
    for f in candidates:
        try:
            f.unlink()
            deleted += 1
            print(f"  deleted: {f.relative_to(repo_root)}")
        except Exception as e:
            print(f"  FAILED: {f.relative_to(repo_root)} -> {e}")

    print(f"\nDone. Deleted {deleted}/{len(candidates)} file(s).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
