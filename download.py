#!/usr/bin/env python3
"""Fetch data from the upstream HF dataset futo-org/swipe.futo.org.

The full dataset is ~6.87 GB and lives on Hugging Face, not in this repo.
Use --sample to peek without downloading, or pull specific files on demand.

    pip install huggingface_hub datasets

Examples:
    python download.py --sample
    python download.py --config swipe-1 --split train --out ./data
    python download.py --all --out ./data        # full ~6.87 GB snapshot
"""
import argparse
import sys

REPO = "futo-org/swipe.futo.org"

CONFIG_FILES = {
    "swipe-1": {"train": "train.jsonl", "dev": "dev.jsonl", "test": "test.jsonl"},
    "swipe-2": {"train": "swipe-2/swipe2.jsonl"},
    "swipe-3": {"train": "swipe-3/swipe3.jsonl"},
    "swipe-4": {"train": "swipe-4/swipe4.jsonl"},
    "swipe-5": {"train": "swipe-5/swipe5.jsonl"},
}


def sample(n: int) -> None:
    """Stream the first n records of swipe-1/train without a full download."""
    from datasets import load_dataset

    ds = load_dataset(REPO, "swipe-1", split="train", streaming=True)
    for i, row in zip(range(n), ds):
        pts = row.get("data", [])
        print(f"[{i}] word={row['word']!r} points={len(pts)} session={row['session'][:18]}…")


def pull_file(config: str, split: str, out: str) -> None:
    from huggingface_hub import hf_hub_download

    rel = CONFIG_FILES[config][split]
    path = hf_hub_download(repo_id=REPO, filename=rel, repo_type="dataset", local_dir=out)
    print(f"downloaded {rel} -> {path}")


def pull_all(out: str) -> None:
    from huggingface_hub import snapshot_download

    path = snapshot_download(repo_id=REPO, repo_type="dataset", local_dir=out)
    print(f"snapshot -> {path}  (~6.87 GB)")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sample", action="store_true", help="stream a few records, no big download")
    p.add_argument("--n", type=int, default=5, help="how many records for --sample")
    p.add_argument("--config", choices=list(CONFIG_FILES), help="config to pull")
    p.add_argument("--split", default="train", help="split within the config")
    p.add_argument("--all", action="store_true", help="full snapshot (~6.87 GB)")
    p.add_argument("--out", default="./data", help="output dir for downloads")
    a = p.parse_args()

    if a.sample:
        sample(a.n)
    elif a.all:
        pull_all(a.out)
    elif a.config:
        pull_file(a.config, a.split, a.out)
    else:
        p.print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
