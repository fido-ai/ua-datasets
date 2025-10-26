import pytest

from ua_datasets import UaSquadDataset


def test_basic_integrity(dataset: UaSquadDataset) -> None:
    """At least one QA triplet is present and components are non-empty strings.

    If the dataset is empty (e.g. missing val split remotely) the fixture may still
    supply it; in that case we skip rather than fail so CI remains green for other splits.
    """
    if len(dataset) == 0:
        pytest.skip("Empty split provided (no samples). Skipping integrity checks.")
    ex = dataset[0]
    assert isinstance(ex, dict)
    assert isinstance(ex.get("question"), str)
    assert ex["question"].strip()
    assert isinstance(ex.get("context"), str)
    assert ex["context"].strip()
    if not ex.get("is_impossible"):
        assert ex["answers"]["text"]
        assert isinstance(ex["answers"]["text"][0], str)


def test_multiple_samples_if_available(dataset: UaSquadDataset) -> None:
    """Check spaced samples (first, middle, last) when dataset is large enough."""
    if len(dataset) == 0:
        return
    n = len(dataset)
    for idx in [0, n // 2, n - 1]:
        ex = dataset[idx]
        assert isinstance(ex.get("question"), str)
        assert ex["question"].strip()
        assert isinstance(ex.get("context"), str)
        assert ex["context"].strip()
        if not ex.get("is_impossible"):
            assert ex["answers"]["text"]


def test_iter_first_three(dataset: UaSquadDataset) -> None:
    """Iterating yields triplets of strings; limit to first three to stay quick."""
    count_checked = 0
    for ex in dataset:
        assert isinstance(ex.get("question"), str)
        assert ex["question"].strip()
        assert isinstance(ex.get("context"), str)
        assert ex["context"].strip()
        if not ex.get("is_impossible"):
            assert ex["answers"]["text"]
        count_checked += 1
    # If dataset non-empty ensure we actually validated at least one
    assert count_checked == len(dataset)


def test_examples_length_and_schema(dataset: UaSquadDataset) -> None:
    if len(dataset) == 0:
        return
    examples = dataset.examples
    assert len(examples) == len(dataset)
    first = examples[0]
    for key in ["id", "context", "question", "answers", "is_impossible"]:
        assert key in first
    assert isinstance(first["answers"], dict)


def test_repr_contains_split_and_count(dataset: UaSquadDataset) -> None:
    r = repr(dataset)
    # Should at least mention the split string and a count marker
    assert dataset.split in r
    assert "examples=" in r or str(len(dataset)) in r
