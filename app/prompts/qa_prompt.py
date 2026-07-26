"""Prompt used for repository question answering."""

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)

from app.prompts.SystemPrompt import SYSTEM_PROMPT


QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_PROMPT
            + """

Use the retrieved repository context below to answer the user's question.

<context>
{context}
</context>

When possible:

- Mention the relevant file names.
- Explain the flow between functions or classes.
- If multiple files are involved, explain their relationship.
- If the context is insufficient, say so explicitly.
""",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)