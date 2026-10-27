import hashlib
import re
from dataclasses import dataclass
from pathlib import PurePath
from typing import Iterable

ALLOWED_EXTENSIONS = {".csv", ".json", ".jsonl"}
MAX_FILE_BYTES = 25 * 1024 * 1024


@dataclass(frozen=True)
class FileManifest:
    file_name: str
    size_bytes: int
    sha256: str


def validate_file_metadata(file_name: str, size_bytes: int) -> str:
    safe_name = PurePath(file_name).name
    if safe_name != file_name or file_name in {"", ".", ".."}:
        raise ValueError("File name must not contain a path.")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", file_name):
        raise ValueError("File name contains unsupported characters.")
    if PurePath(file_name).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("File type is not allowed.")
    if size_bytes < 0 or size_bytes > MAX_FILE_BYTES:
        raise ValueError("File size is outside the allowed limit.")
    return file_name


def build_manifest(file_name: str, content: bytes) -> FileManifest:
    validate_file_metadata(file_name, len(content))
    return FileManifest(file_name, len(content), hashlib.sha256(content).hexdigest())


def check_required_columns(columns: Iterable[str], required: Iterable[str]) -> None:
    available = {c.strip().lower() for c in columns}
    missing = {c.lower() for c in required} - available
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
