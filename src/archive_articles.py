#!/usr/bin/env python3
"""Archive the four SAGB articles into this repo, so the site does not depend on
sportsanalytics.studentorg.berkeley.edu staying up.

These are Colin's own articles. What is stored is the prose only: images are dropped
because the 24 published figures are already embedded in the portfolio itself as base64,
and keeping external <img> references would reintroduce exactly the dependency this is
meant to remove. Where a figure sat, a marker is left so the reader knows one belonged
there.

Attributes are stripped so the text inherits the portfolio's own typography rather than
dragging in SAGB's stylesheet.

Run:  python3 src/archive_articles.py
"""
import html as html_mod
import os
import re
import sys
import time
import urllib.request

BASE = "https://sportsanalytics.studentorg.berkeley.edu/articles/"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "articles")

SLUGS = {
    "bridges-iron-man-streak": "Mikal Bridges: How Probable Was The Iron Man's Streak?",
    "g-league-call-ups": "G-League Call-Ups: A Way to Find Hidden Gems?",
    "russell-westbrook-resurgence": "Russell Westbrook and His Resurgence with the Denver Nuggets",
    "guards-post-up": "Should Guards be Posting Up More Often?",
}
KEEP = r"p|h3|h4|ul|ol|li|blockquote|table|thead|tbody|tr|th|td|em|strong|b|i|sup|sub|br|code|span"


def fetch(slug):
    req = urllib.request.Request(BASE + slug + ".html", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", errors="ignore")


def extract(raw):
    """Pull the largest <article> block, then reduce it to safe, unstyled prose."""
    blocks = re.findall(r"<article[^>]*>(.*?)</article>", raw, re.S)
    if not blocks:
        raise SystemExit("no <article> block found — SAGB markup changed")
    s = max(blocks, key=len)

    s = re.sub(r"<(script|style|nav|form|iframe|noscript)[^>]*>.*?</\1>", "", s, flags=re.S)
    # figures: replace with a marker rather than an external reference
    s = re.sub(r"<figure[^>]*>.*?</figure>", '<p class="figmark">[figure]</p>', s, flags=re.S)
    s = re.sub(r"<img[^>]*>", '<span class="figmark">[figure]</span>', s)
    s = re.sub(r"<a[^>]*>(.*?)</a>", r"\1", s, flags=re.S)      # drop links; many are relative
    s = re.sub(r"<h1[^>]*>.*?</h1>", "", s, flags=re.S)         # title is supplied by the page
    s = re.sub(r"<h2[^>]*>.*?</h2>", "", s, flags=re.S, count=1)

    # strip every tag that is not in KEEP, and every attribute on the ones that are
    def clean_tag(m):
        closing, name, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if not re.fullmatch(KEEP, name):
            return ""
        if closing:
            return f"</{name}>"
        cls = re.search(r'class="(figmark)"', attrs or "")
        return f'<{name} class="figmark">' if cls else f"<{name}>"

    s = re.sub(r"<(/?)([a-zA-Z0-9]+)((?:\s[^>]*)?)/?>", clean_tag, s)
    s = re.sub(r"[ \t]{2,}", " ", s)          # the source is deeply indented
    s = re.sub(r"\n\s*\n+", "\n", s)
    s = re.sub(r"<p>\s*</p>", "", s)
    return s.strip()


def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for i, (slug, title) in enumerate(SLUGS.items()):
        if i:
            time.sleep(2)
        try:
            body = extract(fetch(slug))
        except Exception as e:
            print(f"  FAILED {slug}: {e}", file=sys.stderr)
            continue
        words = len(re.sub(r"<[^>]+>", " ", body).split())
        stamp = time.strftime("%Y-%m-%d")
        head = (f'<p class="archnote">Archived copy, retrieved {stamp} from the Sports '
                f'Analytics Group at Berkeley. Figures appear above; markers show where '
                f'they sat in the original.</p>\n')
        open(os.path.join(OUT, slug + ".html"), "w").write(head + body + "\n")
        print(f"  {slug:32s} {words:5d} words")
        total += words
    print(f"  archived {total:,} words into src/articles/")


if __name__ == "__main__":
    main()
