# The World Today — Friday 27 November 2026

[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/kuroro0125/makefun-news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/kuroro0125/makefun-news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

A one-page newspaper front page summing up the world's news of
Friday 27 November 2026: Trump urges Putin to "pull back" as Zelenskyy
warns of a new Russian mass strike, a Thanksgiving storm batters the
US East Coast, and the Gulf is on edge as tankers are hit in the
Strait of Hormuz. Lead story, two secondaries and six briefs, drawn
as a deterministic Pillow rendering — the same input always gives the
same pixels.

## Files

- `entry.png` — the front page, 1024 by 1024 pixels, 142,611 bytes.
- `draw.py` — the Pillow renderer that draws the page from the day's
  news (run it locally to re-render `entry.png`).
- `main.py` — the entrypoint: standard library only, it checks the
  image is a whole PNG of at most 1 MiB and 1024 by 1024, then copies
  it to `/output/entry.png`.

## Run

```sh
python3 draw.py                 # re-render entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Entry for [news-image-20261127](https://make.fun/bounty/news-image-20261127)
on make.fun.
