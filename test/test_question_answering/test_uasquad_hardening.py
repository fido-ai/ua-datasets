import json
from pathlib import Path

import pytest

from ua_datasets.question_answering.uasquad_question_answering import (
    ParseError,
    UaSquadDataset,
)


def _write(root: Path, name: str, obj: object) -> Path:
    p = root / name
    if isinstance(obj, str):
        p.write_text(obj, encoding="utf8")
    else:
        p.write_text(json.dumps(obj), encoding="utf8")
    return p


@pytest.fixture
def qa_tmp_root(tmp_path: Path) -> Path:
    return tmp_path


def test_malformed_json_raises(qa_tmp_root: Path) -> None:
    _write(qa_tmp_root, "train.json", "{not-json}")
    with pytest.raises(ParseError):
        UaSquadDataset(root=qa_tmp_root, split="train", download=False)


def test_empty_data_list_raises(qa_tmp_root: Path) -> None:
    _write(qa_tmp_root, "train.json", {"data": []})
    with pytest.raises(ParseError):
        UaSquadDataset(root=qa_tmp_root, split="train", download=False)


def test_answer_frequencies_and_unique(qa_tmp_root: Path) -> None:
    obj = {
        "data": [
            {"question": "Q1", "context": "C1", "answer": "A1"},
            {"question": "Q2", "context": "C2", "answer": "A1"},
            {"question": "Q3", "context": "C3", "answer": "A2"},
        ]
    }
    _write(qa_tmp_root, "train.json", obj)
    ds = UaSquadDataset(root=qa_tmp_root, split="train", download=False)
    freqs = ds.answer_frequencies()
    assert freqs == {"A1": 2, "A2": 1}
    assert ds.unique_answers == {"A1", "A2"}


def test_force_download_skip(monkeypatch: pytest.MonkeyPatch, qa_tmp_root: Path) -> None:
    # Existing file should bypass network when force_download False
    _write(qa_tmp_root, "train.json", {"data": [{"question": "Q", "context": "C", "answer": "A"}]})
    called = {"count": 0}

    def fake_urlopen(url: str, timeout: int = 0) -> None:  # pragma: no cover - should not be used
        called["count"] += 1
        raise AssertionError("Should not download when file exists and force_download=False")

    monkeypatch.setattr(
        "ua_datasets.question_answering.uasquad_question_answering.urlopen", fake_urlopen
    )
    UaSquadDataset(root=qa_tmp_root, split="train", download=True, force_download=False)
    assert called["count"] == 0


def test_force_download_replaces(monkeypatch: pytest.MonkeyPatch, qa_tmp_root: Path) -> None:
    # Initial file
    _write(qa_tmp_root, "train.json", {"data": [{"question": "Q", "context": "C", "answer": "A"}]})
    new_payload = {"data": [{"question": "QNEW", "context": "CNEW", "answer": "ANEW"}]}

    class FakeResp:
        def __init__(self, data: bytes) -> None:
            self._data = data

        def read(self) -> bytes:
            return self._data

        def __enter__(self) -> "FakeResp":
            return self

        def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
            return None

    def fake_urlopen(url: str, timeout: int = 0) -> FakeResp:
        return FakeResp(json.dumps(new_payload).encode("utf8"))

    monkeypatch.setattr(
        "ua_datasets.question_answering.uasquad_question_answering.urlopen", fake_urlopen
    )
    ds = UaSquadDataset(root=qa_tmp_root, split="train", download=True, force_download=True)
    assert len(ds) == 1
    ex = ds[0]
    assert ex["question"] == "QNEW"
    if not ex.get("is_impossible"):
        assert ex["answers"]["text"][0] == "ANEW"
