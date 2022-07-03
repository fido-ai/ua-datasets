from urllib import request
from pathlib import Path
from typing import Any, Tuple, List


class MovaInstitutePOSDataset:

    data_file = 'https://lab.mova.institute/files/robochyi_tb.conllu.txt'

    def __init__(self, root: str, download: bool = True) -> None:
        self.root = Path(root)
        self.file_name = 'mova_institute_pos_dataset.txt'
        self.dataset_path = self.root / self.file_name

        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError(
                'Dataset not found.' +
                ' You can use download=True to download it'
            )

        self._samples, self._labels = self._load_data()

    @property
    def labels(self) -> List[Any]:
        return self._labels

    @property
    def data(self) -> List[Any]:
        return self._samples

    def _load_data(self) -> Tuple[List[Any], List[Any]]:
        samples, labels = list(), list()
        curr_sample, curr_label = list(), list()
        with open(self.dataset_path, 'r', encoding='utf8') as file:
            for line in file:
                if line[0].isdigit():
                    idx, word_sample, _, word_label, *_ = line.split('\t')
                    curr_sample.append(word_sample)
                    curr_label.append(word_label)
                elif line[0] == '\n':
                    samples.append(curr_sample)
                    labels.append(curr_label)
                    curr_sample, curr_label = list(), list()
        return samples, labels

    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        sample = self._samples[idx]
        label = self._labels[idx]
        return sample, label

    def __len__(self) -> int:
        return len(self._samples)

    def _check_exists(self) -> bool:
        return self.dataset_path.exists()

    def download(self) -> None:
        if self._check_exists():
            return

        self.root.mkdir(exist_ok=True)

        text = request.urlopen(self.data_file).read().decode('utf8')
        with open(self.dataset_path, 'w', encoding='utf8') as f:
            for line in text.split('\\n'):
                f.write(line + '\n')
