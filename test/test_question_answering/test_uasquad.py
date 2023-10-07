import pytest

@pytest.mark.parametrize("idx", [1, 10, 100])
def test_dataset_type(idx, dataset):
    q, c, a = dataset[idx]
    assert type(q) == str
    assert type(c) == str 
    assert type(a) == str

@pytest.mark.parametrize("dataset_size", [13_859])
def test_dataset_size(dataset_size, dataset):
    assert len(dataset) == dataset_size