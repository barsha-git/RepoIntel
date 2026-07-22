class Embedder:
    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.model_name = model_name

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[float(len(text))] for text in texts]
