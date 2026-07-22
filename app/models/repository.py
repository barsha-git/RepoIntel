from dataclasses import dataclass
from pathlib import Path

@dataclass(slots=True)
class Repository:
    Owner: str
    repo_name: str
    url: str
    local_path: Path
