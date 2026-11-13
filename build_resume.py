#!/usr/bin/env python3
"""Build an ATS-friendly resume PDF from a Markdown resume.

Harness layout: one folder per job target, each holding its own resume:

    resumes/<target>/resume.md      — the resume for that target (source of truth)
    resumes/<target>/<Name>_Resume.pdf  — the generated PDF, written beside it

Edit the markdown, then run:

    python3 build_resume.py resumes/<target>/resume.md [--pages N] [--open] [--snapshot "what changed"]

The PDF lands next to the input, named <Name>_Resume.pdf, where Name is the
bold name on the first line of the markdown. Use --out to write elsewhere.

What it does:
  1. Parses the markdown structure (name/contact header, summary paragraph,
     SKILLS / EXPERIENCE / PROJECTS / EDUCATION sections, job lines, bullets,
     footnotes, hard line breaks).
  2. Renders single-column ATS-safe HTML: Helvetica, no tables/images,
     uppercase section headings, ligatures disabled (Helvetica's "fi"
     ligature breaks keyword extraction in strict ATS parsers).
  3. Prints to PDF with headless Chrome (no page header/footer), AUTO-FITTING
     to the page limit (--pages, default 2): it tries the FIT_STEPS spacing presets from roomiest to
     tightest and keeps the first render that fits. No manual tuning needed.
  4. Verifies with pypdf: reports page count and checks that every long word
     from the markdown survives text extraction (catches ligature/encoding
     regressions).

Chrome is found via the RESUME_CHROME environment variable (full path to a
Chrome or Chromium binary), then the macOS default install, then google-chrome,
chromium or chromium-browser on PATH.

If even the tightest preset spills past the page limit, the tightest render is
kept and a warning is printed. At that point the fix is trimming content, not
adding smaller presets — below ~9pt the resume starts to look cramped.
"""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

MAC_CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROME_ON_PATH = ("google-chrome", "chromium", "chromium-browser")
SECTION_NAMES = {"SKILLS", "EXPERIENCE", "PROJECTS", "EDUCATION"}

DEFAULT_PAGES = 2
# (font-size pt, line-height) presets, roomiest first. The build keeps the
# first one whose render fits the page limit.
FIT_STEPS = [
    (9.5, 1.30),
    (9.4, 1.27),
    (9.4, 1.24),
    (9.3, 1.22),
    (9.3, 1.20),
    (9.2, 1.18),
    (9.1, 1.16),
]


def resume_name(md_text: str) -> str:
    """The person's name: first line of the markdown, bold markers stripped."""
    for line in md_text.splitlines():
        if line.strip():
            return " ".join(re.sub(r"[\*_]", "", line).split())
    return ""


def default_out(md_path: Path, name: str) -> Path:
    """<Name>_Resume.pdf beside the markdown file."""
    stem = re.sub(r"\s+", "_", name.strip()) or "Resume"
    stem = re.sub(r"[/\\:]", "", stem)
    return md_path.parent / f"{stem}_Resume.pdf"


def find_chrome() -> Optional[str]:
    """RESUME_CHROME, then the macOS default, then Chrome/Chromium on PATH."""
    env = os.environ.get("RESUME_CHROME")
    if env and Path(env).exists():
        return env
    if Path(MAC_CHROME).exists():
        return MAC_CHROME
    for cmd in CHROME_ON_PATH:
        found = shutil.which(cmd)
        if found:
            return found
    return None


def css(body_pt: float, line_height: float) -> str:
    return f"""
  @page {{ size: Letter; margin: 0.5in; }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: Helvetica, Arial, sans-serif;
    font-size: {body_pt}pt;
    line-height: {line_height};
    color: #111;
    margin: 0;
    font-variant-ligatures: none;
    font-feature-settings: "liga" 0, "clig" 0;
  }}
  h1 {{ font-size: 16pt; margin: 0 0 2pt 0; letter-spacing: 0.3px; }}
  .contact {{ margin: 0 0 6pt 0; }}
  h2 {{
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    border-bottom: 1px solid #888;
    padding-bottom: 1pt;
    margin: 11pt 0 3.5pt 0;
  }}
  p {{ margin: 0 0 3.5pt 0; }}
  p.skill {{ margin: 0 0 3pt 0; }}
  p.job {{ margin: 5pt 0 1pt 0; }}
  p.job:first-of-type {{ margin-top: 2pt; }}
  ul {{ margin: 1pt 0 3pt 0; padding-left: 13pt; }}
  li {{ margin: 0 0 1pt 0; break-inside: avoid; }}
  p.job {{ break-after: avoid; }}
  p.job.sub, ul.sub {{ margin-left: 13pt; }}
  .note {{ font-style: italic; font-size: {body_pt - 0.1}pt; margin: 4pt 0 0 0; }}
  .edu {{ margin: 4pt 0 2pt 0; }}
"""


def inline(md: str) -> str:
    """Markdown inline formatting → HTML. Links become plain text (ATS-safe)."""
    s = html.escape(md, quote=False)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)  # [text](url) → text
    s = s.replace(r"\*", "&#42;")  # escaped literal asterisk (footnote markers)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s


def paragraph_html(lines: list[str], cls: str) -> str:
    """Join a block's lines; markdown hard breaks (trailing two spaces) → <br>."""
    parts = []
    for i, line in enumerate(lines):
        parts.append(inline(line.rstrip()))
        if i < len(lines) - 1:
            parts.append("<br>")
    cls_attr = f' class="{cls}"' if cls else ""
    return f"<p{cls_attr}>{''.join(parts)}</p>"


def build_body(md_text: str) -> str:
    blocks = [b for b in re.split(r"\n\s*\n", md_text) if b.strip()]
    out = []
    section = None
    sub = False  # inside a sub-entry (an italic-led job line nested under a bold one)
    for idx, block in enumerate(blocks):
        lines = [l for l in block.split("\n") if l.strip()]
        first = lines[0].strip()

        if idx == 0:
            # Header block: bold name line + contact line.
            name = re.sub(r"\*", "", lines[0]).strip()
            out.append(f"<h1>{html.escape(name)}</h1>")
            if len(lines) > 1:
                out.append(paragraph_html(lines[1:], "contact"))
            continue

        m = re.fullmatch(r"\*\*([A-Z &]+)\*\*", first)
        if m and m.group(1).strip() in SECTION_NAMES:
            section = m.group(1).strip()
            sub = False
            out.append(f"<h2>{section.title()}</h2>")
            continue

        if section is None:
            # Paragraph(s) before the first named section = the summary.
            out.append("<h2>Summary</h2>")
            out.append(paragraph_html(lines, ""))
            continue

        if first.startswith("* "):
            items = "".join(
                f"<li>{inline(l.strip()[2:])}</li>" for l in lines if l.strip().startswith("* ")
            )
            out.append(f'<ul class="sub">{items}</ul>' if sub else f"<ul>{items}</ul>")
        elif first.startswith(r"*\*"):
            out.append(paragraph_html(lines, "note"))
        elif section == "SKILLS":
            out.append(paragraph_html(lines, "skill"))
        elif section == "EDUCATION":
            out.append(paragraph_html(lines, "edu"))
        else:  # EXPERIENCE / PROJECTS entry headers
            # A header led by italics (*Role* — dates) is a sub-entry of the bold
            # header above it: it and its bullets indent, so one employer with
            # several roles, or one company with several products and clients,
            # reads as a single listing. Indent is CSS margin only (ATS-safe).
            sub = first.startswith("*") and not first.startswith("**")
            out.append(paragraph_html(lines, "job sub" if sub else "job"))
    return "\n".join(out)


def render_pdf(
    body_html: str, body_pt: float, line_height: float, out: Path, chrome: str, title: str
) -> None:
    page = (
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<title>{html.escape(title)}</title><style>{css(body_pt, line_height)}</style></head>"
        f"<body>\n{body_html}\n</body></html>"
    )
    with tempfile.TemporaryDirectory() as td:
        html_path = Path(td) / "resume.html"
        html_path.write_text(page, encoding="utf-8")
        result = subprocess.run(
            [
                chrome,
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--print-to-pdf={out}",
                html_path.as_uri(),
            ],
            capture_output=True,
            text=True,
        )
    if not out.exists():
        sys.exit(f"Chrome failed to produce a PDF:\n{result.stderr}")


def page_count(pdf_path: Path) -> int:
    from pypdf import PdfReader

    return len(PdfReader(str(pdf_path)).pages)


def verify_words(pdf_path: Path, md_text: str) -> list[str]:
    """Return long words from the markdown missing from the PDF text layer."""
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    extracted = " ".join(page.extract_text() or "" for page in reader.pages).lower()
    plain = re.sub(r"[\*\\\[\]\(\)]", " ", md_text).lower()
    words = {w for w in re.findall(r"[a-z][a-z\-]{7,}", plain)}
    # Words may hyphen-wrap across lines in the PDF; check with hyphens/newlines stripped too.
    squashed = re.sub(r"[\s\-]", "", extracted)
    return sorted(w for w in words if w not in extracted and w.replace("-", "") not in squashed)


def snapshot(md_path: Path, note: str) -> Path:
    """Copy the resume Markdown to versions/vNN.md beside it and log the version.

    Versions are files, not git history, because a user's resumes are gitignored.
    The log (versions/log.md) gets one line per version: number, date, note.
    """
    import datetime
    import shutil

    vdir = md_path.parent / "versions"
    vdir.mkdir(exist_ok=True)
    existing = sorted(vdir.glob("v[0-9][0-9].md"))
    n = int(existing[-1].stem[1:]) + 1 if existing else 1
    dest = vdir / f"v{n:02d}.md"
    shutil.copy2(md_path, dest)
    log = vdir / "log.md"
    if not log.exists():
        log.write_text("# Versions\n\nOne line per snapshot. Restore one by copying it over `resume.md` and snapshotting again; a version is never deleted or edited.\n\n", encoding="utf-8")
    today = datetime.date.today().isoformat()
    with log.open("a", encoding="utf-8") as f:
        f.write(f"- v{n:02d} ({today}): {note}\n")
    return dest


def positive_int(value: str) -> int:
    """argparse type for --pages: an integer of at least 1."""
    try:
        n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not an integer: {value!r}")
    if n < 1:
        raise argparse.ArgumentTypeError(f"must be at least 1: {n}")
    return n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("md", type=Path, help="path to the resume Markdown file")
    ap.add_argument(
        "--out", type=Path, default=None, help="output PDF path (default: <Name>_Resume.pdf beside the input)"
    )
    ap.add_argument(
        "--pages",
        type=positive_int,
        default=DEFAULT_PAGES,
        metavar="N",
        help=f"page limit to auto-fit to (default: {DEFAULT_PAGES}); take it from the page limit in profile.md",
    )
    ap.add_argument("--open", action="store_true", help="open the PDF when done")
    ap.add_argument(
        "--snapshot",
        metavar="NOTE",
        default=None,
        help="before building, copy the Markdown to versions/vNN.md beside it and log NOTE",
    )
    args = ap.parse_args()

    if not args.md.exists():
        sys.exit(f"resume markdown not found: {args.md}")
    chrome = find_chrome()
    if chrome is None:
        sys.exit(
            "Chrome not found. Set the RESUME_CHROME environment variable to the full path "
            "of a Chrome or Chromium binary (or install google-chrome, chromium or "
            "chromium-browser on PATH)."
        )

    if args.snapshot:
        dest = snapshot(args.md, args.snapshot)
        print(f"snapshot {dest}")

    md_text = args.md.read_text(encoding="utf-8")
    name = resume_name(md_text)
    title = f"{name} — Resume" if name else "Resume"
    out = args.out if args.out else default_out(args.md, name)
    body_html = build_body(md_text)

    pages = None
    for body_pt, line_height in FIT_STEPS:
        render_pdf(body_html, body_pt, line_height, out, chrome, title)
        pages = page_count(out)
        if pages <= args.pages:
            break

    missing = verify_words(out, md_text)
    print(
        f"wrote {out} ({out.stat().st_size:,} bytes, {pages} page(s) "
        f"at {body_pt}pt / line-height {line_height})"
    )
    status = 0
    if missing:
        print(f"WARNING: {len(missing)} word(s) did not survive text extraction: {missing[:10]}")
        status = 1
    else:
        print("text extraction verified: all long words from the markdown are present")
    if pages > args.pages:
        print(
            f"WARNING: still {pages} pages (limit {args.pages}) even at the tightest preset — "
            f"trim content in {args.md.name}; do not shrink type further"
        )
        status = 1

    if args.open:
        subprocess.run(["open", str(out)])
    return status


if __name__ == "__main__":
    sys.exit(main())
