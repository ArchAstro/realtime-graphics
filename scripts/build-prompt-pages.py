#!/usr/bin/env python3
"""Regenerate prompts/*/index.html with the prompt-page framework."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"
CATALOG_PATH = ROOT / "techniques" / "catalog.json"

PROMPT_ORDER = [
    "01-snowflow-waterbending",
    "02-desert-explorer",
    "03-claude-of-duty",
    "04-the-long-silence",
    "05-solebound-shoe-repair",
    "06-sdf-blend-shell-creatures",
    "07-bustling-3d-city",
    "08-cod-zombies-clone",
    "09-tower-crane-construction",
    "10-panama-canal-locks",
    "11-painterly-grass-world",
    "12-luxury-mansion-night",
]


def md_inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


def md_to_html(text: str) -> str:
    lines = text.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    in_code = False
    code_buf: list[str] = []
    in_ul = in_ol = False
    table_rows: list[list[str]] = []

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return
        out.append('<div class="table-wrap"><table>')
        for ri, row in enumerate(table_rows):
            if all(re.match(r"^:?-+:?$", c.strip()) for c in row if c.strip()):
                continue
            tag = "th" if ri == 0 else "td"
            out.append(
                "<tr>"
                + "".join(f"<{tag}>{md_inline(c.strip())}</{tag}>" for c in row)
                + "</tr>"
            )
        out.append("</table></div>")
        table_rows = []

    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            close_lists()
            flush_table()
            if not in_code:
                in_code = True
                code_buf = []
            else:
                out.append(
                    f'<pre class="codeblock"><code>{html.escape(chr(10).join(code_buf))}</code></pre>'
                )
                in_code = False
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if "|" in line and line.strip().startswith("|"):
            close_lists()
            cells = [c for c in line.strip().strip("|").split("|")]
            table_rows.append(cells)
            i += 1
            continue
        else:
            flush_table()

        if not line.strip():
            close_lists()
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            close_lists()
            level = len(m.group(1))
            title = m.group(2).strip()
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            out.append(f'<h{level} id="{slug}">{md_inline(title)}</h{level}>')
            i += 1
            continue

        if re.match(r"^[-*]\s+", line):
            if not in_ul:
                close_lists()
                out.append("<ul>")
                in_ul = True
            item = re.sub(r"^[-*]\s+", "", line)
            # avoid double bullets if content starts with -
            item = re.sub(r"^[-*]\s+", "", item)
            out.append(f"<li>{md_inline(item)}</li>")
            i += 1
            continue

        if re.match(r"^\d+\.\s+", line):
            if not in_ol:
                close_lists()
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{md_inline(re.sub(r'^\\d+\\.\\s+', '', line))}</li>")
            i += 1
            continue

        if line.strip() == "---":
            close_lists()
            out.append("<hr />")
            i += 1
            continue

        if line.startswith("> "):
            close_lists()
            out.append(f"<blockquote>{md_inline(line[2:])}</blockquote>")
            i += 1
            continue

        close_lists()
        para = [line]
        while (
            i + 1 < len(lines)
            and lines[i + 1].strip()
            and not re.match(r"^(#{1,4}|[-*]|\d+\.|```|\||---)\s?", lines[i + 1])
            and not lines[i + 1].startswith("> ")
        ):
            i += 1
            para.append(lines[i])
        out.append(f"<p>{md_inline(' '.join(para))}</p>")
        i += 1

    close_lists()
    flush_table()
    if in_code:
        out.append(
            f'<pre class="codeblock"><code>{html.escape(chr(10).join(code_buf))}</code></pre>'
        )
    return "\n".join(out)


def parse_meta_facts(meta_md: str) -> dict[str, str]:
    facts: dict[str, str] = {}
    for line in meta_md.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        key, val = cells[0], cells[1]
        if key.lower() in ("field", "---") or re.match(r"^:?-+:?$", key):
            continue
        if re.match(r"^:?-+:?$", val):
            continue
        facts[key] = val
    return facts


def extract_why(meta_md: str) -> str:
    m = re.search(r"\*\*Why it'?s here:\*\*\s*(.+)", meta_md)
    if m:
        return m.group(1).strip()
    # first non-heading paragraph after title
    for line in meta_md.splitlines():
        if line.startswith("**Why"):
            return re.sub(r"^\*\*Why[^*]*\*\*\s*", "", line).strip()
    return ""


def linkify_fact_value(raw: str) -> str:
    """Turn meta.md cell into HTML with real links where possible."""
    # Prefer markdown links first via md_inline path
    if "](" in raw:
        return md_inline(raw)
    # Bare URLs
    if re.match(r"^https?://", raw.strip()):
        u = html.escape(raw.strip())
        return f'<a href="{u}" target="_blank" rel="noopener">{u}</a>'
    # backticks
    return md_inline(raw)


def build_facts_html(facts: dict[str, str]) -> str:
    if not facts:
        return ""
    # preferred order
    order = [
        "Author",
        "Model",
        "Stack",
        "Effort",
        "Demo",
        "Repo",
        "Reddit",
        "X",
        "X writeup",
        "Perf",
        "Duration",
        "When",
        "Prompt file in repo",
    ]
    keys = [k for k in order if k in facts] + [k for k in facts if k not in order]
    parts = []
    for k in keys:
        parts.append(
            f'<div class="fact"><span class="fact-key">{html.escape(k)}</span>'
            f'<div class="fact-val">{linkify_fact_value(facts[k])}</div></div>'
        )
    return f'<div class="facts">{"".join(parts)}</div>'


def hero_actions(facts: dict[str, str]) -> str:
    btns = []
    for key, label in (("Demo", "Open demo ↗"), ("Repo", "GitHub ↗"), ("Reddit", "Reddit ↗"), ("X", "X / Twitter ↗"), ("X writeup", "Writeup ↗")):
        if key not in facts:
            continue
        val = facts[key]
        m = re.search(r"\((https?://[^)]+)\)", val)
        url = m.group(1) if m else (val.strip() if val.strip().startswith("http") else "")
        if not url:
            continue
        cls = "btn primary" if key == "Demo" else "btn"
        btns.append(
            f'<a class="{cls}" href="{html.escape(url)}" target="_blank" rel="noopener">{label}</a>'
        )
    return "\n".join(btns)


def load_catalog():
    if CATALOG_PATH.exists():
        return json.loads(CATALOG_PATH.read_text())
    return {"techniques": {}, "prompts": {}}


def main():
    catalog = load_catalog()
    techniques = catalog.get("techniques") or {}
    prompts_cat = catalog.get("prompts") or {}

    # discover folders
    folders = [p for p in PROMPTS.iterdir() if p.is_dir() and (p / "meta.md").exists()]
    folders.sort(key=lambda p: p.name)

    # ordered list for prev/next
    ordered = [p for pid in PROMPT_ORDER for p in folders if p.name == pid]
    for p in folders:
        if p not in ordered:
            ordered.append(p)

    for idx, folder in enumerate(ordered):
        pid = folder.name
        cat = prompts_cat.get(pid) or {}
        title = cat.get("title") or pid
        blurb = cat.get("blurb") or ""
        tech_ids = cat.get("techniques") or []

        meta_path = folder / "meta.md"
        meta_md = meta_path.read_text() if meta_path.exists() else ""
        facts = parse_meta_facts(meta_md)
        why = extract_why(meta_md)

        # content files
        prompt_files = sorted(
            [
                p
                for p in folder.iterdir()
                if p.suffix == ".md"
                and p.name.startswith("prompt")
            ],
            key=lambda p: p.name,
        )
        notes_path = folder / "notes.md"

        # Residual overview: strip title, why line, field tables, "see prompt.md"
        residual = meta_md
        residual = re.sub(r"^#.*$", "", residual, count=1, flags=re.M)
        residual = re.sub(r"\*\*Why it'?s here:\*\*.+", "", residual)
        # remove markdown tables
        residual = re.sub(
            r"(?m)^\|.+\|\s*\n(?:\|[-:| ]+\|\s*\n)?(?:\|.+\|\s*\n)*",
            "",
            residual,
        )
        residual = re.sub(
            r"(?im)^##\s*Prompt\s*\n+See .+$",
            "",
            residual,
        )
        residual = re.sub(r"\n{3,}", "\n\n", residual).strip()
        overview_html = md_to_html(residual) if residual else ""

        # prev/next
        prev_f = ordered[idx - 1] if idx > 0 else None
        next_f = ordered[idx + 1] if idx + 1 < len(ordered) else None
        prev_title = (prompts_cat.get(prev_f.name) or {}).get("title", prev_f.name) if prev_f else ""
        next_title = (prompts_cat.get(next_f.name) or {}).get("title", next_f.name) if next_f else ""

        # TOC items
        toc_items = [('overview', 'Overview')]
        if prompt_files:
            toc_items.append(('prompt', 'Prompt' if len(prompt_files) == 1 else 'Prompts'))
        if notes_path.exists():
            toc_items.append(('notes', 'Notes'))
        if tech_ids:
            toc_items.append(('techniques', 'Techniques'))

        toc_html = "\n".join(
            f'<a href="#{sid}">{html.escape(label)}</a>' for sid, label in toc_items
        )

        # techniques cards
        tech_cards = []
        for tid in tech_ids:
            t = techniques.get(tid) or {}
            ttitle = t.get("title") or tid
            twhy = t.get("why") or ""
            demo = t.get("demo") or f"{tid}.html"
            tech_cards.append(
                f"""
            <div class="tech-card">
              <div class="t-title">{html.escape(ttitle)}</div>
              <div class="t-why">{html.escape(twhy)}</div>
              <div class="t-links">
                <a href="/techniques/#{html.escape(tid)}">Notes</a>
                <a href="/techniques/demos/{html.escape(demo)}">Live demo</a>
              </div>
            </div>"""
            )
        tech_section = ""
        if tech_cards:
            tech_section = f"""
        <section class="card" id="techniques">
          <div class="card-head"><h2>Related techniques</h2></div>
          <div class="card-body">
            <div class="tech-grid">{''.join(tech_cards)}</div>
          </div>
        </section>"""

        # prompt sections
        prompt_blocks = []
        for pi, pf in enumerate(prompt_files):
            label = "Prompt" if pf.name == "prompt.md" else pf.stem.replace("prompt-", "Prompt · ").replace("-", " ")
            body = md_to_html(pf.read_text())
            # raw text for copy — prefer fenced code content if whole file is one fence
            raw_for_copy = pf.read_text()
            # strip outer markdown chrome for cleaner copy of pure prompt files
            copy_id = "prompt-source" if pi == 0 else f"prompt-source-{pi}"
            copy_btn = ""
            if pi == 0:
                copy_btn = """
              <div style="display:flex;align-items:center;gap:0.65rem">
                <span class="copy-status" id="copy-status"></span>
                <button type="button" class="btn ghost" id="copy-prompt">Copy prompt</button>
              </div>"""
            prompt_blocks.append(
                f"""
        <section class="card prompt-panel" id="{'prompt' if pi == 0 else 'prompt-' + str(pi)}">
          <div class="card-head">
            <h2>{html.escape(label)}</h2>
            {copy_btn}
          </div>
          <div class="card-body">
            <div class="prompt-body" id="{copy_id}" data-raw="{html.escape(raw_for_copy)}">
              <div class="doc">{body}</div>
            </div>
          </div>
        </section>"""
            )
        # Use data-raw for copy instead of innerText of HTML
        prompts_html = "\n".join(prompt_blocks)

        notes_section = ""
        if notes_path.exists():
            notes_section = f"""
        <section class="card" id="notes">
          <div class="card-head"><h2>Notes</h2></div>
          <div class="card-body">
            <div class="doc">{md_to_html(notes_path.read_text())}</div>
          </div>
        </section>"""

        why_html = f'<p class="why"><strong>Why it\'s here.</strong> {md_inline(why)}</p>' if why else ""
        facts_html = build_facts_html(facts)
        actions = hero_actions(facts)
        residual_block = (
            f'<div class="doc overview-doc" style="margin-top:1rem">{overview_html}</div>'
            if overview_html.strip()
            else ""
        )

        prev_btn = (
            f'<a href="/prompts/{prev_f.name}/">← {html.escape(prev_title)}</a>'
            if prev_f
            else '<a class="is-disabled" href="#">← Prev</a>'
        )
        next_btn = (
            f'<a href="/prompts/{next_f.name}/">{html.escape(next_title)} →</a>'
            if next_f
            else '<a class="is-disabled" href="#">Next →</a>'
        )

        num = pid.split("-")[0]

        page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)} — Prompt archive</title>
  <link rel="stylesheet" href="/techniques/shared.css" />
  <link rel="stylesheet" href="/prompts/prompt-page.css" />
</head>
<body class="prompt-page">
  <div class="shell site-content">
    <div class="topnav">
      <div class="crumbs">
        <a href="/">Home</a> ·
        <a href="/techniques/">Techniques</a> ·
        <a href="/techniques/demos/">Demos</a> ·
        <a href="/prompts/">Prompts</a>
      </div>
      <div class="pager">
        {prev_btn}
        {next_btn}
      </div>
    </div>

    <header class="hero">
      <div class="hero-kicker">
        <span class="hero-num">{html.escape(num)}</span>
        <span class="hero-id">{html.escape(pid)}</span>
      </div>
      <h1>{html.escape(title)}</h1>
      <p class="hero-blurb">{html.escape(blurb)}</p>
      <div class="hero-actions">
        {actions}
        <a class="btn" href="/prompts/">All prompts</a>
      </div>
    </header>

    <div class="layout-prompt">
      <aside class="toc">
        <div class="toc-label">On this page</div>
        <nav>
          {toc_html}
        </nav>
      </aside>

      <div class="main-col">
        <section class="card" id="overview">
          <div class="card-head"><h2>Overview</h2></div>
          <div class="card-body">
            {why_html}
            {facts_html}
            {residual_block}
          </div>
        </section>

        {prompts_html}
        {notes_section}
        {tech_section}

        <div class="footer-nav pager">
          {prev_btn}
          {next_btn}
        </div>
      </div>
    </div>
  </div>
  <script src="/techniques/site-bg.js?v=4"></script>
  <script>
    // Prefer raw markdown for copy (cleaner than rendered text)
    (function () {{
      const btn = document.getElementById("copy-prompt");
      const el = document.getElementById("prompt-source");
      const status = document.getElementById("copy-status");
      if (!btn || !el) return;
      btn.addEventListener("click", async () => {{
        const raw = el.getAttribute("data-raw") || el.innerText || "";
        // decode HTML entities from attribute
        const ta = document.createElement("textarea");
        ta.innerHTML = raw;
        const text = ta.value;
        try {{
          await navigator.clipboard.writeText(text);
          if (status) {{ status.textContent = "Copied"; status.classList.add("show"); setTimeout(() => status.classList.remove("show"), 1600); }}
        }} catch (e) {{
          if (status) {{ status.textContent = "Copy failed"; status.classList.add("show"); }}
        }}
      }});
    }})();
  </script>
  <script src="/prompts/prompt-page.js"></script>
</body>
</html>
"""
        (folder / "index.html").write_text(page)
        print("wrote", pid)

    print(f"Built {len(ordered)} prompt pages.")


if __name__ == "__main__":
    main()
