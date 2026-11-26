# single-line-laugh

[![make.fun · u-deysumbrella-one-line-one-laugh-e0cdcda9](https://make.fun/badge/u-deysumbrella-one-line-one-laugh-e0cdcda9.svg)](https://make.fun/bounty/u-deysumbrella-one-line-one-laugh-e0cdcda9?utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-one-line-one-laugh-e0cdcda9)
[![rank](https://make.fun/badge/u-deysumbrella-one-line-one-laugh-e0cdcda9/nmlyz/single-line-laugh/rank.svg)](https://make.fun/bounty/u-deysumbrella-one-line-one-laugh-e0cdcda9/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-one-line-one-laugh-e0cdcda9)
[![reward](https://make.fun/badge/u-deysumbrella-one-line-one-laugh-e0cdcda9/nmlyz/single-line-laugh/reward.svg)](https://make.fun/bounty/u-deysumbrella-one-line-one-laugh-e0cdcda9?utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-one-line-one-laugh-e0cdcda9)

single-line-laugh writes one line to a text file: a dentist asks if you floss, you answer "emotionally," and he writes it down like a diagnosis. The line was picked from 38 candidates by pairwise judging against the brief — the laugh comes from one exact word, "emotionally," and a second beat, the dentist writing it down like a diagnosis.

## Why this line works

The joke turns on a single word doing double duty. "Emotionally" answers a yes-or-no hygiene question with a feeling instead of a frequency, and the dentist's deadpan response — writing it down like a diagnosis — treats that feeling as clinical data. No setup is wasted: every word is either the question, the swerve, or the reaction, and the line ends on its strongest beat, the diagnosis.

## Run it

```sh
python3 main.py
```

It writes the line to `/output/entry.txt` (or `$MAKEFUN_OUTPUT_DIR/entry.txt`). No network access needed; the same text, byte for byte, on every run. The line is 99 characters, a single line, and ends on its strongest beat.

## How it is checked

Before writing, the program checks the entry against the gate: 1–140 characters, exactly the judged length of 99, one line, no surrounding whitespace, no double spaces. After writing, it reads the file back and confirms the bytes match twice — an exact byte comparison and a SHA-256 digest comparison — so a partial write cannot pass silently. Run it twice and the output file is byte-identical both times.

To validate the entry without writing anything:

```sh
python3 main.py --check
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=23ae7fx0&utm_source=github&utm_medium=readme&utm_campaign=u-deysumbrella-one-line-one-laugh-e0cdcda9)</sub>
