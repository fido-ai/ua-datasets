import csv
import pathlib
from urllib import request
from typing import Tuple, List, Set


class NewsClassificationDataset:

    data_file = 'https://github.com/fido-ai/ua-datasets/releases/download/v0.0.1/'

    def __init__(
            self,
            root: str,
            download: bool = True,
            split: str = 'train',
            return_tags: bool = False):
        """ News Classification Dataset

        Args:
                root (:obj: `str`): Directory path
                download (:obj: `bool`): Whether to download data
                split (:obj: `str`): Which split of the data to load (train or test)
                return_tags (:obj: `bool`, optional): Whether to return text keywords

        """
        self.split = split
        self.return_tags = return_tags
        self.root = pathlib.Path(root)
        self.dataset_path = self.root / (self.split + '.csv')

        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError('Dataset not found.' +
                               ' You can use download=True to download it')

        self._data = self._load_data()

    def _check_exists(self) -> bool:
        return self.dataset_path.exists()

    def download(self) -> None:
        if self._check_exists():
            return

        self.root.mkdir(exist_ok=True)

        text = request.urlopen(
            self.data_file +
            self.split +
            '.csv').read().decode('utf8')
        with open(self.dataset_path, 'w', encoding='utf8') as f:
            for line in text.split('\\n'):
                f.write(line + '\n')

    def _load_data(self) -> List[List[str]]:
        """ Load dataset """
        file = open(self.dataset_path)
        csvreader = csv.reader(file)
        self._columns = next(csvreader)
        samples = list()
        prev = next(csvreader)
        for row in csvreader:
            yield prev
            prev = row
            samples.append(prev)
        return samples

    @property
    def column_names(self) -> List[str]:
        """ Dataset column names """
        return self._columns

    @property
    def labels(self) -> Set[str]:
        """ Target names """
        return set([row[self._columns.index('target')]
                    for row in self._data[:-1]])

    def __getitem__(self, idx: int) -> Tuple[str]:
        title, text, tags, target = self._data[idx]
        if self.return_tags:
            tags = self._preprocess_tags(tags)
            return title, text, tags, target
        else:
            return title, text, target

    @staticmethod
    def _preprocess_tags(tags: str) -> List[str]:
        """ Text tags preprocessing """
        return [el for el in tags.split("|") if el != '']

    def __len__(self) -> int:
        """ Number of rows in the dataset """
        return len(self._data)
