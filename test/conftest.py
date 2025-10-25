"""Global pytest configuration and shared fixtures."""

from __future__ import annotations

from pathlib import Path
from typing import Generator

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--dataset-root",
        action="store",
        default=".data",
        help="Root directory where datasets will be cached/downloaded.",
    )


@pytest.fixture(scope="session")
def dataset_root(request: pytest.FixtureRequest) -> Path:
    """Return the root path for dataset downloads/caches (session scoped)."""
    return Path(request.config.getoption("--dataset-root")).resolve()


@pytest.fixture(scope="session", autouse=True)
def _cleanup_dataset_root(dataset_root: Path) -> Generator[None, None, None]:
    """Remove the dataset root directory after the entire test session.

    Ensures no downloaded artifacts (e.g. `.data` directory) remain in the
    repository after tests complete, keeping the working tree clean.
    """
    yield
    if dataset_root.exists():
        import shutil

        shutil.rmtree(dataset_root, ignore_errors=True)
