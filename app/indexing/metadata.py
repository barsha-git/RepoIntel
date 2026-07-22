from dataclasses import dataclass
from pathlib import Path


@dataclass
class DocumentMetadata:
    source: str
    path: str
    language: str | None = None
