from app.config.setting import setting
from app.github.client import GithubClient
from app.github.models import Repository
from app.verification.model import RepoVerificationResult
from app.verification.verification import VerificationInterface


class RepositoryTopicsVerification(VerificationInterface):
    KEY = 'git.repository.topics'
    DESCRIPTION = "Verifica os topics"

    PASSED = [RepoVerificationResult.of_passed(KEY, '')]

    @classmethod
    def verify(cls, repository: Repository) -> list[RepoVerificationResult]:
        repo: dict = GithubClient.get_repo_by_url(repository.url)
        topics = repo.get('topics', [])

        if not topics:
            return [RepoVerificationResult.of_failure(cls.KEY, 'Nenhum topic definido')]

        accepted = setting.GITHUB_TOPICS
        missing = set(topics) - set(accepted)

        if missing:
            return [RepoVerificationResult.of_failure(cls.KEY, f"Topics não permitidos: {', '.join(missing)}")]

        return cls.PASSED
