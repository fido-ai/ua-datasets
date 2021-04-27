class MovaInstitutePOSDataset:
    
    data_file = 'https://lab.mova.institute/files/robochyi_tb.conllu.txt'
    
    def __init__(self, root:str, train:bool = True, download:bool = True) -> None:
        self.root = Path(root)
        self.file_name = 'mova_institue_pos_dataset.txt'
        self.dataset_path = self.root / self.file_name
        if download:
            self.download()
            
        if not self._check_exists():
            raise RuntimeError('Dataset not found.' + 
                              ' You can use download=True to download it')
        
        self.samples, self.targets = self.load_data(self.dataset_path)
    
    @property
    def labels(self) -> List[Any]:
        return self.targets
    
    @property
    def data(self) -> List[Any]:
        return self.samples
    
    def load_data(self, file_path) -> Tuple[List[Any], List[Any]]:
        samples, targets = list(), list()
        curr_sample, curr_target = list(), list()
        with open(file_path, 'r', encoding='utf8') as file:
            for line in file:
                if line[0].isdigit():
                    line = line.split('\t')
                    curr_sample.append(line[1])
                    curr_target.append(line[3])
                elif line[0] == '\n':
                    samples.append(curr_sample)
                    targets.append(curr_target)
                    curr_sample, curr_target = list(), list()
        return samples, targets
                    
    def __getitem__(self, idx) -> Tuple[Any, Any]:
        sample = self.samples[idx]
        target = self.targets[idx]
        return sample, target
    
    def __len__(self) -> int:
        return len(self.data)
    
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
