
<p align="center">
  <img src="https://github.com/fido-ai/ua-datasets/blob/main/imgs/NaUKMA.png" width="350" title="hover text" alt="NaUKMA FIdo Logo">
</p>

<h1 align="center">
    ua_datasets
</h1>

[![PyPI version](https://img.shields.io/pypi/v/ua-datasets.svg)](https://pypi.org/project/ua-datasets/)
[![Python versions](https://img.shields.io/pypi/pyversions/ua-datasets.svg)](https://pypi.org/project/ua-datasets/)
[![License](https://img.shields.io/pypi/l/ua-datasets.svg)](https://github.com/fido-ai/ua-datasets/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/ua-datasets)](https://pepy.tech/project/ua-datasets)

[![Build CI](https://github.com/fido-ai/ua-datasets/actions/workflows/ci.yml/badge.svg)](https://github.com/fido-ai/ua-datasets/actions/workflows/ci.yml)
[![Code size](https://img.shields.io/github/languages/code-size/fido-ai/ua-datasets)](https://github.com/fido-ai/ua-datasets)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blue.svg)](http://mypy-lang.org/)

[**UA-datasets**](https://fido-ai.github.io/ua-datasets/) provides ready-to-use Ukrainian NLP benchmark datasets with a **single, lightweight Python API**.

> Fast access to Question Answering, News Classification, and POS Tagging corpora — with automatic download, caching, and consistent iteration.

### Why use this library?

- **Unified API**: All datasets expose `len(ds)`, indexing, iteration, and simple frequency helpers.
- **Robust downloads**: Automatic retries, integrity guards, and filename fallbacks for legacy splits.
- **Zero heavy deps**: Pure Python + standard library (core loaders) for quick startup.
- **Repro friendly**: Validation split for UA-SQuAD; classification CSV parsing with resilience to minor format drift.
- **Tooling ready**: Works seamlessly with ruff, mypy, pytest, and uv-based workflows.


_Maintained by the FIdo.ai research group (National University of Kyiv-Mohyla Academy)._

## Minimal Example

```python
# Assumes `uv` workspace already synced with `uv sync` and project installed.

from pathlib import Path
from ua_datasets.question_answering import UaSquadDataset
from ua_datasets.text_classification import NewsClassificationDataset
from ua_datasets.token_classification import MovaInstitutePOSDataset

# Question Answering (first HF-style example dict)
qa = UaSquadDataset(root=Path("./data/ua_squad"), split="train", download=True)
print("QA examples:", len(qa))
example = qa[0]
print(example.keys())  # id, title, context, question, answers, is_impossible
print(example["question"], "->", example["answers"]["text"])  # list of accepted answers

# News Classification
news = NewsClassificationDataset(root=Path("./data/ua_news"), split="train", download=True)
title, text, target, tags = news[0]
print("Label count:", len(news.labels), "First label:", target)

# Part-of-Speech Tagging
pos = MovaInstitutePOSDataset(root=Path("./data/mova_pos"), download=True)
tokens, tags = pos[0]
print(tokens[:8], tags[:8])
```

For development commands see the Installation section below.

## Installation

Choose one of the following methods.

### 1. Using uv (recommended)

Add to an existing project:

```bash
uv add ua-datasets
```


<!-- markdownlint-disable MD033 -->
<details>
<summary><strong>2. Using pip (PyPI)</strong></summary>

```bash
# install
pip install ua_datasets
# upgrade
pip install -U ua_datasets
```

 </details>

<details>
<summary><strong>3. From source (editable install)</strong></summary>

```bash
git clone https://github.com/fido-ai/ua-datasets.git
cd ua-datasets
pip install -e .[dev]  # if you later define optional dev extras
```

Or with uv (editable semantics via local path):

```bash
git clone https://github.com/fido-ai/ua-datasets.git
cd ua-datasets
uv sync --dev
```

</details>
<!-- markdownlint-enable MD033 -->

## Latest Updates

| Date | Highlights |
|------|------------|
| 25-10-2025 | Added validation split for UA-SQuAD and updated package code. |
| 05-07-2022 | Added HuggingFace API for UA-SQuAD (Q&A) and UA-News (Text Classification). |


## Available Datasets

| Task | Dataset | Import Class | Splits | Notes |
|------|---------|--------------|--------|-------|
| Question Answering | UA-SQuAD | `UaSquadDataset` | `train`, `val` | SQuAD v2-style examples (`is_impossible`, multi answers); iteration yields dicts |
| Text Classification | UA-News | `NewsClassificationDataset` | `train`, `test` | CSV (title, text, target[, tags]); optional tag parsing |
| Token Classification | Mova Institute POS | `MovaInstitutePOSDataset` | (single corpus) | CoNLL-U like POS tagging; yields (tokens, tags) per sentence |

## Contribution

In case you are willing to contribute (update any part of the library, add your dataset) do not hesitate to connect through [GitHub Issue](https://github.com/fido-ai/ua-datasets/issues/new/choose). Thanks in advance for your contribution!

## Citation

```bibtex
@software{ua_datasets_2021,
  author = {Ivanyuk-Skulskiy, Bogdan and Zaliznyi, Anton and Reshetar, Oleksand and Protsyk, Oleksiy and Romanchuk, Bohdan and Shpihanovych, Vladyslav},
  month = oct,
  title = {ua_datasets: a collection of Ukrainian language datasets},
  url = {https://github.com/fido-ai/ua-datasets},
  version = {1.0.0},
  year = {2021}
}
```
