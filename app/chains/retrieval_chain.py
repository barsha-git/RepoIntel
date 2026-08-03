"""Retrieval chain."""

from langchain_classic.chains import create_retrieval_chain
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable


class RetrievalChain:

    def create(
        self,
        retriever: BaseRetriever,
        qa_chain: Runnable,
    ) -> Runnable:

        return create_retrieval_chain(
            retriever=retriever,
            combine_docs_chain=qa_chain,
        )