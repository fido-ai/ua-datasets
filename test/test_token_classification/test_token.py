import pytest

@pytest.mark.parametrize("dataset_size", [7_101])
def test_dataset_size(dataset_size, dataset):
    assert len(dataset) == dataset_size
