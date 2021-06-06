import json
from pathlib import Path
from typing import Any, Tuple, List

import gdown


# Ukrainian Stanford Question Answering Dataset
class UaSquadDataset:
    _data = 'https://drive.google.com/uc?id=1nws0WN6kOivvpt8biAn1vEfRIzIrx0B9'

    def __init__(self, root: str, download: bool = True) -> None:
        self.data_link = self._data
        self.root = Path(root)
        self.file_name = f'ua_squad_dataset.json'
        self.dataset_path = self.root / self.file_name

        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError('Dataset not found. ' +
                               'You can use download=True to download it')

        self._questions, self._contexts, self._answers = UaSquadDataset.parse(self.dataset_path)

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

        gdown.download(self.data_link, str(self.dataset_path), quiet=False)

    @staticmethod
    def parse(file_path) -> Tuple[List[Any], List[Any], List[Any]]:
        questions, contexts, answers = list(), list(), list()

        with open(file_path, 'r', encoding='utf8') as file:
            json_obj = json.load(file)

        for qca in json_obj:
            questions.append(qca['Question'])
            contexts.append(qca['Context'])
            answers.append(qca['Answer'])

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
