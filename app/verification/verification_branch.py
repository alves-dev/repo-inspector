from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult, Severity, InspectorConfig
from app.verification.verification import VerificationInterface


class RepositoryBranchVerification(VerificationInterface):
    KEY = 'git.repository.branch.default'
    RULE_DESCRIPTION = "Verifica se a branch default é a 'main'"
    SEVERITY = Severity.ERROR

    DEFAULT = 'main'

    @classmethod
    def verify(cls, repository: Repository, config: InspectorConfig) -> RepoVerificationResult:
        repo: dict = GithubClient.get_repo_by_url(repository.url)
        default_branch = repo.get('default_branch', "")

        if default_branch == cls.DEFAULT:
            return RepoVerificationResult.passed(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY
            )

        return RepoVerificationResult.failure(
            cls.KEY,
            cls.RULE_DESCRIPTION,
            cls.SEVERITY,
            "Branch default não é a 'main'"
        )
