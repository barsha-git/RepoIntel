"""Application logging configuration."""

from loguru import logger

from app.core.config import settings
from app.models.repository import Repository
from app.services.repository_service import RepositoryService

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
logger.info("cloning repositories: {}/{}", repository.owner, repository.name)

# Expose the configured logger
_all_ = ["logger"]