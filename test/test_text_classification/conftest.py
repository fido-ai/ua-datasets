from pathlib import Path

import pytest

from ua_datasets import NewsClassificationDataset


@pytest.fixture(scope="module")
def train_dataset(dataset_root: Path) -> NewsClassificationDataset:
    # Pass Path directly to satisfy type checker (was str via as_posix()).
    return NewsClassificationDataset(root=dataset_root, split="train")


@pytest.fixture(scope="module")
def test_dataset(dataset_root: Path) -> NewsClassificationDataset:
    return NewsClassificationDataset(root=dataset_root, split="test")
