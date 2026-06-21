# swipe.futo.org — Claude-accessible working copy

A lightweight, version-controlled companion to the Hugging Face dataset
**[`futo-org/swipe.futo.org`](https://huggingface.co/datasets/futo-org/swipe.futo.org)**
(MIT, ~1M+ swipe samples, 6.87 GB on HF).

The full dataset is **not** stored here — 7 of its files exceed GitHub's 100 MB
per-file limit (the largest, `train.jsonl`, is 5.16 GB). Instead this repo holds
what you need to understand and work with the data:

| Path | What it is |
|---|---|
| `SCHEMA.md` | Full record format + how to decode swipes into letters |
| `samples/*.jsonl` | Real records from each split/config (first N lines) |
| `layouts/qwerty.json` | Normalized QWERTY key geometry (maps x,y → keys) |
| `download.py` | Pull the full dataset (or stream it) from HF on demand |
| `UPSTREAM_README.md` | The original dataset card from HF |

## What the data is

Volunteer-collected swipe (glide) typing traces from the
[swipe.futo.org](https://swipe.futo.org/) site. Each record is one word, swiped
on a mobile QWERTY keyboard, captured as a time-stamped path of normalized touch
points. Source sentences come from Wikipedia via Mozilla Common Voice.

- **swipe-1** — ~1M swipes, split into `train` / `dev` / `test`.
- **swipe-2 … swipe-5** — later collection runs (single `train` split each).

## Quick start

```bash
pip install huggingface_hub datasets
python download.py --sample        # stream a few records, no big download
python download.py --config swipe-1 --split train --out ./data   # full file
```

## Decoding a swipe (summary — see SCHEMA.md)

Each `data` point is `{t, x, y}` with `x`,`y` normalized to `[0,1]` over the
keyboard canvas. `layouts/qwerty.json` gives each key a center `(cx, cy)` and
half-extents `(rx, ry)` in the **same** normalized space, so the nearest key to
each point (or the sequence of keys the path passes through) reconstructs the
intended letters.
