class QAChain:
    def __init__(self, retriever):
        self.retriever = retriever

    def answer(self, question: str) -> str:
        results = self.retriever.search(question)
        if not results:
            return "No relevant context found."
        return "\n".join(str(result) for result in results)
