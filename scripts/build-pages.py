#!/usr/bin/env python3
"""
Build a static site for GitHub Pages.

Project pages live at https://<org>.github.io/<repo>/ so absolute paths
like /techniques/ must become /realtime-graphics/techniques/.

Usage:
  BASE_PATH=/realtime-graphics python3 scripts/build-pages.py
  python3 scripts/build-pages.py          # default BASE_PATH=/realtime-graphics
  BASE_PATH= python3 scripts/build-pages.py   # no prefix (local-style)
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".pages-dist"
# GitHub project pages default path
BASE = os.environ.get("BASE_PATH", "/realtime-graphics").rstrip("/")

SKIP_DIRS = {
    ".git",
    ".pages-dist",
    "node_modules",
    ".grok",
    "scripts",
    "skills",
    ".github",
}

SKIP_FILES = {
    "package.json",
    "skills.sh.json",
    "techniques.md",
    ".gitignore",
}


def copy_tree() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # Rebuild prompt HTML first (absolute / paths; we rewrite after)
    subprocess.check_call(
        [sys.executable, str(ROOT / "scripts" / "build-prompt-pages.py")],
        cwd=ROOT,
    )

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel.name in SKIP_FILES:
            continue
        if rel.name.startswith(".tmp"):
            continue
        if rel.suffix in {".md"} and rel.parts[0] not in {"prompts"}:
            # keep prompt sources out of pages; techniques.md not needed
            if rel.name == "README.md" and len(rel.parts) == 1:
                continue
            if rel.parts[0] != "prompts":
                continue
        # Include prompt md for raw viewing? skip — HTML is enough
        if rel.parts[0] == "prompts" and rel.suffix == ".md":
            continue

        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


def rewrite_file(path: Path) -> None:
    if path.suffix not in {".html", ".js", ".css", ".json"}:
        return
    text = path.read_text(encoding="utf-8")
    orig = text

    if not BASE:
        return

    # href="/...  src="/...  action="/...  fetch("/...  url("/...
    # Avoid double-prefixing
    def prefix_abs(match: re.Match[str]) -> str:
        prefix, quote, path = match.group(1), match.group(2), match.group(3)
        if path.startswith(BASE + "/") or path == BASE:
            return match.group(0)
        if path.startswith("//"):
            return match.group(0)
        return f"{prefix}{quote}{BASE}{path}{quote}"

    # href="/foo" or href='/foo'
    text = re.sub(
        r"""((?:href|src|action)\s*=\s*)(['"])(/(?!/).*?)\2""",
        prefix_abs,
        text,
    )
    # fetch("/foo") or fetch('/foo')
    text = re.sub(
        r"""(fetch\s*\(\s*)(['"])(/(?!/).*?)\2""",
        prefix_abs,
        text,
    )
    # CSS url(/foo)
    text = re.sub(
        r"""(url\(\s*)(['"]?)(/(?!/).*?)\2(\s*\))""",
        lambda m: (
            m.group(0)
            if m.group(3).startswith(BASE + "/")
            else f"{m.group(1)}{m.group(2)}{BASE}{m.group(3)}{m.group(2)}{m.group(4)}"
        ),
        text,
    )

    # site-bg attach still works; pathname detection optional
    if path.name == "site-bg.js" and "SITE_BASE" not in text:
        pass

    if text != orig:
        path.write_text(text, encoding="utf-8")


def write_nojekyll() -> None:
    (OUT / ".nojekyll").write_text("")


def main() -> None:
    print(f"Building Pages site → {OUT}")
    print(f"  BASE_PATH={BASE!r}")
    copy_tree()
    for path in OUT.rglob("*"):
        if path.is_file():
            rewrite_file(path)
    write_nojekyll()
    # small index check
    index = (OUT / "index.html").read_text(encoding="utf-8")
    sample = re.search(r'href="([^"]+shared\.css[^"]*)"', index)
    print(f"  sample css href: {sample.group(1) if sample else 'n/a'}")
    print("Done.")


if __name__ == "__main__":
    main()
