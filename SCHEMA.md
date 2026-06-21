# Data format

Source: [`futo-org/swipe.futo.org`](https://huggingface.co/datasets/futo-org/swipe.futo.org).
Every file is **JSON Lines** — one JSON object per line, one swiped word per object.

## Record

```jsonc
{
  "id": 65,                         // integer, sequential within the file
  "session": "anon-session-6f52...",// anonymous session UUID (one volunteer sitting)
  "timestamp": 1724390287154,       // epoch ms, when the record was saved
  "word": "The",                    // TARGET word the user was asked to swipe (the label)
  "canvas_width": 422,              // keyboard render width in CSS px
  "canvas_height": 170.3125,        // keyboard render height in CSS px
  "orientation": "portrait-primary",// device orientation during capture
  "data": [                         // the swipe trajectory, time-ordered
    { "t": 1724390286378, "x": 0.4502, "y": 0.1824 },
    { "t": 1724390286507, "x": 0.4786, "y": 0.2177 },
    ...
  ]
}
```

### `data` points
- `t` — epoch ms timestamp of the touch sample. Intervals are irregular
  (~10–50 ms); use deltas for velocity, not a fixed rate.
- `x` — horizontal position, **normalized `[0,1]`** as a fraction of `canvas_width`.
- `y` — vertical position, **normalized `[0,1]`** as a fraction of `canvas_height`.

The first `data[].t` is typically *earlier* than the top-level `timestamp`
(touch happens before the record is committed).

## Notes / gotchas
- Users could retry or skip hard words, so a sentence's words may have gaps —
  records are per-word, not per-sentence, and `session` is the only link between
  words from the same sitting.
- `word` preserves original casing/punctuation as presented (e.g. `"The"`,
  `"Brahmas"`). Normalize before using as a label if you want lowercase.
- `canvas_width`/`canvas_height` vary slightly by device/run (422 vs 426 …).
  Because `x`,`y` are already normalized, you usually don't need the raw px,
  but the aspect ratio matters when comparing to the layout.

## Layout — `layouts/qwerty.json`

```jsonc
{
  "name": "qwerty",
  "letters": "abcdefghijklmnopqrstuvwxyz",
  "keys": [
    { "letter": "a", "cx": 0.1004, "cy": 0.5,    "rx": 0.05, "ry": 0.1666 },
    { "letter": "b", "cx": 0.6004, "cy": 0.8333, "rx": 0.05, "ry": 0.1666 },
    ...
  ]
}
```

- `cx`,`cy` — key center, normalized `[0,1]` in the **same space** as swipe
  `x`,`y`. Three rows: `cy ≈ 0.166` (top, qwertyuiop), `0.5` (middle, asdfghjkl),
  `0.833` (bottom, zxcvbnm).
- `rx`,`ry` — half-width / half-height of the key box. A point is "inside" key
  `k` if `|x-cx| ≤ rx` and `|y-cy| ≤ ry`; otherwise assign by nearest center.

### Reconstructing letters from a swipe (baseline)
1. For each `data` point, find the key whose box contains it, else nearest center.
2. Collapse consecutive duplicates → a candidate key sequence.
3. The intended word's letters are a subsequence of that key sequence (a glide
   path crosses non-target keys in transit), so decoding is a sequence-matching /
   language-model problem, not exact equality. `word` is the ground-truth target
   for training/eval.
