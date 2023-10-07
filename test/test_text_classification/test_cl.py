import pytest

@pytest.mark.parametrize("idx", [1, 10, 100])
def test_dataset_type(idx, train_dataset, test_dataset):
    q, c, a, _ = train_dataset[idx]
    assert type(q) == str
    assert type(c) == str 
    assert type(a) == str

    q, c, a, _ = test_dataset[idx]
    assert type(q) == str
    assert type(c) == str 
    assert type(a) == str

@pytest.mark.parametrize("dataset_size", [120_417])
def test_traindataset_size(dataset_size, train_dataset):
    assert len(train_dataset) == dataset_size

@pytest.mark.parametrize("dataset_size", [30_105])
def test_testdataset_size(dataset_size, test_dataset):
    assert len(test_dataset) == dataset_size