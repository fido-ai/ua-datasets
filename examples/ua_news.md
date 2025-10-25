# UA-News

## Dataset Summary

Ukrainian News is a collection of more than 150 thousand news articles, gathered from more than 20 news resources. Dataset samples are divided into 5 categories: `політика`, `спорт`, `новини`, `бізнес`, `технології`. The dataset is provided by the non-profit student's organization FIdo.ai (machine learning research division of [FIdo](https://www.facebook.com/fido.naukma/), National University of Kyiv-Mohyla Academy) for research purposes in data mining (classification, clustering, keywords extraction, etc.).

Dataset development is still **in progress**

## Dataset Structure

__Parameters__:

- `root` : Directory path

- `download`: Whether to download data

- `split`: Which split of the data to load (train or test)

- `return_tags`: Whether to return text keywords

__Splits__:

- Train :
    - File size: 324 MB
    - Number of samples: 120417
    - Target distribution

        `політика` : 40364 (33.5%)

        `спорт` : 40364 (33.5%)

        `новини` : 40364 (33.5%)

        `бізнес` : 40364 (33.5%)

        `технології` : 40364 (33.5%)

 - Test:
    - File size: 81 MB
    - Number of samples: 30105
    - Target distribution

        `політика` : 40364 (33.5%)

        `спорт` : 40364 (33.5%)

        `новини` : 40364 (33.5%)

        `бізнес` : 40364 (33.5%)

        `технології` : 40364 (33.5%)


__Data sample__
```
{
  "title" : 'На Донеччині зафіксували сьомий випадок коронавірусу',
  "text" : 'Про це повідомив голова Донецької ОДА Павло Кириленко в Facebook ...,
  "tags" : ['Донецька область', 'COVID-19', 'Новини'],
  "target" : 'новини'
 }
```

## Example of usage

### Our API

```python
from ua_datasets import NewsClassificationDataset

train_data = NewsClassificationDataset(root='data/', split='train', return_tags=True)

for title, text, tags, target in train_data:
    print(title, text, tags, target)
```

### Hugging Face 🤗 API

```python
from datasets import load_dataset

dataset = load_dataset("FIdo-AI/ua-news")

for item in dataset["train"]:
    title, text, tags, target = item["title"], item["text"], item["tags"], item["target"]
    print("Title: " + title)
    print("Text: " + text)
    print("Tags: " + tags)
    print("Target: " + target)
```
