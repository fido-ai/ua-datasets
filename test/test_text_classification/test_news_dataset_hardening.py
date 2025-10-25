from pathlib import Path

import pytest

from ua_datasets.text_classification.news_classification import (
    NewsClassificationDataset,
    ParseError,
)


def _write(root: Path, name: str, text: str) -> Path:
    p = root / name
    p.write_text(text, encoding="utf8")
    return p


@pytest.fixture()
def tmp_news_root(tmp_path: Path) -> Path:
    return tmp_path


def test_empty_file_raises_parse_error(tmp_news_root: Path) -> None:
    _write(tmp_news_root, "train.csv", "")
    with pytest.raises(ParseError):
        NewsClassificationDataset(root=tmp_news_root, split="train", download=False)


def test_missing_required_column(tmp_news_root: Path) -> None:
    # Missing target column
    content = "title,text,tags\nA,B,tag1|tag2\n"
    _write(tmp_news_root, "train.csv", content)
    with pytest.raises(ParseError):
        NewsClassificationDataset(root=tmp_news_root, split="train", download=False)


def test_basic_loading_and_label_cache(tmp_news_root: Path) -> None:
    content = "title,text,tags,target\nT1,Body one,tag1|tag2,CLASS1\nT2,Body two,,CLASS2\n"
    _write(tmp_news_root, "train.csv", content)
    ds = NewsClassificationDataset(root=tmp_news_root, split="train", download=False)
    assert len(ds) == 2
    assert ds.labels == {"CLASS1", "CLASS2"}
    freqs = ds.label_frequencies()
    assert freqs == {"CLASS1": 1, "CLASS2": 1}


def test_tag_parsing_return_tags(tmp_news_root: Path) -> None:
    content = "title,text,tags,target\nT1,Body one,tag1|tag2,CLASS1\nT2,Body two,tag3,CLASS1\n"
    _write(tmp_news_root, "train.csv", content)
    ds = NewsClassificationDataset(
        root=tmp_news_root, split="train", download=False, return_tags=True
    )
    title, _text, target, tags = ds[0]
    assert title == "T1"
    assert target == "CLASS1"
    assert tags == ["tag1", "tag2"]
    # second sample
    _, _, _, tags2 = ds[1]
    assert tags2 == ["tag3"]


def test_no_trailing_newline(tmp_news_root: Path) -> None:
    # File ends without newline, should still parse second row
    content = "title,text,tags,target\nT1,Body one,,A\nT2,Body two,,B"  # no trailing newline
    _write(tmp_news_root, "train.csv", content)
    ds = NewsClassificationDataset(root=tmp_news_root, split="train", download=False)
    assert len(ds) == 2


def test_force_download_skips_when_disabled(
    monkeypatch: pytest.MonkeyPatch, tmp_news_root: Path
) -> None:
    # Create existing file then ensure download is *not* called when force_download False
    content = "title,text,tags,target\nT1,Body one,,A\n"
    _write(tmp_news_root, "train.csv", content)
    called = {"count": 0}

    def fake_urlopen(url: str, timeout: int = 0) -> None:
        called["count"] += 1
        raise AssertionError("Should not be called when file exists and force_download=False")

    monkeypatch.setattr("ua_datasets.text_classification.news_classification.urlopen", fake_urlopen)
    NewsClassificationDataset(root=tmp_news_root, split="train", download=False)
    assert called["count"] == 0


def test_force_download_triggers(monkeypatch: pytest.MonkeyPatch, tmp_news_root: Path) -> None:
    content = "title,text,tags,target\nT1,Body one,,A\n"
    _write(tmp_news_root, "train.csv", content)

    # Replace content via forced download
    new_csv = "title,text,tags,target\nN1,Body new,,B\n"

    class FakeResponse:
        def __init__(self, data: bytes) -> None:
            self._data = data

        def read(self) -> bytes:
            return self._data

        def __enter__(self) -> "FakeResponse":
            return self

        def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
            return None

    def fake_urlopen(url: str, timeout: int = 0) -> FakeResponse:
        return FakeResponse(new_csv.encode("utf8"))

    monkeypatch.setattr("ua_datasets.text_classification.news_classification.urlopen", fake_urlopen)
    ds = NewsClassificationDataset(
        root=tmp_news_root, split="train", download=True, force_download=True
    )
    assert len(ds) == 1
    title, *_ = ds[0]
    assert title == "N1"
