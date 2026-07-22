from pathlib import Path


class RepositoryLoader:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def load(self) -> list[Path]:
        return [p for p in self.root.rglob("*") if p.is_file()]
