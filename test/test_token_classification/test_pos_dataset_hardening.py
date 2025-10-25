from pathlib import Path

import pytest

from ua_datasets.token_classification.part_of_speech import (
    MovaInstitutePOSDataset,
    ParseError,
)


@pytest.fixture
def tmp_dataset_root(tmp_path: Path) -> Path:
    return tmp_path


def _write(root: Path, name: str, content: str) -> None:
    (root / name).write_text(content, encoding="utf8")


def test_final_sentence_without_trailing_newline(tmp_dataset_root: Path) -> None:
    content = "1\tToken\t_\tNOUN\n"  # no trailing blank line
    _write(tmp_dataset_root, "final.conllu.txt", content)
    ds: MovaInstitutePOSDataset = MovaInstitutePOSDataset(
        root=tmp_dataset_root, download=False, file_name="final.conllu.txt"
    )
    assert len(ds) == 1
    assert ds[0][0] == ["Token"]


def test_comments_and_blank_lines(tmp_dataset_root: Path) -> None:
    content = (
        "# sent 1\n"
        "1\tA\t_\tDET\n"
        "2\tcat\t_\tNOUN\n"
        "\n"
        "# sent 2\n"
        "1\tSleeps\t_\tVERB\n"
        "2\tquietly\t_\tADV\n"
    )
    _write(tmp_dataset_root, "comments.conllu.txt", content)
    ds: MovaInstitutePOSDataset = MovaInstitutePOSDataset(
        root=tmp_dataset_root, download=False, file_name="comments.conllu.txt"
    )
    assert len(ds) == 2
    assert ds[0][0] == ["A", "cat"]


def test_multiword_tokens_ignored(tmp_dataset_root: Path) -> None:
    content = (
        "1\tI\t_\tPRON\n"
        "2-3\tgo+ing\t_\t_\n"  # multiword range
        "2\tam\t_\tAUX\n"
        "3\tgoing\t_\tVERB\n"
        "4\thome\t_\tNOUN\n"
        "\n"
    )
    _write(tmp_dataset_root, "mwt.conllu.txt", content)
    ds: MovaInstitutePOSDataset = MovaInstitutePOSDataset(
        root=tmp_dataset_root, download=False, file_name="mwt.conllu.txt"
    )
    tokens, tags = ds[0]
    assert tokens == ["I", "am", "going", "home"]
    assert tags == ["PRON", "AUX", "VERB", "NOUN"]


def test_malformed_lines_ignored(tmp_dataset_root: Path) -> None:
    content = "1\tOk\t_\tINTJ\nBADLINE WITHOUT TABS\n2\tthen\t_\tADV\n\n"
    _write(tmp_dataset_root, "bad.conllu.txt", content)
    ds: MovaInstitutePOSDataset = MovaInstitutePOSDataset(
        root=tmp_dataset_root, download=False, file_name="bad.conllu.txt"
    )
    tokens, tags = ds[0]
    assert tokens == ["Ok", "then"]
    assert tags == ["INTJ", "ADV"]


def test_empty_file_raises_parse_error(tmp_dataset_root: Path) -> None:
    _write(tmp_dataset_root, "empty.conllu.txt", "")
    with pytest.raises(ParseError):
        MovaInstitutePOSDataset(root=tmp_dataset_root, download=False, file_name="empty.conllu.txt")


def test_label_frequencies(tmp_dataset_root: Path) -> None:
    content = "1\tHello\t_\tINTJ\n2\tworld\t_\tNOUN\n\n1\tworld\t_\tNOUN\n2\tagain\t_\tADV\n\n"
    _write(tmp_dataset_root, "freq.conllu.txt", content)
    ds: MovaInstitutePOSDataset = MovaInstitutePOSDataset(
        root=tmp_dataset_root, download=False, file_name="freq.conllu.txt"
    )
    freqs = ds.label_frequencies()
    assert freqs["NOUN"] == 2
    assert freqs["INTJ"] == 1
    assert freqs["ADV"] == 1
    # unique_labels still consistent
    assert ds.unique_labels == {"INTJ", "NOUN", "ADV"}
