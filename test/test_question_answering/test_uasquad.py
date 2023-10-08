import pytest

@pytest.mark.parametrize("idx", [1, 10, 100])
def test_dataset_type(idx, dataset):
    question, context, answer = dataset[idx]
    assert isinstance(question, str)
    assert isinstance(context, str)
    assert isinstance(answer, str)

@pytest.mark.parametrize("dataset_size", [13_859])
def test_dataset_size(dataset_size, dataset):
    assert len(dataset) == dataset_size