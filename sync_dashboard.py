#!/usr/bin/env python3
"""Copy the analysis dashboard from the private analysis repo into this public site repo.

GitHub Pages will not serve a private repository on a free plan, so the file is duplicated
here rather than linked.

The source is authored for the Artifact runtime, which supplies the doctype/head/body
wrapper at publish time. Served as a plain file it would render in quirks mode and its
<title> would land in the body, so this splits the source at the end of its leading
head-level block (title, font links, style) and wraps each half into the right element.

    python3 sync_dashboard.py        # then commit and push
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/nba_star_fit/def_dashboard.html")
DST = os.path.join(HERE, "dashboard.html")

HEAD = ('<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="description" content="Defensive and possession analysis of the '
        'projected 2026-27 Philadelphia 76ers, built from rebuilt play-by-play lineups.">\n'
        '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n')


def main():
    if not os.path.exists(SRC):
        sys.exit(f"source not found: {SRC}")
    raw = open(SRC, encoding="utf-8").read()
    m = list(re.finditer(r"</style>", raw))
    cut = m[0].end() if m else 0
    head_src, body_src = raw[:cut].strip(), raw[cut:].strip()
    title = (re.search(r"<title>(.*?)</title>", head_src, re.S) or [None, "Dashboard"])[1].strip()
    open(DST, "w", encoding="utf-8").write(
        HEAD + head_src + "\n</head>\n<body>\n" + body_src + "\n</body>\n</html>\n")
    print(f"  wrapped {len(raw):,} bytes -> dashboard.html   (title: {title!r})")
    print("  live at https://beastbrook888.github.io/dashboard.html after push")


if __name__ == "__main__":
    main()
