from __future__ import annotations

import json
from pathlib import Path

from ua_datasets import UaSquadDataset

TRAIN_JSON = {
    "data": [
        {"question": "What is Python?", "context": "Python is a language.", "answer": "a language"},
        {"question": "Who created Python?", "context": "Guido created it.", "answer": "Guido"},
    ]
}

VAL_JSON = {
    "data": [
        {"question": "Where?", "context": "In Europe.", "answer": "Europe"},
        {"question": "When?", "context": "In 1991.", "answer": "1991"},
        {"question": "Why?", "context": "For fun.", "answer": "For fun"},
    ]
}


def write_json(root: Path, name: str, obj: dict) -> Path:
    p = root / name
    p.write_text(json.dumps(obj), encoding="utf8")
    return p


def test_train_present_no_download(tmp_path: Path) -> None:
    write_json(tmp_path, "train.json", TRAIN_JSON)
    ds = UaSquadDataset(root=tmp_path, split="train", download=False)
    assert len(ds) == 2
    ex = ds[0]
    assert isinstance(ex, dict)
    assert all(isinstance(ex[k], str) and ex[k] for k in ("question", "context"))
    if not ex.get("is_impossible"):
        assert ex["answers"]["text"]
        assert isinstance(ex["answers"]["text"][0], str)


def test_train_missing_no_download(tmp_path: Path) -> None:
    ds = UaSquadDataset(root=tmp_path, split="train", download=False)
    assert len(ds) == 0


def test_val_present_no_download(tmp_path: Path) -> None:
    write_json(tmp_path, "val.json", VAL_JSON)
    ds = UaSquadDataset(root=tmp_path, split="val", download=False)
    assert len(ds) == 3
    ex = ds[len(ds) // 2]
    assert isinstance(ex, dict)
    assert all(isinstance(ex[k], str) and ex[k] for k in ("question", "context"))


def test_val_missing_no_download(tmp_path: Path) -> None:
    ds = UaSquadDataset(root=tmp_path, split="val", download=False)
    assert len(ds) == 0


def test_iter_matches_len(tmp_path: Path) -> None:
    write_json(tmp_path, "train.json", TRAIN_JSON)
    ds = UaSquadDataset(root=tmp_path, split="train", download=False)
    assert len(list(ds)) == len(ds)
