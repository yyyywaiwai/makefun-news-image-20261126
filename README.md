# 26 November 2026, summed up in one picture

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/yyyywaiwai/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/yyyywaiwai/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

`entry.png` packs the day's world news — 26 November 2026 — into a
single 1024×1024 front page, laid out like a newspaper.

The lead is the highway fuel-tanker fire in Cairo: 30 people dead,
39 ambulances sent to the scene. Around it sit seven more stories
from the same day — the Nasdaq sliding roughly 4% as AI worries and
tariffs rattle stocks; fresh US tariffs announced against China and
other trading partners; Ukrainian strikes pushing Russian refining
to a 20-year low; 30 killed in armed attacks in Nigeria's Niger
state; Israel killing a new Hamas security chief in Gaza; Colombia
marking a decade since its landmark peace deal; and Shenzhou-24
lifting off carrying the first foreign astronaut, as BepiColombo
arrives at Mercury.

`main.py` does the handover: it checks that `entry.png` fits the
bounty's limits (PNG, at most 1024×1024, at most 1 MiB) and copies it
unchanged into the output folder, confirming the copy's SHA-256
matches the original. It needs only the Python 3 standard library,
touches no network, and every run gives the same bytes.

## Running it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To check the picture without copying anything:

```sh
python3 main.py --verify-only
```

Bounty: <https://make.fun/bounty/news-image-20261126>
