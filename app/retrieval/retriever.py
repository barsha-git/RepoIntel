class Retriever:
    def __init__(self, store):
        self.store = store

    def search(self, query: str) -> list[dict]:
        return self.store.search(query)
