# Ukrainian News

## Dataset Summary

Ukrainian News is a collection of more than 150 thousand news articles, gathered from more than 20 news resources. Dataset samples are divided into 5 categories: `політика`, `спорт`, `новини`, `бізнес`, `технології`. The dataset is provided by the non-profit student's organization FIdo.ai (machine learning research division of [FIdo](https://www.facebook.com/fido.naukma/), National University of Kyiv-Mohyla Academy) for research purposes in data mining (classification, clustering, keywords extraction, etc.)

Dataset development is still __in progress__


```python
from ua_datasets import NewsClassificationDataset

train_data = NewsClassificationDataset(root='data/', split='train', return_tags=True)
test_data = NewsClassificationDataset(root='data/', split='test', return_tags=True)

for item in train_data:
    title, text, tags, target = item
    print(title, text, tags, target)

for item in test_data:
    title, text, tags, target = item
    print(title, text, tags, target)

```

## Dataset Structure
__Parameters__: </br>
- `root` : Directory path
- `download`: Whether to download data
- `split`: Which split of the data to load (train or test)
- `return_tags`: Whether to return text keywords

----- 
 - Train :
    - File size: 324 MB
    - Number of samples: 120417
    <details> 
    <summary>Target distribution</summary>
 
        `політика` : 40364 (33.5%)
        `спорт` : 40364 (33.5%)
        `новини` : 40364 (33.5%)
        `бізнес` : 40364 (33.5%)
        `технології` : 40364 (33.5%)
    </details>
 - Test file size: 
    - File size: 81 MB
    - Number of samples: 30105
    <details> 
    <summary>Target distribution</summary>
 
        `політика` : 40364 (33.5%)
        `спорт` : 40364 (33.5%)
        `новини` : 40364 (33.5%)
        `бізнес` : 40364 (33.5%)
        `технології` : 40364 (33.5%)
    </details>

An example of 'train' sample looks as following:

```
{
  "title" : 'На Донеччині зафіксували сьомий випадок коронавірусу',
  "text" : 'Про це повідомив голова Донецької ОДА Павло Кириленко в Facebook ...,
  "tags" : ['Донецька область', 'COVID-19', 'Новини'],
  "target" : 'новини'
 }
```

