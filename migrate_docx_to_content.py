import re
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple, List

# =========================
# CONFIG
# =========================
REPO_ROOT = Path(__file__).resolve().parent

SOURCE_DIRS = [
    REPO_ROOT / "01_Prototype_Content_Package_(v1)",
    REPO_ROOT / "03_Timeline_Prototype_Pages",
    REPO_ROOT / "04_Power_in_Arkansas",
    REPO_ROOT / "05_ Community_Impact",
    REPO_ROOT / "06_ Sources_&_Provenance",
    REPO_ROOT / "07_ The_Legislative_Process_in_Arkansas",
    REPO_ROOT / "08_Specs",
    REPO_ROOT / "02_HISTORICAL_SCOPE",
    REPO_ROOT / "00_PROJECT_CHARTER",
]

CONTENT_ROOT = REPO_ROOT / "content"
OVERWRITE_EXISTING_MD = False

# Prefer repo-local pandoc (no PATH required)
PANDOC_CANDIDATES = [
    REPO_ROOT / "tools" / "pandoc" / "pandoc.exe",
    *list((REPO_ROOT / "tools" / "pandoc").glob("**/pandoc.exe")),
    Path("pandoc"),  # PATH fallback
]

REPORT_PATH = REPO_ROOT / "data" / "logs" / "docx_migration_report.json"

# =========================
# HELPERS
# =========================

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[’']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "untitled"

def run_cmd_bytes(args: List[str]) -> Tuple[int, bytes, bytes]:
    """
    Run command capturing stdout/stderr as bytes to avoid Windows console decoding issues.
    """
    p = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout, p.stderr

def safe_decode(b: bytes) -> str:
    # Pandoc output is UTF-8; if not, replace invalid sequences safely
    return b.decode("utf-8", errors="replace")

def find_pandoc() -> Path | None:
    seen = set()
    for cand in PANDOC_CANDIDATES:
        s = str(cand)
        if s in seen:
            continue
        seen.add(s)

        if cand.name.lower() == "pandoc" and len(cand.parts) == 1:
            code, _, _ = run_cmd_bytes(["pandoc", "--version"])
            if code == 0:
                return Path("pandoc")
            continue

        if cand.exists() and cand.is_file():
            code, _, _ = run_cmd_bytes([str(cand), "--version"])
            if code == 0:
                return cand

    return None

def extract_title_from_docname(name: str) -> str:
    base = re.sub(r"\.docx$", "", name, flags=re.IGNORECASE)
    base = re.sub(r"\s*\(.*?\)\s*$", "", base).strip()
    base = base.lstrip("#").strip()
    return base or "Untitled"

def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return ""

def guess_description(markdown_text: str) -> str:
    for ln in markdown_text.splitlines():
        s = ln.strip()
        if not s:
            continue
        if s.startswith("---") or s.startswith("#"):
            continue
        if len(s) >= 40:
            return s[:200]
    return ""

def write_frontmatter(title: str, description: str, tags: List[str]) -> str:
    lines = ["---"]
    lines.append(f"title: {json.dumps(title)}")
    lines.append(f"description: {json.dumps(description)}")
    lines.append("tags:")
    if tags:
        for t in tags:
            lines.append(f"  - {t}")
    else:
        lines.append("  - migration:needs-tags")
    lines.append("---")
    return "\n".join(lines) + "\n\n"

def convert_docx_to_markdown(docx_path: Path, pandoc_path: Path | None) -> Tuple[str, str]:
    if pandoc_path is not None:
        args = [str(pandoc_path), str(docx_path), "-t", "gfm", "--wrap=none"]
        code, out_b, err_b = run_cmd_bytes(args)
        if code == 0:
            md = safe_decode(out_b).strip()
            return md + ("\n" if not md.endswith("\n") else ""), f"pandoc:{pandoc_path}"
        # If pandoc fails, fall back

    # Fallback conversion
    try:
        from docx import Document
        doc = Document(str(docx_path))
        lines = []
        for p in doc.paragraphs:
            txt = p.text.strip()
            if not txt:
                lines.append("")
                continue
            style_name = (p.style.name or "").lower() if p.style is not None else ""
            if "heading 1" in style_name:
                lines.append(f"# {txt}")
            elif "heading 2" in style_name:
                lines.append(f"## {txt}")
            elif "heading 3" in style_name:
                lines.append(f"### {txt}")
            else:
                lines.append(txt)
        md = "\n".join(lines).strip() + "\n"
        return md, "docx-text"
    except Exception:
        return "", "failed"

def route_destination(docx_path: Path) -> Tuple[Path, List[str]]:
    p = docx_path
    parent = p.parent.name
    fname = p.name

    if "Prototype_Content_Package" in str(p.parent):
        base = re.sub(r"\.md(\s*\(.*?\))?\.docx$", "", fname, flags=re.IGNORECASE)
        slug = slugify(base)
        dest = CONTENT_ROOT / "pages" / f"{slug}.md"
        return dest, ["migration:prototype", "section:pages"]

    if parent == "03_Timeline_Prototype_Pages":
        lower = fname.lower()
        if "timeline_eras" in lower:
            era_slug = slugify(re.sub(r"^timeline_eras_", "", re.sub(r"\.md\.docx$", "", fname, flags=re.I), flags=re.I))
            dest = CONTENT_ROOT / "timelines" / "eras" / f"{era_slug}.md"
            return dest, ["migration:prototype", "section:timeline", "type:era"]
        if "timeline_events" in lower:
            event_slug = slugify(re.sub(r"^timeline_events_", "", re.sub(r"\.md\.docx$", "", fname, flags=re.I), flags=re.I))
            dest = CONTENT_ROOT / "timelines" / "events" / f"{event_slug}.md"
            return dest, ["migration:prototype", "section:timeline", "type:event"]
        if "timeline_index" in lower:
            dest = CONTENT_ROOT / "timelines" / "index.md"
            return dest, ["migration:prototype", "section:timeline"]

    if parent == "04_Power_in_Arkansas":
        base = re.sub(r"\.md\.docx$", "", fname, flags=re.IGNORECASE)
        base = re.sub(r"^power_", "", base, flags=re.IGNORECASE)
        slug = slugify(base)
        dest = CONTENT_ROOT / "frameworks" / "power" / f"{slug}.md"
        return dest, ["migration:prototype", "section:power", "module:power"]

    if parent.strip() == "05_ Community_Impact":
        base = re.sub(r"\.md\.docx$", "", fname, flags=re.IGNORECASE)
        slug = slugify(base)
        dest = CONTENT_ROOT / "community-impact" / f"{slug}.md"
        return dest, ["migration:prototype", "section:community-impact"]

    if parent == "06_ Sources_&_Provenance":
        base = re.sub(r"\.md\.docx$", "", fname, flags=re.IGNORECASE)
        slug = slugify(base)
        dest = CONTENT_ROOT / "sources" / f"{slug}.md"
        return dest, ["migration:prototype", "section:sources"]

    if parent == "07_ The_Legislative_Process_in_Arkansas":
        base = re.sub(r"\.md\.docx$", "", fname, flags=re.IGNORECASE)
        slug = slugify(base)
        dest = CONTENT_ROOT / "legislative-process" / f"{slug}.md"
        return dest, ["migration:prototype", "section:legislative"]

    if parent == "02_HISTORICAL_SCOPE":
        title = extract_title_from_docname(fname)
        slug = slugify(title)
        dest = CONTENT_ROOT / "constitutions" / f"{slug}.md"
        return dest, ["migration:scope", "section:constitutions"]

    title = extract_title_from_docname(fname)
    slug = slugify(title)
    dest = CONTENT_ROOT / "pages" / "misc" / f"{slug}.md"
    return dest, ["migration:uncategorized"]

def main() -> None:
    ensure_dir(CONTENT_ROOT)
    ensure_dir(REPO_ROOT / "data" / "logs")

    pandoc_path = find_pandoc()
    print(f"[migrate] Repo root: {REPO_ROOT}")
    print(f"[migrate] Pandoc found: {pandoc_path if pandoc_path else 'NO'}")

    docx_files: List[Path] = []
    for d in SOURCE_DIRS:
        if d.exists():
            docx_files.extend(d.rglob("*.docx"))

    docx_files = sorted(set(docx_files))

    report = {
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "repoRoot": str(REPO_ROOT),
        "pandocFound": str(pandoc_path) if pandoc_path else "",
        "overwriteExistingMd": OVERWRITE_EXISTING_MD,
        "totalDocxFound": len(docx_files),
        "converted": [],
        "skipped": [],
        "failed": []
    }

    if not docx_files:
        print("[migrate] No .docx files found in configured source directories.")
        REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"[migrate] Wrote report: {REPORT_PATH}")
        return

    for docx_path in docx_files:
        if "node_modules" in str(docx_path):
            continue

        dest_path, base_tags = route_destination(docx_path)
        ensure_dir(dest_path.parent)

        if dest_path.exists() and not OVERWRITE_EXISTING_MD:
            report["skipped"].append({"source": str(docx_path), "dest": str(dest_path), "reason": "dest exists"})
            continue

        md_body, method = convert_docx_to_markdown(docx_path, pandoc_path)

        if not md_body.strip():
            report["failed"].append({"source": str(docx_path), "dest": str(dest_path), "method": method, "reason": "empty output"})
            continue

        fallback_title = extract_title_from_docname(docx_path.name)
        first_line = first_nonempty_line(md_body)
        inferred_title = first_line.lstrip("#").strip() if first_line.startswith("#") else fallback_title
        inferred_title = inferred_title or fallback_title

        description = guess_description(md_body)
        fm = write_frontmatter(inferred_title, description, base_tags)
        dest_path.write_text(fm + md_body, encoding="utf-8")

        report["converted"].append({"source": str(docx_path), "dest": str(dest_path), "method": method, "title": inferred_title})

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"[migrate] Converted: {len(report['converted'])}")
    print(f"[migrate] Skipped:   {len(report['skipped'])}")
    print(f"[migrate] Failed:    {len(report['failed'])}")
    print(f"[migrate] Report:    {REPORT_PATH}")
    print("[migrate] Done.")

if __name__ == "__main__":
    main()
