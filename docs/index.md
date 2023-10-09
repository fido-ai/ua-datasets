## UA-datasets in a nutshell
__UA-datasets__ is a collection of Ukrainian language datasets. Our aim is to build a benchmark for research related to 
natural language processing in Ukrainian.

This library is provided by FIdo.ai (machine learning research division of the non-profit student's organization
[FIdo](https://www.facebook.com/fido.naukma/), National University of Kyiv-Mohyla Academy) for research purposes.

## Installation
The library can be installed from PyPi in your virtual environment (e.g. venv, conda env)
```python
pip install ua_datasets
```

## Quick example
```python
from ua_datasets import UaSquadDataset

qa_dataset = UaSquadDataset("data/", download=True)

for question, context, answer in qa_dataset:
    print("Question: " + question)
    print("Context: " + context)
    print("Answer: " + answer)
```


## Citation
If you found this library useful in academic research, please cite:

```bibtex
@software{ua_datasets_2021,
  author = {Ivanyuk-Skulskiy, Bogdan and Zaliznyi, Anton and
   Reshetar, Oleksand and Protsyk, Oleksiy and Romanchuk, Bohdan and
   Shpihanovych, Vladyslav},
  month = oct,
  title = {ua_datasets: a collection of Ukrainian language datasets},
  url = {https://github.com/fido-ai/ua-datasets},
  version = {0.0.1},
  year = {2021}
}
```

(Also consider starring the project [on GitHub](https://github.com/fido-ai/ua-datasets)!)
