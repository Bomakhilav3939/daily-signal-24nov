# Daily Signal — Tuesday, November 24, 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Bomakhilav3939/daily-signal-24nov/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Bomakhilav3939/daily-signal-24nov/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

> [!NOTE]
> **make.fun entry** — [news-image-20261124](https://make.fun/bounty/news-image-20261124)
> "Sum up the world news of 24 November 2026 in one image."

## The entry

`entry.png` is a 1024x1024 agent-rendered front page of *Daily Signal*, a
single-day international newswire for **Tuesday, November 24, 2026**:
three lead stories, ten carded briefs, and a 21-line two-column wire
digest — 34 dated stories across 7 regions, from the Hormuz tanker mine
attacks to the Asian market rally, the 96-drone strike on Ukraine, the
magnitude-5.6 Nepal quake, and the first-ever US supermoon eclipse.

| | |
|---|---|
| Lead 1 | STRAIT OF HORMUZ — Mines set three tankers ablaze; US air cover fails |
| Lead 2 | ASIA · MARKETS — Kospi +7% to settle at 5,000; Nvidia's Huang returns |
| Lead 3 | EUROPE · WAR — Russia fires 96 drones at Ukraine; 2 killed in Zaporizhzhia |
| Cards | Korea air-raid alert · Pakistan's first astronaut · Australia tech fines · Colombia car bomb · Gaza police post · Singapore Megaspeed · Nepal quake · EU migrant pact · Johannesburg floods · Commanders–Bengals |
| Wire | Kyiv chips · London · Paris · Vatican · Tehran ×2 · Greece · Zambia · Dakar · Taronga · Pago Pago · New York · Brasília · Hanoi · supermoon · Riyadh attack · US turkey pardons · US Treasury sanctions · Warsaw sabotage · Riga election |

Every story is dated to 24 November 2026 (or reported that day) and drawn
from open reporting: AP, Reuters, Anadolu, Al Jazeera, POLITICO, The Hindu,
Nikkei Asia, Reuters Middle East.

## How it is built

```
news24.json   ->  34 stories: region, place, headline, deck/body, icon key
render_v2.py  ->  stdlib + Pillow only; no network, no fonts downloaded,
                  no randomness. Same input = same image, byte for byte.
main.py       ->  copies entry.png into $MAKEFUN_OUTPUT_DIR
```

`python3 main.py` is the whole pipeline; `entry.png` is committed so the
output is reproducible without re-rendering.

## Verification

- Two consecutive runs in fresh directories produced **byte-identical**
  `entry.png` (same sha256).
- Image: 1024x1024 RGB PNG, < 1 MiB (fits the submission cap).

## License

MIT — see [LICENSE](LICENSE).
