class VectorStore:
    def __init__(self):
        self.documents: list[dict] = []

    def add(self, document: dict) -> None:
        self.documents.append(document)

    def search(self, query: str) -> list[dict]:
        return [doc for doc in self.documents if query.lower() in str(doc).lower()]
