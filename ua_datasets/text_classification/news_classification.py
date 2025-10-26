"""News classification dataset loader.

Expected CSV Columns
--------------------
Required minimal columns: ``title``, ``text``, ``tags``, ``target`` in that
order. (Historically this dataset has used that order.) If columns are missing
or re-ordered the loader attempts to locate required names; if any mandatory
column is absent a :class:`ParseError` is raised.

Example
-------
>>> ds = NewsClassificationDataset(root=Path('./news'), split='train', download=True)
>>> title, text, target, tags = ds[0]
>>> len(ds), target in ds.labels
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Set, Tuple
from urllib.request import urlopen

from ua_datasets.utils import DownloadFailure, atomic_write_text, download_text_with_retries

__all__ = [
    "DownloadError",
    "NewsClassificationDataset",
    "ParseError",
]


class DownloadError(RuntimeError):
    """Raised when the dataset cannot be downloaded after retries or integrity check fails."""


class ParseError(RuntimeError):
    """Raised when CSV file is empty, malformed, or missing mandatory columns."""


Row = List[str]
Sample = Tuple[str, str, str, Optional[List[str]]]


@dataclass(slots=True)
class NewsClassificationDataset:
    """Ukrainian news classification dataset.

    Parameters
    ----------
    root:
        Directory where the dataset split CSV will be stored or read from.
    download:
        If ``True`` (default), download the split file if it is missing.
    split:
        One of ``"train"`` or ``"test"``.
    return_tags:
        If ``True`` parsed list of tags is returned instead of ``None`` in the
        4th element of each sample tuple.
    """

    root: Path
    download: bool = True
    split: str = "train"
    return_tags: bool = False

    base_url: str = "https://github.com/fido-ai/ua-datasets/releases/download/v0.0.1/"
    force_download: bool = False
    max_retries: int = 3
    timeout: int = 20  # seconds
    expected_sha256: str | None = None
    show_progress: bool = True

    dataset_path: Path = field(init=False)
    _columns: List[str] = field(init=False, default_factory=list)
    _rows: List[Row] = field(init=False, default_factory=list)
    _parsed_tags: Optional[List[List[str]]] = field(init=False, default=None)
    _label_cache: Set[str] = field(init=False, default_factory=set)

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        self.dataset_path = self.root / f"{self.split}.csv"
        if self.download:
            self.download_dataset()
        if not self.dataset_path.exists():
            raise FileNotFoundError(
                "Dataset not found. Use download=True to fetch it or ensure the file exists."
            )
        self._rows = self._load_rows()
        if not self._rows:
            raise ParseError("Loaded zero rows; file may be empty or malformed.")
        # Cache labels for fast repeated access
        self._label_cache = {row[self._columns.index("target")] for row in self._rows}

    def download_dataset(self) -> None:
        """Download the dataset split file if needed using shared helper."""
        if self.dataset_path.exists() and not self.force_download:
            return
        self.root.mkdir(parents=True, exist_ok=True)
        url = f"{self.base_url}{self.split}.csv"
        try:
            text = download_text_with_retries(
                url,
                timeout=self.timeout,
                max_retries=self.max_retries,
                expected_sha256=self.expected_sha256,
                opener=urlopen,
                show_progress=self.show_progress,
            )
        except DownloadFailure as exc:
            raise DownloadError(str(exc)) from exc
        atomic_write_text(self.dataset_path, text)

    def _load_rows(self) -> List[Row]:
        """Load raw rows from CSV, capturing header separately and validating columns."""
        with self.dataset_path.open("r", encoding="utf8", newline="") as f:
            reader = csv.reader(f)
            try:
                self._columns = next(reader)
            except StopIteration as exc:
                raise ParseError("CSV file is empty") from exc
            required = {"title", "text", "target"}
            missing = required - set(self._columns)
            if missing:
                raise ParseError(f"Missing required column(s): {', '.join(sorted(missing))}")
            rows: List[Row] = []
            for row in reader:
                if not row or all(cell == "" for cell in row):
                    continue
                # Basic row length guard
                if len(row) < len(self._columns):
                    # Allow shorter if trailing columns empty, pad to columns length
                    row = row + [""] * (len(self._columns) - len(row))
                rows.append(row)
        return rows

    @property
    def column_names(self) -> List[str]:
        return self._columns

    @property
    def labels(self) -> Set[str]:
        return set(self._label_cache)

    @property
    def data(self) -> List[Row]:
        return self._rows

    @staticmethod
    def _preprocess_tags(tags: str) -> List[str]:
        return [el for el in tags.split("|") if el]

    def _ensure_parsed_tags(self) -> None:
        if not self.return_tags or self._parsed_tags is not None:
            return
        tags_idx = self._columns.index("tags") if "tags" in self._columns else None
        parsed: List[List[str]] = []
        for row in self._rows:
            raw = row[tags_idx] if tags_idx is not None and tags_idx < len(row) else ""
            parsed.append(self._preprocess_tags(raw))
        self._parsed_tags = parsed

    def label_frequencies(self) -> Dict[str, int]:
        freqs: Dict[str, int] = {}
        tgt_idx = self._columns.index("target")
        for row in self._rows:
            tgt = row[tgt_idx]
            freqs[tgt] = freqs.get(tgt, 0) + 1
        return freqs

    def __len__(self) -> int:
        return len(self._rows)

    def __getitem__(self, idx: int) -> Sample:
        title, text, _tags_raw, target = self._rows[idx]
        if self.return_tags:
            self._ensure_parsed_tags()
            assert self._parsed_tags is not None
            return title, text, target, self._parsed_tags[idx]
        return title, text, target, None

    def __iter__(self) -> Iterator[Sample]:
        for i in range(len(self)):
            yield self[i]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(split={self.split!r}, n_rows={len(self)}, n_labels={len(self.labels)}, return_tags={self.return_tags})"
