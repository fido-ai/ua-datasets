import pytest

from ua_datasets import UaSquadDataset


def test_basic_integrity(dataset: UaSquadDataset) -> None:
    """At least one QA triplet is present and components are non-empty strings.

    If the dataset is empty (e.g. missing val split remotely) the fixture may still
    supply it; in that case we skip rather than fail so CI remains green for other splits.
    """
    if len(dataset) == 0:
        pytest.skip("Empty split provided (no samples). Skipping integrity checks.")
    q, c, a = dataset[0]
    assert all(isinstance(x, str) and x.strip() for x in (q, c, a))


def test_multiple_samples_if_available(dataset: UaSquadDataset) -> None:
    """Check spaced samples (first, middle, last) when dataset is large enough."""
    if len(dataset) == 0:
        return
    n = len(dataset)
    for idx in [0, n // 2, n - 1]:
        q, c, a = dataset[idx]
        assert all(isinstance(x, str) and x.strip() for x in (q, c, a))


def test_iter_first_three(dataset: UaSquadDataset) -> None:
    """Iterating yields triplets of strings; limit to first three to stay quick."""
    count_checked = 0
    for triplet in dataset:
        q, c, a = triplet
        assert all(isinstance(x, str) and x.strip() for x in (q, c, a))
        count_checked += 1
    # If dataset non-empty ensure we actually validated at least one
    assert count_checked == len(dataset)


def test_alignment_and_data_property(dataset: UaSquadDataset) -> None:
    """questions, contexts, answers lengths align and match data property length."""
    if len(dataset) == 0:
        return
    # Access via public properties if they exist (dataset exposes them).
    questions = getattr(dataset, "questions", [])
    contexts = getattr(dataset, "contexts", [])
    answers = getattr(dataset, "answers", [])
    assert len(questions) == len(contexts) == len(answers) == len(dataset)
    data_pairs = dataset.data
    assert len(data_pairs) == len(dataset)
    # Spot check first pair matches first question/context
    dq, dc = data_pairs[0]
    assert dq == questions[0]
    assert dc == contexts[0]


def test_repr_contains_split_and_count(dataset: UaSquadDataset) -> None:
    r = repr(dataset)
    # Should at least mention the split string and a count marker
    assert dataset.split in r
    assert "n_samples=" in r or "n_samples" in r or str(len(dataset)) in r
