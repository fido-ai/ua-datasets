from urllib import request
from pathlib import Path
from typing import Any, Tuple, List


# Ukrainian Stanford Question Answering Dataset
class UaSquadDataset:

    _data = 'https://raw.githubusercontent.com/IronTony-Stark/ua-datasets-data/master/ua-squad.txt'

    def __init__(self, root: str, download: bool = True) -> None:
        self.data_link = self._data
        self.root = Path(root)
        self.file_name = f'ua_squad_dataset.txt'
        self.dataset_path = self.root / self.file_name

        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError('Dataset not found. ' +
                               'You can use download=True to download it')

        self._questions, self._contexts, self._answers = self.parse(self.dataset_path)

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
    def parse(file_path) -> Tuple[List[Any], List[Any], List[Any]]:
        questions, contexts, answers = list(), list(), list()

        with open(file_path, 'r', encoding='utf8') as file:
            text = file.read()

        was_question = False
        for line in text.splitlines():
            if line.startswith("Запитання: "):
                if was_question:
                    answers.append("")
                was_question = True

                line = line[len("Запитання: "):]
                questions.append(line)
            elif line.startswith("Питання: "):
                if was_question:
                    answers.append("")
                was_question = True

                line = line[len("Питання: "):]
                questions.append(line)
            elif line.startswith("Відповідь: "):
                was_question = False

                line = line[len("Відповідь: "):]
                answers.append(line)
            elif line.startswith("Контекст: "):
                if was_question:
                    answers.append("")
                was_question = False

                line = line[len("Контекст: "):]
                while len(contexts) != len(questions):
                    contexts.append(line)
            elif line.startswith("Назва: ") or not line:
                pass
            else:
                print("[WARN] Invalid dataset line format: " + line)

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
