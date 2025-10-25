# UA-datasets

> Unified, lightweight access to Ukrainian NLP benchmark datasets (QA, Text Classification, POS tagging) with automatic download, caching and consistent iteration.

**UA-datasets** is maintained by FIdo.ai (machine learning research division of the non-profit student organization [FIdo](https://www.facebook.com/fido.naukma/) at the National University of Kyiv-Mohyla Academy) for research purposes.

---

## Features at a glance

| Capability | Description |
|------------|-------------|
| Unified API | `len(ds)`, indexing, iteration across all datasets |
| Resilient downloads | Retries, integrity / basic validation, fallback filenames (UA-SQuAD val) |
| Minimal deps | Core loaders rely only on the standard library |
| Consistent samples | Typed tuples: QA `(question, context, answer)`, Classification `(title, text, label, tags?)`, POS `(tokens, tags)` |
| Frequency helpers | Simple methods for label/answer frequency analysis |
| Ready for tooling | Works seamlessly with `uv`, `ruff`, `mypy`, `pytest`, `pre-commit` |

---

## Available Datasets

| Task | Dataset | Class | Splits | Notes |
|------|---------|-------|--------|-------|
| Question Answering | UA-SQuAD | `UaSquadDataset` | `train`, `val` | SQuAD-style JSON; legacy val filename fallbacks |
| Text Classification | UA-News | `NewsClassificationDataset` | `train`, `test` | CSV (title,text,target[,tags]); optional tag parsing |
| POS Tagging | Mova Institute POS | `MovaInstitutePOSDataset` | corpus | CoNLL-U like format; yields (tokens, tags) |

---

## Quick Start

```python
from pathlib import Path
from ua_datasets.question_answering import UaSquadDataset

ds = UaSquadDataset(root=Path("./data/ua_squad"), split="train", download=True)
print(f"Samples: {len(ds)}")
question, context, answer = ds[0]
print(question)
print(answer)
```

Text classification:

```python
from ua_datasets.text_classification import NewsClassificationDataset
news = NewsClassificationDataset(root=Path("./data/ua_news"), split="train", download=True)
title, text, label, tags = news[0]
```

POS tagging:
 
```python
from ua_datasets.token_classification import MovaInstitutePOSDataset
pos = MovaInstitutePOSDataset(root=Path("./data/mova_pos"), download=True)
tokens, tags = pos[0]
```

---

## Installation

Choose one method:

### Using `uv` (recommended)

```bash
uv add ua-datasets
```

### Via pip

```bash
pip install ua_datasets
```

### From source (editable)

```bash
git clone https://github.com/fido-ai/ua-datasets.git
cd ua-datasets
pip install -e .
```

---

## Benchmarks & Acknowledgements

- **Benchmarks:** See [Benchmarks](further_details/benchmarks.md) for leaderboard scaffolding.
- **Acknowledgements:** See [Acknowledgements](further_details/acknowledgements.md) for dataset contributors.

---

## Citation

If you found this library useful in academic research, please cite:

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

⭐ Consider starring the project on [GitHub](https://github.com/fido-ai/ua-datasets) to support visibility.

