import pytest 

from ua_datasets import MovaInstitutePOSDataset

@pytest.fixture(scope="module")
def dataset(request):
    root = request.config.getoption("--dataset-root")
    df = MovaInstitutePOSDataset(root=root)
    return df