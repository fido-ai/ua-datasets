import json
from pathlib import Path
from typing import Any, Tuple, List

class ClassificationDataset:
    def __init__(self, root: str, download: bool = False, return_tags: bool = False) -> None:
        self.root = Path(root)
        self.return_tags = return_tags
        self.file_name = 'cl_data_Anton.json'
        self.dataset_path = self.root / self.file_name
        
        if download:
            self.download()
        
        if not self._check_exists():
            raise RuntimeError('Dataset not found. ' +
                                'You can use download=True to download it')

        self._samples_titles, self._samples_texts, self._targets, self._tags = self.load(self.dataset_path)
        
    def _check_exists(self) -> bool:
        return self.dataset_path.exists()
    
    def load(self, file_path) -> Tuple[List[str], List[str], List[str]]:
        samples_title, samples_text, targets, tags = list(), list(), list(), list()

        with open(file_path, 'r', encoding='utf8') as file:
            json_obj = json.load(file)

        for idx in json_obj.keys():
            samples_title.append(json_obj[idx]['title'].rstrip().lstrip())
            samples_text.append(json_obj[idx]['text'])
            targets.append(json_obj[idx]['true_label'])
            tags.append(json_obj[idx]['tags'].split('|')[1:-1])

        return samples_title, samples_text, targets, tags


    def download(self) -> None:
        if self._check_exists():
            return 
        
        self.root.mkdir(exist_ok=True)
        
        text = request.urlopen(self.data_file).read().decode('utf8')
        with open(self.dataset_path, 'w', encoding='utf8') as f:
            for line in text.split('\\n'):
                f.write(line + '\n')
                
    @property
    def labels(self) -> List[str]:
        return self._targets
    
    @property
    def data(self) -> List[str]:
        return self._samples
    
    def __getitem__(self, idx) -> Tuple[str, str]:
        sample_title = self._samples_titles[idx]
        sample_text = self._samples_texts[idx]
        target = self._targets[idx]

        if self.return_tags:
            tags = self._tags[idx]
            return sample_title, sample_text, target, tags
        
        return sample_title, sample_text, target

if __name__ == '__main__':
    dataset = ClassificationDataset('/Users/bogdanivanyuk/Desktop/BERT_train_data/classification_data', return_tags=True)
    print(dataset[0])
