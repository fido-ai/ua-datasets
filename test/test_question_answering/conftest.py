from pathlib import Path
from typing import cast

import pytest

from ua_datasets import UaSquadDataset


@pytest.fixture(scope="module", params=["train", "val"])
def dataset(request: pytest.FixtureRequest, dataset_root: Path) -> UaSquadDataset:
    """UaSquadDataset fixture parametrized over splits.

    Skips gracefully if the remote resource is unavailable or filenames differ
    from the assumed defaults (train.json / val.json) so that other test
    suites can still run.
    """
    split: str = request.param
    try:
        return UaSquadDataset(root=dataset_root, split=split, download=True)
    except Exception as exc:  # pragma: no cover - network/remote variability
        pytest.skip(f"Skipping UaSquadDataset {split!r} split: {exc}")
        # Help mypy understand this function always returns a UaSquadDataset (skip raises)
        return cast(UaSquadDataset, None)  # unreachable
