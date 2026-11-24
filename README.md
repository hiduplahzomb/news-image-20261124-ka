# The Tuesday Herald — News Image 20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/hiduplahzomb/news-image-20261124-ka/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard)
[![reward](https://make.fun/badge/news-image-20261124/hiduplahzomb/news-image-20261124-ka/reward.svg)](https://make.fun/bounty/news-image-20261124)

A newspaper front page summing up Tuesday 24 November 2026's world
news in one image. `main.py` draws the whole page with PIL (no photos):
masthead "THE TUESDAY HERALD", dateline, a dominant lead story, two
illustrated secondary stories, and a briefs strip.

## Stories covered (researched from live headlines, 24 Nov 2026)

- **Lead — NATO sends AWACS to Poland** after three Russian Kh-101
  missiles landed on the alliance's eastern flank on Friday.
- **Ukraine sinks a Russian warship in Libya** — maritime drones sank a
  Russian corvette in a Libyan port on Sunday, a day after a drone hit a
  Russian-linked cargo ship in the Gulf of Finland.
- **Factory fire kills 24 in Indonesia** — at least 24 dead, around 30
  missing after a fire at a candy factory in Banten province.
- **Briefs** — COP31 talks collapse in Antalya (no fossil-fuel deal);
  Nvidia's Jensen Huang returns as CEO, shares surge 31% in a day;
  Verstappen wins the Las Vegas Grand Prix, Alcaraz takes the ATP Finals.

## Run

```sh
python3 main.py            # writes entry.png to $MAKEFUN_OUTPUT_DIR or /output
```

Output: one PNG, 1024×1024, under 1 MiB. `main()` verifies the gate
(format PNG, size ≤ 1024×1024, bytes ≤ 1 MiB) and exits non-zero on
failure.
