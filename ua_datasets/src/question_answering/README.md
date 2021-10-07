# UA-SQuAD
Ukrainian version of [Stanford Question Answering Dataset](https://rajpurkar.github.io/SQuAD-explorer/)

Dataset development is still **in progress**

## Data Sample
```json
{
    "Question": "Якою була мета нової творчої компанії DONDA, створеної Каньє?",
    "Context": "5 січня 2012 року Вест оголосив про створення компанії для творчого контенту DONDA, названої на честь його покійної матері Донди Вест. Під час представлення Вест заявив, що компанія \"продовжить там, де зупинився Стів Джобс\"; DONDA діятиме як \"дизайнерська компанія, яка забезпечить мислителям творчий простір для реалізації своїх мрій та ідей\" з \"метою виготовлення продуктів та поширення досвіду, які люди хочуть отримати й можуть собі дозволити\". Вест, як відомо, мало говорить про діяльність компанії, відсутні як офіційний веб-сайт, так і представлення в соціальних мережах. Креативна філософія DONDA містить необхідність \"розміщувати творців у спільному просторі разом із подібними думками\", щоб \"спростити та естетично вдосконалити все, що ми бачимо, смакуємо, торкаємось та відчуваємо\". Сучасні критики відзначають незмінну мінімалістичну естетику, яка повторюється в багатьох творчих проектах DONDA.",
    "Answer": "виготовлення продуктів та поширення досвіду, які люди хочуть отримати й можуть собі дозволити"
}
```

## Stats
Number of samples: 13 859  
Number of questions without answers: 2 927  
File size: 17.1 MB  

## Usage Example
```python
# print all samples
from ua_datasets import UaSquadDataset

qa_dataset = UaSquadDataset(".")
for i in range(len(qa_dataset)):
    question, context, answer = qa_dataset[i]
    print("Question: " + question)
    print("Context: " + context)
    print("Answer: " + answer)
    print()
```


## Contributors
Kyrpa Mykyta, Ivan Makarov, Tepla Sofiia, Chudnovska Daria, Fedenko Anna, Zaremba Anna, Krainia Daria, Budenkova Marharyta, 
Butunaieva Diana, Stanislavska Kateryna, Samorodova Sofiia, Martynyshyn Yuliia, Matviienko Iryna, Bezruka Anastasiia, 
Mostova Mariia, Stepanenko Liubomyr, Bondarenko Vitaliia, Fedorenko Polina, Sydorka Bohdana, Okhrimenko Mykhailo, 
Hryha Ruslana, Ustynova Olha, Kondratenko Dmytro, Chornomorets Yelyzaveta, Heresh Yuliia, Hynku Anna-Mariia, Tarasiuk Kateryna, 
Demian Biliavskyi, Piatushko Ruslana, Pakholchak Kateryna, Barabukha Mariia, Poltorak Yuliia, Yuliia Fedor, Usenko Viktoriia, 
Balanchuk Yana, Kramchenkov Dmytro, Yatsiuk Mariia, Melnyk Tetiana, Biloverbenko Illia, Boiko Khrystyna, Steshenko Kateryna, 
Korcheva Anna, Syzonenko Anastasiia, Malysheva Alina, Yaroslava Kushcheva, Valeriia Denysenko
