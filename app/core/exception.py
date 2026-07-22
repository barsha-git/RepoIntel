class RepositoryError(Exception):
    """Base exception for repository-related errors."""


class InvalidRepositoryURLError(RepositoryError):
    """Raised when a GitHub repository URL is invalid."""