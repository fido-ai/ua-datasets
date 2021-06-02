from urllib import request
from pathlib import Path
import json
from typing import Any, Tuple, List


# Ukrainian Stanford Question Answering Dataset
class UaSquadDataset:
    _data_train = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json'
    _data_test = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json'

    def __init__(self, root: str, train: bool = True, download: bool = True) -> None:
        self.data_link = self._data_train if train else self._data_test
        self.root = Path(root)
        self.file_name = f'ua_squad_{"train" if train else "test"}_dataset.json'
        self.dataset_path = self.root / self.file_name

        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError('Dataset not found. ' +
                               'You can use download=True to download it')

        self._questions, self._contexts, self._answers = self.load_data(self.dataset_path)

    @property
    def answers(self) -> List[Any]:
        return self._answers

    @property
    def contexts(self) -> List[Any]:
        return self._contexts

    @property
    def questions(self) -> List[Any]:
        return self._questions

    def download(self) -> None:
        if self._check_exists():
            return

        self.root.mkdir(exist_ok=True)

        text = request.urlopen(self.data_link).read().decode('utf8')
        with open(self.dataset_path, 'w', encoding='utf8') as f:
            f.write(text)

    @staticmethod
    def load_data(file_path) -> Tuple[List[Any], List[Any], List[Any]]:
        questions, contexts, answers = list(), list(), list()

        with open(file_path, 'r', encoding='utf8') as file:
            json_obj = json.load(file)

        for topic in json_obj["data"]:
            for paragraph in topic["paragraphs"]:
                context = paragraph["context"]
                for qa in paragraph["qas"]:
                    question = qa["question"]
                    question_answers = qa["answers"]
                    if question_answers:
                        answer = question_answers[0]["text"]
                    else:
                        answer = None

                    questions.append(question)
                    contexts.append(context)
                    answers.append(answer)

        return questions, contexts, answers

    def __getitem__(self, idx) -> Tuple[Any, Any, Any]:
        question = self._questions[idx]
        context = self._contexts[idx]
        answer = self._answers[idx]
        return question, context, answer

    def __len__(self) -> int:
        return len(self._questions)

    def _check_exists(self) -> bool:
        return self.dataset_path.exists()
