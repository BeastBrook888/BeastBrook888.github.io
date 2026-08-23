#!/usr/bin/env python3
"""Rebuild the portfolio page from its sources.

Run from anywhere:   python3 src/build.py

Reads   src/template.html, src/independent.html, src/charts/*.webp
Writes  index.html        <- the site; this is what GitHub Pages serves
        deploy/index.html <- lone copy, for drag-and-drop hosts (Netlify Drop etc.)

Charts and cover images are inlined as base64 WebP so the result is a single
self-contained file with no local dependencies.
"""
import base64
import pathlib
import re
import shutil
import sys

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent

html = (SRC / "template.html").read_text()
html = html.replace("{{INDEPENDENT}}", (SRC / "independent.html").read_text())

for key in sorted(set(re.findall(r"\{\{(c\d[a-z])\}\}", html))):
    img = SRC / "charts" / f"{key}.webp"
    if not img.exists():
        sys.exit(f"missing chart: {img}")
    uri = "data:image/webp;base64," + base64.b64encode(img.read_bytes()).decode()
    html = html.replace("{{%s}}" % key, uri)

leftover = re.findall(r"\{\{[^}]+\}\}", html)
if leftover:
    sys.exit(f"unreplaced placeholders: {leftover}")

out = ROOT / "index.html"
out.write_text(html)

(ROOT / "deploy").mkdir(exist_ok=True)
shutil.copyfile(out, ROOT / "deploy" / "index.html")

print(f"wrote {out}  ({len(html)/1048576:.2f} MB)")
print(f"wrote {ROOT / 'deploy' / 'index.html'}  (drag this folder to a drop host)")
