from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult
from app.verification.verification import VerificationInterface


class RepositoryBranchVerification(VerificationInterface):
    KEY = 'git.repository.branch.default'
    DESCRIPTION = "Verifica se a branch default é a 'main'"
    DEFAULT= 'main'

    PASSED = [RepoVerificationResult.of_passed(KEY, '')]

    @classmethod
    def verify(cls, repository: Repository) -> list[RepoVerificationResult]:
        repo: dict = GithubClient.get_repo_by_url(repository.url)
        default_branch = repo.get('default_branch', "")

        if default_branch == cls.DEFAULT:
            return cls.PASSED

        return [RepoVerificationResult.of_failure(cls.KEY, "Branch default não é a 'main'")]
