"""Part-of-speech tagging dataset loader for the Mova Institute corpus.

This module provides a light-weight, dependency-free interface to download and
parse a (CoNLL-U like) POS tagging dataset with a focus on robustness and
clarity.

Example
-------
>>> ds = MovaInstitutePOSDataset(root=Path('./data'), download=True)
>>> tokens, tags = ds[0]
>>> len(ds), len(tokens) == len(tags)
"""

from collections.abc import Sequence as ABCSequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Generic, Iterator, List, Set, Tuple, TypeVar

from ua_datasets.utils import DownloadFailure, atomic_write_text, download_text_with_retries

__all__ = [
    "DownloadError",
    "MovaInstitutePOSDataset",
    "ParseError",
]

Sentence = List[str]
TagSequence = List[str]


S = TypeVar("S", bound=Sentence)
T = TypeVar("T", bound=TagSequence)


class DownloadError(RuntimeError):
    """Raised when the dataset cannot be downloaded after retries."""


class ParseError(RuntimeError):
    """Raised when the dataset file cannot be parsed into any sentences."""


@dataclass(slots=True)
class MovaInstitutePOSDataset(ABCSequence, Generic[S, T]):
    """Dataset wrapper for the Mova Institute POS tagging corpus.

    Parameters
    ----------
    root:
        Directory where the dataset file will be stored / read from.
    download:
        If True (default) the dataset will be downloaded if missing.
    file_name:
        Local filename for the cached dataset (text format).
    data_file:
        Remote URL containing the dataset contents.
    """

    root: Path
    download: bool = True
    file_name: str = "mova_institute_pos_dataset.txt"
    data_file: str = "https://lab.mova.institute/files/robochyi_tb.conllu.txt"
    force_download: bool = False
    max_retries: int = 3
    timeout: int = 15  # seconds for individual HTTP attempt
    expected_sha256: str | None = None
    show_progress: bool = True

    dataset_path: Path = field(init=False)
    _samples: List[Sentence] = field(init=False, default_factory=list)
    _labels: List[TagSequence] = field(init=False, default_factory=list)
    _unique_labels_cache: Set[str] = field(init=False, default_factory=set)

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        self.dataset_path = self.root / self.file_name
        if self.download:
            self.download_dataset()
        if not self._check_exists():  # Fail early with a clear message.
            raise FileNotFoundError(
                "Dataset not found. Use download=True to fetch it or ensure the file exists."
            )
        self._samples, self._labels = self._load_data()
        if not self._samples:
            raise ParseError(
                f"Parsed zero sentences from dataset file '{self.dataset_path}'. File may be empty or malformed."
            )
        # Cache unique labels (frozenset semantics but returning a set copy in property)
        self._unique_labels_cache = {lab for seq in self._labels for lab in seq}

    @property
    def labels(self) -> List[TagSequence]:
        """Raw label sequences (parallel to `data`)."""
        return self._labels

    @property
    def data(self) -> List[Sentence]:
        """Raw token sequences."""
        return self._samples

    @property
    def unique_labels(self) -> Set[str]:
        """Unique set of tag labels present in the corpus (cached)."""
        return self._unique_labels_cache

    def label_frequencies(self) -> Dict[str, int]:
        """Return a mapping of label -> occurrence count.

        Useful for quick exploratory statistics.
        """
        freqs: Dict[str, int] = {}
        for seq in self._labels:
            for lab in seq:
                freqs[lab] = freqs.get(lab, 0) + 1
        return freqs

    def _iter_conllu_sentences(self) -> Iterator[Tuple[Sentence, TagSequence]]:
        """Yield (tokens, tags) for each sentence in the dataset file."""
        tokens: Sentence = []
        tags: TagSequence = []
        with self.dataset_path.open("r", encoding="utf8") as fh:
            for raw in fh:
                line = raw.rstrip("\n")
                stripped = line.strip()
                if not stripped:  # sentence boundary
                    if tokens:
                        yield tokens, tags
                        tokens, tags = [], []
                    continue
                if stripped.startswith("#"):
                    continue
                parts = stripped.split("\t")
                if len(parts) < 4:
                    continue
                id_field = parts[0]
                # Skip multiword tokens like '3-4'
                if "-" in id_field:
                    continue
                if not id_field.isdigit():
                    continue
                token = parts[1]
                tag = parts[3]
                tokens.append(token)
                tags.append(tag)
            # Flush final sentence if file lacks trailing newline/blank line
            if tokens:
                yield tokens, tags

    def _load_data(self) -> Tuple[List[Sentence], List[TagSequence]]:
        samples: List[Sentence] = []
        labels: List[TagSequence] = []
        for sent, tag_seq in self._iter_conllu_sentences():
            samples.append(sent)
            labels.append(tag_seq)
        return samples, labels

    def __getitem__(self, idx: int) -> Tuple[Sentence, TagSequence]:  # type: ignore[override]
        return self._samples[idx], self._labels[idx]

    def __len__(self) -> int:
        return len(self._samples)

    def __iter__(self) -> Iterator[Tuple[Sentence, TagSequence]]:
        for sample, label in zip(self._samples, self._labels, strict=True):
            yield sample, label

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(n_sentences={len(self)}, unique_labels={len(self.unique_labels)})"

    def _check_exists(self) -> bool:
        return self.dataset_path.exists()

    def download_dataset(self) -> None:
        """Download the raw dataset file if needed using shared retry helper."""
        if self._check_exists() and not self.force_download:
            return
        self.root.mkdir(parents=True, exist_ok=True)
        try:
            text = download_text_with_retries(
                self.data_file,
                timeout=self.timeout,
                max_retries=self.max_retries,
                expected_sha256=self.expected_sha256,
                show_progress=self.show_progress,
            )
        except DownloadFailure as exc:
            raise DownloadError(str(exc)) from exc
        atomic_write_text(self.dataset_path, text)
