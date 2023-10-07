import pytest 

from ua_datasets import NewsClassificationDataset

@pytest.fixture(scope="module")
def train_dataset(request):
    root = request.config.getoption("--dataset-root")
    df = NewsClassificationDataset(root=root, split='train')
    return df

@pytest.fixture(scope="module")
def test_dataset(request):
    root = request.config.getoption("--dataset-root")
    df = NewsClassificationDataset(root=root, split='test')
    return df