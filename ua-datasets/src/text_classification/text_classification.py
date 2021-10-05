import csv
import pathlib
from typing import Any, Tuple, List

class NewsClassification:
	def __init__(self, split: str = 'train', return_keywords: bool = False):
		""" News classification dataset

		Args:
			split (:obj: `str`): Which split of the data to load (train or test)
			return_keywords (:obj: `bool`, optional): Whether to return text keywords 
			
		"""
		self.path = (pathlib.Path(__file__) / ".." / ".." / "..").resolve()
		self.return_keywords = return_keywords
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
		return set([row[-1] for row in self._data])
		#return set([row[-1] for row in self._data])
		
	def __getitem__(self, idx) -> Tuple[str]:
		title, text, tags, target = self._data[idx]
		if self.return_keywords:
			return title, text, tags, target
		else:
			return title, text, target
	
	def __len__(self):
		""" Number of rows in the dataset """
		return len(self._data)

if __name__ == '__main__':
	data = NewsClassification() 
	print(len(data))
	print(data.labels())

	data = NewsClassification(split='test')
	print(len(data))
	print(data.labels())
	