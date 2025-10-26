# UA-SQuAD

## Dataset Summary

Ukrainian version of [Stanford Question Answering Dataset](https://rajpurkar.github.io/SQuAD-explorer/) that includes context, questions and corresponding answers. Current version of the datasets consists of 13 859 samples. Dataset development is still **in progress**.

!!! Info
    Number of samples: 13 859
    Number of questions without answers: 2 927
    File size: 17.1 MB

### Data sample (HF-style)

```json
{
    "id": "3d9f1c2e7a4b1f20",
    "title": "DONDA",
    "context": "5 січня 2012 року Вест оголосив про створення компанії ...",
    "question": "Якою була мета нової творчої компанії DONDA, створеної Каньє?",
    "answers": {"text": ["виготовлення продуктів та поширення досвіду, які люди хочуть отримати й можуть собі дозволити"], "answer_start": [123]},
    "is_impossible": false
}
```

## Example of usage

### Python API (HF-style examples)

```python
from ua_datasets import UaSquadDataset

qa_dataset = UaSquadDataset("data/", split="train", download=True)

for ex in qa_dataset:  # each ex is a dict
    print("Question:", ex["question"]) 
    print("Answers:", ex["answers"]["text"])  # list (may be empty if is_impossible)
    if ex.get("is_impossible"):
        print("(No answer — impossible question)")
    break
```

### Optional: DatasetDict helper (no external Hub required)

If you have the optional `datasets` library installed, you can build a local `DatasetDict`
using the in-package helper (this does NOT call the Hugging Face Hub API if the JSON
files are already cached locally):

```python
from ua_datasets.question_answering.uasquad_question_answering import load_ua_squad_v2

dd = load_ua_squad_v2(root="data/ua_squad", download=True)  # returns a datasets.DatasetDict
row = dd["train"][0]
print(row["question"], row["answers"]["text"], row["is_impossible"])
```

If `datasets` is not installed this helper will raise a `RuntimeError`; install it with:

```bash
uv add datasets  # or: uv add datasets
```

If you don't need a Hugging Face `Dataset`, stick with the pure-Python iteration example above.

### Migration Note

Legacy versions exposed `(question, context, answer)` tuples and keys `Question/Context/Answer` in raw JSON; these have been replaced by the standard SQuAD v2 schema shown above. Update loops to: `for ex in ds: ex['question'], ex['answers']['text']`.

## We thank our contributors

Kyrpa Mykyta, Ivan Makarov, Tepla Sofiia, Chudnovska Daria, Fedenko Anna, Zaremba Anna, Krainia Daria, Budenkova Marharyta, Butunaieva Diana, Stanislavska Kateryna, Samorodova Sofiia, Martynyshyn Yuliia, Matviienko Iryna, Bezruka Anastasiia, Mostova Mariia, Stepanenko Liubomyr, Bondarenko Vitaliia, Fedorenko Polina, Sydorka Bohdana, Okhrimenko Mykhailo, Hryha Ruslana, Ustynova Olha, Kondratenko Dmytro, Chornomorets Yelyzaveta, Heresh Yuliia, Hynku Anna-Mariia, Tarasiuk Kateryna, Demian Biliavskyi, Piatushko Ruslana, Pakholchak Kateryna, Barabukha Mariia, Poltorak Yuliia, Yuliia Fedor, Usenko Viktoriia, Balanchuk Yana, Kramchenkov Dmytro, Yatsiuk Mariia, Melnyk Tetiana, Biloverbenko Illia, Boiko Khrystyna, Steshenko Kateryna, Korcheva Anna, Syzonenko Anastasiia, Malysheva Alina, Yaroslava Kushcheva, Valeriia Denysenko
