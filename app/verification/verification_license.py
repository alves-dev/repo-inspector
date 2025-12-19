from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult, Severity, InspectorConfig
from app.verification.verification import VerificationInterface


class RepositoryLicenseVerification(VerificationInterface):
    KEY = 'git.repository.license'
    RULE_DESCRIPTION = "Verifica se existe uma licença para repos públicos"
    SEVERITY = Severity.WARNING

    PASSED = RepoVerificationResult.passed(
        KEY,
        RULE_DESCRIPTION,
        SEVERITY
    )

    @classmethod
    def verify(cls, repository: Repository, config: InspectorConfig) -> RepoVerificationResult:
        repo: dict = GithubClient.get_repo_by_url(repository.url)
        repo_license = repo.get('license', '')

        if repository.private:
            return cls.PASSED

        if repo_license is None:
            return RepoVerificationResult.failure(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY,
                "Sem licença."
            )

        return cls.PASSED
