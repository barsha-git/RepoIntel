"""Application logging configuration."""

from loguru import logger

from app.core.config import settings

# Remove the default Loguru handler
logger.remove()

# Add a new console handler
logger.add(
    sink=lambda message: print(message, end=""),
    level=settings.log_level,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level:<8}</level> | "
        "{message}"
    ),
)

# Expose the configured logger
_all_ = ["logger"]