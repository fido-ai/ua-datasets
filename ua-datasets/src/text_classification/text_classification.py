import csv
import pathlib
from typing import Any, Tuple, List

class NewsClassification:
	def __init__(self, train: bool = True, return_keywords: bool = True):
		self.train = train
		self.return_keywords = return_keywords
		self.path = (pathlib.Path(__file__) / ".." / ".." / "..").resolve()
		self._data = self.load_data()
		
	def load_data(self):
		if self.train:
			data_path = self.path / 'data/text_classification/train.csv'
		else:
			data_path = self.path / 'data/text_classification/test.csv'
			
		file = open(data_path)
		csvreader = csv.reader(file)
		self.columns = next(csvreader)
		samples = list()
		for row in csvreader:
			samples.append(row)
		return samples
		
	def __getitem__(self, idx):
		title, text, tags, target = self._data[idx]
		if self.return_keywords:
			return title, text, tags, target
		else:
			return title, text, target
	
	def __len__(self):
		return len(self._data)

if __name__ == '__main__':
	data = NewsClassification() 
	print(len(data))

	data = NewsClassification(train=False)
	print(len(data))
	