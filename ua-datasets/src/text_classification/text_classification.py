import csv
import pathlib
from typing import Tuple, List


class NewsClassificationDataset:
	def __init__(self, split: str = 'train', return_tags: bool = False):
		""" News Classification Dataset

		Args:
			split (:obj: `str`): Which split of the data to load (train or test)
			return_tags (:obj: `bool`, optional): Whether to return text keywords 
			
		"""
		self.path = (pathlib.Path(__file__) / ".." / ".." / "..").resolve()
		self.return_tags = return_tags
		self.split = split
		self._data = self._load_data()

	def _load_data(self) -> List[List[str]]:
		""" Load dataset """
		if self.split == 'train':
			data_path = self.path / 'data/text_classification/train.csv'
		elif self.split == 'test':
			data_path = self.path / 'data/text_classification/test.csv'
		else:
			raise NotImplementedError()

		file = open(data_path)
		csvreader = csv.reader(file)
		self.columns = next(csvreader)
		samples = list()
		for row in csvreader:
			samples.append(row)
		return samples

	def column_names(self) -> List[str]:
		""" Dataset column names """
		return self.columns

	def labels(self) -> List[str]:
		""" Target names """
		return set([row[self.columns.index('target')] for row in self._data])
		
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
	