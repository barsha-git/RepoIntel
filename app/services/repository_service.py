from pathlib import Path
import shutil
from urllib.parse import urlparse
from app.models.repository import Repository
from app.core.exception import InvalidRepositoryURLError, RepositoryCloneError, RepositoryAlreadyExistsError, RepositoryNotFoundError, RepositoryUpdateError    
from app.core.config import settings
from git import Repo, GitCommandError
from app.core.logging import logger


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
        """Check if the repository exists locally by checking if the local path exists and is a directory."""
        return (
            repository.local_path.exists() 
            and (repository.local_path / ".git").exists()
        )

    def clone_repository(self, repository: Repository) -> Repository:
        """Clone a GitHub repository into local storage."""

        if self.repository_exists(repository):
            raise RepositoryAlreadyExistsError(
                f"Repository '{repository.Owner}/{repository.repo_name}' already exists."
            )

        repository.local_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:
            Repo.clone_from(
                repository.url,
                repository.local_path,
            )
        except GitCommandError as exc:
            raise RepositoryCloneError(
                f"Failed to clone repository: {repository.url}"
            ) from exc

        return repository

    def update_repository(self, repository: Repository) -> Repository:
        """Pull the latest changes from the remote repository."""

        if not self.repository_exists(repository):
            raise RepositoryNotFoundError(
                f"Repository '{repository.Owner}/{repository.repo_name}' does not exist."
            )

        try:
            repo = Repo(repository.local_path)

            logger.info(
                "Updating repository: {}/{}",
                repository.Owner,
                repository.repo_name,
            )

            repo.remotes.origin.pull()

            logger.success(
                "Repository updated successfully."
            )

            return repository

        except GitCommandError as exc:
            logger.exception("Repository update failed.")

            raise RepositoryUpdateError(
                f"Failed to update repository '{repository.repo_name}'."
            ) from exc


    def delete_repository(self, repository: Repository) -> None:
        """Delete the local repository."""
        if not self.repository_exists(repository):
            raise RepositoryNotFoundError(
                f"Repository '{repository.Owner}/{repository.repo_name}' does not exist."
            )

        logger.info(
            "Deleting repository: {}/{}",
            repository.Owner,
            repository.repo_name,
        )

        shutil.rmtree(repository.local_path)

        logger.success("Repository deleted successfully.")

    def get_local_path(self, repository: Repository) -> Path:
       """Return the local filesystem path of the repository."""
       return repository.local_path

    def prepare_repository(self, url: str) -> Path: 
       repo = self.parse_github_url(url)

       if self.repository_exists(repo):
        self.update_repository(repo)
       else:
        self.clone_repository(repo)

       return repo.local_path