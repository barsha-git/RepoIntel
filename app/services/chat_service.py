class ChatService:
    def __init__(self, chain):
        self.chain = chain

    def ask(self, question: str) -> str:
        return self.chain.answer(question)
