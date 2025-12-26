from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class Finding:
    file: str
    reasons: List[str]
    moved_to: str | None = None


def repo_root_from_script_location() -> Path:
    return Path(__file__).resolve().parent


def read_text_best_effort(p: Path) -> str:
    # Robust reading: try utf-8 first, then fall back to cp1252 to avoid crashing
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="cp1252", errors="replace")


def ensure_parent_dir(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_reason_patterns() -> List[Tuple[str, re.Pattern]]:
    """
    These patterns are intentionally conservative: they flag content that frequently breaks mdsvex
    or indicates DOCX/HTML export soup.
    """
    patterns: List[Tuple[str, re.Pattern]] = [
        # Unicode smart quotes (should be normalized, but if present in raw markdown it’s a red flag)
        ("unicode_smart_quotes", re.compile(r"[\u2018\u2019\u201C\u201D]")),

        # CP1252 control characters that sometimes leak as U+0080..U+009F
        ("cp1252_control_chars", re.compile(r"[\u0080-\u009F]")),

        # HTML soup typical from DOCX conversion
        ("html_paragraph_tags", re.compile(r"</?p\b", re.IGNORECASE)),
        ("html_span_token", re.compile(r"<span\b[^>]*class=[\"']token[\"'][^>]*>", re.IGNORECASE)),

        # Mangled brace entities (common when code blocks got HTML-escaped)
        ("html_entity_braces", re.compile(r"&#123;|&#125;")),

        # mdsvex/Svelte breaker artifact patterns like {’}’} or {“} etc.
        ("brace_quote_artifacts", re.compile(r"\{\s*[’“”‘']\s*\}|\{[’“”‘']\}|\{[’“”‘'][^}]*\}")),
    ]
    return patterns


def find_reasons(text: str, patterns: List[Tuple[str, re.Pattern]]) -> List[str]:
    reasons: List[str] = []
    for name, pat in patterns:
        if pat.search(text):
            reasons.append(name)
    return reasons


def is_markdown_file(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() == ".md"


def relative_to_content(content_root: Path, p: Path) -> Path:
    return p.resolve().relative_to(content_root.resolve())


def quarantine_file(content_root: Path, quarantine_root: Path, file_path: Path) -> Path:
    rel = relative_to_content(content_root, file_path)
    dest = quarantine_root / rel
    ensure_parent_dir(dest)
    # Move the file; preserve metadata where possible
    shutil.move(str(file_path), str(dest))
    return dest


def main() -> None:
    root = repo_root_from_script_location()
    content_root = root / "content"
    quarantine_root = content_root / "_quarantine"

    if not content_root.exists():
        raise SystemExit(f"[quarantine] No ./content folder found at: {content_root}")

    patterns = make_reason_patterns()

    findings: List[Finding] = []
    scanned = 0
    moved = 0

    # Walk content tree but skip _quarantine itself
    for dirpath, dirnames, filenames in os.walk(content_root):
        d = Path(dirpath)

        # prevent descending into _quarantine
        if d == quarantine_root:
            dirnames[:] = []
            continue
        if quarantine_root.name in dirnames:
            dirnames.remove(quarantine_root.name)

        for fn in filenames:
            p = d / fn
            if not is_markdown_file(p):
                continue

            scanned += 1
            text = read_text_best_effort(p)
            reasons = find_reasons(text, patterns)

            if reasons:
                dest = quarantine_file(content_root, quarantine_root, p)
                moved += 1
                findings.append(
                    Finding(
                        file=str(p),
                        reasons=reasons,
                        moved_to=str(dest),
                    )
                )

    # Report output
    logs_dir = root / "data" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    report_path = logs_dir / "quarantine_report.json"

    report: Dict = {
        "generatedAt": now_iso(),
        "repoRoot": str(root),
        "contentRoot": str(content_root),
        "quarantineRoot": str(quarantine_root),
        "scannedMarkdownFiles": scanned,
        "quarantinedFiles": moved,
        "findings": [asdict(f) for f in findings],
        "reasonLegend": {
            "unicode_smart_quotes": "Curly quotes (U+2018/2019/201C/201D) present in markdown.",
            "cp1252_control_chars": "Control range U+0080..U+009F present (often from DOCX export).",
            "html_paragraph_tags": "<p> or </p> tags found (HTML soup from conversions).",
            "html_span_token": "Prism/tokenized HTML spans found (<span class='token'>...).",
            "html_entity_braces": "HTML entities for braces (&#123; &#125;) found (mangled code blocks).",
            "brace_quote_artifacts": "Brace+quote artifacts that often break mdsvex/Svelte parsing.",
        },
    }

    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"[quarantine] Repo root: {root}")
    print(f"[quarantine] Scanned markdown files: {scanned}")
    print(f"[quarantine] Quarantined (moved) files: {moved}")
    print(f"[quarantine] Report: {report_path}")
    if moved:
        print(f"[quarantine] Quarantine folder: {quarantine_root}")


if __name__ == "__main__":
    main()
