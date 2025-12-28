#!/usr/bin/env python3
r"""
Map the /content folder for Arkansas_Political_History.

Outputs:
  - content_map.json : full structured inventory + recommendations
  - content_map.csv  : spreadsheet-friendly inventory
  - content_map.md   : readable grouped report + "fit into system" notes
  - content_graph.json : internal link graph + inbound links (cross-link planning)
  - content_graph.md   : readable link graph highlights + orphan list
  - content_framework_suggestions.json : suggested framework/constitution cross-links (best-effort)

Usage (Windows PowerShell):
  python .\map_content.py --root "C:\Users\User\Desktop\Arkansas_Political_History\content" --out "C:\Users\User\Desktop\Arkansas_Political_History\content"

Notes:
  - This script uses a small custom frontmatter parser (no dependencies).
  - It is tolerant of Windows encodings and weird characters.
  - It will never crash on a single bad file: errors are logged and the scan continues.

If --root is omitted, it assumes the current working directory is the /content folder.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ----------------------------
# Helpers: minimal YAML frontmatter parsing (no dependencies)
# ----------------------------

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)

IGNORE_DIRS = {
    ".git", ".svelte-kit", "node_modules", "dist", "build", ".next", ".vercel",
    ".idea", ".vscode", "__pycache__", ".cache", ".turbo", ".output",
}

TEXT_EXTS = {".md", ".mdx", ".txt", ".yaml", ".yml", ".json", ".toml"}


def safe_read_text(path: Path) -> str:
    """
    Read text safely across Windows encodings.
    """
    for enc in ("utf-8", "utf-8-sig", "cp1252"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
        except Exception:
            break
    return path.read_text(encoding="utf-8", errors="replace")


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """
    Returns: (frontmatter_dict, body_text)

    Minimal YAML-ish frontmatter parser that handles:
      - key: value
      - key:
          - item
          - item
      - simple nested dicts one level deep:
          learning:
            mode: analysis
            estimatedMinutes: 10

    It does NOT fully implement YAML. It's designed to be dependency-free and robust.
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text

    raw = m.group(1)
    body = text[m.end():]

    fm: Dict[str, Any] = {}
    lines = raw.splitlines()

    def parse_scalar(v: str) -> Any:
        v = v.strip().strip('"').strip("'")
        if v.lower() in {"true", "false"}:
            return v.lower() == "true"
        try:
            return int(v)
        except ValueError:
            return v

    current_key: Optional[str] = None
    current_parent: Optional[str] = None

    for line in lines:
        if not line.strip():
            continue

        # list item
        if line.lstrip().startswith("- "):
            item = line.strip()[2:].strip().strip('"').strip("'")
            if current_key is not None:
                # handle either top-level list or nested list
                if current_parent:
                    fm.setdefault(current_parent, {})
                    fm[current_parent].setdefault(current_key, [])
                    if isinstance(fm[current_parent][current_key], list):
                        fm[current_parent][current_key].append(item)
                else:
                    fm.setdefault(current_key, [])
                    if isinstance(fm[current_key], list):
                        fm[current_key].append(item)
            continue

        # nested mapping "  child: value"
        if line.startswith("  ") and ":" in line:
            if current_parent is None:
                # If we see indentation but no parent, ignore safely
                continue
            k, v = line.strip().split(":", 1)
            k = k.strip()
            v = v.strip()
            fm.setdefault(current_parent, {})
            if v == "":
                # start of nested list or nested dict placeholder
                fm[current_parent].setdefault(k, [])
                current_key = k
            else:
                fm[current_parent][k] = parse_scalar(v)
                current_key = k
            continue

        # top-level key: value
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()

            # parent dict start: "learning:"
            if v == "":
                fm.setdefault(k, {})
                current_parent = k
                current_key = None
                continue

            fm[k] = parse_scalar(v)
            current_parent = None
            current_key = k
            continue

    # normalize tags into list
    if "tags" in fm and isinstance(fm["tags"], str):
        fm["tags"] = [fm["tags"]]

    return fm, body


def extract_headings(body: str) -> List[Dict[str, Any]]:
    headings: List[Dict[str, Any]] = []
    for m in HEADING_RE.finditer(body):
        level = len(m.group(1))
        title = m.group(2).strip()
        headings.append({"level": level, "title": title})
    return headings


def extract_links(body: str) -> List[Dict[str, str]]:
    links: List[Dict[str, str]] = []
    for m in MD_LINK_RE.finditer(body):
        text = m.group(1).strip()
        href = m.group(2).strip()
        links.append({"text": text, "href": href})
    return links


def first_nonempty_paragraph(body: str, max_chars: int = 320) -> str:
    cleaned = re.sub(r"^#{1,6}\s+.*$", "", body, flags=re.MULTILINE)
    cleaned = re.sub(r"^---\s*$", "", cleaned, flags=re.MULTILINE)
    cleaned = cleaned.strip()
    parts = re.split(r"\n\s*\n", cleaned)
    for p in parts:
        p = p.strip()
        if not p:
            continue
        p = re.sub(r"\s+", " ", p)
        return (p[:max_chars] + "…") if len(p) > max_chars else p
    return ""


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTS


def walk_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            if is_text_file(p):
                files.append(p)
    return files


# ----------------------------
# Data model
# ----------------------------

@dataclass
class FileRecord:
    rel_path: str
    abs_path: str
    ext: str
    size_bytes: int
    modified: str

    title: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    section: str = ""
    type: str = ""
    contentType: str = ""
    status: str = ""

    headings: List[Dict[str, Any]] = field(default_factory=list)
    preview: str = ""
    links_out: List[Dict[str, str]] = field(default_factory=list)

    inferred_slug: str = ""
    recommended_bucket: str = ""
    notes: List[str] = field(default_factory=list)

    # derived fields for system mapping
    internal_links: List[str] = field(default_factory=list)
    outbound_external_links: List[str] = field(default_factory=list)


# ----------------------------
# System mapping logic
# ----------------------------

def recommend_bucket(rel_path: str, fm: Dict[str, Any]) -> Tuple[str, List[str]]:
    """
    Suggest where the page "fits" in the system.
    """
    notes: List[str] = []

    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]

    section = str(fm.get("section") or "").strip()
    ctype = str(fm.get("contentType") or "").strip()
    ptype = str(fm.get("type") or "").strip()

    rp = rel_path.replace("\\", "/").lower()

    # Frameworks
    if "/framework" in rp or "/frameworks/" in rp or section.lower() == "frameworks" or "module:frameworks" in tags:
        return "Frameworks", notes

    # Constitutions / Eras
    if section.lower() == "constitutions" or "section:constitutions" in tags:
        if ptype.lower() == "era":
            return "Constitutions / Eras", notes
        if ptype.lower() == "constitution":
            return "Constitutions / Documents", notes
        notes.append("Has constitutions section/tag but missing type: Constitution/Era")
        return "Constitutions / Needs Typing", notes

    # Territorial / pre-state roots
    territorial_markers = (
        "territorial", "territory", "territories",
        "territorial governance", "organic act",
        "louisiana territory", "missouri territory", "arkansas territory",
    )
    if any(t in rp for t in territorial_markers):
        return "Territorial Roots (Pre-1836)", notes

    title = str(fm.get("title") or "")
    body_hint = (title + " " + section + " " + ctype).lower()
    if any(t in body_hint for t in ("territor", "organic act", "territory")):
        return "Territorial Roots (Pre-1836)", notes

    # Specs / build docs
    if rp.endswith(".md") and any(k in rp for k in ("spec", "standards", "build", "routing", "netlify", "adapter")):
        return "Specs / Build Docs", notes

    # Explainers / process
    if any(k in rp for k in ("process", "how-", "explainer")) or "legislative process" in body_hint or ctype.lower() in {"explainer", "guide"}:
        return "Explainers / Process", notes

    return "Uncategorized / Review", notes


def normalize_internal_link(href: str, from_rel: str) -> Optional[str]:
    """
    Normalize internal links to a stable comparable string (project-relative-ish).
    We don't know your final router here, so we:
      - keep absolute site links starting with /
      - resolve ./ and ../ relative to the file's folder
      - ignore anchors and query strings
    """
    if not href:
        return None

    href = href.strip()

    # ignore mailto, http(s), etc.
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", href):
        return None

    # strip query/fragment
    href = href.split("#", 1)[0].split("?", 1)[0].strip()
    if not href:
        return None

    if href.startswith("/"):
        return href

    # relative link
    base_dir = Path(from_rel).parent
    try:
        resolved = (base_dir / href).as_posix()
        # keep as relative-to-content style path
        return resolved
    except Exception:
        return href


def extract_link_targets(links: List[Dict[str, str]], from_rel: str) -> Tuple[List[str], List[str]]:
    internal: List[str] = []
    external: List[str] = []
    for l in links or []:
        href = (l.get("href") or "").strip()
        if not href:
            continue
        if re.match(r"^https?://", href, flags=re.IGNORECASE):
            external.append(href)
            continue

        norm = normalize_internal_link(href, from_rel)
        if norm:
            internal.append(norm)
    # de-dupe, preserve order
    def dedupe(seq: List[str]) -> List[str]:
        seen = set()
        out = []
        for x in seq:
            if x in seen:
                continue
            seen.add(x)
            out.append(x)
        return out

    return dedupe(internal), dedupe(external)


def search_territorial_candidates(records: List[FileRecord]) -> List[FileRecord]:
    keys = [
        "territorial", "territory", "territories",
        "governance", "organic act", "territorial government",
        "arkansas territory", "louisiana territory", "missouri territory",
    ]
    scored: List[Tuple[int, FileRecord]] = []
    for r in records:
        hay = f"{r.rel_path}\n{r.title}\n{r.preview}".lower()
        score = sum(1 for k in keys if k in hay)
        if score > 0:
            scored.append((score, r))
    scored.sort(key=lambda x: (-x[0], x[1].rel_path))
    return [r for _, r in scored]


def suggest_framework_mentions(records: List[FileRecord]) -> Dict[str, Any]:
    """
    Best-effort: identify likely framework pages and look for their slug/title mentions in constitutions.
    Produces suggestions, not authoritative truth.
    """
    frameworks: List[Tuple[str, str]] = []  # (slug, title)
    constitutions: List[FileRecord] = []

    for r in records:
        if r.recommended_bucket == "Frameworks":
            slug = r.inferred_slug or slugify(Path(r.rel_path).stem)
            frameworks.append((slug, r.title or Path(r.rel_path).stem))
        if r.recommended_bucket.startswith("Constitutions /"):
            constitutions.append(r)

    suggestions: Dict[str, Any] = {}
    for c in constitutions:
        text_blob = (c.title + "\n" + c.preview + "\n" + " ".join(h["title"] for h in c.headings)).lower()
        hits = []
        for slug, title in frameworks:
            if not title:
                continue
            # match on title words or slug-ish name
            if title.lower() in text_blob or slug.replace("-", " ") in text_blob:
                hits.append({"framework_slug": slug, "framework_title": title})
        if hits:
            suggestions[c.rel_path] = hits

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "note": "These are heuristic mentions found in titles/headings/preview; use as cross-link planning hints.",
        "suggestions": suggestions,
    }


def build_graph(records: List[FileRecord]) -> Dict[str, Any]:
    """
    Build internal link graph and compute inbound links, orphans, etc.
    """
    nodes = {r.rel_path: r for r in records}
    inbound: Dict[str, List[str]] = {r.rel_path: [] for r in records}

    # Attempt to resolve internal links that are relative file paths to actual files.
    rel_set = set(nodes.keys())
    alt_index = {("/" + k): k for k in rel_set}  # if someone links to /path, map to rel_path

    edges: List[Dict[str, str]] = []

    for r in records:
        for target in r.internal_links:
            to_rel: Optional[str] = None

            # direct match on rel_path
            if target in rel_set:
                to_rel = target
            # match on /rel_path
            elif target in alt_index:
                to_rel = alt_index[target]
            # match on same without leading ./ (common)
            else:
                t2 = target.lstrip("./")
                if t2 in rel_set:
                    to_rel = t2
                elif ("/" + t2) in alt_index:
                    to_rel = alt_index["/" + t2]

            if to_rel:
                edges.append({"from": r.rel_path, "to": to_rel})
                inbound[to_rel].append(r.rel_path)
            else:
                # keep unresolved edges in graph for review
                edges.append({"from": r.rel_path, "to": target})

    # Orphans: no inbound links (excluding obvious indexes)
    orphans: List[str] = []
    for rp, ins in inbound.items():
        if ins:
            continue
        name = rp.lower()
        if name.endswith("index.md") or name.endswith("readme.md"):
            continue
        orphans.append(rp)
    orphans.sort(key=str.lower)

    # Top hubs by outbound count (resolved+unresolved internal)
    hubs = sorted(
        ((r.rel_path, len(r.internal_links)) for r in records),
        key=lambda x: (-x[1], x[0].lower()),
    )[:25]

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "nodes": {
            r.rel_path: {
                "title": r.title,
                "bucket": r.recommended_bucket,
                "section": r.section,
                "type": r.type,
                "contentType": r.contentType,
                "status": r.status,
                "internal_out": r.internal_links,
                "external_out": r.outbound_external_links,
            }
            for r in records
        },
        "edges": edges,
        "inbound": inbound,
        "orphans": orphans,
        "top_outbound_hubs": [{"rel_path": rp, "internal_out_count": c} for rp, c in hubs],
    }


def build_report(records: List[FileRecord]) -> Dict[str, Any]:
    by_bucket: Dict[str, List[FileRecord]] = {}
    for r in records:
        by_bucket.setdefault(r.recommended_bucket, []).append(r)

    for b in by_bucket:
        by_bucket[b].sort(key=lambda x: x.rel_path.lower())

    territorial = search_territorial_candidates(records)

    internal_link_counts: Dict[str, int] = {}
    external_link_counts: Dict[str, int] = {}
    for r in records:
        internal_link_counts[r.rel_path] = len(r.internal_links or [])
        external_link_counts[r.rel_path] = len(r.outbound_external_links or [])

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "totals": {
            "files_scanned": len(records),
            "buckets": {k: len(v) for k, v in sorted(by_bucket.items(), key=lambda kv: kv[0].lower())},
        },
        "territorial_candidates": [asdict(r) for r in territorial[:25]],
        "link_metrics": {
            "internal_link_counts": internal_link_counts,
            "external_link_counts": external_link_counts,
        },
        "buckets": {k: [asdict(r) for r in v] for k, v in by_bucket.items()},
    }


def write_markdown_report(root: Path, report: Dict[str, Any], graph: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Content Map Report")
    lines.append("")
    lines.append(f"- Generated: {report['generated_at']}")
    lines.append(f"- Root: `{root}`")
    lines.append(f"- Files scanned: **{report['totals']['files_scanned']}**")
    lines.append("")

    lines.append("## Buckets")
    for bucket, count in report["totals"]["buckets"].items():
        lines.append(f"- **{bucket}**: {count}")
    lines.append("")

    lines.append("## Territorial Governance Candidates (Top Matches)")
    if report["territorial_candidates"]:
        for r in report["territorial_candidates"]:
            lines.append(f"- `{r['rel_path']}` — **{(r.get('title') or '').strip() or '(no title)'}**")
    else:
        lines.append("- None detected. (If you have one, it may not contain obvious keywords.)")
    lines.append("")

    lines.append("## Link Health Highlights")
    lines.append("")
    lines.append("### Orphan Pages (No Inbound Internal Links)")
    if graph.get("orphans"):
        for rp in graph["orphans"][:50]:
            lines.append(f"- `{rp}`")
        if len(graph["orphans"]) > 50:
            lines.append(f"- …and {len(graph['orphans']) - 50} more")
    else:
        lines.append("- None detected.")
    lines.append("")

    lines.append("### Top Internal Link Hubs")
    for item in graph.get("top_outbound_hubs", []):
        lines.append(f"- `{item['rel_path']}` — {item['internal_out_count']} internal links out")
    lines.append("")

    lines.append("## Inventory by Bucket")
    for bucket in sorted(report["buckets"].keys(), key=str.lower):
        lines.append("")
        lines.append(f"### {bucket}")
        for r in report["buckets"][bucket]:
            title = (r.get("title") or "").strip() or "(no title)"
            sec = (r.get("section") or "").strip()
            ptype = (r.get("type") or "").strip()
            ctype = (r.get("contentType") or "").strip()
            status = (r.get("status") or "").strip()
            notes = r.get("notes") or []
            note_txt = f"  Notes: {', '.join(notes)}" if notes else ""
            lines.append(
                f"- `{r['rel_path']}` — **{title}**"
                f"{' | section=' + sec if sec else ''}"
                f"{' | type=' + ptype if ptype else ''}"
                f"{' | contentType=' + ctype if ctype else ''}"
                f"{' | status=' + status if status else ''}"
                f"{note_txt}"
            )
    lines.append("")

    lines.append("## System Fit Recommendations (Auto-Generated)")
    lines.append("")
    lines.append("These are mechanical suggestions based on frontmatter and path patterns:")
    lines.append("")
    lines.append("- Anything tagged `section:constitutions` should include `type: Constitution` or `type: Era`.")
    lines.append("- Framework pages should eventually expose a stable slug (title → slug) to support reverse linking.")
    lines.append("- Territorial pages should be grouped as a pre-1836 root layer feeding into 1836.")
    lines.append("- Pages with no inbound links should either be linked from an index or intentionally isolated.")
    lines.append("")
    lines.append("Next step after this report:")
    lines.append("- Identify the canonical Territorial governance page(s) and link them into the Constitution timeline.")
    lines.append("- Add standardized `frameworks:` and `lenses:` structures to constitution frontmatter for toggles.")
    lines.append("- Generate/maintain indices (constitutions index, frameworks index, eras index) from this scan.")
    lines.append("")

    return "\n".join(lines)


def write_graph_markdown(graph: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Content Link Graph")
    lines.append("")
    lines.append(f"- Generated: {graph.get('generated_at')}")
    lines.append("")

    lines.append("## Orphans (No Inbound Links)")
    for rp in graph.get("orphans", []):
        lines.append(f"- `{rp}`")
    lines.append("")

    lines.append("## Inbound Links (Top 50 by count)")
    inbound = graph.get("inbound", {}) or {}
    ranked = sorted(((k, len(v)) for k, v in inbound.items()), key=lambda x: (-x[1], x[0].lower()))[:50]
    for rp, n in ranked:
        lines.append(f"- `{rp}` — {n} inbound links")
    lines.append("")

    lines.append("## Edges (first 200)")
    for e in (graph.get("edges") or [])[:200]:
        lines.append(f"- `{e['from']}` → `{e['to']}`")
    if len(graph.get("edges") or []) > 200:
        lines.append(f"- …and {len(graph['edges']) - 200} more")
    lines.append("")
    return "\n".join(lines)


def ensure_out_dir(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--root",
        type=str,
        default=".",
        help="Root folder to scan (should be the /content folder).",
    )
    ap.add_argument(
        "--out",
        type=str,
        default=".",
        help="Output folder for reports (default: current directory).",
    )
    ap.add_argument(
        "--include-binary",
        action="store_true",
        help="Also list non-text files in JSON inventory (no parsing).",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    out_dir = Path(args.out).resolve()
    ensure_out_dir(out_dir)

    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Root folder not found or not a directory: {root}")

    # Collect files
    text_files = walk_files(root)
    errors: List[Dict[str, str]] = []
    records: List[FileRecord] = []

    for p in sorted(text_files, key=lambda x: str(x).lower()):
        try:
            rel = str(p.relative_to(root)).replace("\\", "/")
            st = p.stat()
            text = safe_read_text(p)

            fm, body = parse_frontmatter(text)
            headings = extract_headings(body)
            links = extract_links(body)
            preview = first_nonempty_paragraph(body)

            title = str(fm.get("title") or "").strip()
            desc = str(fm.get("description") or "").strip()

            tags = fm.get("tags") or []
            if isinstance(tags, str):
                tags = [tags]
            if tags is None:
                tags = []

            section = str(fm.get("section") or "").strip()
            ptype = str(fm.get("type") or "").strip()
            ctype = str(fm.get("contentType") or "").strip()
            status = str(fm.get("status") or "").strip()

            bucket, notes = recommend_bucket(rel, fm)

            inferred_slug = slugify(title) if title else slugify(Path(rel).stem)

            internal_links, external_links = extract_link_targets(links, rel)

            records.append(
                FileRecord(
                    rel_path=rel,
                    abs_path=str(p),
                    ext=p.suffix.lower(),
                    size_bytes=st.st_size,
                    modified=datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
                    title=title,
                    description=desc,
                    tags=list(tags) if isinstance(tags, list) else [],
                    section=section,
                    type=ptype,
                    contentType=ctype,
                    status=status,
                    headings=headings,
                    preview=preview,
                    links_out=links,
                    inferred_slug=inferred_slug,
                    recommended_bucket=bucket,
                    notes=notes,
                    internal_links=internal_links,
                    outbound_external_links=external_links,
                )
            )
        except Exception as e:
            errors.append({"file": str(p), "error": repr(e)})

    report = build_report(records)
    graph = build_graph(records)
    framework_suggestions = suggest_framework_mentions(records)

    # Write JSON report
    json_path = out_dir / "content_map.json"
    json_path.write_text(
        json.dumps(
            {
                **report,
                "errors": errors,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # Write CSV inventory
    csv_path = out_dir / "content_map.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "rel_path",
                "title",
                "section",
                "type",
                "contentType",
                "status",
                "tags",
                "recommended_bucket",
                "inferred_slug",
                "modified",
                "size_bytes",
                "internal_out_count",
                "external_out_count",
                "preview",
            ]
        )
        for r in records:
            w.writerow(
                [
                    r.rel_path,
                    r.title,
                    r.section,
                    r.type,
                    r.contentType,
                    r.status,
                    ";".join(r.tags or []),
                    r.recommended_bucket,
                    r.inferred_slug,
                    r.modified,
                    r.size_bytes,
                    len(r.internal_links or []),
                    len(r.outbound_external_links or []),
                    r.preview,
                ]
            )

    # Write Markdown reports
    md_path = out_dir / "content_map.md"
    md_path.write_text(write_markdown_report(root, report, graph), encoding="utf-8")

    graph_json_path = out_dir / "content_graph.json"
    graph_json_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")

    graph_md_path = out_dir / "content_graph.md"
    graph_md_path.write_text(write_graph_markdown(graph), encoding="utf-8")

    framework_suggestions_path = out_dir / "content_framework_suggestions.json"
    framework_suggestions_path.write_text(
        json.dumps(framework_suggestions, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Console output
    print("Done.")
    print(f"- JSON: {json_path}")
    print(f"- CSV:  {csv_path}")
    print(f"- MD:   {md_path}")
    print(f"- Graph JSON: {graph_json_path}")
    print(f"- Graph MD:   {graph_md_path}")
    print(f"- Framework Suggestions JSON: {framework_suggestions_path}")

    if errors:
        print("")
        print(f"Warnings: {len(errors)} file(s) could not be parsed. See content_map.json -> errors[]")
        # Print first few errors for convenience
        for item in errors[:10]:
            print(f"- {item['file']}: {item['error']}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
