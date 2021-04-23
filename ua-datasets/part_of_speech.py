import os
from urllib import request


class MovaInstitutePOSDataset:

    data_file = 'https://lab.mova.institute/files/robochyi_tb.conllu.txt'

    def __init__(self, root: str, train: bool = True, download: bool = True):
        self.root = root
        self.file_name = 'dataset.txt'
        if download:
            self.download()

        if not self._check_exists():
            raise RuntimeError('Dataset not found.' +
                               ' You can use download=True to download it')

        self.samples, self.targets = self.load_data(
            os.path.join(self.root, self.file_name))

    @property
    def labels(self):
        return self.targets

    @property
    def data(self):
        return self.samples

    def load_data(self, file_path):
        samples, targets = list(), list()
        curr_sample, curr_target = list(), list()
        with open(file_path, 'r', encoding='utf8') as file:
            for idx, line in enumerate(file):
                if line[0].isdigit():
                    line = line.split('\t')
                    curr_sample.append(line[1])
                    curr_target.append(line[3])
                if line[0] == '\n':
                    samples.append(curr_sample)
                    targets.append(curr_target)
                    curr_sample, curr_target = list(), list()
        return samples, targets

    def __getitem__(self, idx):
        sample = self.samples[idx]
        target = self.targets[idx]
        return sample, target

    def __len__(self):
        return len(self.data)

    def _check_exists(self) -> bool:
        return os.path.exists(os.path.join(self.root, self.file_name))

    def download(self):
        if self._check_exists():
            return

        os.makedirs(self.root, exist_ok=True)

        text = request.urlopen(self.data_file).read().decode('utf8')
        with open(os.path.join(self.root, self.file_name), 'w', encoding='utf8') as f:
            for line in text.split('\\n'):
                f.write(line + '\n')
