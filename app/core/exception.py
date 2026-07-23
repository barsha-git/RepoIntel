class RepositoryError(Exception):
    """Base exception for repository-related errors."""


class InvalidRepositoryURLError(RepositoryError):
    """Raised when a GitHub repository URL is invalid."""

class RepositoryNotFoundError(RepositoryError):
    """Raised when a GitHub repository is not found."""

class RepositoryCloneError(RepositoryError):
    """Raised when cloning a GitHub repository fails."""

class RepositoryAlreadyExistsError(RepositoryError):
    """Raised when a repository already exists locally."""

class RepositoryUpdateError(RepositoryError):
    """Raised when updating a repository fails."""