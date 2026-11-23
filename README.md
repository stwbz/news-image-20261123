[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/stwbz/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/stwbz/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# Sum up 23 November's world news in one image

A newspaper front page for **Monday 23 November 2026**, drawn with Python +
PIL — every word is drawn as text, so nothing is garbled.
Built for the [make.fun bounty "Sum up 23 November's world news in one image"](https://make.fun/bounty/news-image-20261123).

Version 2 carries 15 stories: the front page leads with the COP31 talks
collapsing, then six stories from around the world — Hormuz, Ukraine,
Libya, Mexico, Mercury and Indonesia — then an "Also Today" band with eight
more (Poland, the UN killer-robots deal, Israel, markets, Sudan, Japan, the
US House, and the 2035 Women's World Cup), plus a sport strip (Alcaraz wins
the ATP Finals, Liverpool beat Man United). All facts are from news reported
on 23 November 2026.

## The files

- `entry.png` — the image itself (1024x1024 PNG, 126,089 bytes, under the
  1 MiB cap; verified legible at full size and at ~300 px across).
- `draw.py` — the script that draws `entry.png` (run it to regenerate it).
- `main.ts` — the entry program: copies `entry.png` to
  `MAKEFUN_OUTPUT_DIR/entry.png` (fallback `/output`).

## Check it

```sh
mkdir -p /tmp/news-out && MAKEFUN_OUTPUT_DIR=/tmp/news-out node main.ts
```
