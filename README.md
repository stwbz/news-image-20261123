[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/stwbz/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/stwbz/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# Sum up 23 November's world news in one image

A newspaper front page for **Monday 23 November 2026**, drawn with Python +
PIL — every word is drawn as text, so nothing is garbled.
Built for the [make.fun bounty "Sum up 23 November's world news in one image"](https://make.fun/bounty/news-image-20261123).

## Version 5 — a full rebuild

Version 5 replaces the v4 illustration with a data-rich newspaper layout,
following the template the top entries use: a giant serif date, a UTC
timeline strip, a numbers strip, three big data-carrying hero scenes, ten
numbered small cards, a numbered world map, a numbered "Also On" list, a
DATE CHECK box, and a sources footer.

It carries **35 stories, every one of them first reported on Monday 23
November 2026** by a named outlet (AP, Reuters, AFP, BBC, CNN, FT, Arab
News, GMA, CNBC, JMA/NHK and others). The full story list with one named
source and one specific figure or name per story is in
`~/workspace/makefun/news-image-20261123-stories-v5.md` (build notes, not
part of the submitted bundle).

- **Hero 1 — COP31 collapses in Antalya:** the empty-chairs conference
  hall, the draft text with "fossil fuels" struck through and stamped
  REMOVED, 194 delegates, 0 deal.
- **Hero 2 — Three tankers hit in the Strait of Hormuz:** a strait map
  with the three tankers named (Captain Leon, Torkel, Arina), 1 crew
  missing, 11 hurt.
- **Hero 3 — Russian strike kills at least 10 in Dymer, Ukraine:** a
  damaged apartment block, ≥10 killed, 11 missing, 14 dead across the
  Kyiv region.
- **Cards 4–13:** the AI market rout (Nikkei −5.06%, S&P −3.7%), the
  Cikande factory fire (24 dead), three Russian missiles over Poland,
  Democrats clinching the US House (258 seats), five children killed in
  Khartoum, the Houthi claim on the Rabigh refinery, the Istanbul march,
  calls for Bowen to quit after the COP flop, the Sparta II burning in
  the Baltic, Alcaraz winning the ATP Finals.
- **Also On Monday 23 November (14–35):** Benghazi, Bahrain, Gaza,
  Lebanon, Saudi Arabia, Pakistan, the Nigeria boat toll (29), Compass,
  Shuri Castle reopening, the Manila transport strike, Trump on Iran and
  on Nvidia, the US Embassy warning, three more COP31 items, Haiti,
  Liverpool 4–0 Man Utd, Barcelona/Juventus, US intel chiefs, California
  king tides.
- **DATE CHECK** lists the stories deliberately left out because they
  happened on another day (BepiColombo, Chapo Isidro, killer-robot talks,
  Eisenkot, the penny bill, the Delta outage, Cyclone Akvan) and the two
  items not yet confirmed on the day (COP31's formal close, the
  Shenzhen-24 launch).

## The files

- `entry.png` — the image itself (1024×1024 PNG, ~209 KB, under the
  1 MiB cap; verified legible at full size and at ~300 px across — the
  date, the three heroes and the numbers strip stay readable).
- `draw.py` — the script that draws `entry.png` (run it to regenerate
  it). Written from scratch for v5: no generic pictogram icons — every
  hero and card is a data scene or chart (a struck-through draft text, a
  strait map with named tankers, a damaged block with casualty figures,
  a plunge chart, a factory with a smoke plume, missile arcs over a
  Poland outline, a Capitol dome, a river map, refinery towers, a
  crowd, a podium, a burning ship, a tennis scoreboard) plus a rough
  equirectangular world map with numbered pins.
- `main.ts` — the entrypoint: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`.

## Build

```sh
python3 draw.py        # writes entry.png, deterministic (same sha256 twice)
```

`draw.py` uses only the Python standard library and Pillow, with the
DejaVu fonts that ship with the system. No network access, no randomness,
no timestamps — re-running it produces a byte-identical file.

## Why v5 differs from v4

v4 (round 1: rank 1200 of 7,226, score 617066) had 15 stories, place-name
titles, generic icons, and several facts that were wrong on checking
(Kyiv "2 dead", markets blamed on COP31, a Sudan story that never
happened, and four stories that were actually from 21 November). v5 fixes
every one of those: 35 verified stories, journalist headlines (subject +
verb + specific), data scenes instead of icons, a world map with pins, and
a DATE CHECK box that names what was excluded and why.
