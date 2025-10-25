from pathlib import Path

import pytest

from ua_datasets.token_classification.part_of_speech import MovaInstitutePOSDataset


@pytest.fixture(scope="module")
def dataset(dataset_root: Path) -> MovaInstitutePOSDataset:
    return MovaInstitutePOSDataset(root=dataset_root, download=True)
