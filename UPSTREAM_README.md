---
language:
- en
license: mit

configs:
- config_name: swipe-1
  data_files:
  - split: train
    path: train.jsonl
  - split: test
    path: test.jsonl
  - split: validation
    path: dev.jsonl

- config_name: swipe-2
  data_files:
  - split: train
    path: swipe-2/swipe2.jsonl

- config_name: swipe-3
  data_files:
  - split: train
    path: swipe-3/swipe3.jsonl


- config_name: swipe-4
  data_files:
  - split: train
    path: swipe-4/swipe4.jsonl


- config_name: swipe-5
  data_files:
  - split: train
    path: swipe-5/swipe5.jsonl
---
# Dataset Card for swipe.futo.org

This dataset contains multiple collection runs from the [swipe.futo.org](https://swipe.futo.org/) website. The QWERTY layout definition is provided [here](swipe-5/layouts/qwerty.json)

## Collection process

Users were able to volunteer to contribute to our dataset. After visiting the site on a mobile device, they were given words to swipe as part of a pre-defined sentence set.

Users were allowed to go back to retry words, or skip words if they're too hard. Because of this there may be gaps where some words are missing from the data even though the rest of the sentence is there.

# swipe-1

There are around 1 million swipes overall.

These are provided in `train.jsonl`, `test.jsonl`, `dev.jsonl` splits in the root of the repository.

The sentences are from Wikipedia, taken from the wiki txt files on
[Mozilla Common Voice](https://github.com/common-voice/common-voice/tree/main/server/data/en). 

Around 5% of swipes were filtered out for failing to meet validity checks (target and swipe word didn't match, etc).

# swipe-2..5

There were four smaller collection runs after the first, each detailed in their subdirectory's README. These runs are intended to cover some of the shortcomings of the main dataset.
* [swipe-2](swipe-2/README.md) - 28095 swipes
* [swipe-3](swipe-3/README.md) - 38228 swipes
* [swipe-4](swipe-4/README.md) - 50300 swipes
* [swipe-5](swipe-5/README.md) - 59247 swipes

We didn't make any significant marketing push for these, so there may be a stronger selection bias of people who chose to contribute to these sets compared to the main set (more techy users or existing FUTO Keyboard users).

Each subdirectory contains a jsonl file containing the data.

These are much smaller than the initial run which collected over a million swipes. As a result, we don't release train/test/dev splits but just provide one jsonl file per collection.

The data provided is completely unfiltered and contains some percent of invalid data. You can filter it yourself by the `distance` column to remove most invalid data, but this can also remove some valid data.