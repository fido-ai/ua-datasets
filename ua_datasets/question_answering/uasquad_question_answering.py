from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Set
from urllib.request import urlopen

from ua_datasets.utils import DownloadFailure, atomic_write_text, download_text_with_retries

__all__ = [
    "DownloadError",
    "ParseError",
    "UaSquadDataset",
    "load_ua_squad_v2",
]

# Public (lightweight) representation of a SQuAD v2 style example.
# We intentionally keep this a plain dict-compatible shape instead of introducing
# pydantic/dataclasses for each row to avoid overhead and preserve zero heavy deps.
HFStyleExample = Dict[str, Any]


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
    show_progress: bool = True
    # If True (default) skip flat-format training examples whose 'answer' value is an empty string.
    # This avoids polluting the training set with ambiguous empty-answer placeholders while still
    # retaining explicit impossible examples represented by a missing 'answer' key (answer=None).
    ignore_empty_answer: bool = True

    dataset_path: Optional[Path] = field(init=False, default=None)
    # SQuAD v2 style expanded storage
    _examples: List[HFStyleExample] = field(init=False, default_factory=list)
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
            self._examples = []
            return
        self._examples = self._parse(
            self.dataset_path,
            ignore_empty_answer=self.ignore_empty_answer,
            split=self.split,
        )
        if not self._examples:
            raise ParseError(
                f"Parsed zero QA examples from '{self.dataset_path}'. File may be malformed."
            )
        # Build unique answer cache ignoring empties and impossible examples.
        self._unique_answers_cache = {
            t
            for ex in self._examples
            if not ex.get("is_impossible")
            for t in ex.get("answers", {}).get("text", [])
            if t
        }

    @property
    def unique_answers(self) -> Set[str]:
        return set(self._unique_answers_cache)

    def answer_frequencies(self) -> Dict[str, int]:
        freqs: Dict[str, int] = {}
        for ex in self._examples:
            if ex.get("is_impossible"):
                continue
            for t in ex.get("answers", {}).get("text", []):
                if not t:
                    continue
                freqs[t] = freqs.get(t, 0) + 1
        return freqs

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
                    show_progress=self.show_progress,
                )
                atomic_write_text(path, text)
                return path
            except DownloadFailure:
                continue
        return None

    @staticmethod
    def _parse(
        path: Path,
        *,
        ignore_empty_answer: bool = True,
        split: str | None = None,
    ) -> List[HFStyleExample]:
        """Parse flat (train-like) or nested SQuAD / SQuAD v2 style JSON into HF style examples only."""
        with path.open("r", encoding="utf8") as f:
            try:
                obj = json.load(f)
            except json.JSONDecodeError as exc:
                raise ParseError(f"Failed to decode JSON file '{path}': {exc}") from exc

        data = obj.get("data", [])
        examples: List[HFStyleExample] = []

        def _gen_id(question: str, context: str) -> str:
            # Lightweight deterministic id (not cryptographic, good enough for local uniqueness)
            import hashlib

            h = hashlib.sha1()
            h.update((question + "\n" + context).encode("utf-8"))
            return h.hexdigest()[:16]

        def _compute_answer_start(context: str, answer_text: str) -> int:
            return context.find(answer_text) if answer_text else -1

        nested_format = (
            data
            and isinstance(data, list)
            and isinstance(data[0], dict)
            and "paragraphs" in data[0]
        )

        if nested_format:
            # SQuAD / SQuAD v2 style validation (or full) format
            for article in data:
                title = article.get("title")
                for para in article.get("paragraphs", []):
                    raw_context = para.get("context")
                    if raw_context is None:
                        continue
                    context = str(raw_context).strip()
                    if not context:
                        continue
                    for qa in para.get("qas", []):
                        raw_question = qa.get("question")
                        if raw_question is None:
                            continue
                        question = str(raw_question).strip()
                        if not question:
                            continue
                        # answers may be empty in SQuAD v2
                        ans_objs = qa.get("answers") or []
                        texts: List[str] = []
                        starts: List[int] = []
                        for cand in ans_objs:
                            t = str(cand.get("text", "")).strip()
                            if not t:
                                continue
                            start = cand.get("answer_start")
                            if isinstance(start, int) and start >= 0:
                                # validate substring alignment quickly (best effort)
                                if context[start : start + len(t)] != t:
                                    # fallback to search
                                    start = _compute_answer_start(context, t)
                            else:
                                start = _compute_answer_start(context, t)
                            if start >= 0:
                                texts.append(t)
                                starts.append(start)
                        is_impossible = bool(qa.get("is_impossible", len(texts) == 0))
                        examples.append(
                            {
                                "id": qa.get("id") or _gen_id(question, context),
                                "title": title,
                                "context": context,
                                "question": question,
                                "answers": {"text": texts, "answer_start": starts},
                                "is_impossible": is_impossible,
                            }
                        )
        else:
            # Flat simplified train-like structure with singular 'answer'
            for item in data:
                if not isinstance(item, dict):
                    continue
                question = str(item.get("question", "")).strip()
                context = str(item.get("context", "")).strip()
                answer = item.get("answer")
                if not question or not context:
                    continue
                if answer is None:
                    # impossible (no answer provided)
                    texts = []
                    starts = []
                    is_impossible = True
                else:
                    ans_text = str(answer).strip()
                    if not ans_text:
                        # Empty string answer
                        if ignore_empty_answer and split == "train":
                            # Skip this example entirely when training to avoid noisy empties.
                            continue
                        # Keep as impossible example for non-train splits (evaluation) or when flag disabled.
                        texts = []
                        starts = []
                        is_impossible = True
                    else:
                        start_pos = _compute_answer_start(context, ans_text)
                        if start_pos == -1:
                            # Accept provided answer text even if not found in context for synthetic tests;
                            # record start as -1 to indicate unknown alignment.
                            texts = [ans_text]
                            starts = [-1]
                            is_impossible = False
                        else:
                            texts = [ans_text]
                            starts = [start_pos]
                            is_impossible = False
                examples.append(
                    {
                        "id": _gen_id(question, context),
                        "title": None,
                        "context": context,
                        "question": question,
                        "answers": {"text": texts, "answer_start": starts},
                        "is_impossible": is_impossible,
                    }
                )

        return examples

    def __getitem__(self, idx: int) -> HFStyleExample:
        return self._examples[idx]

    def __len__(self) -> int:
        return len(self._examples)

    def __iter__(self) -> Iterator[HFStyleExample]:
        for ex in self._examples:
            yield ex

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(split={self.split!r}, examples={len(self._examples)}, unique_answers={len(self._unique_answers_cache)})"

    def _check_exists(self) -> bool:
        return bool(self.dataset_path and self.dataset_path.exists())

    # ---- SQuAD v2 style accessors -------------------------------------------------
    @property
    def examples(self) -> List[HFStyleExample]:
        """Full list of SQuAD v2 style examples.

        Each example dict has keys: id, title, context, question, answers, is_impossible.
        Answers is a dict {'text': List[str], 'answer_start': List[int]} as expected by
        Hugging Face's squad_v2 format. No heavy HF dependency is required here.
        """
        return list(self._examples)

    def to_hf_dict(self) -> List[Dict[str, Any]]:  # lightweight alias
        """Alias returning examples (intended for quick serialization)."""
        return self.examples

    def to_hf_dataset(self) -> Any:  # pragma: no cover - optional convenience
        """Return a Hugging Face Dataset (requires 'datasets' installed).

        This keeps the core library free from the dependency; import is local.
        """
        try:  # local import to avoid hard dependency
            import importlib

            ds_mod = importlib.import_module("datasets")
            Dataset = ds_mod.Dataset
        except Exception as exc:
            raise RuntimeError(
                "The 'datasets' package is required for to_hf_dataset(); install with 'pip install datasets'."
            ) from exc
        return Dataset.from_list(self._examples)


# ----------------------------------------------------------------------------
# Convenience loader mimicking Hugging Face squad_v2 DatasetDict structure.
# ----------------------------------------------------------------------------
def load_ua_squad_v2(
    root: Path | str = Path("./data/ua_squad"),
    *,
    download: bool = True,
    force_download: bool = False,
    features: Any | None = None,
) -> Any:
    """Load UA-SQuAD splits and return a ``datasets.DatasetDict`` matching squad_v2 shape.

    Parameters
    ----------
    root : Path | str
        Root directory where ``train.json`` / ``val.json`` (or fallbacks) reside / will be downloaded.
    download : bool
        Whether to download missing splits.
    force_download : bool
        Re-download even if local files exist.
    features : Optional[datasets.Features]
        Custom features to cast onto the resulting datasets. If omitted a default
        SQuAD v2 style schema is applied.

    Returns
    -------
    datasets.DatasetDict
        With keys ``train`` and ``validation`` each exposing columns:
        id, title, context, question, answers{"text": list[str], "answer_start": list[int]}, is_impossible.
    """
    try:  # local import to avoid hard dependency
        import importlib

        ds_mod = importlib.import_module("datasets")
        DatasetDict = ds_mod.DatasetDict
        Features = ds_mod.Features
        Sequence = ds_mod.Sequence
        Value = ds_mod.Value
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise RuntimeError(
            "The 'datasets' package is required for load_ua_squad_v2(); install with 'uv add datasets'."
        ) from exc

    root = Path(root)
    train_ds = UaSquadDataset(
        root=root, split="train", download=download, force_download=force_download
    ).to_hf_dataset()
    val_ds = UaSquadDataset(
        root=root, split="val", download=download, force_download=force_download
    ).to_hf_dataset()

    if features is None:
        features = Features(
            {
                "id": Value("string"),
                "title": Value("string"),
                "context": Value("string"),
                "question": Value("string"),
                "answers": {
                    "text": Sequence(Value("string")),
                    "answer_start": Sequence(Value("int32")),
                },
                "is_impossible": Value("bool"),
            }
        )

    train_ds = train_ds.cast(features)
    val_ds = val_ds.cast(features)
    return DatasetDict({"train": train_ds, "validation": val_ds})
