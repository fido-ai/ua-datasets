"""Shared internal utilities (network + atomic file helpers).

This consolidates retrying download logic and atomic write operations used by
multiple dataset loaders.

"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from time import sleep
from typing import Any, Callable, Optional
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

__all__ = [
    "DownloadFailure",
    "atomic_write_text",
    "download_text_with_retries",
]


class DownloadFailure(RuntimeError):
    """Raised when a download ultimately fails after retries."""


def download_text_with_retries(
    url: str,
    *,
    timeout: int = 15,
    max_retries: int = 3,
    expected_sha256: str | None = None,
    backoff_factor: float = 0.5,
    validate: Optional[Callable[[str], bool]] = None,
    opener: Callable[..., Any] = urlopen,
    show_progress: bool = False,
    chunk_size: int = 8192,
) -> str:
    """Download URL returning decoded UTF-8 text with retries & optional integrity.

    Enhanced with an optional streaming progress bar (stdout) using only the
    standard library to preserve the project's minimal dependency footprint.

    Parameters
    ----------
    url : str
        Resource to fetch (HTTP/HTTPS).
    timeout : int
        Per-attempt timeout (seconds).
    max_retries : int
        Maximum number of attempts before failing.
    expected_sha256 : str | None
        If provided, the hex digest must match the downloaded bytes.
    backoff_factor : float
        Linear backoff factor (sleep = factor * attempt_number).
    validate : Callable[[str], bool] | None
        Optional predicate applied to decoded text; must return True for success.
    opener : Callable[..., Any]
        Function used to open the URL (injected for test monkeypatching).
    show_progress : bool
        If True, prints a simple ASCII progress indicator while streaming.
    chunk_size : int
        Byte size for streaming chunks when show_progress is enabled.
    """
    attempt = 0
    last_exc: Exception | None = None
    while attempt < max_retries:
        attempt += 1
        try:
            # Use provided opener (enables test monkeypatching at call sites)
            with opener(url, timeout=timeout) as resp:  # nosec - caller controls domain
                if show_progress:
                    # Attempt to read content length for percentage; fallback to 0 (unknown)
                    try:
                        total_size = int(getattr(resp, "headers", {}).get("Content-Length", "0"))
                    except Exception:
                        total_size = 0
                    downloaded = 0
                    buf = bytearray()
                    while True:
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        buf.extend(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            pct = downloaded / total_size * 100
                            bar_width = 30
                            filled = int(bar_width * downloaded / total_size)
                            bar = "#" * filled + "-" * (bar_width - filled)
                            print(
                                f"\rDownloading {url} [{bar}] {pct:5.1f}% ({downloaded}/{total_size} bytes)",
                                end="",
                                flush=True,
                            )
                        else:
                            print(f"\rDownloading {url} {downloaded} bytes", end="", flush=True)
                    data = bytes(buf)
                    # Ensure newline after completion for clean subsequent output
                    print()
                else:
                    data = resp.read()
            if expected_sha256 is not None:
                digest = sha256(data).hexdigest()
                if digest.lower() != expected_sha256.lower():
                    raise DownloadFailure(
                        f"SHA256 mismatch for {url}: expected {expected_sha256} got {digest}"
                    )
            text = data.decode("utf8")
            if not text.strip():
                raise DownloadFailure("Downloaded content empty/whitespace.")
            if validate and not validate(text):
                raise DownloadFailure("Validation predicate rejected content.")
            return text
        except (HTTPError, URLError, TimeoutError, DownloadFailure) as exc:
            last_exc = exc
            if attempt < max_retries:
                sleep(backoff_factor * attempt)
            else:
                break
        except UnicodeDecodeError as exc:
            last_exc = exc
            break
        except Exception as exc:  # unknown fatal
            last_exc = exc
            break
    raise DownloadFailure(f"Failed to download {url} after {max_retries} attempts: {last_exc}")


def atomic_write_text(path: Path, text: str, *, encoding: str = "utf8") -> None:
    """Write text atomically by first writing to a temporary sibling file.

    Ensures readers do not observe a partially written file.
    """
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding=encoding)
    tmp.replace(path)
