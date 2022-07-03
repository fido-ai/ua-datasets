# UA-SQuAD
Ukrainian version of [Stanford Question Answering Dataset](https://rajpurkar.github.io/SQuAD-explorer/)

Dataset development is still **in progress**

## Demo
### Using our API
```python
from ua_datasets import UaSquadDataset

qa_dataset = UaSquadDataset("data/")
for qca in qa_dataset:
    question, context, answer = qca
    print("Question: " + question)
    print("Context: " + context)
    print("Answer: " + answer)
```
### Using Hugging Face 🤗 API
```python
from datasets import load_dataset

dataset = load_dataset("FIdo-AI/ua-squad", field="data")
for qca in dataset['train']:
    question, context, answer = qca['Question'], qca['Context'], qca['Answer']
    print("Question: " + question)
    print("Context: " + context)
    print("Answer: " + answer)
```

## Dataset Structure
__Parameters__:</br>
- `root` : Directory path
- `download`: Whether to download data
 
__Data sample__
```json
{
    "Question": "Якою була мета нової творчої компанії DONDA, створеної Каньє?",
    "Context": "5 січня 2012 року Вест оголосив про створення компанії ...",
    "Answer": "виготовлення продуктів та поширення досвіду, які люди хочуть отримати й можуть собі дозволити"
}
```

## General info
Number of samples: 13 859  
Number of questions without answers: 2 927  
File size: 17.1 MB  


## Contributors
Kyrpa Mykyta, Ivan Makarov, Tepla Sofiia, Chudnovska Daria, Fedenko Anna, Zaremba Anna, Krainia Daria, Budenkova Marharyta, 
Butunaieva Diana, Stanislavska Kateryna, Samorodova Sofiia, Martynyshyn Yuliia, Matviienko Iryna, Bezruka Anastasiia, 
Mostova Mariia, Stepanenko Liubomyr, Bondarenko Vitaliia, Fedorenko Polina, Sydorka Bohdana, Okhrimenko Mykhailo, 
Hryha Ruslana, Ustynova Olha, Kondratenko Dmytro, Chornomorets Yelyzaveta, Heresh Yuliia, Hynku Anna-Mariia, Tarasiuk Kateryna, 
Demian Biliavskyi, Piatushko Ruslana, Pakholchak Kateryna, Barabukha Mariia, Poltorak Yuliia, Yuliia Fedor, Usenko Viktoriia, 
Balanchuk Yana, Kramchenkov Dmytro, Yatsiuk Mariia, Melnyk Tetiana, Biloverbenko Illia, Boiko Khrystyna, Steshenko Kateryna, 
Korcheva Anna, Syzonenko Anastasiia, Malysheva Alina, Yaroslava Kushcheva, Valeriia Denysenko
