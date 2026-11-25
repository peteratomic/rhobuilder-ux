#!/usr/bin/env python3
"""Build the rhobuilder manual as web pages.

Reads the unmodified upstream docs in vendor/rhobuilder/docs/src (plus the repo's
CONTRIBUTING.md and SECURITY.md) and writes styled HTML pages to ux/docs/.
No markdown file is ever linked to: every .md link is rewritten to its page.

Usage:  python3 ux/build.py
Needs:  pip install markdown pygments
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import markdown
    from pygments.formatters import HtmlFormatter
    from pygments import highlight
    from pygments.lexers import JsonLexer
except ImportError:
    sys.exit("Missing dependencies. Run:  pip install markdown pygments")

UX = Path(__file__).resolve().parent
REPO = UX.parent / "vendor" / "rhobuilder"
SRC = REPO / "docs" / "src"
OUT = UX / "docs"
GITHUB = "https://github.com/rhovision-org/rhobuilder/blob/main/"

# Upstream files outside docs/src that the manual links to, rendered as pages too.
EXTRA = {
    "CONTRIBUTING.md": ("project/contributing", "Contributing guide"),
    "SECURITY.md": ("project/security-policy", "Security policy"),
}


def upstream_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def parse_summary() -> list[tuple[str, list[tuple[str, str]]]]:
    """SUMMARY.md -> [(section, [(title, slug), ...]), ...]"""
    sections: list[tuple[str, list[tuple[str, str]]]] = []
    for line in (SRC / "SUMMARY.md").read_text().splitlines():
        if line.startswith("# ") and line.strip() != "# Summary":
            sections.append((line[2:].strip(), []))
        m = re.match(r"\s*-\s*\[(.+?)\]\((.+?)\.md\)", line)
        if m and sections:
            sections[-1][1].append((m.group(1), m.group(2)))
    return sections


def collect_pages() -> dict[str, Path]:
    """slug -> source file, for every page we will build."""
    pages = {str(p.relative_to(SRC).with_suffix("")): p
             for p in SRC.rglob("*.md") if p.name != "SUMMARY.md"}
    for name, (slug, _) in EXTRA.items():
        if (REPO / name).exists():
            pages[slug] = REPO / name
    return pages


def rel(from_slug: str, to: str) -> str:
    """Relative URL from docs/<from_slug>.html to docs/<to>."""
    depth = from_slug.count("/")
    return "../" * depth + to


def rewrite_links(body: str, slug: str, src: Path, pages: dict[str, Path],
                  json_pages: dict[str, str], unresolved: set[str]) -> str:
    src_dir = src.parent

    def fix(m: re.Match) -> str:
        href = m.group(1)
        if href.startswith(("#", "mailto:")):
            return m.group(0)
        target, _, anchor = href.partition("#")
        anchor = "#" + anchor if anchor else ""

        # Absolute GitHub links to files we render ourselves
        if target.startswith(GITHUB):
            path = target[len(GITHUB):]
            if path in EXTRA:
                return f'href="{rel(slug, EXTRA[path][0] + ".html")}{anchor}"'
            if path.startswith("docs/src/") and path.endswith(".md"):
                return f'href="{rel(slug, path[len("docs/src/"):-3] + ".html")}{anchor}"'
            return m.group(0)
        if re.match(r"^[a-z]+://", target):
            return m.group(0)

        resolved = (src_dir / target).resolve()
        try:
            inside = str(resolved.relative_to(SRC.resolve()))
        except ValueError:
            inside = None
        if target.endswith(".md"):
            if inside and inside[:-3] in pages:
                return f'href="{rel(slug, inside[:-3] + ".html")}{anchor}"'
            try:
                repo_rel = str(resolved.relative_to(REPO.resolve()))
            except ValueError:
                repo_rel = target
            if repo_rel in EXTRA:
                return f'href="{rel(slug, EXTRA[repo_rel][0] + ".html")}{anchor}"'
            if repo_rel.startswith("docs/src/") and repo_rel[9:-3] in pages:
                return f'href="{rel(slug, repo_rel[9:-3] + ".html")}{anchor}"'
            unresolved.add(f"{slug}: {href}")
            return f'href="{GITHUB}{repo_rel}{anchor}"'
        if inside and inside in json_pages:
            return f'href="{rel(slug, json_pages[inside] + ".html")}"'
        # Any other repo file (source code etc.): link to GitHub
        try:
            repo_rel = str(resolved.relative_to(REPO.resolve()))
            return f'href="{GITHUB}{repo_rel}{anchor}"'
        except ValueError:
            unresolved.add(f"{slug}: {href}")
            return m.group(0)

    return re.sub(r'href="([^"]+)"', fix, body)


def sidebar(sections, current: str) -> str:
    out = []
    for name, items in sections:
        out.append(f"<h4>{html.escape(name)}</h4><ul>")
        for title, s in items:
            cur = ' aria-current="page"' if s == current else ""
            out.append(f'<li><a href="{rel(current, s + ".html")}"{cur}>{html.escape(title)}</a></li>')
        out.append("</ul>")
    return "".join(out)


def pager(order: list[tuple[str, str]], slug: str) -> str:
    slugs = [s for _, s in order]
    if slug not in slugs:
        return ""
    i = slugs.index(slug)
    parts = []
    if i > 0:
        t, s = order[i - 1]
        parts.append(f'<a class="prev" href="{rel(slug, s + ".html")}"><div class="dir">← Previous</div>'
                     f'<div class="t">{html.escape(t)}</div></a>')
    if i < len(order) - 1:
        t, s = order[i + 1]
        parts.append(f'<a class="next" href="{rel(slug, s + ".html")}"><div class="dir">Next</div>'
                     f'<div class="t">{html.escape(t)} →</div></a>')
    return "".join(parts)


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — rhobuilder</title>
<link rel="stylesheet" href="{root}assets/style.css">
<link rel="stylesheet" href="{root}assets/code.css">
</head>
<body data-page="{slug}" data-root="{root}">
<div class="doc-shell">
  <header class="topbar">
    <a class="brand" href="{root}index.html"><span class="brand-mark" aria-hidden="true">ρ</span>rhobuilder</a>
    <nav class="topnav">
      <a class="hide-sm" href="{root}index.html">Choose your path</a>
      <a class="hide-sm" href="{root}docs/index.html">Manual</a>
      <button class="menu-toggle" aria-expanded="false" aria-controls="sidebar">Contents</button>
    </nav>
  </header>
  <div class="doc-grid">
    <nav class="sidebar" id="sidebar" aria-label="Manual">{sidebar}</nav>
    <main>
      <article class="prose">
{body}
      </article>
      <nav class="pager" aria-label="Pages">{pager}</nav>
      <footer class="footer">Built from rhobuilder <code>{commit}</code>.</footer>
    </main>
  </div>
</div>
<script src="{root}assets/roles.js"></script>
<script src="{root}assets/docs.js"></script>
</body>
</html>
"""


def render_page(slug, title, body, sections, order, commit):
    root = "../" * (slug.count("/") + 1)
    body = re.sub(r"<table>", '<div class="table-wrap"><table>', body)
    body = body.replace("</table>", "</table></div>")
    out = PAGE.format(title=html.escape(title), root=root, slug=slug, body=body,
                      sidebar=sidebar(sections, slug), pager=pager(order, slug), commit=commit)
    dest = OUT / f"{slug}.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out)


def write_code_css():
    light = HtmlFormatter(style="friendly").get_style_defs(".highlight")
    try:
        dark = HtmlFormatter(style="github-dark").get_style_defs(".highlight")
    except Exception:
        dark = HtmlFormatter(style="monokai").get_style_defs(".highlight")
    reset = ".highlight, .highlight pre { background: var(--code-bg) !important; }\n" \
            ".highlight .err { border: 0 !important; background: none !important; }\n"
    (UX / "assets" / "code.css").write_text(
        "/* Generated by build.py — code highlighting */\n" + light + "\n"
        "@media (prefers-color-scheme: dark) {\n" + dark + "\n}\n" + reset)


def main():
    if not SRC.exists():
        sys.exit("vendor/rhobuilder is empty. Run:  git submodule update --init")
    commit = upstream_commit()
    sections = parse_summary()
    order = [item for _, items in sections for item in items]
    pages = collect_pages()

    # Evidence JSON files become pages too
    json_pages = {str(p.relative_to(SRC)): str(p.relative_to(SRC).with_suffix(""))
                  for p in SRC.rglob("*.json")}

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    write_code_css()

    md = markdown.Markdown(extensions=[
        "tables", "fenced_code", "sane_lists",
        "codehilite", "toc",
    ], extension_configs={
        "codehilite": {"css_class": "highlight", "guess_lang": False},
        "toc": {"permalink": "#", "permalink_class": "headerlink"},
    })

    unresolved: set[str] = set()
    for slug, src in sorted(pages.items()):
        text = src.read_text()
        m = re.search(r"^#\s+(.+)$", text, re.M)
        title = m.group(1).strip() if m else slug
        extra_titles = {s: t for s, t in EXTRA.values()}
        if slug in extra_titles:
            title = extra_titles[slug]
        body = md.reset().convert(text)
        body = rewrite_links(body, slug, src, pages, json_pages, unresolved)
        render_page(slug, title, body, sections, order, commit)

    for src_rel, slug in json_pages.items():
        data = json.loads((SRC / src_rel).read_text())
        pretty = json.dumps(data, indent=2, ensure_ascii=False)
        code = highlight(pretty, JsonLexer(), HtmlFormatter(cssclass="highlight"))
        name = Path(src_rel).name
        intro = ("<p>This is a template, not evidence. It must not be filled in until an approved "
                 "campaign actually runs.</p>" if "template" in name else
                 "<p>A measured evidence record, shown exactly as stored in the repository.</p>")
        body = (f"<h1>{html.escape(name)}</h1>\n{intro}\n"
                f'<p><a href="{rel(slug, "evidence.html")}">← What the evidence records mean</a></p>\n{code}')
        render_page(slug, name, body, sections, order, commit)

    built = len(pages) + len(json_pages)
    print(f"Built {built} pages from rhobuilder {commit} into {OUT.relative_to(UX.parent)}/")
    if unresolved:
        print("Links to markdown files that have no page (sent to GitHub instead):")
        for u in sorted(unresolved):
            print("  ", u)


if __name__ == "__main__":
    main()
