import pytest

@pytest.mark.parametrize("idx", [1, 10, 100])
def test_dataset_type(idx, train_dataset, test_dataset):
    title, text, target, _ = train_dataset[idx]
    assert isinstance(title, str)
    assert isinstance(text, str)
    assert isinstance(target, str)

    title, text, target, _ = test_dataset[idx]
    assert isinstance(title, str)
    assert isinstance(text, str)
    assert isinstance(target, str)

@pytest.mark.parametrize("dataset_size", [120_417])
def test_traindataset_size(dataset_size, train_dataset):
    assert len(train_dataset) == dataset_size

@pytest.mark.parametrize("dataset_size", [30_105])
def test_testdataset_size(dataset_size, test_dataset):
    assert len(test_dataset) == dataset_size