# Ukrainian News

## Dataset Summary

Ukrainian News is a collection of more than 150 thousands news articles, gathered from more than 20 news resources. Dataset samples are divided into 5 categories: `політика`, `спорт`, `новини`, `бізнес`, `технології`. The dataset is provided by the non-profit student's organisation FIdo.ai (machine learning research division of [FIdo](https://www.facebook.com/fido.naukma/), National University of Kyiv-Mohyla Academy) for research purposes in data mining (classification, clustering, keywords extraction, etc.)

Dataset development is still in progress


## Dataset Structure

```python
from ua_datasets import NewsClassificationDataset
train_data = NewsClassificationDataset(root = 'data/', split = 'train', return_tags = True)
```

 - Train :
    - File size: 324 MB
    - Number of samples: 120417 
 - Test file size: 
    - File size: 81 MB
    - Number of samples: 30105

An example of 'train' looks as following:

```
{
  "title" : 'На Донеччині зафіксували сьомий випадок коронавірусу',
  "text" : 'Про це повідомив голова Донецької ОДА Павло Кириленко в Facebook ...,
  "tags" : ['Донецька область', 'COVID-19', 'Новини'],
  "target" : 'новини'
```

----- 
__Parameters__: </br>
- `root` : Directory path
- `download`: Whether to download data
- `split`: Which split of the data to load (train or test)
- `return_tags`: Whether to return text keywords

