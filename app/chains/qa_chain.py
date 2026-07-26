"""Question Answer Chain."""

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable

from app.prompts import qa_prompt


class QuestionAnswerChain:
    """
    Build the repository question-answering chain.

    This chain receives:
        - retrieved documents
        - chat history
        - user question

    and produces a final answer.
    """

    def __init__(
        self,
        llm: BaseChatModel,
    ) -> None:
        self._llm = llm

    def create(self) -> Runnable:
        """
        Create the QA chain.
        """

        return create_stuff_documents_chain(
            llm=self._llm,
            prompt=qa_prompt.QA_PROMPT,
        )