import pytest

from ua_datasets import UaSquadDataset


def pytest_addoption(parser):
    """Add option to specify dataset location when executing tests from CLI.
    Ex: pytest --dataset-loc=checkpoints/data.csv tests/data --verbose --disable-warnings
    """
    parser.addoption(
        "--dataset-root", action="store", default='.data', help="Dataset location."
    )

@pytest.fixture(scope="module")
def dataset(request):
    root = request.config.getoption("--dataset-root")
    dataset = UaSquadDataset(root=root)
    return dataset