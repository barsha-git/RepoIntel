"""Chat model service."""

from langchain_core.language_models import BaseChatModel
from langchain_groq import ChatGroq

from app.core.config import settings
from app.core.logging import logger


class ChatModelService:
    """Manage chat language models."""

    def __init__(self) -> None:
        """Initialize the chat model."""

        self._model = self._load_model()

    @property
    def model(self) -> BaseChatModel:
        """
        Return the configured chat model.
        """

        return self._model

    def _load_model(self) -> BaseChatModel:
        """
        Load the configured chat model.
        """

        logger.info(
            "Loading {} chat model...",
            settings.LLM_PROVIDERS,
        )

        match settings.LLM_PROVIDERS.lower():

            case "groq":

                model = ChatGroq(
                    model=settings.LLM_MODEL_NAME,
                    temperature=settings.LLM_MODEL_TEMPERATURE,
                    max_tokens=settings.LLM_MODEL_MAX_TOKENS,
                    api_key=settings.GROQ_API_KEY,
                )

            case _:

                raise ValueError(
                    f"Unsupported provider: {settings.LLM_PROVIDERS}"
                )

        logger.success(
            "{} loaded successfully.",
            settings.LLM_MODEL_NAME,
        )

        return model

    def get_model_name(self) -> str:
        """
        Return the configured model name.
        """

        return settings.LLM_MODEL_NAME

    def get_provider(self) -> str:
        """
        Return the configured provider.
        """

        return settings.LLM_PROVIDERS
