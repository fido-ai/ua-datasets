from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Set, Tuple
from urllib.request import urlopen

from ua_datasets.utils import DownloadFailure, atomic_write_text, download_text_with_retries

__all__ = [
    "DownloadError",
    "ParseError",
    "UaSquadDataset",
]

QATriplet = Tuple[str, str, str]


class DownloadError(RuntimeError):
    """Raised when a split cannot be downloaded after retries or integrity check fails."""


class ParseError(RuntimeError):
    """Raised when the JSON file is malformed or yields zero valid QA triplets."""


@dataclass(slots=True)
class UaSquadDataset:
    """Ukrainian SQuAD-style Question Answering dataset.

    Parameters
    ----------
    root:
        Directory where splits will be cached.
    split:
        One of ``"train"`` or ``"val"``.
    download:
        If ``True`` (default) downloads the split file if it is missing.
    file_map:
        Optional mapping from split name to filename. Defaults to
        ``{"train": "train.json", "val": "val.json"}``.
    base_url:
        Base URL path ending with a slash from which filenames are resolved.
    """

    root: Path
    split: str = "train"
    download: bool = True
    file_map: dict[str, List[str]] = field(
        default_factory=lambda: {
            "train": ["train.json"],
            "val": ["val.json", "validation.json", "dev.json", "val.jspon"],
        }
    )
    base_url: str = "https://huggingface.co/datasets/FIdo-AI/ua-squad/resolve/main/"
    force_download: bool = False
    max_retries: int = 3
    timeout: int = 20  # seconds
    expected_sha256: str | None = None

    dataset_path: Optional[Path] = field(init=False, default=None)
    _questions: List[str] = field(init=False, default_factory=list)
    _contexts: List[str] = field(init=False, default_factory=list)
    _answers: List[str] = field(init=False, default_factory=list)
    _unique_answers_cache: Set[str] = field(init=False, default_factory=set)

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        if self.split not in self.file_map:
            raise ValueError(
                f"Unsupported split '{self.split}'. Expected one of: {list(self.file_map)}"
            )
        self.dataset_path = self._resolve_or_download_split()
        if self.dataset_path is None:
            # Graceful empty dataset (tests expect len==0 allowed)
            self._questions, self._contexts, self._answers = [], [], []
            return
        self._questions, self._contexts, self._answers = self._parse(self.dataset_path)
        if not self._questions:
            # Treat zero parsed entries as malformed unless split truly absent (handled above)
            raise ParseError(
                f"Parsed zero QA triplets from '{self.dataset_path}'. File may be malformed."
            )
        self._unique_answers_cache = set(self._answers)

    @property
    def data(self) -> List[Tuple[str, str]]:
        """Question-context pairs (parallel sequences)."""
        return list(zip(self._questions, self._contexts, strict=True))

    @property
    def labels(self) -> List[str]:
        """Answers list (alias for compatibility)."""
        return self._answers

    @property
    def answers(self) -> List[str]:
        return self._answers

    @property
    def unique_answers(self) -> Set[str]:
        return set(self._unique_answers_cache)

    def answer_frequencies(self) -> Dict[str, int]:
        freqs: Dict[str, int] = {}
        for a in self._answers:
            freqs[a] = freqs.get(a, 0) + 1
        return freqs

    @property
    def contexts(self) -> List[str]:
        return self._contexts

    @property
    def questions(self) -> List[str]:
        return self._questions

    def _resolve_or_download_split(self) -> Path | None:
        """Locate or download split file with retries & optional integrity."""
        candidates = self.file_map[self.split]
        self.root.mkdir(parents=True, exist_ok=True)

        # Existing file short-circuit
        for name in candidates:
            path = self.root / name
            if path.exists() and not self.force_download:
                return path
        if not self.download:
            return None

        for name in candidates:
            path = self.root / name
            url = f"{self.base_url}{name}"
            try:
                text = download_text_with_retries(
                    url,
                    timeout=self.timeout,
                    max_retries=self.max_retries,
                    expected_sha256=self.expected_sha256,
                    validate=lambda t: t.lstrip().startswith("{") or t.lstrip().startswith("["),
                    opener=urlopen,
                )
                atomic_write_text(path, text)
                return path
            except DownloadFailure:
                continue
        return None

    @staticmethod
    def _parse(path: Path) -> Tuple[List[str], List[str], List[str]]:
        """Parse either flat or nested (SQuAD-style) schema.

        Supported formats:
        1. Flat: {"data": [{"question", "context", "answer"}]}
        2. Nested SQuAD: {"data": [{"paragraphs": [{"context": str, "qas": [{
           "question": str, "answers": [{"text": str}, ...]}]}]}]}
        """
        with path.open("r", encoding="utf8") as f:
            try:
                obj = json.load(f)
            except json.JSONDecodeError as exc:
                raise ParseError(f"Failed to decode JSON file '{path}': {exc}") from exc

        data = obj.get("data", [])
        questions: List[str] = []
        contexts: List[str] = []
        answers: List[str] = []

        if (
            data
            and isinstance(data, list)
            and isinstance(data[0], dict)
            and "paragraphs" in data[0]
        ):
            for article in data:
                for para in article.get("paragraphs", []):
                    context = para.get("context")
                    if context is None:
                        continue
                    # Normalize and skip empty / whitespace-only contexts
                    context = str(context).strip()
                    if not context:
                        continue

                    for qa in para.get("qas", []):
                        question = qa.get("question")
                        if question is None:
                            continue
                        question = str(question).strip()
                        if not question:
                            continue

                        ans_list = qa.get("answers") or []
                        answer_text = None
                        for candidate in ans_list:
                            answer_text = candidate.get("text")
                            if answer_text:
                                break
                        if answer_text is None:
                            # some formats have 'plausible_answers'
                            for candidate in qa.get("plausible_answers", []):
                                answer_text = candidate.get("text")
                                if answer_text:
                                    break
                        if answer_text is None:
                            continue
                        answer_text = str(answer_text).strip()
                        if not answer_text:
                            continue

                        questions.append(question)
                        contexts.append(context)
                        answers.append(answer_text)
        else:
            for item in data:
                if not isinstance(item, dict):
                    continue
                question = item.get("question")
                context = item.get("context")
                answer = item.get("answer")
                if question is None or context is None or answer is None:
                    continue
                question, context, answer = (
                    str(question).strip(),
                    str(context).strip(),
                    str(answer).strip(),
                )
                if not (question and context and answer):
                    continue

                questions.append(question)
                contexts.append(context)
                answers.append(answer)

        return questions, contexts, answers

    def __getitem__(self, idx: int) -> QATriplet:
        return self._questions[idx], self._contexts[idx], self._answers[idx]

    def __len__(self) -> int:
        return len(self._questions)

    def __iter__(self) -> Iterator[QATriplet]:
        for i in range(len(self)):
            yield self[i]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(split={self.split!r}, n_samples={len(self)}, unique_answers={len(self._unique_answers_cache)})"

    def _check_exists(self) -> bool:
        return bool(self.dataset_path and self.dataset_path.exists())
