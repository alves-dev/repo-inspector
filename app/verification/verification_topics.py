from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult, Severity, InspectorConfig
from app.verification.verification import VerificationInterface


class RepositoryTopicsVerification(VerificationInterface):
    KEY = 'git.repository.topics'
    RULE_DESCRIPTION = "Verifica os topics"
    SEVERITY = Severity.WARNING

    @classmethod
    def verify(cls, repository: Repository, config: InspectorConfig) -> RepoVerificationResult:
        repo: dict = GithubClient.get_repo_by_url(repository.url)
        topics = repo.get('topics', [])

        if not topics:
            return RepoVerificationResult.failure(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY,
                "Nenhum topic definido"
            )

        missing = set(topics) - set(config.github_topics)

        if missing:
            return RepoVerificationResult.failure(
                cls.KEY,
                cls.RULE_DESCRIPTION,
                cls.SEVERITY,
                f"Topics não permitidos: {', '.join(missing)}"
            )

        return RepoVerificationResult.passed(
            cls.KEY,
            cls.RULE_DESCRIPTION,
            cls.SEVERITY
        )
