"""Application logging configuration."""

from loguru import logger

from app.core.config import settings

# Remove the default Loguru handler
logger.remove()

# Add a new console handler
logger.add(
    sink=lambda message: print(message, end=""),
    level=settings.LOG_LEVEL,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level:<8}</level> | "
        "{message}"
    ),
)
