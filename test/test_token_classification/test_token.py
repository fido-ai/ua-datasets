import pytest

from ua_datasets.token_classification.part_of_speech import MovaInstitutePOSDataset


@pytest.mark.parametrize("dataset_size", [7100])
def test_dataset_size(dataset_size: int, dataset: MovaInstitutePOSDataset) -> None:
    assert len(dataset) == dataset_size


def test_first_sample_non_empty(dataset: MovaInstitutePOSDataset) -> None:
    sample, labels = dataset[0]
    assert sample, "First token sequence should not be empty"
    assert labels, "First label sequence should not be empty"
    assert len(sample) == len(labels), "Sample and label length must match"


def test_unique_labels(dataset: MovaInstitutePOSDataset) -> None:
    unique = dataset.unique_labels
    assert isinstance(unique, set)
    assert unique, "There should be at least one unique label"
    # Basic sanity: POS tags often include 'NOUN' or similar; do a soft check
    assert any(len(tag) > 1 for tag in unique)


def test_iteration(dataset: MovaInstitutePOSDataset) -> None:
    first = next(iter(dataset))
    assert isinstance(first, tuple)
    assert len(first) == 2
    tokens, tags = first
    assert len(tokens) == len(tags)
