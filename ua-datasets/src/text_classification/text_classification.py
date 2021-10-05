import csv
import pathlib
from typing import Any, Tuple, List

class NewsClassification:
	def __init__(self, split: str = 'train', return_tags: bool = False):
		""" News classification dataset

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
		
	def __getitem__(self, idx) -> Tuple[str]:
		title, text, tags, target = self._data[idx]
		if self.return_tags:
			tags = self._preprocess_tags(tags)
			return title, text, tags, target
		else:
			return title, text, target
	
	def _preprocess_tags(self, tags) -> List[str]:
		""" Text tags preprocessing """
		return [el for el in tags.split("|") if el != '']

	def __len__(self):
		""" Number of rows in the dataset """
		return len(self._data)

if __name__ == '__main__':
	data = NewsClassification(return_tags=True) 
	print(len(data))
	print(data[0])
	print(data.labels())

	data = NewsClassification(split='test')
	print(len(data))
	print(data.labels())
	