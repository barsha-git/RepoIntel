from pathlib import Path
from urllib.parse import urlparse
from app.models.repository import Repository
from app.core.exception import InvalidRepositoryURLError
from app.core.config import settings


class RepositoryService:
    """Manage Git repositories."""

    def parse_github_url(self, url: str) -> Repository:
        """
        Parse and normalize a GitHub repository URL.

        Example:
            https://github.com/langchain-ai/langchain.git

        Returns:
            Repository
        """

        parsed = urlparse(url)

        # Validate domain
        if parsed.netloc != "github.com":
            raise InvalidRepositoryURLError(
                "Only GitHub repositories are supported."
            )

        # Remove leading/trailing slashes
        path = parsed.path.strip("/")

        parts = path.split("/")

        if len(parts) < 2:
            raise InvalidRepositoryURLError(
                "Invalid GitHub repository URL."
            )

        owner = parts[0]
        repo_name = parts[1]

        # Normalize ".git"
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        local_path = (
            Path(settings.STORAGE_PATH)
            / "repositories"
            / owner
            / repo_name
        )

        return Repository(
            Owner=owner,
            repo_name=repo_name,
            url=url,
            local_path=local_path,
        )


    def repository_exists(self, repository: Repository) -> bool:
        ...

    def get_local_path(self, repository: Repository):
        ...

    def clone_repository(self, repository: Repository):
        ...

    def update_repository(self, repository: Repository):
        ...

    def delete_repository(self, repository: Repository):
        ...
