import json
from urllib import request
from pathlib import Path
from typing import Any, Tuple, List


class UaSquadDataset:

    _data = 'https://github.com/fido-ai/ua-datasets/releases/download/v0.0.1/ua_squad_dataset.json'

    def __init__(self, root: str, download: bool = True) -> None:
        """ Ukrainian Stanford Question Answering Dataset

        Args:
            root (:obj: `str`): Root directory where data will be stored
            download (:obj: `bool`, optional): Whether to download data to the root directory. If the data
            already exists, it will not be downloaded again

        """
        self.data_link = self._data
        self.root = Path(root)
        self.file_name = f'ua_squad_dataset.json'
        self.dataset_path = self.root / self.file_name

        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError('Dataset not found. ' +
                               'You can use download=True to download it')

        self._questions, self._contexts, self._answers = UaSquadDataset.parse(
            self.dataset_path)

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

        text = request.urlopen(self._data).read().decode('utf8')
        with open(self.dataset_path, 'w', encoding='utf8') as f:
            f.write(text)

    @staticmethod
    def parse(file_path: str) -> Tuple[List[Any], List[Any], List[Any]]:
        questions, contexts, answers = list(), list(), list()

        with open(file_path, 'r', encoding='utf8') as file:
            json_obj = json.load(file)

        for qca in json_obj:
            questions.append(qca['Question'])
            contexts.append(qca['Context'])
            answers.append(qca['Answer'])

        return questions, contexts, answers

    def __getitem__(self, idx: int) -> Tuple[Any, Any, Any]:
        question = self._questions[idx]
        context = self._contexts[idx]
        answer = self._answers[idx]
        return question, context, answer

    def __len__(self) -> int:
        return len(self._questions)

    def _check_exists(self) -> bool:
        return self.dataset_path.exists()
