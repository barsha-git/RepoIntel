"""Prompt used to rewrite follow-up questions."""

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)


CONTEXTUALIZE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Given the conversation history and the latest user question,
rewrite the latest question into a standalone question.

Do NOT answer the question.

Only rewrite it if necessary.

Otherwise return it unchanged.
""",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)