# Basketball Analytics Portfolio — Colin Rondon

A single-page portfolio of four articles published with the
[Sports Analytics Group at Berkeley](https://sportsanalytics.studentorg.berkeley.edu/)
(Dec 2024 – Jun 2026), plus two independent NBA analytics projects.

Each entry carries its research question, data sources, method, headline findings,
the published charts, and an honest note on what it gets wrong.

**Live site:** https://beastbrook888.github.io

## Layout

```
index.html          the site — a single self-contained file, no local dependencies
src/
  template.html     page source; edit this, never index.html
  independent.html  the two independent-project cards
  charts/           24 published figures, downscaled to WebP (836 KB)
  build.py          inlines the charts and writes ../index.html
deploy/             build copy for drag-and-drop hosts (git-ignored)
```

## Rebuilding

```sh
python3 src/build.py
```

Requires only the Python standard library. Charts and cover images are embedded as
base64 WebP, so `index.html` works from any location — including opened directly
from disk. The only external request is Google Fonts, which degrades to system
fonts if unavailable.

## Editing your contact details

They live near the top of `src/template.html`, in the block marked
`FILL IN YOUR CONTACT DETAILS HERE`. Change them there and rebuild.

## Where the charts come from

All 24 figures are the charts **as published**, not re-plotted. The four SAGB
articles' figures were pulled from the live site (`/images/dj-pics/<slug>/`);
`c5a` is a screenshot of the interactive report built by `~/nba-availability-model`.
Cover images are uncropped and embedded once each as a CSS variable, then used at
two sizes.

Note: the Bridges article's cover on the SAGB site (`main.jpg`) currently 404s, so
that cover was taken from the higher-resolution in-body copy (`1a.png`).
