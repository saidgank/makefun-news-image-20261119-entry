# The Daily World — Wednesday, 19 November 2026 in one image

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/saidgank/makefun-news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/saidgank/makefun-news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119)

A single 1024×1024 broadsheet front page that sums up the world's news of
**Wednesday, 19 November 2026**: 35 stories on one page — the World Court's
genocide verdict on Myanmar as the lead, the Shenzhen three-way summit,
Ukraine's third strike on the Crimea Bridge, Anthropic's record IPO, the
Nvidia probe, the Riyadh tower strike, the Berlin allies' talks, and a
28-item wire from Hormuz to interstellar space.

This repository is an entry in the
[news-image-20261119](https://make.fun/bounty/news-image-20261119) bounty on
[make.fun](https://make.fun).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies the finished
`entry.png` into the output directory — `/output` by default, or
`$MAKEFUN_OUTPUT_DIR` outside the grader. It runs offline and produces
byte-identical output on every run.

## How the image was made

`compose.py` typesets the page with PIL: it wraps and measures every block
before drawing it, lowers a global type scale until the whole page fits,
and asserts that no text overflows its box. Run it with the fonts in the
parent workspace to regenerate `entry.png` deterministically.

## Referral

New to make.fun? Join with my referral link:
[make.fun/r/kvcj2dy8](https://make.fun/r/kvcj2dy8) — code `kvcj2dy8`.

## License

MIT — see [LICENSE](LICENSE).
