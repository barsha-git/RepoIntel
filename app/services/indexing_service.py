from app.indexing.repository_loader import RepositoryLoader
from app.indexing.splitter import TextSplitter


class IndexingService:
    def __init__(self, root: str):
        self.loader = RepositoryLoader(root)
        self.splitter = TextSplitter()

    def index(self) -> list[dict]:
        files = self.loader.load()
        return [{"path": str(file)} for file in files]
